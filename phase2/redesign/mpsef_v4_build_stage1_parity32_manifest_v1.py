#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

VERSION="MPSEF_V4_STAGE1_PARITY32_MANIFEST_V1"
SALT="MPSEF-V4-STAGE1-PARITY-32-20261001-A"
EXPECTED_PACKET_SHA="8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1"
N=32

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def rank(uid): return hashlib.sha256(f"{SALT}|{uid}".encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--packet",required=True)
    ap.add_argument("--out-prefix",default="MPSEF_V4_STAGE1_PARITY32_MANIFEST_V1")
    a=ap.parse_args()
    p=Path(a.packet)
    got=sha_bytes(p.read_bytes())
    if got!=EXPECTED_PACKET_SHA:
        raise RuntimeError(f"PACKET_SHA_MISMATCH:{got}")
    rows=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(rows)!=128:
        raise RuntimeError(f"PACKET_COUNT_MISMATCH:{len(rows)}")
    selected=sorted(rows,key=lambda r:(rank(str(r["uid"])),str(r["uid"])))[:N]
    out=[{
        "rank_index":i+1,
        "rank_sha256":rank(str(r["uid"])),
        "uid":r["uid"],
        "case_id":r["case_id"],
        "cluster_id":r["cluster_id"],
        "source_sha256":r["source_sha256"],
    } for i,r in enumerate(selected)]
    op=Path(a.out_prefix+".jsonl")
    op.write_text("\n".join(json.dumps(x,ensure_ascii=False,sort_keys=True) for x in out)+"\n",encoding="utf-8")
    summary={
        "record_id":VERSION,
        "status":"PASS",
        "salt":SALT,
        "packet_sha256":got,
        "n":len(out),
        "uid_count":len({x["uid"] for x in out}),
        "cluster_count":len({x["cluster_id"] for x in out}),
        "manifest_sha256":sha_bytes(op.read_bytes()),
        "gold_reference_consulted":False,
        "proposer_output_consulted":False,
        "quality_metric_computed":False,
    }
    Path(a.out_prefix+"_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
