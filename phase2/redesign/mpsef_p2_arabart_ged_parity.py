#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import torch
import torch.nn.functional as F
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from camel_tools.utils.dediac import dediac_ar
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

SALT = "MPSEF-P2-ARABART-GED-PARITY-V1-20260930-A"


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


def morph_text_official(disambig, text: str) -> str:
    # Direct transcription of the public CAMeL-Lab README inference recipe.
    text_disambig = disambig.disambiguate(text.split())
    morph_pp_text = [
        dediac_ar(w_disambig.analyses[0].analysis["diac"])
        for w_disambig in text_disambig
    ]
    return " ".join(morph_pp_text)


def ged_official(ged_tokenizer, ged_model, morph_text: str):
    inputs = ged_tokenizer([morph_text], return_tensors="pt")
    with torch.no_grad():
        logits = ged_model(**inputs).logits
    preds = F.softmax(logits, dim=-1).squeeze()[1:-1]
    pred_ged_labels = [
        ged_model.config.id2label[p.item()]
        for p in torch.argmax(preds, -1)
    ]
    return pred_ged_labels


def gec_official(gec_tokenizer, gec_model, morph_text: str, ged_labels):
    ged_label2ids = gec_model.config.ged_label2id
    tokens, expanded_labels = [], []

    for word, label in zip(morph_text.split(), ged_labels):
        word_tokens = gec_tokenizer.tokenize(word)
        if len(word_tokens) > 0:
            tokens.extend(word_tokens)
            expanded_labels.extend([label for _ in range(len(word_tokens))])

    input_ids = gec_tokenizer.convert_tokens_to_ids(tokens)
    input_ids = [gec_tokenizer.bos_token_id] + input_ids + [gec_tokenizer.eos_token_id]

    label_ids = [
        ged_label2ids.get(label, ged_label2ids["<pad>"])
        for label in expanded_labels
    ]
    label_ids = [ged_label2ids["UC"]] + label_ids + [ged_label2ids["UC"]]
    attention_mask = [1 for _ in range(len(input_ids))]

    gen_kwargs = {
        "num_beams": 5,
        "max_length": 100,
        "num_return_sequences": 1,
        "no_repeat_ngram_size": 0,
        "early_stopping": False,
        "ged_tags": torch.tensor([label_ids]),
        "attention_mask": torch.tensor([attention_mask]),
    }

    with torch.no_grad():
        generated = gec_model.generate(torch.tensor([input_ids]), **gen_kwargs)

    generated_text = gec_tokenizer.batch_decode(
        generated,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]

    return {
        "tokens": tokens,
        "input_ids": input_ids,
        "label_ids": label_ids,
        "generated_text": generated_text,
    }


def mpsef_runner(disambig, ged_tokenizer, ged_model, gec_tokenizer, gec_model, text: str):
    # Independently structured MP-SEF implementation of the frozen public path.
    words = text.split()
    dis = disambig.disambiguate(words)
    morph_tokens = []
    for item in dis:
        if not item.analyses:
            raise RuntimeError("No morphological analysis returned")
        morph_tokens.append(dediac_ar(item.analyses[0].analysis["diac"]))
    morph_text = " ".join(morph_tokens)

    enc = ged_tokenizer([morph_text], return_tensors="pt")
    with torch.no_grad():
        logits = ged_model(**enc).logits
    core_logits = logits.squeeze(0)[1:-1]
    label_ndx = core_logits.argmax(dim=-1).tolist()
    ged_labels = [ged_model.config.id2label[int(i)] for i in label_ndx]

    ged_label2ids = gec_model.config.ged_label2id
    subwords = []
    expanded = []
    for word, label in zip(morph_text.split(), ged_labels):
        pieces = gec_tokenizer.tokenize(word)
        if pieces:
            subwords.extend(pieces)
            expanded.extend([label] * len(pieces))

    input_ids = [
        gec_tokenizer.bos_token_id,
        *gec_tokenizer.convert_tokens_to_ids(subwords),
        gec_tokenizer.eos_token_id,
    ]
    label_ids = [
        ged_label2ids["UC"],
        *[ged_label2ids.get(x, ged_label2ids["<pad>"]) for x in expanded],
        ged_label2ids["UC"],
    ]
    attention_mask = [1] * len(input_ids)

    with torch.no_grad():
        generated = gec_model.generate(
            torch.tensor([input_ids]),
            num_beams=5,
            max_length=100,
            num_return_sequences=1,
            no_repeat_ngram_size=0,
            early_stopping=False,
            ged_tags=torch.tensor([label_ids]),
            attention_mask=torch.tensor([attention_mask]),
        )

    generated_text = gec_tokenizer.batch_decode(
        generated,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0]

    return {
        "morph_text": morph_text,
        "ged_labels": ged_labels,
        "tokens": subwords,
        "input_ids": input_ids,
        "label_ids": label_ids,
        "generated_text": generated_text,
    }


def model_manifest(root: Path):
    rows = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rows.append({
                "path": str(p.relative_to(root)),
                "bytes": p.stat().st_size,
                "sha256": sha256_file(p),
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--ged-model-dir", required=True)
    ap.add_argument("--gec-model-dir", required=True)
    ap.add_argument("--sample-n", type=int, default=64)
    ap.add_argument("--out-prefix", default="MPSEF_P2_ARABART_GED_PARITY_V1")
    args = ap.parse_args()

    rows = [
        json.loads(line)
        for line in Path(args.calibration).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    selected = sorted(rows, key=lambda r: rank_uid(r["uid"]))[: args.sample_n]

    # Default public model is MSA. Explicit use_gpu=False is behaviorally
    # equivalent on GitHub CPU runners because the implementation otherwise
    # falls back to CPU when CUDA is unavailable.
    disambig = BERTUnfactoredDisambiguator.pretrained(
        model_name="msa",
        use_gpu=False,
        pretrained_cache=False,
    )

    ged_tokenizer = AutoTokenizer.from_pretrained(args.ged_model_dir)
    ged_model = BertForTokenClassification.from_pretrained(args.ged_model_dir)
    ged_model.eval()

    gec_tokenizer = AutoTokenizer.from_pretrained(args.gec_model_dir)
    gec_model = MBartForConditionalGeneration.from_pretrained(args.gec_model_dir)
    gec_model.eval()

    records = []
    counts = {
        "morph_match": 0,
        "ged_match": 0,
        "tokens_match": 0,
        "input_ids_match": 0,
        "label_ids_match": 0,
        "generated_exact_match": 0,
        "generated_normalized_match": 0,
        "all_field_match": 0,
    }

    for idx, row in enumerate(selected, start=1):
        src = row["source"]

        ref_morph = morph_text_official(disambig, src)
        ref_ged = ged_official(ged_tokenizer, ged_model, ref_morph)
        ref_gec = gec_official(gec_tokenizer, gec_model, ref_morph, ref_ged)

        got = mpsef_runner(
            disambig,
            ged_tokenizer,
            ged_model,
            gec_tokenizer,
            gec_model,
            src,
        )

        checks = {
            "morph_match": ref_morph == got["morph_text"],
            "ged_match": ref_ged == got["ged_labels"],
            "tokens_match": ref_gec["tokens"] == got["tokens"],
            "input_ids_match": ref_gec["input_ids"] == got["input_ids"],
            "label_ids_match": ref_gec["label_ids"] == got["label_ids"],
            "generated_exact_match": ref_gec["generated_text"] == got["generated_text"],
            "generated_normalized_match": norm(ref_gec["generated_text"]) == norm(got["generated_text"]),
        }
        checks["all_field_match"] = all(checks.values())

        for key, val in checks.items():
            counts[key] += int(val)

        records.append({
            "case_id": row["case_id"],
            "uid": row["uid"],
            "source": src,
            "official": {
                "morph_text": ref_morph,
                "ged_labels": ref_ged,
                **ref_gec,
            },
            "runner": got,
            **checks,
        })

        if idx == 1 or idx % 8 == 0 or idx == len(selected):
            print(
                "P2_PARITY_PROGRESS "
                + json.dumps(
                    {
                        "processed": idx,
                        "total": len(selected),
                        "all_field_match": counts["all_field_match"],
                        "last_case_id": row["case_id"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    sample_uid_sha = hashlib.sha256(
        ("\n".join(r["uid"] for r in selected) + "\n").encode("utf-8")
    ).hexdigest()

    summary = {
        "record_id": "MPSEF_P2_ARABART_GED_PARITY_V1",
        "status": "PASS" if counts["all_field_match"] == len(selected) else "FAIL",
        "sample_n": len(selected),
        "sample_salt": SALT,
        "sample_uid_sha256": sample_uid_sha,
        "counts": counts,
        "generation": {
            "num_beams": 5,
            "max_length": 100,
            "num_return_sequences": 1,
            "no_repeat_ngram_size": 0,
            "early_stopping": False,
        },
        "gold_reference_consulted": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
    }

    prefix = Path(args.out_prefix)
    Path(str(prefix) + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    Path(str(prefix) + "_TRACE.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in records) + "\n",
        encoding="utf-8",
    )
    Path(str(prefix) + "_GED_MODEL_MANIFEST.json").write_text(
        json.dumps(model_manifest(Path(args.ged_model_dir)), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    Path(str(prefix) + "_GEC_MODEL_MANIFEST.json").write_text(
        json.dumps(model_manifest(Path(args.gec_model_dir)), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    if summary["status"] != "PASS":
        raise SystemExit(2)
    print("RUN_COMPLETE MPSEF_P2_ARABART_GED_PARITY_V1", flush=True)


if __name__ == "__main__":
    main()
