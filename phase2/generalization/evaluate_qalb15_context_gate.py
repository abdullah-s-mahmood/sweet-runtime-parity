"""Evaluate frozen QALB15 L2 runtime decisions against corrected DEV.

The runtime event file already exists before corrected text is read.
Persisted project result contains no QALB text.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path

from phase2.arabart_audit.build_full_arabart_edit_queue import align, group_nonkeep

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/dev/QALB-2015-L2-Dev.sent.no_ids"
COR=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/dev/QALB-2015-L2-Dev.cor.no_ids"
EVENTS=ROOT/"artifacts"/"QALB15_CONTEXT_RUNTIME_EVENTS.jsonl"
RUN=ROOT/"artifacts"/"QALB15_CONTEXT_RUNTIME_SUMMARY.json"
OUT=ROOT/"PHASE2_QALB15_CONTEXT_GENERALIZATION_RESULTS.json"

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
        else:
            span=[-1,-1]
        gb=[x["base"] for x in outs]
        sb=[x["base"] for x in srcs]
        out.append({
            "source_lexical_span":span,
            "source_bases":sb,
            "gold_bases":gb,
            "source_sha256":sha_text("\u241f".join(sb)),
            "gold_sha256":sha_text("\u241f".join(gb)),
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

def eval_policy(events,gold_by_line,policy,decision):
    accepted=[x for x in events if x["runtime_decisions"][policy]==decision]
    counts={};details=[]
    for ev in accepted:
        cls,g=classify(ev,gold_by_line[ev["line_id"]])
        counts[cls]=counts.get(cls,0)+1
        details.append({
            "event_id":ev["event_id"],
            "line_id":ev["line_id"],
            "line_hash":ev["line_hash"],
            "event_type":ev["event_type"],
            "source_lexical_span":ev["source_lexical_span"],
            "event_cost":ev["event_cost"],
            "source_bases_sha256":ev["source_bases_sha256"],
            "candidate_bases_sha256":ev["candidate_bases_sha256"],
            "source_morph":ev["source_morph"],
            "classification":cls,
            "gold_source_sha256":g["source_sha256"] if g else None,
            "gold_output_sha256":g["gold_sha256"] if g else None,
        })
    return {
        "candidate_events":len(accepted),
        "classification_counts":counts,
        "exact_gold_supported":counts.get("EXACT_GOLD_SUPPORTED",0),
        "needs_contextual_review":len(accepted)-counts.get("EXACT_GOLD_SUPPORTED",0),
        "event_audit_hashes":details,
    }

def main():
    run=json.loads(RUN.read_text(encoding="utf-8"))
    events=jl(EVENTS)
    raw=[x.strip() for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()]
    cor=[x.strip() for x in COR.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(raw)==len(cor)
    ids=run["selected_line_ids"]
    gold_by_line={i:gold_events(raw[i-1],cor[i-1]) for i in ids}

    policies={
        "WAW_ALIF_VERB_ONLY":eval_policy(events,gold_by_line,"WAW_ALIF_VERB_ONLY","ACCEPT"),
        "ACCUSATIVE_ALIF_SINGLE":eval_policy(events,gold_by_line,"ACCUSATIVE_ALIF_SINGLE","DIAGNOSTIC"),
        "FINAL_ALIF_GENERIC":eval_policy(events,gold_by_line,"FINAL_ALIF_GENERIC","DIAGNOSTIC"),
    }
    result={
        "status":"PHASE2_QALB15_CONTEXT_GENERALIZATION_GOLD_COMPARED",
        "development_generalization_only":True,
        "runtime_decisions_materialized_before_gold":True,
        "policy_frozen_before_gold":True,
        "corpus":"QALB-2015 L2 DEV deterministic 100-line raw-hash slice",
        "license_policy":"internal research/evaluation; no QALB text persisted",
        "selection_seed":run["selection_seed"],
        "selected_line_ids":ids,
        "selected_line_hashes":run["selected_line_hashes"],
        "runtime_events":len(events),
        "policy_results":policies,
        "nun_family_auto_accept":False,
        "qalb15_test_read":False,
        "qalb_text_persisted":False,
        "interpretation_contract":{
            "EXACT_GOLD_SUPPORTED":"automatic support",
            "SAME_GOLD_SPAN_DIFFERENT_OUTPUT":"contextual review required",
            "GOLD_OVERLAP_NONEXACT_SPAN":"contextual/alignment review required",
            "NO_GOLD_EDIT_OVERLAP":"contextual review required; not automatically wrong"
        }
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "runtime_events":result["runtime_events"],
        "policy_results":{k:{kk:vv for kk,vv in v.items() if kk!="event_audit_hashes"} for k,v in policies.items()}
    },ensure_ascii=False))

if __name__=="__main__":
    main()
