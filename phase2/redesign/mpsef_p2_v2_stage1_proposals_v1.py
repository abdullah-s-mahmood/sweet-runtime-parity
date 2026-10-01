#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

from mpsef_p2_v2_real_model_stage0 import (
    EXPECTED_GED_WEIGHT_SHA,
    EXPECTED_GEC_WEIGHT_SHA,
    Stage0Error,
    sha256_file,
    sha_json,
    morph_words,
    infer_word_level_ged,
    project_to_gec,
    generate_with_ged_hook,
)
from process_progress_v1 import update_state

VERSION = "MPSEF_V4_P2_V2_STAGE1_RUNNER_V1"
PROPOSER_ID = "P2_V2_ARABART_GED_MORPH_WORDALIGNED"
PROPOSER_VERSION = "P2_V2_1"
FAMILY_ID = "SEQ2SEQ_GED_MORPH"
ANCESTRY_ID = "ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"
EXPECTED_PACKET_CASES = 128


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def classify_failure(exc: Exception) -> tuple[str, str]:
    msg = str(exc)
    if any(k in msg for k in (
        "ZERO_TOKEN_WORD",
        "GED_ZERO_TOKEN_WORD",
        "GEC_ZERO_TOKEN_WORD",
    )):
        return "TOKENIZATION_FAILED", msg
    if any(k in msg for k in (
        "WORD_IDENTITY",
        "WORD_BIJECTION",
        "WORD_COVERAGE",
        "WORD_LABEL_COUNT",
        "DUPLICATE_WORD",
        "MORPH_COUNT",
        "MORPH_OUTPUT_COUNT",
    )):
        return "WORD_IDENTITY_FAILED", msg
    if any(k in msg for k in (
        "OVER_BUDGET",
        "INPUT_TOO_LONG",
        "SEGMENT_OVERFLOW",
        "SEGMENT_FIELD_LENGTH",
    )):
        return "TRUNCATED_OR_LENGTH_UNPROVEN", msg
    if any(k in msg for k in (
        "TERMINAL_EOS",
        "GENERATION_CEILING",
        "EMPTY_GENERATION",
    )):
        return "GENERATION_INCOMPLETE", msg
    if any(k in msg for k in (
        "GED_TAGS_NOT_CONSUMED",
        "GED_EMBEDDING_LAYER_MISSING",
        "GED_TAG_INTERFACE_UNPROVEN",
    )):
        return "MODEL_INTERFACE_UNPROVEN", msg
    if "SHA_MISMATCH" in msg:
        return "RUNTIME_IDENTITY_MISMATCH", msg
    return "EXECUTION_FAILED", f"{type(exc).__name__}:{msg}"


def validate_packet(rows):
    if len(rows) != EXPECTED_PACKET_CASES:
        raise RuntimeError(f"packet case count mismatch: {len(rows)}")
    if len({r["uid"] for r in rows}) != EXPECTED_PACKET_CASES:
        raise RuntimeError("packet duplicate UID")
    if len({r["cluster_id"] for r in rows}) != EXPECTED_PACKET_CASES:
        raise RuntimeError("packet cluster count/uniqueness failure")
    for r in rows:
        if r.get("role") != "C_F":
            raise RuntimeError(f'{r.get("uid")}: non-C_F packet row')
        if sha_text(r["source"]) != r["source_sha256"]:
            raise RuntimeError(f'{r["uid"]}: packet source SHA mismatch')


def run(args):
    packet_path = Path(args.packet)
    rows = read_jsonl(packet_path)
    validate_packet(rows)

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

    state_path = Path(args.progress_state)
    started = time.time()
    out_rows = []
    counts = Counter()

    update_state(
        state_path, VERSION, "P2_V2_STAGE1", 0, len(rows),
        "RUNNING", "models loaded; proposal generation starting"
    )

    for idx, row in enumerate(rows, start=1):
        source = row["source"]
        rec = {
            "record_id": "MPSEF_V4_P2_V2_STAGE1_PROPOSAL_V1",
            "registry_namespace": REGISTRY_NAMESPACE,
            "proposer_id": PROPOSER_ID,
            "proposer_version": PROPOSER_VERSION,
            "family_id": FAMILY_ID,
            "ancestry_id": ANCESTRY_ID,
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
            "source_only": True,
            "gold_reference_consulted": False,
            "quality_scored": False,
            "raw_execution_state": None,
            "failure_reasons": [],
            "full_proposer_output": None,
            "output_sha256": None,
            "trace": None,
            "runtime_identity": identities,
            "legalizer_status": "NOT_RUN",
            "protected_touch": None,
            "protection_reasons": [],
            "provenance_complete": False,
        }

        try:
            words = morph_words(disambig, source)
            labels, segments, ged_trace = infer_word_level_ged(
                words, ged_tokenizer, ged_model
            )
            if len(labels) != len(words):
                raise Stage0Error("REAL_GED_WORD_LABEL_COUNT_MISMATCH")
            prepared = project_to_gec(
                words, labels, gec_tokenizer, gec_model
            )
            generation = generate_with_ged_hook(
                gec_tokenizer, gec_model, prepared
            )
            output = generation["decoded_text"]

            if not isinstance(output, str):
                raise Stage0Error("GEC_OUTPUT_NOT_STRING")
            if output == "":
                state = "EMPTY_OUTPUT"
                reasons = ["EMPTY_OUTPUT"]
            else:
                state = "OK"
                reasons = []

            rec.update({
                "raw_execution_state": state,
                "failure_reasons": reasons,
                "full_proposer_output": output,
                "output_sha256": sha_text(output),
                "trace": {
                    "morph_words": words,
                    "morph_word_count": len(words),
                    "word_level_ged_labels": labels,
                    "ged_label_count": len(labels),
                    "ged_segments": segments,
                    "ged_word_identity_trace": ged_trace,
                    "gec_word_map": prepared["word_map"],
                    "gec_input_ids_sha256": sha_json(prepared["input_ids"]),
                    "gec_ged_label_ids_sha256": sha_json(
                        prepared["ged_label_ids"]
                    ),
                    "gec_input_length": len(prepared["input_ids"]),
                    "gec_label_length": len(prepared["ged_label_ids"]),
                    "generation": generation,
                },
                "provenance_complete": True,
            })
        except Exception as exc:
            state, reason = classify_failure(exc)
            rec.update({
                "raw_execution_state": state,
                "failure_reasons": [reason],
                "provenance_complete": True,
            })

        counts[rec["raw_execution_state"]] += 1
        out_rows.append(rec)

        if idx == 1 or idx % args.progress_every == 0 or idx == len(rows):
            update_state(
                state_path, VERSION, "P2_V2_STAGE1", idx, len(rows),
                "RUNNING" if idx < len(rows) else "COMPLETE",
                f'last_uid={row["uid"]}; state={rec["raw_execution_state"]}'
            )

    if len(out_rows) != len(rows):
        raise RuntimeError("proposal accounting mismatch")
    if {r["uid"] for r in out_rows} != {r["uid"] for r in rows}:
        raise RuntimeError("proposal UID accounting mismatch")

    out_path = Path(args.out_prefix + ".jsonl")
    out_path.write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False, sort_keys=True)
            for r in out_rows
        ) + "\n",
        encoding="utf-8",
    )

    elapsed = time.time() - started
    summary = {
        "record_id": "MPSEF_V4_P2_V2_STAGE1_PROPOSALS_V1",
        "runner_version": VERSION,
        "status": "SOURCE_ONLY_PROPOSALS_READY",
        "cases": len(out_rows),
        "clusters": len({r["cluster_id"] for r in out_rows}),
        "state_counts": dict(sorted(counts.items())),
        "packet_sha256": hashlib.sha256(packet_path.read_bytes()).hexdigest(),
        "proposal_artifact_sha256": hashlib.sha256(
            out_path.read_bytes()
        ).hexdigest(),
        "runtime_identity": identities,
        "elapsed_seconds": elapsed,
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
    ap.add_argument("--ged-model-dir", required=True)
    ap.add_argument("--gec-model-dir", required=True)
    ap.add_argument(
        "--out-prefix",
        default="MPSEF_V4_P2_V2_STAGE1_PROPOSALS_V1",
    )
    ap.add_argument(
        "--progress-state",
        default="MPSEF_V4_P2_V2_STAGE1_PROGRESS.json",
    )
    ap.add_argument("--progress-every", type=int, default=4)
    args = ap.parse_args()
    run(args)


if __name__ == "__main__":
    main()
