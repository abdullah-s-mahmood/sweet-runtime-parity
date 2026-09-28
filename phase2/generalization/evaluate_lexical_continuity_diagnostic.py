"""Evaluate frozen lexical continuity flags against prior hash-only adjudication."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FEAT=ROOT/"artifacts"/"LEXICAL_CONTINUITY_FEATURES.jsonl"
MAN=ROOT/"PHASE2_CROSS_MODEL_AGREEMENT_MANUAL_REVIEW.json"
RESULT=ROOT/"PHASE2_LEXICAL_CONTINUITY_DIAGNOSTIC_RESULTS.json"

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rows=jl(FEAT)
    man=json.loads(MAN.read_text(encoding="utf-8"))
    manual={x["agreement_id"]:x for x in man["items"]}
    labels={}
    for r in rows:
        x=manual.get(r["agreement_id"])
        labels[r["agreement_id"]]=(
            {"class":x["manual_class"],"severity":x["severity"]}
            if x else {"class":"SUPPORTED_CORRECTION","severity":"LOW"}
        )
    supported={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
    policies={}
    for p in ("LEXEME_DISJOINT_VETO","LEXEME_AND_ROOT_DISJOINT_VETO","CANDIDATE_UNANALYZABLE_ONLY"):
        review=[r for r in rows if r["runtime_decisions"][p]=="REVIEW"]
        keep=[r for r in rows if r["runtime_decisions"][p]=="KEEP_ACCEPT"]
        total_supported=sum(labels[x["agreement_id"]]["class"] in supported for x in rows)
        total_wrong=sum(labels[x["agreement_id"]]["class"]=="WRONG_CORRECTION" for x in rows)
        total_unsafe=sum(labels[x["agreement_id"]]["class"] not in supported for x in rows)
        kept_supported=sum(labels[x["agreement_id"]]["class"] in supported for x in keep)
        captured_wrong=sum(labels[x["agreement_id"]]["class"]=="WRONG_CORRECTION" for x in review)
        captured_unsafe=sum(labels[x["agreement_id"]]["class"] not in supported for x in review)
        high_wrong_captured=sum(
            labels[x["agreement_id"]]["class"]=="WRONG_CORRECTION"
            and labels[x["agreement_id"]]["severity"] in ("HIGH","CRITICAL")
            for x in review
        )
        policies[p]={
            "review":len(review),"keep_accept":len(keep),
            "supported_retained":kept_supported,"supported_total":total_supported,
            "supported_retention":kept_supported/total_supported if total_supported else None,
            "wrong_captured":captured_wrong,"wrong_total":total_wrong,
            "wrong_capture_recall":captured_wrong/total_wrong if total_wrong else None,
            "unsafe_captured":captured_unsafe,"unsafe_total":total_unsafe,
            "unsafe_capture_recall":captured_unsafe/total_unsafe if total_unsafe else None,
            "high_or_critical_wrong_captured":high_wrong_captured,
            "wrong_remaining_in_keep":sum(labels[x["agreement_id"]]["class"]=="WRONG_CORRECTION" for x in keep),
            "partial_remaining_in_keep":sum(labels[x["agreement_id"]]["class"]=="PARTIAL_CORRECTION" for x in keep),
            "unnecessary_remaining_in_keep":sum(labels[x["agreement_id"]]["class"]=="UNNECESSARY_EDIT" for x in keep),
            "keep_accept_supported_precision":kept_supported/len(keep) if keep else None,
        }

    def interpretation(v):
        if v["wrong_capture_recall"]>=0.75 and v["supported_retention"]>=0.90:return "STRONG_SIGNAL"
        if v["wrong_capture_recall"]>=0.50 and v["supported_retention"]>=0.90:return "PROMISING_SIGNAL"
        return "WEAK_OR_UNHELPFUL"

    result={
        "status":"PHASE2_LEXICAL_CONTINUITY_DIAGNOSTIC_EVALUATED",
        "diagnostic_only":True,
        "same_consumed_cross_corpus_slice":True,
        "runtime_features_materialized_before_manual_labels_loaded":True,
        "rows":len(rows),
        "policy_results":{p:{**v,"pre_registered_interpretation":interpretation(v)} for p,v in policies.items()},
        "promotion_rule":"No policy can be promoted from this diagnostic. A promising/strong lexical veto must be frozen and tested unchanged on fresh disjoint evidence.",
        "qalb15_test_read":False,
    }
    RESULT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":
    main()
