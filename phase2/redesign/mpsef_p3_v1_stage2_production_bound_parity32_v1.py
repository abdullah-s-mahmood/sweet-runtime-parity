#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

VERSION = "MPSEF_P3_V1_STAGE2_PRODUCTION_BOUND_PARITY32_V1"
EXPECTED_MANIFEST_SHA = "384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e"
EXPECTED_P1_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P3_SHA = "69720287154071611a0e0d0af2a6689ef6ed5242acf374fb945de70013a16083"
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--p1-proposals", required=True)
    ap.add_argument("--frozen-p3", required=True)
    ap.add_argument("--single", required=True)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--repeat", required=True)
    ap.add_argument("--reversed", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    if sha_file(args.manifest) != EXPECTED_MANIFEST_SHA:
        raise RuntimeError("PARITY32_MANIFEST_SHA_MISMATCH")
    if sha_file(args.p1_proposals) != EXPECTED_P1_SHA:
        raise RuntimeError("P1_PROPOSAL_SHA_MISMATCH")
    if sha_file(args.frozen_p3) != EXPECTED_P3_SHA:
        raise RuntimeError("P3_FROZEN_PROPOSAL_SHA_MISMATCH")

    manifest = load_jsonl(args.manifest)
    p1 = load_jsonl(args.p1_proposals)
    frozen = load_jsonl(args.frozen_p3)
    single = load_jsonl(args.single)
    batch = load_jsonl(args.batch)
    repeat = load_jsonl(args.repeat)
    reverse = load_jsonl(args.reversed)

    p1_by = {r["uid"]: r for r in p1}
    frozen_by = {r["uid"]: r for r in frozen}
    single_by = {r["uid"]: r for r in single}
    batch_by = {r["uid"]: r for r in batch}
    repeat_by = {r["uid"]: r for r in repeat}
    reverse_by = {r["uid"]: r for r in reverse}

    expected = {m["uid"] for m in manifest}
    if len(expected) != EXPECTED_N:
        raise RuntimeError("PARITY32_UID_COUNT_MISMATCH")
    for name, by in (
        ("single", single_by),
        ("batch", batch_by),
        ("repeat", repeat_by),
        ("reverse", reverse_by),
    ):
        if set(by) != expected or len(by) != EXPECTED_N:
            raise RuntimeError(f"{name.upper()}_UID_SET_MISMATCH")

    counts = {
        "single_vs_batch": 0,
        "batch_vs_reversed": 0,
        "batch_vs_repeat": 0,
        "batch_vs_frozen_trace": 0,
        "batch_output_vs_frozen_output": 0,
        "parent_identity": 0,
    }
    rows = []

    for m in manifest:
        uid = m["uid"]
        p = p1_by[uid]
        fz = frozen_by[uid]
        s = single_by[uid]
        b = batch_by[uid]
        rp = repeat_by[uid]
        rv = reverse_by[uid]

        a = s["pnx_trace"] == b["pnx_trace"]
        c = b["pnx_trace"] == rv["pnx_trace"]
        d = b["pnx_trace"] == rp["pnx_trace"]
        e = b["pnx_trace"] == fz["pnx_trace"]
        f = b["full_proposer_output"] == fz["full_proposer_output"]
        g = (
            b["parent_output_sha256"] == p["output_sha256"]
            and b["input_sha256"] == p["output_sha256"]
            and b["input_text"] == p["full_proposer_output"]
            and fz["parent_output_sha256"] == p["output_sha256"]
            and fz["input_sha256"] == p["output_sha256"]
        )

        counts["single_vs_batch"] += int(a)
        counts["batch_vs_reversed"] += int(c)
        counts["batch_vs_repeat"] += int(d)
        counts["batch_vs_frozen_trace"] += int(e)
        counts["batch_output_vs_frozen_output"] += int(f)
        counts["parent_identity"] += int(g)

        rows.append({
            "uid": uid,
            "rank_index": m["rank_index"],
            "single_vs_batch": a,
            "batch_vs_reversed": c,
            "batch_vs_repeat": d,
            "batch_vs_frozen_trace": e,
            "batch_output_vs_frozen_output": f,
            "parent_identity": g,
            "batch_output_sha256": b["output_sha256"],
            "frozen_output_sha256": fz["output_sha256"],
            "stage_b_domain_v1": b["stage_b_domain_from_p1"],
        })

    status = (
        "PASS"
        if all(v == EXPECTED_N for v in counts.values())
        else "FAIL"
    )
    result = {
        "record_id": VERSION,
        "status": status,
        "n": EXPECTED_N,
        "counts": counts,
        "manifest_sha256": EXPECTED_MANIFEST_SHA,
        "p1_proposal_sha256": EXPECTED_P1_SHA,
        "p3_frozen_proposal_sha256": EXPECTED_P3_SHA,
        "production_adapter_cli_used": True,
        "single_case_invocation": "PRODUCTION_CLI_BATCH_SIZE_1",
        "production_batch_size": 32,
        "exact_frozen_p1_parent_reused": True,
        "p1_rerun": False,
        "rows": rows,
        "project_source_loaded": True,
        "project_source_scope": "FROZEN_STAGE1_PARITY32_ONLY",
        "project_gold_loaded": False,
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
    }
    Path(args.out).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "record_id": VERSION,
        "status": status,
        "n": EXPECTED_N,
        "counts": counts,
        "production_adapter_cli_used": True,
        "p1_rerun": False,
        "project_gold_loaded": False,
    }, ensure_ascii=False, indent=2))

    if status != "PASS":
        failures = [
            r for r in rows
            if not all([
                r["single_vs_batch"],
                r["batch_vs_reversed"],
                r["batch_vs_repeat"],
                r["batch_vs_frozen_trace"],
                r["batch_output_vs_frozen_output"],
                r["parent_identity"],
            ])
        ]
        print(json.dumps(
            {"parity_failures": failures},
            ensure_ascii=False,
            indent=2,
        ))
        raise RuntimeError("P3_STAGE2_PRODUCTION_BOUND_PARITY32_FAILED")


if __name__ == "__main__":
    main()
