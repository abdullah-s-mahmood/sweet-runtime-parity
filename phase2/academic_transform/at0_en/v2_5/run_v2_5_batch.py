#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
from typing import Iterable

HERE = pathlib.Path(__file__).resolve().parent
AT0 = HERE.parent
V24 = AT0 / "v2_4"
V25 = AT0 / "v2_5"

EXTRACTOR_PATH = V24 / "gate_b2" / "b2_2_relation_aware_extractor.py"
ALIGNER_PATH = V25 / "gate_b1" / "b1_aligner.py"

RUNTIME_ID = "AT0-EN V2.5"
DEFAULT_RECORD_TIMEOUT_SECONDS = 60.0
DEFAULT_MAX_ASSERTIONS_PER_SIDE = 128

ALLOWED_INPUT_KEYS = {"record_id", "source_text", "candidate_text"}


def loadmod(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def invalid(record_id: str, reason: str) -> dict:
    return {
        "record_id": record_id,
        "predicted_outcome": "INVALID_VERIFICATION",
        "invalid_reason": reason,
        "runtime_id": RUNTIME_ID,
        "model_inference": False,
        "assertion_alignment": [],
        "relation_alignment": [],
    }


def validate_record(record: dict) -> str | None:
    if set(record) != ALLOWED_INPUT_KEYS:
        return "INPUT_SCHEMA_MISMATCH"
    if not isinstance(record["record_id"], str) or not record["record_id"]:
        return "INVALID_RECORD_ID"
    if not isinstance(record["source_text"], str) or not record["source_text"].strip():
        return "EMPTY_SOURCE_TEXT"
    if not isinstance(record["candidate_text"], str) or not record["candidate_text"].strip():
        return "EMPTY_CANDIDATE_TEXT"
    return None


def process_record(record: dict, max_assertions_per_side: int) -> dict:
    reason = validate_record(record)
    rid = str(record.get("record_id", ""))
    if reason:
        return invalid(rid, reason)

    ra = loadmod("v25_runtime_extractor", EXTRACTOR_PATH)
    b1 = loadmod("v25_runtime_aligner", ALIGNER_PATH)

    source_graph = ra.relation_aware_extract(record["source_text"], f"{rid}-SRC")
    candidate_graph = ra.relation_aware_extract(record["candidate_text"], f"{rid}-CAND")

    source_n = len(source_graph["assertions"])
    candidate_n = len(candidate_graph["assertions"])

    if source_n == 0 or candidate_n == 0:
        return invalid(rid, "UNUSABLE_EMPTY_ASSERTION_REPRESENTATION")

    if source_n > max_assertions_per_side or candidate_n > max_assertions_per_side:
        return invalid(rid, "ASSERTION_COUNT_OUT_OF_SUPPORTED_ENVELOPE")

    pred = b1.align_pair({
        "pair_id": rid,
        "source_graph": source_graph,
        "candidate_graph": candidate_graph,
    })

    return {
        "record_id": rid,
        "predicted_outcome": pred["predicted_outcome"],
        "invalid_reason": None,
        "runtime_id": RUNTIME_ID,
        "model_inference": False,
        "assertion_alignment": pred["assertion_alignment"],
        "relation_alignment": pred["relation_alignment"],
    }


def run_child_command(command: list[str], stdin_text: str, timeout_seconds: float) -> tuple[str, str | None]:
    """
    Execute one isolated child exactly once.

    Returns:
      ("OK", stdout) on zero exit;
      ("TIMEOUT", None) on timeout;
      ("CRASH", diagnostic) on nonzero/launch failure.

    There is intentionally no retry.
    """
    try:
        proc = subprocess.run(
            command,
            input=stdin_text,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT", None
    except Exception as exc:
        return "CRASH", f"{type(exc).__name__}:{exc}"

    if proc.returncode != 0:
        diag = (proc.stderr or "").strip()
        return "CRASH", f"EXIT_{proc.returncode}:{diag[:1000]}"
    return "OK", proc.stdout


def guarded_process_record(record: dict, timeout_seconds: float, max_assertions_per_side: int) -> dict:
    rid = str(record.get("record_id", ""))
    reason = validate_record(record)
    if reason:
        return invalid(rid, reason)

    cmd = [
        sys.executable,
        str(pathlib.Path(__file__).resolve()),
        "--child",
        "--max-assertions-per-side",
        str(max_assertions_per_side),
    ]
    status, payload = run_child_command(
        cmd,
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n",
        timeout_seconds,
    )

    if status == "TIMEOUT":
        return invalid(rid, "RECORD_TIMEOUT")
    if status == "CRASH":
        return invalid(rid, "CHILD_PROCESS_CRASH")

    try:
        out = json.loads(payload)
    except Exception:
        return invalid(rid, "CHILD_OUTPUT_INVALID_JSON")

    if out.get("record_id") != rid:
        return invalid(rid, "CHILD_RECORD_ID_MISMATCH")
    if out.get("predicted_outcome") not in {
        "PASS_CANDIDATE", "REJECT", "REVIEW", "INVALID_VERIFICATION"
    }:
        return invalid(rid, "CHILD_OUTCOME_INVALID")
    return out


def parse_jsonl_bytes(raw: bytes) -> list[dict]:
    text = raw.decode("utf-8")
    out = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except Exception as exc:
            raise ValueError(f"Invalid JSON at line {lineno}: {exc}") from exc
        if not isinstance(obj, dict):
            raise ValueError(f"Input line {lineno} is not a JSON object.")
        out.append(obj)
    return out


def run_batch(
    input_path: pathlib.Path,
    output_path: pathlib.Path,
    expected_input_sha256: str | None,
    expected_count: int | None,
    timeout_seconds: float,
    max_assertions_per_side: int,
):
    raw = input_path.read_bytes()
    actual_sha = sha256_bytes(raw)
    if expected_input_sha256 and actual_sha != expected_input_sha256:
        raise RuntimeError(
            f"Input SHA-256 mismatch: expected {expected_input_sha256}, got {actual_sha}"
        )

    records = parse_jsonl_bytes(raw)
    if expected_count is not None and len(records) != expected_count:
        raise RuntimeError(
            f"Input count mismatch: expected {expected_count}, got {len(records)}"
        )

    ids = [str(r.get("record_id", "")) for r in records]
    if len(set(ids)) != len(ids):
        raise RuntimeError("Duplicate record IDs in input.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    outputs = []

    for record in records:
        # Strictly sequential one-record execution.
        outputs.append(
            guarded_process_record(
                record,
                timeout_seconds=timeout_seconds,
                max_assertions_per_side=max_assertions_per_side,
            )
        )

    if len(outputs) != len(records):
        raise RuntimeError("Output count differs from input count.")
    if [o["record_id"] for o in outputs] != ids:
        raise RuntimeError("Output record IDs/order differ from input.")

    output_path.write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in outputs),
        encoding="utf-8",
        newline="\n",
    )

    print(json.dumps({
        "runtime_id": RUNTIME_ID,
        "input_sha256": actual_sha,
        "input_count": len(records),
        "output_count": len(outputs),
        "timeout_seconds": timeout_seconds,
        "max_assertions_per_side": max_assertions_per_side,
        "retry_count": 0,
        "outcomes": {
            key: sum(x["predicted_outcome"] == key for x in outputs)
            for key in ["PASS_CANDIDATE", "REJECT", "REVIEW", "INVALID_VERIFICATION"]
        },
        "output_sha256": sha256_bytes(output_path.read_bytes()),
    }, indent=2, sort_keys=True))


def child_main(max_assertions_per_side: int):
    raw = sys.stdin.read()
    record = json.loads(raw)
    result = process_record(record, max_assertions_per_side)
    sys.stdout.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--child", action="store_true")
    ap.add_argument("--input", type=pathlib.Path)
    ap.add_argument("--output", type=pathlib.Path)
    ap.add_argument("--expected-input-sha256")
    ap.add_argument("--expected-count", type=int)
    ap.add_argument("--timeout-seconds", type=float, default=DEFAULT_RECORD_TIMEOUT_SECONDS)
    ap.add_argument(
        "--max-assertions-per-side",
        type=int,
        default=DEFAULT_MAX_ASSERTIONS_PER_SIDE,
    )
    args = ap.parse_args()

    if args.child:
        child_main(args.max_assertions_per_side)
        return

    if args.input is None or args.output is None:
        ap.error("--input and --output are required in batch mode.")

    if args.timeout_seconds <= 0:
        ap.error("--timeout-seconds must be >0.")
    if args.max_assertions_per_side <= 0:
        ap.error("--max-assertions-per-side must be >0.")

    run_batch(
        args.input,
        args.output,
        expected_input_sha256=args.expected_input_sha256,
        expected_count=args.expected_count,
        timeout_seconds=args.timeout_seconds,
        max_assertions_per_side=args.max_assertions_per_side,
    )


if __name__ == "__main__":
    main()
