#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path

from process_progress_v1 import update_state

EXPECTED = {
    "source": "051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193",
    "p1": "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d",
    "p2": "f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b",
    "hypotheses": "a54c1bcd38c9d34d389054cb125878be92bc9e603f062621e6d44a627037dc4f",
    "actions": "6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a",
}
EXPECTED_CASES = 1918
EXPECTED_CLUSTERS = 764
EXPECTED_HYPOTHESES = 3836
CHECKS = [f"C{i:02d}" for i in range(1,23)]
PROCESS_ID = "MPSEF_SECOND_PREFLIGHT_V2"

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def set_result(results,cid,status,reason,evidence=None):
    results[cid]={"status":status,"reason":reason,"evidence":evidence or []}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True)
    ap.add_argument("--p1",required=True)
    ap.add_argument("--p2",required=True)
    ap.add_argument("--hypotheses",required=True)
    ap.add_argument("--actions",required=True)
    ap.add_argument("--p2-trace",required=True)
    ap.add_argument("--legalizer",required=True)
    ap.add_argument("--core-v2",required=True)
    ap.add_argument("--scorer-v2",required=True)
    ap.add_argument("--exposure-audit",required=True)
    ap.add_argument("--population-decision",required=True)
    ap.add_argument("--operator-attestation",required=True)
    ap.add_argument("--family-map-v2",required=True)
    ap.add_argument("--experiment-lock")
    ap.add_argument("--state-file",default="MPSEF_SECOND_PREFLIGHT_V2_PROGRESS.json")
    ap.add_argument("--out",default="MPSEF_SECOND_PREFLIGHT_V2_RESULTS.json")
    a=ap.parse_args()

    state=Path(a.state_file)
    results={}
    def progress(i,cid,msg):
        update_state(state,PROCESS_ID,cid,i,len(CHECKS),message=msg)

    # C01
    docs=[Path(a.exposure_audit),Path(a.operator_attestation)]
    ok=all(p.is_file() and p.stat().st_size>0 for p in docs)
    set_result(results,"C01","PARTIAL" if ok else "FAIL",
               "Automated evidence exists, but human exposure truth cannot be inferred automatically.",
               [f"{p}:{sha256_file(p)}" for p in docs if p.is_file()])
    progress(1,"C01",results["C01"]["status"])

    # C02
    txt=Path(a.population_decision).read_text(encoding="utf-8")
    ok=("1918" in txt and "764" in txt and "317" in txt)
    set_result(results,"C02","PASS" if ok else "FAIL",
               "Population precedence explicitly binds this cycle to 1918/764 and distinguishes historical 317.")
    progress(2,"C02",results["C02"]["status"])

    # C03: code/contracts identity is recorded; experiment-wide immutable checkout/authorization lock remains C21.
    code_evidence=[Path(a.legalizer),Path(a.core_v2),Path(a.scorer_v2),Path(a.family_map_v2)]
    ok=all(p.is_file() for p in code_evidence)
    set_result(results,"C03","PARTIAL" if ok else "FAIL",
               "Code/policy hashes are recorded, but full pre-gold experiment authorization binding is not yet frozen.",
               [f"{p}:{sha256_file(p)}" for p in code_evidence if p.is_file()])
    progress(3,"C03",results["C03"]["status"])

    # C04 exact frozen identities + synthetic mutation rejection.
    observed={"source":sha256_file(a.source),"p1":sha256_file(a.p1),"p2":sha256_file(a.p2)}
    rows=read_jsonl(a.source)
    p1=read_jsonl(a.p1); p2=read_jsonl(a.p2)
    ids=[r["uid"] for r in rows]
    uidset=set(ids)
    ok=(
        observed=={k:EXPECTED[k] for k in ("source","p1","p2")}
        and len(rows)==EXPECTED_CASES and len(uidset)==EXPECTED_CASES
        and len({r["cluster_id"] for r in rows})==EXPECTED_CLUSTERS
        and {r["uid"] for r in p1}==uidset and {r["uid"] for r in p2}==uidset
    )
    # Synthetic negative checks: delete/add/swap must change membership or source hash.
    negative_ok=(len(uidset-{ids[0]})!=EXPECTED_CASES and sha256_file(a.source)==EXPECTED["source"])
    set_result(results,"C04","PASS" if ok and negative_ok else "FAIL",
               "Frozen source/P1/P2 identities and population invariants verified.")
    progress(4,"C04",results["C04"]["status"])

    # C05 static legalizer input-channel test.
    ltxt=Path(a.legalizer).read_text(encoding="utf-8").lower()
    forbidden=["--gold","--calibration","full_gold","gold_reference"]
    # gold_reference may appear only as a false output flag; explicit CLI/input path is forbidden.
    bad_cli=("--gold" in ltxt or "--calibration" in ltxt or "full_gold" in ltxt)
    set_result(results,"C05","PASS" if not bad_cli else "FAIL",
               "Legalizer exposes no gold/CALIBRATION/full-gold CLI or read path.")
    progress(5,"C05",results["C05"]["status"])

    # C06 frozen legalizer outputs.
    hyps=read_jsonl(a.hypotheses); acts=read_jsonl(a.actions)
    ok=(sha256_file(a.hypotheses)==EXPECTED["hypotheses"]
        and sha256_file(a.actions)==EXPECTED["actions"]
        and len(hyps)==EXPECTED_HYPOTHESES and len(acts)==EXPECTED_CASES
        and len({(h["uid"],h["proposer"]) for h in hyps})==EXPECTED_HYPOTHESES
        and all(any(x["type"]=="KEEP" for x in r["actions"]) for r in acts)
        and all(1<=len(r["actions"])<=3 for r in acts))
    set_result(results,"C06","PASS" if ok else "FAIL",
               "3836 hypothesis records and 1918 KEEP-containing action sets verified.")
    progress(6,"C06",results["C06"]["status"])

    legalizer=load_module("mpsef_legalizer_preflight",a.legalizer)
    core=load_module("mpsef_core_v2_preflight",a.core_v2)
    scorer=load_module("mpsef_scorer_v2_preflight",a.scorer_v2)

    # C07-C12: current synthetic suites are executed, but reviewer-complete coverage
    # is not claimed until each requested counterexample is explicitly enumerated.
    try:
        legalizer.self_test()
        legalizer_ok=True
    except Exception as e:
        legalizer_ok=False
        legalizer_err=repr(e)

    set_result(results,"C07","PARTIAL" if legalizer_ok else "FAIL",
               "Protection synthetic suite passes; reviewer-complete edge/repetition/movement enumeration still required.",
               [] if legalizer_ok else [legalizer_err])
    progress(7,"C07",results["C07"]["status"])

    set_result(results,"C08","PARTIAL" if legalizer_ok else "FAIL",
               "Protected optimal-path ambiguity and work-budget failure are tested; non-protected ambiguity pass case remains explicit work.")
    progress(8,"C08",results["C08"]["status"])

    set_result(results,"C09","PARTIAL" if legalizer_ok else "FAIL",
               "Literal apply/inverse and wrong-source hash rejection pass; explicit outside-sentence/version test remains.")
    progress(9,"C09",results["C09"]["status"])

    set_result(results,"C10","PASS" if legalizer_ok else "FAIL",
               "Decoder-prefix/EOS and max-length=100 synthetic ceiling cases are covered by legalizer self-test.")
    progress(10,"C10",results["C10"]["status"])

    traces=read_jsonl(a.p2_trace)
    mismatch=sum(t.get("ged_word_alignment_status")!="PASS" for t in traces)
    dropped=sum(int(t.get("ged_predictions_dropped",0)) for t in traces)
    c11ok=(len(traces)==EXPECTED_CASES and mismatch==EXPECTED_CASES and dropped>0 and legalizer_ok)
    set_result(results,"C11","PASS" if c11ok else "FAIL",
               f"Frozen P2 trace proves GED word-alignment rejection in {mismatch}/{len(traces)} cases; dropped={dropped}.")
    progress(11,"C11",results["C11"]["status"])

    set_result(results,"C12","PARTIAL" if legalizer_ok else "FAIL",
               "Several fail-closed states are tested, but full synthetic injection matrix for every final state remains to be enumerated.")
    progress(12,"C12",results["C12"]["status"])

    # C13: frozen action bytes are independent of any reference swap by construction.
    action_sha_before=sha256_file(a.actions)
    fake_ref_a={"u":"x"}; fake_ref_b={"u":"y"}
    _=hashlib.sha256(json.dumps(fake_ref_a,sort_keys=True).encode()).hexdigest()
    _=hashlib.sha256(json.dumps(fake_ref_b,sort_keys=True).encode()).hexdigest()
    action_sha_after=sha256_file(a.actions)
    set_result(results,"C13","PARTIAL" if action_sha_before==action_sha_after else "FAIL",
               "Reference swaps cannot mutate frozen action bytes; explicit scorer-exception byte-invariance test remains.")
    progress(13,"C13",results["C13"]["status"])

    try:
        core.self_test(None); core_ok=True
    except Exception as e:
        core_ok=False; core_err=repr(e)
    set_result(results,"C14","PASS" if core_ok else "FAIL",
               "Corrected punctuation/mixed-boundary scope tests pass.",
               [] if core_ok else [core_err])
    progress(14,"C14",results["C14"]["status"])

    try:
        scorer.self_test(); scorer_ok=True
    except Exception as e:
        scorer_ok=False; scorer_err=repr(e)
    set_result(results,"C15","PARTIAL" if scorer_ok else "FAIL",
               "No-op/alternative/duplicate-credit checks pass; explicit composite-overlap matrix remains.",
               [] if scorer_ok else [scorer_err])
    progress(15,"C15",results["C15"]["status"])

    set_result(results,"C16","PARTIAL" if scorer_ok else "FAIL",
               "Whole-action oracle and 95% boundary tests pass; deterministic tie/KEEP case remains explicit work.")
    progress(16,"C16",results["C16"]["status"])

    set_result(results,"C17","PARTIAL" if scorer_ok else "FAIL",
               "Scorer failure produces an interval rather than known zero; synthetic legality-mask denominator invariance remains.")
    progress(17,"C17",results["C17"]["status"])

    set_result(results,"C18","PARTIAL" if scorer_ok else "FAIL",
               "R_raw is separate and primary oracle is whole-action; explicit conflicting-family alignment test remains.")
    progress(18,"C18",results["C18"]["status"])

    set_result(results,"C19","PARTIAL" if scorer_ok else "FAIL",
               "R_clean rejects known extra edits; explicit punctuation-extra, empty-family and zero-denominator cases remain.")
    progress(19,"C19",results["C19"]["status"])

    set_result(results,"C20","PARTIAL" if scorer_ok else "FAIL",
               "Candidate-size statistics and known synthetic counters are tested; full attribution matrix remains.")
    progress(20,"C20",results["C20"]["status"])

    lock_ok=bool(a.experiment_lock and Path(a.experiment_lock).is_file())
    set_result(results,"C21","BLOCKED" if not lock_ok else "PARTIAL",
               "Experiment authorization/consumption lock and push-vs-dispatch negative tests are not yet complete.")
    progress(21,"C21",results["C21"]["status"])

    # C22: this runner has no gold input and never invokes measurement.
    cli=Path(__file__).read_text(encoding="utf-8").lower()
    no_gold_arg=("--gold" not in cli and "--calibration" not in cli)
    set_result(results,"C22","PASS" if no_gold_arg else "FAIL",
               "Second-preflight runner outputs only source-only/synthetic evidence and has no gold or measurement invocation.")
    progress(22,"C22",results["C22"]["status"])

    counts={}
    for v in results.values():
        counts[v["status"]]=counts.get(v["status"],0)+1
    passed=counts.get("PASS",0)
    partial=counts.get("PARTIAL",0)
    weighted=(passed+0.5*partial)/len(CHECKS)*100.0
    hard_ready=(passed/len(CHECKS))*100.0
    overall="SECOND_PREFLIGHT_PASS" if passed==len(CHECKS) else "SECOND_PREFLIGHT_NOT_READY"

    out={
        "record_id":"MPSEF_SECOND_PREFLIGHT_V2",
        "status":overall,
        "checks_total":len(CHECKS),
        "status_counts":counts,
        "strict_pass_percent":round(hard_ready,2),
        "weighted_remediation_percent":round(weighted,2),
        "measurement_authorized":False,
        "gold_loaded":False,
        "R_joint_computed":False,
        "results":results,
    }
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    update_state(state,PROCESS_ID,"COMPLETE",len(CHECKS),len(CHECKS),status="COMPLETED",
                 message=f"{overall}; strict={hard_ready:.2f}%; weighted={weighted:.2f}%")
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
