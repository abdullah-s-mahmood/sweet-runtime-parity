from __future__ import annotations
import hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent
AT0=ROOT.parent
sys.path.insert(0,str(AT0/"v2_2"/"redteam"))
import at0_v2_2_independent_redteam as r1
sys.path.insert(0,str(AT0/"v2_3"/"holdout"))
import at0_v2_3_holdout_v1 as r2

def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

rows=[]
exclusions=[]

for cid,text in sorted(r1.SAFE.items()):
    if cid in {"EN08","EN09"}:
        exclusions.append({
            "source":"V2.2_SAFE",
            "case_id":cid,
            "reason":"LABEL_DEFECT_OR_SCOPE_AMBIGUITY",
            "detail":"EN08 broadens the source causal limitation to blanket non-generalizability; EN09 omits the priority-direction relation present in source_text."
        })
        continue
    rows.append({
        "calibration_id":f"CAL-SAFE-V22-{cid}",
        "label":"SAFE",
        "case_id":cid,
        "source_sha256":r1.CASES[cid]["source_sha256"],
        "candidate_text":text,
        "candidate_sha256":sha(text),
        "provenance":"V2.2_CONSUMED_SAFE_CONTROL",
        "consumed_development":True
    })

for cid,text in sorted(r2.SAFE.items()):
    rows.append({
        "calibration_id":f"CAL-SAFE-V23-{cid}",
        "label":"SAFE",
        "case_id":cid,
        "source_sha256":r1.CASES[cid]["source_sha256"],
        "candidate_text":text,
        "candidate_sha256":sha(text),
        "provenance":"V2.3_CONSUMED_UNSEEN_HOLDOUT_SAFE_AFTER_OPENING",
        "consumed_development":True
    })

for tid,cid,text in r1.ATTACKS:
    rows.append({
        "calibration_id":f"CAL-ADV-V22-{tid}",
        "label":"ADVERSARIAL",
        "case_id":cid,
        "source_sha256":r1.CASES[cid]["source_sha256"],
        "candidate_text":text,
        "candidate_sha256":sha(text),
        "provenance":"V2.2_CONSUMED_INDEPENDENT_REDTEAM_ATTACK",
        "consumed_development":True
    })

for tid,cid,text in r2.ATTACKS:
    rows.append({
        "calibration_id":f"CAL-ADV-V23-{tid}",
        "label":"ADVERSARIAL",
        "case_id":cid,
        "source_sha256":r1.CASES[cid]["source_sha256"],
        "candidate_text":text,
        "candidate_sha256":sha(text),
        "provenance":"V2.3_CONSUMED_UNSEEN_HOLDOUT_ATTACK_AFTER_OPENING",
        "consumed_development":True
    })

ids=[x["calibration_id"] for x in rows]
assert len(ids)==len(set(ids))
safe=sum(x["label"]=="SAFE" for x in rows)
adv=sum(x["label"]=="ADVERSARIAL" for x in rows)
assert safe==22, safe
assert adv==36, adv
assert len(rows)==58
assert len(exclusions)==2

out=ROOT/"calibration"
out.mkdir(exist_ok=True)
pop=out/"V2_4_SEMANTIC_CALIBRATION_V1.jsonl"
pop.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in rows),encoding="utf-8")
exc=out/"V2_4_CALIBRATION_EXCLUSIONS_V1.json"
exc.write_text(json.dumps(exclusions,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
manifest={
    "schema_version":"1.0.0",
    "phase":"AT0-EN-V2.4",
    "population":"SEMANTIC_CALIBRATION_V1",
    "status":"FROZEN_BEFORE_SEMANTIC_SCORING",
    "total":len(rows),
    "safe":safe,
    "adversarial":adv,
    "excluded_controls":len(exclusions),
    "all_examples_consumed_development":True,
    "confirmation_population_included":False,
    "semantic_scores_observed":False,
    "population_sha256":hashlib.sha256(pop.read_bytes()).hexdigest(),
    "exclusions_sha256":hashlib.sha256(exc.read_bytes()).hexdigest(),
    "source_assertions_sha256":hashlib.sha256((ROOT/"SOURCE_ASSERTIONS_V1.json").read_bytes()).hexdigest()
}
(out/"V2_4_SEMANTIC_CALIBRATION_MANIFEST_V1.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(manifest,indent=2))
