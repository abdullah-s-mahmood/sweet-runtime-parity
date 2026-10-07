#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, hashlib, json, pathlib

EXPECTED_PAIRS={f"{a}-{b}" for a in range(5) for b in range(a+1,5)}
EXPECTED_R44A_SHA="6f20f12e8bcb814067f689f5acc27918b98de93e6e88dd1ebb53d7689bc1d946"
EXPECTED_MANIFEST_SHA="799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720"

def sha256(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def read_jsonl(p):
    return [json.loads(x) for x in pathlib.Path(p).read_text().splitlines() if x.strip()]

def write_jsonl(p,rows):
    with pathlib.Path(p).open("w",encoding="utf-8") as f:
        for r in rows:f.write(json.dumps(r,sort_keys=True)+"\n")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pairs-root",type=pathlib.Path,required=True)
    ap.add_argument("--manifest",type=pathlib.Path,required=True)
    ap.add_argument("--r44a-bank",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=False)

    m=json.loads(a.manifest.read_text())
    if m.get("manifest_sha256")!=EXPECTED_MANIFEST_SHA: raise RuntimeError("manifest identity")
    design=set(m["design_documents"]); verify=set(m["verify_internal_documents"]); oldsel=set(m["excluded_old_select_documents"])
    foldmap={int(x["fold"]):set(x["documents"]) for x in m["oof_folds"]}

    if sha256(a.r44a_bank)!=EXPECTED_R44A_SHA: raise RuntimeError("R44A bank SHA")
    r44a=read_jsonl(a.r44a_bank)
    if len(r44a)!=1942: raise RuntimeError("R44A row count")
    r44a_by_fold={k:[] for k in range(5)}
    for r in r44a:
        k=int(r["fold"])
        if r["document"] not in foldmap[k]: raise RuntimeError("R44A fold/document mismatch")
        r44a_by_fold[k].append(r)

    summaries=list(a.pairs_root.rglob("R44B_PAIR_*_SUMMARY.json"))
    if len(summaries)!=10: raise RuntimeError(f"pair summary count {len(summaries)}")
    banks={}
    pair_summaries={}
    for sp in summaries:
        s=json.loads(sp.read_text())
        if s.get("state")!="R44B_PAIR_UPSTREAM_COMPLETE": raise RuntimeError(f"pair state {sp}")
        pair=s["pair_id"]
        if pair in pair_summaries: raise RuntimeError(f"duplicate pair {pair}")
        pair_summaries[pair]=s
        pa,pb=map(int,pair.split("-"))
        if tuple(s["pair"])!=(pa,pb): raise RuntimeError("pair identity")
        train=design-foldmap[pa]-foldmap[pb]
        want=hashlib.sha256(json.dumps(sorted(train)).encode()).hexdigest()
        if s["train_document_ids_sha256"]!=want: raise RuntimeError(f"train hash {pair}")
        if train&verify or train&oldsel or train&foldmap[pa] or train&foldmap[pb]: raise RuntimeError(f"pair leakage {pair}")
        g=s["guards"]
        if not g.get("design_only_training") or not g.get("excluded_pair_absent_from_training"):
            raise RuntimeError(f"guard fail {pair}")
        if any(g.get(k) for k in ["verify_internal_used","old_r43_select_used","historical_dev_read","test_read","factpico_used","consumed_60_rct_holdout_used","other_protected_data_used","head_training"]):
            raise RuntimeError(f"protected/head guard {pair}")

        for side in (pa,pb):
            pattern=f"R44B_PAIR_{pair}_SIDE_{side}_CANDIDATES.jsonl"
            matches=list(a.pairs_root.rglob(pattern))
            if len(matches)!=1: raise RuntimeError(f"bank locate {pair}/{side}: {len(matches)}")
            bp=matches[0]; rows=read_jsonl(bp)
            ss=s["sides"][str(side)]
            if len(rows)!=ss["candidate_bank_rows"] or sha256(bp)!=ss["candidate_bank_sha256"]:
                raise RuntimeError(f"bank identity {pair}/{side}")
            seen=set()
            for r in rows:
                if r["pair_id"]!=pair or r["prediction_side"]!=side or r["excluded_pair"]!=[pa,pb]:
                    raise RuntimeError(f"row provenance {pair}/{side}")
                if r["document"] not in foldmap[side]: raise RuntimeError(f"row side doc {pair}/{side}")
                key=(r["document"],r["sentence"],r["start"],r["end"],r["b_type"])
                if key in seen: raise RuntimeError(f"duplicate row {pair}/{side}")
                seen.add(key)
            banks[(pair,side)]=rows

    if set(pair_summaries)!=EXPECTED_PAIRS: raise RuntimeError(f"pair inventory {set(pair_summaries)}")

    outer_summary={}
    all_meta_rows=0
    for k in range(5):
        meta=[]; expected_docs=design-foldmap[k]
        used_docs=set()
        for j in range(5):
            if j==k: continue
            pair=f"{min(k,j)}-{max(k,j)}"
            rows=banks[(pair,j)]
            for r in rows:
                if k not in r["excluded_pair"]: raise RuntimeError(f"outer exclusion missing {k}/{j}")
                if r["document"] in foldmap[k]: raise RuntimeError(f"outer leakage row {k}/{j}")
                q=dict(r); q["outer_fold"]=k; q["inner_validation_fold"]=j; meta.append(q)
                used_docs.add(q["document"])
        # Candidate-bearing docs may be a subset, but every row must come from outer-train.
        if not used_docs <= expected_docs: raise RuntimeError(f"outer meta docs {k}")
        meta.sort(key=lambda r:(r["document"],r["sentence"],r["start"],r["end"],r["b_type"],r["pair_id"]))
        mp=a.out/f"R44B_OUTER_{k}_META_TRAIN.jsonl"; write_jsonl(mp,meta)

        ev=[]
        for r in r44a_by_fold[k]:
            q=dict(r); q["outer_fold"]=k; q["source"]="R44A_FROZEN_OUTER_EVAL"; ev.append(q)
        ev.sort(key=lambda r:(r["document"],r["sentence"],r["start"],r["end"],r["b_type"]))
        ep=a.out/f"R44B_OUTER_{k}_EVAL.jsonl"; write_jsonl(ep,ev)

        mt=collections.Counter(r["target"] for r in meta); et=collections.Counter(r["target"] for r in ev)
        all_meta_rows+=len(meta)
        outer_summary[str(k)]={
          "outer_train_documents":len(expected_docs),
          "outer_eval_documents":len(foldmap[k]),
          "meta_candidate_rows":len(meta),
          "meta_target_counts":dict(mt),
          "meta_C_support":mt.get("C",0),
          "meta_sha256":sha256(mp),
          "eval_candidate_rows":len(ev),
          "eval_target_counts":dict(et),
          "eval_C_support":et.get("C",0),
          "eval_sha256":sha256(ep),
          "outer_eval_absent_from_meta_rows":all(r["document"] not in foldmap[k] for r in meta),
          "meta_generation_models_exclude_outer_eval":all(k in r["excluded_pair"] for r in meta),
        }

    report={
      "state":"R44B_PAIR_AGGREGATE_PASS",
      "pair_count":10,
      "logical_inner_edges":20,
      "pair_inventory":sorted(pair_summaries),
      "total_meta_rows_across_outer_problems":all_meta_rows,
      "outer":outer_summary,
      "r44a_bank_sha256":EXPECTED_R44A_SHA,
      "manifest_sha256":EXPECTED_MANIFEST_SHA,
      "verify_internal_used":False,
      "old_select_used":False,
      "protected_data_used":False,
      "head_training":False,
      "next_action":"VERIFY_CONTEXT_CACHE_THEN_SEPARATE_HEAD_TRAINING_AUTHORIZATION"
    }
    (a.out/"R44B_PAIR_AGGREGATE_SUMMARY.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"state":report["state"],"pair_count":10,
      "outer_meta_rows":{k:v["meta_candidate_rows"] for k,v in outer_summary.items()},
      "outer_meta_C":{k:v["meta_C_support"] for k,v in outer_summary.items()}},indent=2))

if __name__=="__main__": main()
