#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

EXPECTED_CASES = 6888
EXPECTED_UID_SHA256 = "3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9"
EXPECTED_MODEL_REVISION = "21286e56ce98a86362db540863f91c083b8970f9"
EXPECTED_MODEL_WEIGHT_SHA256 = "9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d"
EXPECTED_IMPL_REVISION = "4d552ca3ae98029550f27fc52aa1b22883e16e61"

ARABIC_RE = re.compile(r"[\u0600-\u06ff]")

def norm(s: str) -> str:
    return " ".join((s or "").strip().split())

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def uid_digest(uids):
    return hashlib.sha256(("\n".join(uids) + "\n").encode("utf-8")).hexdigest()

def classify_op(src_tokens, out_tokens, i1, i2, j1, j2):
    s = src_tokens[i1:i2]
    t = out_tokens[j1:j2]
    if i1 == i2:
        return "INSERT"
    if j1 == j2:
        return "DELETE"
    if len(s) == 1 and len(t) > 1 and "".join(s) == "".join(t):
        return "PURE_SPLIT"
    if len(s) > 1 and len(t) == 1 and "".join(s) == "".join(t):
        return "PURE_MERGE"
    if len(s) == 1 and len(t) == 1:
        return "EDIT"
    return "REPLACE_BLOCK"

def exact_gold_support(rec, span, replacement):
    replacement = norm(replacement)
    matches = []
    for idx, g in enumerate(rec.get("gold_edits", [])):
        if list(g.get("source_span", [])) == list(span) and norm(g.get("replacement", "")) == replacement:
            matches.append(idx)
    return matches

def load_rewrite_impl(upstream_root: Path):
    sys.path.insert(0, str(upstream_root))
    from edits.edit import SubwordEdit

    def resolve_merges(sent, edits):
        out = []
        for subword, edit in zip(sent, edits):
            if edit.startswith("M"):
                if out:
                    out[-1] = out[-1] + subword
                else:
                    out.append(subword)
            else:
                out.append(subword)
        return out

    def detokenize(sent):
        out = []
        for subword in sent:
            if subword.startswith("##"):
                if out:
                    out[-1] = out[-1] + subword[2:]
                else:
                    out.append(subword[2:])
            else:
                out.append(subword)
        return " ".join(out)

    def rewrite_one(subwords, edits):
        rewritten = []
        non_applicable = []
        for subword, raw_edit in zip(subwords, edits):
            edit = SubwordEdit(subword=subword, raw_subword=subword, edit=raw_edit)
            if edit.is_applicable(subword):
                rewritten.append(edit.apply(subword))
            else:
                rewritten.append(subword)
                non_applicable.append({"subword": subword, "edit": raw_edit})
        return detokenize(resolve_merges(rewritten, edits)), non_applicable

    return rewrite_one

def verify_weight(model_dir: Path):
    candidates = [p for p in model_dir.rglob("*") if p.is_file() and p.name in {"pytorch_model.bin", "model.safetensors"}]
    if not candidates:
        raise SystemExit("No model weight file found")
    hashes = [{"path": str(p.relative_to(model_dir)), "sha256": sha256_file(p)} for p in sorted(candidates)]
    if EXPECTED_MODEL_WEIGHT_SHA256 not in {x["sha256"] for x in hashes}:
        raise SystemExit(f"Frozen model weight SHA256 mismatch: {hashes}")
    return hashes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", default="M2H_CALIBRATION_V1.jsonl")
    ap.add_argument("--model-dir", default="h1_model")
    ap.add_argument("--upstream-root", default="upstream/text-editing")
    ap.add_argument("--model-revision", default=EXPECTED_MODEL_REVISION)
    ap.add_argument("--impl-revision", default=EXPECTED_IMPL_REVISION)
    ap.add_argument("--batch-size", type=int, default=16)
    args = ap.parse_args()

    if args.model_revision != EXPECTED_MODEL_REVISION:
        raise SystemExit("Unexpected H1 model revision")
    if args.impl_revision != EXPECTED_IMPL_REVISION:
        raise SystemExit("Unexpected H1 implementation revision")

    cal_path = Path(args.calibration)
    rows = [json.loads(x) for x in cal_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(rows) != EXPECTED_CASES:
        raise SystemExit(f"CALIBRATION case count mismatch: {len(rows)}")
    uids = [r["uid"] for r in rows]
    if len(set(uids)) != EXPECTED_CASES or uid_digest(uids) != EXPECTED_UID_SHA256:
        raise SystemExit("CALIBRATION UID integrity failure")

    weight_hashes = verify_weight(Path(args.model_dir))

    import torch
    from transformers import BertForTokenClassification, BertTokenizer

    tokenizer = BertTokenizer.from_pretrained(args.model_dir)
    model = BertForTokenClassification.from_pretrained(args.model_dir)
    model.eval()
    rewrite_one = load_rewrite_impl(Path(args.upstream_root))

    raw_out = []
    cand_out = []
    cand_counter = 0
    truncated_cases = 0
    non_applicable_total = 0
    gold_supported = 0
    reference_unsupported = 0
    operation_counts = Counter()

    with torch.no_grad():
        for base in range(0, len(rows), args.batch_size):
            batch_rows = rows[base:base + args.batch_size]
            batch_words = [r["source"].split() for r in batch_rows]
            token_lengths = [len(tokenizer.tokenize(r["source"])) + 2 for r in batch_rows]
            enc = tokenizer(
                batch_words,
                is_split_into_words=True,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            )
            logits = model(**enc).logits
            probs = torch.nn.functional.softmax(logits, dim=-1)
            max_probs, pred_ids = torch.max(probs, dim=-1)

            for bi, rec in enumerate(batch_rows):
                valid_len = int(enc["attention_mask"][bi].sum().item())
                ids = enc["input_ids"][bi, 1:valid_len - 1].tolist()
                labels = [model.config.id2label[int(x)] for x in pred_ids[bi, 1:valid_len - 1].tolist()]
                label_probs = [float(x) for x in max_probs[bi, 1:valid_len - 1].tolist()]
                subwords = tokenizer.convert_ids_to_tokens(ids)
                if not (len(subwords) == len(labels) == len(label_probs)):
                    raise SystemExit(f"Prediction length mismatch for {rec['case_id']}")

                rewritten, non_app = rewrite_one(subwords, labels)
                truncated = token_lengths[bi] > 512
                truncated_cases += int(truncated)
                non_applicable_total += len(non_app)

                raw_out.append({
                    "case_id": rec["case_id"],
                    "uid": rec["uid"],
                    "source": rec["source"],
                    "h1_rewrite": norm(rewritten),
                    "subwords": subwords,
                    "top1_labels": labels,
                    "top1_probabilities": label_probs,
                    "non_applicable_edits": non_app,
                    "truncated": truncated,
                    "model_revision": EXPECTED_MODEL_REVISION,
                    "implementation_revision": EXPECTED_IMPL_REVISION,
                    "decode_passes": 1,
                    "top_k": 1,
                })

                src_tokens = rec["source"].split()
                out_tokens = norm(rewritten).split()
                sm = difflib.SequenceMatcher(a=src_tokens, b=out_tokens, autojunk=False)
                for tag, i1, i2, j1, j2 in sm.get_opcodes():
                    if tag == "equal":
                        continue
                    replacement = norm(" ".join(out_tokens[j1:j2]))
                    surface = norm(" ".join(src_tokens[i1:i2]))
                    if i1 == i2 and not replacement:
                        continue
                    if i1 != i2 and surface == replacement:
                        continue

                    cand_counter += 1
                    op = classify_op(src_tokens, out_tokens, i1, i2, j1, j2)
                    operation_counts[op] += 1
                    gold_matches = exact_gold_support(rec, [i1, i2], replacement)
                    support = "EXACT_GOLD_SUPPORTED" if gold_matches else "REFERENCE_UNSUPPORTED"
                    gold_supported += int(bool(gold_matches))
                    reference_unsupported += int(not gold_matches)

                    cand_out.append({
                        "candidate_id": f"M2H-H1-CAND-{cand_counter:07d}",
                        "case_id": rec["case_id"],
                        "uid": rec["uid"],
                        "source_span": [i1, i2],
                        "source_surface": surface,
                        "candidate_replacement": replacement,
                        "alignment_opcode": tag,
                        "derived_operation": op,
                        "gold_support": support,
                        "matched_gold_edit_indices": gold_matches,
                        "contains_arabic": bool(ARABIC_RE.search(surface + replacement)),
                        "invariant": {
                            "span_in_bounds": 0 <= i1 <= i2 <= len(src_tokens),
                            "non_noop": surface != replacement,
                            "original_source_anchored": True,
                        },
                        "h1_sentence_record_case_id": rec["case_id"],
                    })

    if len(raw_out) != EXPECTED_CASES:
        raise SystemExit("Raw H1 output case count mismatch")
    if len({x["candidate_id"] for x in cand_out}) != len(cand_out):
        raise SystemExit("Duplicate candidate IDs")
    if any(not all(c["invariant"].values()) for c in cand_out):
        raise SystemExit("Candidate invariant failure")

    Path("M2H_H1_CALIBRATION_INFERENCE_V1.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in raw_out) + "\n", encoding="utf-8"
    )
    Path("M2H_H1_CALIBRATION_CANDIDATES_V1.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in cand_out) + ("\n" if cand_out else ""), encoding="utf-8"
    )

    summary = {
        "record_id": "M2H_H1_CALIBRATION_CANDIDATES_V1",
        "status": "PASS",
        "scope": "CALIBRATION_ONLY",
        "cases": len(raw_out),
        "candidates": len(cand_out),
        "exact_gold_supported_candidates": gold_supported,
        "reference_unsupported_candidates": reference_unsupported,
        "strict_reference_support_rate": (gold_supported / len(cand_out)) if cand_out else None,
        "truncated_cases": truncated_cases,
        "non_applicable_h1_edits": non_applicable_total,
        "derived_operation_counts": dict(operation_counts),
        "model_revision": EXPECTED_MODEL_REVISION,
        "implementation_revision": EXPECTED_IMPL_REVISION,
        "model_weight_files": weight_hashes,
        "candidate_generation": {
            "decode_passes": 1,
            "top_k": 1,
            "confidence_used_as_safety_evidence": False,
        },
        "integrity": {
            "calibration_uid_sha256": EXPECTED_UID_SHA256,
            "internal_evaluation_opened": False,
            "stress_diagnostic_opened": False,
            "confirmation_opened": False,
            "holdout_opened": False,
            "a7ta_reserved_opened": False,
            "reserved_nahw_opened": False,
            "qalb15_test_opened": False,
        },
        "scientific_note": "REFERENCE_UNSUPPORTED is not automatically WRONG because QALB is single-reference."
    }
    Path("M2H_H1_CALIBRATION_CANDIDATE_SUMMARY_V1.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
