from __future__ import annotations
import importlib.util, pathlib

HERE=pathlib.Path(__file__).resolve().parent
BRIDGE=HERE/"b2_extraction_bridge.py"

src=BRIDGE.read_text(encoding="utf-8")
for forbidden in ["gold_alignment","gold_relation_alignment","expected_outcome","scenario_class"]:
    assert forbidden not in src, forbidden

spec=importlib.util.spec_from_file_location("bridge",BRIDGE)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

fake={
  "evidence_spans":[
    {"span_id":"SP1","container_type":"SENTENCE","container_id":"x","char_start":0,"char_end":20,"quote":"Group A required 42 s"}
  ],
  "anchors":[
    {"anchor_id":"A1","anchor_type":"VALUE","normalized":42},
    {"anchor_id":"A2","anchor_type":"UNIT","normalized":"s"}
  ],
  "assertions":[
    {
      "assertion_id":"AS1","criticality":"CRITICAL","subject":"Group A","predicate_normalized":"REQUIRE",
      "object":"completion","polarity":"POSITIVE","modality":"ASSERTED","causality":"NONE",
      "scope_operators":[],"temporal_context":[],"population":[],"baseline":[],
      "extraction_status":"CERTAIN","anchor_refs":["A1","A2"],"evidence_span_ids":["SP1"]
    }
  ]
}
g=m.bridge_extracted_graph(fake,"G1")
assert g["relations"]==[]
assert len(g["assertions"])==1
a=g["assertions"][0]
assert a["bindings"]=={"unit":"s","value":42},a["bindings"]
assert a["evidence"]=="Group A required 42 s"
assert a["predicate"]=="REQUIRE"

print("B2 bridge contract regressions: PASS")
