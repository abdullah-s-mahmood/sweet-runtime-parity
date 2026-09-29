"""Evaluate frozen contextual residual-risk guard decisions against prior adjudication."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FEATURES=ROOT/"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_RUNTIME.json"
AUTO=ROOT/"PHASE2_TRIMODEL_VOTING_RESULTS.json"
MANUAL=ROOT/"PHASE2_TRIMODEL_VOTING_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_RESULTS.json"

SUPPORTED={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
UNSAFE={"PARTIAL_CORRECTION","WRONG_CORRECTION","UNNECESSARY_EDIT"}

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rt=json.loads(RUNTIME.read_text(encoding="utf-8"))
    assert rt["labels_or_gold_read"] is False and rt["rules_frozen_before_labels"] is True
    feats=jl(FEATURES); assert len(feats)==142

    auto=json.loads(AUTO.read_text(encoding="utf-8"))
    audit=auto["policy_results"]["UNANIMOUS_3"]["event_audit_hashes"]
    automatic={x["vote_id"]:x["classification"] for x in audit}
    manual=json.loads(MANUAL.read_text(encoding="utf-8"))
    mm={x["vote_id"]:x for x in manual["items"]}

    labels={};severity={}
    for x in feats:
        vid=x["vote_id"]; cls=automatic[vid]
        if cls=="EXACT_GOLD_SUPPORTED":
            labels[vid]="SUPPORTED_CORRECTION";severity[vid]="LOW"
        else:
            m=mm[vid];labels[vid]=m["manual_class"];severity[vid]=m["severity"]

    base_counts={}
    for c in labels.values():base_counts[c]=base_counts.get(c,0)+1

    results={}
    for p in feats[0]["runtime_decisions"]:
        pas=[x for x in feats if x["runtime_decisions"][p]=="PASS"]
        rev=[x for x in feats if x["runtime_decisions"][p]=="REVIEW"]
        pc={}
        for x in pas:
            c=labels[x["vote_id"]];pc[c]=pc.get(c,0)+1
        supported=sum(labels[x["vote_id"]] in SUPPORTED for x in pas)
        unsafe=sum(labels[x["vote_id"]] in UNSAFE for x in pas)
        wrong=sum(labels[x["vote_id"]]=="WRONG_CORRECTION" for x in pas)
        partial=sum(labels[x["vote_id"]]=="PARTIAL_CORRECTION" for x in pas)
        unnecessary=sum(labels[x["vote_id"]]=="UNNECESSARY_EDIT" for x in pas)
        high=sum(labels[x["vote_id"]] in UNSAFE and severity[x["vote_id"]] in {"HIGH","CRITICAL"} for x in pas)
        precision=supported/len(pas) if pas else None
        qualifies=len(pas)>=10 and wrong==0 and partial==0 and unnecessary==0
        results[p]={
          "pass":len(pas),"review":len(rev),"review_burden":len(rev)/len(feats),
          "pass_class_counts":pc,
          "supported_pass":supported,"unsafe_pass":unsafe,
          "wrong_pass":wrong,"partial_pass":partial,"unnecessary_pass":unnecessary,
          "high_or_critical_unsafe_pass":high,
          "pass_precision":precision,
          "status":"ELIGIBLE_FOR_FRESH_VALIDATION" if qualifies else "NOT_ELIGIBLE",
        }

    obj={
      "status":"PHASE2_CONTEXTUAL_RESIDUAL_GUARD_DIAGNOSTIC_EVALUATED",
      "diagnostic_only":True,
      "population":"consumed 142 UNANIMOUS_3 events",
      "population_label_counts":base_counts,
      "policy_results":results,
      "promotion_allowed_from_this_slice":False,
      "fresh_validation_allowed_only_if_eligible":True,
      "qalb15_test_read":False,"qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped)
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":main()
