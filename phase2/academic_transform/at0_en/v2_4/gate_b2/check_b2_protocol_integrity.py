from __future__ import annotations
import hashlib, json, pathlib

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[6]
B1=HERE.parent/"gate_b1"
A=HERE.parent/"gate_a"

PAIRS=B1/"B1_HUMAN_CORRECT_GRAPH_PAIRS_V1.jsonl"
RAW=HERE/"B2_RAW_TEXT_PAIRS_V1.jsonl"
PROTOCOL=HERE/"B2_DEGRADATION_PROTOCOL_V1.md"
BRIDGE=HERE/"B2_BRIDGE_CONTRACT_V1.md"
ALIGNER=B1/"b1_aligner.py"
EXTRACTOR=A/"source_assertion_extractor.py"
OUT=HERE/"B2_PROTOCOL_INTEGRITY_SUMMARY.json"

EXPECTED_ALIGNER="289d2898c89850f691d52313a1d2a2b12b37cef6b674549215579caedf84cd42"
EXPECTED_EXTRACTOR="32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1"
EXPECTED_B1_PAIRS="29f3790859c8da6baf65db8b0fb372bc881e25d8e3d1e76b9c67b74d49944dca"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p): return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def dedup(xs):
    seen=set(); out=[]
    for x in xs:
        if x not in seen:
            seen.add(x); out.append(x)
    return out
def text_from_graph(g):
    return " ".join(dedup([*(x["evidence"] for x in g["assertions"]),*(x["evidence"] for x in g["relations"])]))

assert sha(ALIGNER)==EXPECTED_ALIGNER, (sha(ALIGNER),EXPECTED_ALIGNER)
assert sha(EXTRACTOR)==EXPECTED_EXTRACTOR, (sha(EXTRACTOR),EXPECTED_EXTRACTOR)
assert sha(PAIRS)==EXPECTED_B1_PAIRS, (sha(PAIRS),EXPECTED_B1_PAIRS)

pairs=rows(PAIRS); raw=rows(RAW)
assert len(pairs)==12 and len(raw)==12
pmap={x["pair_id"]:x for x in pairs}
assert len(pmap)==12
checks=0
for r in raw:
    p=pmap[r["pair_id"]]
    assert r["source_case_id"]==p["source_case_id"]; checks+=1
    assert r["scenario_class"]==p["scenario_class"]; checks+=1
    assert r["mapping_shape"]==p["mapping_shape"]; checks+=1
    assert r["expected_outcome"]==p["expected_outcome"]; checks+=1
    assert r["source_text"]==text_from_graph(p["source_graph"]); checks+=1
    assert r["candidate_text"]==text_from_graph(p["candidate_graph"]); checks+=1
    assert r["source_assertion_evidence_count"]==len(p["source_graph"]["assertions"]); checks+=1
    assert r["candidate_assertion_evidence_count"]==len(p["candidate_graph"]["assertions"]); checks+=1
    assert r["source_relation_evidence_count"]==len(p["source_graph"]["relations"]); checks+=1
    assert r["candidate_relation_evidence_count"]==len(p["candidate_graph"]["relations"]); checks+=1
    assert r["derivation"]=="ASSERTION_EVIDENCE_THEN_RELATION_EVIDENCE_DEDUP_EXACT"; checks+=1
    assert r["source_text"].strip() and r["candidate_text"].strip(); checks+=1

summary={
  "gate":"AT0_EN_V2_4_B2_PROTOCOL_INTEGRITY",
  "status":"PASS",
  "model_inference":False,
  "pair_count":len(raw),
  "checks_passed":checks,
  "arms":["GG","GE","EG","EE"],
  "primary_arm":"EE",
  "frozen_baseline_pair_accuracy":1.0,
  "hashes":{
    "aligner_sha256":sha(ALIGNER),
    "extractor_sha256":sha(EXTRACTOR),
    "b1_pairs_sha256":sha(PAIRS),
    "raw_pairs_sha256":sha(RAW),
    "protocol_sha256":sha(PROTOCOL),
    "bridge_contract_sha256":sha(BRIDGE)
  }
}
OUT.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
