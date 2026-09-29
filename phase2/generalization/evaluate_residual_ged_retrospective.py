"""Evaluate frozen retrospective GED target-clean decisions against closed historical labels."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
F=ROOT/"PHASE2_RESIDUAL_GED_RETROSPECTIVE_FEATURES.jsonl"
R=ROOT/"PHASE2_RESIDUAL_GED_RETROSPECTIVE_RUNTIME.json"
AUTO=ROOT/"PHASE2_TRIMODEL_VOTING_RESULTS.json"
MANUAL=ROOT/"PHASE2_TRIMODEL_VOTING_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_RESIDUAL_GED_RETROSPECTIVE_RESULTS.json"

SUPPORTED={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
UNSAFE={"PARTIAL_CORRECTION","WRONG_CORRECTION","UNNECESSARY_EDIT"}

def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rt=json.loads(R.read_text(encoding="utf-8"))
    assert rt["labels_read"] is False and rt["rows"]==36

    feats=jl(F)
    auto=json.loads(AUTO.read_text(encoding="utf-8"))
    audit=auto["policy_results"]["UNANIMOUS_3"]["event_audit_hashes"]
    automatic={x["vote_id"]:x["classification"] for x in audit}
    manual=json.loads(MANUAL.read_text(encoding="utf-8"))
    mm={x["vote_id"]:x for x in manual["items"]}

    labels={}
    for x in feats:
        vid=x["vote_id"]
        cls=automatic[vid]
        if cls=="EXACT_GOLD_SUPPORTED":
            labels[vid]="SUPPORTED_CORRECTION"
        else:
            labels[vid]=mm[vid]["manual_class"]

    label_counts={}
    for c in labels.values():label_counts[c]=label_counts.get(c,0)+1
    assert sum(labels[v] in SUPPORTED for v in labels)==34,label_counts
    assert sum(labels[v]=="PARTIAL_CORRECTION" for v in labels)==2,label_counts
    assert sum(labels[v]=="WRONG_CORRECTION" for v in labels)==0,label_counts
    assert sum(labels[v]=="UNNECESSARY_EDIT" for v in labels)==0,label_counts

    pas=[x for x in feats if x["runtime_decision"]=="PASS"]
    rev=[x for x in feats if x["runtime_decision"]=="REVIEW"]
    supported_pass=sum(labels[x["vote_id"]] in SUPPORTED for x in pas)
    partial_pass=sum(labels[x["vote_id"]]=="PARTIAL_CORRECTION" for x in pas)
    wrong_pass=sum(labels[x["vote_id"]]=="WRONG_CORRECTION" for x in pas)
    unnecessary_pass=sum(labels[x["vote_id"]]=="UNNECESSARY_EDIT" for x in pas)

    strict=[x for x in feats if x["strict_v1_member"]]
    strict_pass=[x for x in strict if x["runtime_decision"]=="PASS"]
    strict_unsafe_pass=sum(labels[x["vote_id"]] in UNSAFE for x in strict_pass)
    assert len(strict)==19
    assert sum(labels[x["vote_id"]] in SUPPORTED for x in strict)==19

    qualifies=(
      len(pas)>=28 and partial_pass==0 and wrong_pass==0 and unnecessary_pass==0
      and supported_pass>=28 and len(rev)<=8
      and len(strict_pass)>=15 and strict_unsafe_pass==0
    )
    obj={
      "status":"PHASE2_RESIDUAL_GED_RETROSPECTIVE_EVALUATED",
      "diagnostic_only":True,"consumed_population":True,
      "features_frozen_before_labels":True,
      "rule_version":"GED_TARGET_CLEAN_BOTH",
      "population_total":len(feats),"population_label_counts":label_counts,
      "pass":len(pas),"review":len(rev),"review_burden":len(rev)/len(feats),
      "supported_pass":supported_pass,
      "supported_retention":supported_pass/34,
      "partial_pass":partial_pass,"partial_captured":2-partial_pass,
      "wrong_pass":wrong_pass,"unnecessary_pass":unnecessary_pass,
      "pass_precision":supported_pass/len(pas) if pas else None,
      "strict_v1_total":len(strict),"strict_v1_pass":len(strict_pass),
      "strict_v1_retention":len(strict_pass)/19,
      "strict_v1_unsafe_pass":strict_unsafe_pass,
      "pre_registered_criterion_met":qualifies,
      "status_for_next_step":"ELIGIBLE_FOR_FOURTH_DISJOINT_VALIDATION" if qualifies else "CLOSE_HYPOTHESIS_DO_NOT_SPEND_FRESH_SLICE",
      "promotion_allowed":False,
      "fourth_slice_allowed":qualifies,
      "qalb15_test_read":False,"qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in OUT.read_text(encoding="utf-8"))
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":main()
