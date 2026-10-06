#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from datetime import datetime, timezone

from transformers import AutoTokenizer

EXPECTED = {
    "train": "6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e",
    "dev": "3b12534fedec35660587e6a5084b0b8ff11267c1da4a2f5afe9aa16c4941340a",
    "config": "56bab767c02bc792897638feb8addc06d483d9c73769a5f554bbabea1f5507a1",
    "tokenizer_config": "53b6f42b8b8daddbdc6d3532c324187a92b46c1602bd6e8d4ad5a413b4fc90e1",
    "vocab": "7b36651908a88bc38bda41b728b2a598191e0d3b553cbacf7b1e5f026d5b5b9f",
}
FROZEN_MAX_LENGTH = 256


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_conll(path: pathlib.Path):
    out, toks, tags = [], [], []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            if toks:
                out.append((toks, tags))
                toks, tags = [], []
            continue
        p = raw.split("\t")
        if len(p) != 2:
            p = raw.rsplit(None, 1)
        if len(p) != 2:
            raise RuntimeError(f"bad line {raw!r}")
        tok, tag = p
        if tok == "-DOCSTART-":
            if toks:
                out.append((toks, tags))
                toks, tags = [], []
            continue
        toks.append(tok)
        tags.append(tag)
    if toks:
        out.append((toks, tags))
    return out


def audit_split(name, sentences, tokenizer):
    max_encoded = -1
    max_sentence_index = None
    over_256 = []
    over_512 = []
    truncation_losses = []
    lengths = []

    for si, (tokens, _tags) in enumerate(sentences):
        full = tokenizer(
            tokens,
            is_split_into_words=True,
            truncation=False,
            padding=False,
            add_special_tokens=True,
            return_attention_mask=False,
        )
        encoded_len = len(full["input_ids"])
        lengths.append(encoded_len)
        if encoded_len > max_encoded:
            max_encoded = encoded_len
            max_sentence_index = si

        if encoded_len > FROZEN_MAX_LENGTH:
            over_256.append({"sentence_index": si, "word_tokens": len(tokens), "wordpieces_with_specials": encoded_len})
        if encoded_len > 512:
            over_512.append({"sentence_index": si, "word_tokens": len(tokens), "wordpieces_with_specials": encoded_len})

        truncated = tokenizer(
            tokens,
            is_split_into_words=True,
            truncation=True,
            max_length=FROZEN_MAX_LENGTH,
            padding="max_length",
            return_attention_mask=False,
        )
        wids = truncated.word_ids()
        observed = sorted({w for w in wids if w is not None})
        observed_count = len(observed)
        if observed_count != len(tokens):
            truncation_losses.append(
                {
                    "sentence_index": si,
                    "word_tokens": len(tokens),
                    "observed_word_tokens_at_256": observed_count,
                    "missing_word_tokens": len(tokens) - observed_count,
                    "wordpieces_with_specials": encoded_len,
                }
            )

    lengths_sorted = sorted(lengths)
    def pct(q):
        if not lengths_sorted:
            return None
        pos = int(round((len(lengths_sorted) - 1) * q))
        return lengths_sorted[pos]

    return {
        "split": name,
        "sentences": len(sentences),
        "frozen_max_length": FROZEN_MAX_LENGTH,
        "max_wordpieces_with_specials": max_encoded,
        "max_sentence_index": max_sentence_index,
        "p95_wordpieces_with_specials": pct(0.95),
        "p99_wordpieces_with_specials": pct(0.99),
        "sentences_over_256": len(over_256),
        "sentences_over_512": len(over_512),
        "sentences_with_word_loss_at_256": len(truncation_losses),
        "over_256_cases": over_256,
        "over_512_cases": over_512,
        "truncation_loss_cases": truncation_losses,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", type=pathlib.Path, required=True)
    ap.add_argument("--dev", type=pathlib.Path, required=True)
    ap.add_argument("--model-dir", type=pathlib.Path, required=True)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=False)

    identities = {
        "train": sha256(args.train),
        "dev": sha256(args.dev),
        "config": sha256(args.model_dir / "config.json"),
        "tokenizer_config": sha256(args.model_dir / "tokenizer_config.json"),
        "vocab": sha256(args.model_dir / "vocab.txt"),
    }
    for key, want in EXPECTED.items():
        if identities[key] != want:
            raise RuntimeError(f"{key} hash mismatch: {identities[key]} != {want}")

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True, use_fast=True)
    config = json.loads((args.model_dir / "config.json").read_text(encoding="utf-8"))
    native_limit = int(config["max_position_embeddings"])

    train = audit_split("train", read_conll(args.train), tokenizer)
    dev = audit_split("dev", read_conll(args.dev), tokenizer)

    result = {
        "state": "R4_2C_TOKENIZER_CAPACITY_AUDIT_COMPLETE",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "identities": identities,
        "tokenizer_class": tokenizer.__class__.__name__,
        "frozen_protocol_max_length": FROZEN_MAX_LENGTH,
        "model_native_max_position_embeddings": native_limit,
        "train": train,
        "dev": dev,
        "guards": {
            "training_performed": False,
            "weights_loaded": False,
            "test_files_read": False,
            "factpico_used": False,
            "consumed_60_rct_holdout_used": False,
            "opened_30_rct_diagnostic_used": False,
            "thresholds_changed": False,
        },
    }
    if train["sentences_over_512"] or dev["sentences_over_512"]:
        result["capacity_classification"] = "NATIVE_512_INSUFFICIENT_FOR_AT_LEAST_ONE_SENTENCE"
    elif train["sentences_over_256"] or dev["sentences_over_256"]:
        result["capacity_classification"] = "FROZEN_256_INSUFFICIENT_BUT_NATIVE_512_SUFFICIENT"
    else:
        result["capacity_classification"] = "FROZEN_256_SUFFICIENT"

    raw = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_pre_hash_sha256"] = hashlib.sha256(raw).hexdigest()
    (args.out / "R4_2C_TOKENIZER_CAPACITY_AUDIT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    status = {
        "state": "COMPLETED",
        "progress_percent": 100.0,
        "current_stage": "TOKENIZER_CAPACITY_AUDIT_COMPLETE",
        "completed_units": 2,
        "total_units": 2,
        "last_successful_checkpoint": "R4_2C_TOKENIZER_CAPACITY_AUDIT.json",
        "last_progress_at": datetime.now(timezone.utc).isoformat(),
        "next_expected_step": "FREEZE_EXECUTION_ONLY_RECOVERY_DECISION",
        "failure_or_stall_reason": None,
    }
    (args.out / "PROCESS_STATUS.json").write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
