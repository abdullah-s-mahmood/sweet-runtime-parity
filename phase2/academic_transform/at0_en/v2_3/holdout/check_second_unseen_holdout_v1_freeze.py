from __future__ import annotations
import hashlib, json, pathlib, collections

ROOT=pathlib.Path(__file__).resolve().parent
manifest=json.loads((ROOT/"SECOND_UNSEEN_HOLDOUT_V1_MANIFEST.json").read_text(encoding="utf-8"))
inputs_path=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_INPUTS.jsonl"
labels_path=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_LABELS.jsonl"
verifier=ROOT.parent/"at0_v2_3_assertion_graph.py"
cases=ROOT.parent.parent/"cases.jsonl"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rows(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

ins=rows(inputs_path); labs=rows(labels_path)
assert sha(inputs_path)==manifest["frozen_files"]["inputs_sha256"], (sha(inputs_path),manifest["frozen_files"]["inputs_sha256"])
assert sha(labels_path)==manifest["frozen_files"]["labels_sha256"], (sha(labels_path),manifest["frozen_files"]["labels_sha256"])
assert sha(verifier)==manifest["verifier_binding"]["sha256"], (sha(verifier),manifest["verifier_binding"]["sha256"])
assert sha(cases)==manifest["source_identity"]["cases_sha256_recorded"], (sha(cases),manifest["source_identity"]["cases_sha256_recorded"])
assert len(ins)==36 and len(labs)==36
ids_i=[x["holdout_id"] for x in ins]; ids_l=[x["holdout_id"] for x in labs]
assert len(set(ids_i))==36 and len(set(ids_l))==36 and ids_i==ids_l
k=collections.Counter(x["kind"] for x in labs)
assert k=={"SAFE_CONTROL":12,"ADVERSARIAL":24}, k
per=collections.Counter(x["case_id"] for x in labs if x["kind"]=="ADVERSARIAL")
assert set(per)=={f"EN{i:02d}" for i in range(1,13)}
assert set(per.values())=={2}, per
safe=collections.Counter(x["case_id"] for x in labs if x["kind"]=="SAFE_CONTROL")
assert set(safe)=={f"EN{i:02d}" for i in range(1,13)} and set(safe.values())=={1}
assert all(x["expected"]=="PASS_CANDIDATE" for x in labs if x["kind"]=="SAFE_CONTROL")
assert all(x["expected"]=="NOT_PASS" for x in labs if x["kind"]=="ADVERSARIAL")
summary={
 "gate":"SECOND_UNSEEN_HOLDOUT_V1_FREEZE_INTEGRITY",
 "status":"PASS",
 "scoring_performed":False,
 "model_inference":False,
 "inputs_sha256":sha(inputs_path),
 "labels_sha256":sha(labels_path),
 "verifier_sha256":sha(verifier),
 "cases_sha256":sha(cases),
 "total":len(ins),
 "safe_controls":k["SAFE_CONTROL"],
 "adversarial":k["ADVERSARIAL"],
 "unique_ids":len(set(ids_i)),
 "adversarial_per_case":dict(sorted(per.items()))
}
out=ROOT/"SECOND_UNSEEN_HOLDOUT_V1_FREEZE_INTEGRITY.json"
out.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
