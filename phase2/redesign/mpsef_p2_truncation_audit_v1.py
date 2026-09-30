#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import torch
from transformers import AutoTokenizer, MBartForConditionalGeneration

EXPECTED_GEC_REV = "410588a318d988cdcfdbf64cf5745ed4adea0f6a"
EXPECTED_GEC_WEIGHT_SHA = "5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f"
EXPECTED_PROPOSAL_SHA = "f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b"
EXPECTED_CASES = 1918
MAX_LENGTH = 100

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def actual_sequence_length(ids, eos_id, pad_id):
    seq = list(map(int, ids))
    if eos_id is not None and eos_id in seq:
        return seq.index(eos_id) + 1, True
    while seq and pad_id is not None and seq[-1] == pad_id:
        seq.pop()
    return len(seq), False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proposals", required=True)
    ap.add_argument("--gec-model-dir", required=True)
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    proposal_path = Path(args.proposals)
    observed_sha = sha256_file(proposal_path)
    if observed_sha != EXPECTED_PROPOSAL_SHA:
        raise RuntimeError(f"proposal artifact SHA mismatch: {observed_sha}")

    rows = [
        json.loads(line)
        for line in proposal_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) != EXPECTED_CASES:
        raise RuntimeError(f"proposal count mismatch: {len(rows)}")
    if not (0 <= args.start < args.end <= len(rows)):
        raise RuntimeError("invalid chunk range")
    if args.start % args.batch_size != 0:
        raise RuntimeError("chunk start must preserve original batch boundary")

    weight_sha = sha256_file(Path(args.gec_model_dir) / "pytorch_model.bin")
    if weight_sha != EXPECTED_GEC_WEIGHT_SHA:
        raise RuntimeError(f"GEC weight SHA mismatch: {weight_sha}")

    tok = AutoTokenizer.from_pretrained(args.gec_model_dir)
    model = MBartForConditionalGeneration.from_pretrained(args.gec_model_dir)
    model.eval()

    eos_id = tok.eos_token_id
    pad_id = tok.pad_token_id
    results = []
    chunk = rows[args.start:args.end]

    for local_start in range(0, len(chunk), args.batch_size):
        batch = chunk[local_start:local_start + args.batch_size]
        max_in = max(len(r["gec_input_ids"]) for r in batch)
        ids_batch, labels_batch, masks = [], [], []
        ged_pad = model.config.ged_label2id["<pad>"]

        for r in batch:
            ids = list(map(int, r["gec_input_ids"]))
            labels = list(map(int, r["gec_ged_label_ids"]))
            if len(ids) != len(labels):
                raise RuntimeError(f"input/label mismatch for {r['uid']}")
            pad_n = max_in - len(ids)
            ids_batch.append(ids + [pad_id] * pad_n)
            labels_batch.append(labels + [ged_pad] * pad_n)
            masks.append([1] * len(ids) + [0] * pad_n)

        with torch.no_grad():
            generated = model.generate(
                torch.tensor(ids_batch),
                num_beams=5,
                max_length=MAX_LENGTH,
                num_return_sequences=1,
                no_repeat_ngram_size=0,
                early_stopping=False,
                ged_tags=torch.tensor(labels_batch),
                attention_mask=torch.tensor(masks),
            )

        decoded = tok.batch_decode(
            generated,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )

        for r, ids, text in zip(batch, generated.tolist(), decoded):
            actual_len, eos_seen = actual_sequence_length(ids, eos_id, pad_id)
            max_reached = actual_len >= MAX_LENGTH
            results.append({
                "uid": r["uid"],
                "case_id": r["case_id"],
                "frozen_output_sha256": r["output_sha256"],
                "rerun_output_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "output_exact_match": text == r["full_proposer_output"],
                "generated_tensor_width": len(ids),
                "generated_actual_length": actual_len,
                "eos_seen": eos_seen,
                "eos_at_last_actual_token": bool(
                    eos_seen and actual_len > 0 and int(ids[actual_len - 1]) == eos_id
                ),
                "max_length_reached": max_reached,
                "max_length": MAX_LENGTH,
            })

        processed = min(local_start + len(batch), len(chunk))
        global_done = args.start + processed
        print(
            f"P2_TRUNCATION_AUDIT_PROGRESS {global_done}/{args.end} "
            f"chunk={args.start}:{args.end}",
            flush=True,
        )

    if len(results) != args.end - args.start:
        raise RuntimeError("chunk result count mismatch")
    mismatches = sum(not r["output_exact_match"] for r in results)
    if mismatches:
        raise RuntimeError(f"frozen/rerun output mismatch count={mismatches}")

    out = Path(args.out)
    out.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n",
        encoding="utf-8",
    )
    summary = {
        "record_id": "MPSEF_P2_TRUNCATION_AUDIT_CHUNK_V1",
        "status": "PASS",
        "start": args.start,
        "end": args.end,
        "cases": len(results),
        "output_exact_matches": len(results) - mismatches,
        "max_length_reached": sum(r["max_length_reached"] for r in results),
        "no_eos": sum(not r["eos_seen"] for r in results),
        "max_generated_actual_length": max(
            (r["generated_actual_length"] for r in results), default=0
        ),
        "proposal_sha256": observed_sha,
        "gec_revision": EXPECTED_GEC_REV,
        "gec_weight_sha256": weight_sha,
        "gold_reference_consulted": False,
        "r_joint_computed": False,
    }
    Path(str(out) + ".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)

if __name__ == "__main__":
    main()
