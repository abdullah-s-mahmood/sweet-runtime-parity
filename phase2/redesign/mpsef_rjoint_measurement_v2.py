#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import signal
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))

from mpsef_rjoint_core_v2 import evaluate_action_against_gold, import_m2
from mpsef_rjoint_score_v2 import score_population
from process_progress_v1 import update_state

VERSION="MPSEF_RJOINT_MEASUREMENT_V2"
EXPERIMENT_ID="MPSEF-RJOINT-V2-CF1918-20261001-A"
ACTION_SCORING_TIMEOUT_SECONDS=60

EXPECTED_CASES=1918
EXPECTED_CLUSTERS=764
EXPECTED_SOURCE_SHA="051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_ACTIONS_SHA="6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a"
EXPECTED_HYPOTHESES_SHA="b4736383019d017780a8bfe4b076a0cd742e71bccfbb50350da8fa59b7c9ac75"
EXPECTED_DIAGNOSTIC_SHA="2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e"
EXPECTED_FULL_GOLD_SHA="971b6fbb28dc3767193e7a4b0f722c3abebfc8600155a57093ba483dac6491e8"

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def require_evidence(path):
    x=json.loads(Path(path).read_text(encoding="utf-8"))
    if x.get("experiment_id")!=EXPERIMENT_ID:
        raise RuntimeError("measurement evidence experiment mismatch")
    if x.get("consumption_claimed") is not True:
        raise RuntimeError("measurement requires durable consumption claim")
    if x.get("gold_access_allowed_after_claim") is not True:
        raise RuntimeError("measurement gold access flag absent")
    if x.get("measurement_authorized") is not True:
        raise RuntimeError("measurement authorization evidence false")
    return x

class ActionScoringTimeout(TimeoutError):
    pass

def _alarm_handler(signum, frame):
    raise ActionScoringTimeout(
        f"action scoring exceeded frozen {ACTION_SCORING_TIMEOUT_SECONDS}s limit"
    )

def make_timed_evaluator(lev):
    def evaluate(output,source,gold):
        old_handler=signal.getsignal(signal.SIGALRM)
        try:
            signal.signal(signal.SIGALRM,_alarm_handler)
            signal.setitimer(signal.ITIMER_REAL,ACTION_SCORING_TIMEOUT_SECONDS)
            return evaluate_action_against_gold(lev,output,source,gold)
        finally:
            signal.setitimer(signal.ITIMER_REAL,0)
            signal.signal(signal.SIGALRM,old_handler)
    return evaluate

def self_test():
    good={
        "experiment_id":EXPERIMENT_ID,
        "consumption_claimed":True,
        "gold_access_allowed_after_claim":True,
        "measurement_authorized":True,
    }
    assert good["consumption_claimed"]
    assert ACTION_SCORING_TIMEOUT_SECONDS==60
    print(json.dumps({
        "self_test":"PASS",
        "version":VERSION,
        "action_scoring_timeout_seconds":ACTION_SCORING_TIMEOUT_SECONDS,
    },ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--authorization-evidence")
    ap.add_argument("--source-manifest")
    ap.add_argument("--action-sets")
    ap.add_argument("--hypotheses")
    ap.add_argument("--diagnostic-components")
    ap.add_argument("--gold-projection")
    ap.add_argument("--gold-projection-summary")
    ap.add_argument("--upstream-root")
    ap.add_argument("--state-file",default="MPSEF_RJOINT_MEASUREMENT_V2_PROGRESS.json")
    ap.add_argument("--out-prefix",default="MPSEF_RJOINT_MEASUREMENT_V2")
    args=ap.parse_args()

    if args.self_test:
        self_test()
        return

    needed=[
        args.authorization_evidence,args.source_manifest,args.action_sets,args.hypotheses,
        args.diagnostic_components,args.gold_projection,args.gold_projection_summary,args.upstream_root
    ]
    if any(x is None for x in needed):
        raise SystemExit("missing measurement input")

    evidence=require_evidence(args.authorization_evidence)
    state_path=Path(args.state_file)
    update_state(state_path,VERSION,"VALIDATING_FROZEN_INPUTS",0,EXPECTED_CASES)

    sourcep=Path(args.source_manifest)
    actionp=Path(args.action_sets)
    hypp=Path(args.hypotheses)
    diagp=Path(args.diagnostic_components)
    goldp=Path(args.gold_projection)
    goldsum=Path(args.gold_projection_summary)

    expected={
        sourcep:EXPECTED_SOURCE_SHA,
        actionp:EXPECTED_ACTIONS_SHA,
        hypp:EXPECTED_HYPOTHESES_SHA,
        diagp:EXPECTED_DIAGNOSTIC_SHA,
    }
    for p,h in expected.items():
        if sha256_file(p)!=h:
            raise RuntimeError(f"frozen input SHA mismatch: {p}")

    source_rows=read_jsonl(sourcep)
    action_sets=read_jsonl(actionp)
    hypothesis_rows=read_jsonl(hypp)
    diagnostic_rows=read_jsonl(diagp)
    projection_rows=read_jsonl(goldp)
    ps=json.loads(goldsum.read_text(encoding="utf-8"))

    if ps.get("status")!="CF_GOLD_PROJECTION_COMPLETE":
        raise RuntimeError("gold projection incomplete")
    if ps.get("experiment_id")!=EXPERIMENT_ID:
        raise RuntimeError("gold projection experiment mismatch")
    if ps.get("cases")!=EXPECTED_CASES or ps.get("clusters")!=EXPECTED_CLUSTERS:
        raise RuntimeError("gold projection population mismatch")
    if ps.get("source_manifest_sha256")!=EXPECTED_SOURCE_SHA:
        raise RuntimeError("gold projection source mismatch")
    if ps.get("full_gold_m2_sha256")!=EXPECTED_FULL_GOLD_SHA:
        raise RuntimeError("gold projection full-gold identity mismatch")
    if ps.get("projection_jsonl_sha256")!=sha256_file(goldp):
        raise RuntimeError("gold projection self-hash mismatch")
    if ps.get("consumption_claimed_before_gold_access") is not True:
        raise RuntimeError("gold projection did not prove prior consumption claim")
    if ps.get("metric_computed") is not False:
        raise RuntimeError("projection unexpectedly computed metric")

    if len(source_rows)!=EXPECTED_CASES or len(action_sets)!=EXPECTED_CASES:
        raise RuntimeError("source/action population mismatch")
    if len(hypothesis_rows)!=EXPECTED_CASES*2 or len(diagnostic_rows)!=EXPECTED_CASES*2:
        raise RuntimeError("hypothesis/diagnostic population mismatch")
    if len(projection_rows)!=EXPECTED_CASES:
        raise RuntimeError("projection row count mismatch")

    source_uids={x["uid"] for x in source_rows}
    if len(source_uids)!=EXPECTED_CASES:
        raise RuntimeError("source UID duplication")
    for rows,label in ((action_sets,"actions"),(projection_rows,"gold projection")):
        if {x["uid"] for x in rows}!=source_uids:
            raise RuntimeError(f"{label} UID mismatch")
    if {x["uid"] for x in hypothesis_rows}!=source_uids:
        raise RuntimeError("hypothesis UID mismatch")
    if {x["uid"] for x in diagnostic_rows}!=source_uids:
        raise RuntimeError("diagnostic UID mismatch")

    gold_by_uid={x["uid"]:x["gold"] for x in projection_rows}
    _,lev=import_m2(args.upstream_root)
    timed_evaluate=make_timed_evaluator(lev)

    def progress(processed,total,uid):
        update_state(
            state_path,VERSION,"SCORING_FROZEN_ACTION_SETS",
            processed,total,
            message=f"last_uid={uid}; no metric emitted in progress channel",
        )
        if processed==1 or processed%25==0 or processed==total:
            print(f"RJOINT_V2_PROGRESS {processed}/{total}",flush=True)

    result=score_population(
        lev,
        source_rows,
        action_sets,
        hypothesis_rows,
        diagnostic_rows,
        gold_by_uid,
        evaluate_fn=timed_evaluate,
        progress_callback=progress,
    )

    per_sentence=result.pop("per_sentence")
    result.update({
        "status":"MEASUREMENT_COMPLETE",
        "experiment_id":EXPERIMENT_ID,
        "cases":EXPECTED_CASES,
        "clusters":EXPECTED_CLUSTERS,
        "action_scoring_timeout_seconds":ACTION_SCORING_TIMEOUT_SECONDS,
        "source_manifest_sha256":sha256_file(sourcep),
        "executable_actions_sha256":sha256_file(actionp),
        "hypotheses_sha256":sha256_file(hypp),
        "diagnostic_components_sha256":sha256_file(diagp),
        "gold_projection_sha256":sha256_file(goldp),
        "full_gold_m2_sha256":ps["full_gold_m2_sha256"],
        "consumption_claimed_before_gold_access":True,
        "measurement_authorized":bool(evidence["measurement_authorized"]),
        "selector_trained":False,
        "internal_evaluation_opened":False,
        "stress_diagnostic_opened":False,
        "reserved_data_opened":False,
    })

    prefix=Path(args.out_prefix)
    summaryp=Path(str(prefix)+"_SUMMARY.json")
    perp=Path(str(prefix)+"_PER_SENTENCE.jsonl")
    summaryp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    perp.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in per_sentence)+"\n",encoding="utf-8")

    update_state(
        state_path,VERSION,"COMPLETE",EXPECTED_CASES,EXPECTED_CASES,status="COMPLETED",
        message="measurement output written; metric values intentionally omitted from progress state",
    )
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":
    main()
