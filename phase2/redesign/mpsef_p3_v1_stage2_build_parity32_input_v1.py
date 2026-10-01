#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_MANIFEST_SHA = "384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e"
EXPECTED_P1_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_N = 32


def sha_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path):
    return [
        json.loads(x)
        for x in Path(path).read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def write_jsonl(path, rows):
    Path(path).write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False, sort_keys=True)
            for r in rows
        ) + "\n",
        encoding="utf-8",
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--p1-proposals", required=True)
    ap.add_argument("--ordered-out", required=True)
    ap.add_argument("--reversed-out", required=True)
    args = ap.parse_args()

    if sha_file(args.manifest) != EXPECTED_MANIFEST_SHA:
        raise RuntimeError("P3_STAGE2_PARITY32_MANIFEST_SHA_MISMATCH")
    if sha_file(args.p1_proposals) != EXPECTED_P1_SHA:
        raise RuntimeError("P3_STAGE2_PARITY32_P1_SHA_MISMATCH")

    manifest = load_jsonl(args.manifest)
    p1 = load_jsonl(args.p1_proposals)
    if len(manifest) != EXPECTED_N:
        raise RuntimeError(f"P3_STAGE2_PARITY32_COUNT_MISMATCH:{len(manifest)}")

    by_p1 = {r["uid"]: r for r in p1}
    rows = []
    for m in manifest:
        uid = m["uid"]
        if uid not in by_p1:
            raise RuntimeError(f"P3_STAGE2_PARITY32_P1_UID_MISSING:{uid}")
        p = by_p1[uid]
        if p["source_version_hash"] != m["source_sha256"]:
            raise RuntimeError(f"P3_STAGE2_PARITY32_SOURCE_SHA_MISMATCH:{uid}")
        rows.append({
            "uid": p["uid"],
            "case_id": p["case_id"],
            "cluster_id": p["cluster_id"],
            "source": p["source"],
            "source_sha256": p["source_version_hash"],
        })

    if len(rows) != EXPECTED_N or len({r["uid"] for r in rows}) != EXPECTED_N:
        raise RuntimeError("P3_STAGE2_PARITY32_INPUT_UID_VALIDATION_FAILED")

    write_jsonl(args.ordered_out, rows)
    write_jsonl(args.reversed_out, list(reversed(rows)))

    print(json.dumps({
        "record_id": "MPSEF_P3_V1_STAGE2_PARITY32_INPUT_BUILDER_V1",
        "status": "PASS",
        "n": EXPECTED_N,
        "ordered_sha256": sha_file(args.ordered_out),
        "reversed_sha256": sha_file(args.reversed_out),
        "gold_reference_consulted": False,
    }, indent=2))


if __name__ == "__main__":
    main()
