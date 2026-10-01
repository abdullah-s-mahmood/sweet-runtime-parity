#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from transformers import BertForTokenClassification, BertTokenizer

from mpsef_p1_cf_proposals_v1 import install_rewrite_compat
from mpsef_p3_v1_stage1_v1 import single_pnx, batch_pnx

VERSION = "MPSEF_P3_V1_STAGE1_PARITY32_REMEDIATION_V1"
EXPECTED_MANIFEST_SHA = "384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e"
EXPECTED_P1_PROPOSAL_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P3_PROPOSAL_SHA = "69720287154071611a0e0d0af2a6689ef6ed5242acf374fb945de70013a16083"
EXPECTED_PNX_WEIGHT_SHA = "d98d683f9ef1738c27f5031c99483d93e9f73c4116c158a97a678270c84fd262"
EXPECTED_N = 32


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--p1-proposals", required=True)
    ap.add_argument("--p3-proposals", required=True)
    ap.add_argument("--pnx-model-dir", required=True)
    ap.add_argument("--upstream-root", required=True)
    ap.add_argument("--out", default="MPSEF_P3_V1_STAGE1_PARITY32_REMEDIATION_V1.json")
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    p1_path = Path(args.p1_proposals)
    p3_path = Path(args.p3_proposals)
    model_dir = Path(args.pnx_model_dir)

    if sha_bytes(manifest_path.read_bytes()) != EXPECTED_MANIFEST_SHA:
        raise RuntimeError("PARITY32_MANIFEST_SHA_MISMATCH")
    if sha_bytes(p1_path.read_bytes()) != EXPECTED_P1_PROPOSAL_SHA:
        raise RuntimeError("P1_PROPOSAL_SHA_MISMATCH")
    if sha_bytes(p3_path.read_bytes()) != EXPECTED_P3_PROPOSAL_SHA:
        raise RuntimeError("P3_STAGE1_PROPOSAL_SHA_MISMATCH")
    if sha_file(model_dir / "pytorch_model.bin") != EXPECTED_PNX_WEIGHT_SHA:
        raise RuntimeError("PNX_WEIGHT_SHA_MISMATCH")

    manifest = load_jsonl(manifest_path)
    p1_rows = load_jsonl(p1_path)
    p3_rows = load_jsonl(p3_path)

    if len(manifest) != EXPECTED_N:
        raise RuntimeError(f"PARITY32_COUNT_MISMATCH:{len(manifest)}")

    p1_by_uid = {r["uid"]: r for r in p1_rows}
    p3_by_uid = {r["uid"]: r for r in p3_rows}

    selected = []
    for m in manifest:
        uid = m["uid"]
        if uid not in p1_by_uid:
            raise RuntimeError(f"P1_PARENT_UID_MISSING:{uid}")
        if uid not in p3_by_uid:
            raise RuntimeError(f"P3_UID_MISSING:{uid}")

        p1 = p1_by_uid[uid]
        p3 = p3_by_uid[uid]

        if p1["source_version_hash"] != m["source_sha256"]:
            raise RuntimeError(f"P1_SOURCE_SHA_MISMATCH:{uid}")
        if p3["source_sha256"] != m["source_sha256"]:
            raise RuntimeError(f"P3_SOURCE_SHA_MISMATCH:{uid}")

        parent_text = p1["full_proposer_output"]
        parent_sha = p1["output_sha256"]

        if sha_text(parent_text) != parent_sha:
            raise RuntimeError(f"P1_PARENT_OUTPUT_SHA_INVALID:{uid}")
        if p3["parent_output_sha256"] != parent_sha:
            raise RuntimeError(f"P3_PARENT_SHA_NOT_P1:{uid}")
        if p3["input_sha256"] != parent_sha:
            raise RuntimeError(f"P3_INPUT_SHA_NOT_P1:{uid}")
        if p3["input_text"] != parent_text:
            raise RuntimeError(f"P3_INPUT_TEXT_NOT_P1:{uid}")

        selected.append((m, p1, p3))

    rewrite = install_rewrite_compat(Path(args.upstream_root))
    tokenizer = BertTokenizer.from_pretrained(model_dir)
    model = BertForTokenClassification.from_pretrained(model_dir)
    model.eval()

    parents = [p1["full_proposer_output"] for _, p1, _ in selected]

    # 1) single
    single = {}
    for m, p1, _ in selected:
        single[m["uid"]] = single_pnx(
            model, tokenizer, rewrite, p1["full_proposer_output"]
        )

    # 2) true batch over the exact 32
    batch_steps = batch_pnx(model, tokenizer, rewrite, parents)
    batch = {
        m["uid"]: step
        for (m, _, _), step in zip(selected, batch_steps)
    }

    # 3) reversed batch
    reversed_selected = list(reversed(selected))
    reversed_steps = batch_pnx(
        model,
        tokenizer,
        rewrite,
        [p1["full_proposer_output"] for _, p1, _ in reversed_selected],
    )
    reversed_batch = {
        m["uid"]: step
        for (m, _, _), step in zip(reversed_selected, reversed_steps)
    }

    # 4) repeat original batch
    repeat_steps = batch_pnx(model, tokenizer, rewrite, parents)
    repeat = {
        m["uid"]: step
        for (m, _, _), step in zip(selected, repeat_steps)
    }

    counts = {
        "single_vs_batch": 0,
        "batch_vs_reversed": 0,
        "batch_vs_repeat": 0,
        "batch_vs_frozen_trace": 0,
        "batch_output_vs_frozen_output": 0,
        "parent_identity": 0,
    }
    rows = []

    for m, p1, frozen in selected:
        uid = m["uid"]
        s = single[uid]
        b = batch[uid]
        rb = reversed_batch[uid]
        rp = repeat[uid]
        frozen_trace = frozen["pnx_trace"]
        frozen_output = frozen["full_proposer_output"]

        a = s == b
        c = b == rb
        d = b == rp
        e = b == frozen_trace
        f = b["output"] == frozen_output
        g = (
            frozen["parent_output_sha256"] == p1["output_sha256"]
            and frozen["input_sha256"] == p1["output_sha256"]
            and frozen["input_text"] == p1["full_proposer_output"]
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
            "source_sha256": m["source_sha256"],
            "parent_output_sha256": p1["output_sha256"],
            "frozen_output_sha256": frozen["output_sha256"],
            "fresh_output_sha256": sha_text(b["output"]),
            "single_vs_batch": a,
            "batch_vs_reversed": c,
            "batch_vs_repeat": d,
            "batch_vs_frozen_trace": e,
            "batch_output_vs_frozen_output": f,
            "parent_identity": g,
        })

    status = "PASS" if all(v == EXPECTED_N for v in counts.values()) else "FAIL"

    result = {
        "record_id": VERSION,
        "status": status,
        "n": EXPECTED_N,
        "manifest_sha256": EXPECTED_MANIFEST_SHA,
        "p1_proposal_sha256": EXPECTED_P1_PROPOSAL_SHA,
        "p3_stage1_proposal_sha256": EXPECTED_P3_PROPOSAL_SHA,
        "pnx_weight_sha256": EXPECTED_PNX_WEIGHT_SHA,
        "counts": counts,
        "rows": rows,
        "project_source_loaded": True,
        "project_source_scope": "FROZEN_STAGE1_PARITY32_ONLY",
        "project_gold_loaded": False,
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "proposal_artifact_modified": False,
        "p1_rerun": False,
        "exact_frozen_p1_parent_reused": True,
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
        "project_gold_loaded": result["project_gold_loaded"],
        "quality_metric_computed": result["quality_metric_computed"],
        "proposal_artifact_modified": result["proposal_artifact_modified"],
        "p1_rerun": result["p1_rerun"],
        "exact_frozen_p1_parent_reused": result["exact_frozen_p1_parent_reused"],
    }, ensure_ascii=False, indent=2))

    if status != "PASS":
        raise RuntimeError("P3_V1_STAGE1_PARITY32_REMEDIATION_FAILED")


if __name__ == "__main__":
    main()
