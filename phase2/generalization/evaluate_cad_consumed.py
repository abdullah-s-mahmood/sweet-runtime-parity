"""Evaluate frozen CAD consumed decisions only after feature materialization."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
F=ROOT/"PHASE2_CAD_CONSUMED_FEATURES.jsonl"
R=ROOT/"PHASE2_CAD_CONSUMED_RUNTIME.json"
THIRD_MANUAL=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_MANUAL_REVIEW.json"
OLD_AUTO=ROOT/"PHASE2_TRIMODEL_VOTING_RESULTS.json"
OLD_MANUAL=ROOT/"PHASE2_TRIMODEL_VOTING_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_CAD_CONSUMED_RESULTS.json"

SUPPORTED={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}
UNSAFE={"PARTIAL_CORRECTION","WRONG_CORRECTION","UNNECESSARY_EDIT"}

def jl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def eval_population(rows,labels):
    pas=[x for x in rows if x["runtime_decision"]=="PASS"]
    rev=[x for x in rows if x["runtime_decision"]=="REVIEW"]
    counts={}
    for x in pas:
        c=labels[x["vote_id"]];counts[c]=counts.get(c,0)+1
    supported=sum(labels[x["vote_id"]] in SUPPORTED for x in pas)
    partial=sum(labels[x["vote_id"]]=="PARTIAL_CORRECTION" for x in pas)
    wrong=sum(labels[x["vote_id"]]=="WRONG_CORRECTION" for x in pas)
    unnecessary=sum(labels[x["vote_id"]]=="UNNECESSARY_EDIT" for x in pas)
    return {
        "total":len(rows),"pass":len(pas),"review":len(rev),
        "pass_class_counts":counts,
        "supported_pass":supported,
        "partial_pass":partial,"wrong_pass":wrong,"unnecessary_pass":unnecessary,
        "unsafe_pass":partial+wrong+unnecessary,
        "pass_precision":supported/len(pas) if pas else None,
    }

def main():
    rt=json.loads(R.read_text(encoding="utf-8"))
    assert rt["current_labels_read"] is False
    assert rt["external_model_frozen"] is True

    rows=jl(F)
    third=[x for x in rows if x["population"]=="THIRD_V1_14"]
    old=[x for x in rows if x["population"]=="EARLIER_ORTHO_MORPH_36"]
    assert len(third)==14 and len(old)==36

    tm=json.loads(THIRD_MANUAL.read_text(encoding="utf-8"))
    third_partial={x["vote_id"] for x in tm["items"] if x["manual_class"]=="PARTIAL_CORRECTION"}
    third_wrong={x["vote_id"] for x in tm["items"] if x["manual_class"]=="WRONG_CORRECTION"}
    third_unnec={x["vote_id"] for x in tm["items"] if x["manual_class"]=="UNNECESSARY_EDIT"}
    assert len(third_partial)==2 and not third_wrong and not third_unnec
    third_labels={}
    for x in third:
        vid=x["vote_id"]
        third_labels[vid]="PARTIAL_CORRECTION" if vid in third_partial else "SUPPORTED_CORRECTION"
    assert sum(v in SUPPORTED for v in third_labels.values())==12

    auto=json.loads(OLD_AUTO.read_text(encoding="utf-8"))
    automatic={x["vote_id"]:x["classification"] for x in auto["policy_results"]["UNANIMOUS_3"]["event_audit_hashes"]}
    manual=json.loads(OLD_MANUAL.read_text(encoding="utf-8"))
    mm={x["vote_id"]:x["manual_class"] for x in manual["items"]}
    old_labels={}
    for x in old:
        vid=x["vote_id"]
        old_labels[vid]="SUPPORTED_CORRECTION" if automatic[vid]=="EXACT_GOLD_SUPPORTED" else mm[vid]
    assert sum(v in SUPPORTED for v in old_labels.values())==34
    assert sum(v=="PARTIAL_CORRECTION" for v in old_labels.values())==2
    assert sum(v=="WRONG_CORRECTION" for v in old_labels.values())==0
    assert sum(v=="UNNECESSARY_EDIT" for v in old_labels.values())==0

    third_res=eval_population(third,third_labels)
    old_res=eval_population(old,old_labels)

    strict=[x for x in old if x["strict_v1_member"]]
    assert len(strict)==19
    strict_res=eval_population(strict,old_labels)
    assert sum(old_labels[x["vote_id"]] in SUPPORTED for x in strict)==19

    third_ok=(
        third_res["pass"]>=10 and third_res["supported_pass"]>=10
        and third_res["partial_pass"]==0 and third_res["wrong_pass"]==0
        and third_res["unnecessary_pass"]==0
    )
    old_ok=(
        old_res["supported_pass"]>=24
        and old_res["partial_pass"]==0 and old_res["wrong_pass"]==0
        and old_res["unnecessary_pass"]==0
    )
    strict_ok=(
        strict_res["pass"]>=12 and strict_res["unsafe_pass"]==0
    )
    qualifies=third_ok and old_ok and strict_ok

    obj={
        "status":"PHASE2_CAD_FEASIBILITY_EVALUATED",
        "external_training_frozen":True,
        "features_frozen_before_current_labels":True,
        "third_v1_14":third_res,
        "earlier_ortho_morph_36":old_res,
        "earlier_strict_v1_19":strict_res,
        "criteria":{
            "third_slice_met":third_ok,
            "earlier_36_met":old_ok,
            "nested_strict_v1_met":strict_ok,
            "all_consumed_criteria_met":qualifies,
        },
        "status_for_next_step":"ELIGIBLE_TO_PREREGISTER_FOURTH_DISJOINT_VALIDATION" if qualifies else "CAD_FEASIBILITY_NOT_PROMISING",
        "fourth_slice_allowed":qualifies,
        "promotion_allowed":False,
        "qalb15_test_read":False,
        "qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in OUT.read_text(encoding="utf-8"))
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":main()
