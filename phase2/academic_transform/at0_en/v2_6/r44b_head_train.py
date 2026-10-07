#!/usr/bin/env python3
from __future__ import annotations

import argparse, datetime, hashlib, json, math, pathlib, random, traceback
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from safetensors.torch import save_file

from r44b_b1_preflight import J0, J1

EXPECTED_ATTEMPT_ID="R44B_B1_DEV_J0J1_ATTEMPT_1"
SEED=44
EPOCHS=10
BATCH_SIZE=64
LR=1e-3
WEIGHT_DECAY=.01
GRAD_CLIP=1.0
CLASSES=["NONE","P","I","C","O"]
TYPES=["P","I","C","O"]
SECTIONS=["TITLE","METHODS","UNKNOWN"]
TYPE2ID={x:i for i,x in enumerate(TYPES)}
SEC2ID={x:i for i,x in enumerate(SECTIONS)}
CLASS2ID={x:i for i,x in enumerate(CLASSES)}

EXPECTED_MANIFEST_SHA="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720"
EXPECTED_R44A_SHA="6f20f12e8bcb814067f689f5acc27918b98de93e6e88dd1ebb53d7689bc1d946"
EXPECTED_BASE_SHA="3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68"
EXPECTED_DESIGN_SHA="f8b49420cb17a5cb3f67f3120f9362b5e6b15fbb148176eab20105790bab1e18"
EXPECTED_CONTEXT_SHA="6bb548884cafb2a14e19b7d691b393dcf0ab9b5cc6add14e6ab0a873be33361b"
EXPECTED_INDEX_SHA="db9a6bae51a4db38d244e9e0a98f44b5dbfb246f694db5397c6e204cd58881dd"
EXPECTED_PARAMS={"J0":584631,"J1":667836}
FEATURE_ALLOWLIST=[
    "context_start","context_end","context_inside_mean","context_previous_or_edge","context_following_or_edge",
    "width","b_type","section","b_conf","boundary_start_prob","boundary_end_prob",
    "normalized_example_index","normalized_span_start",
]
FORBIDDEN_MODEL_FIELDS=["target","taxonomy","goldless_example","gold","gold_span","label","tags"]

def sha256_path(p:pathlib.Path)->str:
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def sha256_text(s:str)->str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def canonical_manifest_sha(m:dict)->str:
    q=dict(m)
    q.pop("manifest_sha256",None)
    return sha256_text(json.dumps(q,sort_keys=True,separators=(",",":")))

def read_jsonl(p:pathlib.Path):
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]

def write_json(p:pathlib.Path,obj):
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def write_jsonl(p:pathlib.Path,rows):
    with p.open("w",encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r,sort_keys=True,separators=(",",":"))+"\n")

def seed_fresh():
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True)

def finite01(v,name):
    x=float(v)
    if not math.isfinite(x) or x<0.0 or x>1.0:
        raise RuntimeError(f"{name} outside finite [0,1]: {x}")
    return x

def load_context(context_root:pathlib.Path):
    cp=context_root/"R44B_BASE_CONTEXT_FLOAT32.npy"
    ip=context_root/"R44B_BASE_CONTEXT_INDEX.json"
    sp=context_root/"R44B_BASE_CONTEXT_SUMMARY.json"
    s=json.loads(sp.read_text())
    if s.get("state")!="R44B_BASE_CONTEXT_CACHE_PASS": raise RuntimeError("context state")
    if s.get("base_model_sha256")!=EXPECTED_BASE_SHA or s.get("design_source_sha256")!=EXPECTED_DESIGN_SHA:
        raise RuntimeError("context source identity")
    if s.get("context_npy_sha256")!=EXPECTED_CONTEXT_SHA or s.get("index_sha256")!=EXPECTED_INDEX_SHA:
        raise RuntimeError("context declared hash")
    if sha256_path(cp)!=EXPECTED_CONTEXT_SHA or sha256_path(ip)!=EXPECTED_INDEX_SHA:
        raise RuntimeError("context physical hash")
    if any(bool(s.get(k)) for k in ["labels_used","verify_internal_used","old_select_used","protected_data_used"]):
        raise RuntimeError("context guard")
    ctx=np.load(cp,mmap_mode="r",allow_pickle=False)
    if ctx.shape!=(26595,768) or ctx.dtype!=np.float32 or not np.isfinite(ctx).all():
        raise RuntimeError(f"context tensor invalid {ctx.shape}/{ctx.dtype}")
    idx=json.loads(ip.read_text()); index={}; offset=0
    for q in idx:
        key=(int(q["document"]),int(q["sentence"]))
        if key in index: raise RuntimeError(f"duplicate context index {key}")
        if int(q["offset"])!=offset or int(q["length"])<=0: raise RuntimeError(f"context offset {key}")
        index[key]=q; offset+=int(q["length"])
    if len(index)!=1034 or offset!=26595: raise RuntimeError("context index accounting")
    return ctx,index,s

def feature_tensors(rows,ctx,index,include_targets=True):
    starts=[]; ends=[]; insides=[]; prevs=[]; nexts=[]
    pedges=[]; nedges=[]; widths=[]; btypes=[]; secs=[]; scalars=[]; ys=[]
    seen=set()
    for r in rows:
        ident=(int(r["document"]),int(r["sentence"]),int(r["start"]),int(r["end"]),str(r["b_type"]))
        if ident in seen: raise RuntimeError(f"duplicate candidate row {ident}")
        seen.add(ident)
        key=ident[:2]
        if key not in index: raise RuntimeError(f"missing context index {key}")
        q=index[key]; off=int(q["offset"]); n=int(q["length"])
        s=int(r["start"]); e=int(r["end"]); w=e-s
        if not 0<=s<e<=n: raise RuntimeError(f"candidate bounds {ident}/{n}")
        if int(r["width"])!=w or not 1<=w<=64: raise RuntimeError(f"candidate width {ident}/{w}")
        bt=str(r["b_type"]); sec=str(r["section"])
        if bt not in TYPE2ID or sec not in SEC2ID: raise RuntimeError(f"categorical feature {ident}")
        arr=ctx[off:off+n]
        starts.append(np.asarray(arr[s],dtype=np.float32))
        ends.append(np.asarray(arr[e-1],dtype=np.float32))
        insides.append(np.asarray(arr[s:e].mean(axis=0),dtype=np.float32))
        pe=s==0; ne=e==n
        prevs.append(np.zeros(768,np.float32) if pe else np.asarray(arr[s-1],dtype=np.float32))
        nexts.append(np.zeros(768,np.float32) if ne else np.asarray(arr[e],dtype=np.float32))
        pedges.append(pe); nedges.append(ne); widths.append(w); btypes.append(TYPE2ID[bt]); secs.append(SEC2ID[sec])
        scalars.append([
            finite01(r["b_conf"],"b_conf"),
            finite01(r["boundary_start_prob"],"boundary_start_prob"),
            finite01(r["boundary_end_prob"],"boundary_end_prob"),
            finite01(r["normalized_example_index"],"normalized_example_index"),
            finite01(r["normalized_span_start"],"normalized_span_start"),
        ])
        if include_targets:
            t=str(r["target"])
            if t not in CLASS2ID: raise RuntimeError(f"target {t}")
            ys.append(CLASS2ID[t])
    vec=lambda x:torch.from_numpy(np.stack(x).astype(np.float32,copy=False))
    out=[
        vec(starts),vec(ends),vec(insides),vec(prevs),vec(nexts),
        torch.tensor(pedges,dtype=torch.bool),torch.tensor(nedges,dtype=torch.bool),
        torch.tensor(widths,dtype=torch.long),torch.tensor(btypes,dtype=torch.long),
        torch.tensor(secs,dtype=torch.long),torch.tensor(scalars,dtype=torch.float32),
    ]
    if include_targets: out.append(torch.tensor(ys,dtype=torch.long))
    return tuple(out)

def feature_fingerprint(features):
    h=hashlib.sha256()
    for t in features:
        a=t.detach().cpu().contiguous().numpy()
        h.update(str(a.dtype).encode()); h.update(str(a.shape).encode()); h.update(a.tobytes(order="C"))
    return h.hexdigest()

def build_model(head):
    seed_fresh()
    cls={"J0":J0,"J1":J1}.get(head)
    if cls is None: raise RuntimeError("head must be J0/J1")
    m=cls()
    n=sum(p.numel() for p in m.parameters() if p.requires_grad)
    if n!=EXPECTED_PARAMS[head]: raise RuntimeError(f"{head} parameter count {n}")
    return m

def fit_head(train_features,head,out_dir:pathlib.Path,epochs=EPOCHS,batch_size=BATCH_SIZE,status_path=None,status_meta=None):
    if epochs!=EPOCHS or batch_size!=BATCH_SIZE:
        raise RuntimeError("scientific schedule mutation")
    *x,y=train_features
    n=len(y)
    if n<=0: raise RuntimeError("empty training rows")
    model=build_model(head)
    ds=TensorDataset(*x,y)
    g=torch.Generator(); g.manual_seed(SEED)
    loader=DataLoader(ds,batch_size=batch_size,shuffle=True,generator=g,num_workers=0,drop_last=False)
    opt=torch.optim.AdamW(model.parameters(),lr=LR,weight_decay=WEIGHT_DECAY)
    total_steps=len(loader)*epochs
    if total_steps<=0: raise RuntimeError("zero optimizer steps")
    sched=torch.optim.lr_scheduler.LambdaLR(opt,lr_lambda=lambda step:max(0.0,1.0-(step/total_steps)))
    loss_fn=nn.CrossEntropyLoss()
    trace=[]; global_step=0
    model.train()
    for ep in range(1,epochs+1):
        loss_sum=0.0; count=0
        for batch in loader:
            xb=list(batch[:-1]); yb=batch[-1]
            opt.zero_grad(set_to_none=True)
            logits=model(*xb)
            loss=loss_fn(logits,yb)
            if not torch.isfinite(loss): raise RuntimeError("nonfinite train loss")
            loss.backward()
            if not all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters()):
                raise RuntimeError("nonfinite train gradient")
            torch.nn.utils.clip_grad_norm_(model.parameters(),GRAD_CLIP,error_if_nonfinite=True)
            opt.step(); sched.step(); global_step+=1
            loss_sum+=float(loss.detach())*len(yb); count+=len(yb)
        epoch_loss=loss_sum/count
        trace.append({"epoch":ep,"mean_loss":epoch_loss,"global_step":global_step,"lr":float(opt.param_groups[0]["lr"])})
        if status_path is not None:
            meta=dict(status_meta or {})
            write_json(status_path,{
                **meta,
                "state":"RUNNING","current_stage":"TRAINING","current_epoch":ep,
                "epochs_total":epochs,"global_step":global_step,"total_steps":total_steps,
                "latest_loss":epoch_loss,"progress_percent":round(90.0*ep/epochs,6),
                "last_progress_at":now(),"failure_or_stall_reason":None,
            })
    if global_step!=total_steps: raise RuntimeError("optimizer step accounting")
    ckpt=out_dir/f"R44B_{head}_FINAL_MODEL.safetensors"
    save_file({k:v.detach().cpu().contiguous() for k,v in model.state_dict().items()},str(ckpt))
    return model,trace,ckpt,total_steps

def predict(model,features,batch_size=256):
    x=features
    ds=TensorDataset(*x)
    loader=DataLoader(ds,batch_size=batch_size,shuffle=False,num_workers=0,drop_last=False)
    parts=[]
    model.eval()
    with torch.no_grad():
        for batch in loader:
            probs=torch.softmax(model(*batch),dim=-1)
            if probs.ndim!=2 or probs.shape[1]!=5 or not torch.isfinite(probs).all():
                raise RuntimeError("invalid probabilities")
            parts.append(probs.cpu())
    p=torch.cat(parts,dim=0)
    if p.shape[0]!=len(x[0]): raise RuntimeError("prediction completeness")
    if torch.max(torch.abs(p.sum(dim=1)-1.0)).item()>1e-5: raise RuntimeError("probability normalization")
    return p.numpy()

def scientific_run(a):
    if a.attempt_id!=EXPECTED_ATTEMPT_ID:
        raise RuntimeError(f"attempt identity mismatch {a.attempt_id}")
    out=a.out
    out.mkdir(parents=True,exist_ok=False)
    status=out/"PROCESS_STATUS.json"
    write_json(status,{"state":"INITIALIZING","scientific_attempt_started":False,
                       "attempt_id":a.attempt_id,"outer_fold":a.outer_fold,"head":a.head,
                       "progress_percent":0.0,"last_progress_at":now()})

    m=json.loads(a.manifest.read_text())
    got=canonical_manifest_sha(m)
    if m.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA or got!=EXPECTED_MANIFEST_SHA:
        raise RuntimeError(f"canonical manifest hash {got}")
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); oldsel=set(m["excluded_old_select_documents"])
    folds={int(q["fold"]):set(q["documents"]) for q in m["oof_folds"]}
    if len(design)!=256 or len(verify)!=64 or set(folds)!=set(range(5)) or set().union(*folds.values())!=design:
        raise RuntimeError("manifest structure")
    if design&verify or design&oldsel or verify&oldsel: raise RuntimeError("manifest isolation")
    if a.outer_fold not in folds: raise RuntimeError("outer fold")

    agg=json.loads((a.nested_root/"R44B_PAIR_AGGREGATE_SUMMARY.json").read_text())
    if agg.get("state")!="R44B_PAIR_AGGREGATE_PASS" or agg.get("pair_count")!=10:
        raise RuntimeError("nested aggregate identity")
    if agg.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA or agg.get("r44a_bank_sha256")!=EXPECTED_R44A_SHA:
        raise RuntimeError("nested provenance")
    if any(bool(agg.get(k)) for k in ["verify_internal_used","old_select_used","protected_data_used","head_training"]):
        raise RuntimeError("nested access guard")

    k=a.outer_fold
    meta_p=a.nested_root/f"R44B_OUTER_{k}_META_TRAIN.jsonl"
    eval_p=a.nested_root/f"R44B_OUTER_{k}_EVAL.jsonl"
    osum=agg["outer"][str(k)]
    if sha256_path(meta_p)!=osum["meta_sha256"] or sha256_path(eval_p)!=osum["eval_sha256"]:
        raise RuntimeError("outer bank SHA")
    meta=read_jsonl(meta_p); ev=read_jsonl(eval_p)
    if len(meta)!=int(osum["meta_candidate_rows"]) or len(ev)!=int(osum["eval_candidate_rows"]):
        raise RuntimeError("outer row count")
    if any(int(r["document"]) in folds[k] for r in meta): raise RuntimeError("outer row leaked into meta")
    if any(int(r["document"]) not in folds[k] for r in ev): raise RuntimeError("outer eval doc mismatch")

    ctx,index,ctx_summary=load_context(a.context_root)
    train=feature_tensors(meta,ctx,index,include_targets=True)
    eval_x=feature_tensors(ev,ctx,index,include_targets=False)

    # Freeze feature allowlist behavior before the first optimizer update.
    if meta:
        probe=[dict(meta[0])]
        f0=feature_tensors(probe,ctx,index,include_targets=False)
        probe[0]["target"]="NONE" if meta[0]["target"]!="NONE" else "P"
        probe[0]["taxonomy"]="SYNTHETIC_MUTATION_MUST_NOT_ENTER_FEATURES"
        probe[0]["goldless_example"]=not bool(probe[0].get("goldless_example",False))
        f1=feature_tensors(probe,ctx,index,include_targets=False)
        if feature_fingerprint(f0)!=feature_fingerprint(f1):
            raise RuntimeError("forbidden metadata affects model features")

    write_json(status,{
        "state":"RUNNING","scientific_attempt_started":True,"first_optimizer_update_pending":True,
        "attempt_id":a.attempt_id,"outer_fold":k,"head":a.head,"meta_rows":len(meta),"eval_rows":len(ev),
        "progress_percent":0.0,"last_progress_at":now(),
        "seed":SEED,"epochs":EPOCHS,"batch_size":BATCH_SIZE,
    })
    model,trace,ckpt,total_steps=fit_head(
        train,a.head,out,EPOCHS,BATCH_SIZE,status_path=status,
        status_meta={"scientific_attempt_started":True,"attempt_id":a.attempt_id,
                     "outer_fold":k,"head":a.head,"meta_rows":len(meta),"eval_rows":len(ev)}
    )
    write_json(status,{
        "state":"RUNNING","scientific_attempt_started":True,"first_optimizer_update_pending":False,
        "attempt_id":a.attempt_id,"outer_fold":k,"head":a.head,"meta_rows":len(meta),"eval_rows":len(ev),
        "global_steps":total_steps,"current_stage":"EVALUATION_NO_GRAD",
        "progress_percent":95.0,"last_progress_at":now(),
    })
    probs=predict(model,eval_x)

    prob_rows=[]
    for r,p in zip(ev,probs):
        q={
            "outer_fold":k,"head":a.head,
            "document":int(r["document"]),"sentence":int(r["sentence"]),
            "start":int(r["start"]),"end":int(r["end"]),"b_type":str(r["b_type"]),
            "target":str(r["target"]),"taxonomy":str(r.get("taxonomy","")),
            "p_NONE":float(p[0]),"p_P":float(p[1]),"p_I":float(p[2]),"p_C":float(p[3]),"p_O":float(p[4]),
        }
        prob_rows.append(q)
    pp=out/f"R44B_OUTER_{k}_{a.head}_PROBS.jsonl"
    write_jsonl(pp,prob_rows)

    summary={
        "state":"R44B_HEAD_FOLD_COMPLETE","scientific_attempt_started":True,
        "attempt_id":a.attempt_id,"outer_fold":k,"head":a.head,"seed":SEED,
        "schedule":{"epochs":EPOCHS,"batch_size":BATCH_SIZE,"optimizer":"AdamW","lr":LR,
                    "weight_decay":WEIGHT_DECAY,"gradient_clip":GRAD_CLIP,
                    "scheduler":"linear_decay_no_warmup","early_stopping":False,
                    "checkpoint_selection":"FINAL_FIXED_EPOCH_ONLY","loss":"ordinary_5way_cross_entropy"},
        "parameter_count":EXPECTED_PARAMS[a.head],
        "feature_allowlist":FEATURE_ALLOWLIST,
        "forbidden_model_fields":FORBIDDEN_MODEL_FIELDS,
        "meta_rows":len(meta),"meta_sha256":sha256_path(meta_p),
        "eval_rows":len(ev),"eval_sha256":sha256_path(eval_p),
        "manifest_canonical_sha256":got,
        "nested_aggregate_sha256":sha256_path(a.nested_root/"R44B_PAIR_AGGREGATE_SUMMARY.json"),
        "context_summary_sha256":sha256_path(a.context_root/"R44B_BASE_CONTEXT_SUMMARY.json"),
        "context_npy_sha256":EXPECTED_CONTEXT_SHA,"context_index_sha256":EXPECTED_INDEX_SHA,
        "checkpoint_sha256":sha256_path(ckpt),"probabilities_sha256":sha256_path(pp),
        "optimizer_steps":total_steps,"training_trace":trace,
        "guards":{
            "fresh_model_optimizer_scheduler_rng":True,
            "meta_only_optimizer_updates":True,
            "evaluation_model_eval":True,
            "evaluation_no_grad":True,
            "mechanics_state_reused":False,
            "verify_internal_used":False,"old_select_used":False,"protected_data_used":False,
            "threshold_evaluation_performed":False,"calibration_fitted":False,
            "early_stopping_used":False,"checkpoint_shopping":False,
        },
        "next_action":"AGGREGATE_ONLY_AFTER_ALL_10_FOLD_HEAD_JOBS_COMPLETE",
    }
    sp=out/f"R44B_OUTER_{k}_{a.head}_SUMMARY.json"; write_json(sp,summary)
    write_json(status,{
        "state":"COMPLETED","scientific_attempt_started":True,"attempt_id":a.attempt_id,
        "outer_fold":k,"head":a.head,"progress_percent":100.0,"last_progress_at":now(),"meta_rows":len(meta),"eval_rows":len(ev),
        "optimizer_steps":total_steps,"checkpoint_sha256":summary["checkpoint_sha256"],
        "probabilities_sha256":summary["probabilities_sha256"],
        "next_action":"AGGREGATE_ONLY_AFTER_ALL_10_FOLD_HEAD_JOBS_COMPLETE",
    })
    print(json.dumps(summary,indent=2,sort_keys=True))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--attempt-id",required=True)
    ap.add_argument("--nested-root",type=pathlib.Path,required=True)
    ap.add_argument("--context-root",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--outer-fold",type=int,required=True)
    ap.add_argument("--head",choices=["J0","J1"],required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()
    try:
        scientific_run(a)
    except Exception as e:
        try:
            a.out.mkdir(parents=True,exist_ok=True)
            write_json(a.out/"PROCESS_STATUS.json",{
                "state":"FAILED","attempt_id":getattr(a,"attempt_id",None),
                "outer_fold":a.outer_fold,"head":a.head,"last_progress_at":now(),
                "error_type":type(e).__name__,"error":str(e),
                "traceback_tail":traceback.format_exc().splitlines()[-20:],
            })
        finally:
            raise

if __name__=="__main__":
    main()
