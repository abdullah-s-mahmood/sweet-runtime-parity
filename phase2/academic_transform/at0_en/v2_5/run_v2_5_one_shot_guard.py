#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys

RUNTIME_ID = "AT0-EN V2.5"
EXPECTED_FACTPICO_INPUT_SHA256 = "ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82"
EXPECTED_FACTPICO_COUNT = 345
FACTPICO_AUTHORIZATION_ID = "FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001"
DURABLE_LEDGER_PROVIDER = "github:abdullah-s-mahmood/sweet-runtime-parity@factpico-v25-one-shot-ledger"
DURABLE_LEDGER_KEY = (
    "claims/real/"
    + FACTPICO_AUTHORIZATION_ID
    + "/"
    + EXPECTED_FACTPICO_INPUT_SHA256
    + "/ATTEMPT_CLAIM.json"
)


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def exclusive_json(path: pathlib.Path, payload: dict) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o444)
    try:
        data = (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=pathlib.Path, required=True)
    ap.add_argument("--attempt-dir", type=pathlib.Path, required=True)
    ap.add_argument("--attempt-id", required=True)
    ap.add_argument("--runner", type=pathlib.Path, required=True)
    ap.add_argument("--timeout-seconds", type=float, default=60.0)
    ap.add_argument("--max-assertions-per-side", type=int, default=128)
    ap.add_argument("--expected-input-sha256", default=EXPECTED_FACTPICO_INPUT_SHA256)
    ap.add_argument("--expected-count", type=int, default=EXPECTED_FACTPICO_COUNT)
    ap.add_argument("--authorization-id")
    ap.add_argument("--durable-ledger-provider")
    ap.add_argument("--durable-ledger-key")
    ap.add_argument("--durable-ledger-commit-sha")
    args = ap.parse_args()

    if os.environ.get("ACAD_PASS_V25_SYNTHETIC_TEST_MODE") == "1":
        raise RuntimeError("Synthetic test mode must be disabled for a one-shot attempt.")
    if os.environ.get("ACAD_PASS_V25_SYNTHETIC_FAULT_MAP"):
        raise RuntimeError("Synthetic fault map must be absent for a one-shot attempt.")

    real_factpico = (
        args.expected_input_sha256 == EXPECTED_FACTPICO_INPUT_SHA256
        and args.expected_count == EXPECTED_FACTPICO_COUNT
    )
    if real_factpico:
        if args.authorization_id != FACTPICO_AUTHORIZATION_ID:
            raise RuntimeError("Missing or incorrect frozen FactPICO authorization ID.")
        if args.durable_ledger_provider != DURABLE_LEDGER_PROVIDER:
            raise RuntimeError("Missing or incorrect frozen durable-ledger provider.")
        if args.durable_ledger_key != DURABLE_LEDGER_KEY:
            raise RuntimeError("Missing or incorrect frozen durable-ledger key.")
        if not args.durable_ledger_commit_sha:
            raise RuntimeError("Durable-ledger claim commit SHA is required before FactPICO inference.")

    if args.attempt_dir.exists():
        raise RuntimeError("Attempt directory already exists; attempt is consumed or output already frozen.")

    actual_input_sha = sha256_file(args.input)
    if actual_input_sha != args.expected_input_sha256:
        raise RuntimeError("Input SHA-256 mismatch before one-shot claim.")

    args.attempt_dir.parent.mkdir(parents=True, exist_ok=True)
    os.mkdir(args.attempt_dir)

    claim_path = args.attempt_dir / "ATTEMPT_CLAIM.json"
    predictions_path = args.attempt_dir / "FACTPICO_V25_PREDICTIONS.jsonl"
    stdout_path = args.attempt_dir / "RUNNER_STDOUT.txt"
    stderr_path = args.attempt_dir / "RUNNER_STDERR.txt"

    exclusive_json(claim_path, {
        "attempt_id": args.attempt_id,
        "state": "CONSUMED_BEFORE_INFERENCE",
        "runtime_id": RUNTIME_ID,
        "input_sha256": actual_input_sha,
        "expected_count": args.expected_count,
        "timeout_seconds": args.timeout_seconds,
        "max_assertions_per_side": args.max_assertions_per_side,
        "retry_count": 0,
        "authorization_id": args.authorization_id,
        "durable_ledger_provider": args.durable_ledger_provider,
        "durable_ledger_key": args.durable_ledger_key,
        "durable_ledger_commit_sha": args.durable_ledger_commit_sha,
    })

    cmd = [
        sys.executable,
        str(args.runner),
        "--input", str(args.input),
        "--output", str(predictions_path),
        "--expected-input-sha256", args.expected_input_sha256,
        "--expected-count", str(args.expected_count),
        "--timeout-seconds", str(args.timeout_seconds),
        "--max-assertions-per-side", str(args.max_assertions_per_side),
    ]

    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    stdout_path.write_text(proc.stdout or "", encoding="utf-8")
    stderr_path.write_text(proc.stderr or "", encoding="utf-8")

    if proc.returncode != 0:
        exclusive_json(args.attempt_dir / "ATTEMPT_ABORTED.json", {
            "attempt_id": args.attempt_id,
            "state": "ABORTED_CONSUMED",
            "returncode": proc.returncode,
        })
        raise SystemExit(proc.returncode)

    if not predictions_path.exists():
        raise RuntimeError("Runner returned success without predictions artifact.")

    prediction_sha = sha256_file(predictions_path)
    exclusive_json(args.attempt_dir / "PREDICTION_FREEZE.json", {
        "attempt_id": args.attempt_id,
        "state": "PREDICTIONS_FROZEN",
        "runtime_id": RUNTIME_ID,
        "prediction_sha256": prediction_sha,
        "input_sha256": actual_input_sha,
        "retry_count": 0,
        "authorization_id": args.authorization_id,
        "durable_ledger_provider": args.durable_ledger_provider,
        "durable_ledger_key": args.durable_ledger_key,
        "durable_ledger_commit_sha": args.durable_ledger_commit_sha,
    })

    predictions_path.chmod(0o444)
    print(json.dumps({
        "attempt_id": args.attempt_id,
        "prediction_sha256": prediction_sha,
        "predictions": str(predictions_path),
        "state": "PREDICTIONS_FROZEN",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
