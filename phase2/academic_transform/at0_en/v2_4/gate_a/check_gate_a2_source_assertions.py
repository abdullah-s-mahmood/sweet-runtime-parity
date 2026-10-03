from __future__ import annotations
import collections, hashlib, importlib.util, json, pathlib

HERE=pathlib.Path(__file__).resolve().parent
AT0=HERE.parents[1]
SCHEMA_PATH=HERE.parent/"gate0"/"SCIENTIFIC_ASSERTION_GRAPH_SCHEMA_V1.json"
EXTRACTOR=HERE/"source_assertion_extractor.py"
CASES=AT0/"cases.jsonl"
OUT=HERE/"results"
OUT.mkdir(exist_ok=True)
PRED=OUT/"GATE_A2_SOURCE_ASSERTIONS.jsonl"
SUMMARY=OUT/"GATE_A2_SOURCE_ASSERTION_SUMMARY.json"

def rows(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

spec=importlib.util.spec_from_file_location("a2",EXTRACTOR)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

schema=json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
cases=rows(CASES)
src=EXTRACTOR.read_text(encoding="utf-8")
assert "GATE0_DEV_REFERENCE_V1" not in src
assert "GATE_A1_ANCHOR_REFERENCE_V1" not in src

assertion_schema=schema["$defs"]["assertion"]
required=set(assertion_schema["required"])
props=assertion_schema["properties"]
enum_fields={k:set(v["enum"]) for k,v in props.items() if isinstance(v,dict) and "enum" in v}

all_graphs=[]
status_counts=collections.Counter()
type_counts=collections.Counter()
role_counts=collections.Counter()
assertion_count=0
anchor_count=0
sentence_count=0
represented_sentence_count=0
evidence_exact_checks=0

for case in cases:
    g=mod.extract_source_assertions(case)
    assert g["schema_version"]=="2.4-gate0-v1"
    assert g["source_identity"]["source_sha256"]==case["source_sha256"]
    assert g["relations"]==[]

    evidence_ids=set()
    evidence_map={}
    for e in g["evidence_spans"]:
        sid=e["span_id"]
        assert sid not in evidence_ids
        evidence_ids.add(sid); evidence_map[sid]=e
        a,b=e["char_start"],e["char_end"]
        assert a is not None and b is not None and 0 <= a < b <= len(case["source_text"])
        assert case["source_text"][a:b]==e["quote"]
        # A decimal point must never be treated as a sentence/claim boundary.
        assert not (b < len(case["source_text"]) and b >= 2 and case["source_text"][b-1]=="." and case["source_text"][b-2].isdigit() and case["source_text"][b].isdigit())
        evidence_exact_checks+=1

    anchor_ids=set()
    for a in g["anchors"]:
        assert a["anchor_id"] not in anchor_ids
        anchor_ids.add(a["anchor_id"])
        assert a["evidence_span_ids"]
        assert set(a["evidence_span_ids"]) <= evidence_ids
    anchor_count+=len(anchor_ids)

    assertion_ids=set()
    for a in g["assertions"]:
        assert a["assertion_id"] not in assertion_ids
        assertion_ids.add(a["assertion_id"])
        assert required <= set(a), (case["case_id"], required-set(a))
        assert set(a["evidence_span_ids"]) <= evidence_ids
        assert set(a.get("anchor_refs",[])) <= anchor_ids
        for field,allowed in enum_fields.items():
            if field in a:
                assert a[field] in allowed, (case["case_id"],field,a[field])
        if a["unresolved_slots"]:
            assert a["extraction_status"]!="CERTAIN"
        quote=evidence_map[a["evidence_span_ids"][0]]["quote"].lower()
        if any(x in quote for x in [" found that "," whether "," rather than "]):
            assert a["extraction_status"]!="CERTAIN", (case["case_id"],a["assertion_id"],quote)
        if a["subject"]=="UNRESOLVED":
            assert a["extraction_status"]=="AMBIGUOUS"
        status_counts[a["extraction_status"]]+=1
        type_counts[a["assertion_type"]]+=1
        role_counts[a["discourse_role"]]+=1
    assertion_count+=len(assertion_ids)
    assert assertion_ids, case["case_id"]

    cov=g["coverage"]
    assert cov["coverage_status"]=="UNKNOWN"
    cb=set(cov["claim_bearing_span_ids"])
    rep=set(cov["represented_span_ids"])
    unrep=set(cov["unrepresented_span_ids"])
    assert rep.isdisjoint(unrep)
    assert rep | unrep == cb
    assert set(cov["unowned_anchor_ids"])==anchor_ids
    assert all(x in evidence_ids for x in cb)
    sentence_count+=len(cb)
    represented_sentence_count+=len(rep)

    all_graphs.append(g)

assert status_counts["CERTAIN"]>0, status_counts
assert status_counts["UNCERTAIN"]+status_counts["AMBIGUOUS"]>0, status_counts

PRED.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in all_graphs),encoding="utf-8")
summary={
  "gate":"AT0_EN_V2_4_GATE_A2_SOURCE_ASSERTION_PROTOTYPE",
  "status":"PASS",
  "model_inference":False,
  "gold_reference_read":False,
  "case_count":len(cases),
  "assertion_count":assertion_count,
  "anchor_count":anchor_count,
  "sentence_count":sentence_count,
  "represented_sentence_count":represented_sentence_count,
  "structural_sentence_representation_rate":represented_sentence_count/sentence_count if sentence_count else 0.0,
  "extraction_status_counts":dict(status_counts),
  "assertion_type_counts":dict(type_counts),
  "discourse_role_counts":dict(role_counts),
  "evidence_exact_span_checks":evidence_exact_checks,
  "relations_emitted":0,
  "semantic_anchor_ownership_assessed":False,
  "semantic_coverage_claimed":False,
  "coverage_status":"UNKNOWN_BY_DESIGN",
  "hashes":{
    "schema_sha256":sha(SCHEMA_PATH),
    "extractor_sha256":sha(EXTRACTOR),
    "cases_sha256":sha(CASES),
    "predictions_sha256":sha(PRED)
  }
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
