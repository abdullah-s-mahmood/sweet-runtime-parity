#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import tempfile
import time
from pathlib import Path

import torch

from process_progress_v1 import update_state
from mpsef_p2_v2_stage1_v1 import build_models, terminal_state_from_exception
from mpsef_p2_v2_real_model_stage0 import (
    Stage0Error,
    build_ged_segments,
    inspect_generation_config,
    morph_words,
    project_to_gec,
    sha_json,
)

VERSION = "MPSEF_P2_V2_STAGE2_PRODUCTION_ADAPTER_V1"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"
PROPOSER_ID = "P2_V2_ARABART_GED_MORPH_WORDALIGNED"
PROPOSER_VERSION = "P2_V2_1"
FAMILY_ID = "SEQ2SEQ_GED_MORPH"
ANCESTRY_ID = "ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR"

STAGES = [
    "SOURCE_IDENTITY",
    "MORPH_ANALYSIS",
    "GED_TOKENIZATION",
    "GED_WORD_IDENTITY",
    "GED_INFERENCE",
    "GEC_PROJECTION",
    "GEC_TOKENIZATION",
    "GENERATION",
    "OUTPUT_DECODE",
]
ALLOWED_STAGE_STATUS = {"PASS", "FAIL", "NOT_REACHED", "UNKNOWN"}

_TERMINATION_REQUESTED = False


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def append_jsonl_durable(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())


def load_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def new_stage_status():
    return {stage: "NOT_REACHED" for stage in STAGES}


def assert_stage_status(stage_status):
    if set(stage_status) != set(STAGES):
        raise RuntimeError("P2_STAGE2_STAGE_LEDGER_KEYS_INVALID")
    bad = {
        k: v for k, v in stage_status.items()
        if v not in ALLOWED_STAGE_STATUS
    }
    if bad:
        raise RuntimeError(f"P2_STAGE2_STAGE_LEDGER_VALUES_INVALID:{bad}")


def stage_fail(stage_status, stage):
    if stage not in stage_status:
        raise RuntimeError(f"P2_STAGE2_UNKNOWN_STAGE:{stage}")
    stage_status[stage] = "FAIL"


def stage_pass(stage_status, stage):
    if stage not in stage_status:
        raise RuntimeError(f"P2_STAGE2_UNKNOWN_STAGE:{stage}")
    stage_status[stage] = "PASS"


def _signal_handler(signum, frame):
    global _TERMINATION_REQUESTED
    _TERMINATION_REQUESTED = True


def install_signal_handlers():
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)


def infer_ged_with_preserved_segments(words, tokenizer, model, segments):
    by_word = {}
    trace = []
    logits_shapes = []

    def attach_and_raise(exc):
        evidence = {
            "partial_ged_word_identity_trace": sorted(
                trace, key=lambda x: x["morph_word_index"]
            ),
            "partial_ged_logits_shapes": list(logits_shapes),
            "partial_ged_word_labels_by_index": {
                str(k): v for k, v in sorted(by_word.items())
            },
        }
        setattr(exc, "p2_stage2_ged_evidence", evidence)
        raise exc

    try:
        with torch.no_grad():
            for seg in segments:
                ids = torch.tensor([seg["input_ids"]], dtype=torch.long)
                mask = torch.tensor([seg["attention_mask"]], dtype=torch.long)
                types = torch.tensor([seg["token_type_ids"]], dtype=torch.long)
                logits = model(
                    input_ids=ids,
                    attention_mask=mask,
                    token_type_ids=types,
                ).logits[0]
                logits_shapes.append(list(logits.shape))
                pred_ids = logits.argmax(dim=-1).tolist()
                if len(pred_ids) != len(seg["input_ids"]):
                    attach_and_raise(
                        Stage0Error("GED_LOGIT_LENGTH_MISMATCH")
                    )

                for wr in seg["word_records"]:
                    wi = wr["morph_word_index"]
                    if wi in by_word:
                        attach_and_raise(
                            Stage0Error(
                                f"GED_DUPLICATE_WORD_INDEX:{wi}"
                            )
                        )
                    p = wr["ged_first_wordpiece_index"]
                    if seg["label_mask"][p] == -100:
                        attach_and_raise(
                            Stage0Error("GED_FIRST_WORDPIECE_MASKED")
                        )
                    for q in range(
                        wr["ged_wordpiece_start"] + 1,
                        wr["ged_wordpiece_end"],
                    ):
                        if seg["label_mask"][q] != -100:
                            attach_and_raise(
                                Stage0Error(
                                    "GED_NONFIRST_WORDPIECE_UNMASKED"
                                )
                            )
                    pid = int(pred_ids[p])
                    label = model.config.id2label[pid]
                    by_word[wi] = label
                    trace.append({
                        **wr,
                        "ged_prediction_position": p,
                        "ged_label_id": pid,
                        "ged_label_name": label,
                    })
    except Stage0Error:
        raise
    except Exception as exc:
        attach_and_raise(exc)

    if set(by_word) != set(range(len(words))):
        attach_and_raise(
            Stage0Error(
                f"GED_WORD_COVERAGE_FAILED:{sorted(by_word)}"
            )
        )

    labels = [by_word[i] for i in range(len(words))]
    trace = sorted(trace, key=lambda x: x["morph_word_index"])
    for i, rec in enumerate(trace):
        if (
            rec["morph_word_index"] != i
            or rec["morph_word_text"] != words[i]
        ):
            attach_and_raise(
                Stage0Error(
                    "GED_WORD_IDENTITY_ORDER_OR_TEXT_MISMATCH"
                )
            )

    return labels, trace, logits_shapes


def generate_with_evidence(tokenizer, model, prepared):
    encoder = model.model.encoder
    if not hasattr(encoder, "embed_ged_tags"):
        raise Stage0Error("GEC_GED_EMBEDDING_LAYER_MISSING")

    cfg = inspect_generation_config(model, tokenizer)
    evidence = {
        "effective_generation_config": cfg,
        "generated_token_ids": None,
        "generation_token_count": None,
        "terminal_eos_index": None,
        "generation_hit_ceiling": None,
        "decoder_prefix_equals_eos": (
            cfg["decoder_start_token_id"] == cfg["eos_token_id"]
        ),
        "ged_embedding_hook_calls": [],
    }

    hook_calls = []

    def hook(module, inputs, output):
        hook_calls.append({
            "input_shape": (
                list(inputs[0].shape) if inputs else None
            ),
            "output_shape": list(output.shape),
        })

    handle = encoder.embed_ged_tags.register_forward_hook(hook)
    try:
        with torch.no_grad():
            generated = model.generate(
                torch.tensor(
                    [prepared["input_ids"]], dtype=torch.long
                ),
                num_beams=cfg["num_beams"],
                max_length=cfg["max_length"],
                num_return_sequences=cfg["num_return_sequences"],
                no_repeat_ngram_size=cfg["no_repeat_ngram_size"],
                early_stopping=cfg["early_stopping"],
                ged_tags=torch.tensor(
                    [prepared["ged_label_ids"]], dtype=torch.long
                ),
                attention_mask=torch.tensor(
                    [prepared["attention_mask"]], dtype=torch.long
                ),
            )
    except Exception as exc:
        evidence["ged_embedding_hook_calls"] = hook_calls
        setattr(exc, "p2_stage2_generation_evidence", evidence)
        raise
    finally:
        handle.remove()

    raw = generated[0].tolist()
    evidence["generated_token_ids"] = raw
    evidence["generation_token_count"] = len(raw)
    evidence["ged_embedding_hook_calls"] = hook_calls

    if not hook_calls:
        exc = Stage0Error(
            "GEC_GED_TAGS_NOT_CONSUMED_DURING_GENERATE"
        )
        setattr(exc, "p2_stage2_generation_evidence", evidence)
        raise exc

    prefix_len = 1
    eos = cfg["eos_token_id"]
    body = raw[prefix_len:]
    eos_positions = [
        i + prefix_len
        for i, tok in enumerate(body)
        if tok == eos
    ]
    hit_ceiling = len(raw) >= cfg["max_length"]
    evidence["generation_hit_ceiling"] = hit_ceiling

    if not eos_positions:
        exc = Stage0Error("GEC_TERMINAL_EOS_UNPROVEN")
        setattr(exc, "p2_stage2_generation_evidence", evidence)
        raise exc

    terminal = eos_positions[0]
    evidence["terminal_eos_index"] = terminal

    if hit_ceiling and terminal == len(raw) - 1:
        exc = Stage0Error(
            "GEC_EOS_AT_GENERATION_CEILING_FAIL_CLOSED"
        )
        setattr(exc, "p2_stage2_generation_evidence", evidence)
        raise exc

    return generated, evidence


def failure_stage_for_exception(exc, current_stage):
    text = str(exc)
    if "GEC_ZERO_TOKEN_WORD" in text:
        return "GEC_TOKENIZATION"
    if "GED_ZERO_TOKEN_WORD" in text:
        return "GED_TOKENIZATION"
    if (
        "GED_WORD" in text
        or "FIRST_WORDPIECE" in text
        or "NONFIRST_WORDPIECE" in text
        or "DUPLICATE_WORD_INDEX" in text
    ):
        return "GED_WORD_IDENTITY"
    if "GED_LOGIT" in text:
        return "GED_INFERENCE"
    if (
        "GEC_WORD_LABEL" in text
        or "UNKNOWN_GED_LABEL" in text
        or "CONDITIONING_LENGTH" in text
        or "INPUT_TOO_LONG" in text
    ):
        return "GEC_PROJECTION"
    if (
        "EOS" in text
        or "GENERATION" in text
        or "GED_TAGS_NOT_CONSUMED" in text
        or "GED_EMBEDDING" in text
    ):
        return "GENERATION"
    return current_stage


def base_record(row):
    return {
        "record_id": "MPSEF_P2_V2_STAGE2_PROPOSAL_V1",
        "adapter_version": VERSION,
        "registry_namespace": REGISTRY_NAMESPACE,
        "proposer_id": PROPOSER_ID,
        "proposer_version": PROPOSER_VERSION,
        "family_id": FAMILY_ID,
        "ancestry_id": ANCESTRY_ID,
        "role": "HETEROGENEOUS_CANDIDATE",
        "uid": row["uid"],
        "case_id": row["case_id"],
        "cluster_id": row["cluster_id"],
        "source": row["source"],
        "source_sha256": row["source_sha256"],
        "input_text": row["source"],
        "input_sha256": row["source_sha256"],
        "parent_proposer_id": None,
        "parent_proposer_version": None,
        "parent_output_sha256": None,
        "full_proposer_output": None,
        "output_sha256": None,
        "execution_state": "UNKNOWN_FAILURE",
        "failure_stage": None,
        "failure_reasons": [],
        "stage_status": new_stage_status(),
        "provenance_complete": True,
        "source_only": True,
        "gold_reference_consulted": False,
        "quality_scored": False,
        "morph_words": None,
        "morph_word_count": None,
        "morphology_sha256": None,
        "ged_segments": None,
        "ged_segment_count": None,
        "ged_word_identity_trace": None,
        "ged_logits_shapes": None,
        "word_level_ged_labels": None,
        "ged_label_count": None,
        "gec_word_map": None,
        "gec_input_ids_sha256": None,
        "gec_ged_label_ids_sha256": None,
        "gec_input_length": None,
        "gec_label_length": None,
        "effective_generation_config": None,
        "generated_token_ids": None,
        "generation_token_count": None,
        "terminal_eos_index": None,
        "generation_hit_ceiling": None,
        "decoder_prefix_equals_eos": None,
        "ged_embedding_hook_calls": None,
        "ged_embedding_hook_call_count": None,
        "partial_ged_word_identity_trace": None,
        "partial_ged_logits_shapes": None,
        "partial_ged_word_labels_by_index": None,
        "runtime_seconds": None,
    }


def apply_generation_evidence(rec, evidence):
    if not isinstance(evidence, dict):
        return
    for key in (
        "effective_generation_config",
        "generated_token_ids",
        "generation_token_count",
        "terminal_eos_index",
        "generation_hit_ceiling",
        "decoder_prefix_equals_eos",
        "ged_embedding_hook_calls",
    ):
        if key in evidence:
            rec[key] = evidence[key]
    if isinstance(rec.get("ged_embedding_hook_calls"), list):
        rec["ged_embedding_hook_call_count"] = len(
            rec["ged_embedding_hook_calls"]
        )


def run_one(row, models):
    (
        ged_tokenizer,
        ged_model,
        gec_tokenizer,
        gec_model,
        disambig,
        _identities,
    ) = models

    rec = base_record(row)
    started = time.monotonic()
    current_stage = "SOURCE_IDENTITY"

    try:
        if sha_text(row["source"]) != row["source_sha256"]:
            raise Stage0Error("SOURCE_SHA_MISMATCH")
        stage_pass(rec["stage_status"], "SOURCE_IDENTITY")

        current_stage = "MORPH_ANALYSIS"
        words = morph_words(disambig, row["source"])
        rec["morph_words"] = words
        rec["morph_word_count"] = len(words)
        rec["morphology_sha256"] = sha_json(words)
        stage_pass(rec["stage_status"], "MORPH_ANALYSIS")

        current_stage = "GED_TOKENIZATION"
        segments = build_ged_segments(words, ged_tokenizer)
        rec["ged_segments"] = segments
        rec["ged_segment_count"] = len(segments)
        stage_pass(rec["stage_status"], "GED_TOKENIZATION")

        current_stage = "GED_INFERENCE"
        labels, ged_trace, logits_shapes = (
            infer_ged_with_preserved_segments(
                words, ged_tokenizer, ged_model, segments
            )
        )
        rec["word_level_ged_labels"] = labels
        rec["ged_label_count"] = len(labels)
        rec["ged_word_identity_trace"] = ged_trace
        rec["ged_logits_shapes"] = logits_shapes
        stage_pass(rec["stage_status"], "GED_WORD_IDENTITY")
        stage_pass(rec["stage_status"], "GED_INFERENCE")

        current_stage = "GEC_PROJECTION"
        prepared = project_to_gec(
            words, labels, gec_tokenizer, gec_model
        )
        rec["gec_word_map"] = prepared["word_map"]
        rec["gec_input_ids_sha256"] = sha_json(
            prepared["input_ids"]
        )
        rec["gec_ged_label_ids_sha256"] = sha_json(
            prepared["ged_label_ids"]
        )
        rec["gec_input_length"] = len(prepared["input_ids"])
        rec["gec_label_length"] = len(
            prepared["ged_label_ids"]
        )
        stage_pass(rec["stage_status"], "GEC_TOKENIZATION")
        stage_pass(rec["stage_status"], "GEC_PROJECTION")

        current_stage = "GENERATION"
        generated, gen_evidence = generate_with_evidence(
            gec_tokenizer, gec_model, prepared
        )
        apply_generation_evidence(rec, gen_evidence)
        stage_pass(rec["stage_status"], "GENERATION")

        current_stage = "OUTPUT_DECODE"
        output = gec_tokenizer.batch_decode(
            generated,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]
        if not isinstance(output, str):
            raise Stage0Error("P2V2_OUTPUT_NOT_STRING")
        rec["full_proposer_output"] = output
        rec["output_sha256"] = sha_text(output)
        if output == "":
            rec["execution_state"] = "EMPTY_OUTPUT"
            rec["failure_reasons"] = ["P2V2_EMPTY_OUTPUT"]
        else:
            rec["execution_state"] = "OK"
        stage_pass(rec["stage_status"], "OUTPUT_DECODE")

    except Exception as exc:
        ged_evidence = getattr(
            exc, "p2_stage2_ged_evidence", None
        )
        if isinstance(ged_evidence, dict):
            rec["partial_ged_word_identity_trace"] = (
                ged_evidence.get("partial_ged_word_identity_trace")
            )
            rec["partial_ged_logits_shapes"] = (
                ged_evidence.get("partial_ged_logits_shapes")
            )
            rec["partial_ged_word_labels_by_index"] = (
                ged_evidence.get("partial_ged_word_labels_by_index")
            )
        evidence = getattr(
            exc, "p2_stage2_generation_evidence", None
        )
        apply_generation_evidence(rec, evidence)
        fail_stage = failure_stage_for_exception(
            exc, current_stage
        )
        rec["failure_stage"] = fail_stage
        if rec["stage_status"].get(fail_stage) != "PASS":
            stage_fail(rec["stage_status"], fail_stage)
        rec["execution_state"] = terminal_state_from_exception(exc)
        rec["failure_reasons"] = [
            f"{type(exc).__name__}:{str(exc)}"
        ]

    rec["runtime_seconds"] = time.monotonic() - started
    assert_stage_status(rec["stage_status"])
    return rec


def run(args):
    global _TERMINATION_REQUESTED
    _TERMINATION_REQUESTED = False
    install_signal_handlers()

    input_path = Path(args.input_jsonl)
    out_path = Path(args.out_jsonl)
    run_state_path = Path(args.run_state)
    progress_path = Path(args.progress_state)

    if out_path.exists() and out_path.stat().st_size > 0:
        raise RuntimeError(
            "P2_STAGE2_SILENT_RESUME_FORBIDDEN:"
            + str(out_path)
        )

    if args.expected_input_sha256:
        got = sha_file(input_path)
        if got != args.expected_input_sha256:
            raise RuntimeError(
                f"P2_STAGE2_INPUT_SHA_MISMATCH:{got}"
            )

    rows = load_jsonl(input_path)
    if len(rows) != args.expected_count:
        raise RuntimeError(
            f"P2_STAGE2_INPUT_COUNT_MISMATCH:{len(rows)}"
        )
    if len({r["uid"] for r in rows}) != len(rows):
        raise RuntimeError("P2_STAGE2_DUPLICATE_INPUT_UID")

    models = build_models(args)
    identities = models[-1]

    atomic_write_json(
        run_state_path,
        {
            "schema": "MPSEF_P2_V2_STAGE2_RUN_STATE_V1",
            "status": "RUNNING",
            "adapter_version": VERSION,
            "input_sha256": sha_file(input_path),
            "expected_count": args.expected_count,
            "durable_completed_count": 0,
            "current_uid": None,
            "current_index": None,
            "termination_requested": False,
            "model_identities": identities,
        },
    )
    update_state(
        progress_path,
        process_id=VERSION,
        stage="INITIALIZE",
        processed=0,
        total=len(rows),
        status="RUNNING",
        message="production adapter initialized",
    )

    for idx, row in enumerate(rows, start=1):
        if _TERMINATION_REQUESTED:
            atomic_write_json(
                run_state_path,
                {
                    **json.loads(
                        run_state_path.read_text(encoding="utf-8")
                    ),
                    "status": "INTERRUPTED_BEFORE_NEXT_UID",
                    "termination_requested": True,
                    "current_uid": None,
                    "current_index": None,
                },
            )
            raise SystemExit(143)

        state = json.loads(
            run_state_path.read_text(encoding="utf-8")
        )
        atomic_write_json(
            run_state_path,
            {
                **state,
                "status": "RUNNING_UID",
                "current_uid": row["uid"],
                "current_index": idx,
                "termination_requested": False,
            },
        )

        rec = run_one(row, models)
        append_jsonl_durable(out_path, rec)

        atomic_write_json(
            run_state_path,
            {
                **state,
                "status": "RUNNING",
                "current_uid": None,
                "current_index": None,
                "durable_completed_count": idx,
                "last_completed_uid": row["uid"],
                "termination_requested": _TERMINATION_REQUESTED,
            },
        )
        update_state(
            progress_path,
            process_id=VERSION,
            stage="PRODUCTION_INFERENCE",
            processed=idx,
            total=len(rows),
            status="RUNNING",
            message=(
                f'uid={row["uid"]} '
                f'state={rec["execution_state"]}'
            ),
        )

        if _TERMINATION_REQUESTED:
            current = json.loads(
                run_state_path.read_text(encoding="utf-8")
            )
            atomic_write_json(
                run_state_path,
                {
                    **current,
                    "status": "INTERRUPTED_AFTER_DURABLE_UID",
                    "termination_requested": True,
                },
            )
            raise SystemExit(143)

    output_rows = load_jsonl(out_path)
    if len(output_rows) != args.expected_count:
        raise RuntimeError(
            f"P2_STAGE2_TERMINAL_RECORD_COUNT_MISMATCH:"
            f"{len(output_rows)}"
        )
    if len({r["uid"] for r in output_rows}) != args.expected_count:
        raise RuntimeError(
            "P2_STAGE2_TERMINAL_UID_UNIQUENESS_FAILED"
        )
    if {r["uid"] for r in output_rows} != {
        r["uid"] for r in rows
    }:
        raise RuntimeError("P2_STAGE2_TERMINAL_UID_SET_MISMATCH")

    final_state = json.loads(
        run_state_path.read_text(encoding="utf-8")
    )
    atomic_write_json(
        run_state_path,
        {
            **final_state,
            "status": "COMPLETE",
            "durable_completed_count": args.expected_count,
            "current_uid": None,
            "current_index": None,
            "aborted_count": 0,
            "not_attempted_count": 0,
            "output_sha256": sha_file(out_path),
        },
    )
    update_state(
        progress_path,
        process_id=VERSION,
        stage="COMPLETE",
        processed=args.expected_count,
        total=args.expected_count,
        status="COMPLETE",
        message="all terminal records durable and validated",
    )

    summary = {
        "record_id": VERSION,
        "status": "COMPLETE",
        "input_sha256": sha_file(input_path),
        "output_sha256": sha_file(out_path),
        "cases": len(output_rows),
        "clusters": len({r["cluster_id"] for r in output_rows}),
        "state_counts": {},
        "failure_stage_counts": {},
        "model_identities": identities,
        "gold_reference_consulted": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
    }
    for rec in output_rows:
        st = rec["execution_state"]
        summary["state_counts"][st] = (
            summary["state_counts"].get(st, 0) + 1
        )
        fs = rec.get("failure_stage")
        if fs is not None:
            summary["failure_stage_counts"][fs] = (
                summary["failure_stage_counts"].get(fs, 0) + 1
            )

    if args.summary:
        atomic_write_json(Path(args.summary), summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-jsonl", required=True)
    ap.add_argument("--expected-count", type=int, required=True)
    ap.add_argument("--expected-input-sha256")
    ap.add_argument("--ged-model-dir", required=True)
    ap.add_argument("--gec-model-dir", required=True)
    ap.add_argument("--out-jsonl", required=True)
    ap.add_argument("--run-state", required=True)
    ap.add_argument("--progress-state", required=True)
    ap.add_argument("--summary")
    args = ap.parse_args()
    run(args)


if __name__ == "__main__":
    main()
