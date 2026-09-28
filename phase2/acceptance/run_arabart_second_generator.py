"""Run the public CAMeL-Lab AraBART+Morph+GED Arabic GEC model.

Development-only second candidate generator for Phase 2.
The generated sentence is NEVER accepted as product output. It is stored only
as an independent source of local edit evidence.

Official upstream:
  CAMeL-Lab/arabic-gec@8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf
Models:
  CAMeL-Lab/camelbert-msa-qalb14-ged-13
  CAMeL-Lab/arabart-qalb14-gec-ged-13
"""
from __future__ import annotations

import json
import platform
import subprocess
from pathlib import Path

import torch
import torch.nn.functional as F
import transformers
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from camel_tools.utils.dediac import dediac_ar
from transformers import AutoTokenizer, BertForTokenClassification, MBartForConditionalGeneration

ROOT = Path(__file__).resolve().parents[2]
DEV = ROOT / "phase2" / "arabic_eval" / "DEVELOPMENT_TARGETS.jsonl"
ART = ROOT / "artifacts"
GED_DIR = ROOT / "models" / "arabart_ged_qalb14"
GEC_DIR = ROOT / "models" / "arabart_gec_qalb14_ged13"
UPSTREAM = ROOT / "upstream" / "arabic-gec"
UPSTREAM_SHA = "8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"


def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def morph_preprocess(text: str, disambig):
    words = text.split()
    dis = disambig.disambiguate(words)
    if len(dis) != len(words):
        raise RuntimeError(f"morph disambiguation length drift: {len(dis)} != {len(words)}")
    out = []
    meta = []
    for src, wd in zip(words, dis):
        if not wd.analyses:
            out.append(dediac_ar(src))
            meta.append({"source_word": src, "status": "NO_ANALYSIS", "model_word": dediac_ar(src)})
            continue
        ana = wd.analyses[0].analysis
        diac = ana.get("diac", src)
        model_word = dediac_ar(diac)
        out.append(model_word)
        meta.append({
            "source_word": src,
            "status": "TOP_ANALYSIS",
            "model_word": model_word,
            "analysis": {
                k: ana.get(k) for k in ("diac","lex","pos","cas","mod","stt","gen","num","per","asp","vox")
            },
        })
    return " ".join(out), meta


def ged_word_labels(text: str, tokenizer, model):
    words = text.split()
    # Fast-tokenizer word mapping if available. The fallback reproduces the
    # README's first-subword logic conservatively.
    enc = tokenizer(words, is_split_into_words=True, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        logits = model(**enc).logits[0]
        probs = F.softmax(logits, dim=-1)
    try:
        word_ids = enc.word_ids(batch_index=0)
    except Exception:
        word_ids = None

    if word_ids is not None:
        first = {}
        for ti, wi in enumerate(word_ids):
            if wi is None or wi in first:
                continue
            first[wi] = ti
        if len(first) != len(words):
            raise RuntimeError(f"GED word mapping incomplete: {len(first)} != {len(words)}")
        rows = []
        for wi, word in enumerate(words):
            ti = first[wi]
            pred = int(torch.argmax(probs[ti]).item())
            rows.append({
                "word_index": wi,
                "word": word,
                "label": model.config.id2label[pred],
                "top_probability": float(probs[ti, pred].item()),
                "error_probability": float(1.0 - probs[ti, model.config.label2id["UC"]].item()),
            })
        return rows

    # Conservative fallback.
    enc2 = tokenizer([text], return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        probs2 = F.softmax(model(**enc2).logits[0], dim=-1)[1:-1]
    if len(probs2) < len(words):
        raise RuntimeError("GED fallback produced fewer predictions than words")
    rows = []
    for wi, word in enumerate(words):
        pred = int(torch.argmax(probs2[wi]).item())
        rows.append({
            "word_index": wi,
            "word": word,
            "label": model.config.id2label[pred],
            "top_probability": float(probs2[wi, pred].item()),
            "error_probability": float(1.0 - probs2[wi, model.config.label2id["UC"]].item()),
        })
    return rows


def featurize_gec(tokenizer, words, ged_rows, label_map):
    tokens = []
    labels = []
    if len(words) != len(ged_rows):
        raise RuntimeError("GEC word/GED length mismatch")
    for word, g in zip(words, ged_rows):
        pieces = tokenizer.tokenize(word)
        if pieces:
            tokens.extend(pieces)
            labels.extend([g["label"]] * len(pieces))
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    label_ids = [label_map.get(x, label_map["<pad>"]) for x in labels]
    input_ids = [tokenizer.bos_token_id] + input_ids + [tokenizer.eos_token_id]
    label_ids = [label_map["UC"]] + label_ids + [label_map["UC"]]
    if len(input_ids) != len(label_ids):
        raise RuntimeError("GEC input/GED id mismatch")
    return {
        "input_ids": torch.tensor([input_ids], dtype=torch.long),
        "attention_mask": torch.ones((1, len(input_ids)), dtype=torch.long),
        "ged_tags": torch.tensor([label_ids], dtype=torch.long),
    }


def main():
    ART.mkdir(parents=True, exist_ok=True)
    upstream_sha = subprocess.check_output(["git","-C",str(UPSTREAM),"rev-parse","HEAD"], text=True).strip()
    if upstream_sha != UPSTREAM_SHA:
        raise RuntimeError(f"Arabic-GEC upstream drift: {upstream_sha}")

    dev = read_jsonl(DEV)
    passages = {}
    for row in dev:
        passages.setdefault(int(row["passage_id"]), row["source"])
    if len(passages) != 41:
        raise RuntimeError(f"expected 41 passages, got {len(passages)}")

    morph = BERTUnfactoredDisambiguator.pretrained()
    ged_tok = AutoTokenizer.from_pretrained(str(GED_DIR), local_files_only=True, use_fast=True)
    ged_model = BertForTokenClassification.from_pretrained(str(GED_DIR), local_files_only=True).eval().cpu()
    gec_tok = AutoTokenizer.from_pretrained(str(GEC_DIR), local_files_only=True, use_fast=False)
    gec_model = MBartForConditionalGeneration.from_pretrained(str(GEC_DIR), local_files_only=True).eval().cpu()

    label_map = gec_model.config.ged_label2id
    if "UC" not in label_map or "<pad>" not in label_map:
        raise RuntimeError("GEC model missing GED label map")

    results = {}
    with torch.no_grad():
        for pid, source in sorted(passages.items()):
            morph_text, morph_meta = morph_preprocess(source, morph)
            ged_rows = ged_word_labels(morph_text, ged_tok, ged_model)
            feat = featurize_gec(gec_tok, morph_text.split(), ged_rows, label_map)
            generated = gec_model.generate(
                feat["input_ids"],
                attention_mask=feat["attention_mask"],
                ged_tags=feat["ged_tags"],
                num_beams=5,
                max_length=min(512, max(96, int(feat["input_ids"].shape[1] * 2.2))),
                num_return_sequences=1,
                no_repeat_ngram_size=0,
                early_stopping=False,
            )
            text = gec_tok.batch_decode(
                generated,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0].strip()
            results[str(pid)] = {
                "source": source,
                "morph_preprocessed": morph_text,
                "morph_words": morph_meta,
                "ged_words": ged_rows,
                "generated_raw": text,
            }
            print(json.dumps({"passage_id": pid, "generated_chars": len(text)}, ensure_ascii=False))

    revisions = {}
    rev_file = ART / "ARABART_MODEL_REVISIONS.json"
    if rev_file.exists():
        revisions = json.loads(rev_file.read_text(encoding="utf-8"))

    out = {
        "status": "DEVELOPMENT_ARABART_SECOND_GENERATOR_COMPLETE",
        "not_product_output": True,
        "no_gold_used_in_generation": True,
        "upstream_repo": "CAMeL-Lab/arabic-gec",
        "upstream_commit": upstream_sha,
        "runtime": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "transformers": transformers.__version__,
        },
        "models": revisions,
        "passages": results,
        "important_limitations": [
            "AraBART full generated sentences are evidence only and are never accepted directly.",
            "This reproduction uses the official public Morph+GED integration family on QALB14, not a model tuned to Nahw.",
            "Local edit alignment and candidate agreement are evaluated separately after generation.",
        ],
    }
    path = ART / "ARABART_SECOND_GENERATOR.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": out["status"], "passages": len(results), "output": str(path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
