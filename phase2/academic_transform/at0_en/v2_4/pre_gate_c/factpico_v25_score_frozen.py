#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import pathlib
from collections import Counter, defaultdict

SCORER_ID = "FACTPICO_V25_H1_SCORER_V1"
EXPECTED_COUNT = 345
EXPECTED_GOLD_SHA256 = "6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48"
EXPECTED_ELIGIBILITY_SHA256 = "d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255"
EXPECTED_PREDICTION_SHA256 = "925c8a073f4304fe751af072c1d1b8fc64455104e8ed2f23a88c3fc3e6ad496b"
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
OUTCOMES = ("PASS_CANDIDATE", "REJECT", "REVIEW", "INVALID_VERIFICATION")
BOOTSTRAP_SEED = 20261004
BOOTSTRAP_RESAMPLES = 10000
PERCENTILE_METHOD = "TYPE7_LINEAR_INTERPOLATION"
BOOTSTRAP_INDEX_GENERATOR = "SHA256_COUNTER_MOD_N_V1"
THRESHOLD = 0.75

def sha256_path(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def canonical_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def read_jsonl(path: pathlib.Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def percentile_type7(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("Cannot compute percentile of empty values")
    xs = sorted(values)
    if len(xs) == 1:
        return float(xs[0])
    h = (len(xs) - 1) * q
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return float(xs[lo])
    frac = h - lo
    return float(xs[lo] + frac * (xs[hi] - xs[lo]))

def deterministic_index(seed: int, replicate: int, draw: int, n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    raw = f"{seed}\0{replicate}\0{draw}".encode("ascii")
    return int.from_bytes(hashlib.sha256(raw).digest(), "big") % n

def per_source_rates(rows: list[dict], success_outcome: str) -> dict[str, float]:
    by = defaultdict(list)
    for r in rows:
        by[r["source_cluster_id"]].append(r)
    return {
        sid: sum(x["predicted_outcome"] == success_outcome for x in items) / len(items)
        for sid, items in by.items()
    }

def utility_metrics(rows: list[dict], success_outcome: str) -> dict:
    if not rows:
        raise ValueError("Empty utility population")
    sources = sorted({r["source_cluster_id"] for r in rows})
    by_source = {sid: [r for r in rows if r["source_cluster_id"] == sid] for sid in sources}
    pair_point = sum(r["predicted_outcome"] == success_outcome for r in rows) / len(rows)
    source_rates = per_source_rates(rows, success_outcome)
    macro_point = sum(source_rates.values()) / len(source_rates)

    boot_micro = []
    boot_macro = []
    for rep in range(BOOTSTRAP_RESAMPLES):
        sampled = [sources[deterministic_index(BOOTSTRAP_SEED, rep, d, len(sources))]
                   for d in range(len(sources))]
        sampled_rows = []
        sampled_rates = []
        for sid in sampled:
            items = by_source[sid]
            sampled_rows.extend(items)
            sampled_rates.append(
                sum(x["predicted_outcome"] == success_outcome for x in items) / len(items)
            )
        micro = sum(x["predicted_outcome"] == success_outcome for x in sampled_rows) / len(sampled_rows)
        macro = sum(sampled_rates) / len(sampled_rates)
        boot_micro.append(micro)
        boot_macro.append(macro)

    return {
        "success_outcome": success_outcome,
        "record_count": len(rows),
        "source_count": len(sources),
        "pair_micro": pair_point,
        "source_macro": macro_point,
        "pair_micro_ci95": [
            percentile_type7(boot_micro, 0.025),
            percentile_type7(boot_micro, 0.975),
        ],
        "source_macro_ci95": [
            percentile_type7(boot_macro, 0.025),
            percentile_type7(boot_macro, 0.975),
        ],
        "threshold": THRESHOLD,
        "pair_gate_pass": pair_point >= THRESHOLD,
        "source_gate_pass": macro_point >= THRESHOLD,
        "gate_pass": pair_point >= THRESHOLD and macro_point >= THRESHOLD,
    }

def outcome_counts(rows: list[dict]) -> dict[str, int]:
    c = Counter(r["predicted_outcome"] for r in rows)
    unknown = set(c) - set(OUTCOMES)
    if unknown:
        raise RuntimeError(f"Unknown prediction outcomes: {sorted(unknown)}")
    return {k: int(c.get(k, 0)) for k in OUTCOMES}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", type=pathlib.Path, required=True)
    ap.add_argument("--gold", type=pathlib.Path, required=True)
    ap.add_argument("--eligibility", type=pathlib.Path, required=True)
    ap.add_argument("--out-dir", type=pathlib.Path, required=True)
    args = ap.parse_args()

    if sha256_path(args.predictions) != EXPECTED_PREDICTION_SHA256:
        raise RuntimeError("Prediction SHA-256 mismatch")
    if sha256_path(args.gold) != EXPECTED_GOLD_SHA256:
        raise RuntimeError("Gold SHA-256 mismatch")
    if sha256_path(args.eligibility) != EXPECTED_ELIGIBILITY_SHA256:
        raise RuntimeError("Eligibility SHA-256 mismatch")

    preds = read_jsonl(args.predictions)
    gold = read_jsonl(args.gold)
    if len(preds) != EXPECTED_COUNT or len(gold) != EXPECTED_COUNT:
        raise RuntimeError("Prediction/gold count mismatch")

    pred_ids = [r["record_id"] for r in preds]
    gold_ids = [r["record_id"] for r in gold]
    if len(set(pred_ids)) != EXPECTED_COUNT or len(set(gold_ids)) != EXPECTED_COUNT:
        raise RuntimeError("Duplicate IDs")
    if set(pred_ids) != set(gold_ids):
        missing = sorted(set(gold_ids) - set(pred_ids))
        extra = sorted(set(pred_ids) - set(gold_ids))
        raise RuntimeError(f"INVALID_H1_EVALUATION: exact ID set mismatch missing={len(missing)} extra={len(extra)}")

    with args.eligibility.open("r", encoding="utf-8", newline="") as f:
        elig = list(csv.DictReader(f))
    if len(elig) != EXPECTED_COUNT:
        raise RuntimeError("Eligibility count mismatch")
    elig_ids = [r["record_id"] for r in elig]
    if len(set(elig_ids)) != EXPECTED_COUNT or set(elig_ids) != set(gold_ids):
        raise RuntimeError("INVALID_H1_EVALUATION: eligibility ID mismatch")

    gmap = {r["record_id"]: r for r in gold}
    emap = {r["record_id"]: r for r in elig}
    joined = []
    for p in preds:
        rid = p["record_id"]
        g = gmap[rid]
        e = emap[rid]
        checks = {
            "source_cluster_id": "source_sha256",
            "model_type": "model_type",
            "annotation_provenance": "annotation_provenance",
            "gold_class_v5": "gold_class_v5",
        }
        for gf, ef in checks.items():
            if str(g[gf]) != str(e[ef]):
                raise RuntimeError(f"Eligibility/gold mismatch {rid} field={gf}")
        if p.get("predicted_outcome") not in OUTCOMES:
            raise RuntimeError(f"Unknown outcome for {rid}")
        joined.append({
            "record_id": rid,
            "predicted_outcome": p["predicted_outcome"],
            "invalid_reason": p.get("invalid_reason"),
            "runtime_id": p.get("runtime_id"),
            **g,
        })

    class_counts = Counter(r["gold_class_v5"] for r in joined)
    if dict(class_counts) != EXPECTED_CLASSES:
        raise RuntimeError(f"Frozen class count mismatch: {dict(class_counts)}")
    class_sources = {
        cls: len({r["source_cluster_id"] for r in joined if r["gold_class_v5"] == cls})
        for cls in EXPECTED_CLASSES
    }
    if class_sources != EXPECTED_CLASS_SOURCES:
        raise RuntimeError(f"Frozen class source-count mismatch: {class_sources}")

    error_rows = [r for r in joined if r["gold_class_v5"] == "ERROR_STRICT"]
    safe_rows = [r for r in joined if r["gold_class_v5"] == "SAFE_STRICT_CONTROL"]

    unsafe_pass_records = [r for r in error_rows if r["predicted_outcome"] == "PASS_CANDIDATE"]
    unsafe_pass_sources = sorted({r["source_cluster_id"] for r in unsafe_pass_records})
    safety_pass = len(unsafe_pass_records) == 0
    safety = {
        "population": "ERROR_STRICT",
        "record_count": len(error_rows),
        "source_count": len({r["source_cluster_id"] for r in error_rows}),
        "unsafe_event": "PASS_CANDIDATE",
        "unsafe_pass_record_count": len(unsafe_pass_records),
        "unsafe_pass_source_count": len(unsafe_pass_sources),
        "gate_pass": safety_pass,
        "zero_event_one_sided_exact_95_upper_bound_source": (
            1.0 - 0.05 ** (1.0 / len({r["source_cluster_id"] for r in error_rows}))
            if len(unsafe_pass_sources) == 0 else None
        ),
    }

    negative = utility_metrics(error_rows, "REJECT")
    positive = utility_metrics(safe_rows, "PASS_CANDIDATE")

    class_diagnostics = {}
    for cls in EXPECTED_CLASSES:
        rr = [r for r in joined if r["gold_class_v5"] == cls]
        counts = outcome_counts(rr)
        class_diagnostics[cls] = {
            "record_count": len(rr),
            "source_count": len({r["source_cluster_id"] for r in rr}),
            "outcomes": counts,
            "rates": {k: counts[k] / len(rr) for k in OUTCOMES},
        }

    per_model = {}
    for cls in EXPECTED_CLASSES:
        per_model[cls] = {}
        models = sorted({r["model_type"] for r in joined if r["gold_class_v5"] == cls})
        for model in models:
            rr = [r for r in joined if r["gold_class_v5"] == cls and r["model_type"] == model]
            counts = outcome_counts(rr)
            per_model[cls][model] = {
                "record_count": len(rr),
                "source_count": len({r["source_cluster_id"] for r in rr}),
                "outcomes": counts,
                "rates": {k: counts[k] / len(rr) for k in OUTCOMES},
            }

    if not safety_pass:
        overall = "FAIL_H1_SAFETY"
    elif negative["gate_pass"] and positive["gate_pass"]:
        overall = "FACTPICO_V5_THREE_GATE_PASS"
    else:
        overall = "H1_FULL_PASS_NOT_ACHIEVED"

    summary = {
        "scorer_id": SCORER_ID,
        "status": "SCORED_AND_FROZEN_PENDING_ARTIFACT_HASH",
        "scope": "SOURCE_BOUNDED_CRITICAL_RCT_PICO_FIDELITY_SUBGATE",
        "record_count": len(joined),
        "exact_record_id_join": True,
        "prediction_sha256": EXPECTED_PREDICTION_SHA256,
        "gold_sha256": EXPECTED_GOLD_SHA256,
        "eligibility_sha256": EXPECTED_ELIGIBILITY_SHA256,
        "bootstrap": {
            "unit": "WHOLE_SOURCE_CLUSTER",
            "source_order": "LEXICOGRAPHIC_SOURCE_CLUSTER_ID",
            "resamples": BOOTSTRAP_RESAMPLES,
            "seed": BOOTSTRAP_SEED,
            "index_generator": BOOTSTRAP_INDEX_GENERATOR,
            "percentile_method": PERCENTILE_METHOD,
            "ci": [0.025, 0.975],
        },
        "hard_safety_gate": safety,
        "negative_utility_gate": negative,
        "positive_antidegeneracy_gate": positive,
        "class_diagnostics": class_diagnostics,
        "per_model_diagnostics": per_model,
        "overall_factpico_v5_decision": overall,
        "gold_join_performed": True,
        "scoring_performed": True,
        "prediction_rerun_performed": False,
        "adaptive_change_performed": False,
        "interpretation_performed": False,
        "stop_boundary": "RESULTS_FROZEN_STOP_BEFORE_INTERPRETATION",
    }

    args.out_dir.mkdir(parents=True, exist_ok=False)
    joined_path = args.out_dir / "FACTPICO_V25_JOINED_ROWS.jsonl"
    joined_path.write_text(
        "".join(canonical_json(r) + "\n" for r in joined),
        encoding="utf-8", newline="\n"
    )
    summary_path = args.out_dir / "FACTPICO_V25_SCORING_SUMMARY.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n"
    )
    diag_path = args.out_dir / "FACTPICO_V25_CLASS_MODEL_DIAGNOSTICS.json"
    diag_path.write_text(
        json.dumps(
            {"class_diagnostics": class_diagnostics, "per_model_diagnostics": per_model},
            ensure_ascii=False, sort_keys=True, indent=2
        ) + "\n",
        encoding="utf-8", newline="\n"
    )

    freeze = {
        "scorer_id": SCORER_ID,
        "prediction_sha256": EXPECTED_PREDICTION_SHA256,
        "gold_sha256": EXPECTED_GOLD_SHA256,
        "eligibility_sha256": EXPECTED_ELIGIBILITY_SHA256,
        "joined_rows_sha256": sha256_path(joined_path),
        "scoring_summary_sha256": sha256_path(summary_path),
        "diagnostics_sha256": sha256_path(diag_path),
        "record_count": len(joined),
        "exact_record_id_join": True,
        "gold_join_performed": True,
        "scoring_performed": True,
        "prediction_rerun_performed": False,
        "interpretation_performed": False,
        "stop_boundary": "RESULTS_FROZEN_STOP_BEFORE_INTERPRETATION",
    }
    freeze_path = args.out_dir / "FACTPICO_V25_SCORING_FREEZE.json"
    freeze_path.write_text(
        json.dumps(freeze, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n"
    )
    print(json.dumps({"summary": summary, "freeze": freeze}, sort_keys=True))

if __name__ == "__main__":
    main()
