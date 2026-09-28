"""Evaluate already-frozen ZAEBUC DEV runtime decisions against DEV corrected text.

This script runs only after the runtime event file exists.
No runtime decision is changed here.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path

from phase2.arabart_audit.build_full_arabart_edit_queue import align, group_nonkeep

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/ZAEBUC-v1.0/data/ar/dev/dev.sent.raw"
COR=UP/"data/gec/ZAEBUC-v1.0/data/ar/dev/dev.sent.cor"
EVENTS=ROOT/"artifacts"/"ZAEBUC_DEV_RUNTIME_EVENTS.jsonl"
RUNTIME=ROOT/"artifacts"/"ZAEBUC_DEV_RUNTIME_SUMMARY.json"
OUT=ROOT/"PHASE2_ZAEBUC_GENERALIZATION_RESULTS.json"

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def gold_events(raw,cor):
    ops,total=align(raw,cor)
    out=[]
    for g in group_nonkeep(ops):
        srcs=[x["src"] for x in g if x["src"]]
        outs=[x["out"] for x in g if x["out"]]
        if srcs:
            lex=[x["lexical_index"] for x in srcs]
            ls=[min(lex),max(lex)+1]
        else:
            ls=[-1,-1]
        out.append({
            "source_lexical_span":ls,
            "source_bases":[x["base"] for x in srcs],
            "gold_bases":[x["base"] for x in outs],
            "gold_words":[x["surface"] for x in outs],
            "primitive_ops":[x["op"] for x in g],
            "cost":sum(float(x["cost"]) for x in g),
        })
    return out

def overlap(a,b):
    if a[0]<0 or b[0]<0:return False
    return max(a[0],b[0])<min(a[1],b[1])

def classify(event,gold):
    span=event["source_lexical_span"]
    exact_span=[g for g in gold if g["source_lexical_span"]==span]
    for g in exact_span:
        if event["output_bases"]==g["gold_bases"]:
            return "EXACT_GOLD_SUPPORTED",g
    ovs=[g for g in gold if overlap(span,g["source_lexical_span"])]
    if exact_span:
        return "SAME_GOLD_SPAN_DIFFERENT_OUTPUT",exact_span[0]
    if ovs:
        return "GOLD_OVERLAP_NONEXACT_SPAN",ovs[0]
    return "NO_GOLD_EDIT_OVERLAP",None

def main():
    runtime=json.loads(RUNTIME.read_text(encoding="utf-8"))
    events=jl(EVENTS)
    raw=[x.strip() for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()]
    cor=[x.strip() for x in COR.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(raw)==len(cor)==runtime["raw_lines"]

    gold_by_line={i+1:gold_events(s,t) for i,(s,t) in enumerate(zip(raw,cor))}
    policy_results={}
    for policy in ("EVENT_STRUCTURAL_TYPED","EVENT_STRUCTURAL_STRICT"):
        accepted=[x for x in events if x["runtime_decisions"][policy]=="ACCEPT"]
        counts={}
        details=[]
        for x in accepted:
            cls,g=classify(x,gold_by_line[x["line_id"]])
            counts[cls]=counts.get(cls,0)+1
            details.append({
                "event_id":x["event_id"],
                "line_id":x["line_id"],
                "event_type":x["event_type"],
                "source_text":x["source_text"],
                "candidate_output":" ".join(x["output_words"]),
                "source_lexical_span":x["source_lexical_span"],
                "classification":cls,
                "gold_event":g,
                "event_cost":x["event_cost"],
            })
        policy_results[policy]={
            "accepted":len(accepted),
            "automatic_gold_classification_counts":counts,
            "exact_gold_supported":counts.get("EXACT_GOLD_SUPPORTED",0),
            "needs_manual_adjudication":len(accepted)-counts.get("EXACT_GOLD_SUPPORTED",0),
            "accepted_details":details,
        }

    # Gold structural family diagnostics: the gate is not tuned from this.
    total_gold=sum(len(x) for x in gold_by_line.values())
    obj={
        "status":"PHASE2_ZAEBUC_DISJOINT_GENERALIZATION_GOLD_COMPARED",
        "external_corpus":"ZAEBUC-v1.0 Arabic DEV",
        "external_license":"CC BY-NC-SA 4.0",
        "runtime_decisions_materialized_before_gold":True,
        "rules_frozen_before_gold":True,
        "raw_lines":len(raw),
        "runtime_events":len(events),
        "gold_edit_events":total_gold,
        "policy_results":policy_results,
        "interpretation_contract":{
            "EXACT_GOLD_SUPPORTED":"May be counted as automatic support.",
            "SAME_GOLD_SPAN_DIFFERENT_OUTPUT":"Requires contextual adjudication; may be valid alternative, partial, or wrong.",
            "GOLD_OVERLAP_NONEXACT_SPAN":"Requires contextual/alignment adjudication.",
            "NO_GOLD_EDIT_OVERLAP":"Requires contextual adjudication; do not automatically call wrong because alternative corrections are possible."
        },
        "license_note":"No full ZAEBUC corpus text is committed. accepted_details contain only bounded excerpts needed for scientific audit and remain subject to ZAEBUC CC BY-NC-SA 4.0.",
        "test_split_read":False,
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":obj["status"],
        "raw_lines":obj["raw_lines"],
        "runtime_events":obj["runtime_events"],
        "gold_edit_events":obj["gold_edit_events"],
        "policies":{p:{k:v for k,v in d.items() if k!="accepted_details"} for p,d in policy_results.items()},
    },ensure_ascii=False))

if __name__=="__main__":
    main()
