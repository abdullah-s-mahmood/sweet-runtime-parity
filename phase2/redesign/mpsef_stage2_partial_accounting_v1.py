#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

VERSION="MPSEF_STAGE2_PARTIAL_ACCOUNTING_V1"

def load_input(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def load_durable_output(path):
    p=Path(path)
    rows=[]; errors=[]
    if not p.exists():
        return rows, errors
    for lineno,line in enumerate(p.read_text(encoding="utf-8",errors="replace").splitlines(),start=1):
        if not line.strip(): continue
        try:
            rows.append(json.loads(line))
        except Exception as exc:
            errors.append({"line":lineno,"error":f"{type(exc).__name__}:{exc}"})
    return rows, errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-jsonl",required=True)
    ap.add_argument("--output-jsonl",required=True)
    ap.add_argument("--run-state",required=True)
    ap.add_argument("--expected-count",type=int,required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    inp=load_input(args.input_jsonl)
    if len(inp)!=args.expected_count or len({r["uid"] for r in inp})!=args.expected_count:
        raise RuntimeError("PARTIAL_ACCOUNTING_INPUT_IDENTITY_FAIL")
    input_order=[r["uid"] for r in inp]
    input_set=set(input_order)

    out,parse_errors=load_durable_output(args.output_jsonl)
    completed=[]
    seen=set()
    duplicate=[]
    foreign=[]
    for r in out:
        uid=r.get("uid")
        if uid not in input_set:
            foreign.append(uid); continue
        if uid in seen:
            duplicate.append(uid); continue
        seen.add(uid); completed.append(uid)

    state={}
    sp=Path(args.run_state)
    if sp.exists():
        try: state=json.loads(sp.read_text(encoding="utf-8"))
        except Exception as exc: state={"status":"RUN_STATE_UNREADABLE","error":f"{type(exc).__name__}:{exc}"}

    current_uid=state.get("current_uid")
    aborted=[]
    if current_uid in input_set and current_uid not in seen:
        aborted=[current_uid]

    not_attempted=[u for u in input_order if u not in seen and u not in set(aborted)]
    complete=(
        len(seen)==args.expected_count and not aborted and not not_attempted
        and not duplicate and not foreign and not parse_errors
        and state.get("status")=="COMPLETE"
    )

    payload={
        "record_id":VERSION,
        "status":"COMPLETE" if complete else "PARTIAL_OR_INTERRUPTED",
        "expected_count":args.expected_count,
        "completed_count":len(seen),
        "aborted_count":len(aborted),
        "not_attempted_count":len(not_attempted),
        "completed_uids":completed,
        "aborted_uids":aborted,
        "not_attempted_uids":not_attempted,
        "duplicate_output_uids":duplicate,
        "foreign_output_uids":foreign,
        "output_parse_errors":parse_errors,
        "run_state_status":state.get("status"),
        "run_state_current_uid":current_uid,
        "completion_claim_allowed":complete,
    }
    Path(args.out).write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:payload[k] for k in (
        "record_id","status","expected_count","completed_count","aborted_count",
        "not_attempted_count","run_state_status","completion_claim_allowed"
    )},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
