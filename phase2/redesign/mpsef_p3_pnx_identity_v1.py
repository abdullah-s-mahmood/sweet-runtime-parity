#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download
from transformers import BertTokenizer, BertForTokenClassification

VERSION = "MPSEF_P3_PNX_IDENTITY_V1"
REPO_ID = "CAMeL-Lab/text-editing-qalb14-pnx"


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_json(obj) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def run(out_path: Path):
    info = HfApi().model_info(REPO_ID)
    rev = info.sha
    if not rev or len(rev) != 40:
        raise RuntimeError(f"invalid resolved revision: {rev!r}")

    src = Path(snapshot_download(repo_id=REPO_ID, revision=rev))
    model_dir = Path("pnx_model")
    if model_dir.exists():
        shutil.rmtree(model_dir)
    shutil.copytree(src, model_dir, symlinks=False)

    weight = model_dir / "pytorch_model.bin"
    if not weight.exists():
        raise RuntimeError("pytorch_model.bin missing")

    tok = BertTokenizer.from_pretrained(model_dir)
    model = BertForTokenClassification.from_pretrained(model_dir)

    id2label = {str(k): v for k, v in model.config.id2label.items()}
    label2id = {str(k): int(v) for k, v in model.config.label2id.items()}

    tokenizer_files = {}
    for name in (
        "vocab.txt",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "tokenizer.json",
    ):
        p = model_dir / name
        if p.exists():
            tokenizer_files[name] = sha_file(p)

    result = {
        "record_id": VERSION,
        "status": "PASS",
        "repo_id": REPO_ID,
        "resolved_revision": rev,
        "weight_sha256": sha_file(weight),
        "config_sha256": hashlib.sha256(
            model.config.to_json_string().encode()
        ).hexdigest(),
        "id2label_sha256": sha_json(id2label),
        "label2id_sha256": sha_json(label2id),
        "tokenizer_class": type(tok).__name__,
        "model_class": type(model).__name__,
        "vocab_size": len(tok),
        "num_labels": model.config.num_labels,
        "tokenizer_file_sha256": tokenizer_files,
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "model_inference_run": False,
    }

    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="MPSEF_P3_PNX_IDENTITY_V1.json")
    args = ap.parse_args()
    run(Path(args.out))


if __name__ == "__main__":
    main()
