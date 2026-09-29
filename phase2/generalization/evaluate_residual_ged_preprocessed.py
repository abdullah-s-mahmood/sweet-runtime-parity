"""Evaluate preprocessing-faithful residual GED decisions on consumed labels."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
F=ROOT/"PHASE2_RESIDUAL_GED_PREPROCESSED_FEATURES.jsonl"
R=ROOT/"PHASE2_RESIDUAL_GED_PREPROCESSED_RUNTIME.json"
M=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_RESIDUAL_GED_PREPROCESSED_RESULTS.json"

def jl(p):return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rt=json.loads(R.read_text(encoding="utf-8"))
    assert rt["labels_read"] is False and rt["preprocessing_faithful"] is True
    feats=jl(F);manual=json.loads(M.read_text(encoding="utf-8"))
    partial={x["vote_id"] for x in manual["items"] if x["manual_class"]=="PARTIAL_CORRECTION"}
    labels={x["vote_id"]:("PARTIAL" if x["vote_id"] in partial else "SUPPORTED") for x in feats}
    assert len(partial)==2 and sum(v=="SUPPORTED" for v in labels.values())==12

    results={}
    for p in feats[0]["runtime_decisions"]:
        pas=[x for x in feats if x["runtime_decisions"][p]=="PASS"]
        rev=[x for x in feats if x["runtime_decisions"][p]=="REVIEW"]
        sp=sum(labels[x["vote_id"]]=="SUPPORTED" for x in pas)
        pp=sum(labels[x["vote_id"]]=="PARTIAL" for x in pas)
        qualifies=len(pas)>=10 and pp==0 and sp>=10 and len(rev)<=4
        results[p]={
          "pass":len(pas),"review":len(rev),"review_burden":len(rev)/14,
          "supported_pass":sp,"partial_pass":pp,"partial_captured":2-pp,
          "supported_retained":sp,"supported_retention":sp/12,
          "status":"PROMISING_FOR_RETROSPECTIVE_REPLICATION" if qualifies else "NOT_PROMISING",
        }
    obj={
      "status":"PHASE2_RESIDUAL_GED_PREPROCESSED_EVALUATED",
      "diagnostic_only":True,"consumed_population":True,
      "features_frozen_before_labels":True,
      "preprocessing_faithful":True,
      "preprocessing_already_candidate_count":rt["preprocessing_already_candidate_count"],
      "policy_results":results,
      "target_rule_promising":results["GED_TARGET_CLEAN_BOTH"]["status"].startswith("PROMISING"),
      "promotion_allowed":False,"fourth_slice_allowed":False,
      "next_action":"RETROSPECTIVE_REPLICATION_ON_EARLIER_CONSUMED_POPULATION" if results["GED_TARGET_CLEAN_BOTH"]["status"].startswith("PROMISING") else "CLOSE_RESIDUAL_GED_TARGET_CLEAN",
      "qalb15_test_read":False,"qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in OUT.read_text(encoding="utf-8"))
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":main()
