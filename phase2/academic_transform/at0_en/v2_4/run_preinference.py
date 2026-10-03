from __future__ import annotations
import json,pathlib,re,sys
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from v2_4_hybrid_core import *

m=json.loads((ROOT/"SEMANTIC_MODEL_MANIFEST.json").read_text(encoding="utf-8"))
rows=[]
def check(name,cond,msg=""):
    rows.append({"test":name,"status":"PASS" if cond else "FAIL","detail":msg})

check("P01_SCHEMA",m["schema_version"]=="1.0.0")
check("P02_NO_INFERENCE_AUTH",m["semantic_inference_authorized"] is False and m["new_generator_inference_authorized"] is False)
check("P03_THRESHOLDS_UNFROZEN",m["thresholds"]["status"]=="UNFROZEN_CALIBRATION_REQUIRED" and m["thresholds"]["values"] is None)
check("P04_TWO_WITNESSES",len(m["witnesses"])==2)
check("P05_EXACT_REVISIONS",all(re.fullmatch(r"[0-9a-f]{40}",w["revision"]) for w in m["witnesses"]))
check("P06_NO_MAIN_ALIAS",all(w["revision"]!="main" for w in m["witnesses"]))
check("P07_MODEL_HASHES",all(re.fullmatch(r"[0-9a-f]{64}",w["model_sha256"]) for w in m["witnesses"]))
h=next(w for w in m["witnesses"] if w["witness_id"]=="HHEM_2_1_OPEN")
d=next(w for w in m["witnesses"] if w["witness_id"]=="DEBERTA_NLI")
check("P08_HHEM_REMOTE_CODE",h["trust_remote_code"] is True and {"configuration_hhem_v2.py","modeling_hhem_v2.py"}.issubset(h["required_repository_files"]))
check("P09_HHEM_TRANSITIVE_PIN",re.fullmatch(r"[0-9a-f]{40}",h["transitive_runtime_dependency"]["revision"]) is not None)
check("P10_DEBERTA_LABELS",d["label_semantics"]=={"0":"entailment","1":"neutral","2":"contradiction"})
check("P11_HARD_PRECEDENCE",fuse(hard_findings=[HardFinding("X","HARD")],source_assertion_witnesses=[],candidate_claim_witnesses=[])=="HARD_REJECT")
ws=[SemanticWitness("A","S1","SOURCE_TO_CANDIDATE","ENTAILS",True),SemanticWitness("B","S1","SOURCE_TO_CANDIDATE","ENTAILS",True)]
wc=[SemanticWitness("A","C1","CANDIDATE_TO_SOURCE","ENTAILS",True),SemanticWitness("B","C1","CANDIDATE_TO_SOURCE","ENTAILS",True)]
check("P12_TWO_WAY_PASS",fuse(hard_findings=[],source_assertion_witnesses=ws,candidate_claim_witnesses=wc)=="VERIFIED_FOR_REVIEW")
dis=[SemanticWitness("A","S1","SOURCE_TO_CANDIDATE","ENTAILS",True),SemanticWitness("B","S1","SOURCE_TO_CANDIDATE","CONTRADICTS",True)]
check("P13_DISAGREEMENT_REVIEW",fuse(hard_findings=[],source_assertion_witnesses=dis,candidate_claim_witnesses=wc)=="REVIEW")
unc=[SemanticWitness("A","S1","SOURCE_TO_CANDIDATE","UNCERTAIN",True)]
check("P14_UNCERTAIN_REVIEW",fuse(hard_findings=[],source_assertion_witnesses=unc,candidate_claim_witnesses=wc)=="REVIEW")
bad=[SemanticWitness("A","S1","SOURCE_TO_CANDIDATE","CONTRADICTS",True),SemanticWitness("B","S1","SOURCE_TO_CANDIDATE","CONTRADICTS",True)]
check("P15_SEMANTIC_REJECT",fuse(hard_findings=[],source_assertion_witnesses=bad,candidate_claim_witnesses=wc)=="SEMANTIC_REJECT")
check("P16_UNCALIBRATED_REVIEW",fuse(hard_findings=[],source_assertion_witnesses=[SemanticWitness("A","S1","SOURCE_TO_CANDIDATE","ENTAILS",False)],candidate_claim_witnesses=wc)=="REVIEW")
check("P17_KEEP",fuse(hard_findings=[],source_assertion_witnesses=[],candidate_claim_witnesses=[],exact_keep=True)=="KEEP")
out=ROOT/"results"; out.mkdir(exist_ok=True)
payload={"total":len(rows),"passed":sum(x["status"]=="PASS" for x in rows),"failed":sum(x["status"]=="FAIL" for x in rows),"semantic_inference_performed":False,"results":rows}
(out/"V2_4_PREINFERENCE_RESULTS.json").write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
print(json.dumps(payload,indent=2))
if payload["failed"]: raise SystemExit(2)
