#!/usr/bin/env python3
"""
Build the frozen FactPICO H1 V5 prediction input and separate gold artifacts.

This adapter is deterministic transport/identity logic only.
It MUST NOT run AT0-EN V2.4, perform semantic inference, repair text,
or expose FactPICO gold fields to the prediction input.
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

CONTRACT_ID = "H1_FACTPICO_V5"
EXPECTED_ZIP_SHA256 = "ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4"
EXPECTED_PRIMARY_GOLD_SHA256 = "1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd"
EXPECTED_ELIGIBILITY_SHA256 = "d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255"

ALL_EVAL = "data/all_evaluations.csv"
DOUBLE_RATIONALES = "data/doubly_annotated_rationales.csv"
ADD_REST = "data/rest_added_information.csv"
ADD_DOUBLE = "data/doubly_annotated_split_added_information.csv"

EXPECTED_RECORDS = 345
EXPECTED_SOURCES = 115
EXPECTED_MODELS = {"ALPACA": 115, "GPT-4": 115, "LLAMA-2": 115}
EXPECTED_DOUBLE_SOURCES = 25
EXPECTED_NA_SOURCES = 3
EXPECTED_UNRESOLVED_ADD_SOURCES = 15
EXPECTED_EXACT_ADD_PAIRS = 216
EXPECTED_CLASSES = {
    "SAFE_STRICT_CONTROL": 34,
    "ERROR_STRICT": 149,
    "INTERMEDIATE": 153,
    "N_A_SOURCE_DIAGNOSTIC": 9,
}
EXPECTED_CLASS_SOURCES = {
    "SAFE_STRICT_CONTROL": 33,
    "ERROR_STRICT": 83,
    "INTERMEDIATE": 84,
    "N_A_SOURCE_DIAGNOSTIC": 3,
}
EXPECTED_CLASS_MODELS = {
    "SAFE_STRICT_CONTROL": {"ALPACA": 33, "GPT-4": 1, "LLAMA-2": 0},
    "ERROR_STRICT": {"ALPACA": 35, "GPT-4": 45, "LLAMA-2": 69},
    "INTERMEDIATE": {"ALPACA": 44, "GPT-4": 66, "LLAMA-2": 43},
    "N_A_SOURCE_DIAGNOSTIC": {"ALPACA": 3, "GPT-4": 3, "LLAMA-2": 3},
}

PICO_FIELDS = ["Population", "Intervention", "Comparator", "Outcome"]

ELIGIBILITY_FIELDS = [
    "record_id",
    "source_sha256",
    "candidate_sha256",
    "model_type",
    "annotation_provenance",
    "na_source",
    "added_info_span_exact",
    "added_info_identity_unresolved_source",
    "gold_class_v5",
    "pico_error_trigger",
    "results_value",
    "population",
    "intervention",
    "comparator",
    "outcome",
]

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

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

def read_csv_member(zf: zipfile.ZipFile, member: str):
    raw = zf.read(member)
    text = raw.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text))), raw

def as_float(value: str) -> float:
    return float(value)

def fmt_float(value: float) -> str:
    return str(float(value))

def record_id(source_sha: str, model_type: str, candidate_sha: str) -> str:
    return sha256_text(
        "FACTPICO_REC_V1\0" + source_sha + "\0" + model_type + "\0" + candidate_sha
    )

def build(factpico_zip: pathlib.Path, out_dir: pathlib.Path):
    if sha256_path(factpico_zip) != EXPECTED_ZIP_SHA256:
        raise RuntimeError("FactPICO ZIP SHA-256 mismatch")

    with zipfile.ZipFile(factpico_zip) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"ZIP integrity failure at {bad}")

        all_rows, all_raw = read_csv_member(zf, ALL_EVAL)
        if sha256_bytes(all_raw) != EXPECTED_PRIMARY_GOLD_SHA256:
            raise RuntimeError("all_evaluations.csv SHA-256 mismatch")

        double_rows, _ = read_csv_member(zf, DOUBLE_RATIONALES)
        add_rest_rows, _ = read_csv_member(zf, ADD_REST)
        add_double_rows, _ = read_csv_member(zf, ADD_DOUBLE)

    if len(all_rows) != EXPECTED_RECORDS:
        raise RuntimeError(f"Unexpected FactPICO record count: {len(all_rows)}")

    required = {"Abstract", "generation", "model_type", *PICO_FIELDS, "Results"}
    missing = required - set(all_rows[0].keys())
    if missing:
        raise RuntimeError(f"Missing required primary columns: {sorted(missing)}")

    source_candidates = defaultdict(set)
    model_counts = Counter()
    for row in all_rows:
        source = row["Abstract"]
        candidate = row["generation"]
        model = row["model_type"]
        if not source or not candidate or not model:
            raise RuntimeError("Empty source/candidate/model in primary gold")
        source_candidates[source].add(candidate)
        model_counts[model] += 1

    if len(source_candidates) != EXPECTED_SOURCES:
        raise RuntimeError(f"Unexpected unique source count: {len(source_candidates)}")
    if dict(model_counts) != EXPECTED_MODELS:
        raise RuntimeError(f"Unexpected model counts: {dict(model_counts)}")
    if any(len(cands) != 3 for cands in source_candidates.values()):
        raise RuntimeError("Each source must have exactly three unique candidates")

    double_sources = {r["abstract"] for r in double_rows}
    if len(double_sources) != EXPECTED_DOUBLE_SOURCES:
        raise RuntimeError(f"Unexpected double-PICO source count: {len(double_sources)}")

    na_sources = set()
    for row in all_rows:
        vals = [as_float(row[f]) for f in PICO_FIELDS]
        if any(v == 0.0 for v in vals):
            na_sources.add(row["Abstract"])
    if len(na_sources) != EXPECTED_NA_SOURCES:
        raise RuntimeError(f"Unexpected N/A source count: {len(na_sources)}")

    exact_add_pairs = set()
    unresolved_add_sources = set()
    for row in add_rest_rows + add_double_rows:
        source = row["abstract"]
        candidate = row["generation"]
        known = source_candidates.get(source)
        if known is None:
            raise RuntimeError("Added Information row contains unknown source abstract")
        if candidate in known:
            exact_add_pairs.add((source, candidate))
        else:
            unresolved_add_sources.add(source)

    if len(exact_add_pairs) != EXPECTED_EXACT_ADD_PAIRS:
        raise RuntimeError(f"Unexpected exact Added Information pair count: {len(exact_add_pairs)}")
    if len(unresolved_add_sources) != EXPECTED_UNRESOLVED_ADD_SOURCES:
        raise RuntimeError(
            f"Unexpected unresolved Added Information source count: {len(unresolved_add_sources)}"
        )

    prediction_rows = []
    gold_rows = []
    eligibility_rows = []
    seen_ids = set()
    class_counts = Counter()
    class_sources = defaultdict(set)
    class_models = defaultdict(Counter)

    for row in all_rows:
        source = row["Abstract"]
        candidate = row["generation"]
        model = row["model_type"]

        source_sha = sha256_text(source)
        candidate_sha = sha256_text(candidate)
        rid = record_id(source_sha, model, candidate_sha)
        if rid in seen_ids:
            raise RuntimeError(f"Duplicate record ID: {rid}")
        seen_ids.add(rid)

        is_double = source in double_sources
        is_na_source = source in na_sources
        add_exact = (source, candidate) in exact_add_pairs
        add_unresolved_source = source in unresolved_add_sources

        pico_values = {f: as_float(row[f]) for f in PICO_FIELDS}
        results_value = as_float(row["Results"])

        threshold = 1.5 if is_double else 2.0
        pico_error_trigger = int(
            any(v != 0.0 and v <= threshold for v in pico_values.values())
        )

        safe_control = (
            not is_na_source
            and all(v == 4.0 for v in pico_values.values())
            and results_value == 4.0
            and not add_exact
            and not add_unresolved_source
        )

        if is_na_source:
            gold_class = "N_A_SOURCE_DIAGNOSTIC"
        elif safe_control:
            gold_class = "SAFE_STRICT_CONTROL"
        elif pico_error_trigger:
            gold_class = "ERROR_STRICT"
        else:
            gold_class = "INTERMEDIATE"

        prediction_rows.append({
            "record_id": rid,
            "source_text": source,
            "candidate_text": candidate,
        })

        gold_rows.append({
            "record_id": rid,
            "source_cluster_id": source_sha,
            "model_type": model,
            "annotation_provenance": (
                "DOUBLE_PICO_AGGREGATE" if is_double else "SINGLE_PICO"
            ),
            "na_source": int(is_na_source),
            "added_info_span_exact": int(add_exact),
            "added_info_identity_unresolved_source": int(add_unresolved_source),
            "gold_class_v5": gold_class,
            "pico_error_trigger": pico_error_trigger,
            "population": pico_values["Population"],
            "intervention": pico_values["Intervention"],
            "comparator": pico_values["Comparator"],
            "outcome": pico_values["Outcome"],
            "results_value": results_value,
        })

        eligibility_rows.append({
            "record_id": rid,
            "source_sha256": source_sha,
            "candidate_sha256": candidate_sha,
            "model_type": model,
            "annotation_provenance": (
                "DOUBLE_PICO_AGGREGATE" if is_double else "SINGLE_PICO"
            ),
            "na_source": int(is_na_source),
            "added_info_span_exact": int(add_exact),
            "added_info_identity_unresolved_source": int(add_unresolved_source),
            "gold_class_v5": gold_class,
            "pico_error_trigger": pico_error_trigger,
            "results_value": results_value,
            "population": pico_values["Population"],
            "intervention": pico_values["Intervention"],
            "comparator": pico_values["Comparator"],
            "outcome": pico_values["Outcome"],
        })

        class_counts[gold_class] += 1
        class_sources[gold_class].add(source_sha)
        class_models[gold_class][model] += 1

    if dict(class_counts) != EXPECTED_CLASSES:
        raise RuntimeError(f"V5 class count mismatch: {dict(class_counts)}")
    actual_class_sources = {k: len(class_sources[k]) for k in EXPECTED_CLASSES}
    if actual_class_sources != EXPECTED_CLASS_SOURCES:
        raise RuntimeError(f"V5 class source-count mismatch: {actual_class_sources}")
    actual_class_models = {
        cls: {m: int(class_models[cls].get(m, 0)) for m in EXPECTED_MODELS}
        for cls in EXPECTED_CLASSES
    }
    if actual_class_models != EXPECTED_CLASS_MODELS:
        raise RuntimeError(f"V5 class model-count mismatch: {actual_class_models}")

    prediction_rows.sort(key=lambda x: x["record_id"])
    gold_rows.sort(key=lambda x: x["record_id"])
    eligibility_rows.sort(key=lambda x: x["record_id"])

    out_dir.mkdir(parents=True, exist_ok=True)

    prediction_path = out_dir / "FACTPICO_H1_V5_PREDICTION_INPUT_PRIVATE.jsonl"
    gold_path = out_dir / "FACTPICO_H1_V5_GOLD_PRIVATE.jsonl"
    eligibility_path = out_dir / "FACTPICO_HARD_GOLD_ELIGIBILITY_MANIFEST_V5.csv"
    build_manifest_path = out_dir / "FACTPICO_H1_V5_BUILD_MANIFEST.json"

    prediction_path.write_text(
        "".join(canonical_json(r) + "\n" for r in prediction_rows),
        encoding="utf-8",
        newline="\n",
    )
    gold_path.write_text(
        "".join(canonical_json(r) + "\n" for r in gold_rows),
        encoding="utf-8",
        newline="\n",
    )

    with eligibility_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(ELIGIBILITY_FIELDS)
        for r in eligibility_rows:
            writer.writerow([
                r["record_id"],
                r["source_sha256"],
                r["candidate_sha256"],
                r["model_type"],
                r["annotation_provenance"],
                r["na_source"],
                r["added_info_span_exact"],
                r["added_info_identity_unresolved_source"],
                r["gold_class_v5"],
                r["pico_error_trigger"],
                fmt_float(r["results_value"]),
                fmt_float(r["population"]),
                fmt_float(r["intervention"]),
                fmt_float(r["comparator"]),
                fmt_float(r["outcome"]),
            ])

    if sha256_path(eligibility_path) != EXPECTED_ELIGIBILITY_SHA256:
        raise RuntimeError("Regenerated V5 eligibility manifest SHA-256 mismatch")

    allowed_prediction_keys = {"record_id", "source_text", "candidate_text"}
    forbidden_gold_keys = {
        "Population", "Intervention", "Comparator", "Outcome", "Results",
        "population", "intervention", "comparator", "outcome", "results_value",
        "gold_class_v5", "pico_error_trigger", "na_source",
        "annotation_provenance", "added_info_span_exact",
        "added_info_identity_unresolved_source",
    }
    for r in prediction_rows:
        if set(r) != allowed_prediction_keys:
            raise RuntimeError(f"Unexpected prediction-input keys: {sorted(r)}")
        if forbidden_gold_keys & set(r):
            raise RuntimeError("Gold leakage into prediction input")

    pred_ids = [r["record_id"] for r in prediction_rows]
    gold_ids = [r["record_id"] for r in gold_rows]
    if pred_ids != gold_ids:
        raise RuntimeError("Prediction/gold record IDs are not exactly aligned")

    adapter_path = pathlib.Path(__file__).resolve()

    manifest = {
        "contract_id": CONTRACT_ID,
        "factpico_zip_sha256": EXPECTED_ZIP_SHA256,
        "primary_gold_member": ALL_EVAL,
        "primary_gold_sha256": EXPECTED_PRIMARY_GOLD_SHA256,
        "adapter_sha256": sha256_path(adapter_path),
        "record_count": len(prediction_rows),
        "source_cluster_count": len({r["source_cluster_id"] for r in gold_rows}),
        "double_pico_source_count": len(double_sources),
        "na_source_count": len(na_sources),
        "exact_added_information_pair_count": len(exact_add_pairs),
        "unresolved_added_information_source_count": len(unresolved_add_sources),
        "class_counts": dict(class_counts),
        "class_source_counts": actual_class_sources,
        "class_model_counts": actual_class_models,
        "prediction_input_sha256": sha256_path(prediction_path),
        "gold_file_sha256": sha256_path(gold_path),
        "eligibility_manifest_sha256": sha256_path(eligibility_path),
        "prediction_input_contains_gold_fields": False,
        "prediction_input_allowed_keys": sorted(allowed_prediction_keys),
        "prediction_gold_id_sets_exact_match": True,
        "source_cluster_unit": "SHA256(exact Abstract text)",
        "prediction_context": "full_abstract_to_full_summary",
        "results_negative_trigger": False,
        "gold_join_allowed_only_after_prediction_freeze": True,
        "v2_4_execution_performed": False,
    }
    build_manifest_path.write_text(
        canonical_json(manifest) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    output = dict(manifest)
    output["build_manifest_sha256"] = sha256_path(build_manifest_path)
    print(json.dumps(output, indent=2, sort_keys=True))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--factpico-zip", type=pathlib.Path, required=True)
    p.add_argument("--out-dir", type=pathlib.Path, required=True)
    args = p.parse_args()
    build(args.factpico_zip, args.out_dir)

if __name__ == "__main__":
    main()
