#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,os
from pathlib import Path

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-lock",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    lock=json.load(open(args.input_lock,encoding="utf-8"))
    assert lock["status"]=="PASS"
    assert lock["population"]["cases"]==1918 and lock["population"]["clusters"]==764
    assert lock["full_cf_execution_authorized_by_this_record"] is True
    for p,expected in lock["authoritative_file_sha256"].items():
        assert sha(p)==expected,(p,sha(p),expected)
    wf=".github/workflows/phase2-mpsef-p2-v2-stage2-full-cf-production.yml"
    acct="phase2/redesign/mpsef_stage2_partial_accounting_v1.py"
    payload={
      "record_id":"MPSEF_P2_V2_STAGE2_FULL_CF_EXECUTION_IDENTITY_GATE_V1",
      "status":"PASS",
      "git_commit":os.environ.get("GITHUB_SHA"),
      "workflow_path":wf,
      "workflow_sha256":sha(wf),
      "partial_accounting_sha256":sha(acct),
      "adapter_sha256":sha("phase2/redesign/mpsef_p2_v2_stage2_production_adapter_v1.py"),
      "watchdog_sha256":sha("phase2/redesign/run_with_progress_watchdog_v2.py"),
      "input_lock_run_id":36898163047,
      "input_lock_artifact_id":11180920946,
      "input_lock_artifact_digest":"sha256:239395994cdf22bc7c6353de19601caab650dba7e24eedac91795ff453d87b2a",
      "p2_runtime_freeze_sha256":lock["p2"]["runtime_freeze_sha256"],
      "cf_manifest_sha256":lock["population"]["manifest_sha256"],
      "p1_proposal_sha256":lock["frozen_p1"]["proposal_sha256"],
      "gold_reference_allowed":False,
      "quality_metric_allowed":False,
      "r_joint_allowed":False,
    }
    Path(args.out).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(payload,indent=2))

if __name__=="__main__": main()
