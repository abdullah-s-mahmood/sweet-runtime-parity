"""Evaluate frozen local-edit semantic backstop decisions.

This stage reads prior cross-model gold classification/manual adjudication only
after semantic runtime decisions are materialized.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FEATURES=ROOT/"PHASE2_LOCAL_EDIT_SEMANTIC_BACKSTOP_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_LOCAL_EDIT_SEMANTIC_BACKSTOP_RUNTIME.json"
AUTO=ROOT/"PHASE2_CROSS_MODEL_AGREEMENT_RESULTS.json"
MANUAL=ROOT/"PHASE2_CROSS_MODEL_AGREEMENT_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_LOCAL_EDIT_SEMANTIC_BACKSTOP_RESULTS.json"

SUPPORTED={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
UNSAFE={"WRONG_CORRECTION","PARTIAL_CORRECTION","UNNECESSARY_EDIT"}

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    runtime=json.loads(RUNTIME.read_text(encoding="utf-8"))
    assert runtime["labels_or_gold_read"] is False
    assert runtime["thresholds_frozen_before_labels"] is True
    feats=jl(FEATURES)

    auto=json.loads(AUTO.read_text(encoding="utf-8"))
    audit=auto["policy_results"]["EXACT_SINGLE_SUB_AGREEMENT"]["event_audit_hashes"]
    automatic={x["agreement_id"]:x["classification"] for x in audit}
    manual=json.loads(MANUAL.read_text(encoding="utf-8"))
    manual_map={x["agreement_id"]:x for x in manual["items"]}

    labels={}
    severities={}
    for x in feats:
        aid=x["agreement_id"]
        cls=automatic[aid]
        if cls=="EXACT_GOLD_SUPPORTED":
            labels[aid]="SUPPORTED_CORRECTION"
            severities[aid]="LOW"
        else:
            m=manual_map.get(aid)
            assert m is not None,(aid,cls)
            labels[aid]=m["manual_class"]
            severities[aid]=m.get("severity","UNKNOWN")

    counts={}
    for c in labels.values():counts[c]=counts.get(c,0)+1
    assert sum(counts.values())==159,counts
    supported_total=sum(c in SUPPORTED for c in labels.values())
    unsafe_total=sum(c in UNSAFE for c in labels.values())

    results={}
    for policy in feats[0]["runtime_decisions"]:
        rev=[x for x in feats if x["runtime_decisions"][policy]=="REVIEW"]
        pas=[x for x in feats if x["runtime_decisions"][policy]=="PASS"]
        def n(rows,klass):
            return sum(labels[x["agreement_id"]]==klass for x in rows)
        supported_review=sum(labels[x["agreement_id"]] in SUPPORTED for x in rev)
        supported_pass=sum(labels[x["agreement_id"]] in SUPPORTED for x in pas)
        unsafe_review=sum(labels[x["agreement_id"]] in UNSAFE for x in rev)
        unsafe_pass=sum(labels[x["agreement_id"]] in UNSAFE for x in pas)
        wrong_review=n(rev,"WRONG_CORRECTION")
        partial_review=n(rev,"PARTIAL_CORRECTION")
        unnecessary_review=n(rev,"UNNECESSARY_EDIT")
        highcrit_unsafe_review=sum(
            labels[x["agreement_id"]] in UNSAFE
            and severities[x["agreement_id"]] in {"HIGH","CRITICAL"}
            for x in rev
        )
        highcrit_unsafe_total=sum(
            labels[x["agreement_id"]] in UNSAFE
            and severities[x["agreement_id"]] in {"HIGH","CRITICAL"}
            for x in feats
        )
        review_burden=len(rev)/len(feats)
        supported_retention=supported_pass/supported_total if supported_total else None
        unsafe_capture=unsafe_review/unsafe_total if unsafe_total else None
        wrong_total=sum(c=="WRONG_CORRECTION" for c in labels.values())
        wrong_capture=wrong_review/wrong_total if wrong_total else None
        residual_precision=supported_pass/(supported_pass+unsafe_pass) if supported_pass+unsafe_pass else None
        promising=(
            unsafe_capture>=0.50
            and wrong_capture>=0.50
            and supported_retention>=0.80
            and review_burden<=0.25
        )
        results[policy]={
            "pass":len(pas),
            "review":len(rev),
            "review_burden":review_burden,
            "supported_total":supported_total,
            "supported_retained":supported_pass,
            "supported_false_review":supported_review,
            "supported_retention":supported_retention,
            "unsafe_total":unsafe_total,
            "unsafe_captured":unsafe_review,
            "unsafe_residual_pass":unsafe_pass,
            "unsafe_capture":unsafe_capture,
            "wrong_captured":wrong_review,
            "wrong_total":wrong_total,
            "wrong_capture":wrong_capture,
            "partial_captured":partial_review,
            "unnecessary_captured":unnecessary_review,
            "high_or_critical_unsafe_captured":highcrit_unsafe_review,
            "high_or_critical_unsafe_total":highcrit_unsafe_total,
            "residual_pass_precision":residual_precision,
            "status":"PROMISING_FOR_FRESH_VALIDATION" if promising else "NOT_PROMISING_ON_CONSUMED_SLICE",
        }

    result={
        "status":"PHASE2_LOCAL_EDIT_SEMANTIC_BACKSTOP_DIAGNOSTIC_EVALUATED",
        "diagnostic_only":True,
        "consumed_population":True,
        "runtime_decisions_materialized_before_labels":True,
        "population_label_counts":counts,
        "policy_results":results,
        "promotion_allowed_from_this_slice":False,
        "next_rule":"Only a pre-registered promising policy may be copied unchanged to a fresh disjoint validation slice.",
        "qalb15_test_read":False,
        "qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped),"Arabic/QALB text leaked"
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":
    main()
