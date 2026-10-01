#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import urllib.request
from pathlib import Path

VERSION = "MPSEF_MEASUREMENT_GUARD_V2"
EXPERIMENT_ID = "MPSEF-RJOINT-V2-CF1918-20261001-A"
CONSUMED_CONTEXT = "acad-pass/mpsef-rjoint-v2-consumed"

EXPECTED = {
    "source_manifest_sha256": "051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193",
    "p1_proposal_sha256": "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d",
    "p2_proposal_sha256": "f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b",
    "executable_actions_sha256": "6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a",
    "hypotheses_sha256": "b4736383019d017780a8bfe4b076a0cd742e71bccfbb50350da8fa59b7c9ac75",
    "diagnostic_components_sha256": "2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e",
    "gold_m2_sha256": "971b6fbb28dc3767193e7a4b0f722c3abebfc8600155a57093ba483dac6491e8",
    "core_v2_sha256": "2f86146e5485cf79da5a3db44b9f8c86ee2b7ea60bac5859ff9a079fe66d3588",
    "scorer_v2_sha256": "5fdcf0653cd0fafd3195444b926c19d8ab0fdef18dea8c728af1ca171821e2da",
}

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def require_hex_sha(value, name):
    if not isinstance(value,str) or not re.fullmatch(r"[0-9a-f]{40}",value):
        raise RuntimeError(f"{name} must be exact 40-char lowercase git SHA")

def validate_experiment(exp):
    if exp.get("record_id")!="MPSEF_RJOINT_EXPERIMENT_ID_V2":
        raise RuntimeError("experiment record_id mismatch")
    if exp.get("experiment_id")!=EXPERIMENT_ID:
        raise RuntimeError("experiment_id mismatch")
    if exp.get("status")!="IDENTITY_FROZEN_NOT_AUTHORIZED":
        raise RuntimeError("experiment identity file status changed unexpectedly")
    pop=exp.get("population",{})
    if pop.get("role")!="C_F" or pop.get("cases")!=1918 or pop.get("clusters")!=764:
        raise RuntimeError("experiment population mismatch")
    if pop.get("source_manifest_sha256")!=EXPECTED["source_manifest_sha256"]:
        raise RuntimeError("experiment source SHA mismatch")
    if exp.get("primary_gate",{}).get("threshold")!=0.95:
        raise RuntimeError("experiment threshold changed")
    cp=exp.get("consumption_policy",{})
    if cp.get("status_context")!=CONSUMED_CONTEXT:
        raise RuntimeError("consumption context mismatch")
    if cp.get("claim_before_gold_access") is not True:
        raise RuntimeError("claim-before-gold must be true")
    if exp.get("authorization",{}).get("measurement_authorized") is not False:
        raise RuntimeError("experiment identity file must not authorize measurement")
    return True

def validate_authorization(auth, exp, preflight):
    validate_experiment(exp)
    if auth.get("record_id")!="MPSEF_RJOINT_MEASUREMENT_AUTHORIZATION_V2":
        raise RuntimeError("authorization record_id mismatch")
    if auth.get("decision")!="AUTHORIZE_SINGLE_CORRECTED_C_F_MEASUREMENT":
        raise RuntimeError("authorization decision mismatch")
    if auth.get("experiment_id")!=EXPERIMENT_ID:
        raise RuntimeError("authorization experiment mismatch")
    if auth.get("measurement_version")!="MPSEF_RJOINT_MEASUREMENT_V2":
        raise RuntimeError("measurement version mismatch")
    if auth.get("single_run_only") is not True:
        raise RuntimeError("single_run_only must be true")
    require_hex_sha(auth.get("code_commit_sha"),"code_commit_sha")

    sp=auth.get("second_preflight",{})
    if sp.get("status")!="PASS":
        raise RuntimeError("second preflight is not PASS")
    if sp.get("run_id") != preflight.get("run_id"):
        raise RuntimeError("second preflight run mismatch")
    if sp.get("artifact_id") != preflight.get("artifact_id"):
        raise RuntimeError("second preflight artifact mismatch")
    if sp.get("summary_sha256") != preflight.get("summary_sha256"):
        raise RuntimeError("second preflight summary hash mismatch")
    if sp.get("code_commit_sha") != auth.get("code_commit_sha"):
        raise RuntimeError("preflight/code commit mismatch")
    if preflight.get("status")!="PASS":
        raise RuntimeError("preflight summary status mismatch")
    if preflight.get("measurement_authorized_by_preflight") is not False:
        raise RuntimeError("preflight must not authorize measurement")
    if preflight.get("project_gold_loaded") is not False:
        raise RuntimeError("second preflight loaded project gold")
    if preflight.get("project_metric_computed") is not False:
        raise RuntimeError("second preflight computed metric")

    fi=auth.get("frozen_inputs",{})
    for key,val in EXPECTED.items():
        if fi.get(key)!=val:
            raise RuntimeError(f"authorization frozen input mismatch: {key}")

    if auth.get("claim_scope") != (
        "DEVELOPMENT_FEASIBILITY / ADAPTIVELY_CONSUMED QALB-2014 ORIGIN / "
        "NOT_INDEPENDENT_GENERALIZATION_EVIDENCE"
    ):
        raise RuntimeError("claim scope mismatch")

    if auth.get("selector_authorized") is not False:
        raise RuntimeError("selector authorization forbidden")
    if auth.get("auto_safe_authorized") is not False:
        raise RuntimeError("AUTO_SAFE authorization forbidden")
    if auth.get("reserved_sets_authorized") is not False:
        raise RuntimeError("reserved-set authorization forbidden")
    return True

def consumed_status_present(statuses):
    for s in statuses:
        if s.get("context")==CONSUMED_CONTEXT:
            return True
    return False

def github_request(url, token, method="GET", payload=None):
    data=None if payload is None else json.dumps(payload).encode("utf-8")
    req=urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization":f"Bearer {token}",
            "Accept":"application/vnd.github+json",
            "X-GitHub-Api-Version":"2022-11-28",
            "Content-Type":"application/json",
        },
    )
    with urllib.request.urlopen(req,timeout=30) as r:
        raw=r.read()
    return json.loads(raw.decode("utf-8")) if raw else {}

def claim_experiment(repo, code_commit_sha, token, target_url=None):
    require_hex_sha(code_commit_sha,"code_commit_sha")
    statuses=github_request(
        f"https://api.github.com/repos/{repo}/commits/{code_commit_sha}/statuses?per_page=100",
        token,
    )
    if not isinstance(statuses,list):
        raise RuntimeError("unexpected commit-status response")
    if consumed_status_present(statuses):
        raise RuntimeError("EXPERIMENT_ALREADY_CONSUMED")

    payload={
        "state":"success",
        "context":CONSUMED_CONTEXT,
        "description":"CONSUMED before gold access; no sequential rerun allowed",
    }
    if target_url:
        payload["target_url"]=target_url
    github_request(
        f"https://api.github.com/repos/{repo}/statuses/{code_commit_sha}",
        token,
        method="POST",
        payload=payload,
    )

    verify=github_request(
        f"https://api.github.com/repos/{repo}/commits/{code_commit_sha}/statuses?per_page=100",
        token,
    )
    if not consumed_status_present(verify):
        raise RuntimeError("CONSUMPTION_CLAIM_NOT_DURABLE")
    return True

def self_test():
    exp={
        "record_id":"MPSEF_RJOINT_EXPERIMENT_ID_V2",
        "experiment_id":EXPERIMENT_ID,
        "status":"IDENTITY_FROZEN_NOT_AUTHORIZED",
        "population":{"role":"C_F","cases":1918,"clusters":764,"source_manifest_sha256":EXPECTED["source_manifest_sha256"]},
        "primary_gate":{"threshold":0.95},
        "consumption_policy":{"status_context":CONSUMED_CONTEXT,"claim_before_gold_access":True},
        "authorization":{"measurement_authorized":False},
    }
    pre={
        "status":"PASS","run_id":123,"artifact_id":456,
        "summary_sha256":"a"*64,
        "project_gold_loaded":False,"project_metric_computed":False,
        "measurement_authorized_by_preflight":False,
    }
    auth={
        "record_id":"MPSEF_RJOINT_MEASUREMENT_AUTHORIZATION_V2",
        "decision":"AUTHORIZE_SINGLE_CORRECTED_C_F_MEASUREMENT",
        "experiment_id":EXPERIMENT_ID,
        "measurement_version":"MPSEF_RJOINT_MEASUREMENT_V2",
        "single_run_only":True,
        "code_commit_sha":"b"*40,
        "second_preflight":{
            "status":"PASS","run_id":123,"artifact_id":456,
            "summary_sha256":"a"*64,"code_commit_sha":"b"*40,
        },
        "frozen_inputs":dict(EXPECTED),
        "claim_scope":"DEVELOPMENT_FEASIBILITY / ADAPTIVELY_CONSUMED QALB-2014 ORIGIN / NOT_INDEPENDENT_GENERALIZATION_EVIDENCE",
        "selector_authorized":False,"auto_safe_authorized":False,"reserved_sets_authorized":False,
    }
    pre["code_commit_sha"]="b"*40
    assert validate_authorization(auth,exp,pre)
    assert consumed_status_present([]) is False
    assert consumed_status_present([{"context":"other"}]) is False
    assert consumed_status_present([{"context":CONSUMED_CONTEXT,"state":"success"}]) is True
    # Any historical status with the context counts as consumed, regardless of latest state.
    assert consumed_status_present([
        {"context":CONSUMED_CONTEXT,"state":"failure"},
        {"context":"other","state":"success"},
    ]) is True

    bad=json.loads(json.dumps(auth))
    bad["frozen_inputs"]["executable_actions_sha256"]="0"*64
    try:
        validate_authorization(bad,exp,pre)
    except RuntimeError:
        pass
    else:
        raise AssertionError("bad action hash was accepted")

    print(json.dumps({
        "self_test":"PASS",
        "guard_version":VERSION,
        "experiment_id":EXPERIMENT_ID,
        "consumed_context":CONSUMED_CONTEXT,
    },ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--validate",action="store_true")
    ap.add_argument("--claim",action="store_true")
    ap.add_argument("--experiment-file")
    ap.add_argument("--authorization-file")
    ap.add_argument("--preflight-file")
    ap.add_argument("--repo")
    ap.add_argument("--code-commit-sha")
    ap.add_argument("--target-url")
    args=ap.parse_args()

    if args.self_test:
        self_test()
        return

    if args.validate:
        if not all([args.experiment_file,args.authorization_file,args.preflight_file]):
            raise SystemExit("missing validation input")
        validate_authorization(
            load_json(args.authorization_file),
            load_json(args.experiment_file),
            load_json(args.preflight_file),
        )
        print("MPSEF_MEASUREMENT_GUARD_V2_AUTHORIZATION_OK")
        return

    if args.claim:
        token=os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("GITHUB_TOKEN missing")
        if not args.repo or not args.code_commit_sha:
            raise SystemExit("repo/code commit missing")
        claim_experiment(args.repo,args.code_commit_sha,token,args.target_url)
        print("MPSEF_MEASUREMENT_GUARD_V2_CONSUMPTION_CLAIMED")
        return

    raise SystemExit("choose --self-test, --validate, or --claim")

if __name__=="__main__":
    main()
