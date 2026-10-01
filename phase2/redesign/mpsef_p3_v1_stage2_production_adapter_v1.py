#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import statistics
import tempfile
import time
from pathlib import Path

from transformers import BertForTokenClassification, BertTokenizer

from mpsef_p1_cf_proposals_v1 import install_rewrite_compat
from mpsef_p3_v1_stage1_v1 import batch_pnx
from mpsef_stageb_change_domain_classifier_v1 import (
    VERSION as CLASSIFIER_VERSION,
    classify_stageb_change,
)
from process_progress_v1 import update_state


VERSION = "MPSEF_P3_V1_STAGE2_PRODUCTION_ADAPTER_V1"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"
PROPOSER_ID = "P3_V1_SWEET_NOPNX2_PNX1"
PROPOSER_VERSION = "P3_V1_1"
FAMILY_ID = "SWEET_QALB14"
ANCESTRY_ID = "P1_CONTROL_PLUS_PNX1"
PARENT_PROPOSER_ID = "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2"
PARENT_PROPOSER_VERSION = "P1_FROZEN_V1"

EXPECTED_P1_PROPOSAL_SHA256 = (
    "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
)
EXPECTED_PNX_WEIGHT_SHA256 = (
    "d98d683f9ef1738c27f5031c99483d93e9f73c4116c158a97a678270c84fd262"
)
EXPECTED_PNX_CONFIG_SHA256 = (
    "2b65052e89f8a44585e3618febf7b65593db109e475f7569ac5d4a96799350f0"
)

_TERMINATION_REQUESTED = False


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def append_jsonl_durable(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def load_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def _signal_handler(signum, frame):
    global _TERMINATION_REQUESTED
    _TERMINATION_REQUESTED = True


def install_signal_handlers():
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)


def validate_inputs(input_rows, p1_rows):
    if len({r["uid"] for r in input_rows}) != len(input_rows):
        raise RuntimeError("P3_STAGE2_DUPLICATE_INPUT_UID")
    by_p1 = {r["uid"]: r for r in p1_rows}
    if len(by_p1) != len(p1_rows):
        raise RuntimeError("P3_STAGE2_DUPLICATE_P1_UID")

    selected = []
    for row in input_rows:
        uid = row["uid"]
        if sha_text(row["source"]) != row["source_sha256"]:
            raise RuntimeError(f"P3_STAGE2_SOURCE_SHA_INVALID:{uid}")
        if uid not in by_p1:
            raise RuntimeError(f"P3_STAGE2_P1_PARENT_UID_MISSING:{uid}")

        parent = by_p1[uid]
        parent_source_sha = parent.get("source_version_hash")
        if parent_source_sha != row["source_sha256"]:
            raise RuntimeError(
                f"P3_STAGE2_P1_PARENT_SOURCE_SHA_MISMATCH:{uid}"
            )
        parent_output = parent.get("full_proposer_output")
        parent_sha = parent.get("output_sha256")
        if not isinstance(parent_output, str):
            raise RuntimeError(f"P3_STAGE2_P1_PARENT_OUTPUT_MISSING:{uid}")
        if sha_text(parent_output) != parent_sha:
            raise RuntimeError(f"P3_STAGE2_P1_PARENT_OUTPUT_SHA_INVALID:{uid}")

        selected.append((row, parent))
    return selected


def build_runtime(args):
    model_dir = Path(args.pnx_model_dir)
    weight_sha = sha_file(model_dir / "pytorch_model.bin")
    if weight_sha != EXPECTED_PNX_WEIGHT_SHA256:
        raise RuntimeError(f"P3_STAGE2_PNX_WEIGHT_SHA_MISMATCH:{weight_sha}")

    rewrite = install_rewrite_compat(Path(args.upstream_root))
    tokenizer = BertTokenizer.from_pretrained(model_dir)
    model = BertForTokenClassification.from_pretrained(model_dir)
    model.eval()

    cfg_sha = hashlib.sha256(
        model.config.to_json_string().encode()
    ).hexdigest()
    if cfg_sha != EXPECTED_PNX_CONFIG_SHA256:
        raise RuntimeError(f"P3_STAGE2_PNX_CONFIG_SHA_MISMATCH:{cfg_sha}")

    identities = {
        "pnx_weight_sha256": weight_sha,
        "pnx_config_sha256": cfg_sha,
        "tokenizer_class": type(tokenizer).__name__,
        "vocab_size": len(tokenizer),
        "max_position_embeddings": getattr(
            model.config, "max_position_embeddings", None
        ),
        "classifier_version": CLASSIFIER_VERSION,
    }
    return model, tokenizer, rewrite, identities


def make_record(row, parent):
    parent_output = parent["full_proposer_output"]
    parent_sha = parent["output_sha256"]
    return {
        "record_id": "MPSEF_P3_V1_STAGE2_PROPOSAL_V1",
        "adapter_version": VERSION,
        "registry_namespace": REGISTRY_NAMESPACE,
        "proposer_id": PROPOSER_ID,
        "proposer_version": PROPOSER_VERSION,
        "family_id": FAMILY_ID,
        "ancestry_id": ANCESTRY_ID,
        "role": "OPTIONAL_PUNCTUATION_FULLCORRECTION_EXTENSION",
        "uid": row["uid"],
        "case_id": row["case_id"],
        "cluster_id": row["cluster_id"],
        "source": row["source"],
        "source_sha256": row["source_sha256"],
        "parent_proposer_id": PARENT_PROPOSER_ID,
        "parent_proposer_version": PARENT_PROPOSER_VERSION,
        "parent_output": parent_output,
        "parent_output_sha256": parent_sha,
        "input_text": parent_output,
        "input_sha256": parent_sha,
        "full_proposer_output": None,
        "output_sha256": None,
        "execution_state": "UNKNOWN_FAILURE",
        "failure_reasons": [],
        "stage_b_domain_from_p1": "UNAVAILABLE_COMPARISON",
        "stage_b_classifier_version": CLASSIFIER_VERSION,
        "pnx_trace": None,
        "runtime_measurement_type": "ALLOCATED_BATCH_TIME",
        "runtime_seconds": None,
        "source_only": True,
        "gold_reference_consulted": False,
        "quality_scored": False,
        "provenance_complete": True,
    }


def run(args):
    global _TERMINATION_REQUESTED
    _TERMINATION_REQUESTED = False
    install_signal_handlers()

    input_path = Path(args.input_jsonl)
    p1_path = Path(args.p1_proposals)
    out_path = Path(args.out_jsonl)
    run_state_path = Path(args.run_state)
    progress_path = Path(args.progress_state)

    if out_path.exists() and out_path.stat().st_size > 0:
        raise RuntimeError(
            "P3_STAGE2_SILENT_RESUME_FORBIDDEN:" + str(out_path)
        )

    if args.expected_input_sha256:
        got = sha_file(input_path)
        if got != args.expected_input_sha256:
            raise RuntimeError(f"P3_STAGE2_INPUT_SHA_MISMATCH:{got}")

    if sha_file(p1_path) != EXPECTED_P1_PROPOSAL_SHA256:
        raise RuntimeError("P3_STAGE2_FROZEN_P1_ARTIFACT_SHA_MISMATCH")

    input_rows = load_jsonl(input_path)
    p1_rows = load_jsonl(p1_path)
    if len(input_rows) != args.expected_count:
        raise RuntimeError(
            f"P3_STAGE2_INPUT_COUNT_MISMATCH:{len(input_rows)}"
        )

    selected = validate_inputs(input_rows, p1_rows)
    model, tokenizer, rewrite, identities = build_runtime(args)

    atomic_write_json(
        run_state_path,
        {
            "schema": "MPSEF_P3_V1_STAGE2_RUN_STATE_V1",
            "status": "RUNNING",
            "adapter_version": VERSION,
            "input_sha256": sha_file(input_path),
            "p1_parent_artifact_sha256": sha_file(p1_path),
            "expected_count": args.expected_count,
            "durable_completed_count": 0,
            "current_uids": [],
            "termination_requested": False,
            "runtime_identities": identities,
        },
    )
    update_state(
        progress_path,
        process_id=VERSION,
        stage="INITIALIZE",
        processed=0,
        total=len(selected),
        status="RUNNING",
        message="P3 production adapter initialized",
    )

    runtimes = []
    durable_count = 0
    for start in range(0, len(selected), args.batch_size):
        if _TERMINATION_REQUESTED:
            st = json.loads(run_state_path.read_text(encoding="utf-8"))
            atomic_write_json(
                run_state_path,
                {
                    **st,
                    "status": "INTERRUPTED_BEFORE_NEXT_BATCH",
                    "termination_requested": True,
                    "current_uids": [],
                },
            )
            raise SystemExit(143)

        batch = selected[start:start + args.batch_size]
        current_uids = [row["uid"] for row, _ in batch]
        st = json.loads(run_state_path.read_text(encoding="utf-8"))
        atomic_write_json(
            run_state_path,
            {
                **st,
                "status": "RUNNING_BATCH",
                "current_uids": current_uids,
                "termination_requested": False,
            },
        )

        parent_texts = [p["full_proposer_output"] for _, p in batch]
        t0 = time.monotonic()
        try:
            steps = batch_pnx(
                model, tokenizer, rewrite, parent_texts
            )
            if len(steps) != len(batch):
                raise RuntimeError("P3_STAGE2_BATCH_OUTPUT_COUNT_MISMATCH")
            batch_error = None
        except Exception as exc:
            steps = [None] * len(batch)
            batch_error = f"{type(exc).__name__}:{exc}"

        batch_elapsed = time.monotonic() - t0
        allocated = batch_elapsed / max(1, len(batch))

        for (row, parent), step in zip(batch, steps):
            rec = make_record(row, parent)
            rec["runtime_seconds"] = allocated
            runtimes.append(allocated)

            if batch_error is not None:
                rec["execution_state"] = "EXECUTION_FAILED"
                rec["failure_reasons"] = [batch_error]
                rec["stage_b_domain_from_p1"] = (
                    "UNAVAILABLE_COMPARISON"
                )
            else:
                final = step["output"]
                rec["pnx_trace"] = step
                rec["full_proposer_output"] = final
                rec["output_sha256"] = sha_text(final)
                if final == "":
                    rec["execution_state"] = "EMPTY_OUTPUT"
                    rec["failure_reasons"] = ["P3_EMPTY_OUTPUT"]
                else:
                    rec["execution_state"] = "OK"
                rec["stage_b_domain_from_p1"] = (
                    classify_stageb_change(
                        parent["full_proposer_output"],
                        final,
                    )
                )

            append_jsonl_durable(out_path, rec)
            durable_count += 1

        st = json.loads(run_state_path.read_text(encoding="utf-8"))
        atomic_write_json(
            run_state_path,
            {
                **st,
                "status": "RUNNING",
                "current_uids": [],
                "durable_completed_count": durable_count,
                "last_completed_uid": batch[-1][0]["uid"],
                "termination_requested": _TERMINATION_REQUESTED,
            },
        )
        update_state(
            progress_path,
            process_id=VERSION,
            stage="PRODUCTION_PNX",
            processed=durable_count,
            total=len(selected),
            status="RUNNING",
            message=(
                f"batch_end_uid={batch[-1][0]['uid']} "
                f"durable={durable_count}"
            ),
        )

        if _TERMINATION_REQUESTED:
            st = json.loads(run_state_path.read_text(encoding="utf-8"))
            atomic_write_json(
                run_state_path,
                {
                    **st,
                    "status": "INTERRUPTED_AFTER_DURABLE_BATCH",
                    "termination_requested": True,
                },
            )
            raise SystemExit(143)

    out_rows = load_jsonl(out_path)
    if len(out_rows) != args.expected_count:
        raise RuntimeError(
            f"P3_STAGE2_TERMINAL_RECORD_COUNT_MISMATCH:{len(out_rows)}"
        )
    if len({r["uid"] for r in out_rows}) != args.expected_count:
        raise RuntimeError("P3_STAGE2_TERMINAL_UID_UNIQUENESS_FAILED")
    if {r["uid"] for r in out_rows} != {
        r["uid"] for r in input_rows
    }:
        raise RuntimeError("P3_STAGE2_TERMINAL_UID_SET_MISMATCH")

    st = json.loads(run_state_path.read_text(encoding="utf-8"))
    atomic_write_json(
        run_state_path,
        {
            **st,
            "status": "COMPLETE",
            "current_uids": [],
            "durable_completed_count": args.expected_count,
            "aborted_count": 0,
            "not_attempted_count": 0,
            "output_sha256": sha_file(out_path),
        },
    )
    update_state(
        progress_path,
        process_id=VERSION,
        stage="COMPLETE",
        processed=args.expected_count,
        total=args.expected_count,
        status="COMPLETE",
        message="all P3 terminal records durable and validated",
    )

    state_counts = {}
    domain_counts = {}
    for rec in out_rows:
        state_counts[rec["execution_state"]] = (
            state_counts.get(rec["execution_state"], 0) + 1
        )
        d = rec["stage_b_domain_from_p1"]
        domain_counts[d] = domain_counts.get(d, 0) + 1

    ordered = sorted(runtimes)
    rank95 = max(1, (95 * len(ordered) + 99) // 100)
    summary = {
        "record_id": VERSION,
        "status": "COMPLETE",
        "cases": len(out_rows),
        "clusters": len({r["cluster_id"] for r in out_rows}),
        "input_sha256": sha_file(input_path),
        "p1_parent_artifact_sha256": sha_file(p1_path),
        "output_sha256": sha_file(out_path),
        "state_counts": state_counts,
        "stage_b_classifier_version": CLASSIFIER_VERSION,
        "stage_b_domain_counts": domain_counts,
        "batch_size": args.batch_size,
        "runtime_measurement_type": "ALLOCATED_BATCH_TIME",
        "runtime_seconds_mean_allocated": statistics.mean(runtimes),
        "runtime_seconds_median_allocated": statistics.median(runtimes),
        "runtime_seconds_p95_nearest_rank_allocated": ordered[rank95 - 1],
        "runtime_identities": identities,
        "p1_rerun": False,
        "exact_frozen_p1_parent_reused": True,
        "gold_reference_consulted": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
    }
    if args.summary:
        atomic_write_json(Path(args.summary), summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-jsonl", required=True)
    ap.add_argument("--expected-count", type=int, required=True)
    ap.add_argument("--expected-input-sha256")
    ap.add_argument("--p1-proposals", required=True)
    ap.add_argument("--pnx-model-dir", required=True)
    ap.add_argument("--upstream-root", required=True)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--out-jsonl", required=True)
    ap.add_argument("--run-state", required=True)
    ap.add_argument("--progress-state", required=True)
    ap.add_argument("--summary")
    args = ap.parse_args()
    run(args)


if __name__ == "__main__":
    main()
