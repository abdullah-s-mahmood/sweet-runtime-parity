#!/usr/bin/env python3
"""
Score frozen AT0-EN V2.4 outcomes against the preregistered PLABA-2024 H1 contract.

This scorer performs no semantic inference and must be used only AFTER
predictions have been frozen and hashed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import random
from collections import defaultdict

ALLOWED_OUTCOMES = {
    "PASS_CANDIDATE",
    "REJECT",
    "REVIEW",
    "INVALID_VERIFICATION",
}
POSITIVE_MIN = 0.75
NEGATIVE_CONTAIN_MIN = 0.75
NEGATIVE_AUTOPASS_CLUSTER_MAX = 0
BOOTSTRAP_REPS = 10000
BOOTSTRAP_SEED = 20261004

def sha256_path(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(path: pathlib.Path):
    rows = []
    seen = set()
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        rid = row["record_id"]
        if rid in seen:
            raise RuntimeError(f"Duplicate record_id at {path}:{lineno}: {rid}")
        seen.add(rid)
        rows.append(row)
    return rows

def percentile(xs, q):
    if not xs:
        return None
    ys = sorted(xs)
    if len(ys) == 1:
        return float(ys[0])
    pos = (len(ys) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return float(ys[lo])
    frac = pos - lo
    return float(ys[lo] * (1 - frac) + ys[hi] * frac)

def bootstrap_cluster_macro(cluster_values, reps=BOOTSTRAP_REPS, seed=BOOTSTRAP_SEED):
    ids = sorted(cluster_values)
    if not ids:
        return {"estimate": None, "ci95": [None, None], "clusters": 0}
    estimate = sum(cluster_values[k] for k in ids) / len(ids)
    rng = random.Random(seed)
    boot = []
    for _ in range(reps):
        sample = [ids[rng.randrange(len(ids))] for _ in range(len(ids))]
        boot.append(sum(cluster_values[k] for k in sample) / len(sample))
    return {
        "estimate": estimate,
        "ci95": [percentile(boot, 0.025), percentile(boot, 0.975)],
        "clusters": len(ids),
        "bootstrap_replicates": reps,
        "bootstrap_seed": seed,
    }

def zero_event_upper_95(n):
    if n <= 0:
        return None
    return 1.0 - math.pow(0.05, 1.0 / n)

def score(gold_path: pathlib.Path, prediction_path: pathlib.Path, out_path: pathlib.Path):
    gold_rows = read_jsonl(gold_path)
    pred_rows = read_jsonl(prediction_path)

    gold = {r["record_id"]: r for r in gold_rows}
    pred = {r["record_id"]: r for r in pred_rows}

    if set(gold) != set(pred):
        missing = sorted(set(gold) - set(pred))
        extra = sorted(set(pred) - set(gold))
        result = {
            "status": "INVALID_H1_EVALUATION",
            "reason": "prediction_record_id_set_mismatch",
            "missing_prediction_count": len(missing),
            "extra_prediction_count": len(extra),
            "missing_prediction_ids_first20": missing[:20],
            "extra_prediction_ids_first20": extra[:20],
            "gold_sha256": sha256_path(gold_path),
            "prediction_sha256": sha256_path(prediction_path),
        }
        out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    positive_by_pmid = defaultdict(list)
    negative_by_pmid = defaultdict(list)
    middle_outcomes = defaultdict(int)
    outcome_counts = defaultdict(int)
    invalid_by_stratum = defaultdict(int)
    pass_extreme_positive = 0
    pass_extreme_negative = 0
    extreme_pass_total = 0

    negative_autopass_event_pmids = set()

    for rid, g in gold.items():
        p = pred[rid]
        outcome = p.get("predicted_outcome")
        if outcome not in ALLOWED_OUTCOMES:
            raise RuntimeError(f"Invalid predicted_outcome for {rid}: {outcome!r}")

        stratum = g["gold_stratum"]
        pmid = str(g["pmid"])
        outcome_counts[outcome] += 1
        if outcome == "INVALID_VERIFICATION":
            invalid_by_stratum[stratum] += 1

        if stratum == "EXTREME_POSITIVE":
            ok = 1.0 if outcome == "PASS_CANDIDATE" else 0.0
            positive_by_pmid[pmid].append(ok)
            if outcome == "PASS_CANDIDATE":
                pass_extreme_positive += 1
                extreme_pass_total += 1

        elif stratum == "EXTREME_NEGATIVE":
            ok = 1.0 if outcome in {"REJECT", "REVIEW"} else 0.0
            negative_by_pmid[pmid].append(ok)
            if outcome == "PASS_CANDIDATE":
                pass_extreme_negative += 1
                extreme_pass_total += 1
                negative_autopass_event_pmids.add(pmid)

        elif stratum == "MIDDLE":
            middle_outcomes[outcome] += 1
        else:
            raise RuntimeError(f"Unexpected gold stratum for {rid}: {stratum}")

    pos_cluster_values = {
        pmid: sum(vals) / len(vals) for pmid, vals in positive_by_pmid.items()
    }
    neg_cluster_values = {
        pmid: sum(vals) / len(vals) for pmid, vals in negative_by_pmid.items()
    }

    pos_metric = bootstrap_cluster_macro(pos_cluster_values)
    neg_metric = bootstrap_cluster_macro(neg_cluster_values)

    neg_event_count = len(negative_autopass_event_pmids)
    neg_cluster_count = len(negative_by_pmid)
    if neg_event_count == 0:
        neg_zero_upper = zero_event_upper_95(neg_cluster_count)
    else:
        neg_zero_upper = None

    positive_micro = (
        sum(sum(v) for v in positive_by_pmid.values())
        / sum(len(v) for v in positive_by_pmid.values())
    )
    negative_micro = (
        sum(sum(v) for v in negative_by_pmid.values())
        / sum(len(v) for v in negative_by_pmid.values())
    )

    selective_precision_extremes = (
        pass_extreme_positive / extreme_pass_total if extreme_pass_total else None
    )

    gates = {
        "positive_cluster_macro_pass_acceptance_min_0_75":
            pos_metric["estimate"] is not None and pos_metric["estimate"] >= POSITIVE_MIN,
        "negative_cluster_macro_valid_containment_min_0_75":
            neg_metric["estimate"] is not None and neg_metric["estimate"] >= NEGATIVE_CONTAIN_MIN,
        "negative_clusters_with_any_auto_pass_zero":
            neg_event_count <= NEGATIVE_AUTOPASS_CLUSTER_MAX,
    }

    if not gates["negative_clusters_with_any_auto_pass_zero"]:
        status = "FAIL_H1_UNSAFE_AUTO_PASS_ON_WORST_HUMAN_GOLD"
    elif not all(gates.values()):
        status = "MIXED_H1_UTILITY_OR_COVERAGE_FAIL"
    else:
        status = "PASS_H1_PLABA_RESEARCH_PROGRESSION"

    result = {
        "contract_id": "H1_PLABA2024_EXTREME_V1",
        "status": status,
        "gold_sha256": sha256_path(gold_path),
        "prediction_sha256": sha256_path(prediction_path),
        "eligible_record_count": len(gold),
        "positive_cluster_macro_pass_acceptance": pos_metric,
        "negative_cluster_macro_valid_containment": neg_metric,
        "positive_micro_pass_acceptance": positive_micro,
        "negative_micro_valid_containment": negative_micro,
        "negative_auto_pass": {
            "event_cluster_count": neg_event_count,
            "eligible_negative_clusters": neg_cluster_count,
            "event_pmids": sorted(negative_autopass_event_pmids),
            "one_sided_95_upper_if_zero": neg_zero_upper,
        },
        "extreme_stratum_pass_selective_precision": selective_precision_extremes,
        "invalid_verification_count_by_stratum": dict(sorted(invalid_by_stratum.items())),
        "middle_outcome_distribution": dict(sorted(middle_outcomes.items())),
        "all_outcome_counts": dict(sorted(outcome_counts.items())),
        "hard_gates": gates,
        "notes": [
            "MIDDLE has no ACAD_PASS gold mapping and is diagnostic only.",
            "INVALID_VERIFICATION remains in denominators and is not counted as success.",
            "Confidence intervals use PMID-cluster bootstrap and do not establish population representativeness.",
            "Zero-event bound is a benchmark-cluster model bound, not a general production-risk claim."
        ],
    }
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gold", type=pathlib.Path, required=True)
    p.add_argument("--predictions", type=pathlib.Path, required=True)
    p.add_argument("--out", type=pathlib.Path, required=True)
    args = p.parse_args()
    score(args.gold, args.predictions, args.out)

if __name__ == "__main__":
    main()
