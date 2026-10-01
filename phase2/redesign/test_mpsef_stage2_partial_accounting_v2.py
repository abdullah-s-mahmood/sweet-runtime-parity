#!/usr/bin/env python3
from __future__ import annotations

import json
from mpsef_stage2_partial_accounting_v2 import classify


def rows(*uids):
    return [{"uid": u} for u in uids]


def check(name, payload, expected, results):
    for k, v in expected.items():
        if payload[k] != v:
            raise AssertionError(
                f"{name}:{k}: expected={v!r} got={payload[k]!r}"
            )
    results[name] = "PASS"


def main():
    r = {}

    check(
        "P2_SINGLE_UID_INTERRUPTED",
        classify(
            rows("A", "B", "C"),
            rows("A"),
            [],
            {"status": "RUNNING_UID", "current_uid": "B"},
        ),
        {
            "completed_count": 1,
            "aborted_count": 1,
            "aborted_uids": ["B"],
            "not_attempted_count": 1,
            "not_attempted_uids": ["C"],
            "completion_claim_allowed": False,
        },
        r,
    )

    check(
        "P3_BATCH_INTERRUPTED",
        classify(
            rows("A", "B", "C", "D"),
            rows("A"),
            [],
            {
                "status": "RUNNING_BATCH",
                "current_uids": ["B", "C"],
            },
        ),
        {
            "completed_count": 1,
            "aborted_count": 2,
            "aborted_uids": ["B", "C"],
            "not_attempted_count": 1,
            "not_attempted_uids": ["D"],
            "completion_claim_allowed": False,
        },
        r,
    )

    check(
        "P3_DURABLE_BATCH_AFTER_SIGNAL",
        classify(
            rows("A", "B", "C"),
            rows("A", "B"),
            [],
            {
                "status": "INTERRUPTED_AFTER_DURABLE_BATCH",
                "current_uids": ["A", "B"],
            },
        ),
        {
            "completed_count": 2,
            "aborted_count": 0,
            "not_attempted_count": 1,
            "not_attempted_uids": ["C"],
            "completion_claim_allowed": False,
        },
        r,
    )

    check(
        "COMPLETE",
        classify(
            rows("A", "B"),
            rows("A", "B"),
            [],
            {"status": "COMPLETE", "current_uids": []},
        ),
        {
            "completed_count": 2,
            "aborted_count": 0,
            "not_attempted_count": 0,
            "completion_claim_allowed": True,
        },
        r,
    )

    x = classify(
        rows("A", "B"),
        [{"uid": "A"}, {"uid": "A"}],
        [],
        {"status": "RUNNING"},
    )
    assert x["duplicate_output_uids"] == ["A"]
    assert x["completion_claim_allowed"] is False
    r["DUPLICATE_FAIL_CLOSED"] = "PASS"

    x = classify(
        rows("A", "B"),
        [{"uid": "X"}],
        [],
        {"status": "RUNNING", "current_uids": ["B"]},
    )
    assert "X" in x["foreign_output_uids"]
    assert x["aborted_uids"] == ["B"]
    assert x["completion_claim_allowed"] is False
    r["FOREIGN_FAIL_CLOSED"] = "PASS"

    print(json.dumps({
        "record_id": "MPSEF_STAGE2_PARTIAL_ACCOUNTING_V2_SYNTHETIC_TEST",
        "status": "PASS",
        "test_count": len(r),
        "tests": r,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
