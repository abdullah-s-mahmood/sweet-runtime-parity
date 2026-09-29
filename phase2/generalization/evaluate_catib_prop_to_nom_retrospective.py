"""Evaluate frozen CATiB PROP-to-NOM retrospective decisions after feature freeze."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FEAT=ROOT/"PHASE2_CATIB_PROP_TO_NOM_FEATURES.jsonl"
RT=ROOT/"PHASE2_CATIB_PROP_TO_NOM_RUNTIME.json"
AUTO=ROOT/"PHASE2_TRIMODEL_VOTING_RESULTS.json"
MAN=ROOT/"PHASE2_TRIMODEL_VOTING_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_CATIB_PROP_TO_NOM_RESULTS.json"
SUPPORTED={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
UNSAFE={"PARTIAL_CORRECTION","WRONG_CORRECTION","UNNECESSARY_EDIT"}

def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rt=json.loads(RT.read_text(encoding="utf-8"))
    assert rt["labels_or_gold_read"] is False and rt["rule_frozen_before_labels"] is True
    feat=jl(FEAT);assert len(feat)==36
    auto=json.loads(AUTO.read_text(encoding="utf-8"))
    audit=auto["policy_results"]["UNANIMOUS_3"]["event_audit_hashes"]
    amap={x["vote_id"]:x["classification"] for x in audit}
    man=json.loads(MAN.read_text(encoding="utf-8"));mmap={x["vote_id"]:x for x in man["items"]}
    labels={}
    for x in feat:
        vid=x["vote_id"]
        if amap[vid]=="EXACT_GOLD_SUPPORTED": labels[vid]="SUPPORTED_CORRECTION"
        else: labels[vid]=mmap[vid]["manual_class"]

    pas=[x for x in feat if x["runtime_decision"]=="PASS"]
    v1=[x for x in feat if x["strict_v1_pass"]]
    v1pas=[x for x in v1 if x["runtime_decision"]=="PASS"]
    counts={}
    for x in pas:
        c=labels[x["vote_id"]];counts[c]=counts.get(c,0)+1
    supported=sum(labels[x["vote_id"]] in SUPPORTED for x in pas)
    unsafe=sum(labels[x["vote_id"]] in UNSAFE for x in pas)
    wrong=sum(labels[x["vote_id"]]=="WRONG_CORRECTION" for x in pas)
    partial=sum(labels[x["vote_id"]]=="PARTIAL_CORRECTION" for x in pas)
    unnecessary=sum(labels[x["vote_id"]]=="UNNECESSARY_EDIT" for x in pas)
    v1_supported=sum(labels[x["vote_id"]] in SUPPORTED for x in v1pas)
    criterion=(len(pas)>=10 and wrong==0 and partial==0 and unnecessary==0 and len(v1pas)>=10)
    obj={
      "status":"CATIB_PROP_TO_NOM_RETROSPECTIVE_EVALUATED",
      "diagnostic_only":True,"consumed_population":True,
      "rule_version":"CATIB_PROP_TO_NOM_EVIDENCE_V1",
      "population_total":36,"accepted":len(pas),"review":36-len(pas),
      "accepted_class_counts":counts,"accepted_supported":supported,"accepted_unsafe":unsafe,
      "accepted_wrong":wrong,"accepted_partial":partial,"accepted_unnecessary":unnecessary,
      "accepted_precision":supported/len(pas) if pas else None,
      "strict_v1_subset_total":len(v1),"strict_v1_subset_accepted":len(v1pas),
      "strict_v1_subset_accepted_supported":v1_supported,
      "pre_registered_promising_criterion_met":criterion,
      "status_for_next_step":"PROMISING_FOR_FRESH_VALIDATION" if criterion else "NOT_PROMISING",
      "promotion_allowed":False,
      "fresh_validation_allowed_only_if_pre_registered_again":criterion,
      "qalb15_test_read":False,"qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in OUT.read_text(encoding="utf-8"))
    print(json.dumps(obj))

if __name__=="__main__":main()
