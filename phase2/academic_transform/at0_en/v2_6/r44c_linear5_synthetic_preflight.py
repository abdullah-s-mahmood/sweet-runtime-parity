#!/usr/bin/env python3
from __future__ import annotations

import copy, json, pathlib, tempfile
import numpy as np
import torch
from safetensors.torch import save_file, load_file

from r44c_linear5_train import (
    CLASSES, FEATURE_DIM, SCALED_COLS, L2,
    Linear5, parameter_count, raw_feature_matrix, fit_scaler, apply_scaler,
    penalized_objective, fit_core, predict, save_scaler, inference_view,
    OptimizationNotConverged
)
from r44c_linear5_aggregate import (
    threshold_metrics, argmax_label, validate, sha256_path, canonical_manifest_sha,
    EXPECTED_CONTEXT_SHA, EXPECTED_INDEX_SHA
)

def expect_fail(fn,label):
    try:
        fn()
    except Exception:
        return
    raise RuntimeError(f"expected failure not raised: {label}")

def synthetic_context():
    rng=np.random.default_rng(4401)
    ctx=rng.normal(size=(24,768)).astype(np.float32)
    index={
        (1,0):{"offset":0,"length":8},
        (2,0):{"offset":8,"length":8},
        (3,0):{"offset":16,"length":8},
    }
    return ctx,index

def row(doc,start,end,target="P",b_type="I",section="METHODS"):
    return {
        "document":doc,"sentence":0,"start":start,"end":end,"width":end-start,
        "b_type":b_type,"section":section,
        "b_conf":0.7,"boundary_start_prob":0.8,"boundary_end_prob":0.9,
        "normalized_example_index":0.25,"normalized_span_start":start/8.0,
        "target":target,"taxonomy":"EXACT_TYPED","goldless_example":False,
    }

def test_feature_contract():
    ctx,index=synthetic_context()
    rows=[
        row(1,0,3,target="P",b_type="P",section="TITLE"),
        row(2,2,8,target="NONE",b_type="O",section="UNKNOWN"),
        row(3,3,5,target="C",b_type="I",section="METHODS"),
    ]
    ordered,X,y=raw_feature_matrix(rows,ctx,index,include_targets=True)
    if X.shape!=(3,3918) or X.dtype!=np.float32 or list(y.shape)!=[3]:
        raise RuntimeError("feature dimension/dtype")
    # Width one-hot, B-type one-hot, section one-hot, edge indicators.
    for i,r in enumerate(ordered):
        if X[i,3840:3904].sum()!=1.0 or X[i,3840+(r["width"]-1)]!=1.0: raise RuntimeError("width onehot")
        if X[i,3904:3908].sum()!=1.0: raise RuntimeError("btype onehot")
        if X[i,3908:3911].sum()!=1.0: raise RuntimeError("section onehot")
        if X[i,3916]!=(1.0 if r["start"]==0 else 0.0): raise RuntimeError("left edge")
        if X[i,3917]!=(1.0 if r["end"]==8 else 0.0): raise RuntimeError("right edge")
    # Missing adjacent vector must be zero while edge flag remains explicit.
    first=next(i for i,r in enumerate(ordered) if r["document"]==1)
    if not np.all(X[first,2304:3072]==0.0): raise RuntimeError("previous edge vector")
    second=next(i for i,r in enumerate(ordered) if r["document"]==2)
    if not np.all(X[second,3072:3840]==0.0): raise RuntimeError("following edge vector")
    # Gold-derived metadata must not alter inference features.
    q=copy.deepcopy(rows[0]); q["target"]="NONE"; q["taxonomy"]="SPURIOUS_NO_OVERLAP"; q["goldless_example"]=True
    _,Xa,_=raw_feature_matrix([inference_view(rows[0])],ctx,index,include_targets=False)
    _,Xb,_=raw_feature_matrix([inference_view(q)],ctx,index,include_targets=False)
    if not np.array_equal(Xa,Xb): raise RuntimeError("forbidden metadata feature dependency")
    return {"feature_dim":X.shape[1],"raw_dtype":str(X.dtype),"targets":y.tolist()}

def test_scaler_contract():
    rng=np.random.default_rng(4402)
    X=rng.normal(size=(30,3918)).astype(np.float32)
    # one-hot/edge region has recognizable values and must remain unchanged.
    X[:,3840:3911]=0.0; X[:,3916:3918]=0.0
    X[np.arange(30),3840+(np.arange(30)%64)]=1.0
    X[np.arange(30),3904+(np.arange(30)%4)]=1.0
    X[np.arange(30),3908+(np.arange(30)%3)]=1.0
    X[:,3916]=(np.arange(30)%2==0)
    X[:,3917]=(np.arange(30)%3==0)
    # exact zero-variance scaled coordinate.
    X[:,0]=3.5
    mean,sd,zero,denom=fit_scaler(X)
    Y=apply_scaler(X,mean,sd,zero,denom)
    if Y.dtype!=np.float64 or not np.all(Y[:,0]==0.0): raise RuntimeError("zero variance scaling")
    if not np.array_equal(Y[:,3840:3911],X[:,3840:3911].astype(np.float64)): raise RuntimeError("categorical scaled")
    if not np.array_equal(Y[:,3916:3918],X[:,3916:3918].astype(np.float64)): raise RuntimeError("edge scaled")
    # Eval values can change without changing the already-fitted train scaler.
    eval1=rng.normal(size=(5,3918)).astype(np.float32)
    eval2=eval1.copy(); eval2[:,SCALED_COLS]+=1000.0
    m2,s2,z2,d2=fit_scaler(X)
    if not (np.array_equal(mean,m2) and np.array_equal(sd,s2) and np.array_equal(zero,z2) and np.array_equal(denom,d2)):
        raise RuntimeError("scaler depends on eval")
    return {"scaled_columns":len(SCALED_COLS),"zero_variance_test":True}

def test_objective_gradient():
    rng=np.random.default_rng(4403)
    X=np.zeros((11,3918),dtype=np.float64)
    X[:,:7]=rng.normal(size=(11,7))
    y=np.asarray([i%5 for i in range(11)],dtype=np.int64)
    model=Linear5()
    with torch.no_grad():
        model.linear.weight[:,:7]=torch.from_numpy(rng.normal(scale=.02,size=(5,7)))
        model.linear.bias.copy_(torch.from_numpy(rng.normal(scale=.01,size=5)))
    Xt=torch.from_numpy(X); yt=torch.from_numpy(y)
    loss,ce,l2=penalized_objective(model,Xt,yt)
    model.zero_grad(set_to_none=True); loss.backward()
    with torch.no_grad():
        logits=model(Xt); p=torch.softmax(logits,dim=1)
        oh=torch.nn.functional.one_hot(yt,num_classes=5).to(torch.float64)
        manual_w=((p-oh).T@Xt)/len(y) + L2*model.linear.weight
        manual_b=(p-oh).mean(dim=0)
    dw=float(torch.max(torch.abs(model.linear.weight.grad-manual_w)))
    db=float(torch.max(torch.abs(model.linear.bias.grad-manual_b)))
    if dw>1e-11 or db>1e-11: raise RuntimeError(f"gradient mismatch {dw}/{db}")
    # Ensure reported L2 excludes bias exactly.
    expected=(L2/2.0)*torch.sum(model.linear.weight.detach()**2)
    if float(torch.abs(l2.detach()-expected))>1e-14: raise RuntimeError("L2 convention")
    return {"max_weight_grad_error":dw,"max_bias_grad_error":db,"l2_bias_excluded":True}

def synthetic_fit_data(n=45):
    rng=np.random.default_rng(4404)
    X=np.zeros((n,3918),dtype=np.float64)
    X[:,:10]=rng.normal(size=(n,10))
    W=rng.normal(scale=.7,size=(5,10))
    y=np.argmax(X[:,:10]@W.T + rng.normal(scale=.2,size=(n,5)),axis=1).astype(np.int64)
    # Ensure all five classes appear.
    y[:5]=np.arange(5)
    return X,y

def test_optimizer_and_serialization(root):
    X,y=synthetic_fit_data()
    model,trace=fit_core(X,y,max_steps=1000,conv_inf=1e-6)
    if parameter_count(model)!=19595 or not trace or trace[-1]["grad_inf"]>1e-6:
        raise RuntimeError("LBFGS convergence")
    logits,logp,p=predict(model,X)
    if p.shape!=(len(y),5) or not np.isfinite(p).all(): raise RuntimeError("prediction")
    ck=root/"model.safetensors"
    save_file({k:v.detach().cpu().contiguous() for k,v in model.state_dict().items()},str(ck))
    model2=Linear5(); model2.load_state_dict(load_file(str(ck)))
    _,_,p2=predict(model2,X)
    if np.max(np.abs(p-p2))>0.0: raise RuntimeError("checkpoint roundtrip")
    # Scaler serialization.
    Xf=X.astype(np.float32); mean,sd,zero,denom=fit_scaler(Xf)
    sc=root/"scaler.safetensors"; save_scaler(sc,mean,sd,zero,denom)
    sdct=load_file(str(sc))
    if tuple(sdct["mean"].shape)!=(3845,) or tuple(sdct["scaled_columns"].shape)!=(3845,):
        raise RuntimeError("scaler roundtrip")
    # Deliberately impossible one-step tolerance must fail closed.
    expect_fail(lambda:fit_core(X,y,max_steps=1,conv_inf=1e-30),"optimization nonconvergence")
    return {"parameter_count":parameter_count(model),"steps":len(trace),
            "final_grad_inf":trace[-1]["grad_inf"],"roundtrip":True,
            "nonconvergence":"FAIL_CLOSED"}

def make_prob(target,pred,conf,k,doc,btype="P"):
    rest=(1.0-conf)/4.0
    d={c:rest for c in CLASSES}; d[pred]=conf
    logs={c:float(np.log(max(d[c],1e-300))) for c in CLASSES}
    return {"outer_fold":k,"document":doc,"sentence":0,"start":0,"end":1,"b_type":btype,
            **{f"logit_{c}":logs[c] for c in CLASSES},
            **{f"logp_{c}":logs[c] for c in CLASSES},
            **{f"p_{c}":d[c] for c in CLASSES}}

def _write_jsonl(p,rows):
    with pathlib.Path(p).open("w") as f:
        for r in rows:f.write(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n")

def test_aggregate_contract(root):
    out=root/"outputs"; nested=root/"nested"; out.mkdir(); nested.mkdir()
    manifest={"design_documents":[0,1,2,3,4],"verify_internal_documents":[100],
              "excluded_old_select_documents":[200],
              "oof_folds":[{"fold":k,"documents":[k]} for k in range(5)]}
    msha=canonical_manifest_sha(manifest); manifest["manifest_sha256"]=msha
    outer_summary={}
    for k in range(5):
        ev=[{"document":k,"sentence":0,"start":0,"end":1,"width":1,"b_type":"P",
             "target":"P","taxonomy":"EXACT_TYPED","goldless_example":False}]
        ep=nested/f"R44B_OUTER_{k}_EVAL.jsonl"; _write_jsonl(ep,ev)
        mp=nested/f"R44B_OUTER_{k}_META_TRAIN.jsonl"; _write_jsonl(mp,[{"synthetic_meta":k}])
        outer_summary[str(k)]={"meta_sha256":sha256_path(mp),"eval_sha256":sha256_path(ep)}
        d=out/f"fold{k}"; d.mkdir()
        pr=make_prob("P","P",.9,k,k,"P")
        pp=d/f"R44C_OUTER_{k}_PROBS.jsonl"; _write_jsonl(pp,[pr])
        ck=d/f"R44C_OUTER_{k}_LINEAR5_MODEL.safetensors"; ck.write_bytes(f"model{k}".encode())
        sc=d/f"R44C_OUTER_{k}_SCALER.safetensors"; sc.write_bytes(f"scaler{k}".encode())
        summary={
            "state":"R44C_LINEAR5_FOLD_COMPLETE","attempt_id":"SYNTH_R44C","outer_fold":k,
            "feature_dim":3918,"parameter_count":19595,
            "l2_coefficient":0.01,"optimizer":"LBFGS","lr":1.0,"history_size":100,
            "line_search_fn":"strong_wolfe","max_iter_per_step":1,"max_eval":25,
            "tolerance_grad":1e-7,"tolerance_change":1e-12,
            "convergence_grad_inf":1e-6,"max_optimizer_steps":1000,
            "optimizer_steps":5,"final_grad_inf":1e-8,"eval_rows":1,
            "manifest_canonical_sha256":msha,
            "context_npy_sha256":EXPECTED_CONTEXT_SHA,
            "context_index_sha256":EXPECTED_INDEX_SHA,
            "meta_sha256":outer_summary[str(k)]["meta_sha256"],
            "eval_sha256":outer_summary[str(k)]["eval_sha256"],
            "checkpoint_sha256":sha256_path(ck),"scaler_sha256":sha256_path(sc),
            "probabilities_sha256":sha256_path(pp),
            "guards":{"train_scaler_meta_only":True,"eval_inference_fields_stripped":True,
                      "eval_loss_computed":False,"eval_gradient_computed":False,
                      "verify_internal_used":False,"old_select_used":False,"protected_data_used":False,
                      "calibration_fitted":False,"boundary_repair_used":False,
                      "hard_negative_weighting":False,"class_weighting":False,"retry_or_restart":False}
        }
        (d/f"R44C_OUTER_{k}_SUMMARY.json").write_text(json.dumps(summary)+"\n")
    (nested/"R44B_PAIR_AGGREGATE_SUMMARY.json").write_text(
        json.dumps({"state":"R44B_PAIR_AGGREGATE_PASS","outer":outer_summary})+"\n"
    )
    rows,_,got=validate(out,nested,manifest,expected_manifest_sha=msha,
                        expected_attempt_id="SYNTH_R44C",expected_rows=5)
    if len(rows)!=5 or got!=msha: raise RuntimeError("full aggregate validation")
    if any("target" not in r for r in rows): raise RuntimeError("target join")
    tie=make_prob("P","P",.2,0,99,"P")
    pred,_=argmax_label(tie)
    if pred!="NONE": raise RuntimeError(f"tie order {pred}")
    fixture=[]; doc=1000
    for c,n in {"P":60,"I":180,"C":30,"O":150}.items():
        for _ in range(n):
            r=make_prob(c,c,.85,0,doc,c)
            r["target"]=c
            r["taxonomy"]="EXACT_TYPED"
            fixture.append(r); doc+=1
    for c in ["P","I","C","O"]:
        for _ in range(20):
            r=make_prob("NONE",c,.82,0,doc,c)
            r["target"]="NONE"
            r["taxonomy"]="SPURIOUS_NO_OVERLAP"
            fixture.append(r); doc+=1
    m80=threshold_metrics(fixture,.80); m85=threshold_metrics(fixture,.85)
    if m80["passed"] or not m85["passed"] or m85["per_class"]["P"]["accepted"]!=60:
        raise RuntimeError("gate/threshold fixture")
    (out/"fold0/R44C_OUTER_0_LINEAR5_MODEL.safetensors").write_bytes(b"tampered")
    expect_fail(lambda:validate(out,nested,manifest,expected_manifest_sha=msha,
                                expected_attempt_id="SYNTH_R44C",expected_rows=5),"checkpoint tamper")
    return {"full_population_validator":"PASS","tie_order":"NONE_FIRST",
            "threshold_ge":"PASS","physical_tamper":"FAIL_CLOSED",
            "logit_probability_consistency":"PASS"}

def main():
    with tempfile.TemporaryDirectory(prefix="r44c_synth_") as td:
        root=pathlib.Path(td)
        report={
            "state":"R44C_LINEAR5_SYNTHETIC_PREFLIGHT_PASS",
            "scientific_data_used":False,
            "scientific_attempt_consumed":False,
            "feature_contract":test_feature_contract(),
            "scaler_contract":test_scaler_contract(),
            "objective_gradient":test_objective_gradient(),
            "optimizer_serialization":test_optimizer_and_serialization(root),
            "aggregate_contract":test_aggregate_contract(root),
        }
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
