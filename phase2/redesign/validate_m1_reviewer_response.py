#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCHEMA=json.loads((HERE/"M1_LABEL_SCHEMA.json").read_text(encoding="utf-8"))
QUEUE=[json.loads(x) for x in (HERE/"M1_PILOT_BLINDED_QUEUE.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
CASE_IDS=[x["m1_case_id"] for x in QUEUE]
AXES=list(SCHEMA["axes"])
REQ=SCHEMA["required_free_text"]

def load(path):
    rows=[json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
    return rows

def validate(rows):
    errs=[]
    ids=[x.get("m1_case_id") for x in rows]
    if len(rows)!=len(CASE_IDS): errs.append(f"row_count={len(rows)} expected={len(CASE_IDS)}")
    if len(ids)!=len(set(ids)): errs.append("duplicate m1_case_id")
    missing=sorted(set(CASE_IDS)-set(ids)); extra=sorted(set(ids)-set(CASE_IDS))
    if missing: errs.append("missing ids: "+",".join(missing))
    if extra: errs.append("extra ids: "+",".join(extra))
    for r in rows:
        cid=r.get("m1_case_id","<missing>")
        for axis,allowed in SCHEMA["axes"].items():
            v=r.get(axis)
            if v not in allowed: errs.append(f"{cid}: {axis}={v!r} not in schema")
        for k in REQ:
            v=r.get(k)
            if not isinstance(v,str) or not v.strip(): errs.append(f"{cid}: missing {k}")
        if not r.get("reviewer_id"): errs.append(f"{cid}: missing reviewer_id")
        if r.get("primary_pass_reference_blind") is not True:
            errs.append(f"{cid}: primary_pass_reference_blind must be true")
    return errs

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("response")
    args=ap.parse_args()
    errors=validate(load(args.response))
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors},ensure_ascii=False,indent=2))
        raise SystemExit(1)
    print(json.dumps({"status":"PASS","cases":len(CASE_IDS),"schema":SCHEMA["schema_id"]},ensure_ascii=False,indent=2))
