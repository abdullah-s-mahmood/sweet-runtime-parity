#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request

VERSION = "MPSEF_RJOINT_V4_2_CONSUMPTION_GUARD_V1"
EXPERIMENT_ID = "MPSEF-RJOINT-V4_2-CF1918-20261002-A"
CONSUMED_CONTEXT = "acad-pass/v4-2-rjoint-consumed"


def require_git_sha(value, name):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise RuntimeError(f"{name} must be exact 40-char lowercase git SHA")


def github_request(url, token, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return json.loads(raw.decode("utf-8")) if raw else {}


def consumed_status_present(statuses):
    return any(s.get("context") == CONSUMED_CONTEXT for s in statuses)


def claim_once(repo, code_commit_sha, token, target_url=None):
    require_git_sha(code_commit_sha, "code_commit_sha")
    statuses = github_request(
        f"https://api.github.com/repos/{repo}/commits/{code_commit_sha}/statuses?per_page=100",
        token,
    )
    if not isinstance(statuses, list):
        raise RuntimeError("UNEXPECTED_COMMIT_STATUS_RESPONSE")
    if consumed_status_present(statuses):
        raise RuntimeError("EXPERIMENT_ALREADY_CONSUMED")

    payload = {
        "state": "success",
        "context": CONSUMED_CONTEXT,
        "description": "Single V4.2 development run consumed before gold access",
    }
    if target_url:
        payload["target_url"] = target_url

    github_request(
        f"https://api.github.com/repos/{repo}/statuses/{code_commit_sha}",
        token,
        method="POST",
        payload=payload,
    )

    verify = github_request(
        f"https://api.github.com/repos/{repo}/commits/{code_commit_sha}/statuses?per_page=100",
        token,
    )
    if not consumed_status_present(verify):
        raise RuntimeError("CONSUMPTION_CLAIM_NOT_DURABLE")
    return True


def self_test():
    assert consumed_status_present([]) is False
    assert consumed_status_present([{"context": "other"}]) is False
    assert consumed_status_present([{"context": CONSUMED_CONTEXT, "state": "success"}]) is True
    assert consumed_status_present([{"context": CONSUMED_CONTEXT, "state": "failure"}]) is True
    print(json.dumps({
        "self_test": "PASS",
        "version": VERSION,
        "experiment_id": EXPERIMENT_ID,
        "context": CONSUMED_CONTEXT,
    }))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--claim", action="store_true")
    ap.add_argument("--repo")
    ap.add_argument("--code-commit-sha")
    ap.add_argument("--target-url")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return

    if args.claim:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("GITHUB_TOKEN_MISSING")
        if not args.repo or not args.code_commit_sha:
            raise SystemExit("REPO_OR_CODE_COMMIT_MISSING")
        claim_once(args.repo, args.code_commit_sha, token, args.target_url)
        print("V4_2_CONSUMPTION_CLAIMED")
        return

    raise SystemExit("choose --self-test or --claim")


if __name__ == "__main__":
    main()
