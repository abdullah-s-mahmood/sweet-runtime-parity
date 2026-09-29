"""Evaluate frozen retrospective GED target-clean decisions against prior adjudication."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
F=ROOT/"PHASE2_RESIDUAL_GED_TARGET_RETROSPECTIVE_FEATURES.jsonl"
R=ROOT/"PHASE2_RESIDUAL_GED_TARGET_RETROSPECTIVE_RUNTIME.json"
AUTO=ROOT/"PHASE2_TRIMODEL_VOTING_RESULTS.json"
MANUAL=ROOT/"PHASE2_TRIMODEL_VOTING_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_RESIDUAL_GED_TARGET_RETROSPECTIVE_RESULTS.json"

SUPPORTED={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
UNSAFE={"PARTIAL_CORRECTION","WRONG_CORRECTION","UNNECESSARY_EDIT"}

def jl(p):return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rt=json.loads(R.read_text(encoding="utf-8"));assert rt["labels_read"] is False
    feats=jl(F);assert len(feats)==36
    auto=json.loads(AUTO.read_text(encoding="utf-8"))
    audit=auto["policy_results"]["UNANIMOUS_3"]["event_audit_hashes"]
    automatic={x["vote_id"]:x["classification"] for x in audit}
    manual=json.loads(MANUAL.read_text(encoding="utf-8"))
    mm={x["vote_id"]:x for x in manual["items"]}
    labels={}
    for x in feats:
        vid=x["vote_id"];cls=automatic[vid]
        labels[vid]="SUPPORTED_CORRECTION" if cls=="EXACT_GOLD_SUPPORTED" else mm[vid]["manual_class"]

    pas=[x for x in feats if x["runtime_decision"]=="PASS"]
    rev=[x for x in feats if x["runtime_decision"]=="REVIEW"]
    strict=[x for x in feats if x["strict_v1_subset"]]
    strict_pass=[x for x in strict if x["runtime_decision"]=="PASS"]
    counts={}
    for x in pas:
        c=labels[x["vote_id"]];counts[c]=counts.get(c,0)+1
    supported=sum(labels[x["vote_id"]] in SUPPORTED for x in pas)
    wrong=sum(labels[x["vote_id"]]=="WRONG_CORRECTION" for x in pas)
    partial=sum(labels[x["vote_id"]]=="PARTIAL_CORRECTION" for x in pas)
    unnecessary=sum(labels[x["vote_id"]]=="UNNECESSARY_EDIT" for x in pas)
    unsafe=wrong+partial+unnecessary
    qualifies=len(pas)>=10 and wrong==0 and partial==0 and unnecessary==0 and len(strict_pass)>=10
    obj={
      "status":"PHASE2_RESIDUAL_GED_TARGET_RETROSPECTIVE_EVALUATED",
      "diagnostic_only":True,"consumed_population":True,"features_frozen_before_labels":True,
      "population_total":36,"population_historical_supported":34,"population_historical_partial":2,
      "accepted":len(pas),"review":len(rev),"accepted_class_counts":counts,
      "accepted_supported":supported,"accepted_unsafe":unsafe,
      "accepted_wrong":wrong,"accepted_partial":partial,"accepted_unnecessary":unnecessary,
      "accepted_precision":supported/len(pas) if pas else None,
      "strict_v1_subset_total":len(strict),"strict_v1_subset_pass":len(strict_pass),
      "strict_v1_subset_supported_pass":sum(labels[x["vote_id"]] in SUPPORTED for x in strict_pass),
      "pre_registered_promising_criterion_met":qualifies,
      "status_for_next_step":"ELIGIBLE_FOR_FOURTH_SLICE_PREREGISTRATION" if qualifies else "NOT_PROMISING",
      "promotion_allowed":False,"qalb15_test_read":False,"qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in OUT.read_text(encoding="utf-8"))
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":main()
