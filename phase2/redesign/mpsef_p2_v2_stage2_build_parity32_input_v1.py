#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

EXPECTED_MANIFEST_SHA="384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e"
EXPECTED_P2_SHA="df89c7dc2c7f177b3c4ca02e8df8a291b6de917a81246c5258f1f66652e1f69e"

def sha_file(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def load(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--frozen-p2",required=True)
    ap.add_argument("--fresh-out",required=True)
    ap.add_argument("--reversed-out",required=True)
    args=ap.parse_args()
    if sha_file(args.manifest)!=EXPECTED_MANIFEST_SHA: raise RuntimeError("MANIFEST_SHA_MISMATCH")
    if sha_file(args.frozen_p2)!=EXPECTED_P2_SHA: raise RuntimeError("P2_SHA_MISMATCH")
    m=load(args.manifest); p=load(args.frozen_p2); by={r["uid"]:r for r in p}
    rows=[]
    for x in m:
        r=by[x["uid"]]
        if r["source_sha256"]!=x["source_sha256"]: raise RuntimeError("SOURCE_SHA_MISMATCH:"+x["uid"])
        rows.append({
          "uid":r["uid"],"case_id":r["case_id"],"cluster_id":r["cluster_id"],
          "source":r["source"],"source_sha256":r["source_sha256"]
        })
    if len(rows)!=32 or len({r["uid"] for r in rows})!=32: raise RuntimeError("PARITY_INPUT_COUNT_OR_UID_FAIL")
    def write(path, rr):
        Path(path).write_text("\n".join(json.dumps(r,ensure_ascii=False,sort_keys=True) for r in rr)+"\n",encoding="utf-8")
    write(args.fresh_out,rows)
    write(args.reversed_out,list(reversed(rows)))
    print(json.dumps({
      "status":"PASS","n":32,
      "fresh_sha256":sha_file(args.fresh_out),
      "reversed_sha256":sha_file(args.reversed_out)
    },indent=2))

if __name__=="__main__": main()
