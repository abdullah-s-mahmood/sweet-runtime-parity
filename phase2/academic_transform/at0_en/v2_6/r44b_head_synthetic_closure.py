#!/usr/bin/env python3
from __future__ import annotations

import copy, json, math, pathlib, tempfile
import numpy as np
import torch

from r44b_head_train import (
    feature_tensors, feature_fingerprint, fit_head, predict, build_model,
    EPOCHS, BATCH_SIZE, FEATURE_ALLOWLIST
)
from r44b_head_aggregate import (
    threshold_metrics, choose_lowest_passing, decide, probvec,
    require_exactly_one, ensure_unique_rows, validate_complete,
    sha256_path, canonical_manifest_sha, GOLD_DENOMS
)

CLASSES=["NONE","P","I","C","O"]

def mkprob(target,pred,conf,outer=0,doc=1,sent=0,start=0,end=1,b_type="P"):
    rest=(1.0-conf)/4.0
    probs={c:rest for c in CLASSES}
    probs[pred]=conf
    return {
        "outer_fold":outer,"head":"J0","document":doc,"sentence":sent,
        "start":start,"end":end,"b_type":b_type,"target":target,"taxonomy":"SYNTHETIC",
        **{"p_"+c:probs[c] for c in CLASSES},
    }

def expect_raises(fn,label):
    try:
        fn()
    except Exception:
        return
    raise RuntimeError(f"expected failure not raised: {label}")

def test_feature_allowlist():
    rng=np.random.default_rng(44)
    ctx=rng.normal(size=(12,768)).astype(np.float32)
    index={(1,0):{"offset":0,"length":12}}
    r={
        "document":1,"sentence":0,"start":2,"end":5,"width":3,
        "b_type":"P","section":"METHODS","b_conf":.7,
        "boundary_start_prob":.8,"boundary_end_prob":.9,
        "normalized_example_index":.25,"normalized_span_start":.2,
        "target":"P","taxonomy":"EXACT_TYPED","goldless_example":False,
    }
    f0=feature_tensors([r],ctx,index,include_targets=False)
    q=copy.deepcopy(r)
    q["target"]="NONE"; q["taxonomy"]="SPURIOUS_NO_OVERLAP"; q["goldless_example"]=True
    f1=feature_tensors([q],ctx,index,include_targets=False)
    if feature_fingerprint(f0)!=feature_fingerprint(f1):
        raise RuntimeError("forbidden metadata changed model features")
    return {"feature_allowlist":FEATURE_ALLOWLIST,"fingerprint":feature_fingerprint(f0)}

def synthetic_tensor_batch(n=32):
    g=torch.Generator().manual_seed(44)
    vec=[torch.randn((n,768),generator=g) for _ in range(5)]
    pe=torch.tensor([(i%7)==0 for i in range(n)],dtype=torch.bool)
    ne=torch.tensor([(i%9)==0 for i in range(n)],dtype=torch.bool)
    width=torch.tensor([(i%8)+1 for i in range(n)],dtype=torch.long)
    btype=torch.tensor([i%4 for i in range(n)],dtype=torch.long)
    section=torch.tensor([i%3 for i in range(n)],dtype=torch.long)
    scalars=torch.rand((n,5),generator=g)
    y=torch.tensor([i%5 for i in range(n)],dtype=torch.long)
    return tuple(vec+[pe,ne,width,btype,section,scalars,y])

def test_optimizer_scheduler_serialization(root):
    out={}
    train=synthetic_tensor_batch(32)
    evalx=train[:-1]
    for head in ["J0","J1"]:
        d=root/head; d.mkdir()
        m0=build_model(head)
        before={k:v.detach().clone() for k,v in m0.state_dict().items()}
        model,trace,ckpt,steps=fit_head(train,head,d,EPOCHS,BATCH_SIZE)
        changed=any(not torch.equal(before[k],model.state_dict()[k]) for k in before)
        if not changed: raise RuntimeError(f"{head} optimizer made no update")
        if len(trace)!=10 or trace[-1]["global_step"]!=steps: raise RuntimeError(f"{head} schedule trace")
        if not ckpt.exists() or ckpt.stat().st_size<=0: raise RuntimeError(f"{head} checkpoint missing")
        p=predict(model,evalx)
        if p.shape!=(32,5) or not np.isfinite(p).all(): raise RuntimeError(f"{head} prediction shape")
        out[head]={"optimizer_updated":changed,"epochs":len(trace),"steps":steps,
                   "final_lr":trace[-1]["lr"],"checkpoint_bytes":ckpt.stat().st_size}
    return out

def gate_population():
    rows=[]; doc=1
    # At t=.85 every class passes precision=1 and recall >= .20.
    true_counts={"P":60,"I":180,"C":30,"O":150}
    for c,n in true_counts.items():
        for _ in range(n):
            rows.append(mkprob(c,c,.85,doc=doc,b_type=("P" if c!="P" else "I"))); doc+=1
    # False positives admitted at .80 but rejected at .85, so .80 fails.
    for c in ["P","I","C","O"]:
        for _ in range(20):
            rows.append(mkprob("NONE",c,.82,doc=doc,b_type=c)); doc+=1
    # Explicit NONE argmax rejection.
    rows.append(mkprob("NONE","NONE",.95,doc=doc)); doc+=1
    return rows

def test_gates_and_decision():
    rows=gate_population()
    m80=threshold_metrics(rows,.80)
    m85=threshold_metrics(rows,.85)
    if m80["passed"]: raise RuntimeError(".80 must fail synthetic precision fixture")
    if not m85["passed"]: raise RuntimeError(".85 must pass synthetic fixture")
    metrics,sel=choose_lowest_passing(rows)
    if sel!=.85: raise RuntimeError(f"lowest passing threshold {sel}")
    # >= comparison: every correct row has confidence exactly .85 and must be accepted.
    if m85["per_class"]["P"]["accepted"]!=60: raise RuntimeError(">= comparison not honored")
    # Type correction: P target rows were proposed as b_type I yet count as P TP.
    if m85["per_class"]["P"]["tp"]!=60: raise RuntimeError("type correction accounting")
    # Authoritative denominator preserves absent-proposal recall.
    if abs(m85["per_class"]["P"]["recall"]-(60/GOLD_DENOMS["P"]))>1e-15:
        raise RuntimeError("authoritative recall denominator")
    # Wrong-boundary / target NONE contributes FP when accepted.
    wrong=mkprob("NONE","P",.95,doc=9999,b_type="P")
    one=threshold_metrics([wrong],.95)
    if one["per_class"]["P"]["fp"]!=1: raise RuntimeError("wrong-boundary NONE accounting")
    # NONE argmax must be rejected.
    none=threshold_metrics([mkprob("NONE","NONE",.99,doc=10000)],.80)
    if none["accepted_total"]!=0: raise RuntimeError("NONE rejection")
    # All-class gate: break C while others stay.
    broken=[r for r in rows if not (r["target"]=="C" and int(r["document"])%2==0)]
    if threshold_metrics(broken,.85)["passed"]: raise RuntimeError("all-class gate")
    rep={"J0":{"selected_threshold":.85},"J1":{"selected_threshold":.85}}
    d=decide(rep)
    if d["head"]!="J0" or d["threshold"]!=.85: raise RuntimeError("J0-first precedence")
    d2=decide({"J0":{"selected_threshold":None},"J1":{"selected_threshold":.90}})
    if d2["head"]!="J1": raise RuntimeError("J1 escalation")
    d3=decide({"J0":{"selected_threshold":None},"J1":{"selected_threshold":None}})
    if d3["state"]!="NO_ARCHITECTURE_NOMINATED": raise RuntimeError("no-pass outcome")
    return {"t80_pass":m80["passed"],"t85_pass":m85["passed"],"selected":sel,
            "P_recall":m85["per_class"]["P"]["recall"],"decision":d}

def test_fail_closed_helpers():
    expect_raises(lambda:require_exactly_one([],"missing"),"missing output")
    expect_raises(lambda:require_exactly_one([1,2],"duplicate"),"duplicate output")
    r=mkprob("P","P",.9,doc=1)
    expect_raises(lambda:ensure_unique_rows([r,copy.deepcopy(r)],"dup"),"duplicate row")
    q=copy.deepcopy(r); q["p_P"]=float("nan")
    expect_raises(lambda:probvec(q),"nonfinite probability")
    z=copy.deepcopy(r); z["p_P"]=.5
    expect_raises(lambda:probvec(z),"unnormalized probability")
    return {"missing_output":"FAIL_CLOSED","duplicate_output":"FAIL_CLOSED",
            "duplicate_row":"FAIL_CLOSED","nonfinite":"FAIL_CLOSED","unnormalized":"FAIL_CLOSED"}


def _write_jsonl(p,rows):
    with pathlib.Path(p).open("w",encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n")

def test_full_completeness_validator(root):
    outputs=root/"full_outputs"; nested=root/"nested"
    outputs.mkdir(); nested.mkdir()
    manifest={
        "design_documents":[0,1,2,3,4],
        "verify_internal_documents":[100],
        "excluded_old_select_documents":[200],
        "oof_folds":[{"fold":k,"documents":[k]} for k in range(5)],
    }
    msha=canonical_manifest_sha(manifest); manifest["manifest_sha256"]=msha
    (nested/"R44B_PAIR_AGGREGATE_SUMMARY.json").write_text(json.dumps({"state":"R44B_PAIR_AGGREGATE_PASS"})+"\n")
    for k in range(5):
        ev=[{
            "fold":k,"document":k,"sentence":0,"start":0,"end":1,"width":1,
            "b_type":"P","b_conf":.7,"boundary_start_prob":.8,"boundary_end_prob":.8,
            "target":"P","taxonomy":"EXACT_TYPED","goldless_example":False,"section":"METHODS",
            "normalized_example_index":0.0,"normalized_span_start":0.0,
        }]
        _write_jsonl(nested/f"R44B_OUTER_{k}_EVAL.jsonl",ev)
        for head,params in [("J0",584631),("J1",667836)]:
            d=outputs/f"{head}_{k}"; d.mkdir()
            pr=mkprob("P","P",.9,outer=k,doc=k,b_type="P")
            pp=d/f"R44B_OUTER_{k}_{head}_PROBS.jsonl"; _write_jsonl(pp,[pr])
            ck=d/f"R44B_{head}_FINAL_MODEL.safetensors"; ck.write_bytes(f"synthetic-{head}-{k}".encode())
            summary={
                "state":"R44B_HEAD_FOLD_COMPLETE","attempt_id":"SYNTH_ATTEMPT",
                "head":head,"outer_fold":k,"seed":44,"parameter_count":params,"eval_rows":1,
                "probabilities_sha256":sha256_path(pp),"checkpoint_sha256":sha256_path(ck),
                "schedule":{"epochs":10,"batch_size":64,"optimizer":"AdamW","lr":0.001,
                            "weight_decay":0.01,"gradient_clip":1.0,
                            "scheduler":"linear_decay_no_warmup","early_stopping":False,
                            "checkpoint_selection":"FINAL_FIXED_EPOCH_ONLY","loss":"ordinary_5way_cross_entropy"},
                "guards":{"fresh_model_optimizer_scheduler_rng":True,"meta_only_optimizer_updates":True,
                          "evaluation_model_eval":True,"evaluation_no_grad":True,
                          "mechanics_state_reused":False,"verify_internal_used":False,
                          "old_select_used":False,"protected_data_used":False,
                          "threshold_evaluation_performed":False,"calibration_fitted":False,
                          "early_stopping_used":False,"checkpoint_shopping":False},
            }
            (d/f"R44B_OUTER_{k}_{head}_SUMMARY.json").write_text(json.dumps(summary)+"\n")
    heads,_,got=validate_complete(outputs,nested,manifest,
                                  expected_manifest_sha=msha,
                                  expected_attempt_id="SYNTH_ATTEMPT",
                                  expected_total_rows=5)
    if got!=msha or any(len(heads[h])!=5 for h in ["J0","J1"]):
        raise RuntimeError("synthetic full completeness validator")
    # Physical checkpoint tamper must fail closed.
    tamper=outputs/"J0_0/R44B_J0_FINAL_MODEL.safetensors"
    tamper.write_bytes(b"tampered")
    expect_raises(lambda:validate_complete(outputs,nested,manifest,
                                          expected_manifest_sha=msha,
                                          expected_attempt_id="SYNTH_ATTEMPT",
                                          expected_total_rows=5),
                  "physical checkpoint tamper")
    return {"full_population_validation":"PASS","rows_per_head":5,
            "physical_checkpoint_tamper":"FAIL_CLOSED","manifest_sha":msha}

def main():
    with tempfile.TemporaryDirectory(prefix="r44b_synth_") as td:
        root=pathlib.Path(td)
        report={
            "state":"R44B_HEAD_EXECUTOR_SYNTHETIC_CLOSURE_PASS",
            "scientific_data_used":False,
            "scientific_head_attempt_consumed":False,
            "feature_allowlist":test_feature_allowlist(),
            "optimizer_scheduler_serialization":test_optimizer_scheduler_serialization(root),
            "gate_contract":test_gates_and_decision(),
            "fail_closed":test_fail_closed_helpers(),
            "full_completeness_validator":test_full_completeness_validator(root),
            "frozen_gold_denominators":GOLD_DENOMS,
            "next_action":"FREEZE_EXECUTOR_IDENTITIES_THEN_AUTHORIZE_ONE_REAL_DEVELOPMENT_J0_J1_ATTEMPT",
        }
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
