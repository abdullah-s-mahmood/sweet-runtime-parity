#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

from transformers import BertForTokenClassification, BertTokenizer

from mpsef_p1_cf_proposals_v1 import (
    install_rewrite_compat,
    infer_pass,
    sha256_file,
)
from process_progress_v1 import update_state

VERSION = "MPSEF_V4_P3_V1_STAGE1_RUNNER_V1"
PROPOSER_ID = "P3_V1_SWEET_NOPNX2_PNX1"
PROPOSER_VERSION = "P3_V1_1"
FAMILY_ID = "SWEET_QALB14"
ANCESTRY_ID = "P1_CONTROL_PLUS_PNX1"
PARENT_ID = "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2"
PARENT_VERSION = "P1_FROZEN_V1"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"
EXPECTED_PACKET_CASES = 128
PARITY_N = 32
PARITY_SALT = "MPSEF-V4-STAGE1-PARITY-32-20261001-A"


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def parity_rank(uid: str) -> str:
    return sha_text(PARITY_SALT + "|" + uid)


def validate_packet(rows):
    if len(rows) != EXPECTED_PACKET_CASES:
        raise RuntimeError(f"packet case count mismatch: {len(rows)}")
    if len({r["uid"] for r in rows}) != EXPECTED_PACKET_CASES:
        raise RuntimeError("packet duplicate UID")
    if len({r["cluster_id"] for r in rows}) != EXPECTED_PACKET_CASES:
        raise RuntimeError("packet cluster uniqueness failure")
    for r in rows:
        if r.get("role") != "C_F":
            raise RuntimeError(f'{r.get("uid")}: non-C_F packet row')
        if sha_text(r["source"]) != r["source_sha256"]:
            raise RuntimeError(f'{r["uid"]}: packet source SHA mismatch')


def index_parent_rows(parent_rows):
    out = {}
    for r in parent_rows:
        uid = r["uid"]
        if uid in out:
            raise RuntimeError(f"duplicate P1 parent UID: {uid}")
        out[uid] = r
    return out


def run(args):
    packet_path = Path(args.packet)
    packet = read_jsonl(packet_path)
    validate_packet(packet)

    parent_rows = read_jsonl(Path(args.p1_proposals))
    parents = index_parent_rows(parent_rows)

    model_weight_sha = sha256_file(Path(args.pnx_model_dir) / "pytorch_model.bin")
    if model_weight_sha != args.expected_pnx_weight_sha:
        raise RuntimeError(
            f"PNX_WEIGHT_SHA_MISMATCH:{model_weight_sha}"
        )

    rewrite = install_rewrite_compat(Path(args.upstream_root))
    tokenizer = BertTokenizer.from_pretrained(args.pnx_model_dir)
    model = BertForTokenClassification.from_pretrained(args.pnx_model_dir)
    model.eval()

    identities = {
        "pnx_model_revision": args.expected_pnx_revision,
        "pnx_weight_sha256": model_weight_sha,
        "upstream_text_editing_revision": args.expected_upstream_revision,
        "pnx_config_sha256": hashlib.sha256(
            model.config.to_json_string().encode()
        ).hexdigest(),
        "pnx_tokenizer_class": type(tokenizer).__name__,
        "pnx_vocab_size": len(tokenizer),
        "decode_iter": 1,
    }

    state_path = Path(args.progress_state)
    update_state(
        state_path, VERSION, "P3_V1_STAGE1", 0, len(packet),
        "RUNNING", "Pnx model loaded; parent-bound cascade starting"
    )

    out_rows = []
    counts = Counter()
    started = time.time()

    for idx, row in enumerate(packet, start=1):
        uid = row["uid"]
        rec = {
            "record_id": "MPSEF_V4_P3_V1_STAGE1_PROPOSAL_V1",
            "registry_namespace": REGISTRY_NAMESPACE,
            "proposer_id": PROPOSER_ID,
            "proposer_version": PROPOSER_VERSION,
            "family_id": FAMILY_ID,
            "ancestry_id": ANCESTRY_ID,
            "uid": uid,
            "case_id": row["case_id"],
            "cluster_id": row["cluster_id"],
            "source": row["source"],
            "source_sha256": row["source_sha256"],
            "parent_proposer_id": PARENT_ID,
            "parent_proposer_version": PARENT_VERSION,
            "parent_output_sha256": None,
            "input_text": None,
            "input_sha256": None,
            "raw_execution_state": None,
            "failure_reasons": [],
            "full_proposer_output": None,
            "output_sha256": None,
            "trace": None,
            "runtime_identity": identities,
            "source_only": True,
            "gold_reference_consulted": False,
            "quality_scored": False,
            "legalizer_status": "NOT_RUN",
            "protected_touch": None,
            "protection_reasons": [],
            "provenance_complete": False,
        }

        try:
            if uid not in parents:
                raise RuntimeError("P1_PARENT_UID_MISSING")
            p = parents[uid]
            if p["source_version_hash"] != row["source_sha256"]:
                raise RuntimeError("P1_PARENT_SOURCE_HASH_MISMATCH")
            if p["source"] != row["source"]:
                raise RuntimeError("P1_PARENT_SOURCE_TEXT_MISMATCH")
            if p.get("proposer_id") != "P1_SWEET_QALB14_NOPNX_ITER2":
                raise RuntimeError("P1_PARENT_PROPOSER_ID_MISMATCH")

            parent_output = p["full_proposer_output"]
            parent_hash = sha_text(parent_output)
            if parent_hash != p["output_sha256"]:
                raise RuntimeError("P1_PARENT_OUTPUT_HASH_MISMATCH")

            rec["parent_output_sha256"] = parent_hash
            rec["input_text"] = parent_output
            rec["input_sha256"] = parent_hash

            step = infer_pass(
                model, tokenizer, rewrite, [parent_output.split()]
            )[0]
            output = step["output"]
            if not isinstance(output, str):
                raise RuntimeError("PNX_OUTPUT_NOT_STRING")

            state = "EMPTY_OUTPUT" if output == "" else "OK"
            reasons = ["EMPTY_OUTPUT"] if state != "OK" else []
            rec.update({
                "raw_execution_state": state,
                "failure_reasons": reasons,
                "full_proposer_output": output,
                "output_sha256": sha_text(output),
                "trace": {
                    "parent_output_sha256": parent_hash,
                    "pnx_pass": 1,
                    "pnx_subwords": step["subwords"],
                    "pnx_labels": step["labels"],
                    "pnx_output": output,
                },
                "provenance_complete": True,
            })
        except Exception as exc:
            msg = f"{type(exc).__name__}:{str(exc)}"
            if "P1_PARENT" in msg:
                state = "INPUT_IDENTITY_FAILED"
            elif "token" in msg.lower():
                state = "TOKENIZATION_FAILED"
            else:
                state = "EXECUTION_FAILED"
            rec.update({
                "raw_execution_state": state,
                "failure_reasons": [msg],
                "provenance_complete": True,
            })

        counts[rec["raw_execution_state"]] += 1
        out_rows.append(rec)

        if idx == 1 or idx % args.progress_every == 0 or idx == len(packet):
            update_state(
                state_path, VERSION, "P3_V1_STAGE1", idx, len(packet),
                "RUNNING" if idx < len(packet) else "COMPLETE",
                f'last_uid={uid}; state={rec["raw_execution_state"]}'
            )

    # Frozen 32-UID parity subset: compare single outputs above to one
    # deterministic batch call. Only raw-execution OK rows can participate.
    parity_uids = [
        r["uid"]
        for r in sorted(packet, key=lambda x: (parity_rank(x["uid"]), x["uid"]))[:PARITY_N]
    ]
    by_uid = {r["uid"]: r for r in out_rows}
    parity_inputs = []
    parity_expected = []
    for uid in parity_uids:
        rec = by_uid[uid]
        if rec["raw_execution_state"] != "OK":
            raise RuntimeError(
                f"P3_PARITY_UID_NOT_EXECUTABLE:{uid}:{rec['raw_execution_state']}"
            )
        parity_inputs.append(rec["input_text"].split())
        parity_expected.append(rec)

    batch_steps = infer_pass(model, tokenizer, rewrite, parity_inputs)
    parity_matches = 0
    for uid, step, expected in zip(parity_uids, batch_steps, parity_expected):
        if step["output"] != expected["full_proposer_output"]:
            raise RuntimeError(f"P3_SINGLE_BATCH_PARITY_FAILED:{uid}")
        if step["subwords"] != expected["trace"]["pnx_subwords"]:
            raise RuntimeError(f"P3_SINGLE_BATCH_SUBWORD_PARITY_FAILED:{uid}")
        if step["labels"] != expected["trace"]["pnx_labels"]:
            raise RuntimeError(f"P3_SINGLE_BATCH_LABEL_PARITY_FAILED:{uid}")
        parity_matches += 1

    if parity_matches != PARITY_N:
        raise RuntimeError("P3_PARITY_COUNT_MISMATCH")

    out_path = Path(args.out_prefix + ".jsonl")
    out_path.write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False, sort_keys=True)
            for r in out_rows
        ) + "\n",
        encoding="utf-8",
    )

    summary = {
        "record_id": "MPSEF_V4_P3_V1_STAGE1_PROPOSALS_V1",
        "runner_version": VERSION,
        "status": "SOURCE_ONLY_PROPOSALS_READY",
        "cases": len(out_rows),
        "clusters": len({r["cluster_id"] for r in out_rows}),
        "state_counts": dict(sorted(counts.items())),
        "packet_sha256": hashlib.sha256(packet_path.read_bytes()).hexdigest(),
        "parent_artifact_sha256": hashlib.sha256(
            Path(args.p1_proposals).read_bytes()
        ).hexdigest(),
        "proposal_artifact_sha256": hashlib.sha256(
            out_path.read_bytes()
        ).hexdigest(),
        "runtime_identity": identities,
        "parity_salt": PARITY_SALT,
        "parity_n": PARITY_N,
        "parity_match": parity_matches,
        "elapsed_seconds": time.time() - started,
        "project_source_loaded": True,
        "project_source_scope": "C_F_STAGE1_SOURCE_ONLY",
        "project_gold_loaded": False,
        "reference_content_used": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "legalizer_run": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
        "reserved_data_opened": False,
    }
    Path(args.out_prefix + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--p1-proposals", required=True)
    ap.add_argument("--pnx-model-dir", required=True)
    ap.add_argument("--upstream-root", required=True)
    ap.add_argument("--expected-pnx-revision", required=True)
    ap.add_argument("--expected-pnx-weight-sha", required=True)
    ap.add_argument("--expected-upstream-revision", required=True)
    ap.add_argument(
        "--out-prefix",
        default="MPSEF_V4_P3_V1_STAGE1_PROPOSALS_V1",
    )
    ap.add_argument(
        "--progress-state",
        default="MPSEF_V4_P3_V1_STAGE1_PROGRESS.json",
    )
    ap.add_argument("--progress-every", type=int, default=8)
    args = ap.parse_args()
    run(args)


if __name__ == "__main__":
    main()
