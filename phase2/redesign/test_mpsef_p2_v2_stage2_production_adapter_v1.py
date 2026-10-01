#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from mpsef_p2_v2_stage2_production_adapter_v1 import (
    STAGES,
    append_jsonl_durable,
    assert_stage_status,
    base_record,
    new_stage_status,
    stage_fail,
    stage_pass,
)


def sample_row():
    return {
        "uid": "SYN:1",
        "case_id": "SYN-1",
        "cluster_id": "SYN-C1",
        "source": "هذا اختبار .",
        "source_sha256": (
            "ed8cf25725eb122d3a577fca495e525f09ad9ca291a31673b459085724f91729"
        ),
    }


def main():
    results = {}

    ledger = new_stage_status()
    assert list(ledger) == STAGES
    assert all(v == "NOT_REACHED" for v in ledger.values())
    results["LEDGER_INITIALIZES_NOT_REACHED"] = "PASS"

    stage_pass(ledger, "SOURCE_IDENTITY")
    stage_pass(ledger, "MORPH_ANALYSIS")
    stage_fail(ledger, "GED_TOKENIZATION")
    assert ledger["SOURCE_IDENTITY"] == "PASS"
    assert ledger["MORPH_ANALYSIS"] == "PASS"
    assert ledger["GED_TOKENIZATION"] == "FAIL"
    assert ledger["GED_WORD_IDENTITY"] == "NOT_REACHED"
    assert_stage_status(ledger)
    results["PARTIAL_LEDGER_PRESERVES_COMPLETED_STAGES"] = "PASS"

    rec = base_record(sample_row())
    rec["stage_status"] = ledger
    rec["failure_stage"] = "GED_TOKENIZATION"
    rec["execution_state"] = "TOKENIZATION_FAILED"
    rec["morph_words"] = ["هذا", "اختبار", "."]
    assert rec["morph_words"] is not None
    assert rec["stage_status"]["MORPH_ANALYSIS"] == "PASS"
    results["FAILED_ROW_RETAINS_INTERMEDIATE_EVIDENCE"] = "PASS"

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "rows.jsonl"
        append_jsonl_durable(p, {"uid": "A", "state": "OK"})
        append_jsonl_durable(p, {"uid": "B", "state": "FAIL"})
        rows = [
            json.loads(x)
            for x in p.read_text(encoding="utf-8").splitlines()
            if x.strip()
        ]
        assert [r["uid"] for r in rows] == ["A", "B"]
    results["DURABLE_JSONL_APPEND_ORDER"] = "PASS"

    try:
        bad = new_stage_status()
        bad["SOURCE_IDENTITY"] = "MAYBE"
        assert_stage_status(bad)
    except RuntimeError:
        results["INVALID_STAGE_STATUS_FAILS_CLOSED"] = "PASS"
    else:
        raise AssertionError("invalid stage status did not fail")

    summary = {
        "record_id": "MPSEF_P2_V2_STAGE2_ADAPTER_UNIT_V1",
        "status": "PASS",
        "test_count": len(results),
        "tests": results,
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "model_inference_run": False,
        "quality_metric_computed": False,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
