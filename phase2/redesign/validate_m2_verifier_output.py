#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

ENUMS={
 "candidate_status":{"KEEP_CORRECT","REPAIR_COMPLETE","REPAIR_INCOMPLETE","CANDIDATE_WRONG","AMBIGUOUS"},
 "necessity":{"CHANGE_NEEDED","NO_CHANGE_NEEDED","UNCERTAIN"},
 "local_correctness":{"CORRECT","INCORRECT","NOT_APPLICABLE","UNCERTAIN"},
 "contextual_correctness":{"CORRECT","INCORRECT","UNCERTAIN"},
 "residual_error":{"NONE","PRESENT","UNCERTAIN"},
 "meaning_preservation":{"PRESERVED","CHANGED","UNCERTAIN"},
 "decision":{"ACCEPT","REVIEW","REJECT"},
 "confidence":{"LOW","MEDIUM","HIGH"},
}

def load_jsonl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("blind")
    ap.add_argument("pred")
    args=ap.parse_args()
    blind=load_jsonl(args.blind); pred=load_jsonl(args.pred)
    ids=[x["case_id"] for x in blind]
    errs=[]
    if len(pred)!=len(ids): errs.append(f"prediction_count={len(pred)} expected={len(ids)}")
    pids=[x.get("case_id") for x in pred]
    if len(pids)!=len(set(pids)): errs.append("duplicate prediction case_id")
    miss=sorted(set(ids)-set(pids)); extra=sorted(set(pids)-set(ids))
    if miss: errs.append("missing:"+",".join(miss))
    if extra: errs.append("extra:"+",".join(extra))
    for r in pred:
        cid=r.get("case_id","<missing>")
        for k,allowed in ENUMS.items():
            if r.get(k) not in allowed: errs.append(f"{cid}:{k}={r.get(k)!r}")
        reason=r.get("brief_reason")
        if not isinstance(reason,str) or not reason.strip(): errs.append(f"{cid}:missing brief_reason")
        elif len(reason.split())>35: errs.append(f"{cid}:brief_reason exceeds 35 whitespace tokens")
        if r.get("candidate_status")=="REPAIR_INCOMPLETE" and r.get("decision")=="ACCEPT":
            errs.append(f"{cid}:REPAIR_INCOMPLETE cannot ACCEPT")
    out={"status":"PASS" if not errs else "FAIL","cases":len(ids),"errors":errs}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(0 if not errs else 1)
