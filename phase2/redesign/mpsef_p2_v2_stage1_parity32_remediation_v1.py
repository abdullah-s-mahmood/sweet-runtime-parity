#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from mpsef_p2_v2_stage1_v1 import build_models, infer_one, parity_signature

VERSION = "MPSEF_P2_V2_STAGE1_PARITY32_REMEDIATION_V1"
EXPECTED_MANIFEST_SHA = "384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e"
EXPECTED_P2_PROPOSAL_SHA = "df89c7dc2c7f177b3c4ca02e8df8a291b6de917a81246c5258f1f66652e1f69e"
EXPECTED_N = 32


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def load_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--p2-proposals", required=True)
    ap.add_argument("--ged-model-dir", required=True)
    ap.add_argument("--gec-model-dir", required=True)
    ap.add_argument("--out", default="MPSEF_P2_V2_STAGE1_PARITY32_REMEDIATION_V1.json")
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    p2_path = Path(args.p2_proposals)

    if sha_bytes(manifest_path.read_bytes()) != EXPECTED_MANIFEST_SHA:
        raise RuntimeError("PARITY32_MANIFEST_SHA_MISMATCH")
    if sha_bytes(p2_path.read_bytes()) != EXPECTED_P2_PROPOSAL_SHA:
        raise RuntimeError("P2_STAGE1_PROPOSAL_SHA_MISMATCH")

    manifest = load_jsonl(manifest_path)
    p2_rows = load_jsonl(p2_path)
    if len(manifest) != EXPECTED_N:
        raise RuntimeError(f"PARITY32_COUNT_MISMATCH:{len(manifest)}")

    by_uid = {r["uid"]: r for r in p2_rows}
    if len(by_uid) != len(p2_rows):
        raise RuntimeError("P2_STAGE1_DUPLICATE_UID")

    selected = []
    for m in manifest:
        uid = m["uid"]
        if uid not in by_uid:
            raise RuntimeError(f"P2_STAGE1_UID_MISSING:{uid}")
        frozen = by_uid[uid]
        if frozen["source_sha256"] != m["source_sha256"]:
            raise RuntimeError(f"P2_SOURCE_SHA_FIELD_MISMATCH:{uid}")
        if sha_text(frozen["source"]) != m["source_sha256"]:
            raise RuntimeError(f"P2_SOURCE_TEXT_SHA_MISMATCH:{uid}")
        selected.append((m, frozen))

    models = build_models(args)

    fresh = {}
    for m, frozen in selected:
        row = {
            "uid": frozen["uid"],
            "case_id": frozen["case_id"],
            "cluster_id": frozen["cluster_id"],
            "source": frozen["source"],
            "source_sha256": frozen["source_sha256"],
        }
        fresh[m["uid"]] = infer_one(row, models, include_trace=True)

    repeat = {}
    for m, frozen in selected:
        row = {
            "uid": frozen["uid"],
            "case_id": frozen["case_id"],
            "cluster_id": frozen["cluster_id"],
            "source": frozen["source"],
            "source_sha256": frozen["source_sha256"],
        }
        repeat[m["uid"]] = infer_one(row, models, include_trace=True)

    reversed_run = {}
    for m, frozen in reversed(selected):
        row = {
            "uid": frozen["uid"],
            "case_id": frozen["case_id"],
            "cluster_id": frozen["cluster_id"],
            "source": frozen["source"],
            "source_sha256": frozen["source_sha256"],
        }
        reversed_run[m["uid"]] = infer_one(row, models, include_trace=True)

    counts = {
        "fresh_vs_repeat": 0,
        "fresh_vs_reordered": 0,
        "fresh_vs_frozen_trace_output": 0,
    }
    rows = []

    for m, frozen in selected:
        uid = m["uid"]
        sig_fresh = parity_signature(fresh[uid])
        sig_repeat = parity_signature(repeat[uid])
        sig_reverse = parity_signature(reversed_run[uid])
        sig_frozen = parity_signature(frozen)

        a = sig_fresh == sig_repeat
        b = sig_fresh == sig_reverse
        c = sig_fresh == sig_frozen

        counts["fresh_vs_repeat"] += int(a)
        counts["fresh_vs_reordered"] += int(b)
        counts["fresh_vs_frozen_trace_output"] += int(c)

        rows.append({
            "uid": uid,
            "rank_index": m["rank_index"],
            "source_sha256": m["source_sha256"],
            "frozen_execution_state": frozen.get("execution_state"),
            "fresh_execution_state": fresh[uid].get("execution_state"),
            "frozen_output_sha256": frozen.get("output_sha256"),
            "fresh_output_sha256": fresh[uid].get("output_sha256"),
            "fresh_vs_repeat": a,
            "fresh_vs_reordered": b,
            "fresh_vs_frozen_trace_output": c,
        })

    status = "PASS" if all(v == EXPECTED_N for v in counts.values()) else "FAIL"

    result = {
        "record_id": VERSION,
        "status": status,
        "n": EXPECTED_N,
        "manifest_sha256": EXPECTED_MANIFEST_SHA,
        "p2_stage1_proposal_sha256": EXPECTED_P2_PROPOSAL_SHA,
        "counts": counts,
        "true_model_batch_call_supported": False,
        "batch_vs_single_parity": "NOT_APPLICABLE_SINGLE_CASE_MODEL_CALL_IMPLEMENTATION",
        "rows": rows,
        "project_source_loaded": True,
        "project_source_scope": "FROZEN_STAGE1_PARITY32_ONLY",
        "project_gold_loaded": False,
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "proposal_artifact_modified": False,
    }

    Path(args.out).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "record_id": result["record_id"],
        "status": result["status"],
        "n": result["n"],
        "counts": result["counts"],
        "batch_vs_single_parity": result["batch_vs_single_parity"],
        "project_gold_loaded": result["project_gold_loaded"],
        "quality_metric_computed": result["quality_metric_computed"],
        "proposal_artifact_modified": result["proposal_artifact_modified"],
    }, ensure_ascii=False, indent=2))

    if status != "PASS":
        raise RuntimeError("P2_V2_STAGE1_PARITY32_REMEDIATION_FAILED")


if __name__ == "__main__":
    main()
