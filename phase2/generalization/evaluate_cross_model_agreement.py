"""Evaluate frozen cross-model agreement decisions against QALB-2015 L2 TRAIN gold.

The runtime agreement artifact must already exist before corrected text is opened.
The committed result contains no QALB text.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path

from phase2.generalization.cross_model_common import read_jsonl,read_nonempty_lines,sha_text
from phase2.arabart_audit.build_full_arabart_edit_queue import align,group_nonkeep

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
COR=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.cor.no_ids"
RUNTIME=ROOT/"artifacts"/"CROSS_MODEL_AGREEMENT_RUNTIME.json"
FEATURES=ROOT/"artifacts"/"CROSS_MODEL_AGREEMENT_FEATURES.jsonl"
OUT=ROOT/"PHASE2_CROSS_MODEL_AGREEMENT_RESULTS.json"

def file_sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def gold_events(raw,cor):
    ops,_=align(raw,cor)
    out=[]
    for g in group_nonkeep(ops):
        srcs=[x["src"] for x in g if x["src"]]
        outs=[x["out"] for x in g if x["out"]]
        if srcs:
            ids=[x["lexical_index"] for x in srcs]
            span=[min(ids),max(ids)+1]
        else:
            span=[-1,-1]
        sb=[x["base"] for x in srcs];ob=[x["base"] for x in outs]
        out.append({
            "source_lexical_span":span,
            "source_hash":sha_text("\u241f".join(sb)),
            "output_hash":sha_text("\u241f".join(ob)),
            "output_bases":ob,
        })
    return out

def overlap(a,b):
    if a[0]<0 or b[0]<0:return False
    return max(a[0],b[0])<min(a[1],b[1])

def classify(row,gold):
    span=row["source_lexical_span"]
    exact=[g for g in gold if g["source_lexical_span"]==span]
    for g in exact:
        if row["output_hash"]==g["output_hash"]:
            return "EXACT_GOLD_SUPPORTED",g
    if exact:return "SAME_GOLD_SPAN_DIFFERENT_OUTPUT",exact[0]
    ovs=[g for g in gold if overlap(span,g["source_lexical_span"])]
    if ovs:return "GOLD_OVERLAP_NONEXACT_SPAN",ovs[0]
    return "NO_GOLD_EDIT_OVERLAP",None

def policy_result(rows,gold_by_line,policy):
    acc=[x for x in rows if x["runtime_decisions"][policy]=="ACCEPT"]
    counts={};audit=[];by_line={}
    for x in acc:
        cls,g=classify(x,gold_by_line[x["line_id"]])
        counts[cls]=counts.get(cls,0)+1
        by_line[str(x["line_id"])]=by_line.get(str(x["line_id"]),0)+1
        audit.append({
            "agreement_id":x["agreement_id"],
            "line_id":x["line_id"],
            "line_hash":x["line_hash"],
            "source_lexical_span":x["source_lexical_span"],
            "span_length":x["span_length"],
            "source_hash":x["source_hash"],
            "candidate_hash":x["output_hash"],
            "classification":cls,
            "gold_source_hash":g["source_hash"] if g else None,
            "gold_output_hash":g["output_hash"] if g else None,
            "veto_count":len(x["veto_reasons"]),
        })
    return {
        "accepted":len(acc),
        "classification_counts":counts,
        "exact_gold_supported":counts.get("EXACT_GOLD_SUPPORTED",0),
        "needs_contextual_review":len(acc)-counts.get("EXACT_GOLD_SUPPORTED",0),
        "accepted_line_count":len(by_line),
        "max_accepts_in_one_line":max(by_line.values()) if by_line else 0,
        "span_length_counts":{
            str(n):sum(x["span_length"]==n for x in acc)
            for n in sorted({x["span_length"] for x in acc})
        },
        "event_audit_hashes":audit,
    }

def main():
    runtime=json.loads(RUNTIME.read_text(encoding="utf-8"))
    assert runtime["gold_read"] is False
    assert runtime["policy_frozen_before_gold"] is True
    rows=read_jsonl(FEATURES)

    raw=read_nonempty_lines(RAW)
    cor=read_nonempty_lines(COR)
    assert len(raw)==len(cor)
    ids=runtime["selected_line_ids"]
    for line_id,line_hash in zip(ids,runtime["selected_line_hashes"]):
        assert sha_text(runtime["selection_seed"]+"|"+raw[line_id-1])==line_hash

    gold={i:gold_events(raw[i-1],cor[i-1]) for i in ids}
    policies={
        "EXACT_SINGLE_SUB_AGREEMENT":policy_result(rows,gold,"EXACT_SINGLE_SUB_AGREEMENT"),
        "EXACT_BOUNDED_SUB_EVENT_AGREEMENT":policy_result(rows,gold,"EXACT_BOUNDED_SUB_EVENT_AGREEMENT"),
    }
    primary=policies["EXACT_SINGLE_SUB_AGREEMENT"]
    result={
        "status":"PHASE2_CROSS_MODEL_AGREEMENT_GOLD_COMPARED",
        "development_generalization_only":True,
        "runtime_decisions_materialized_before_gold":True,
        "policy_frozen_before_gold":True,
        "corpus":"QALB-2015 L2 TRAIN deterministic raw-only 50-line slice",
        "license_policy":"internal research/evaluation; no QALB text persisted",
        "selection_seed":runtime["selection_seed"],
        "selected_line_ids":ids,
        "selected_line_hashes":runtime["selected_line_hashes"],
        "runtime_artifact_sha256":file_sha(RUNTIME),
        "agreement_features_sha256":file_sha(FEATURES),
        "sweet_event_rows":runtime["sweet_event_rows"],
        "arabart_event_rows":runtime["arabart_event_rows"],
        "exact_agreement_rows":runtime["exact_agreement_rows"],
        "policy_results":policies,
        "primary_success_contract":{
            "preferred_minimum_accepts":10,
            "coverage_status":"SUFFICIENT_FOR_REVIEW" if primary["accepted"]>=10 else "UNPROVEN_LOW_COVERAGE",
            "any_demonstrably_wrong_after_review":"MODIFY",
            "any_partial_after_review":"DO_NOT_PROMOTE",
        },
        "qalb15_test_read":False,
        "qalb_text_persisted":False,
        "interpretation_contract":{
            "EXACT_GOLD_SUPPORTED":"automatic support",
            "SAME_GOLD_SPAN_DIFFERENT_OUTPUT":"bounded contextual review required",
            "GOLD_OVERLAP_NONEXACT_SPAN":"bounded contextual/alignment review required",
            "NO_GOLD_EDIT_OVERLAP":"bounded contextual review required; not automatically wrong"
        }
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    # Strict leakage guard: no Arabic corpus text may be committed.
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped),"Arabic text leaked into committed QALB result"
    print(json.dumps({
        "status":result["status"],
        "sweet_event_rows":result["sweet_event_rows"],
        "arabart_event_rows":result["arabart_event_rows"],
        "exact_agreement_rows":result["exact_agreement_rows"],
        "policy_results":{k:{kk:vv for kk,vv in v.items() if kk!="event_audit_hashes"} for k,v in policies.items()},
        "primary_success_contract":result["primary_success_contract"],
    },ensure_ascii=False))

if __name__=="__main__":
    main()
