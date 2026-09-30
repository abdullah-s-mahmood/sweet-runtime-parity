#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

JACCARD_THRESHOLD = 0.90
LENGTH_RATIO_THRESHOLD = 0.90
EXPECTED_TOTAL = 6888
EXPECTED_TRAIN = 6571
EXPECTED_DEV = 317
EXPECTED_CLUSTERS = 6871
EXPECTED_NON_SINGLETON = 15
EXPECTED_MAX_CLUSTER = 4
EXPECTED_DEV_CLUSTERS = 317
EXPECTED_CROSS_SPLIT_CLUSTERS = 0


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_key(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


class DSU:
    def __init__(self, n: int):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1


def build_clusters(rows):
    norms = []
    words = []
    token_sets = []

    for row in rows:
        norm = source_key(row["source"])
        toks = norm.split()
        norms.append(norm)
        words.append(toks)
        token_sets.append(set(toks))

    dsu = DSU(len(rows))

    exact = defaultdict(list)
    for i, norm in enumerate(norms):
        exact[norm].append(i)
    for inds in exact.values():
        for j in inds[1:]:
            dsu.union(inds[0], j)

    freq = Counter()
    for token_set in token_sets:
        freq.update(token_set)

    ordered = [
        sorted(token_set, key=lambda token: (freq[token], token))
        for token_set in token_sets
    ]

    inverted = defaultdict(list)
    candidate_pairs = set()

    for i, toks in enumerate(ordered):
        n = len(toks)
        if n == 0:
            continue

        # Exact AllPairs prefix filtering for Jaccard threshold.
        prefix_len = n - math.ceil(JACCARD_THRESHOLD * n) + 1
        prefix_len = max(1, min(n, prefix_len))

        for token in toks[:prefix_len]:
            for j in inverted[token]:
                a, b = len(token_sets[j]), n
                if a == 0:
                    continue
                if min(a, b) / max(a, b) < JACCARD_THRESHOLD:
                    continue

                wj, wi = len(words[j]), len(words[i])
                if wj == 0 or wi == 0:
                    continue
                if min(wj, wi) / max(wj, wi) < LENGTH_RATIO_THRESHOLD:
                    continue

                candidate_pairs.add((j, i))

            inverted[token].append(i)

    near_edges = []
    for j, i in sorted(candidate_pairs):
        union = token_sets[j] | token_sets[i]
        jaccard = (
            len(token_sets[j] & token_sets[i]) / len(union)
            if union
            else 1.0
        )
        length_ratio = min(len(words[j]), len(words[i])) / max(
            len(words[j]), len(words[i])
        )

        if (
            jaccard >= JACCARD_THRESHOLD
            and length_ratio >= LENGTH_RATIO_THRESHOLD
        ):
            dsu.union(j, i)
            near_edges.append(
                {
                    "uid_a": rows[j]["uid"],
                    "uid_b": rows[i]["uid"],
                    "jaccard": jaccard,
                    "length_ratio": length_ratio,
                }
            )

    comps = defaultdict(list)
    for i in range(len(rows)):
        comps[dsu.find(i)].append(i)

    clusters = []
    cluster_by_index = {}

    for inds in comps.values():
        uids = sorted(rows[i]["uid"] for i in inds)
        cluster_id = sha256_bytes("\n".join(uids).encode("utf-8"))
        clusters.append((cluster_id, sorted(inds)))
        for i in inds:
            cluster_by_index[i] = cluster_id

    clusters.sort(key=lambda item: item[0])
    return clusters, cluster_by_index, near_edges


def write_json(path: Path, obj) -> None:
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, items) -> None:
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    cal_path = Path(args.calibration)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    rows = [
        json.loads(line)
        for line in cal_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    split_counts = Counter(row["split"] for row in rows)

    if len(rows) != EXPECTED_TOTAL:
        raise SystemExit(f"total mismatch: {len(rows)} != {EXPECTED_TOTAL}")
    if split_counts["train"] != EXPECTED_TRAIN:
        raise SystemExit(
            f"train mismatch: {split_counts['train']} != {EXPECTED_TRAIN}"
        )
    if split_counts["dev"] != EXPECTED_DEV:
        raise SystemExit(
            f"dev mismatch: {split_counts['dev']} != {EXPECTED_DEV}"
        )

    clusters, cluster_by_index, near_edges = build_clusters(rows)

    non_singleton = sum(len(inds) > 1 for _, inds in clusters)
    max_cluster = max(len(inds) for _, inds in clusters)

    cross_split_clusters = []
    dev_cluster_ids = []

    cluster_records = []
    for cluster_id, inds in clusters:
        splits = sorted({rows[i]["split"] for i in inds})
        if "dev" in splits:
            dev_cluster_ids.append(cluster_id)
        if len(splits) > 1:
            cross_split_clusters.append(cluster_id)

        cluster_records.append(
            {
                "cluster_id": cluster_id,
                "size": len(inds),
                "uids": sorted(rows[i]["uid"] for i in inds),
                "case_ids": sorted(rows[i]["case_id"] for i in inds),
                "original_splits": splits,
                "contains_dev": "dev" in splits,
                "contains_train": "train" in splits,
            }
        )

    observed = {
        "total_records": len(rows),
        "train_records": split_counts["train"],
        "dev_records": split_counts["dev"],
        "total_clusters": len(clusters),
        "non_singleton_clusters": non_singleton,
        "max_cluster_size": max_cluster,
        "dev_clusters": len(dev_cluster_ids),
        "cross_split_clusters": len(cross_split_clusters),
        "near_duplicate_edges": len(near_edges),
    }

    expected = {
        "total_records": EXPECTED_TOTAL,
        "train_records": EXPECTED_TRAIN,
        "dev_records": EXPECTED_DEV,
        "total_clusters": EXPECTED_CLUSTERS,
        "non_singleton_clusters": EXPECTED_NON_SINGLETON,
        "max_cluster_size": EXPECTED_MAX_CLUSTER,
        "dev_clusters": EXPECTED_DEV_CLUSTERS,
        "cross_split_clusters": EXPECTED_CROSS_SPLIT_CLUSTERS,
    }

    for key, value in expected.items():
        if observed[key] != value:
            raise SystemExit(
                f"preflight mismatch {key}: {observed[key]} != {value}"
            )

    exposure = []
    feasibility = []
    train_internal = []

    for i, row in enumerate(rows):
        cluster_id = cluster_by_index[i]
        original_split = row["split"]
        is_dev = original_split == "dev"

        record = {
            "case_id": row["case_id"],
            "uid": row["uid"],
            "original_split": original_split,
            "line_no": row["line_no"],
            "cluster_id": cluster_id,
            "source_sha256": sha256_bytes(row["source"].encode("utf-8")),
            "feasibility_population": (
                "D_DEV_FEAS_V1" if is_dev else "D_TRAIN_INTERNAL_V1"
            ),
            # Conservative exposure state from frozen project history.
            "source_only_exposed": True,
            "gold_exposed": True,
            "aggregate_result_exposed": True,
            "error_analysis_exposed": False,
            "fit_exposed": False,
            "threshold_selection_exposed": False,
            "unknown_exposure": True,
            "proposer_training_overlap_status": (
                "MODEL_DEVELOPMENT_EVALUATION_EXPOSURE"
                if is_dev
                else "KNOWN_OR_HIGHLY_EXPECTED_DIRECT_TRAIN_OVERLAP"
            ),
            "independence_claim_allowed": False,
        }
        exposure.append(record)

        member = {
            "case_id": row["case_id"],
            "uid": row["uid"],
            "original_split": original_split,
            "line_no": row["line_no"],
            "cluster_id": cluster_id,
            "source_sha256": record["source_sha256"],
        }

        if is_dev:
            feasibility.append(member)
        else:
            train_internal.append(member)

    # Strong membership integrity.
    all_ids = {row["case_id"] for row in rows}
    exposure_ids = {row["case_id"] for row in exposure}
    feas_ids = {row["case_id"] for row in feasibility}
    train_ids = {row["case_id"] for row in train_internal}

    if exposure_ids != all_ids:
        raise SystemExit("exposure ledger membership mismatch")
    if feas_ids & train_ids:
        raise SystemExit("dev/train population overlap")
    if feas_ids | train_ids != all_ids:
        raise SystemExit("dev/train population coverage mismatch")
    if len(feasibility) != EXPECTED_DEV:
        raise SystemExit("feasibility population size mismatch")
    if any(item["original_split"] != "dev" for item in feasibility):
        raise SystemExit("train record found in feasibility population")

    dev_clusters_in_manifest = {item["cluster_id"] for item in feasibility}
    train_clusters_in_manifest = {item["cluster_id"] for item in train_internal}
    if dev_clusters_in_manifest & train_clusters_in_manifest:
        raise SystemExit("cross-split cluster found in population manifests")

    write_jsonl(out / "MPSEF_EXPOSURE_LEDGER_V1.jsonl", exposure)
    write_jsonl(out / "MPSEF_CLUSTER_MAP_V1.jsonl", cluster_records)
    write_jsonl(out / "MPSEF_FEASIBILITY_POPULATION_V1.jsonl", feasibility)
    write_jsonl(out / "MPSEF_TRAIN_INTERNAL_POPULATION_V1.jsonl", train_internal)
    write_jsonl(out / "MPSEF_NEAR_DUPLICATE_EDGES_V1.jsonl", near_edges)

    exposure_summary = {
        "record_id": "MPSEF_EXPOSURE_LEDGER_SUMMARY_V1",
        "records": len(exposure),
        "all_gold_exposed": all(x["gold_exposed"] for x in exposure),
        "all_aggregate_result_exposed": all(
            x["aggregate_result_exposed"] for x in exposure
        ),
        "all_independence_claim_allowed_false": all(
            not x["independence_claim_allowed"] for x in exposure
        ),
        "train_overlap_status_counts": dict(
            Counter(x["proposer_training_overlap_status"] for x in exposure)
        ),
        "unknown_exposure_records": sum(
            x["unknown_exposure"] for x in exposure
        ),
    }

    cluster_summary = {
        "record_id": "MPSEF_CLUSTER_MAP_SUMMARY_V1",
        **observed,
        "jaccard_threshold": JACCARD_THRESHOLD,
        "length_ratio_threshold": LENGTH_RATIO_THRESHOLD,
        "cross_split_cluster_ids": cross_split_clusters,
    }

    feasibility_summary = {
        "record_id": "MPSEF_FEASIBILITY_POPULATION_SUMMARY_V1",
        "population_id": "D_DEV_FEAS_V1",
        "records": len(feasibility),
        "clusters": len(dev_clusters_in_manifest),
        "original_split": "dev",
        "training_origin_records": 0,
        "independence_status": "DEVELOPMENTAL_NOT_INDEPENDENT",
        "candidate_metric_computed": False,
    }

    train_summary = {
        "record_id": "MPSEF_TRAIN_INTERNAL_POPULATION_SUMMARY_V1",
        "population_id": "D_TRAIN_INTERNAL_V1",
        "records": len(train_internal),
        "clusters": len(train_clusters_in_manifest),
        "original_split": "train",
        "primary_feasibility_use_allowed": False,
        "candidate_metric_computed": False,
    }

    preflight = {
        "record_id": "MPSEF_PRE_UNION_MANIFEST_PREFLIGHT_V1",
        "status": "PASS",
        "calibration_sha256": sha256_file(cal_path),
        "observed": observed,
        "expected": expected,
        "feasibility_population_records": len(feasibility),
        "feasibility_population_clusters": len(dev_clusters_in_manifest),
        "train_internal_records": len(train_internal),
        "train_internal_clusters": len(train_clusters_in_manifest),
        "population_cluster_overlap": 0,
        "candidate_metric_computed": False,
        "reference_content_used_for_manifest_generation": False,
        "gold_edit_content_used_for_manifest_generation": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
        "reserved_data_opened": False,
    }

    write_json(out / "MPSEF_EXPOSURE_LEDGER_SUMMARY_V1.json", exposure_summary)
    write_json(out / "MPSEF_CLUSTER_MAP_SUMMARY_V1.json", cluster_summary)
    write_json(
        out / "MPSEF_FEASIBILITY_POPULATION_SUMMARY_V1.json",
        feasibility_summary,
    )
    write_json(
        out / "MPSEF_TRAIN_INTERNAL_POPULATION_SUMMARY_V1.json",
        train_summary,
    )
    write_json(out / "MPSEF_PRE_UNION_MANIFEST_PREFLIGHT_V1.json", preflight)

    # Hash all produced evidence files.
    output_files = sorted(
        p for p in out.iterdir()
        if p.is_file() and p.name != "MPSEF_PRE_UNION_MANIFEST_SHA256.txt"
    )
    with (out / "MPSEF_PRE_UNION_MANIFEST_SHA256.txt").open(
        "w", encoding="utf-8"
    ) as f:
        for path in output_files:
            f.write(f"{sha256_file(path)}  {path.name}\n")

    print(json.dumps(preflight, ensure_ascii=False, indent=2), flush=True)
    print("RUN_COMPLETE MPSEF_PRE_UNION_MANIFESTS_V1", flush=True)


if __name__ == "__main__":
    main()
