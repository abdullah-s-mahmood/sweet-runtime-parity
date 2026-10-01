#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from transformers import BertForTokenClassification, BertTokenizer

from mpsef_p1_cf_proposals_v1 import install_rewrite_compat, infer_pass

VERSION = "MPSEF_P1_STAGE1_PARITY32_REMEDIATION_V1"
EXPECTED_MANIFEST_SHA = "384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e"
EXPECTED_P1_PROPOSAL_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P1_WEIGHT_SHA = "9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d"
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


def run_two_pass(model, tokenizer, rewrite, texts):
    pass1 = infer_pass(
        model, tokenizer, rewrite, [t.split() for t in texts]
    )
    pass1_outputs = [x["output"] for x in pass1]
    pass2 = infer_pass(
        model, tokenizer, rewrite, [t.split() for t in pass1_outputs]
    )
    return [
        {
            "pass1_output": a["output"],
            "pass1_trace": a,
            "pass2_output": b["output"],
            "pass2_trace": b,
        }
        for a, b in zip(pass1, pass2)
    ]


def compact_signature(x):
    return {
        "pass1_output": x["pass1_output"],
        "pass2_output": x["pass2_output"],
        "pass1_trace": x["pass1_trace"],
        "pass2_trace": x["pass2_trace"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--p1-proposals", required=True)
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--upstream-root", required=True)
    ap.add_argument("--out", default="MPSEF_P1_STAGE1_PARITY32_REMEDIATION_V1.json")
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    p1_path = Path(args.p1_proposals)
    model_dir = Path(args.model_dir)

    if sha_bytes(manifest_path.read_bytes()) != EXPECTED_MANIFEST_SHA:
        raise RuntimeError("PARITY32_MANIFEST_SHA_MISMATCH")
    if sha_bytes(p1_path.read_bytes()) != EXPECTED_P1_PROPOSAL_SHA:
        raise RuntimeError("P1_PROPOSAL_SHA_MISMATCH")
    if sha_file(model_dir / "pytorch_model.bin") != EXPECTED_P1_WEIGHT_SHA:
        raise RuntimeError("P1_MODEL_WEIGHT_SHA_MISMATCH")

    manifest = load_jsonl(manifest_path)
    p1_rows = load_jsonl(p1_path)
    if len(manifest) != EXPECTED_N:
        raise RuntimeError(f"PARITY32_COUNT_MISMATCH:{len(manifest)}")

    p1_by_uid = {r["uid"]: r for r in p1_rows}
    selected = []
    for m in manifest:
        uid = m["uid"]
        if uid not in p1_by_uid:
            raise RuntimeError(f"P1_UID_MISSING:{uid}")
        r = p1_by_uid[uid]
        if r["source_version_hash"] != m["source_sha256"]:
            raise RuntimeError(f"P1_SOURCE_SHA_MISMATCH:{uid}")
        if sha_text(r["source"]) != m["source_sha256"]:
            raise RuntimeError(f"P1_SOURCE_TEXT_SHA_MISMATCH:{uid}")
        if sha_text(r["full_proposer_output"]) != r["output_sha256"]:
            raise RuntimeError(f"P1_FROZEN_OUTPUT_SHA_MISMATCH:{uid}")
        selected.append((m, r))

    rewrite = install_rewrite_compat(Path(args.upstream_root))
    tokenizer = BertTokenizer.from_pretrained(model_dir)
    model = BertForTokenClassification.from_pretrained(model_dir)
    model.eval()

    # 1) single
    single = {}
    for m, r in selected:
        x = run_two_pass(model, tokenizer, rewrite, [r["source"]])[0]
        single[m["uid"]] = x

    # 2) true batch
    texts = [r["source"] for _, r in selected]
    batch_list = run_two_pass(model, tokenizer, rewrite, texts)
    batch = {
        m["uid"]: x
        for (m, _), x in zip(selected, batch_list)
    }

    # 3) reversed batch
    reversed_selected = list(reversed(selected))
    reversed_list = run_two_pass(
        model,
        tokenizer,
        rewrite,
        [r["source"] for _, r in reversed_selected],
    )
    reversed_batch = {
        m["uid"]: x
        for (m, _), x in zip(reversed_selected, reversed_list)
    }

    # 4) repeat original batch
    repeat_list = run_two_pass(model, tokenizer, rewrite, texts)
    repeat = {
        m["uid"]: x
        for (m, _), x in zip(selected, repeat_list)
    }

    rows = []
    counts = {
        "single_vs_batch": 0,
        "batch_vs_reversed": 0,
        "batch_vs_repeat": 0,
        "fresh_vs_frozen_output": 0,
    }

    for m, frozen in selected:
        uid = m["uid"]
        s = compact_signature(single[uid])
        b = compact_signature(batch[uid])
        rb = compact_signature(reversed_batch[uid])
        rp = compact_signature(repeat[uid])

        single_batch = s == b
        batch_reversed = b == rb
        batch_repeat = b == rp
        fresh_frozen = b["pass2_output"] == frozen["full_proposer_output"]

        counts["single_vs_batch"] += int(single_batch)
        counts["batch_vs_reversed"] += int(batch_reversed)
        counts["batch_vs_repeat"] += int(batch_repeat)
        counts["fresh_vs_frozen_output"] += int(fresh_frozen)

        rows.append({
            "uid": uid,
            "rank_index": m["rank_index"],
            "source_sha256": m["source_sha256"],
            "frozen_output_sha256": frozen["output_sha256"],
            "fresh_output_sha256": sha_text(b["pass2_output"]),
            "single_vs_batch": single_batch,
            "batch_vs_reversed": batch_reversed,
            "batch_vs_repeat": batch_repeat,
            "fresh_vs_frozen_output": fresh_frozen,
        })

    status = "PASS" if all(v == EXPECTED_N for v in counts.values()) else "FAIL"

    result = {
        "record_id": VERSION,
        "status": status,
        "n": EXPECTED_N,
        "manifest_sha256": EXPECTED_MANIFEST_SHA,
        "p1_proposal_sha256": EXPECTED_P1_PROPOSAL_SHA,
        "p1_weight_sha256": EXPECTED_P1_WEIGHT_SHA,
        "counts": counts,
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
        k: result[k]
        for k in (
            "record_id", "status", "n", "counts",
            "project_gold_loaded", "quality_metric_computed",
            "proposal_artifact_modified",
        )
    }, ensure_ascii=False, indent=2))

    if status != "PASS":
        raise RuntimeError("P1_STAGE1_PARITY32_REMEDIATION_FAILED")


if __name__ == "__main__":
    main()
