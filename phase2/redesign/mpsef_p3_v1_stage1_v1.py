#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import statistics
import time
from pathlib import Path

import torch
from transformers import BertForTokenClassification, BertTokenizer

from mpsef_p1_cf_proposals_v1 import install_rewrite_compat, infer_pass
from process_progress_v1 import update_state

VERSION = "MPSEF_P3_V1_STAGE1_RUNNER_V1"
PROPOSER_ID = "P3_V1_SWEET_NOPNX2_PNX1"
PROPOSER_VERSION = "P3_V1_1"
FAMILY_ID = "SWEET_QALB14"
ANCESTRY_ID = "P1_CONTROL_PLUS_PNX1"

EXPECTED_PACKET_SHA256 = "8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1"
EXPECTED_UID_LIST_SHA256 = "e32b468f27653a1bbabfa5c355483c34ffe9b6e4cb2425c36e6c10b714c104ac"
EXPECTED_P1_PROPOSAL_SHA256 = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_REGISTRY_SHA256 = "b448650c571f6c93dffe4825417e4f65d6a8cd02e33bd9551728ceac2b242b1a"
EXPECTED_PNX_REVISION = "a162d77269ab6ff556d2c58c5dff8b967c1f649e"
EXPECTED_PNX_WEIGHT_SHA256 = "d98d683f9ef1738c27f5031c99483d93e9f73c4116c158a97a678270c84fd262"
EXPECTED_PNX_CONFIG_SHA256 = "2b65052e89f8a44585e3618febf7b65593db109e475f7569ac5d4a96799350f0"
EXPECTED_CASES = 128
PARITY_N = 8


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


def change_domain(a: str, b: str) -> str:
    if a == b:
        return "NO_CHANGE_FROM_P1"
    import difflib, unicodedata
    classes = set()
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        for ch in a[i1:i2] + b[j1:j2]:
            if ch.isspace():
                classes.add("SPACE")
            elif unicodedata.category(ch).startswith("P"):
                classes.add("PUNCT")
            else:
                classes.add("LEXICAL")
    if classes == {"PUNCT"}:
        return "PUNCTUATION_ONLY_FROM_P1"
    if classes == {"SPACE"}:
        return "BOUNDARY_ONLY_FROM_P1"
    if classes == {"LEXICAL"}:
        return "LEXICAL_ONLY_FROM_P1"
    return "MIXED_FROM_P1"


def validate_inputs(packet_path: Path, p1_path: Path):
    if sha_bytes(packet_path.read_bytes()) != EXPECTED_PACKET_SHA256:
        raise RuntimeError("P3_PACKET_SHA_MISMATCH")
    if sha_bytes(p1_path.read_bytes()) != EXPECTED_P1_PROPOSAL_SHA256:
        raise RuntimeError("P3_P1_PARENT_ARTIFACT_SHA_MISMATCH")

    packet = load_jsonl(packet_path)
    p1_rows = load_jsonl(p1_path)
    if len(packet) != EXPECTED_CASES:
        raise RuntimeError(f"P3_PACKET_COUNT_MISMATCH:{len(packet)}")

    by_uid = {r["uid"]: r for r in p1_rows}
    if len(by_uid) != len(p1_rows):
        raise RuntimeError("P3_P1_PARENT_DUPLICATE_UID")

    selected = []
    for row in packet:
        uid = row["uid"]
        if uid not in by_uid:
            raise RuntimeError(f"P3_P1_PARENT_UID_MISSING:{uid}")
        parent = by_uid[uid]
        if parent["source_version_hash"] != row["source_sha256"]:
            raise RuntimeError(f"P3_P1_PARENT_SOURCE_SHA_MISMATCH:{uid}")
        parent_output = parent["full_proposer_output"]
        parent_sha = sha_text(parent_output)
        if parent_sha != parent["output_sha256"]:
            raise RuntimeError(f"P3_P1_PARENT_OUTPUT_SHA_MISMATCH:{uid}")
        selected.append((row, parent))
    return selected


def validate_no_silent_truncation(tokenizer, model, parent_text: str):
    words = parent_text.split()
    enc = tokenizer(
        words,
        is_split_into_words=True,
        add_special_tokens=True,
        truncation=False,
    )
    n = len(enc["input_ids"])
    maxpos = getattr(model.config, "max_position_embeddings", None)
    if isinstance(maxpos, int) and n > maxpos:
        raise RuntimeError(f"P3_PNX_INPUT_TOO_LONG:{n}>{maxpos}")
    return n


def single_pnx(model, tokenizer, rewrite, parent_text: str):
    validate_no_silent_truncation(tokenizer, model, parent_text)
    step = infer_pass(model, tokenizer, rewrite, [parent_text.split()])[0]
    return step


def batch_pnx(model, tokenizer, rewrite, parent_texts):
    for text in parent_texts:
        validate_no_silent_truncation(tokenizer, model, text)
    steps = infer_pass(
        model,
        tokenizer,
        rewrite,
        [t.split() for t in parent_texts],
    )
    if len(steps) != len(parent_texts):
        raise RuntimeError("P3_BATCH_OUTPUT_COUNT_MISMATCH")
    return steps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--p1-proposals", required=True)
    ap.add_argument("--pnx-model-dir", required=True)
    ap.add_argument("--upstream-root", required=True)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--out-prefix", default="MPSEF_P3_V1_STAGE1_V1")
    ap.add_argument("--progress-state", default="MPSEF_P3_V1_STAGE1_PROGRESS.json")
    args = ap.parse_args()

    packet_path = Path(args.packet)
    p1_path = Path(args.p1_proposals)
    selected = validate_inputs(packet_path, p1_path)

    weight_sha = sha_file(Path(args.pnx_model_dir) / "pytorch_model.bin")
    if weight_sha != EXPECTED_PNX_WEIGHT_SHA256:
        raise RuntimeError(f"P3_PNX_WEIGHT_SHA_MISMATCH:{weight_sha}")

    rewrite = install_rewrite_compat(Path(args.upstream_root))
    tokenizer = BertTokenizer.from_pretrained(args.pnx_model_dir)
    model = BertForTokenClassification.from_pretrained(args.pnx_model_dir)
    model.eval()

    cfg_sha = hashlib.sha256(
        model.config.to_json_string().encode()
    ).hexdigest()
    if cfg_sha != EXPECTED_PNX_CONFIG_SHA256:
        raise RuntimeError(f"P3_PNX_CONFIG_SHA_MISMATCH:{cfg_sha}")

    progress_path = Path(args.progress_state)
    total_work = PARITY_N * 2 + EXPECTED_CASES
    done = 0
    update_state(
        progress_path,
        process_id="MPSEF_P3_V1_STAGE1_V1",
        stage="INITIALIZE",
        processed=0,
        total=total_work,
        status="RUNNING",
        message="validated frozen P1 parent artifact and Pnx model identity",
    )

    # True batch-vs-single parity on the first 8 already-frozen packet UIDs.
    parity = selected[:PARITY_N]
    singles = []
    for row, parent in parity:
        step = single_pnx(
            model, tokenizer, rewrite, parent["full_proposer_output"]
        )
        singles.append(step)
        done += 1
        update_state(
            progress_path,
            "MPSEF_P3_V1_STAGE1_V1",
            "PARITY_SINGLE",
            done,
            total_work,
            message=f'uid={row["uid"]}',
        )

    batch_steps = batch_pnx(
        model,
        tokenizer,
        rewrite,
        [parent["full_proposer_output"] for _, parent in parity],
    )
    for i, ((row, _), b, s) in enumerate(zip(parity, batch_steps, singles)):
        if b != s:
            raise RuntimeError(
                f'P3_BATCH_SINGLE_PARITY_FAILED:{row["uid"]}'
            )
        done += 1
        update_state(
            progress_path,
            "MPSEF_P3_V1_STAGE1_V1",
            "PARITY_BATCH",
            done,
            total_work,
            message=f'uid={row["uid"]}',
        )

    out_rows = []
    runtimes = []
    changed = 0
    identical_parent = 0
    domains = {}
    failures = 0

    started = time.monotonic()
    for start in range(0, len(selected), args.batch_size):
        batch = selected[start:start + args.batch_size]
        parent_texts = [p["full_proposer_output"] for _, p in batch]
        t0 = time.monotonic()
        try:
            steps = batch_pnx(
                model, tokenizer, rewrite, parent_texts
            )
            batch_error = None
        except Exception as exc:
            steps = [None] * len(batch)
            batch_error = f"{type(exc).__name__}:{exc}"

        batch_elapsed = time.monotonic() - t0
        per_case = batch_elapsed / max(1, len(batch))

        for (row, parent), step in zip(batch, steps):
            parent_output = parent["full_proposer_output"]
            parent_sha = parent["output_sha256"]
            if sha_text(parent_output) != parent_sha:
                raise RuntimeError(
                    f'P3_PARENT_OUTPUT_IDENTITY_MISMATCH:{row["uid"]}'
                )

            if batch_error is not None:
                state = "EXECUTION_FAILED"
                final = None
                reasons = [batch_error]
                domain = "ALIGNMENT_FAILED"
                trace = None
                failures += 1
            else:
                final = step["output"]
                if final == "":
                    state = "EMPTY_OUTPUT"
                    reasons = ["P3_EMPTY_OUTPUT"]
                    failures += 1
                else:
                    state = "OK"
                    reasons = []
                domain = change_domain(parent_output, final)
                trace = step
                if final == parent_output:
                    identical_parent += 1
                else:
                    changed += 1
                domains[domain] = domains.get(domain, 0) + 1

            rec = {
                "record_id": "MPSEF_P3_V1_STAGE1_PROPOSAL_V1",
                "registry_namespace": "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A",
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
                "parent_proposer_id": "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2",
                "parent_proposer_version": "P1_FROZEN_V1",
                "parent_output": parent_output,
                "parent_output_sha256": parent_sha,
                "input_text": parent_output,
                "input_sha256": parent_sha,
                "full_proposer_output": final,
                "output_sha256": None if final is None else sha_text(final),
                "execution_state": state,
                "failure_reasons": reasons,
                "stage_b_domain_from_p1": domain,
                "pnx_trace": trace,
                "runtime_seconds": per_case,
                "source_only": True,
                "gold_reference_consulted": False,
                "quality_scored": False,
                "provenance_complete": True,
            }
            out_rows.append(rec)
            runtimes.append(per_case)
            done += 1
            update_state(
                progress_path,
                "MPSEF_P3_V1_STAGE1_V1",
                "STAGE1_PNX",
                done,
                total_work,
                message=f'uid={row["uid"]} state={state}',
            )

    out_path = Path(args.out_prefix + ".jsonl")
    out_path.write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False, sort_keys=True)
            for r in out_rows
        ) + "\n",
        encoding="utf-8",
    )

    ordered = sorted(runtimes)
    rank = max(1, int((95 * len(ordered) + 99) // 100))

    summary = {
        "record_id": "MPSEF_P3_V1_STAGE1_V1",
        "status": "SOURCE_ONLY_PROPOSALS_COMPLETE",
        "proposer_id": PROPOSER_ID,
        "proposer_version": PROPOSER_VERSION,
        "family_id": FAMILY_ID,
        "packet_sha256": EXPECTED_PACKET_SHA256,
        "p1_parent_proposal_sha256": EXPECTED_P1_PROPOSAL_SHA256,
        "registry_sha256": EXPECTED_REGISTRY_SHA256,
        "pnx_revision": EXPECTED_PNX_REVISION,
        "pnx_weight_sha256": weight_sha,
        "pnx_config_sha256": cfg_sha,
        "cases": len(out_rows),
        "clusters": len({r["cluster_id"] for r in out_rows}),
        "execution_ok": sum(r["execution_state"] == "OK" for r in out_rows),
        "execution_failures": failures,
        "identical_to_p1_count": identical_parent,
        "changed_from_p1_count": changed,
        "stage_b_domain_counts": domains,
        "batch_single_parity_n": PARITY_N,
        "batch_single_parity_match": PARITY_N,
        "batch_size": args.batch_size,
        "runtime_seconds_total_batch_pass": time.monotonic() - started,
        "runtime_seconds_mean_per_case_allocated": statistics.mean(runtimes),
        "runtime_seconds_median_per_case_allocated": statistics.median(runtimes),
        "runtime_seconds_p95_nearest_rank_allocated": ordered[rank - 1],
        "max_rss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "project_source_loaded": True,
        "project_source_scope": "FROZEN_STAGE1_128_ONLY",
        "gold_reference_consulted": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "quality_claimed": False,
        "p1_rerun": False,
        "exact_frozen_p1_parent_reused": True,
    }

    Path(args.out_prefix + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    update_state(
        progress_path,
        "MPSEF_P3_V1_STAGE1_V1",
        "COMPLETE",
        total_work,
        total_work,
        status="COMPLETE",
        message="P3 Stage1 source-only proposals complete",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
