from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import socket
import sys
import time

def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(path: pathlib.Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def write_jsonl_atomic(path: pathlib.Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in rows), encoding="utf-8")
    os.replace(tmp, path)

def verify_group(root: pathlib.Path, expected: dict[str, str], group: str):
    rows = []
    for name, expected_hash in expected.items():
        p = root / name
        if not p.exists():
            raise RuntimeError(f"MISSING_FILE:{group}:{name}")
        actual = sha256_file(p)
        rows.append({"group": group, "file": name, "expected": expected_hash, "actual": actual, "match": actual == expected_hash})
        if actual != expected_hash:
            raise RuntimeError(f"HASH_MISMATCH:{group}:{name}")
    return rows

def block_network():
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_DATASETS_OFFLINE"] = "1"
    def blocked(self, *args, **kwargs):
        raise RuntimeError("NETWORK_FORBIDDEN_DURING_SEMANTIC_SCORING")
    socket.socket.connect = blocked

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--witness", choices=["HHEM", "DEBERTA"], required=True)
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--hash-lock", required=True)
    ap.add_argument("--hhem")
    ap.add_argument("--flan")
    ap.add_argument("--deberta")
    ap.add_argument("--output", required=True)
    ap.add_argument("--batch-size", type=int, default=8)
    args = ap.parse_args()

    pair_path = pathlib.Path(args.pairs)
    pair_sha = sha256_file(pair_path)
    expected_pair_sha = "27eaeb6bd6ab1a2b9ef3ff477cfa767c6e8c5526a85dcf9c491f32d8f9ac0460"
    if pair_sha != expected_pair_sha:
        raise RuntimeError(f"PAIR_MANIFEST_SHA_MISMATCH:{pair_sha}")

    pairs = read_jsonl(pair_path)
    if len(pairs) != 462:
        raise RuntimeError(f"PAIR_COUNT_MISMATCH:{len(pairs)}")
    ids = [x["pair_id"] for x in pairs]
    if len(ids) != len(set(ids)):
        raise RuntimeError("DUPLICATE_PAIR_ID")

    lock = json.loads(pathlib.Path(args.hash_lock).read_text(encoding="utf-8"))
    hash_checks = []

    if args.witness == "HHEM":
        if not args.hhem or not args.flan:
            raise RuntimeError("HHEM_AND_FLAN_PATHS_REQUIRED")
        hdir, fdir = pathlib.Path(args.hhem), pathlib.Path(args.flan)
        hash_checks += verify_group(hdir, lock["hhem"]["files"], "hhem")
        hash_checks += verify_group(fdir, lock["flan_runtime_dependency"]["files"], "flan_runtime_dependency")
    else:
        if not args.deberta:
            raise RuntimeError("DEBERTA_PATH_REQUIRED")
        ddir = pathlib.Path(args.deberta)
        hash_checks += verify_group(ddir, lock["deberta_nli"]["files"], "deberta_nli")

    # Network is forbidden after exact artifact acquisition and hash verification.
    block_network()

    import torch
    import transformers
    from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer

    torch.set_num_threads(min(4, os.cpu_count() or 1))
    torch.manual_seed(20261003)

    rows = []
    started = time.time()

    if args.witness == "HHEM":
        hdir, fdir = pathlib.Path(args.hhem).resolve(), pathlib.Path(args.flan).resolve()
        cfg = AutoConfig.from_pretrained(str(hdir), trust_remote_code=True, local_files_only=True)
        cfg.foundation = str(fdir)
        model = AutoModelForSequenceClassification.from_pretrained(
            str(hdir), config=cfg, trust_remote_code=True, local_files_only=True
        )
        model.eval()
        if model.__class__.__name__ != "HHEMv2ForSequenceClassification":
            raise RuntimeError(f"HHEM_CLASS_MISMATCH:{model.__class__.__name__}")
        for start in range(0, len(pairs), args.batch_size):
            batch = pairs[start:start + args.batch_size]
            text_pairs = [(x["premise"], x["hypothesis"]) for x in batch]
            with torch.no_grad():
                scores = model.predict(text_pairs).detach().cpu().tolist()
            if len(scores) != len(batch):
                raise RuntimeError("HHEM_BATCH_LENGTH_MISMATCH")
            for p, score in zip(batch, scores):
                rows.append({
                    "pair_id": p["pair_id"],
                    "calibration_id": p["calibration_id"],
                    "case_id": p["case_id"],
                    "direction": p["direction"],
                    "witness": "HHEM_2_1_OPEN",
                    "consistency_score": float(score),
                })
            write_jsonl_atomic(pathlib.Path(args.output), rows)
        model_identity = {
            "class": model.__class__.__name__,
            "parameters": sum(p.numel() for p in model.parameters()),
            "foundation_local": str(fdir),
        }
    else:
        ddir = pathlib.Path(args.deberta).resolve()
        cfg = AutoConfig.from_pretrained(str(ddir), local_files_only=True)
        labels = {str(k): str(v).lower() for k, v in cfg.id2label.items()}
        if labels != {"0": "entailment", "1": "neutral", "2": "contradiction"}:
            raise RuntimeError(f"DEBERTA_LABEL_MAP_MISMATCH:{labels}")
        tokenizer = AutoTokenizer.from_pretrained(str(ddir), local_files_only=True)
        model = AutoModelForSequenceClassification.from_pretrained(str(ddir), config=cfg, local_files_only=True)
        model.eval()
        if model.__class__.__name__ != "DebertaV2ForSequenceClassification":
            raise RuntimeError(f"DEBERTA_CLASS_MISMATCH:{model.__class__.__name__}")
        for start in range(0, len(pairs), args.batch_size):
            batch = pairs[start:start + args.batch_size]
            enc = tokenizer(
                [x["premise"] for x in batch],
                [x["hypothesis"] for x in batch],
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            )
            with torch.no_grad():
                logits = model(**enc).logits
                probs = torch.softmax(logits, dim=-1).detach().cpu().tolist()
            if len(probs) != len(batch):
                raise RuntimeError("DEBERTA_BATCH_LENGTH_MISMATCH")
            for p, pr in zip(batch, probs):
                rows.append({
                    "pair_id": p["pair_id"],
                    "calibration_id": p["calibration_id"],
                    "case_id": p["case_id"],
                    "direction": p["direction"],
                    "witness": "DEBERTA_NLI",
                    "entailment_probability": float(pr[0]),
                    "neutral_probability": float(pr[1]),
                    "contradiction_probability": float(pr[2]),
                })
            write_jsonl_atomic(pathlib.Path(args.output), rows)
        model_identity = {
            "class": model.__class__.__name__,
            "parameters": sum(p.numel() for p in model.parameters()),
            "labels": labels,
            "tokenizer_class": tokenizer.__class__.__name__,
            "max_length": 512,
        }

    if len(rows) != 462 or {x["pair_id"] for x in rows} != set(ids):
        raise RuntimeError("SCORE_COMPLETENESS_FAILURE")

    output_path = pathlib.Path(args.output)
    summary = {
        "gate": "AT0_EN_V2_4_RAW_SEMANTIC_WITNESS_SCORING_V1",
        "witness": args.witness,
        "status": "PASS",
        "pairs_scored": len(rows),
        "pair_manifest_sha256": pair_sha,
        "output_sha256": sha256_file(output_path),
        "elapsed_seconds": round(time.time() - started, 3),
        "batch_size": args.batch_size,
        "network_after_artifact_acquisition": False,
        "new_generator_inference": False,
        "confirmation_population_accessed": False,
        "threshold_selection_performed": False,
        "runtime": {
            "python": sys.version.split()[0],
            "torch": torch.__version__,
            "transformers": transformers.__version__,
        },
        "model_identity": model_identity,
        "hash_checks": hash_checks,
    }
    summary_path = output_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
