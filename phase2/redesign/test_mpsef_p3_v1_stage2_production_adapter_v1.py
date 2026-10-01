#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from mpsef_p3_v1_stage2_production_adapter_v1 import (
    EXPECTED_P1_PROPOSAL_SHA256,
    append_jsonl_durable,
    make_record,
    validate_inputs,
)


def sha_text(s):
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def main():
    results = {}

    source = "هذا نص"
    parent_out = "هذا نص."
    row = {
        "uid": "SYN:1",
        "case_id": "S1",
        "cluster_id": "C1",
        "source": source,
        "source_sha256": sha_text(source),
    }
    p1 = {
        "uid": "SYN:1",
        "source_version_hash": sha_text(source),
        "full_proposer_output": parent_out,
        "output_sha256": sha_text(parent_out),
    }

    selected = validate_inputs([row], [p1])
    assert len(selected) == 1
    results["EXACT_PARENT_IDENTITY_PASS"] = "PASS"

    rec = make_record(row, p1)
    assert rec["input_text"] == parent_out
    assert rec["input_sha256"] == p1["output_sha256"]
    assert rec["parent_output_sha256"] == p1["output_sha256"]
    results["P3_INPUT_BOUND_TO_P1_OUTPUT"] = "PASS"

    bad = dict(p1)
    bad["output_sha256"] = "0" * 64
    try:
        validate_inputs([row], [bad])
    except RuntimeError:
        results["PARENT_OUTPUT_SHA_FAILS_CLOSED"] = "PASS"
    else:
        raise AssertionError("bad parent sha accepted")

    try:
        validate_inputs([row], [])
    except RuntimeError:
        results["MISSING_PARENT_FAILS_CLOSED"] = "PASS"
    else:
        raise AssertionError("missing parent accepted")

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "rows.jsonl"
        append_jsonl_durable(p, {"uid": "A"})
        append_jsonl_durable(p, {"uid": "B"})
        got = [
            json.loads(x)["uid"]
            for x in p.read_text(encoding="utf-8").splitlines()
            if x.strip()
        ]
        assert got == ["A", "B"]
    results["DURABLE_APPEND_ORDER"] = "PASS"

    summary = {
        "record_id": "MPSEF_P3_V1_STAGE2_PRODUCTION_ADAPTER_UNIT_V1",
        "status": "PASS",
        "test_count": len(results),
        "tests": results,
        "expected_p1_artifact_sha256": EXPECTED_P1_PROPOSAL_SHA256,
        "p1_rerun": False,
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
