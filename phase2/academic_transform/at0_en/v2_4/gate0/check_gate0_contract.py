from __future__ import annotations
import hashlib, json, pathlib

GATE0=pathlib.Path(__file__).resolve().parent
AT0=GATE0.parents[2]
SCHEMA=GATE0/"SCIENTIFIC_ASSERTION_GRAPH_SCHEMA_V1.json"
CRIT=GATE0/"CRITICALITY_RULES_V1.json"
OUTCOME=GATE0/"OUTCOME_CONTRACT_V1.json"
REF=GATE0/"GATE0_DEV_REFERENCE_V1.jsonl"
CASES=AT0/"cases.jsonl"
SUMMARY=GATE0/"GATE0_CONTRACT_TEST_SUMMARY.json"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
crit=json.loads(CRIT.read_text(encoding="utf-8"))
outcome=json.loads(OUTCOME.read_text(encoding="utf-8"))
refs=jsonl(REF)
cases={x["case_id"]:x for x in jsonl(CASES)}

checks=[]
def ck(name,cond,detail=None):
    checks.append({"check":name,"pass":bool(cond),"detail":detail})
    if not cond: raise AssertionError(f"{name}: {detail}")

ck("schema_version",schema["properties"]["schema_version"]["const"]=="2.4-gate0-v1")
ck("schema_has_assertions_relations_coverage",all(x in schema["required"] for x in ["assertions","relations","coverage"]))
assertion_props=schema["$defs"]["assertion"]["properties"]
for field in ["subject","predicate_raw","predicate_normalized","exclusions","citation_refs","equation_refs","symbol_bindings","quantifiers","extraction_status","evidence","anchors"]:
    ck("schema_assertion_field_"+field,field in assertion_props)
relation_types=set(schema["$defs"]["relation"]["properties"]["relation_type"]["enum"])
for rt in ["HAS_VALUE","HAS_UNIT","AT_TIME","IN_POPULATION","RELATIVE_TO","CITES","DEFINES","MEASURES","PRECEDES","FIXED_BEFORE","UNCHANGED_DURING","HAS_MODALITY","HAS_CAUSALITY","DISTINCT_FROM"]:
    ck("schema_relation_"+rt,rt in relation_types)

ck("criticality_levels",set(crit["levels"])=={"CRITICAL","MATERIAL","NON_MATERIAL"})
ck("outcome_precedence",outcome["precedence"]==["INVALID_VERIFICATION","REJECT","REVIEW","PASS_CANDIDATE"])
ck("outcome_set",set(outcome["outcomes"])=={"PASS_CANDIDATE","REJECT","REVIEW","INVALID_VERIFICATION"})
ck("pass_requires_trace",any("traceable evidence" in x for x in outcome["rules"]["PASS_CANDIDATE"]["requirements"]))
ck("noncompensation_present",len(outcome["non_compensation"])>=3)

expected={"EN04","EN05","EN06","EN07","EN09","EN12"}
ck("reference_case_set",{x["case_id"] for x in refs}==expected,{x["case_id"] for x in refs})
ck("reference_count",len(refs)==6,len(refs))

seen_assertions=set()
type_seen=set()
relation_seen=set()
for rec in refs:
    cid=rec["case_id"]
    ck(cid+"_development_only",rec.get("development_only") is True)
    ck(cid+"_source_exists",cid in cases)
    ck(cid+"_source_text_exact",rec["source_text"]==cases[cid]["source_text"])
    ck(cid+"_source_sha_exact",rec["source_sha256"]==cases[cid]["source_sha256"])
    ck(cid+"_source_sha_computed",hashlib.sha256(rec["source_text"].encode("utf-8")).hexdigest()==rec["source_sha256"])
    local_ids=set()
    for a in rec["gold_assertions"]:
        aid=a["id"]
        ck(cid+"_assertion_id_unique_local_"+aid,aid not in local_ids)
        ck(cid+"_assertion_id_unique_global_"+aid,aid not in seen_assertions)
        local_ids.add(aid); seen_assertions.add(aid)
        ck(cid+"_evidence_present_"+aid,a["evidence"] in rec["source_text"],a["evidence"])
        ck(cid+"_criticality_valid_"+aid,a["criticality"] in {"CRITICAL","MATERIAL","NON_MATERIAL"})
        type_seen.add(a["type"])
    for rel in rec["gold_relations"]:
        ck(cid+"_relation_from_valid_"+rel["from"],rel["from"] in local_ids,rel)
        ck(cid+"_relation_criticality_valid_"+rel["relation"],rel["criticality"] in {"CRITICAL","MATERIAL","NON_MATERIAL"})
        relation_seen.add(rel["relation"])

for needed in ["RELATIONAL","ASSOCIATIONAL","NEGATION","SCOPE","QUANTITATIVE","COMPARATIVE","PROCEDURAL","EQUATION","DEFINITIONAL"]:
    ck("reference_type_"+needed,needed in type_seen,sorted(type_seen))
for needed in ["CITES","IN_POPULATION","RELATIVE_TO","PRECEDES","FIXED_BEFORE","UNCHANGED_DURING","DEFINES","MEASURES"]:
    ck("reference_relation_"+needed,needed in relation_seen,sorted(relation_seen))

summary={
    "gate":"AT0_EN_V2_4_GATE0_CONTRACT",
    "status":"PASS",
    "model_inference":False,
    "reference_cases":sorted(expected),
    "reference_case_count":len(refs),
    "reference_assertion_count":sum(len(x["gold_assertions"]) for x in refs),
    "reference_relation_count":sum(len(x["gold_relations"]) for x in refs),
    "checks_total":len(checks),
    "checks_passed":sum(x["pass"] for x in checks),
    "files":{
        "schema_sha256":sha(SCHEMA),
        "criticality_sha256":sha(CRIT),
        "outcome_sha256":sha(OUTCOME),
        "reference_sha256":sha(REF),
        "cases_sha256":sha(CASES)
    }
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
