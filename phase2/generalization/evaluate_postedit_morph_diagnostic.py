"""Evaluate frozen post-edit stability/morphology decisions after label freeze."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FEATURES=ROOT/"PHASE2_POSTEDIT_MORPH_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_POSTEDIT_MORPH_RUNTIME.json"
AUTO=ROOT/"PHASE2_TRIMODEL_VOTING_RESULTS.json"
MANUAL=ROOT/"PHASE2_TRIMODEL_VOTING_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_POSTEDIT_MORPH_RESULTS.json"

SUPPORTED={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
UNSAFE={"WRONG_CORRECTION","PARTIAL_CORRECTION","UNNECESSARY_EDIT"}

def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    runtime=json.loads(RUNTIME.read_text(encoding="utf-8"))
    assert runtime["labels_or_gold_read"] is False
    assert runtime["policy_frozen_before_labels"] is True
    feats=jl(FEATURES)

    auto=json.loads(AUTO.read_text(encoding="utf-8"))
    audit=auto["policy_results"]["UNANIMOUS_3"]["event_audit_hashes"]
    relation={x["vote_id"]:x["classification"] for x in audit}
    manual=json.loads(MANUAL.read_text(encoding="utf-8"))
    mmap={x["vote_id"]:x for x in manual["items"]}

    labels={};severity={}
    for x in feats:
        vid=x["vote_id"]
        if relation[vid]=="EXACT_GOLD_SUPPORTED":
            labels[vid]="SUPPORTED_CORRECTION";severity[vid]="LOW"
        else:
            m=mmap[vid]
            labels[vid]=m["manual_class"];severity[vid]=m["severity"]

    counts={}
    for v in labels.values():counts[v]=counts.get(v,0)+1
    assert counts.get("SUPPORTED_CORRECTION",0)+counts.get("SUPPORTED_ALTERNATIVE",0)==126,counts
    assert sum(counts.get(x,0) for x in UNSAFE)==16,counts

    supported_total=126; unsafe_total=16; wrong_total=4
    high_wrong_total=sum(labels[x["vote_id"]]=="WRONG_CORRECTION" and severity[x["vote_id"]]=="HIGH" for x in feats)

    results={}
    for policy in feats[0]["runtime_decisions"]:
        rev=[x for x in feats if x["runtime_decisions"][policy]=="REVIEW"]
        pas=[x for x in feats if x["runtime_decisions"][policy]=="PASS"]
        sup_pass=sum(labels[x["vote_id"]] in SUPPORTED for x in pas)
        sup_rev=supported_total-sup_pass
        unsafe_rev=sum(labels[x["vote_id"]] in UNSAFE for x in rev)
        unsafe_pass=unsafe_total-unsafe_rev
        wrong_rev=sum(labels[x["vote_id"]]=="WRONG_CORRECTION" for x in rev)
        partial_rev=sum(labels[x["vote_id"]]=="PARTIAL_CORRECTION" for x in rev)
        unnec_rev=sum(labels[x["vote_id"]]=="UNNECESSARY_EDIT" for x in rev)
        high_wrong_rev=sum(labels[x["vote_id"]]=="WRONG_CORRECTION" and severity[x["vote_id"]]=="HIGH" for x in rev)
        burden=len(rev)/len(feats)
        retention=sup_pass/supported_total
        unsafe_capture=unsafe_rev/unsafe_total
        wrong_capture=wrong_rev/wrong_total
        precision=sup_pass/(sup_pass+unsafe_pass) if sup_pass+unsafe_pass else None
        promising=(
            unsafe_capture>=0.50
            and wrong_capture>=0.75
            and high_wrong_rev==high_wrong_total
            and retention>=0.80
            and burden<=0.30
        )
        results[policy]={
            "pass":len(pas),"review":len(rev),"review_burden":burden,
            "supported_total":supported_total,"supported_retained":sup_pass,
            "supported_false_review":sup_rev,"supported_retention":retention,
            "unsafe_total":unsafe_total,"unsafe_captured":unsafe_rev,
            "unsafe_residual_pass":unsafe_pass,"unsafe_capture":unsafe_capture,
            "wrong_total":wrong_total,"wrong_captured":wrong_rev,"wrong_capture":wrong_capture,
            "partial_captured":partial_rev,"unnecessary_captured":unnec_rev,
            "high_wrong_total":high_wrong_total,"high_wrong_captured":high_wrong_rev,
            "residual_pass_precision":precision,
            "status":"PROMISING_FOR_FRESH_VALIDATION" if promising else "NOT_PROMISING_ON_CONSUMED_SLICE",
        }

    obj={
        "status":"PHASE2_POSTEDIT_MORPH_DIAGNOSTIC_EVALUATED",
        "diagnostic_only":True,
        "consumed_population":True,
        "runtime_decisions_materialized_before_labels":True,
        "population_label_counts":counts,
        "policy_results":results,
        "promotion_allowed_from_this_slice":False,
        "fresh_validation_allowed_for":[p for p,v in results.items() if v["status"]=="PROMISING_FOR_FRESH_VALIDATION"],
        "qalb15_test_read":False,
        "qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped),"Arabic text leaked"
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":
    main()
