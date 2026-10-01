#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_CASES = 1918
EXPECTED_P1_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P2_SHA = "f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b"
VERSION = "MPSEF_DIAGNOSTIC_COMPONENTS_V1"

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def validate_components(row):
    src=row["source"]
    out=row["full_proposer_output"]
    comps=row.get("diagnostic_components_only")
    if not isinstance(comps,list):
        raise RuntimeError(f'{row["uid"]}: missing diagnostic components')
    for i,c in enumerate(comps):
        ss,se=c["source_start"],c["source_end"]
        os,oe=c["output_start"],c["output_end"]
        if src[ss:se] != c["source_text"]:
            raise RuntimeError(f'{row["uid"]}:{i}: source slice mismatch')
        if out[os:oe] != c["output_text"]:
            raise RuntimeError(f'{row["uid"]}:{i}: output slice mismatch')
        if c["op"] not in {"REPLACE","DELETE","INSERT","EQUAL"}:
            # SequenceMatcher emits REPLACE/DELETE/INSERT for non-equal ops.
            raise RuntimeError(f'{row["uid"]}:{i}: unexpected op {c["op"]}')
    return comps

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--p1-proposals",required=True)
    ap.add_argument("--p2-proposals",required=True)
    ap.add_argument("--out-prefix",default="MPSEF_DIAGNOSTIC_COMPONENTS_V1")
    args=ap.parse_args()

    p1p,p2p=Path(args.p1_proposals),Path(args.p2_proposals)
    if sha256_file(p1p)!=EXPECTED_P1_SHA: raise RuntimeError("P1 SHA mismatch")
    if sha256_file(p2p)!=EXPECTED_P2_SHA: raise RuntimeError("P2 SHA mismatch")

    p1=read_jsonl(p1p); p2=read_jsonl(p2p)
    if len(p1)!=EXPECTED_CASES or len(p2)!=EXPECTED_CASES:
        raise RuntimeError("population mismatch")
    if {x["uid"] for x in p1}!={x["uid"] for x in p2}:
        raise RuntimeError("UID-set mismatch")

    out=[]
    total_components=0
    for proposer,rows in (("P1",p1),("P2",p2)):
        for row in rows:
            comps=validate_components(row)
            total_components += len(comps)
            out.append({
                "record_id":VERSION,
                "uid":row["uid"],
                "case_id":row["case_id"],
                "cluster_id":row["cluster_id"],
                "proposer":proposer,
                "source_sha256":row["source_version_hash"],
                "output_sha256":row["output_sha256"],
                "source":row["source"],
                "output":row["full_proposer_output"],
                "alignment_version":row.get("source_to_output_alignment_status"),
                "components":comps,
                "component_count":len(comps),
                "diagnostic_only":True,
                "executable":False,
                "gold_reference_consulted":False,
            })

    out.sort(key=lambda x:(x["uid"],x["proposer"]))
    path=Path(args.out_prefix+".jsonl")
    path.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")

    summary={
        "record_id":VERSION,
        "status":"DIAGNOSTIC_COMPONENTS_FROZEN",
        "records":len(out),
        "expected_records":EXPECTED_CASES*2,
        "cases":EXPECTED_CASES,
        "total_components":total_components,
        "P1_proposal_sha256":sha256_file(p1p),
        "P2_proposal_sha256":sha256_file(p2p),
        "diagnostic_jsonl_sha256":sha256_file(path),
        "gold_reference_consulted":False,
        "reference_content_used":False,
        "executable_actions_created":False,
        "R_joint_computed":False,
        "R_raw_computed":False,
    }
    Path(args.out_prefix+"_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":
    main()
