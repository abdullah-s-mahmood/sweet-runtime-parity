"""Evaluate frozen contextual contradiction flags against prior hash-only adjudication.

Diagnostic only. Runtime features already exist.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FEAT=ROOT/"artifacts"/"CONTEXTUAL_CONTRADICTION_FEATURES.jsonl"
MAN=ROOT/"PHASE2_CROSS_MODEL_AGREEMENT_MANUAL_REVIEW.json"
RESULT=ROOT/"PHASE2_CONTEXTUAL_CONTRADICTION_DIAGNOSTIC_RESULTS.json"

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rows=jl(FEAT)
    man=json.loads(MAN.read_text(encoding="utf-8"))
    manual={x["agreement_id"]:x for x in man["items"]}
    # Exact-gold-supported primary events were not manually listed; they are supported correction.
    labels={}
    for r in rows:
        x=manual.get(r["agreement_id"])
        if x:
            labels[r["agreement_id"]]={"class":x["manual_class"],"severity":x["severity"]}
        else:
            labels[r["agreement_id"]]={"class":"SUPPORTED_CORRECTION","severity":"LOW"}

    supported={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
    policies={}
    for p in ("GED_CONTRADICTION","GED_OR_NO_MORPH"):
        review=[r for r in rows if r["runtime_decisions"][p]=="REVIEW"]
        keep=[r for r in rows if r["runtime_decisions"][p]=="KEEP_ACCEPT"]
        def count(rs,cls):
            return sum(labels[x["agreement_id"]]["class"]==cls for x in rs)
        total_supported=sum(labels[x["agreement_id"]]["class"] in supported for x in rows)
        total_wrong=sum(labels[x["agreement_id"]]["class"]=="WRONG_CORRECTION" for x in rows)
        total_unsafe=sum(labels[x["agreement_id"]]["class"] not in supported for x in rows)
        kept_supported=sum(labels[x["agreement_id"]]["class"] in supported for x in keep)
        captured_wrong=sum(labels[x["agreement_id"]]["class"]=="WRONG_CORRECTION" for x in review)
        captured_unsafe=sum(labels[x["agreement_id"]]["class"] not in supported for x in review)
        kept_wrong=sum(labels[x["agreement_id"]]["class"]=="WRONG_CORRECTION" for x in keep)
        kept_partial=sum(labels[x["agreement_id"]]["class"]=="PARTIAL_CORRECTION" for x in keep)
        kept_unnecessary=sum(labels[x["agreement_id"]]["class"]=="UNNECESSARY_EDIT" for x in keep)
        policies[p]={
            "review":len(review),"keep_accept":len(keep),
            "supported_retained":kept_supported,
            "supported_total":total_supported,
            "supported_retention":kept_supported/total_supported if total_supported else None,
            "wrong_captured":captured_wrong,
            "wrong_total":total_wrong,
            "wrong_capture_recall":captured_wrong/total_wrong if total_wrong else None,
            "unsafe_captured":captured_unsafe,
            "unsafe_total":total_unsafe,
            "unsafe_capture_recall":captured_unsafe/total_unsafe if total_unsafe else None,
            "wrong_remaining_in_keep":kept_wrong,
            "partial_remaining_in_keep":kept_partial,
            "unnecessary_remaining_in_keep":kept_unnecessary,
            "keep_accept_supported_precision":kept_supported/len(keep) if keep else None,
            "review_ids":[x["agreement_id"] for x in review],
        }

    result={
        "status":"PHASE2_CONTEXTUAL_CONTRADICTION_DIAGNOSTIC_EVALUATED",
        "diagnostic_only":True,
        "same_consumed_cross_corpus_slice":True,
        "runtime_features_materialized_before_manual_labels_loaded":True,
        "rows":len(rows),
        "policy_results":policies,
        "backoff_diagnostic":{
            "rows":sum(x["features"]["backoff_or_nounprop_fallback"] for x in rows)
        },
        "promotion_rule":"No policy can be promoted from this diagnostic; any promising veto must be frozen and tested on a fresh disjoint slice.",
        "qalb15_test_read":False
    }
    RESULT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({**result,"policy_results":{k:{kk:vv for kk,vv in v.items() if kk!="review_ids"} for k,v in policies.items()}},ensure_ascii=False))

if __name__=="__main__":
    main()
