#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json
from pathlib import Path

from transformers import BertForTokenClassification, BertTokenizer

from mpsef_p1_cf_proposals_v1 import (
    EXPECTED_MODEL_REV,
    EXPECTED_UPSTREAM_REV,
    EXPECTED_WEIGHT_SHA,
    batch_runner,
    install_rewrite_compat,
    sha256_file,
    single_runner,
)
from process_progress_v1 import update_state

VERSION="MPSEF_V4_STAGE1_P1_PARITY32_V1"
EXPECTED_PACKET_SHA="8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1"
EXPECTED_PARITY_SHA="384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e"
EXPECTED_P1_SHA="2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def load(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--packet",required=True)
    ap.add_argument("--parity-manifest",required=True)
    ap.add_argument("--p1-proposals",required=True)
    ap.add_argument("--model-dir",required=True)
    ap.add_argument("--upstream-root",required=True)
    ap.add_argument("--progress-state",default="MPSEF_V4_STAGE1_P1_PARITY32_PROGRESS.json")
    ap.add_argument("--out",default="MPSEF_V4_STAGE1_P1_PARITY32_V1.json")
    a=ap.parse_args()

    for path,exp,name in [
        (a.packet,EXPECTED_PACKET_SHA,"PACKET"),
        (a.parity_manifest,EXPECTED_PARITY_SHA,"PARITY"),
        (a.p1_proposals,EXPECTED_P1_SHA,"P1"),
    ]:
        got=sha_bytes(Path(path).read_bytes())
        if got!=exp: raise RuntimeError(f"{name}_SHA_MISMATCH:{got}")

    packet={r["uid"]:r for r in load(a.packet)}
    parity=load(a.parity_manifest)
    frozen={r["uid"]:r for r in load(a.p1_proposals)}
    uids=[r["uid"] for r in parity]
    if len(uids)!=32 or len(set(uids))!=32:
        raise RuntimeError("PARITY32_UID_COUNT_INVALID")
    rows=[packet[u] for u in uids]
    for r in rows:
        if r["source_sha256"]!=parity[uids.index(r["uid"])]["source_sha256"]:
            raise RuntimeError(f'PARITY_SOURCE_SHA_MISMATCH:{r["uid"]}')
        if r["uid"] not in frozen:
            raise RuntimeError(f'FROZEN_P1_UID_MISSING:{r["uid"]}')

    weight_sha=sha256_file(Path(a.model_dir)/"pytorch_model.bin")
    if weight_sha!=EXPECTED_WEIGHT_SHA:
        raise RuntimeError(f"P1_WEIGHT_SHA_MISMATCH:{weight_sha}")
    rewrite=install_rewrite_compat(Path(a.upstream_root))
    tok=BertTokenizer.from_pretrained(a.model_dir)
    model=BertForTokenClassification.from_pretrained(a.model_dir)
    model.eval()

    progress=Path(a.progress_state)
    total=128
    done=0
    update_state(progress,VERSION,"SINGLE",0,total,status="RUNNING",message="starting P1 parity32")

    singles={}
    for r in rows:
        tr=single_runner(model,tok,rewrite,r["source"].split())
        singles[r["uid"]]=tr
        done+=1
        update_state(progress,VERSION,"SINGLE",done,total,message=f'uid={r["uid"]}')

    def run_batch(order):
        br=batch_runner(model,tok,rewrite,order,32)
        return {r["uid"]:[p1,p2] for r,(p1,p2) in zip(order,br)}

    original=run_batch(rows)
    for r in rows:
        uid=r["uid"]
        if original[uid]!=singles[uid]:
            raise RuntimeError(f"P1_SINGLE_BATCH_MISMATCH:{uid}")
        if singles[uid][0]!=frozen[uid]["pass1_trace"]:
            raise RuntimeError(f"P1_SINGLE_FROZEN_PASS1_MISMATCH:{uid}")
        if singles[uid][1]!=frozen[uid]["pass2_trace"]:
            raise RuntimeError(f"P1_SINGLE_FROZEN_PASS2_MISMATCH:{uid}")
        if singles[uid][1]["output"]!=frozen[uid]["full_proposer_output"]:
            raise RuntimeError(f"P1_SINGLE_FROZEN_OUTPUT_MISMATCH:{uid}")
        done+=1
        update_state(progress,VERSION,"BATCH",done,total,message=f'uid={uid}')

    rev=run_batch(list(reversed(rows)))
    for r in rows:
        uid=r["uid"]
        if rev[uid]!=singles[uid]:
            raise RuntimeError(f"P1_REORDERED_BATCH_MISMATCH:{uid}")
        done+=1
        update_state(progress,VERSION,"REORDERED_BATCH",done,total,message=f'uid={uid}')

    rep=run_batch(rows)
    for r in rows:
        uid=r["uid"]
        if rep[uid]!=original[uid]:
            raise RuntimeError(f"P1_REPEAT_BATCH_MISMATCH:{uid}")
        done+=1
        update_state(progress,VERSION,"REPEAT_BATCH",done,total,message=f'uid={uid}')

    result={
        "record_id":VERSION,
        "status":"PASS",
        "n":32,
        "single_vs_batch_match":32,
        "single_vs_frozen_pass1_match":32,
        "single_vs_frozen_pass2_match":32,
        "single_vs_frozen_final_output_match":32,
        "reordered_batch_match":32,
        "repeat_batch_match":32,
        "model_revision":EXPECTED_MODEL_REV,
        "model_weight_sha256":weight_sha,
        "upstream_revision":EXPECTED_UPSTREAM_REV,
        "packet_sha256":EXPECTED_PACKET_SHA,
        "parity_manifest_sha256":EXPECTED_PARITY_SHA,
        "frozen_p1_proposal_sha256":EXPECTED_P1_SHA,
        "project_source_loaded":True,
        "project_gold_loaded":False,
        "quality_metric_computed":False,
        "proposal_artifact_modified":False,
    }
    Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    update_state(progress,VERSION,"COMPLETE",total,total,status="COMPLETE",message="P1 parity32 complete")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
