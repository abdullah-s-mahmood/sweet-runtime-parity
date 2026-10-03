from __future__ import annotations
import hashlib, importlib.util, json, pathlib

ROOT=pathlib.Path(__file__).resolve().parent
V23=ROOT.parent
AT0=V23.parent

EXPECTED={
  "verifier":"d82af97d276131477ab2f8c452f24e3302703f54b856a8ad46547af59d7ec0da",
  "inputs":"b1633df5e0418082a990945dfc92a267f6cdc8c943b385d7edc2d8b9181f551c",
  "cases":"d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7"
}
VERIFIER=V23/"at0_v2_3_assertion_graph.py"
INPUTS=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_INPUTS.jsonl"
CASES=AT0/"cases.jsonl"
OUT=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_PREDICTIONS.jsonl"
META=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_PREDICTIONS_META.json"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

assert sha(VERIFIER)==EXPECTED["verifier"], (sha(VERIFIER),EXPECTED["verifier"])
assert sha(INPUTS)==EXPECTED["inputs"], (sha(INPUTS),EXPECTED["inputs"])
assert sha(CASES)==EXPECTED["cases"], (sha(CASES),EXPECTED["cases"])

spec=importlib.util.spec_from_file_location("v23",VERIFIER)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

cases={}
for line in CASES.read_text(encoding="utf-8").splitlines():
    if line.strip():
        x=json.loads(line); cases[x["case_id"]]=x

inputs=[json.loads(x) for x in INPUTS.read_text(encoding="utf-8").splitlines() if x.strip()]
assert len(inputs)==36
assert len({x["holdout_id"] for x in inputs})==36

rows=[]
for x in inputs:
    src=cases[x["case_id"]]["source_text"]
    res=mod.validate(x["case_id"],src,x["text"])
    rows.append({
      "holdout_id":x["holdout_id"],
      "case_id":x["case_id"],
      "prediction":res["disposition"],
      "hard_findings":res["hard_findings"],
      "review_findings":res["review_findings"],
      "findings":res["findings"],
      "candidate_sha256":hashlib.sha256(x["text"].encode("utf-8")).hexdigest(),
      "source_sha256":hashlib.sha256(src.encode("utf-8")).hexdigest()
    })

OUT.write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in rows),encoding="utf-8")
pred_sha=sha(OUT)
counts={}
for r in rows: counts[r["prediction"]]=counts.get(r["prediction"],0)+1
META.write_text(json.dumps({
  "status":"PREDICTIONS_FROZEN_BEFORE_LABEL_EVALUATION",
  "labels_read":False,
  "model_inference":False,
  "count":len(rows),
  "prediction_counts":counts,
  "verifier_sha256":sha(VERIFIER),
  "inputs_sha256":sha(INPUTS),
  "cases_sha256":sha(CASES),
  "predictions_sha256":pred_sha
},indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(META.read_text())
