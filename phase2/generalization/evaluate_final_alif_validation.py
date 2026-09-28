"""Evaluate frozen FINAL_ALIF decisions on the preselected ZAEBUC TRAIN slice."""
from __future__ import annotations
import json
from pathlib import Path
from phase2.generalization.evaluate_zaebuc_generalization import gold_events,classify

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/ZAEBUC-v1.0/data/ar/train/train.sent.raw"
COR=UP/"data/gec/ZAEBUC-v1.0/data/ar/train/train.sent.cor"
EV=ROOT/"artifacts"/"ZAEBUC_TRAIN_FINAL_ALIF_RUNTIME_EVENTS.jsonl"
RT=ROOT/"artifacts"/"ZAEBUC_TRAIN_FINAL_ALIF_RUNTIME.json"
OUT=ROOT/"PHASE2_FINAL_ALIF_GENERALIZATION_RESULTS.json"

def jl(p):return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    runtime=json.loads(RT.read_text(encoding="utf-8"))
    events=jl(EV)
    raw=[x.strip() for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()]
    cor=[x.strip() for x in COR.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(raw)==len(cor)==runtime["total_raw_lines"]
    selected=set(runtime["selected_line_ids"])
    gold={i:gold_events(raw[i-1],cor[i-1]) for i in selected}

    policies={}
    for policy in ("FINAL_ALIF_EVENT_ONLY","FINAL_ALIF_SINGLE_ONLY"):
        acc=[x for x in events if x["runtime_decisions"][policy]=="ACCEPT"]
        counts={};details=[]
        for x in acc:
            cls,g=classify(x,gold[x["original_line_id"]])
            counts[cls]=counts.get(cls,0)+1
            details.append({
                "event_id":x["event_id"],
                "original_line_id":x["original_line_id"],
                "event_type":x["event_type"],
                "source_text":x["source_text"],
                "candidate_output":" ".join(x["output_words"]),
                "source_lexical_span":x["source_lexical_span"],
                "classification":cls,
                "gold_event":g,
                "event_cost":x["event_cost"],
            })
        policies[policy]={
            "accepted":len(acc),
            "classification_counts":counts,
            "exact_gold_supported":counts.get("EXACT_GOLD_SUPPORTED",0),
            "needs_manual_adjudication":len(acc)-counts.get("EXACT_GOLD_SUPPORTED",0),
            "accepted_details":details,
        }

    obj={
        "status":"PHASE2_FINAL_ALIF_DISJOINT_VALIDATION_GOLD_COMPARED",
        "external_corpus":"ZAEBUC-v1.0 Arabic TRAIN deterministic 30-line raw-hash slice",
        "external_license":"CC BY-NC-SA 4.0",
        "selection_seed":runtime["selection_seed"],
        "selected_line_ids":runtime["selected_line_ids"],
        "runtime_decisions_materialized_before_gold":True,
        "policy_frozen_before_gold":True,
        "nun_family_auto_accept":False,
        "runtime_events":len(events),
        "policy_results":policies,
        "interpretation_contract":{
            "EXACT_GOLD_SUPPORTED":"automatic support",
            "SAME_GOLD_SPAN_DIFFERENT_OUTPUT":"manual contextual adjudication required",
            "GOLD_OVERLAP_NONEXACT_SPAN":"manual contextual/alignment adjudication required",
            "NO_GOLD_EDIT_OVERLAP":"manual contextual adjudication required"
        },
        "zaebuc_test_read":False,
        "license_note":"Only bounded accepted-event excerpts persisted; full external corpus is not committed."
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":obj["status"],
        "runtime_events":obj["runtime_events"],
        "policies":{k:{kk:vv for kk,vv in v.items() if kk!="accepted_details"} for k,v in policies.items()}
    },ensure_ascii=False))

if __name__=="__main__":
    main()
