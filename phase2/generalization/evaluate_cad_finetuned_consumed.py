"""Evaluate frozen fine-tuned CAD consumed decisions after feature materialization."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
F=ROOT/"PHASE2_CAD_FINETUNED_CONSUMED_FEATURES.jsonl"
R=ROOT/"PHASE2_CAD_FINETUNED_CONSUMED_RUNTIME.json"
THIRD_MANUAL=ROOT/"PHASE2_ORTHO_ISOLATED_VALIDATION_MANUAL_REVIEW.json"
OLD_AUTO=ROOT/"PHASE2_TRIMODEL_VOTING_RESULTS.json"
OLD_MANUAL=ROOT/"PHASE2_TRIMODEL_VOTING_MANUAL_REVIEW.json"
OUT=ROOT/"PHASE2_CAD_FINETUNED_CONSUMED_RESULTS.json"
SUPPORTED={"SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE"}

def jl(p):return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def ev(rows,labels):
 pas=[x for x in rows if x["runtime_decision"]=="PASS"];rev=[x for x in rows if x["runtime_decision"]=="REVIEW"]
 counts={}
 for x in pas:
  c=labels[x["vote_id"]];counts[c]=counts.get(c,0)+1
 sup=sum(labels[x["vote_id"]] in SUPPORTED for x in pas);par=sum(labels[x["vote_id"]]=="PARTIAL_CORRECTION" for x in pas);wr=sum(labels[x["vote_id"]]=="WRONG_CORRECTION" for x in pas);un=sum(labels[x["vote_id"]]=="UNNECESSARY_EDIT" for x in pas)
 return {"total":len(rows),"pass":len(pas),"review":len(rev),"pass_class_counts":counts,"supported_pass":sup,"partial_pass":par,"wrong_pass":wr,"unnecessary_pass":un,"unsafe_pass":par+wr+un,"pass_precision":sup/len(pas) if pas else None}
def main():
 rt=json.loads(R.read_text(encoding="utf-8"));assert rt["current_labels_read"] is False and rt["external_model_frozen"] is True
 rows=jl(F);third=[x for x in rows if x["population"]=="THIRD_V1_14"];old=[x for x in rows if x["population"]=="EARLIER_ORTHO_MORPH_36"];assert len(third)==14 and len(old)==36
 tm=json.loads(THIRD_MANUAL.read_text(encoding="utf-8"));partial={x["vote_id"] for x in tm["items"] if x["manual_class"]=="PARTIAL_CORRECTION"};assert len(partial)==2
 tl={x["vote_id"]:("PARTIAL_CORRECTION" if x["vote_id"] in partial else "SUPPORTED_CORRECTION") for x in third}
 auto=json.loads(OLD_AUTO.read_text(encoding="utf-8"));automatic={x["vote_id"]:x["classification"] for x in auto["policy_results"]["UNANIMOUS_3"]["event_audit_hashes"]}
 manual=json.loads(OLD_MANUAL.read_text(encoding="utf-8"));mm={x["vote_id"]:x["manual_class"] for x in manual["items"]}
 ol={x["vote_id"]:("SUPPORTED_CORRECTION" if automatic[x["vote_id"]]=="EXACT_GOLD_SUPPORTED" else mm[x["vote_id"]]) for x in old}
 assert sum(v in SUPPORTED for v in ol.values())==34 and sum(v=="PARTIAL_CORRECTION" for v in ol.values())==2
 a=ev(third,tl);b=ev(old,ol);strict=[x for x in old if x["strict_v1_member"]];c=ev(strict,ol);assert len(strict)==19
 aok=a["pass"]>=10 and a["supported_pass"]>=10 and a["unsafe_pass"]==0
 bok=b["supported_pass"]>=24 and b["unsafe_pass"]==0
 cok=c["pass"]>=12 and c["unsafe_pass"]==0
 q=aok and bok and cok
 obj={"status":"PHASE2_CAD_FINETUNED_FEASIBILITY_EVALUATED","external_training_frozen":True,"features_frozen_before_current_labels":True,"third_v1_14":a,"earlier_ortho_morph_36":b,"earlier_strict_v1_19":c,"criteria":{"third_slice_met":aok,"earlier_36_met":bok,"nested_strict_v1_met":cok,"all_consumed_criteria_met":q},"status_for_next_step":"ELIGIBLE_TO_PREREGISTER_FOURTH_DISJOINT_VALIDATION" if q else "STOP_PHASE2_ARABIC_AUTO_ACCEPT_REVIEW_FIRST","fourth_slice_allowed":q,"promotion_allowed":False,"qalb15_test_read":False,"qalb_text_persisted":False}
 OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");assert not any("\u0600"<=c<="\u06ff" for c in OUT.read_text(encoding="utf-8"));print(json.dumps(obj,ensure_ascii=False))
if __name__=="__main__":main()
