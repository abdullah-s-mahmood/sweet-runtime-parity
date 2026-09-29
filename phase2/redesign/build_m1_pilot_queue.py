#!/usr/bin/env python3
"""Rebuild the M1 blinded pilot from already-consumed Phase-2 Nahw evidence.

Historical labels are used only for deterministic stratification and are omitted
from the reviewer packet. This script never reads QALB, sealed data, or a new split.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
APPLIED=ROOT/"PHASE2_SURGICAL_APPLIED_EDIT_ADJUDICATION.jsonl"
QUEUE=ROOT/"PHASE2_SURGICAL_ADJUDICATION_QUEUE.jsonl"
OUT=Path(__file__).with_name("M1_PILOT_BLINDED_QUEUE.jsonl")

def rows(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def fnv1a(text):
    h=0x811C9DC5
    for ch in text:
        h ^= ord(ch)
        h=(h*0x01000193)&0xFFFFFFFF
    return h

def pick(pool, n):
    pool=sorted(pool,key=lambda x: fnv1a(f'{x["passage_id"]}:{x["edit_index"]}'))
    out=[]; seen=set()
    for x in pool:
        if len(out)>=n: break
        if x["passage_id"] not in seen:
            out.append(x); seen.add(x["passage_id"])
    for x in pool:
        if len(out)>=n: break
        if x not in out: out.append(x)
    return out

applied=rows(APPLIED)
passages={x["passage_id"]:x for x in rows(QUEUE)}
unsafe=[x for x in applied if x["classification"] in {"WRONG_CORRECTION","PARTIAL_CORRECTION","UNNECESSARY_EDIT"}]
positives=(
    pick([x for x in applied if x["classification"]=="SUPPORTED_CORRECTION"],8)
    + pick([x for x in applied if x["classification"]=="SUPPORTED_ALTERNATIVE"],5)
)
selected=sorted(unsafe+positives,key=lambda x: fnv1a(f'{x["passage_id"]}:{x["edit_index"]}'))
assert len(selected)==24

out=[]
for i,x in enumerate(selected,1):
    src=passages[x["passage_id"]]["source"]; a,b=x["source_span"]
    out.append({
      "m1_case_id":f"M1P-{i:03d}",
      "source_collection":"PHASE2_CONSUMED_NAHW_SURGICAL",
      "source_record":{"passage_id":x["passage_id"],"edit_index":x["edit_index"]},
      "source_text":src,
      "candidate_text":src[:a]+x["replacement"]+src[b:],
      "proposed_edit":{"source_span":x["source_span"],"source_surface":x["source_text"],"replacement_surface":x["replacement"]},
      "reviewer_packet_version":"M1_EDIT_CONTRACT_V1",
      "historical_labels_exposed_to_reviewer":False,
      "model_identity_exposed_to_reviewer":False,
      "reference_exposed_in_primary_pass":False
    })
OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
print(f"wrote {len(out)} cases to {OUT}")
