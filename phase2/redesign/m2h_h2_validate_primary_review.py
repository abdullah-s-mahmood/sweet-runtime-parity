#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_PACKET_SHA256 = "e8e7dd687267cb4a53ea30c8f089114358b24123d9a0b4f3fbc9f061a404d9de"
EXPECTED_ROWS = 250

ALLOWED = {
    "necessity": {
        "REQUIRED_CORRECTION",
        "OPTIONAL_OR_STYLISTIC",
        "NO_CORRECTION_NEEDED",
        "UNCERTAIN",
    },
    "candidate_correctness": {
        "CORRECT_IN_CONTEXT",
        "ACCEPTABLE_ALTERNATIVE",
        "INCORRECT",
        "UNCERTAIN",
    },
    "meaning_fidelity": {
        "PRESERVED",
        "CHANGED",
        "UNCERTAIN",
    },
    "final_blinded_disposition": {
        "SUPPORTED_MANDATORY",
        "SUPPORTED_OPTIONAL_OR_ALTERNATIVE",
        "UNNECESSARY_EDIT",
        "WRONG_CORRECTION",
        "UNCERTAIN_REVIEW",
    },
}

REQUIRED_KEYS = {
    "packet_id",
    "necessity",
    "candidate_correctness",
    "meaning_fidelity",
    "final_blinded_disposition",
    "brief_rationale",
}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(p: Path):
    rows = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception as e:
            raise SystemExit(f"{p}:{i}: invalid JSON: {e}")
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--review", required=True)
    ap.add_argument("--reviewer-id", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    packet_path = Path(args.packet)
    review_path = Path(args.review)

    if sha256_file(packet_path) != EXPECTED_PACKET_SHA256:
        raise SystemExit("Blind packet SHA256 mismatch")

    packet = read_jsonl(packet_path)
    review = read_jsonl(review_path)

    if len(packet) != EXPECTED_ROWS:
        raise SystemExit(f"packet row count mismatch: {len(packet)}")
    if len(review) != EXPECTED_ROWS:
        raise SystemExit(f"review row count mismatch: {len(review)}")

    packet_ids = [r["packet_id"] for r in packet]
    if len(set(packet_ids)) != EXPECTED_ROWS:
        raise SystemExit("duplicate packet IDs")

    seen = set()
    errors = []

    for i, row in enumerate(review, 1):
        keys = set(row)
        if keys != REQUIRED_KEYS:
            errors.append(f"row {i}: keys mismatch: {sorted(keys)}")
            continue

        pid = row["packet_id"]
        if pid in seen:
            errors.append(f"row {i}: duplicate packet_id {pid}")
        seen.add(pid)

        if pid not in set(packet_ids):
            errors.append(f"row {i}: unknown packet_id {pid}")

        for field, allowed in ALLOWED.items():
            if row[field] not in allowed:
                errors.append(f"row {i}: invalid {field}={row[field]!r}")

        rationale = row["brief_rationale"]
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"row {i}: missing rationale")

        if row["final_blinded_disposition"] == "SUPPORTED_MANDATORY":
            if row["necessity"] != "REQUIRED_CORRECTION":
                errors.append(f"row {i}: SUPPORTED_MANDATORY requires REQUIRED_CORRECTION")
            if row["candidate_correctness"] != "CORRECT_IN_CONTEXT":
                errors.append(f"row {i}: SUPPORTED_MANDATORY requires CORRECT_IN_CONTEXT")
            if row["meaning_fidelity"] != "PRESERVED":
                errors.append(f"row {i}: SUPPORTED_MANDATORY requires PRESERVED")

    if set(packet_ids) != seen:
        missing = sorted(set(packet_ids) - seen)
        extra = sorted(seen - set(packet_ids))
        errors.append(f"packet coverage mismatch; missing={missing[:5]}, extra={extra[:5]}")

    if errors:
        for e in errors[:100]:
            print("ERROR", e)
        raise SystemExit(f"review validation failed with {len(errors)} errors")

    summary = {
        "record_id": "M2H_H2_ALIF_VARIANT_PRIMARY_REVIEW_VALIDATION_V1",
        "status": "PASS",
        "reviewer_id": args.reviewer_id,
        "packet_sha256": EXPECTED_PACKET_SHA256,
        "review_sha256": sha256_file(review_path),
        "rows": len(review),
        "complete_packet_coverage": True,
        "label_schema_valid": True,
        "mandatory_internal_consistency_valid": True,
        "blinded_stage": "A",
    }

    Path(args.out).write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
