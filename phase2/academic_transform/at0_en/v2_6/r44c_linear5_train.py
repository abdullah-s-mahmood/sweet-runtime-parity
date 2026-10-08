#!/usr/bin/env python3
from __future__ import annotations

import argparse, datetime, hashlib, json, math, pathlib, random, traceback
import numpy as np
import torch
from torch import nn
from safetensors.torch import save_file, load_file

ATTEMPT_ID="R44C_LINEAR5_L2_DEV_ATTEMPT_1"
SEED=44
CLASSES=["NONE","P","I","C","O"]
TYPES=["P","I","C","O"]
SECTIONS=["TITLE","METHODS","UNKNOWN"]
CLASS2ID={x:i for i,x in enumerate(CLASSES)}
TYPE2ID={x:i for i,x in enumerate(TYPES)}
SEC2ID={x:i for i,x in enumerate(SECTIONS)}

FEATURE_DIM=3918
CONTEXT_DIM=3840
WIDTH_START=3840
BTYPE_START=3904
SECTION_START=3908
SCALAR_START=3911
EDGE_START=3916
SCALED_COLS=np.array(list(range(0,3840))+list(range(3911,3916)),dtype=np.int64)

L2=0.01
LR=1.0
HISTORY_SIZE=100
MAX_STEPS=1000
MAX_EVAL=25
TOL_GRAD_OPT=1e-7
TOL_CHANGE=1e-12
CONVERGENCE_INF=1e-6

EXPECTED_MANIFEST_SHA="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720"
EXPECTED_R44A_SHA="6f20f12e8bcb814067f689f5acc27918b98de93e6e88dd1ebb53d7689bc1d946"
EXPECTED_BASE_SHA="3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68"
EXPECTED_DESIGN_SHA="f8b49420cb17a5cb3f67f3120f9362b5e6b15fbb148176eab20105790bab1e18"
EXPECTED_CONTEXT_SHA="6bb548884cafb2a14e19b7d691b393dcf0ab9b5cc6add14e6ab0a873be33361b"
EXPECTED_INDEX_SHA="db9a6bae51a4db38d244e9e0a98f44b5dbfb246f694db5397c6e204cd58881dd"

MODEL_FEATURE_FIELDS=[
    "document","sentence","start","end","width","b_type","section",
    "b_conf","boundary_start_prob","boundary_end_prob",
    "normalized_example_index","normalized_span_start"
]
FORBIDDEN_INFERENCE_FIELDS=["target","taxonomy","goldless_example","gold","gold_span","label","tags"]

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha256_path(p:pathlib.Path)->str:
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def sha256_text(s:str)->str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def canonical_manifest_sha(m:dict)->str:
    q=dict(m); q.pop("manifest_sha256",None)
    return sha256_text(json.dumps(q,sort_keys=True,separators=(",",":")))

def read_jsonl(p:pathlib.Path):
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]

def write_json(p:pathlib.Path,obj):
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")

def write_jsonl(p:pathlib.Path,rows):
    with p.open("w",encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n")

def finite01(v,name):
    x=float(v)
    if not math.isfinite(x) or x<0.0 or x>1.0:
        raise RuntimeError(f"{name} outside finite [0,1]: {x}")
    return x

def inference_view(r:dict)->dict:
    return {k:r[k] for k in MODEL_FEATURE_FIELDS}

def row_sort_key(r):
    return (
        int(r["document"]),int(r["sentence"]),int(r["start"]),int(r["end"]),
        TYPE2ID[str(r["b_type"])]
    )

def candidate_key(r):
    return (int(r["document"]),int(r["sentence"]),int(r["start"]),int(r["end"]),str(r["b_type"]))

def load_context(context_root:pathlib.Path):
    cp=context_root/"R44B_BASE_CONTEXT_FLOAT32.npy"
    ip=context_root/"R44B_BASE_CONTEXT_INDEX.json"
    sp=context_root/"R44B_BASE_CONTEXT_SUMMARY.json"
    s=json.loads(sp.read_text())
    if s.get("state")!="R44B_BASE_CONTEXT_CACHE_PASS": raise RuntimeError("context state")
    if s.get("base_model_sha256")!=EXPECTED_BASE_SHA or s.get("design_source_sha256")!=EXPECTED_DESIGN_SHA:
        raise RuntimeError("context source identity")
    if s.get("context_npy_sha256")!=EXPECTED_CONTEXT_SHA or s.get("index_sha256")!=EXPECTED_INDEX_SHA:
        raise RuntimeError("context declared SHA")
    if sha256_path(cp)!=EXPECTED_CONTEXT_SHA or sha256_path(ip)!=EXPECTED_INDEX_SHA:
        raise RuntimeError("context physical SHA")
    if any(bool(s.get(k)) for k in ["labels_used","verify_internal_used","old_select_used","protected_data_used"]):
        raise RuntimeError("context guard")
    ctx=np.load(cp,mmap_mode="r",allow_pickle=False)
    if ctx.shape!=(26595,768) or ctx.dtype!=np.float32 or not np.isfinite(ctx).all():
        raise RuntimeError(f"context invalid {ctx.shape}/{ctx.dtype}")
    index={}; offset=0
    for q in json.loads(ip.read_text()):
        key=(int(q["document"]),int(q["sentence"]))
        if key in index: raise RuntimeError(f"duplicate context index {key}")
        if int(q["offset"])!=offset or int(q["length"])<=0: raise RuntimeError(f"context offset {key}")
        index[key]=q; offset+=int(q["length"])
    if len(index)!=1034 or offset!=26595: raise RuntimeError("context index accounting")
    return ctx,index,s

def raw_feature_matrix(rows,ctx,index,include_targets=False):
    rows=sorted(rows,key=row_sort_key)
    X=np.zeros((len(rows),FEATURE_DIM),dtype=np.float32)
    y=np.zeros((len(rows),),dtype=np.int64) if include_targets else None
    seen=set()
    for i,r in enumerate(rows):
        ident=candidate_key(r)
        if ident in seen: raise RuntimeError(f"duplicate candidate {ident}")
        seen.add(ident)
        key=ident[:2]
        if key not in index: raise RuntimeError(f"missing context {key}")
        q=index[key]; off=int(q["offset"]); n=int(q["length"])
        s=int(r["start"]); e=int(r["end"]); w=e-s
        if not 0<=s<e<=n: raise RuntimeError(f"bounds {ident}/{n}")
        if int(r["width"])!=w or not 1<=w<=64: raise RuntimeError(f"width {ident}/{w}")
        bt=str(r["b_type"]); sec=str(r["section"])
        if bt not in TYPE2ID or sec not in SEC2ID: raise RuntimeError(f"category {ident}")
        arr=ctx[off:off+n]
        pieces=[
            np.asarray(arr[s],dtype=np.float32),
            np.asarray(arr[e-1],dtype=np.float32),
            np.asarray(arr[s:e].mean(axis=0),dtype=np.float32),
            np.zeros(768,np.float32) if s==0 else np.asarray(arr[s-1],dtype=np.float32),
            np.zeros(768,np.float32) if e==n else np.asarray(arr[e],dtype=np.float32),
        ]
        X[i,0:3840]=np.concatenate(pieces).astype(np.float32,copy=False)
        X[i,WIDTH_START+(w-1)]=1.0
        X[i,BTYPE_START+TYPE2ID[bt]]=1.0
        X[i,SECTION_START+SEC2ID[sec]]=1.0
        X[i,SCALAR_START:SCALAR_START+5]=np.asarray([
            finite01(r["b_conf"],"b_conf"),
            finite01(r["boundary_start_prob"],"boundary_start_prob"),
            finite01(r["boundary_end_prob"],"boundary_end_prob"),
            finite01(r["normalized_example_index"],"normalized_example_index"),
            finite01(r["normalized_span_start"],"normalized_span_start"),
        ],dtype=np.float32)
        X[i,EDGE_START]=1.0 if s==0 else 0.0
        X[i,EDGE_START+1]=1.0 if e==n else 0.0
        if include_targets:
            t=str(r["target"])
            if t not in CLASS2ID: raise RuntimeError(f"target {t}")
            y[i]=CLASS2ID[t]
    if X.shape[1]!=FEATURE_DIM or not np.isfinite(X).all(): raise RuntimeError("feature matrix")
    return rows,X,y

def fit_scaler(X_train_f32):
    if X_train_f32.dtype!=np.float32: raise RuntimeError("pooling/raw matrix must be float32")
    X=X_train_f32.astype(np.float64,copy=True)
    vals=X[:,SCALED_COLS]
    mean=vals.mean(axis=0,dtype=np.float64)
    sd=vals.std(axis=0,ddof=0,dtype=np.float64)
    if not np.isfinite(mean).all() or not np.isfinite(sd).all(): raise RuntimeError("nonfinite scaler")
    zero=(sd==0.0)
    denom=np.maximum(sd,1e-6)
    return mean,sd,zero,denom

def apply_scaler(X_f32,mean,sd,zero,denom):
    X=X_f32.astype(np.float64,copy=True)
    vals=(X[:,SCALED_COLS]-mean)/denom
    if np.any(zero): vals[:,zero]=0.0
    X[:,SCALED_COLS]=vals
    if X.dtype!=np.float64 or not np.isfinite(X).all(): raise RuntimeError("scaled matrix")
    return X

class Linear5(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear=nn.Linear(FEATURE_DIM,5,bias=True,dtype=torch.float64)
        with torch.no_grad():
            self.linear.weight.zero_()
            self.linear.bias.zero_()
    def forward(self,x):
        return self.linear(x)

def parameter_count(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def seed_runtime():
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)

def penalized_objective(model,X,y):
    logits=model(X)
    ce=nn.functional.cross_entropy(logits,y,reduction="mean")
    l2=(L2/2.0)*torch.sum(model.linear.weight*model.linear.weight)
    return ce+l2,ce,l2

class OptimizationNotConverged(RuntimeError): pass

def fit_core(X_np,y_np,max_steps=MAX_STEPS,conv_inf=CONVERGENCE_INF,status_cb=None):
    seed_runtime()
    model=Linear5()
    if parameter_count(model)!=19595: raise RuntimeError(f"parameter count {parameter_count(model)}")
    X=torch.from_numpy(np.asarray(X_np,dtype=np.float64))
    y=torch.from_numpy(np.asarray(y_np,dtype=np.int64))
    if X.shape!=(len(y),FEATURE_DIM): raise RuntimeError("train shape")
    opt=torch.optim.LBFGS(
        model.parameters(),lr=LR,max_iter=1,max_eval=MAX_EVAL,
        tolerance_grad=TOL_GRAD_OPT,tolerance_change=TOL_CHANGE,
        history_size=HISTORY_SIZE,line_search_fn="strong_wolfe"
    )
    trace=[]
    for step in range(1,max_steps+1):
        def closure():
            opt.zero_grad(set_to_none=True)
            loss,_,_=penalized_objective(model,X,y)
            if not torch.isfinite(loss): raise RuntimeError("nonfinite closure objective")
            loss.backward()
            if not all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters()):
                raise RuntimeError("nonfinite closure gradient")
            return loss
        opt.step(closure)
        opt.zero_grad(set_to_none=True)
        loss,ce,l2=penalized_objective(model,X,y)
        loss.backward()
        grads=[p.grad.detach().abs().max() for p in model.parameters() if p.grad is not None]
        ginf=float(torch.stack(grads).max()) if grads else 0.0
        vals={"step":step,"objective":float(loss.detach()),"ce":float(ce.detach()),
              "l2":float(l2.detach()),"grad_inf":ginf}
        if not all(math.isfinite(float(vals[k])) for k in ["objective","ce","l2","grad_inf"]):
            raise RuntimeError("nonfinite post-step diagnostic")
        trace.append(vals)
        if status_cb is not None: status_cb(vals)
        if ginf<=conv_inf:
            return model,trace
    raise OptimizationNotConverged(f"gradient infinity norm {trace[-1]['grad_inf'] if trace else None} > {conv_inf} after {max_steps} steps")

def predict(model,X_np):
    X=torch.from_numpy(np.asarray(X_np,dtype=np.float64))
    model.eval()
    with torch.no_grad():
        logits=model(X)
        logp=torch.log_softmax(logits,dim=-1)
        p=torch.softmax(logits,dim=-1)
    if logits.shape!=(len(X_np),5) or not torch.isfinite(logits).all() or not torch.isfinite(p).all():
        raise RuntimeError("prediction tensor")
    if float(torch.max(torch.abs(p.sum(dim=1)-1.0)))>1e-12: raise RuntimeError("probability normalization")
    return logits.cpu().numpy(),logp.cpu().numpy(),p.cpu().numpy()

def save_scaler(path,mean,sd,zero,denom):
    save_file({
        "mean":torch.from_numpy(mean.astype(np.float64)),
        "sd":torch.from_numpy(sd.astype(np.float64)),
        "denom":torch.from_numpy(denom.astype(np.float64)),
        "zero_mask":torch.from_numpy(zero.astype(np.uint8)),
        "scaled_columns":torch.from_numpy(SCALED_COLS.astype(np.int64)),
    },str(path))

def scientific_run(a):
    if a.attempt_id!=ATTEMPT_ID: raise RuntimeError("attempt id")
    out=a.out; out.mkdir(parents=True,exist_ok=False)
    status=out/"PROCESS_STATUS.json"
    write_json(status,{"state":"INITIALIZING","attempt_id":a.attempt_id,
                       "outer_fold":a.outer_fold,"scientific_attempt_started":False,
                       "progress_percent":0.0,"last_progress_at":now()})

    m=json.loads(a.manifest.read_text()); got=canonical_manifest_sha(m)
    if m.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA or got!=EXPECTED_MANIFEST_SHA:
        raise RuntimeError("canonical manifest")
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); oldsel=set(m["excluded_old_select_documents"])
    folds={int(q["fold"]):set(q["documents"]) for q in m["oof_folds"]}
    if len(design)!=256 or len(verify)!=64 or set(folds)!=set(range(5)) or set().union(*folds.values())!=design:
        raise RuntimeError("manifest structure")
    if design&verify or design&oldsel or verify&oldsel: raise RuntimeError("manifest isolation")

    agg=json.loads((a.nested_root/"R44B_PAIR_AGGREGATE_SUMMARY.json").read_text())
    if agg.get("state")!="R44B_PAIR_AGGREGATE_PASS" or agg.get("pair_count")!=10: raise RuntimeError("nested aggregate")
    if agg.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA or agg.get("r44a_bank_sha256")!=EXPECTED_R44A_SHA:
        raise RuntimeError("nested identity")
    if any(bool(agg.get(k)) for k in ["verify_internal_used","old_select_used","protected_data_used","head_training"]):
        raise RuntimeError("nested guard")

    k=int(a.outer_fold)
    meta_p=a.nested_root/f"R44B_OUTER_{k}_META_TRAIN.jsonl"
    eval_p=a.nested_root/f"R44B_OUTER_{k}_EVAL.jsonl"
    osum=agg["outer"][str(k)]
    if sha256_path(meta_p)!=osum["meta_sha256"] or sha256_path(eval_p)!=osum["eval_sha256"]:
        raise RuntimeError("outer bank SHA")
    meta=read_jsonl(meta_p); ev=read_jsonl(eval_p)
    if len(meta)!=int(osum["meta_candidate_rows"]) or len(ev)!=int(osum["eval_candidate_rows"]):
        raise RuntimeError("outer row counts")
    if any(int(r["document"]) in folds[k] for r in meta): raise RuntimeError("outer leakage meta")
    if any(int(r["document"]) not in folds[k] for r in ev): raise RuntimeError("outer eval docs")

    ctx,index,_=load_context(a.context_root)
    meta_sorted,Xm32,ym=raw_feature_matrix(meta,ctx,index,include_targets=True)
    eval_in=[inference_view(r) for r in ev]
    eval_sorted,Xe32,_=raw_feature_matrix(eval_in,ctx,index,include_targets=False)

    mean,sd,zero,denom=fit_scaler(Xm32)
    Xm=apply_scaler(Xm32,mean,sd,zero,denom)
    Xe=apply_scaler(Xe32,mean,sd,zero,denom)

    scaler_p=out/f"R44C_OUTER_{k}_SCALER.safetensors"
    save_scaler(scaler_p,mean,sd,zero,denom)

    write_json(status,{"state":"RUNNING","attempt_id":a.attempt_id,"outer_fold":k,
                       "scientific_attempt_started":True,"first_optimizer_update_pending":True,
                       "meta_rows":len(meta_sorted),"eval_rows":len(eval_sorted),
                       "progress_percent":0.0,"last_progress_at":now()})
    def cb(v):
        payload={"state":"RUNNING","attempt_id":a.attempt_id,"outer_fold":k,
                 "scientific_attempt_started":True,"first_optimizer_update_pending":False,
                 "current_stage":"OPTIMIZATION","optimizer_step":v["step"],
                 "max_optimizer_steps":MAX_STEPS,"objective":v["objective"],"ce":v["ce"],
                 "l2":v["l2"],"grad_inf":v["grad_inf"],
                 "progress_percent":round(90.0*min(v["step"],MAX_STEPS)/MAX_STEPS,6),
                 "last_progress_at":now()}
        write_json(status,payload)
        print("PROCESS_STATUS "+json.dumps(payload,sort_keys=True),flush=True)

    model,trace=fit_core(Xm,ym,status_cb=cb)
    ckpt=out/f"R44C_OUTER_{k}_LINEAR5_MODEL.safetensors"
    save_file({kk:vv.detach().cpu().contiguous() for kk,vv in model.state_dict().items()},str(ckpt))

    logits,logp,probs=predict(model,Xe)
    rows=[]
    for r,z,lp,p in zip(eval_sorted,logits,logp,probs):
        rows.append({
            "outer_fold":k,
            "document":int(r["document"]),"sentence":int(r["sentence"]),
            "start":int(r["start"]),"end":int(r["end"]),"b_type":str(r["b_type"]),
            **{f"logit_{c}":float(z[i]) for i,c in enumerate(CLASSES)},
            **{f"logp_{c}":float(lp[i]) for i,c in enumerate(CLASSES)},
            **{f"p_{c}":float(p[i]) for i,c in enumerate(CLASSES)},
        })
    pp=out/f"R44C_OUTER_{k}_PROBS.jsonl"; write_jsonl(pp,rows)
    final=trace[-1]
    summary={
        "state":"R44C_LINEAR5_FOLD_COMPLETE","attempt_id":a.attempt_id,"outer_fold":k,
        "scientific_attempt_started":True,
        "meta_rows":len(meta_sorted),"eval_rows":len(eval_sorted),
        "feature_dim":FEATURE_DIM,"parameter_count":parameter_count(model),
        "l2_coefficient":L2,"optimizer":"LBFGS","lr":LR,"history_size":HISTORY_SIZE,
        "line_search_fn":"strong_wolfe","max_iter_per_step":1,"max_eval":MAX_EVAL,
        "tolerance_grad":TOL_GRAD_OPT,"tolerance_change":TOL_CHANGE,
        "convergence_grad_inf":CONVERGENCE_INF,"max_optimizer_steps":MAX_STEPS,
        "optimizer_steps":len(trace),"final_objective":final["objective"],
        "final_train_ce":final["ce"],"final_l2":final["l2"],"final_grad_inf":final["grad_inf"],
        "meta_sha256":sha256_path(meta_p),"eval_sha256":sha256_path(eval_p),
        "manifest_canonical_sha256":got,
        "context_npy_sha256":EXPECTED_CONTEXT_SHA,"context_index_sha256":EXPECTED_INDEX_SHA,
        "checkpoint_sha256":sha256_path(ckpt),"scaler_sha256":sha256_path(scaler_p),
        "probabilities_sha256":sha256_path(pp),
        "guards":{
            "train_scaler_meta_only":True,"eval_inference_fields_stripped":True,
            "eval_loss_computed":False,"eval_gradient_computed":False,
            "verify_internal_used":False,"old_select_used":False,"protected_data_used":False,
            "calibration_fitted":False,"boundary_repair_used":False,
            "hard_negative_weighting":False,"class_weighting":False,
            "retry_or_restart":False,
        },
        "optimization_trace":trace,
    }
    sp=out/f"R44C_OUTER_{k}_SUMMARY.json"; write_json(sp,summary)
    write_json(status,{"state":"COMPLETED","attempt_id":a.attempt_id,"outer_fold":k,
                       "scientific_attempt_started":True,"progress_percent":100.0,
                       "optimizer_steps":len(trace),"final_grad_inf":final["grad_inf"],
                       "checkpoint_sha256":summary["checkpoint_sha256"],
                       "probabilities_sha256":summary["probabilities_sha256"],
                       "last_progress_at":now()})
    print(json.dumps(summary,indent=2,sort_keys=True))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--attempt-id",required=True)
    ap.add_argument("--nested-root",type=pathlib.Path,required=True)
    ap.add_argument("--context-root",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--outer-fold",type=int,choices=range(5),required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()
    try:
        scientific_run(a)
    except Exception as e:
        try:
            a.out.mkdir(parents=True,exist_ok=True)
            write_json(a.out/"PROCESS_STATUS.json",{
                "state":"FAILED","attempt_id":getattr(a,"attempt_id",None),
                "outer_fold":getattr(a,"outer_fold",None),"error_type":type(e).__name__,
                "error":str(e),"last_progress_at":now(),
                "traceback_tail":traceback.format_exc().splitlines()[-30:]
            })
        finally:
            raise

if __name__=="__main__":
    main()
