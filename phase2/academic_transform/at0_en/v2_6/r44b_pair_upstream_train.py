#!/usr/bin/env python3
from __future__ import annotations
import argparse, gc, hashlib, json, os, pathlib
import torch
from transformers import AutoTokenizer, BertForTokenClassification

from r44a_oof_fold_train import (
    EXPECTED_TRAIN_SHA, EXPECTED_R44_MANIFEST_SHA, EXPECTED_CONVERTED_SHA,
    CLASSES, TokenDataset, source_spans, source_boundary_tags,
    train_token, infer_heldout, candidate_bank, sha256_path, sha_text,
    write_json, now, seed_all
)

def parse_pair(s):
    p=tuple(sorted(int(x) for x in s.split("-")))
    if len(p)!=2 or p[0]==p[1] or p[0] not in range(5) or p[1] not in range(5):
        raise argparse.ArgumentTypeError("pair must be e.g. 0-1")
    return p

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preconverted-base",type=pathlib.Path,required=True)
    ap.add_argument("--design-source",type=pathlib.Path,required=True)
    ap.add_argument("--design-summary",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--pair",type=parse_pair,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); seed_all(); a.out.mkdir(parents=True,exist_ok=False)
    status=a.out/"PROCESS_STATUS.json"
    pa,pb=a.pair; pair_id=f"{pa}-{pb}"

    mp=a.preconverted_base/"model.safetensors"
    if not mp.exists() or sha256_path(mp)!=EXPECTED_CONVERTED_SHA:
        raise RuntimeError("preconverted base identity mismatch")
    if (a.preconverted_base/"pytorch_model.bin").exists():
        raise RuntimeError("unexpected pickle weight")

    dss=json.loads(a.design_summary.read_text())
    if dss.get("state")!="R44_DESIGN_SOURCE_PACKAGE_PASS": raise RuntimeError("design summary state")
    if dss.get("source_train_sha256")!=EXPECTED_TRAIN_SHA: raise RuntimeError("TRAIN provenance")
    if dss.get("r44_manifest_sha256")!=EXPECTED_R44_MANIFEST_SHA: raise RuntimeError("manifest provenance")
    if sha256_path(a.design_source)!=dss.get("design_source_sha256"): raise RuntimeError("design source SHA")

    m=json.loads(a.manifest.read_text())
    if m.get("manifest_sha256")!=EXPECTED_R44_MANIFEST_SHA: raise RuntimeError("manifest SHA")
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); oldsel=set(m["excluded_old_select_documents"])
    foldmap={int(x["fold"]):set(x["documents"]) for x in m["oof_folds"]}
    if set(foldmap)!=set(range(5)) or set().union(*foldmap.values())!=design:
        raise RuntimeError("fold manifest")
    train_ids=design-foldmap[pa]-foldmap[pb]
    if train_ids&foldmap[pa] or train_ids&foldmap[pb] or train_ids&verify or train_ids&oldsel:
        raise RuntimeError("pair document isolation")
    if len(train_ids)+len(foldmap[pa])+len(foldmap[pb])!=256:
        raise RuntimeError("pair partition accounting")

    src=json.loads(a.design_source.read_text())
    if src.get("state")!="R44_DESIGN_SOURCE_MATERIALIZED": raise RuntimeError("design source state")
    docs={}
    for d in src["documents"]:
        di=int(d["original_document"])
        docs[di]=[(s["tokens"],s["tags"]) for s in d["sentences"]]
    if set(docs)!=design or set(docs)&verify or set(docs)&oldsel:
        raise RuntimeError("physical DESIGN isolation")

    rows=[]; train_gold={c:0 for c in CLASSES}
    for di in sorted(train_ids):
        for tokens,tags in docs[di]:
            for c,s,e in source_spans(tags): train_gold[c]+=1
            rows.append((tokens,tags,source_boundary_tags(tags)))

    write_json(status,{
      "state":"RUNNING","current_stage":"INITIALIZING","pair":pair_id,
      "progress_percent":0.0,"train_documents":len(train_ids),
      "heldout_folds":[pa,pb],"last_progress_at":now(),"failure_or_stall_reason":None
    })

    tok=AutoTokenizer.from_pretrained(a.preconverted_base,local_files_only=True,use_fast=True)
    bds=TokenDataset(rows,tok,"bio")
    binfo=train_token("B_CANDIDATE",a.preconverted_base,bds,a.out/"b_candidate",5e-5,0.0,10,8,status,0,10)
    del bds; gc.collect()
    bndds=TokenDataset(rows,tok,"boundary")
    bdinfo=train_token("C_BOUNDARY",a.preconverted_base,bndds,a.out/"c_boundary",5e-5,.01,3,8,status,10,3)
    del bndds; gc.collect()

    bmodel=BertForTokenClassification.from_pretrained(a.out/"b_candidate",local_files_only=True)
    boundary=BertForTokenClassification.from_pretrained(a.out/"c_boundary",local_files_only=True)
    tok=AutoTokenizer.from_pretrained(a.out/"b_candidate",local_files_only=True,use_fast=True)

    side_results={}
    for side in (pa,pb):
        held=foldmap[side]
        _,sections,proposals,viol,bnd=infer_heldout(bmodel,boundary,tok,docs,held)
        bank,metrics=candidate_bank(side,docs,held,sections,proposals,viol,bnd)
        for r in bank:
            r["excluded_pair"]=[pa,pb]
            r["pair_id"]=pair_id
            r["prediction_side"]=side
        bp=a.out/f"R44B_PAIR_{pair_id}_SIDE_{side}_CANDIDATES.jsonl"
        with bp.open("w",encoding="utf-8") as f:
            for r in bank:f.write(json.dumps(r,sort_keys=True)+"\n")
        side_results[str(side)]={
          "heldout_documents":len(held),
          "heldout_document_ids_sha256":sha_text(json.dumps(sorted(held))),
          "candidate_bank_rows":len(bank),
          "candidate_bank_sha256":sha256_path(bp),
          "metrics":metrics,
        }

    summary={
      "state":"R44B_PAIR_UPSTREAM_COMPLETE",
      "pair":[pa,pb],"pair_id":pair_id,"seed":44,
      "source_train_sha256":EXPECTED_TRAIN_SHA,
      "design_source_sha256":sha256_path(a.design_source),
      "r44_manifest_sha256":EXPECTED_R44_MANIFEST_SHA,
      "converted_base_sha256":EXPECTED_CONVERTED_SHA,
      "train_documents":len(train_ids),
      "train_document_ids_sha256":sha_text(json.dumps(sorted(train_ids))),
      "train_gold_counts":train_gold,
      "models":{"B_CANDIDATE":binfo,"C_BOUNDARY":bdinfo},
      "sides":side_results,
      "guards":{
        "design_only_training":True,
        "excluded_pair_absent_from_training":True,
        "verify_internal_used":False,
        "old_r43_select_used":False,
        "historical_dev_read":False,
        "test_read":False,
        "factpico_used":False,
        "consumed_60_rct_holdout_used":False,
        "other_protected_data_used":False,
        "head_training":False,
        "checkpoint_selection":"FINAL_FIXED_EPOCH_ONLY",
      },
      "next_action":"ASSEMBLE_ONLY_AFTER_ALL_10_PAIR_JOBS_COMPLETE"
    }
    sp=a.out/f"R44B_PAIR_{pair_id}_SUMMARY.json"; write_json(sp,summary)
    write_json(status,{
      "state":"COMPLETED","current_stage":"PAIR_UPSTREAM_COMPLETE","pair":pair_id,
      "progress_percent":100.0,"train_documents":len(train_ids),
      "candidate_rows_by_side":{k:v["candidate_bank_rows"] for k,v in side_results.items()},
      "last_progress_at":now(),"failure_or_stall_reason":None,
      "next_action":"ASSEMBLE_ONLY_AFTER_ALL_10_PAIR_JOBS_COMPLETE"
    })
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__": main()
