#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib
import numpy as np

from r44c_linear5_train import (
    CLASSES,TYPES,SECTIONS,EXPECTED_MANIFEST_SHA,EXPECTED_R44A_SHA,
    canonical_manifest_sha,sha256_path,read_jsonl,load_context,
    raw_feature_matrix,inference_view,FEATURE_DIM
)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--nested-root",type=pathlib.Path,required=True)
    ap.add_argument("--context-root",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()
    if a.out.exists() and any(a.out.iterdir()):
        raise RuntimeError(f"pre-existing nonempty output directory: {a.out}")
    a.out.mkdir(parents=True,exist_ok=True)

    m=json.loads(a.manifest.read_text())
    got=canonical_manifest_sha(m)
    if got!=EXPECTED_MANIFEST_SHA or m.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA:
        raise RuntimeError("manifest canonical SHA")
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); oldsel=set(m["excluded_old_select_documents"])
    folds={int(q["fold"]):set(q["documents"]) for q in m["oof_folds"]}
    if len(design)!=256 or len(verify)!=64 or set().union(*folds.values())!=design:
        raise RuntimeError("manifest structure")
    if design&verify or design&oldsel or verify&oldsel: raise RuntimeError("split isolation")

    ag=json.loads((a.nested_root/"R44B_PAIR_AGGREGATE_SUMMARY.json").read_text())
    if ag.get("state")!="R44B_PAIR_AGGREGATE_PASS" or ag.get("pair_count")!=10:
        raise RuntimeError("nested aggregate")
    if ag.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA or ag.get("r44a_bank_sha256")!=EXPECTED_R44A_SHA:
        raise RuntimeError("nested identity")
    if any(bool(ag.get(k)) for k in ["verify_internal_used","old_select_used","protected_data_used","head_training"]):
        raise RuntimeError("nested guard")

    ctx,index,cs=load_context(a.context_root)
    outer={}; eval_total=0; audited_rows=0; max_width=0
    for k in range(5):
        mp=a.nested_root/f"R44B_OUTER_{k}_META_TRAIN.jsonl"
        ep=a.nested_root/f"R44B_OUTER_{k}_EVAL.jsonl"
        s=ag["outer"][str(k)]
        if sha256_path(mp)!=s["meta_sha256"] or sha256_path(ep)!=s["eval_sha256"]:
            raise RuntimeError(f"bank SHA {k}")
        meta=read_jsonl(mp); ev=read_jsonl(ep)
        if len(meta)!=int(s["meta_candidate_rows"]) or len(ev)!=int(s["eval_candidate_rows"]):
            raise RuntimeError(f"bank count {k}")
        if any(int(r["document"]) in folds[k] for r in meta): raise RuntimeError(f"meta leakage {k}")
        if any(int(r["document"]) not in folds[k] for r in ev): raise RuntimeError(f"eval docs {k}")
        if {int(r["document"]) for r in meta}&{int(r["document"]) for r in ev}: raise RuntimeError(f"doc overlap {k}")
        # Build raw features only. No scaler statistic and no model fit.
        ms,Xm,ym=raw_feature_matrix(meta,ctx,index,include_targets=True)
        clean_eval=[inference_view(r) for r in ev]
        es,Xe,_=raw_feature_matrix(clean_eval,ctx,index,include_targets=False)
        if Xm.shape!=(len(meta),FEATURE_DIM) or Xe.shape!=(len(ev),FEATURE_DIM):
            raise RuntimeError(f"feature dimension {k}")
        if Xm.dtype!=np.float32 or Xe.dtype!=np.float32: raise RuntimeError("raw dtype")
        # Explicitly prove no gold-derived fields survive the EVAL inference view.
        if any(any(f in q for f in ["target","taxonomy","goldless_example","tags","gold","gold_span","label"]) for q in clean_eval):
            raise RuntimeError("eval metadata survived inference view")
        target_counts=collections.Counter(r["target"] for r in meta)
        if set(target_counts)-set(CLASSES): raise RuntimeError("unknown target")
        widths=[int(r["width"]) for r in meta+ev]; max_width=max(max_width,max(widths))
        audited_rows+=len(meta)+len(ev); eval_total+=len(ev)
        outer[str(k)]={
            "meta_rows":len(meta),"eval_rows":len(ev),
            "meta_target_counts":dict(target_counts),
            "feature_dim":FEATURE_DIM,
            "raw_feature_dtype":"float32",
            "meta_documents":len({int(r["document"]) for r in meta}),
            "eval_documents":len({int(r["document"]) for r in ev}),
            "meta_sha256":sha256_path(mp),"eval_sha256":sha256_path(ep),
        }
    if eval_total!=1942: raise RuntimeError(f"eval total {eval_total}")
    report={
        "state":"R44C_LINEAR5_FROZEN_INPUT_PREFLIGHT_PASS",
        "manifest_canonical_sha256":got,
        "context_npy_sha256":cs["context_npy_sha256"],
        "context_index_sha256":cs["index_sha256"],
        "outer":outer,"eval_total":eval_total,"audited_rows":audited_rows,
        "max_candidate_width":max_width,
        "feature_dim":FEATURE_DIM,
        "scaler_statistics_computed":False,
        "optimizer_created":False,
        "model_created":False,
        "scientific_attempt_consumed":False,
        "verify_internal_used":False,
        "old_select_used":False,
        "protected_data_used":False,
        "next_action":"COMBINE_WITH_SOURCE_FREE_SYNTHETIC_PREFLIGHT_BEFORE_EXECUTOR_FREEZE"
    }
    (a.out/"R44C_LINEAR5_FROZEN_INPUT_PREFLIGHT.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=="__main__": main()
