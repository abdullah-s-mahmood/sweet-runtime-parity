"""Descriptive evaluation of already-frozen dependency features.

No acceptance rule is optimized or promoted here.
"""
from __future__ import annotations
import json
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FEATURES=ROOT/"PHASE2_DEPENDENCY_GOVERNOR_FEATURES.jsonl"
RUNTIME=ROOT/"PHASE2_DEPENDENCY_GOVERNOR_RUNTIME.json"
MANUAL=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_DEPENDENCY_GOVERNOR_RESULTS.json"

def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rt=json.loads(RUNTIME.read_text(encoding="utf-8"))
    assert rt["labels_or_gold_read"] is False and rt["rule_defined"] is False
    feats=jl(FEATURES);assert len(feats)==14
    man=json.loads(MANUAL.read_text(encoding="utf-8"))
    mmap={x["vote_id"]:x["manual_class"] for x in man["items"]}
    labels={x["vote_id"]:mmap.get(x["vote_id"],"SUPPORTED_CORRECTION") for x in feats}

    groups=defaultdict(list)
    for x in feats:
        cls="PARTIAL" if labels[x["vote_id"]]=="PARTIAL_CORRECTION" else "SUPPORTED"
        groups[cls].append(x)
    assert len(groups["PARTIAL"])==2 and len(groups["SUPPORTED"])==12

    change_keys=sorted(feats[0]["changed"])
    changes={}
    for k in change_keys:
        changes[k]={
          cls:sum(bool(x["changed"].get(k)) for x in rows)
          for cls,rows in groups.items()
        }

    cats={}
    for side in ["source_dependency","candidate_dependency"]:
        for k in ["anchor_pos","anchor_deprel","head_kind","head_direction_bucket","head_pos","head_deprel","prev_pos","prev_deprel","next_pos","next_deprel"]:
            cats[side+"."+k]={
              cls:dict(Counter(str(x[side].get(k)) for x in rows))
              for cls,rows in groups.items()
            }

    event_summary=[]
    for x in feats:
        event_summary.append({
          "vote_id":x["vote_id"],
          "class":"PARTIAL" if labels[x["vote_id"]]=="PARTIAL_CORRECTION" else "SUPPORTED",
          "any_structural_category_changed":x["any_structural_category_changed"],
          "changed":x["changed"],
          "source_anchor_pos":x["source_dependency"].get("anchor_pos"),
          "source_anchor_deprel":x["source_dependency"].get("anchor_deprel"),
          "source_head_pos":x["source_dependency"].get("head_pos"),
          "source_head_deprel":x["source_dependency"].get("head_deprel"),
          "source_head_direction_bucket":x["source_dependency"].get("head_direction_bucket"),
          "candidate_anchor_deprel":x["candidate_dependency"].get("anchor_deprel"),
          "candidate_head_pos":x["candidate_dependency"].get("head_pos"),
          "candidate_head_deprel":x["candidate_dependency"].get("head_deprel"),
          "candidate_head_direction_bucket":x["candidate_dependency"].get("head_direction_bucket"),
        })

    obj={
      "status":"PHASE2_DEPENDENCY_GOVERNOR_DIAGNOSTIC_EVALUATED",
      "diagnostic_only":True,"consumed_population":True,
      "features_frozen_before_manual_label_read":True,
      "label_counts":{"SUPPORTED":12,"PARTIAL":2},
      "change_feature_counts":changes,
      "categorical_distributions":cats,
      "event_summary":event_summary,
      "rule_optimization_permitted":False,
      "promotion_allowed":False,
      "fresh_validation_allowed":False,
      "next_action":"INTERPRET_FEATURES_AND_FORM_HYPOTHESIS_ONLY",
      "qalb15_test_read":False,"qalb_text_persisted":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped)
    print(json.dumps(obj))

if __name__=="__main__":main()
