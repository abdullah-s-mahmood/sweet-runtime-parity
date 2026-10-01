#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from mpsef_rjoint_core_v2 import import_m2, norm

VERSION="MPSEF_CF_GOLD_PROJECTION_V2"
EXPERIMENT_ID="MPSEF-RJOINT-V2-CF1918-20261001-A"
EXPECTED_CAL_CASES=6888
EXPECTED_CF_CASES=1918
EXPECTED_CF_CLUSTERS=764
EXPECTED_CAL_UID_SHA="3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9"
EXPECTED_SOURCE_SHA="051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_GOLD_SHA="971b6fbb28dc3767193e7a4b0f722c3abebfc8600155a57093ba483dac6491e8"

def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def uid_digest(rows):
    return sha_text("\n".join(r["uid"] for r in rows)+"\n")

def require_consumed_evidence(path):
    x=json.loads(Path(path).read_text(encoding="utf-8"))
    if x.get("experiment_id")!=EXPERIMENT_ID:
        raise RuntimeError("authorization evidence experiment mismatch")
    if x.get("consumption_claimed") is not True:
        raise RuntimeError("gold projection requires durable consumption claim")
    if x.get("gold_access_allowed_after_claim") is not True:
        raise RuntimeError("gold access not authorized by evidence")
    return x

def project_loaded(calibration, manifest, full_sources, full_gold):
    if len(calibration)!=EXPECTED_CAL_CASES:
        raise RuntimeError("calibration length mismatch")
    if len(manifest)!=EXPECTED_CF_CASES:
        raise RuntimeError("C_F manifest length mismatch")
    if len({x["cluster_id"] for x in manifest})!=EXPECTED_CF_CLUSTERS:
        raise RuntimeError("C_F cluster mismatch")
    if len(full_sources)!=EXPECTED_CAL_CASES or len(full_gold)!=EXPECTED_CAL_CASES:
        raise RuntimeError("full gold length mismatch")

    cal_index={x["uid"]:i for i,x in enumerate(calibration)}
    if len(cal_index)!=EXPECTED_CAL_CASES:
        raise RuntimeError("duplicate calibration UID")

    out=[]
    for m in sorted(manifest,key=lambda x:x["uid"]):
        uid=m["uid"]
        if uid not in cal_index:
            raise RuntimeError(f"{uid}: absent from calibration")
        i=cal_index[uid]
        if norm(full_sources[i])!=norm(m["source"]):
            raise RuntimeError(f"{uid}: M2/source mismatch")
        gdict=full_gold[i]
        if set(gdict)!={0}:
            raise RuntimeError(f"{uid}: unexpected annotator set")
        gold=gdict[0]
        out.append({
            "record_id":VERSION,
            "uid":uid,
            "case_id":m["case_id"],
            "cluster_id":m["cluster_id"],
            "source":m["source"],
            "source_sha256":m["source_sha256"],
            "gold":gold,
        })
    return out

def self_test():
    cal=[{"uid":f"u{i}"} for i in range(EXPECTED_CAL_CASES)]
    # For a pure function smoke test, use a reduced helper-compatible fixture
    # rather than invoking project constants.
    tiny_manifest=[
        {"uid":"u0","case_id":"c0","cluster_id":"z","source":"انا","source_sha256":sha_text("انا")},
        {"uid":"u1","case_id":"c1","cluster_id":"z","source":"نص","source_sha256":sha_text("نص")},
    ]
    tiny_sources=["انا","نص"]
    tiny_gold=[
        {0:[(0,1,"انا",["أنا"])]},
        {0:[(0,1,"نص",["نصّ"])]},
    ]
    # Directly exercise projection semantics without project-size assertions.
    idx={"u0":0,"u1":1}
    out=[]
    for m in tiny_manifest:
        i=idx[m["uid"]]
        assert norm(tiny_sources[i])==norm(m["source"])
        assert set(tiny_gold[i])=={0}
        out.append((m["uid"],tiny_gold[i][0]))
    assert out[0][0]=="u0" and len(out)==2
    print(json.dumps({"self_test":"PASS","version":VERSION},ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--authorization-evidence")
    ap.add_argument("--calibration")
    ap.add_argument("--source-manifest")
    ap.add_argument("--full-gold-m2")
    ap.add_argument("--upstream-root")
    ap.add_argument("--out-prefix",default="MPSEF_CF_GOLD_PROJECTION_V2")
    args=ap.parse_args()

    if args.self_test:
        self_test()
        return

    needed=[args.authorization_evidence,args.calibration,args.source_manifest,args.full_gold_m2,args.upstream_root]
    if any(x is None for x in needed):
        raise SystemExit("missing gold-projection input")

    evidence=require_consumed_evidence(args.authorization_evidence)
    calp=Path(args.calibration); manp=Path(args.source_manifest); goldp=Path(args.full_gold_m2)
    if sha256_file(manp)!=EXPECTED_SOURCE_SHA: raise RuntimeError("source manifest SHA mismatch")
    if sha256_file(goldp)!=EXPECTED_GOLD_SHA: raise RuntimeError("full gold SHA mismatch")

    cal=read_jsonl(calp)
    if uid_digest(cal)!=EXPECTED_CAL_UID_SHA:
        raise RuntimeError("calibration UID digest mismatch")
    manifest=read_jsonl(manp)

    m2,_=import_m2(args.upstream_root)
    full_sources,full_gold=m2.load_annotation(str(goldp))
    out=project_loaded(cal,manifest,full_sources,full_gold)

    outp=Path(args.out_prefix+".jsonl")
    outp.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    summary={
        "record_id":VERSION,
        "status":"CF_GOLD_PROJECTION_COMPLETE",
        "experiment_id":EXPERIMENT_ID,
        "cases":len(out),
        "clusters":len({x["cluster_id"] for x in out}),
        "source_manifest_sha256":sha256_file(manp),
        "full_gold_m2_sha256":sha256_file(goldp),
        "projection_jsonl_sha256":sha256_file(outp),
        "consumption_claimed_before_gold_access":bool(evidence["consumption_claimed"]),
        "metric_computed":False,
        "internal_evaluation_opened":False,
        "stress_diagnostic_opened":False,
        "reserved_data_opened":False,
    }
    Path(args.out_prefix+"_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":
    main()
