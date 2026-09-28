"""Phase 2 Selective Surgical Gate — Arabic GED localization probe.

Development-only. Runs public CAMeLBERT GED-13 models on the same 41 Nahw
passages and records word-level error-localization signals. It never uses Nahw
gold targets as model input.

The GED models are evaluated as localization gates only; this script does not
modify text and does not claim non-target GED predictions are false positives
because Nahw's extracted references are local, not exhaustive passage gold.
"""
from __future__ import annotations

import argparse
import json
import platform
import re
from pathlib import Path

import torch
import transformers
from transformers import AutoModelForTokenClassification, AutoTokenizer

HERE = Path(__file__).resolve().parents[1] / "arabic_eval"
ROOT = HERE.parents[1]
DEV = HERE / "DEVELOPMENT_TARGETS.jsonl"

MODELS = {
    "zaebuc_ged13": ROOT / "models" / "ged_zaebuc",
    "qalb14_ged13": ROOT / "models" / "ged_qalb14",
}


def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def word_spans(text: str):
    return [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"\S+", text)]


def first_piece_word_predictions(text: str, tokenizer, model):
    """Mimic GED training semantics: classify the first wordpiece of each word."""
    words = [w for _, _, w in word_spans(text)]
    spans = word_spans(text)
    pieces = []
    first_indices = []
    for word in words:
        wp = tokenizer.tokenize(word)
        if not wp:
            wp = [tokenizer.unk_token]
        first_indices.append(len(pieces))
        pieces.extend(wp)

    ids = tokenizer.convert_tokens_to_ids(pieces)
    input_ids = [tokenizer.cls_token_id] + ids + [tokenizer.sep_token_id]
    attention = [1] * len(input_ids)
    token_type = [0] * len(input_ids)
    with torch.no_grad():
        logits = model(
            input_ids=torch.tensor([input_ids]),
            attention_mask=torch.tensor([attention]),
            token_type_ids=torch.tensor([token_type]),
        ).logits[0]
        probs = torch.softmax(logits, dim=-1)

    results = []
    for wi, pi in enumerate(first_indices):
        tensor_index = 1 + pi
        score, pred = probs[tensor_index].max(dim=-1)
        label = model.config.id2label[int(pred)]
        a, b, word = spans[wi]
        results.append({
            "word_index": wi,
            "span": [a, b],
            "word": word,
            "label": label,
            "score": float(score),
            "is_error": label != "UC",
            "first_wordpiece": pieces[pi],
        })
    return results


def overlaps(a, b, c, d):
    return a < d and b > c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=ROOT / "artifacts" / "SELECTIVE_GED_LOCALIZATION.json")
    ap.add_argument("--revisions", type=Path, default=ROOT / "artifacts" / "GED_MODEL_REVISIONS.json")
    args = ap.parse_args()

    if not platform.python_version().startswith("3.10."):
        raise RuntimeError(platform.python_version())
    if not torch.__version__.startswith("1.12.1"):
        raise RuntimeError(torch.__version__)
    if transformers.__version__ != "4.30.0":
        raise RuntimeError(transformers.__version__)

    dev = read_jsonl(DEV)
    assert len(dev) == 150
    passage_rows = {}
    for row in dev:
        passage_rows.setdefault(row["passage_id"], row)
    assert len(passage_rows) == 41

    loaded = {}
    for name, folder in MODELS.items():
        tok = AutoTokenizer.from_pretrained(str(folder), local_files_only=True, use_fast=False)
        model = AutoModelForTokenClassification.from_pretrained(str(folder), local_files_only=True).eval().cpu()
        loaded[name] = (tok, model)

    passages = {}
    target_eval = {name: [] for name in MODELS}
    for pid, row in passage_rows.items():
        text = row["source"]
        passages[str(pid)] = {"source": text, "models": {}}
        for name, (tok, model) in loaded.items():
            preds = first_piece_word_predictions(text, tok, model)
            passages[str(pid)]["models"][name] = preds

    for row in dev:
        a, b = row["target_start"], row["target_end"]
        for name in MODELS:
            preds = passages[str(row["passage_id"])]["models"][name]
            target_words = [p for p in preds if overlaps(p["span"][0], p["span"][1], a, b)]
            detected = any(p["is_error"] for p in target_words)
            target_eval[name].append({
                "case_id": row["case_id"],
                "target_id": row["target_id"],
                "passage_id": row["passage_id"],
                "target_span": [a, b],
                "target_error": row["target_error"],
                "detected": detected,
                "overlap_words": target_words,
            })

    summary = {}
    for name, rows in target_eval.items():
        detected = sum(x["detected"] for x in rows)
        all_word_preds = [
            p for passage in passages.values()
            for p in passage["models"][name]
        ]
        err_words = sum(p["is_error"] for p in all_word_preds)
        summary[name] = {
            "published_targets": 150,
            "published_target_locations_detected": detected,
            "target_location_recall": detected / 150,
            "unique_passages": 41,
            "all_source_words": len(all_word_preds),
            "words_flagged_non_UC": err_words,
            "non_UC_word_rate": err_words / len(all_word_preds),
            "important_limit": "Non-target flagged words are not labeled false positives because extracted Nahw targets are not exhaustive passage annotations.",
        }

    output = {
        "status": "DEVELOPMENT_GED_LOCALIZATION_PROBE",
        "no_gold_used_as_input": True,
        "models": list(MODELS),
        "resolved_model_revisions": json.loads(args.revisions.read_text(encoding="utf-8")) if args.revisions.exists() else None,
        "summary": summary,
        "passages": passages,
        "target_evaluation": target_eval,
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "transformers": transformers.__version__,
        },
        "method_limitations": [
            "Public GED-13 models were originally trained with contextual morphological preprocessing in the EMNLP 2023 setup.",
            "This feasibility probe uses source text directly so it does not reproduce the full published morph-preprocessed GED pipeline.",
            "The model is used only as a deployable localization signal; target labels are used after inference for development evaluation.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ged_localization_summary": summary}, ensure_ascii=False))


if __name__ == "__main__":
    main()
