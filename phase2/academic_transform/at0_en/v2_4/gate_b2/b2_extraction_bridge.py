from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
GATE_A=HERE.parent/"gate_a"
EXTRACTOR_PATH=GATE_A/"source_assertion_extractor.py"

spec=importlib.util.spec_from_file_location("a2",EXTRACTOR_PATH)
a2=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a2)

ALLOWED_MODALITY={"ASSERTED","MAY","CAN","COULD","LIKELY","POSSIBLE","UNCERTAIN","OTHER"}
ALLOWED_CAUSALITY={"NONE","ASSOCIATION_ONLY","CAUSAL","EXPLICIT_NON_CAUSAL"}
ALLOWED_POLARITY={"POSITIVE","NEGATIVE"}
ALLOWED_CRITICALITY={"CRITICAL","MATERIAL","NON_MATERIAL"}
ALLOWED_CONFIDENCE={"CERTAIN","UNCERTAIN","AMBIGUOUS"}

ANCHOR_PREFIX={
    "COUNT":"count",
    "SYMBOL":"symbol",
    "EQUATION":"equation",
    "CITATION":"citation",
    "TIME":"time_anchor",
    "SEED":"seed",
    "GROUP":"group_anchor",
    "VALUE":"value",
    "UNIT":"unit",
}

def sha256_text(text:str)->str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _case(case_id:str,text:str)->dict:
    return {
        "case_id":case_id,
        "source_text":text,
        "source_sha256":sha256_text(text),
    }

def _bindings(assertion:dict, anchors_by_id:dict)->dict:
    selected=[]
    for aid in assertion.get("anchor_refs",[]):
        if aid not in anchors_by_id:
            raise ValueError(f"missing anchor ref {aid}")
        selected.append(anchors_by_id[aid])

    by_type={}
    for a in selected:
        by_type.setdefault(a["anchor_type"],[]).append(a)

    out={}
    for typ,items in sorted(by_type.items()):
        prefix=ANCHOR_PREFIX.get(typ,typ.lower())
        vals=[x["normalized"] for x in items]
        if typ in {"VALUE","UNIT","SEED"} and len(vals)==1:
            out[prefix]=vals[0]
        else:
            for i,val in enumerate(vals,1):
                out[f"{prefix}_{i}"]=val
    return out

def bridge_extracted_graph(extracted:dict, graph_id:str)->dict:
    evidence={x["span_id"]:x for x in extracted["evidence_spans"]}
    anchors={x["anchor_id"]:x for x in extracted["anchors"]}

    assertions=[]
    for a in extracted["assertions"]:
        if not a["evidence_span_ids"]:
            raise ValueError(f"assertion {a['assertion_id']} has no evidence span")
        sid=a["evidence_span_ids"][0]
        if sid not in evidence:
            raise ValueError(f"assertion {a['assertion_id']} references missing evidence span {sid}")

        criticality=a["criticality"]
        polarity=a["polarity"]
        modality=a["modality"]
        causality=a["causality"]
        confidence=a["extraction_status"]

        if criticality not in ALLOWED_CRITICALITY:
            raise ValueError(f"unsupported criticality {criticality}")
        if polarity not in ALLOWED_POLARITY:
            raise ValueError(f"unsupported polarity {polarity}")
        if modality not in ALLOWED_MODALITY:
            raise ValueError(f"unsupported modality {modality}")
        if causality not in ALLOWED_CAUSALITY:
            raise ValueError(f"unsupported causality {causality}")
        if confidence not in ALLOWED_CONFIDENCE:
            raise ValueError(f"unsupported confidence {confidence}")

        assertions.append({
            "id":a["assertion_id"],
            "criticality":criticality,
            "subject":a["subject"],
            "predicate":a["predicate_normalized"],
            "object":a["object"],
            "polarity":polarity,
            "modality":modality,
            "causality":causality,
            "scope":list(a["scope_operators"]),
            "time":list(a["temporal_context"]),
            "population":list(a["population"]),
            "baseline":list(a["baseline"]),
            "bindings":_bindings(a,anchors),
            "confidence_status":confidence,
            "evidence":evidence[sid]["quote"],
        })

    if not assertions:
        raise ValueError("non-empty raw text produced no assertions")

    # Frozen B2 contract: do not infer missing semantic relations.
    return {
        "graph_id":graph_id,
        "assertions":assertions,
        "relations":[],
    }

def extract_and_bridge(text:str, case_id:str, graph_id:str)->dict:
    extracted=a2.extract_source_assertions(_case(case_id,text))
    return bridge_extracted_graph(extracted,graph_id)
