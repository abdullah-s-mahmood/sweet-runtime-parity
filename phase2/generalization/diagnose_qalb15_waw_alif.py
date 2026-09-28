"""Raw-only diagnostic for WAW->WAW+ALIF candidate scarcity on QALB15 DEV.

Reads no corrected/gold text. Produces aggregate counts only, no QALB text.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
EVENTS=ROOT/"artifacts"/"QALB15_CONTEXT_RUNTIME_EVENTS.jsonl"
OUT=ROOT/"PHASE2_QALB15_WAW_ALIF_RAW_DIAGNOSTIC.json"

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rows=jl(EVENTS)
    candidates=[]
    for x in rows:
        sb=x.get("source_bases") or []
        cb=x.get("candidate_bases") or []
        if len(sb)==len(cb)==1 and x.get("primitive_ops")==["SUB"] and cb[0]==sb[0]+"ا" and sb[0].endswith("و"):
            morph=(x.get("source_morph") or [None])[0] or {}
            candidates.append({
                "event_id":x["event_id"],
                "line_id":x["line_id"],
                "line_hash":x["line_hash"],
                "event_cost":x["event_cost"],
                "source_hash":x["source_bases_sha256"],
                "candidate_hash":x["candidate_bases_sha256"],
                "pos":morph.get("pos"),
                "num":morph.get("num"),
                "per":morph.get("per"),
                "asp":morph.get("asp"),
                "mod":morph.get("mod"),
                "vox":morph.get("vox"),
            })
    pos_counts={}
    feature_counts={}
    for x in candidates:
        pos_counts[str(x["pos"])]=pos_counts.get(str(x["pos"]),0)+1
        key="|".join(str(x[k]) for k in ("pos","num","per","asp","mod","vox"))
        feature_counts[key]=feature_counts.get(key,0)+1
    obj={
        "status":"QALB15_WAW_ALIF_RAW_ONLY_DIAGNOSTIC_COMPLETE",
        "gold_read":False,
        "candidate_shape":"single SUB; source ends و; candidate == source + ا",
        "candidate_count":len(candidates),
        "event_cost_le_025":sum(x["event_cost"]<=0.25 for x in candidates),
        "pos_counts":pos_counts,
        "morph_feature_counts":feature_counts,
        "hashed_event_records":candidates,
        "qalb_text_persisted":False,
        "interpretation":"Diagnostic only. Must not be used to retune/evaluate a policy on the consumed QALB15 DEV slice."
    }
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in obj.items() if k!="hashed_event_records"},ensure_ascii=False))

if __name__=="__main__":
    main()
