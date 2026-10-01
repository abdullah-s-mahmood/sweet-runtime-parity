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
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

from mpsef_p2_v2_real_model_stage0 import (
    EXPECTED_GED_WEIGHT_SHA,
    EXPECTED_GEC_WEIGHT_SHA,
    Stage0Error,
    generate_with_ged_hook,
    infer_word_level_ged,
    morph_words,
    project_to_gec,
    sha256_file,
    sha_json,
)

VERSION = "MPSEF_P2_V2_STAGE1_RUNNER_V1"
PROPOSER_ID = "P2_V2_ARABART_GED_MORPH_WORDALIGNED"
PROPOSER_VERSION = "P2_V2_1"
FAMILY_ID = "SEQ2SEQ_GED_MORPH"
ANCESTRY_ID = "ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR"

EXPECTED_PACKET_SHA256 = "8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1"
EXPECTED_UID_LIST_SHA256 = "e32b468f27653a1bbabfa5c355483c34ffe9b6e4cb2425c36e6c10b714c104ac"
EXPECTED_CLUSTER_LIST_SHA256 = "95b895d424d404d80a70b5acb8ac8b98fe8b461f8b03c2532a7535853f9a25ca"
EXPECTED_REGISTRY_SHA256 = "b448650c571f6c93dffe4825417e4f65d6a8cd02e33bd9551728ceac2b242b1a"
EXPECTED_CASES = 128
EXPECTED_CLUSTERS = 128
PARITY_N = 8


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def load_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def terminal_state_from_exception(exc: Exception):
    s = str(exc)
    if "ZERO_TOKEN" in s or "TOKEN" in s and "UNKNOWN" not in s:
        return "TOKENIZATION_FAILED"
    if "WORD_" in s or "GED_WORD" in s or "MORPH_" in s:
        return "WORD_IDENTITY_FAILED"
    if "INPUT_TOO_LONG" in s or "OVER_BUDGET" in s or "CEILING" in s:
        return "TRUNCATED_OR_LENGTH_UNPROVEN"
    if "EOS" in s or "GENERATION" in s:
        return "GENERATION_INCOMPLETE"
    if "GED_TAG" in s or "EMBEDDING" in s:
        return "MODEL_INTERFACE_UNPROVEN"
    return "EXECUTION_FAILED"


def build_models(args):
    ged_weight = sha256_file(Path(args.ged_model_dir) / "pytorch_model.bin")
    gec_weight = sha256_file(Path(args.gec_model_dir) / "pytorch_model.bin")
    if ged_weight != EXPECTED_GED_WEIGHT_SHA:
        raise RuntimeError(f"GED_WEIGHT_SHA_MISMATCH:{ged_weight}")
    if gec_weight != EXPECTED_GEC_WEIGHT_SHA:
        raise RuntimeError(f"GEC_WEIGHT_SHA_MISMATCH:{gec_weight}")

    ged_tokenizer = AutoTokenizer.from_pretrained(args.ged_model_dir)
    ged_model = BertForTokenClassification.from_pretrained(args.ged_model_dir)
    ged_model.eval()

    gec_tokenizer = AutoTokenizer.from_pretrained(args.gec_model_dir)
    gec_model = MBartForConditionalGeneration.from_pretrained(args.gec_model_dir)
    gec_model.eval()

    disambig = BERTUnfactoredDisambiguator.pretrained(
        model_name="msa", use_gpu=False, pretrained_cache=False
    )

    identities = {
        "ged_weight_sha256": ged_weight,
        "gec_weight_sha256": gec_weight,
        "ged_config_sha256": hashlib.sha256(
            ged_model.config.to_json_string().encode()
        ).hexdigest(),
        "gec_config_sha256": hashlib.sha256(
            gec_model.config.to_json_string().encode()
        ).hexdigest(),
        "ged_id2label_sha256": sha_json(
            {str(k): v for k, v in ged_model.config.id2label.items()}
        ),
        "ged_label2id_sha256": sha_json(
            {str(k): int(v) for k, v in ged_model.config.label2id.items()}
        ),
        "gec_ged_label2id_sha256": sha_json(
            {str(k): int(v) for k, v in gec_model.config.ged_label2id.items()}
        ),
        "ged_tokenizer_class": type(ged_tokenizer).__name__,
        "gec_tokenizer_class": type(gec_tokenizer).__name__,
        "ged_vocab_size": len(ged_tokenizer),
        "gec_vocab_size": len(gec_tokenizer),
        "gec_has_embed_ged_tags": hasattr(
            gec_model.model.encoder, "embed_ged_tags"
        ),
    }
    if not identities["gec_has_embed_ged_tags"]:
        raise RuntimeError("GEC_GED_EMBEDDING_LAYER_MISSING")

    return ged_tokenizer, ged_model, gec_tokenizer, gec_model, disambig, identities


def infer_one(row, models, include_trace=True):
    ged_tokenizer, ged_model, gec_tokenizer, gec_model, disambig, _ = models
    source = row["source"]
    started = time.monotonic()

    try:
        words = morph_words(disambig, source)
        labels, segments, ged_trace = infer_word_level_ged(
            words, ged_tokenizer, ged_model
        )
        prepared = project_to_gec(
            words, labels, gec_tokenizer, gec_model
        )
        gen = generate_with_ged_hook(
            gec_tokenizer, gec_model, prepared
        )

        output = gen["decoded_text"]
        if not isinstance(output, str):
            raise Stage0Error("P2V2_OUTPUT_NOT_STRING")
        if output == "":
            state = "EMPTY_OUTPUT"
            reasons = ["P2V2_EMPTY_OUTPUT"]
        else:
            state = "OK"
            reasons = []

        elapsed = time.monotonic() - started
        rec = {
            "registry_namespace": "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A",
            "proposer_id": PROPOSER_ID,
            "proposer_version": PROPOSER_VERSION,
            "family_id": FAMILY_ID,
            "ancestry_id": ANCESTRY_ID,
            "role": "HETEROGENEOUS_CANDIDATE",
            "uid": row["uid"],
            "case_id": row["case_id"],
            "cluster_id": row["cluster_id"],
            "source": source,
            "source_sha256": row["source_sha256"],
            "input_text": source,
            "input_sha256": row["source_sha256"],
            "parent_proposer_id": None,
            "parent_proposer_version": None,
            "parent_output_sha256": None,
            "full_proposer_output": output,
            "output_sha256": sha_text(output),
            "execution_state": state,
            "failure_reasons": reasons,
            "provenance_complete": True,
            "source_only": True,
            "gold_reference_consulted": False,
            "quality_scored": False,
            "morph_word_count": len(words),
            "ged_label_count": len(labels),
            "ged_segment_count": len(segments),
            "gec_input_length": len(prepared["input_ids"]),
            "gec_label_length": len(prepared["ged_label_ids"]),
            "generation_token_count": len(gen["generated_token_ids"]),
            "generation_hit_ceiling": gen["hit_ceiling"],
            "terminal_eos_index": gen["terminal_eos_index"],
            "decoder_prefix_equals_eos": gen["decoder_prefix_equals_eos"],
            "ged_embedding_hook_call_count": len(
                gen["ged_embedding_hook_calls"]
            ),
            "runtime_seconds": elapsed,
        }

        if include_trace:
            rec["morph_words"] = words
            rec["word_level_ged_labels"] = labels
            rec["ged_word_identity_trace"] = ged_trace
            rec["ged_segments"] = segments
            rec["gec_word_map"] = prepared["word_map"]
            rec["gec_input_ids_sha256"] = sha_json(prepared["input_ids"])
            rec["gec_ged_label_ids_sha256"] = sha_json(
                prepared["ged_label_ids"]
            )
            rec["generated_token_ids"] = gen["generated_token_ids"]
        return rec

    except Exception as exc:
        elapsed = time.monotonic() - started
        return {
            "registry_namespace": "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A",
            "proposer_id": PROPOSER_ID,
            "proposer_version": PROPOSER_VERSION,
            "family_id": FAMILY_ID,
            "ancestry_id": ANCESTRY_ID,
            "role": "HETEROGENEOUS_CANDIDATE",
            "uid": row["uid"],
            "case_id": row["case_id"],
            "cluster_id": row["cluster_id"],
            "source": source,
            "source_sha256": row["source_sha256"],
            "input_text": source,
            "input_sha256": row["source_sha256"],
            "parent_proposer_id": None,
            "parent_proposer_version": None,
            "parent_output_sha256": None,
            "full_proposer_output": None,
            "output_sha256": None,
            "execution_state": terminal_state_from_exception(exc),
            "failure_reasons": [
                f"{type(exc).__name__}:{str(exc)}"
            ],
            "provenance_complete": True,
            "source_only": True,
            "gold_reference_consulted": False,
            "quality_scored": False,
            "runtime_seconds": elapsed,
        }


def parity_signature(rec):
    keys = [
        "uid",
        "source_sha256",
        "execution_state",
        "output_sha256",
        "morph_word_count",
        "ged_label_count",
        "ged_segment_count",
        "gec_input_length",
        "gec_label_length",
        "generation_token_count",
        "generation_hit_ceiling",
        "terminal_eos_index",
        "decoder_prefix_equals_eos",
        "ged_embedding_hook_call_count",
        "gec_input_ids_sha256",
        "gec_ged_label_ids_sha256",
        "generated_token_ids",
        "word_level_ged_labels",
        "ged_word_identity_trace",
        "ged_segments",
        "gec_word_map",
    ]
    return {k: rec.get(k) for k in keys}


def progress_line(done, total, started, last_elapsed=None):
    elapsed = max(time.monotonic() - started, 1e-9)
    rate = done / elapsed
    remaining = total - done
    eta = remaining / rate if rate > 0 else None
    obj = {
        "type": "P2_V2_STAGE1_PROGRESS",
        "processed": done,
        "total": total,
        "percent": round(100.0 * done / total, 2),
        "elapsed_seconds": round(elapsed, 3),
        "rate_per_min": round(rate * 60.0, 3),
        "eta_seconds": None if eta is None else round(eta, 3),
        "last_case_seconds": None if last_elapsed is None else round(last_elapsed, 3),
    }
    print(json.dumps(obj, ensure_ascii=False), flush=True)


def run(args):
    packet_path = Path(args.packet)
    packet_sha = sha_bytes(packet_path.read_bytes())
    if packet_sha != EXPECTED_PACKET_SHA256:
        raise RuntimeError(f"PACKET_SHA_MISMATCH:{packet_sha}")

    rows = load_jsonl(packet_path)
    if len(rows) != EXPECTED_CASES:
        raise RuntimeError(f"PACKET_CASE_COUNT_MISMATCH:{len(rows)}")
    if len({r["uid"] for r in rows}) != EXPECTED_CASES:
        raise RuntimeError("PACKET_UID_UNIQUENESS_FAILED")
    if len({r["cluster_id"] for r in rows}) != EXPECTED_CLUSTERS:
        raise RuntimeError("PACKET_CLUSTER_UNIQUENESS_FAILED")
    for r in rows:
        if sha_text(r["source"]) != r["source_sha256"]:
            raise RuntimeError(f'{r["uid"]}:SOURCE_SHA_MISMATCH')

    models = build_models(args)
    identities = models[-1]

    # Fixed parity subset is the first PARITY_N UIDs in the already frozen,
    # UID-sorted packet. It is not selected from output behavior.
    parity_rows = rows[:PARITY_N]

    parity_first = [
        infer_one(r, models, include_trace=True)
        for r in parity_rows
    ]
    parity_repeat = [
        infer_one(r, models, include_trace=True)
        for r in parity_rows
    ]
    parity_reversed = {
        rec["uid"]: rec
        for rec in [
            infer_one(r, models, include_trace=True)
            for r in reversed(parity_rows)
        ]
    }

    repeat_matches = 0
    reorder_matches = 0
    for a, b in zip(parity_first, parity_repeat):
        if parity_signature(a) == parity_signature(b):
            repeat_matches += 1
    for a in parity_first:
        if parity_signature(a) == parity_signature(
            parity_reversed[a["uid"]]
        ):
            reorder_matches += 1

    if repeat_matches != PARITY_N:
        raise RuntimeError(
            f"P2V2_STAGE1_REPEAT_PARITY_FAILED:{repeat_matches}/{PARITY_N}"
        )
    if reorder_matches != PARITY_N:
        raise RuntimeError(
            f"P2V2_STAGE1_REORDER_PARITY_FAILED:{reorder_matches}/{PARITY_N}"
        )

    # The frozen P2_V2 inference implementation is single-case at model-call
    # level. No false "batch-vs-single" claim is made. Batch-mode parity is
    # NOT_APPLICABLE until a true batched implementation is introduced.
    batch_model_call_supported = False

    out_rows = []
    started = time.monotonic()
    case_times = []
    progress_line(0, len(rows), started)

    for idx, row in enumerate(rows, start=1):
        rec = infer_one(row, models, include_trace=True)
        out_rows.append(rec)
        case_times.append(float(rec["runtime_seconds"]))
        if idx == 1 or idx % args.progress_every == 0 or idx == len(rows):
            progress_line(
                idx, len(rows), started, rec["runtime_seconds"]
            )

    out_path = Path(args.out_prefix + ".jsonl")
    out_path.write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False, sort_keys=True)
            for r in out_rows
        ) + "\n",
        encoding="utf-8",
    )

    states = {}
    changed = 0
    empty = 0
    ceiling = 0
    for rec in out_rows:
        st = rec["execution_state"]
        states[st] = states.get(st, 0) + 1
        if rec.get("full_proposer_output") == "":
            empty += 1
        if (
            rec.get("full_proposer_output") is not None
            and rec["full_proposer_output"] != rec["source"]
        ):
            changed += 1
        if rec.get("generation_hit_ceiling") is True:
            ceiling += 1

    total_elapsed = time.monotonic() - started
    max_rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    summary = {
        "record_id": "MPSEF_P2_V2_STAGE1_V1",
        "status": "SOURCE_ONLY_PROPOSALS_COMPLETE",
        "proposer_id": PROPOSER_ID,
        "proposer_version": PROPOSER_VERSION,
        "family_id": FAMILY_ID,
        "packet_sha256": packet_sha,
        "registry_sha256": EXPECTED_REGISTRY_SHA256,
        "cases": len(out_rows),
        "clusters": len({r["cluster_id"] for r in out_rows}),
        "execution_states": states,
        "changed_vs_source_count": changed,
        "changed_vs_source_percent": round(100.0 * changed / len(out_rows), 4),
        "empty_output_count": empty,
        "generation_ceiling_count": ceiling,
        "parity_subset_n": PARITY_N,
        "repeat_parity_match": repeat_matches,
        "reorder_parity_match": reorder_matches,
        "true_model_batch_call_supported": batch_model_call_supported,
        "batch_vs_single_parity": "NOT_APPLICABLE_SINGLE_CASE_MODEL_CALL_IMPLEMENTATION",
        "runtime_seconds_total": total_elapsed,
        "runtime_seconds_mean": statistics.mean(case_times),
        "runtime_seconds_median": statistics.median(case_times),
        "runtime_seconds_p95_nearest_rank": sorted(case_times)[
            max(0, min(len(case_times)-1, math.ceil(0.95*len(case_times))-1))
        ] if False else None,
        "max_rss_kb": max_rss_kb,
        "identities": identities,
        "source_only": True,
        "project_source_loaded": True,
        "project_source_scope": "FROZEN_STAGE1_128_ONLY",
        "gold_reference_consulted": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "quality_claimed": False,
    }

    # p95 nearest-rank without importing math through hidden behavior.
    ordered_times = sorted(case_times)
    rank = max(1, int((95 * len(ordered_times) + 99) // 100))
    summary["runtime_seconds_p95_nearest_rank"] = ordered_times[rank - 1]

    summary_path = Path(args.out_prefix + "_SUMMARY.json")
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    parity_path = Path(args.out_prefix + "_PARITY.json")
    parity_path.write_text(
        json.dumps(
            {
                "packet_sha256": packet_sha,
                "parity_uids": [r["uid"] for r in parity_rows],
                "repeat_match": repeat_matches,
                "reorder_match": reorder_matches,
                "true_model_batch_call_supported": False,
                "batch_vs_single_parity": "NOT_APPLICABLE_SINGLE_CASE_MODEL_CALL_IMPLEMENTATION",
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--ged-model-dir", required=True)
    ap.add_argument("--gec-model-dir", required=True)
    ap.add_argument("--out-prefix", default="MPSEF_P2_V2_STAGE1_V1")
    ap.add_argument("--progress-every", type=int, default=8)
    args = ap.parse_args()
    run(args)


if __name__ == "__main__":
    main()
