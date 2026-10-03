from __future__ import annotations
import collections, hashlib, json, pathlib

HERE=pathlib.Path(__file__).resolve().parent
SCHEMA=HERE/"B1_ALIGNMENT_GRAPH_SCHEMA_V1.json"
PAIRS=HERE/"B1_HUMAN_CORRECT_GRAPH_PAIRS_V1.jsonl"
SUMMARY=HERE/"B1_REFERENCE_INTEGRITY_SUMMARY.json"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p): return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
pairs=rows(PAIRS)
assert len(pairs)==12
assert len({x["pair_id"] for x in pairs})==12

allowed_scen=set(schema["properties"]["scenario_class"]["enum"])
allowed_shape=set(schema["properties"]["mapping_shape"]["enum"])
allowed_outcome=set(schema["properties"]["expected_outcome"]["enum"])
allowed_status=set(schema["properties"]["gold_alignment"]["items"]["properties"]["status"]["enum"])
allowed_rel_status=set(schema["properties"]["gold_relation_alignment"]["items"]["properties"]["status"]["enum"])
allowed_conf=set(schema["$defs"]["assertion"]["properties"]["confidence_status"]["enum"])
allowed_rel_types=set(schema["$defs"]["relation"]["properties"]["type"]["enum"])

outcomes=collections.Counter()
shapes=collections.Counter()
scenarios=collections.Counter()
alignment_status=collections.Counter()
relation_status=collections.Counter()
source_assertions=candidate_assertions=source_relations=candidate_relations=0
uncertain_pair_ids=[]
checks=0

for p in pairs:
    assert p["scenario_class"] in allowed_scen; checks+=1
    assert p["mapping_shape"] in allowed_shape; checks+=1
    assert p["expected_outcome"] in allowed_outcome; checks+=1
    outcomes[p["expected_outcome"]]+=1
    shapes[p["mapping_shape"]]+=1
    scenarios[p["scenario_class"]]+=1

    graph_ids=set()
    assertion_ids={}
    relation_ids={}
    for side in ["source_graph","candidate_graph"]:
        g=p[side]
        assert g["graph_id"] not in graph_ids
        graph_ids.add(g["graph_id"])
        aids=set()
        for a in g["assertions"]:
            assert a["id"] not in aids
            aids.add(a["id"])
            assert a["confidence_status"] in allowed_conf
            assert a["evidence"].strip()
            checks+=3
        rids=set()
        for r in g["relations"]:
            assert r["id"] not in rids
            rids.add(r["id"])
            assert r["type"] in allowed_rel_types
            assert r["from"] in aids, (p["pair_id"],side,r)
            assert r["evidence"].strip()
            checks+=4
        assertion_ids[side]=aids
        relation_ids[side]=rids

    source_assertions+=len(assertion_ids["source_graph"])
    candidate_assertions+=len(assertion_ids["candidate_graph"])
    source_relations+=len(relation_ids["source_graph"])
    candidate_relations+=len(relation_ids["candidate_graph"])

    seen_s=set(); seen_c=set()
    for m in p["gold_alignment"]:
        assert m["status"] in allowed_status
        assert set(m["source_ids"]) <= assertion_ids["source_graph"]
        assert set(m["candidate_ids"]) <= assertion_ids["candidate_graph"]
        assert m["source_ids"] or m["candidate_ids"]
        assert m["reason"].strip()
        alignment_status[m["status"]]+=1
        seen_s |= set(m["source_ids"])
        seen_c |= set(m["candidate_ids"])
        checks+=5

    # Every assertion must be accounted for by at least one gold alignment row.
    assert seen_s==assertion_ids["source_graph"], (p["pair_id"],"source",seen_s,assertion_ids["source_graph"])
    assert seen_c==assertion_ids["candidate_graph"], (p["pair_id"],"candidate",seen_c,assertion_ids["candidate_graph"])
    checks+=2

    seen_sr=set(); seen_cr=set()
    for m in p["gold_relation_alignment"]:
        assert m["status"] in allowed_rel_status
        assert set(m["source_relation_ids"]) <= relation_ids["source_graph"]
        assert set(m["candidate_relation_ids"]) <= relation_ids["candidate_graph"]
        assert m["source_relation_ids"] or m["candidate_relation_ids"]
        assert m["reason"].strip()
        relation_status[m["status"]]+=1
        seen_sr |= set(m["source_relation_ids"])
        seen_cr |= set(m["candidate_relation_ids"])
        checks+=5

    # Every graph relation must be explicitly accounted for when relations exist.
    assert seen_sr==relation_ids["source_graph"], (p["pair_id"],"source relations",seen_sr,relation_ids["source_graph"])
    assert seen_cr==relation_ids["candidate_graph"], (p["pair_id"],"candidate relations",seen_cr,relation_ids["candidate_graph"])
    checks+=2

    has_uncertain=any(a["confidence_status"]!="CERTAIN" for side in ["source_graph","candidate_graph"] for a in p[side]["assertions"])
    if p["expected_outcome"]=="REVIEW":
        assert has_uncertain
        assert any(m["status"]=="UNCERTAIN" for m in p["gold_alignment"])
        uncertain_pair_ids.append(p["pair_id"])
        checks+=2

# Pre-frozen distribution requirements
assert outcomes=={"PASS_CANDIDATE":5,"REJECT":6,"REVIEW":1}, outcomes
assert shapes["ONE_TO_MANY"]>=2 and shapes["MANY_TO_ONE"]>=2 and shapes["MIXED"]>=1
assert set(scenarios)==allowed_scen, (set(scenarios),allowed_scen)
assert uncertain_pair_ids==["B1-P10"]

summary={
  "gate":"AT0_EN_V2_4_B1_REFERENCE_INTEGRITY",
  "status":"PASS",
  "model_inference":False,
  "pair_count":len(pairs),
  "outcomes":dict(outcomes),
  "mapping_shapes":dict(shapes),
  "scenario_counts":dict(scenarios),
  "alignment_status_counts":dict(alignment_status),
  "relation_alignment_status_counts":dict(relation_status),
  "source_assertion_count":source_assertions,
  "candidate_assertion_count":candidate_assertions,
  "source_relation_count":source_relations,
  "candidate_relation_count":candidate_relations,
  "uncertain_review_pairs":uncertain_pair_ids,
  "checks_passed":checks,
  "hashes":{
    "schema_sha256":sha(SCHEMA),
    "pairs_sha256":sha(PAIRS)
  }
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
