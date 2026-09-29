#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,sys,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

DATASET="khaled44/arabigee-data"
BASE="https://huggingface.co/datasets/khaled44/arabigee-data/resolve/main"
FILES=["annotations.csv","contexts_nopnx.csv","contexts_pnx.csv"]

def sha(s): return hashlib.sha256(str(s).encode()).hexdigest()
def part(cid):
    v=int(sha(f"M2R-V1|{cid}")[:8],16)%100
    return "DEVELOPMENT" if v<70 else ("CONFIRMATION" if v<85 else "HOLDOUT")

def download_file(name,out):
    urls=[
      f"{BASE}/{name}?download=true",
      f"{BASE}/data/{name}?download=true"
    ]
    last=None
    for u in urls:
        try:
            urllib.request.urlretrieve(u,out)
            if Path(out).stat().st_size>20: return u
        except Exception as e:
            last=e
    raise RuntimeError(f"could not download {name}: {last}")

def main():
    import csv
    work=Path("upstream/arabigee"); work.mkdir(parents=True,exist_ok=True)
    resolved={}
    for f in FILES:
        resolved[f]=download_file(f,work/f)

    with open(work/"annotations.csv",encoding="utf-8-sig",newline="") as fh:
        anns=list(csv.DictReader(fh))
    with open(work/"contexts_nopnx.csv",encoding="utf-8-sig",newline="") as fh:
        ctx=list(csv.DictReader(fh))

    byctx=defaultdict(list)
    for a in anns: byctx[str(a["context_id"])].append(a)

    stats=Counter()
    partition_contexts=Counter()
    dimensions=Counter()
    multi=0
    for c in ctx:
        cid=str(c["context_id"]); partition_contexts[part(cid)]+=1
        aa=byctx.get(cid,[])
        if aa: stats["contexts_with_annotations"]+=1
        if len({(a.get("erroneous_word",""),a.get("target_word","")) for a in aa if a.get("erroneous_word")})>=2:
            multi+=1
        for a in aa:
            stats["annotation_rows_linked"]+=1
            if a.get("orth_code"): dimensions["ORTHOGRAPHY"]+=1
            if a.get("morph_code"): dimensions["MORPHOLOGY"]+=1
            if a.get("synt_code"): dimensions["SYNTAX"]+=1
            if a.get("lex_code"): dimensions["LEXICAL"]+=1

    criteria={
      "annotations_ge_1000":len(anns)>=1000,
      "nopnx_contexts_ge_400":len(ctx)>=400,
      "contexts_with_annotations_ge_300":stats["contexts_with_annotations"]>=300,
      "multi_error_contexts_ge_100":multi>=100,
      "development_contexts_ge_250":partition_contexts["DEVELOPMENT"]>=250,
      "confirmation_contexts_ge_50":partition_contexts["CONFIRMATION"]>=50,
      "holdout_contexts_ge_50":partition_contexts["HOLDOUT"]>=50,
      "orthography_annotations_ge_100":dimensions["ORTHOGRAPHY"]>=100,
      "structured_nonorth_dimensions_present":sum(dimensions[d] for d in ["MORPHOLOGY","SYNTAX","LEXICAL"])>=100
    }
    ready=all(criteria.values())

    summary={
      "status":"M2R_DATA_READY" if ready else "M2R_DATA_NOT_READY",
      "date":"2026-09-30",
      "dataset":DATASET,
      "resolved_files":{k:sha(v) for k,v in resolved.items()},
      "annotation_rows":len(anns),
      "nopnx_context_rows":len(ctx),
      "contexts_with_annotations":stats["contexts_with_annotations"],
      "multi_error_contexts":multi,
      "partition_context_counts":dict(partition_contexts),
      "dimension_annotation_counts":dict(dimensions),
      "criteria":criteria,
      "data_ready":ready,
      "raw_text_persisted":False,
      "holdout_text_exposed":False,
      "forbidden_project_data_read":False
    }
    Path("M2R_DATA_FEASIBILITY_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
    if not ready: raise SystemExit(2)

if __name__=="__main__":
    main()
