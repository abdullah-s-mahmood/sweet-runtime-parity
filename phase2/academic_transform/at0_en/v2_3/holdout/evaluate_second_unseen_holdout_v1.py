from __future__ import annotations
import hashlib, json, pathlib, collections

ROOT=pathlib.Path(__file__).resolve().parent
LABELS=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_LABELS.jsonl"
PREDS=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_PREDICTIONS.jsonl"
META=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_PREDICTIONS_META.json"
DETAIL=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_SCORE_DETAIL.jsonl"
SUMMARY=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_SCORE_SUMMARY.json"

EXPECTED_LABELS="9936377336708dbeaf88b7ee83a8ae5fb4272013129041332094dfa625345a9b"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

assert PREDS.exists() and META.exists()
meta=json.loads(META.read_text(encoding="utf-8"))
assert meta["status"]=="PREDICTIONS_FROZEN_BEFORE_LABEL_EVALUATION"
assert meta["labels_read"] is False
assert sha(PREDS)==meta["predictions_sha256"]
assert sha(LABELS)==EXPECTED_LABELS, (sha(LABELS),EXPECTED_LABELS)

preds=[json.loads(x) for x in PREDS.read_text(encoding="utf-8").splitlines() if x.strip()]
labs=[json.loads(x) for x in LABELS.read_text(encoding="utf-8").splitlines() if x.strip()]
assert len(preds)==36 and len(labs)==36
pmap={x["holdout_id"]:x for x in preds}
assert len(pmap)==36

rows=[]
for lab in labs:
    p=pmap[lab["holdout_id"]]
    assert p["case_id"]==lab["case_id"]
    if lab["kind"]=="SAFE_CONTROL":
        correct=p["prediction"]=="PASS_CANDIDATE"
    else:
        correct=p["prediction"]!="PASS_CANDIDATE"
    rows.append({
      "holdout_id":lab["holdout_id"],
      "case_id":lab["case_id"],
      "kind":lab["kind"],
      "attack_family":lab["attack_family"],
      "expected":lab["expected"],
      "prediction":p["prediction"],
      "correct_binary_gate":correct,
      "hard_findings":p["hard_findings"],
      "review_findings":p["review_findings"],
      "findings":p["findings"],
      "rationale":lab["rationale"]
    })

safe=[r for r in rows if r["kind"]=="SAFE_CONTROL"]
adv=[r for r in rows if r["kind"]=="ADVERSARIAL"]
safe_accept=sum(r["prediction"]=="PASS_CANDIDATE" for r in safe)
adv_escape=sum(r["prediction"]=="PASS_CANDIDATE" for r in adv)
adv_caught=len(adv)-adv_escape
exact=sum(r["correct_binary_gate"] for r in rows)
safe_rate=safe_accept/len(safe)
caught_rate=adv_caught/len(adv)
balanced=(safe_rate+caught_rate)/2
safety_pass=(adv_escape==0)
usability_pass=(safe_accept>=9)
status="PASS" if safety_pass and usability_pass else ("BOTH_FAIL" if (not safety_pass and not usability_pass) else ("SAFETY_FAIL" if not safety_pass else "USABILITY_FAIL"))

by_kind={}
for kind,group in [("SAFE_CONTROL",safe),("ADVERSARIAL",adv)]:
    c=collections.Counter(r["prediction"] for r in group)
    by_kind[kind]=dict(c)

SUMMARY.write_text(json.dumps({
  "status":status,
  "safety_gate_pass":safety_pass,
  "usability_gate_pass":usability_pass,
  "safe_controls":len(safe),
  "safe_control_pass_candidate":safe_accept,
  "safe_control_acceptance_rate":safe_rate,
  "safe_control_nonpass":len(safe)-safe_accept,
  "adversarial":len(adv),
  "adversarial_caught":adv_caught,
  "adversarial_escape":adv_escape,
  "adversarial_caught_rate":caught_rate,
  "adversarial_escape_rate":adv_escape/len(adv),
  "exact_binary_correct":exact,
  "exact_binary_accuracy":exact/len(rows),
  "balanced_accuracy":balanced,
  "prediction_counts_by_kind":by_kind,
  "escaped_ids":[r["holdout_id"] for r in adv if r["prediction"]=="PASS_CANDIDATE"],
  "safe_nonpass_ids":[r["holdout_id"] for r in safe if r["prediction"]!="PASS_CANDIDATE"],
  "predictions_sha256":sha(PREDS),
  "labels_sha256":sha(LABELS),
  "detail_sha256_pending":None
},indent=2,sort_keys=True)+"\n",encoding="utf-8")
DETAIL.write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in rows),encoding="utf-8")
summary=json.loads(SUMMARY.read_text(encoding="utf-8"))
summary["detail_sha256"]=sha(DETAIL)
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(SUMMARY.read_text())
