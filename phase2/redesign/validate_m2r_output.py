#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

DIMS={"ORTHOGRAPHY","MORPHOLOGY","SYNTAX","LEXICAL","OTHER"}
CONF={"HIGH","MEDIUM","LOW"}

def rows(p): return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("blind"); ap.add_argument("pred"); args=ap.parse_args()
    B=rows(args.blind); P=rows(args.pred); ids=[x["case_id"] for x in B]; cand={x["case_id"]:x["candidate"] for x in B}
    errs=[]; pids=[x.get("case_id") for x in P]
    if len(P)!=len(B): errs.append(f"prediction_count={len(P)} expected={len(B)}")
    if len(pids)!=len(set(pids)): errs.append("duplicate case_id")
    if set(pids)!=set(ids): errs.append("case_id set mismatch")
    for r in P:
        cid=r.get("case_id"); text=cand.get(cid,"")
        me=r.get("mandatory_errors"); uo=r.get("uncertain_or_optional")
        if not isinstance(me,list): errs.append(f"{cid}:mandatory_errors not list"); continue
        if not isinstance(uo,list): errs.append(f"{cid}:uncertain_or_optional not list")
        for j,e in enumerate(me):
            if not isinstance(e,dict): errs.append(f"{cid}:mandatory[{j}] not object"); continue
            s=e.get("surface","")
            if not isinstance(s,str) or not s.strip(): errs.append(f"{cid}:mandatory[{j}] empty surface")
            elif s not in text: errs.append(f"{cid}:mandatory[{j}] surface not verbatim in candidate: {s!r}")
            if e.get("dimension") not in DIMS: errs.append(f"{cid}:mandatory[{j}] invalid dimension")
            if e.get("confidence") not in CONF: errs.append(f"{cid}:mandatory[{j}] invalid confidence")
            if not isinstance(e.get("replacement"),str): errs.append(f"{cid}:mandatory[{j}] replacement missing")
            if not isinstance(e.get("brief_reason"),str) or not e["brief_reason"].strip(): errs.append(f"{cid}:mandatory[{j}] reason missing")
    print(json.dumps({"status":"PASS" if not errs else "FAIL","cases":len(B),"errors":errs},ensure_ascii=False,indent=2))
    raise SystemExit(0 if not errs else 1)
