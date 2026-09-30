#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import types
import unicodedata
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import BertForTokenClassification, BertTokenizer

SALT = "MPSEF-P1-ITERATIVE-PARITY-V1-20260930-A"
EXPECTED_MODEL_REV = "21286e56ce98a86362db540863f91c083b8970f9"
EXPECTED_WEIGHT_SHA = "9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d"


def norm(s: str) -> str:
    return " ".join((s or "").strip().split())


def rank_uid(uid: str) -> str:
    return hashlib.sha256((SALT + "|" + uid).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def published_reference(model, tokenizer, rewrite, words):
    text = list(words)
    trace = []
    for pass_index in (1, 2):
        tokenized = tokenizer(text, return_tensors="pt", is_split_into_words=True)
        with torch.no_grad():
            logits = model(**tokenized).logits
            preds = F.softmax(logits.squeeze(0), dim=-1)
            pred_ids = torch.argmax(preds, dim=-1).cpu().numpy()
        labels = [model.config.id2label[int(p)] for p in pred_ids[1:-1]]
        input_ids = tokenized["input_ids"][0][1:-1]
        assert len(labels) == len(input_ids)
        subwords = tokenizer.convert_ids_to_tokens(input_ids)
        output = norm(rewrite(subwords=[subwords], edits=[labels])[0][0])
        trace.append({
            "pass": pass_index,
            "subwords": subwords,
            "labels": labels,
            "output": output,
        })
        text = output.split()
    return trace


def mpsef_runner(model, tokenizer, rewrite, words):
    current_words = list(words)
    trace = []
    for pass_index in range(2):
        enc = tokenizer(
            current_words,
            return_tensors="pt",
            is_split_into_words=True,
        )
        with torch.no_grad():
            logits = model(**enc).logits.squeeze(0)
            label_ids = logits.argmax(dim=-1).tolist()
        core_ids = enc["input_ids"][0][1:-1]
        core_label_ids = label_ids[1:-1]
        if len(core_ids) != len(core_label_ids):
            raise RuntimeError("token/label length mismatch")
        subwords = tokenizer.convert_ids_to_tokens(core_ids)
        labels = [model.config.id2label[int(i)] for i in core_label_ids]
        output = norm(rewrite([subwords], [labels])[0][0])
        trace.append({
            "pass": pass_index + 1,
            "subwords": subwords,
            "labels": labels,
            "output": output,
        })
        current_words = output.split()
    return trace


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--upstream-root", required=True)
    ap.add_argument("--sample-n", type=int, default=64)
    ap.add_argument("--out-prefix", default="MPSEF_P1_ITERATIVE_PARITY_V1")
    args = ap.parse_args()

    rows = [
        json.loads(line)
        for line in Path(args.calibration).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    selected = sorted(rows, key=lambda r: rank_uid(r["uid"]))[:args.sample_n]

    weight = Path(args.model_dir) / "pytorch_model.bin"
    observed_weight_sha = sha256_file(weight)
    if observed_weight_sha != EXPECTED_WEIGHT_SHA:
        raise SystemExit(
            f"weight SHA mismatch: {observed_weight_sha} != {EXPECTED_WEIGHT_SHA}"
        )

    upstream = Path(args.upstream_root).resolve()
    sys.path.insert(0, str(upstream))
    sys.path.insert(0, str(upstream / "gec"))

    # Exact compatibility shim reused from the frozen H1 official-alignment
    # audit. P1 rewrite needs only these CAMeL Tools constants/normalizers;
    # no morphology resource is involved in SWEET NoPnx inference.
    unicode_punct_symbol = frozenset(
        chr(i) for i in range(0x110000)
        if unicodedata.category(chr(i))[0] in {"P", "S"}
    )
    camel_tools_mod = types.ModuleType("camel_tools")
    camel_utils_mod = types.ModuleType("camel_tools.utils")
    camel_charsets_mod = types.ModuleType("camel_tools.utils.charsets")
    camel_normalize_mod = types.ModuleType("camel_tools.utils.normalize")
    camel_charsets_mod.UNICODE_PUNCT_SYMBOL_CHARSET = unicode_punct_symbol
    camel_charsets_mod.AR_LETTERS_CHARSET = frozenset(
        "ءآأؤإئابتثجحخدذرزسشصضطظعغـفقكلمنهوىيٱپچڤگ"
    )
    camel_normalize_mod.normalize_alef_ar = lambda s: re.sub("[إأٱآ]", "ا", s)
    camel_normalize_mod.normalize_alef_maksura_ar = lambda s: s.replace("ى", "ي")
    camel_normalize_mod.normalize_teh_marbuta_ar = lambda s: s.replace("ة", "ه")
    sys.modules["camel_tools"] = camel_tools_mod
    sys.modules["camel_tools.utils"] = camel_utils_mod
    sys.modules["camel_tools.utils.charsets"] = camel_charsets_mod
    sys.modules["camel_tools.utils.normalize"] = camel_normalize_mod

    from gec.tag import rewrite

    tokenizer = BertTokenizer.from_pretrained(args.model_dir)
    model = BertForTokenClassification.from_pretrained(args.model_dir)
    model.eval()

    records = []
    mismatch_count = 0
    pass1_match = 0
    pass2_match = 0
    all_field_match = 0

    for idx, row in enumerate(selected, start=1):
        words = row["source"].split()
        ref = published_reference(model, tokenizer, rewrite, words)
        got = mpsef_runner(model, tokenizer, rewrite, words)

        p1 = ref[0] == got[0]
        p2 = ref[1] == got[1]
        all_ok = p1 and p2
        pass1_match += int(p1)
        pass2_match += int(p2)
        all_field_match += int(all_ok)
        mismatch_count += int(not all_ok)

        records.append({
            "case_id": row["case_id"],
            "uid": row["uid"],
            "source": row["source"],
            "reference_trace": ref,
            "runner_trace": got,
            "pass1_match": p1,
            "pass2_match": p2,
            "all_field_match": all_ok,
        })

        if idx == 1 or idx % 16 == 0 or idx == len(selected):
            print(
                f"P1_PARITY_PROGRESS {idx}/{len(selected)} "
                f"all_match={all_field_match}",
                flush=True,
            )

    sample_uid_sha = hashlib.sha256(
        ("\n".join(r["uid"] for r in selected) + "\n").encode("utf-8")
    ).hexdigest()

    summary = {
        "record_id": "MPSEF_P1_ITERATIVE_PARITY_V1",
        "status": "PASS" if mismatch_count == 0 else "FAIL",
        "sample_n": len(selected),
        "sample_salt": SALT,
        "sample_uid_sha256": sample_uid_sha,
        "model_revision": EXPECTED_MODEL_REV,
        "weight_sha256": observed_weight_sha,
        "decode_iter": 2,
        "pass1_exact_trace_match": pass1_match,
        "pass2_exact_trace_match": pass2_match,
        "all_field_match": all_field_match,
        "mismatches": mismatch_count,
        "gold_reference_consulted": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
    }

    Path(args.out_prefix + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    Path(args.out_prefix + "_TRACE.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in records) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    if mismatch_count:
        raise SystemExit(2)
    print("RUN_COMPLETE MPSEF_P1_ITERATIVE_PARITY_V1", flush=True)


if __name__ == "__main__":
    main()
