#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import torch
from transformers import AutoTokenizer, MBartForConditionalGeneration

sys.path.insert(0, str(Path(__file__).resolve().parent))
from process_progress_v1 import update_state

EXPECTED_CASES = 1918
EXPECTED_SOURCE_SHA = "051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_P2_SHA = "f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b"
EXPECTED_GEC_WEIGHT_SHA = "5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f"
TRACE_VERSION = "MPSEF_P2_GENERATION_TRACE_V1"
MAX_LENGTH = 100
NUM_BEAMS = 5

def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def first_eos_after_prefix(ids, decoder_start_token_id, eos_token_id):
    start = 1 if ids and ids[0] == decoder_start_token_id else 0
    for i in range(start, len(ids)):
        if ids[i] == eos_token_id:
            return i
    return None

def verify_stored_input(proposal, tokenizer, model):
    morph_words = proposal["morph_preprocessed_text"].split()
    labels = proposal["ged_labels"]
    stored_tokens = proposal["gec_subword_tokens"]
    input_ids = proposal["gec_input_ids"]
    label_ids = proposal["gec_ged_label_ids"]

    if len(morph_words) != len(labels):
        raise RuntimeError(f'{proposal["uid"]}: morph/GED count mismatch {len(morph_words)} != {len(labels)}')

    rebuilt_tokens = []
    per_word_piece_counts = []
    for word in morph_words:
        pieces = tokenizer.tokenize(word)
        per_word_piece_counts.append(len(pieces))
        if not pieces:
            raise RuntimeError(f'{proposal["uid"]}: tokenizer produced zero pieces for word {word!r}')
        rebuilt_tokens.extend(pieces)

    if rebuilt_tokens != stored_tokens:
        raise RuntimeError(f'{proposal["uid"]}: stored GEC subword tokens mismatch')

    rebuilt_input_ids = [
        tokenizer.bos_token_id,
        *tokenizer.convert_tokens_to_ids(rebuilt_tokens),
        tokenizer.eos_token_id,
    ]
    if rebuilt_input_ids != input_ids:
        raise RuntimeError(f'{proposal["uid"]}: stored GEC input IDs mismatch')

    if len(label_ids) != len(input_ids):
        raise RuntimeError(f'{proposal["uid"]}: GEC GED-label/input length mismatch')

    config_limit = getattr(model.config, "max_position_embeddings", None)
    tokenizer_limit = getattr(tokenizer, "model_max_length", None)
    finite_tok_limit = tokenizer_limit if isinstance(tokenizer_limit, int) and tokenizer_limit < 10**9 else None
    effective_limits = [x for x in (config_limit, finite_tok_limit) if isinstance(x, int) and x > 0]
    effective_limit = min(effective_limits) if effective_limits else None
    if effective_limit is not None and len(input_ids) > effective_limit:
        raise RuntimeError(
            f'{proposal["uid"]}: input length {len(input_ids)} exceeds model/tokenizer limit {effective_limit}'
        )

    return {
        "morph_word_count": len(morph_words),
        "ged_label_count": len(labels),
        "subword_count": len(stored_tokens),
        "per_word_piece_counts": per_word_piece_counts,
        "gec_input_length": len(input_ids),
        "gec_ged_label_length": len(label_ids),
        "model_max_position_embeddings": config_limit,
        "tokenizer_model_max_length": tokenizer_limit,
        "input_truncated": False,
        "input_truncation_proof": "MANUAL_FROZEN_INPUT_IDS_REBUILT_EXACTLY_AND_WITHIN_DECLARED_LIMIT",
    }

def generate_batch(tokenizer, model, proposals):
    pad_id = tokenizer.pad_token_id
    ged_pad_id = model.config.ged_label2id["<pad>"]
    max_in = max(len(x["gec_input_ids"]) for x in proposals)
    ids_batch, labels_batch, masks = [], [], []

    for p in proposals:
        n = len(p["gec_input_ids"])
        pad_n = max_in - n
        ids_batch.append(p["gec_input_ids"] + [pad_id] * pad_n)
        labels_batch.append(p["gec_ged_label_ids"] + [ged_pad_id] * pad_n)
        masks.append([1] * n + [0] * pad_n)

    with torch.no_grad():
        generated = model.generate(
            torch.tensor(ids_batch),
            num_beams=NUM_BEAMS,
            max_length=MAX_LENGTH,
            num_return_sequences=1,
            no_repeat_ngram_size=0,
            early_stopping=False,
            ged_tags=torch.tensor(labels_batch),
            attention_mask=torch.tensor(masks),
        )

    decoded = tokenizer.batch_decode(
        generated,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )
    return generated.tolist(), decoded

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--p2-proposals", required=True)
    ap.add_argument("--gec-model-dir", required=True)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--state-file", default="MPSEF_P2_GENERATION_TRACE_V1_PROGRESS.json")
    ap.add_argument("--out-prefix", default="MPSEF_P2_GENERATION_TRACE_V1")
    args = ap.parse_args()

    state_file = Path(args.state_file)
    update_state(state_file, TRACE_VERSION, "INITIALIZING", 0, EXPECTED_CASES)

    source_path = Path(args.source_manifest)
    prop_path = Path(args.p2_proposals)
    if sha256_file(source_path) != EXPECTED_SOURCE_SHA:
        raise RuntimeError("source manifest SHA mismatch")
    if sha256_file(prop_path) != EXPECTED_P2_SHA:
        raise RuntimeError("P2 proposal SHA mismatch")

    rows = read_jsonl(source_path)
    props = read_jsonl(prop_path)
    if len(rows) != EXPECTED_CASES or len(props) != EXPECTED_CASES:
        raise RuntimeError("population mismatch")
    source = {x["uid"]: x for x in rows}
    proposals = {x["uid"]: x for x in props}
    if set(source) != set(proposals):
        raise RuntimeError("UID-set mismatch")

    weight_sha = sha256_file(Path(args.gec_model_dir) / "pytorch_model.bin")
    if weight_sha != EXPECTED_GEC_WEIGHT_SHA:
        raise RuntimeError("GEC weight SHA mismatch")

    tokenizer = AutoTokenizer.from_pretrained(args.gec_model_dir)
    model = MBartForConditionalGeneration.from_pretrained(args.gec_model_dir)
    model.eval()

    cfg = model.config
    decoder_start = cfg.decoder_start_token_id
    eos = cfg.eos_token_id
    pad = cfg.pad_token_id
    forced_eos = getattr(cfg, "forced_eos_token_id", None)

    ordered = [proposals[uid] for uid in sorted(proposals)]
    static_checks = {}
    for p in ordered:
        uid = p["uid"]
        if p["source"] != source[uid]["source"]:
            raise RuntimeError(f"{uid}: source text mismatch")
        if p["source_version_hash"] != source[uid]["source_sha256"]:
            raise RuntimeError(f"{uid}: source hash mismatch")
        static_checks[uid] = verify_stored_input(p, tokenizer, model)

    out = []
    exact_output_matches = 0
    ceiling_count = 0
    missing_eos_count = 0

    update_state(state_file, TRACE_VERSION, "REGENERATING_FROZEN_P2_OUTPUTS", 0, EXPECTED_CASES)

    for start in range(0, len(ordered), args.batch_size):
        chunk = ordered[start:start + args.batch_size]
        token_ids_batch, decoded_batch = generate_batch(tokenizer, model, chunk)

        for p, token_ids, decoded in zip(chunk, token_ids_batch, decoded_batch):
            uid = p["uid"]
            decoded_sha = sha_text(decoded)
            if decoded_sha != p["output_sha256"] or decoded != p["full_proposer_output"]:
                raise RuntimeError(f"{uid}: regenerated output differs from frozen P2 proposal")

            exact_output_matches += 1
            eos_pos = first_eos_after_prefix(token_ids, decoder_start, eos)
            if eos_pos is None:
                missing_eos_count += 1
            effective_length = None if eos_pos is None else eos_pos + 1
            reached_ceiling = effective_length is None or effective_length >= MAX_LENGTH
            ceiling_count += int(reached_ceiling)

            s = static_checks[uid]
            out.append({
                "record_id": TRACE_VERSION,
                "uid": uid,
                "case_id": p["case_id"],
                "cluster_id": p["cluster_id"],
                "source_sha256": p["source_version_hash"],
                "output_sha256": p["output_sha256"],
                "decoder_start_token_id": decoder_start,
                "eos_token_id": eos,
                "pad_token_id": pad,
                "forced_eos_token_id": forced_eos,
                "generated_token_ids": token_ids,
                "generated_sequence_tensor_length": len(token_ids),
                "first_eos_after_decoder_prefix_index": eos_pos,
                "effective_generated_length": effective_length,
                "max_length": MAX_LENGTH,
                "reached_generation_ceiling": reached_ceiling,
                "num_beams": NUM_BEAMS,
                "ged_word_count": s["ged_label_count"],
                "morph_word_count": s["morph_word_count"],
                "ged_label_count": s["ged_label_count"],
                "subword_count": s["subword_count"],
                "per_word_piece_counts": s["per_word_piece_counts"],
                "gec_input_length": s["gec_input_length"],
                "gec_ged_label_length": s["gec_ged_label_length"],
                "model_max_position_embeddings": s["model_max_position_embeddings"],
                "tokenizer_model_max_length": s["tokenizer_model_max_length"],
                "input_truncated": s["input_truncated"],
                "input_truncation_proof": s["input_truncation_proof"],
                "regenerated_output_exact_match": True,
                "gold_reference_consulted": False,
            })

        processed = min(start + len(chunk), len(ordered))
        update_state(
            state_file, TRACE_VERSION, "REGENERATING_FROZEN_P2_OUTPUTS",
            processed, EXPECTED_CASES,
            message=f"exact_matches={exact_output_matches}; ceiling={ceiling_count}; missing_eos={missing_eos_count}",
        )
        print(f"P2_TRACE_PROGRESS {processed}/{EXPECTED_CASES}", flush=True)

    if exact_output_matches != EXPECTED_CASES:
        raise RuntimeError("not all regenerated outputs matched frozen P2")

    out_path = Path(args.out_prefix + ".jsonl")
    out_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in out) + "\n",
        encoding="utf-8",
    )

    summary = {
        "record_id": TRACE_VERSION,
        "status": "TRACE_COMPLETE",
        "cases": EXPECTED_CASES,
        "exact_frozen_output_matches": exact_output_matches,
        "generation_ceiling_cases": ceiling_count,
        "missing_terminal_eos_cases": missing_eos_count,
        "source_manifest_sha256": sha256_file(source_path),
        "P2_proposal_sha256": sha256_file(prop_path),
        "GEC_weight_sha256": weight_sha,
        "decoder_start_token_id": decoder_start,
        "eos_token_id": eos,
        "pad_token_id": pad,
        "forced_eos_token_id": forced_eos,
        "max_length": MAX_LENGTH,
        "num_beams": NUM_BEAMS,
        "trace_jsonl_sha256": sha256_file(out_path),
        "gold_reference_consulted": False,
        "reference_content_used": False,
        "R_joint_computed": False,
        "selector_trained": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
        "reserved_data_opened": False,
    }
    Path(args.out_prefix + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    update_state(
        state_file, TRACE_VERSION, "COMPLETE",
        EXPECTED_CASES, EXPECTED_CASES, status="COMPLETED",
        message=f"trace_sha256={summary['trace_jsonl_sha256']}",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)

if __name__ == "__main__":
    main()
