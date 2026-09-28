"""Gold evaluation for frozen WAW_ALIF morphosyntactic decisions.

Runs only after runtime decisions are materialized.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path

from phase2.arabart_audit.build_full_arabart_edit_queue import align, group_nonkeep

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/ZAEBUC-v1.0/data/ar/train/train.sent.raw"
COR=UP/"data/gec/ZAEBUC-v1.0/data/ar/train/train.sent.cor"
EVENTS=ROOT/"artifacts"/"WAW_ALIF_MORPH_RUNTIME_EVENTS.jsonl"
RUN=ROOT/"artifacts"/"WAW_ALIF_MORPH_RUNTIME_SUMMARY.json"
OUT=ROOT/"PHASE2_WAW_ALIF_MORPH_GENERALIZATION_RESULTS.json"

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def gold_events(raw,cor):
    ops,_=align(raw,cor)
    out=[]
    for g in group_nonkeep(ops):
        srcs=[x["src"] for x in g if x["src"]]
        outs=[x["out"] for x in g if x["out"]]
        if srcs:
            lex=[x["lexical_index"] for x in srcs]
            span=[min(lex),max(lex)+1]
        else: span=[-1,-1]
        sb=[x["base"] for x in srcs]; gb=[x["base"] for x in outs]
        out.append({
            "source_lexical_span":span,
            "source_hash":sha_text("\u241f".join(sb)),
            "gold_hash":sha_text("\u241f".join(gb)),
            "gold_bases":gb,
        })
    return out

def overlap(a,b):
    if a[0]<0 or b[0]<0:return False
    return max(a[0],b[0])<min(a[1],b[1])

def classify(ev,gold):
    span=ev["source_lexical_span"]
    exact=[g for g in gold if g["source_lexical_span"]==span]
    for g in exact:
        if ev["candidate_bases"]==g["gold_bases"]:
            return "EXACT_GOLD_SUPPORTED",g
    if exact:return "SAME_GOLD_SPAN_DIFFERENT_OUTPUT",exact[0]
    ovs=[g for g in gold if overlap(span,g["source_lexical_span"])]
    if ovs:return "GOLD_OVERLAP_NONEXACT_SPAN",ovs[0]
    return "NO_GOLD_EDIT_OVERLAP",None

def evalset(events,gold_by_line,policy,decision):
    xs=[x for x in events if x["runtime_decisions"][policy]==decision]
    counts={};details=[]
    for x in xs:
        cls,g=classify(x,gold_by_line[x["line_id"]])
        counts[cls]=counts.get(cls,0)+1
        details.append({
            "event_id":x["event_id"],"line_id":x["line_id"],"line_hash":x["line_hash"],
            "source_lexical_span":x["source_lexical_span"],"event_cost":x["event_cost"],
            "source_hash":x["source_hash"],"candidate_hash":x["candidate_hash"],
            "source_contextual_top":x["source_contextual_top"],
            "candidate_contextual_top":x["candidate_contextual_top"],
            "source_lexical_flags":x["source_lexical_flags"],
            "candidate_lexical_flags":x["candidate_lexical_flags"],
            "classification":cls,
            "gold_source_hash":g["source_hash"] if g else None,
            "gold_output_hash":g["gold_hash"] if g else None,
        })
    return {
        "events":len(xs),
        "classification_counts":counts,
        "exact_gold_supported":counts.get("EXACT_GOLD_SUPPORTED",0),
        "needs_contextual_review":len(xs)-counts.get("EXACT_GOLD_SUPPORTED",0),
        "event_audit_hashes":details,
    }

def main():
    run=json.loads(RUN.read_text(encoding="utf-8"))
    events=jl(EVENTS)
    raw=[x.strip() for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()]
    cor=[x.strip() for x in COR.read_text(encoding="utf-8").splitlines() if x.strip()]
    ids=run["selected_line_ids"]
    gold={i:gold_events(raw[i-1],cor[i-1]) for i in ids}
    result={
        "status":"PHASE2_WAW_ALIF_MORPH_GENERALIZATION_GOLD_COMPARED",
        "runtime_decisions_materialized_before_gold":True,
        "policy_frozen_before_gold":True,
        "external_corpus":"ZAEBUC-v1.0 Arabic TRAIN fresh raw-selected slice",
        "external_license":"CC BY-NC-SA 4.0",
        "selected_line_ids":ids,
        "selected_line_hashes":run["selected_line_hashes"],
        "runtime_events":len(events),
        "policy_results":{
            "SOURCE_SHAPE_ONLY":evalset(events,gold,"SOURCE_SHAPE_ONLY","DIAGNOSTIC"),
            "WAW_ALIF_MORPH_RECOVERY":evalset(events,gold,"WAW_ALIF_MORPH_RECOVERY","DIAGNOSTIC"),
            "WAW_ALIF_MORPH_STRICT":evalset(events,gold,"WAW_ALIF_MORPH_STRICT","ACCEPT"),
        },
        "success_contract":{
            "strict_minimum_preferred_events":3,
            "any_demonstrably_wrong_strict_event":"MODIFY",
            "strict_below_3_events":"UNPROVEN_LOW_COVERAGE"
        },
        "zaebuc_dev_read":False,
        "zaebuc_test_read":False,
        "full_corpus_text_persisted":False,
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "policy_results":{k:{kk:vv for kk,vv in v.items() if kk!="event_audit_hashes"} for k,v in result["policy_results"].items()}
    },ensure_ascii=False))

if __name__=="__main__":
    main()
