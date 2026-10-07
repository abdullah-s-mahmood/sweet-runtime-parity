#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, pathlib
import numpy as np
import torch
from torch import nn

from r44b_b1_preflight import J0, J1

CLASSES=["NONE","P","I","C","O"]
TYPES=["P","I","C","O"]
SECTIONS=["TITLE","METHODS","UNKNOWN"]
TYPE2ID={x:i for i,x in enumerate(TYPES)}
SEC2ID={x:i for i,x in enumerate(SECTIONS)}
CLASS2ID={x:i for i,x in enumerate(CLASSES)}

EXPECTED_MANIFEST_SHA="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720"
EXPECTED_BASE_SHA="3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68"
EXPECTED_DESIGN_SHA="f8b49420cb17a5cb3f67f3120f9362b5e6b15fbb148176eab20105790bab1e18"
EXPECTED_CONTEXT_SHA="6bb548884cafb2a14e19b7d691b393dcf0ab9b5cc6add14e6ab0a873be33361b"
EXPECTED_INDEX_SHA="db9a6bae51a4db38d244e9e0a98f44b5dbfb246f694db5397c6e204cd58881dd"

def sha256(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def read_jsonl(p):
    return [json.loads(x) for x in pathlib.Path(p).read_text().splitlines() if x.strip()]

def finite01(x,name):
    x=float(x)
    if not math.isfinite(x) or x<0.0 or x>1.0:
        raise RuntimeError(f"{name} not finite [0,1]: {x}")
    return x

def build_batch(rows, ctx, index_map):
    starts=[]; ends=[]; insides=[]; prevs=[]; nexts=[]
    pedges=[]; nedges=[]; widths=[]; btypes=[]; secs=[]; scalars=[]; ys=[]
    for r in rows:
        key=(int(r["document"]),int(r["sentence"]))
        ix=index_map[key]; off=int(ix["offset"]); n=int(ix["length"])
        s=int(r["start"]); e=int(r["end"]); w=e-s
        if not (0<=s<e<=n): raise RuntimeError(f"candidate bounds {key} {s}:{e}/{n}")
        if not (1<=w<=64): raise RuntimeError(f"width out of frozen embedding range {w}")
        arr=ctx[off:off+n]
        starts.append(arr[s]); ends.append(arr[e-1]); insides.append(arr[s:e].mean(axis=0))
        pe=(s==0); ne=(e==n)
        prevs.append(np.zeros(768,np.float32) if pe else arr[s-1])
        nexts.append(np.zeros(768,np.float32) if ne else arr[e])
        pedges.append(pe); nedges.append(ne); widths.append(w)
        btypes.append(TYPE2ID[r["b_type"]]); secs.append(SEC2ID[r["section"]])
        scalars.append([
            finite01(r["b_conf"],"b_conf"),
            finite01(r["boundary_start_prob"],"boundary_start_prob"),
            finite01(r["boundary_end_prob"],"boundary_end_prob"),
            finite01(r["normalized_example_index"],"normalized_example_index"),
            finite01(r["normalized_span_start"],"normalized_span_start"),
        ])
        ys.append(CLASS2ID[r["target"]])
    vec=lambda xs:torch.tensor(np.stack(xs),dtype=torch.float32)
    return (
        vec(starts),vec(ends),vec(insides),vec(prevs),vec(nexts),
        torch.tensor(pedges,dtype=torch.bool),torch.tensor(nedges,dtype=torch.bool),
        torch.tensor(widths,dtype=torch.long),torch.tensor(btypes,dtype=torch.long),
        torch.tensor(secs,dtype=torch.long),torch.tensor(scalars,dtype=torch.float32),
        torch.tensor(ys,dtype=torch.long)
    )

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--nested-root",type=pathlib.Path,required=True)
    ap.add_argument("--context-root",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)

    m=json.loads(a.manifest.read_text())
    if m.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA: raise RuntimeError("manifest identity")
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); oldsel=set(m["excluded_old_select_documents"])
    foldmap={int(x["fold"]):set(x["documents"]) for x in m["oof_folds"]}
    if len(design)!=256 or len(verify)!=64 or design&verify or design&oldsel or verify&oldsel:
        raise RuntimeError("manifest split guard")

    cp=a.context_root/"R44B_BASE_CONTEXT_FLOAT32.npy"
    ip=a.context_root/"R44B_BASE_CONTEXT_INDEX.json"
    sp=a.context_root/"R44B_BASE_CONTEXT_SUMMARY.json"
    cs=json.loads(sp.read_text())
    if cs.get("state")!="R44B_BASE_CONTEXT_CACHE_PASS": raise RuntimeError("context state")
    if cs.get("base_model_sha256")!=EXPECTED_BASE_SHA or cs.get("design_source_sha256")!=EXPECTED_DESIGN_SHA:
        raise RuntimeError("context source identity")
    if sha256(cp)!=EXPECTED_CONTEXT_SHA or sha256(ip)!=EXPECTED_INDEX_SHA:
        raise RuntimeError("context physical SHA")
    if cs.get("labels_used") or cs.get("verify_internal_used") or cs.get("old_select_used") or cs.get("protected_data_used"):
        raise RuntimeError("context guard")
    ctx=np.load(cp,mmap_mode="r",allow_pickle=False)
    if ctx.shape!=(26595,768) or ctx.dtype!=np.float32: raise RuntimeError(f"context shape/dtype {ctx.shape}/{ctx.dtype}")
    if not np.isfinite(ctx).all(): raise RuntimeError("nonfinite context")

    idx=json.loads(ip.read_text()); index_map={}; offset=0
    for q in idx:
        key=(int(q["document"]),int(q["sentence"]))
        if key in index_map: raise RuntimeError(f"duplicate context index {key}")
        if int(q["offset"])!=offset or int(q["length"])<=0: raise RuntimeError(f"context offset {key}")
        index_map[key]=q; offset+=int(q["length"])
    if len(index_map)!=1034 or offset!=26595: raise RuntimeError("context index accounting")

    ag=json.loads((a.nested_root/"R44B_PAIR_AGGREGATE_SUMMARY.json").read_text())
    if ag.get("state")!="R44B_PAIR_AGGREGATE_PASS" or ag.get("pair_count")!=10:
        raise RuntimeError("aggregate state")
    if ag.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA:
        raise RuntimeError("aggregate manifest")
    if ag.get("verify_internal_used") or ag.get("old_select_used") or ag.get("protected_data_used") or ag.get("head_training"):
        raise RuntimeError("aggregate guard")

    audited=0; max_width=0; scalar_ranges={k:[1.0,0.0] for k in ["b_conf","boundary_start_prob","boundary_end_prob","normalized_example_index","normalized_span_start"]}
    actual_mechanics={}
    for k in range(5):
        meta_p=a.nested_root/f"R44B_OUTER_{k}_META_TRAIN.jsonl"
        eval_p=a.nested_root/f"R44B_OUTER_{k}_EVAL.jsonl"
        osum=ag["outer"][str(k)]
        if sha256(meta_p)!=osum["meta_sha256"] or sha256(eval_p)!=osum["eval_sha256"]:
            raise RuntimeError(f"outer file SHA {k}")
        meta=read_jsonl(meta_p); ev=read_jsonl(eval_p)
        if len(meta)!=osum["meta_candidate_rows"] or len(ev)!=osum["eval_candidate_rows"]:
            raise RuntimeError(f"outer counts {k}")
        if not meta or not ev: raise RuntimeError(f"empty outer {k}")
        md={int(r["document"]) for r in meta}; ed={int(r["document"]) for r in ev}
        if md&foldmap[k] or not md<=design-foldmap[k]: raise RuntimeError(f"meta docs {k}")
        if not ed<=foldmap[k] or md&ed: raise RuntimeError(f"eval docs {k}")
        seen=set()
        for source,rows in [("meta",meta),("eval",ev)]:
            for r in rows:
                if r["target"] not in CLASSES or r["b_type"] not in TYPES or r["section"] not in SECTIONS:
                    raise RuntimeError(f"categorical feature {k}/{source}")
                key=(int(r["document"]),int(r["sentence"]))
                if key not in index_map: raise RuntimeError(f"missing context {key}")
                n=int(index_map[key]["length"]); s=int(r["start"]); e=int(r["end"]); w=e-s
                if not (0<=s<e<=n): raise RuntimeError(f"bounds {k}/{source}/{key}")
                if int(r["width"])!=w: raise RuntimeError(f"width identity {k}/{source}/{key}")
                if not (1<=w<=64): raise RuntimeError(f"width frozen range {w}")
                max_width=max(max_width,w)
                dup=(source,int(r["document"]),int(r["sentence"]),s,e,r["b_type"])
                if dup in seen: raise RuntimeError(f"duplicate row {dup}")
                seen.add(dup)
                for name in scalar_ranges:
                    x=finite01(r[name],name); scalar_ranges[name][0]=min(scalar_ranges[name][0],x); scalar_ranges[name][1]=max(scalar_ranges[name][1],x)
                audited+=1

        sample=(meta[:8]+ev[:8])
        *features,y=build_batch(sample,ctx,index_map)
        outer_mech={}
        expected={"J0":584631,"J1":667836}
        for name,cls in [("J0",J0),("J1",J1)]:
            torch.manual_seed(44)
            model=cls()
            n=sum(p.numel() for p in model.parameters() if p.requires_grad)
            if n!=expected[name]: raise RuntimeError(f"{name} params {n}")
            logits=model(*features)
            loss=nn.CrossEntropyLoss()(logits,y)
            loss.backward()
            if list(logits.shape)!=[len(sample),5] or not torch.isfinite(loss):
                raise RuntimeError(f"{name} actual mechanics {k}")
            if not all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters()):
                raise RuntimeError(f"{name} nonfinite grad {k}")
            outer_mech[name]={"parameters":n,"actual_batch":len(sample),"loss":float(loss.detach())}
        actual_mechanics[str(k)]=outer_mech

    report={
      "state":"R44B_HEAD_ACTUAL_MECHANICS_PASS",
      "audited_candidate_rows_across_outer_files":audited,
      "context_shape":[26595,768],"context_dtype":"float32",
      "context_sha256":EXPECTED_CONTEXT_SHA,"context_index_sha256":EXPECTED_INDEX_SHA,
      "max_candidate_width":max_width,"scalar_ranges":scalar_ranges,
      "outer_actual_forward_backward":actual_mechanics,
      "J0_parameters":584631,"J1_parameters":667836,
      "scientific_head_training_performed":False,
      "threshold_evaluation_performed":False,
      "verify_internal_used":False,"old_select_used":False,"protected_data_used":False,
      "next_action":"HIGHER_MODEL_REVIEW_THEN_SEPARATE_J0_J1_SCIENTIFIC_TRAINING_AUTHORIZATION"
    }
    (a.out/"R44B_HEAD_ACTUAL_MECHANICS.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=="__main__": main()
