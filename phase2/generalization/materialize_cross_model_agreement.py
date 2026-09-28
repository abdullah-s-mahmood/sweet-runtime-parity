"""Materialize gold-blind exact edit-event agreement between SWEET NoPnx1 and AraBART.

This stage has no QALB corrected/gold file available.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path

from phase2.generalization.cross_model_common import read_jsonl,protected_risk,sha_text

ROOT=Path(__file__).resolve().parents[2]
SWEET_DIR=ROOT/"artifacts"/"sweet"
ARA_DIR=ROOT/"artifacts"/"arabart"
SWEET_EVENTS=SWEET_DIR/"CROSS_SWEET_EVENTS.jsonl"
ARA_EVENTS=ARA_DIR/"CROSS_ARABART_EVENTS.jsonl"
SWEET_SUM=SWEET_DIR/"CROSS_SWEET_SUMMARY.json"
ARA_SUM=ARA_DIR/"CROSS_ARABART_SUMMARY.json"
OUT=ROOT/"artifacts"/"CROSS_MODEL_AGREEMENT_FEATURES.jsonl"
SUMMARY=ROOT/"artifacts"/"CROSS_MODEL_AGREEMENT_RUNTIME.json"

def file_sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def all_sub(e):
    ops=e.get("primitive_ops") or []
    return bool(ops) and all(x=="SUB" for x in ops)

def single_sub(e):
    span=e.get("source_lexical_span") or [-1,-1]
    return (
        e.get("primitive_ops")==["SUB"]
        and len(e.get("source_bases") or [])==1
        and len(e.get("output_bases") or [])==1
        and span[0]>=0 and span[1]-span[0]==1
    )

def bounded_sub(e):
    span=e.get("source_lexical_span") or [-1,-1]
    n=len(e.get("source_bases") or [])
    return (
        all_sub(e)
        and 1<=n<=3
        and len(e.get("output_bases") or [])==n
        and span[0]>=0 and span[1]-span[0]==n
    )

def event_key(e):
    return (
        int(e["line_id"]),
        tuple(map(int,e["source_lexical_span"])),
        tuple(e.get("source_bases") or []),
        tuple(e.get("output_bases") or []),
    )

def main():
    ss=json.loads(SWEET_SUM.read_text(encoding="utf-8"))
    aa=json.loads(ARA_SUM.read_text(encoding="utf-8"))
    assert ss["selection_seed"]==aa["selection_seed"]
    assert ss["selected_line_ids"]==aa["selected_line_ids"]
    assert ss["selected_line_hashes"]==aa["selected_line_hashes"]
    assert ss["raw_sha256"]==aa["raw_sha256"]
    assert ss["gold_read"] is False and aa["gold_read"] is False

    swe=read_jsonl(SWEET_EVENTS)
    ara=read_jsonl(ARA_EVENTS)
    amap={}
    for a in ara:
        amap.setdefault(event_key(a),[]).append(a)

    rows=[];seen=set()
    for s in swe:
        k=event_key(s)
        for a in amap.get(k,[]):
            dedup=(k,s["event_id"],a["event_id"])
            if dedup in seen:continue
            seen.add(dedup)
            veto=sorted(set(protected_risk(s)+protected_risk(a)))
            single=single_sub(s) and single_sub(a)
            bounded=bounded_sub(s) and bounded_sub(a)
            if not veto and tuple(s["source_bases"])==tuple(a["source_bases"]) and tuple(s["output_bases"])==tuple(a["output_bases"]):
                pd="ACCEPT" if single else "REVIEW"
                pb="ACCEPT" if bounded else "REVIEW"
            else:
                pd="REJECT" if veto else "REVIEW"
                pb="REJECT" if veto else "REVIEW"
            source_hash=sha_text("\u241f".join(s["source_bases"]))
            output_hash=sha_text("\u241f".join(s["output_bases"]))
            rows.append({
                "agreement_id":"XAGR-"+sha_text("|".join([
                    str(s["line_id"]),str(s["source_lexical_span"]),
                    source_hash,output_hash
                ]))[:20],
                "line_id":int(s["line_id"]),
                "line_hash":s["line_hash"],
                "source_lexical_span":s["source_lexical_span"],
                "span_length":s["source_lexical_span"][1]-s["source_lexical_span"][0],
                "source_bases":s["source_bases"],
                "output_bases":s["output_bases"],
                "source_surfaces":s["source_surfaces"],
                "output_surfaces":s["output_surfaces"],
                "source_hash":source_hash,
                "output_hash":output_hash,
                "sweet_event_id":s["event_id"],
                "arabart_event_id":a["event_id"],
                "sweet_ops":s["primitive_ops"],
                "arabart_ops":a["primitive_ops"],
                "sweet_event_cost":s["event_cost"],
                "arabart_event_cost":a["event_cost"],
                "veto_reasons":veto,
                "runtime_decisions":{
                    "EXACT_SINGLE_SUB_AGREEMENT":pd,
                    "EXACT_BOUNDED_SUB_EVENT_AGREEMENT":pb,
                },
            })

    # A source/output agreement key should be unique even if alignment internals duplicate.
    uniq={}
    for x in rows:
        key=(x["line_id"],tuple(x["source_lexical_span"]),x["source_hash"],x["output_hash"])
        if key not in uniq:uniq[key]=x
    rows=list(uniq.values())
    rows.sort(key=lambda x:(x["line_id"],x["source_lexical_span"],x["agreement_id"]))

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    policies=["EXACT_SINGLE_SUB_AGREEMENT","EXACT_BOUNDED_SUB_EVENT_AGREEMENT"]
    counts={p:{
        "ACCEPT":sum(x["runtime_decisions"][p]=="ACCEPT" for x in rows),
        "REVIEW":sum(x["runtime_decisions"][p]=="REVIEW" for x in rows),
        "REJECT":sum(x["runtime_decisions"][p]=="REJECT" for x in rows),
    } for p in policies}
    summary={
        "status":"CROSS_MODEL_AGREEMENT_RUNTIME_FROZEN",
        "gold_read":False,
        "selection_seed":ss["selection_seed"],
        "selected_line_ids":ss["selected_line_ids"],
        "selected_line_hashes":ss["selected_line_hashes"],
        "raw_sha256":ss["raw_sha256"],
        "sweet_event_rows":len(swe),
        "arabart_event_rows":len(ara),
        "exact_agreement_rows":len(rows),
        "decision_counts":counts,
        "veto_rows":sum(bool(x["veto_reasons"]) for x in rows),
        "sweet_summary_sha256":file_sha(SWEET_SUM),
        "arabart_summary_sha256":file_sha(ARA_SUM),
        "features_sha256":file_sha(OUT),
        "qalb15_test_read":False,
        "policy_frozen_before_gold":True,
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="selected_line_hashes"},ensure_ascii=False))

if __name__=="__main__":
    main()
