#!/usr/bin/env python3
"""
Build frozen PLABA-2024 H1 prediction inputs and separate gold labels.

This adapter is transport/identity only.
It MUST NOT perform semantic inference, normalization, repair, or label prediction.
It does NOT run AT0-EN V2.4.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import pathlib
import zipfile
from collections import Counter, defaultdict

EXPECTED_JUDGMENTS_SHA256 = "8256f7342c180e881e9c11244a7c24fe3e2fb4bdabf0fdfeb04892e4c8c722ce"
EXPECTED_SOURCE_SHA256 = "f9416ee9ef5a051e79053b526ad7023237cb87d171e79d9623bda4dbd656991e"
EXPECTED_COLUMNS = [
    "Abstract", "Sentence", "Source", "Target",
    "Accuracy", "Completeness", "Simplicity", "Brevity",
]
EXPECTED_RUNS = 19
EXPECTED_SOURCE_SENTENCES = 4060
EXPECTED_GRID = 77140
EXPECTED_GOLD_ROWS = 76790
EXPECTED_PMIDS = 399
EXPECTED_STRATA = {
    "EXTREME_POSITIVE": 51901,
    "EXTREME_NEGATIVE": 4275,
    "MIDDLE": 20614,
}

def sha256_path(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def canonical_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def gold_stratum(acc: int, com: int) -> str:
    if acc == 1 and com == 1:
        return "EXTREME_POSITIVE"
    if acc == -1 or com == -1:
        return "EXTREME_NEGATIVE"
    return "MIDDLE"

def find_member(zf: zipfile.ZipFile, suffix: str) -> str:
    matches = [n for n in zf.namelist() if n.endswith(suffix)]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one member ending {suffix!r}, got {matches}")
    return matches[0]

def load_source_map(source_zip: pathlib.Path):
    source_pairs = {}
    pmid_by_abstract = {}
    with zipfile.ZipFile(source_zip) as zf:
        test_member = find_member(zf, "/test.json")
        data = json.loads(zf.read(test_member).decode("utf-8"))
    for qid, qobj in data.items():
        abstracts = qobj["abstracts"]
        for aid, aobj in abstracts.items():
            abstract_id = f"{qid}_{aid}"
            pmid = str(aobj["PMID"])
            pmid_by_abstract[abstract_id] = pmid
            for sentence_index, source_text in enumerate(aobj["sentences"], start=1):
                key = (abstract_id, sentence_index)
                if key in source_pairs:
                    raise RuntimeError(f"Duplicate source key: {key}")
                source_pairs[key] = {
                    "source_text": source_text,
                    "pmid": pmid,
                }
    return source_pairs, pmid_by_abstract

def build(judgments_zip: pathlib.Path, source_zip: pathlib.Path, out_dir: pathlib.Path):
    if sha256_path(judgments_zip) != EXPECTED_JUDGMENTS_SHA256:
        raise RuntimeError("Manual-judgment archive SHA-256 mismatch")
    if sha256_path(source_zip) != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("Source archive SHA-256 mismatch")

    source_pairs, pmid_by_abstract = load_source_map(source_zip)
    if len(source_pairs) != EXPECTED_SOURCE_SENTENCES:
        raise RuntimeError(f"Unexpected source-sentence count: {len(source_pairs)}")
    if len(set(pmid_by_abstract.values())) != EXPECTED_PMIDS:
        raise RuntimeError("Unexpected unique PMID count")

    prediction_rows = []
    gold_rows = []
    run_names = []
    observed_keys_by_run = defaultdict(set)
    strata_counts = Counter()
    strata_pmids = defaultdict(set)

    with zipfile.ZipFile(judgments_zip) as zf:
        tsv_members = sorted(n for n in zf.namelist() if n.lower().endswith(".tsv"))
        if len(tsv_members) != EXPECTED_RUNS:
            raise RuntimeError(f"Unexpected run count: {len(tsv_members)}")
        for member in tsv_members:
            run_name = pathlib.PurePosixPath(member).name
            run_names.append(run_name)
            text = zf.read(member).decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text), delimiter="\t")
            if reader.fieldnames != EXPECTED_COLUMNS:
                raise RuntimeError(f"Schema mismatch in {run_name}: {reader.fieldnames}")

            for raw in reader:
                abstract_id = raw["Abstract"]
                sentence_index = int(raw["Sentence"])
                key = (abstract_id, sentence_index)
                if key not in source_pairs:
                    raise RuntimeError(f"Unknown source key in {run_name}: {key}")
                if key in observed_keys_by_run[run_name]:
                    raise RuntimeError(f"Duplicate row in {run_name}: {key}")
                observed_keys_by_run[run_name].add(key)

                source_text = raw["Source"]
                target_text = raw["Target"]
                expected_source = source_pairs[key]["source_text"]
                pmid = source_pairs[key]["pmid"]

                if source_text != expected_source:
                    raise RuntimeError(f"Source mismatch in {run_name}: {key}")
                if target_text is None or target_text == "":
                    raise RuntimeError(f"Empty Target in {run_name}: {key}")

                acc = int(raw["Accuracy"])
                com = int(raw["Completeness"])
                sim = int(raw["Simplicity"])
                brv = int(raw["Brevity"])
                for value in (acc, com, sim, brv):
                    if value not in (-1, 0, 1):
                        raise RuntimeError(f"Unexpected Likert value {value} in {run_name}: {key}")

                stratum = gold_stratum(acc, com)
                record_id = f"PLABA24::{run_name}::{abstract_id}::S{sentence_index}"

                prediction_rows.append({
                    "record_id": record_id,
                    "source_text": source_text,
                    "candidate_text": target_text,
                    "metadata": {
                        "dataset": "TREC_PLABA_2024",
                        "run": run_name,
                        "abstract_id": abstract_id,
                        "sentence_index": sentence_index,
                        "pmid": pmid,
                        "source_cluster_id": pmid,
                        "source_sha256": sha256_text(source_text),
                        "candidate_sha256": sha256_text(target_text),
                    },
                })

                gold_rows.append({
                    "record_id": record_id,
                    "pmid": pmid,
                    "run": run_name,
                    "abstract_id": abstract_id,
                    "sentence_index": sentence_index,
                    "accuracy": acc,
                    "completeness": com,
                    "simplicity": sim,
                    "brevity": brv,
                    "gold_stratum": stratum,
                })
                strata_counts[stratum] += 1
                strata_pmids[stratum].add(pmid)

    if len(prediction_rows) != EXPECTED_GOLD_ROWS:
        raise RuntimeError(f"Unexpected gold row count: {len(prediction_rows)}")
    if dict(strata_counts) != EXPECTED_STRATA:
        raise RuntimeError(f"Unexpected stratum counts: {dict(strata_counts)}")

    ids = [r["record_id"] for r in prediction_rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate record_id detected")

    prediction_rows.sort(key=lambda x: x["record_id"])
    gold_rows.sort(key=lambda x: x["record_id"])

    missing_by_run = {
        run: EXPECTED_SOURCE_SENTENCES - len(keys)
        for run, keys in sorted(observed_keys_by_run.items())
    }
    if sum(missing_by_run.values()) != EXPECTED_GRID - EXPECTED_GOLD_ROWS:
        raise RuntimeError("Missing-grid count mismatch")

    out_dir.mkdir(parents=True, exist_ok=True)
    prediction_path = out_dir / "H1_PLABA2024_PREDICTION_INPUT_PRIVATE.jsonl"
    gold_path = out_dir / "H1_PLABA2024_GOLD_PRIVATE.jsonl"
    manifest_path = out_dir / "H1_PLABA2024_BUILD_MANIFEST.json"

    prediction_path.write_text(
        "".join(canonical_json(r) + "\n" for r in prediction_rows),
        encoding="utf-8",
    )
    gold_path.write_text(
        "".join(canonical_json(r) + "\n" for r in gold_rows),
        encoding="utf-8",
    )

    manifest = {
        "contract_id": "H1_PLABA2024_EXTREME_V1",
        "manual_judgments_sha256": EXPECTED_JUDGMENTS_SHA256,
        "source_corpus_sha256": EXPECTED_SOURCE_SHA256,
        "run_count": len(run_names),
        "source_sentence_count": EXPECTED_SOURCE_SENTENCES,
        "expected_run_sentence_grid": EXPECTED_GRID,
        "gold_available_rows": EXPECTED_GOLD_ROWS,
        "gold_missing_rows": EXPECTED_GRID - EXPECTED_GOLD_ROWS,
        "gold_coverage_fraction": EXPECTED_GOLD_ROWS / EXPECTED_GRID,
        "unique_pmids": len(set(pmid_by_abstract.values())),
        "strata": {
            name: {
                "rows": int(strata_counts[name]),
                "pmid_clusters": len(strata_pmids[name]),
            }
            for name in ("EXTREME_POSITIVE", "EXTREME_NEGATIVE", "MIDDLE")
        },
        "missing_rows_by_run": missing_by_run,
        "prediction_input_sha256": sha256_path(prediction_path),
        "gold_file_sha256": sha256_path(gold_path),
        "prediction_input_contains_gold": False,
        "context_policy": "source_sentence_only",
        "source_cluster_unit": "PMID",
    }
    manifest_path.write_text(canonical_json(manifest) + "\n", encoding="utf-8")
    manifest["manifest_sha256"] = sha256_path(manifest_path)

    print(json.dumps(manifest, indent=2, sort_keys=True))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--judgments", type=pathlib.Path, required=True)
    p.add_argument("--source", type=pathlib.Path, required=True)
    p.add_argument("--out-dir", type=pathlib.Path, required=True)
    args = p.parse_args()
    build(args.judgments, args.source, args.out_dir)

if __name__ == "__main__":
    main()
