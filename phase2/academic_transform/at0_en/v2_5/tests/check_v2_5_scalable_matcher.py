#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import itertools
import json
import pathlib
import random
import time
import tracemalloc
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
V25 = HERE.parent
AT0 = V25.parent
V24 = AT0 / "v2_4"

OLD_ALIGNER = V24 / "gate_b1" / "b1_aligner.py"
NEW_ALIGNER = V25 / "gate_b1" / "b1_aligner.py"
B1_PAIRS = V24 / "gate_b1" / "B1_HUMAN_CORRECT_GRAPH_PAIRS_V1.jsonl"
B2_RAW = V24 / "gate_b2" / "B2_RAW_TEXT_PAIRS_V1.jsonl"
B2_EXTRACTOR = V24 / "gate_b2" / "b2_2_relation_aware_extractor.py"

OUT = HERE / "results"
OUT.mkdir(parents=True, exist_ok=True)
REPORT = OUT / "V2_5_SCALABLE_MATCHER_REGRESSION_REPORT.json"

SCALABILITY_SIZES = [9, 10, 12, 16, 32, 64, 128]
SUPPORTED_MAX_N = 128
MATCHER_TIME_BUDGET_SECONDS = 10.0
PEAK_MEMORY_BUDGET_BYTES = 512 * 1024 * 1024


def loadmod(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rows(path: pathlib.Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


old = loadmod("v24_b1", OLD_ALIGNER)
new = loadmod("v25_b1", NEW_ALIGNER)
ra = loadmod("v24_ra", B2_EXTRACTOR)

pairs = rows(B1_PAIRS)
raws = {x["pair_id"]: x for x in rows(B2_RAW)}

assert len(pairs) == 12
assert {x["pair_id"] for x in pairs} == set(raws)


def candidate_tuple(groups):
    out = []
    for _, cg in groups:
        if len(cg) != 1:
            raise AssertionError("candidate_tuple only valid for one-to-one groups")
        out.append(cg[0]["id"])
    return tuple(out)


def group_signature(groups):
    return [
        (
            tuple(x["id"] for x in sg),
            tuple(x["id"] for x in cg),
        )
        for sg, cg in groups
    ]


def assert_same(label, a, b):
    if a != b:
        raise AssertionError(f"{label} mismatch\nOLD={a!r}\nNEW={b!r}")


# ---------------------------------------------------------------------------
# 1. Existing B1 exact integration regression
# ---------------------------------------------------------------------------
b1_diffs = []
for p in pairs:
    op = old.align_pair(p)
    np = new.align_pair(p)
    if op != np:
        b1_diffs.append({
            "pair_id": p["pair_id"],
            "old": op,
            "new": np,
        })

if b1_diffs:
    raise AssertionError(f"B1 integration differences: {[x['pair_id'] for x in b1_diffs]}")


# ---------------------------------------------------------------------------
# 2. Existing B2.2 four-arm regression using unchanged V2.4 extractor
# ---------------------------------------------------------------------------
arm_names = ["GG", "GE", "EG", "EE"]
b2_diffs = []
b2_outcomes = {arm: [] for arm in arm_names}

for p in pairs:
    pid = p["pair_id"]
    raw = raws[pid]
    source_ex = ra.relation_aware_extract(raw["source_text"], f"{pid}-SRC")
    cand_ex = ra.relation_aware_extract(raw["candidate_text"], f"{pid}-CAND")

    arm_graphs = {
        "GG": (p["source_graph"], p["candidate_graph"]),
        "GE": (p["source_graph"], cand_ex),
        "EG": (source_ex, p["candidate_graph"]),
        "EE": (source_ex, cand_ex),
    }

    for arm, (sg, cg) in arm_graphs.items():
        pair_obj = {"pair_id": pid, "source_graph": sg, "candidate_graph": cg}
        op = old.align_pair(pair_obj)
        np = new.align_pair(pair_obj)
        if op != np:
            b2_diffs.append({
                "pair_id": pid,
                "arm": arm,
                "old": op,
                "new": np,
            })
        b2_outcomes[arm].append((pid, p["expected_outcome"], np["predicted_outcome"]))

if b2_diffs:
    raise AssertionError(
        "B2 integration differences: "
        + repr([(x["pair_id"], x["arm"]) for x in b2_diffs])
    )


def arm_metrics(records):
    total = len(records)
    correct = sum(exp == pred for _, exp, pred in records)
    safe = [(pid, pred) for pid, exp, pred in records if exp == "PASS_CANDIDATE"]
    adv = [(pid, pred) for pid, exp, pred in records if exp == "REJECT"]
    review = [(pid, pred) for pid, exp, pred in records if exp == "REVIEW"]
    return {
        "total": total,
        "correct": correct,
        "safe_total": len(safe),
        "safe_pass": sum(pred == "PASS_CANDIDATE" for _, pred in safe),
        "unsafe_adversarial_pass": sum(pred == "PASS_CANDIDATE" for _, pred in adv),
        "review_total": len(review),
        "review_preserved": sum(pred == "REVIEW" for _, pred in review),
        "outcome_counts": dict(Counter(pred for _, _, pred in records)),
    }


b2_metrics = {arm: arm_metrics(b2_outcomes[arm]) for arm in arm_names}

# Required canonical B2.2 behavior.
assert b2_metrics["EE"]["correct"] == 12
assert b2_metrics["EE"]["safe_pass"] == 5
assert b2_metrics["EE"]["unsafe_adversarial_pass"] == 0
assert b2_metrics["EE"]["review_preserved"] == 1
assert b2_metrics["GG"]["correct"] == 12


# ---------------------------------------------------------------------------
# 3. Synthetic exhaustive assignment equivalence oracle, n=2..6
# ---------------------------------------------------------------------------
def make_assertion(i: int, variant: int = 0):
    return {
        "id": f"A{i:03d}",
        "predicate": ["MEASURE", "REDUCE", "INCREASE", "DEFINE"][i % 4],
        "subject": f"group {chr(65 + (i % 6))}",
        "object": f"metric {i % 5}",
        "bindings": {"value": str((i * 3 + variant) % 17), "unit": "mg"},
        "time": [f"day {i % 4}"],
        "population": [f"cohort {i % 3}"],
        "baseline": [f"base {i % 2}"],
        "scope": [f"scope {i % 5}"],
        "polarity": "POSITIVE" if i % 2 == 0 else "NEGATIVE",
        "causality": "NON_CAUSAL",
        "modality": "ASSERTED",
        "confidence_status": "CERTAIN",
        "criticality": "CRITICAL",
        "evidence": f"synthetic evidence {i}",
    }


def mutate_candidate(a, rng):
    a = dict(a)
    a["bindings"] = dict(a["bindings"])
    for key in ["time", "population", "baseline", "scope"]:
        a[key] = list(a[key])
    if rng.random() < 0.20:
        a["subject"] = f"group {chr(65 + ((int(a['id'][1:]) + 1) % 6))}"
    if rng.random() < 0.20:
        idx = int(a["id"][1:])
        a["object"] = f"metric {(idx + 1) % 5}"
    if rng.random() < 0.15:
        a["bindings"]["value"] = str((int(a["bindings"]["value"]) + 1) % 17)
    return a


synthetic_equivalence_cases = 0
for n in range(2, 7):
    # Full tie: content-identical assertions with distinct occurrence IDs.
    source = [make_assertion(0) | {"id": f"S{i:03d}"} for i in range(n)]
    candidate = [make_assertion(0) | {"id": f"C{i:03d}"} for i in range(n)]
    assert_same(
        f"full-tie-n{n}",
        group_signature(old.best_one_to_one(source, candidate)),
        group_signature(new.best_one_to_one(source, candidate)),
    )
    synthetic_equivalence_cases += 1

    for seed in range(40):
        rng = random.Random(20261005 + n * 1000 + seed)
        source = [make_assertion(i) for i in range(n)]
        order = list(range(n))
        rng.shuffle(order)
        candidate = []
        for j in order:
            a = make_assertion(j, seed % 3)
            a["id"] = f"C{j:03d}"
            candidate.append(mutate_candidate(a, rng))

        og = old.best_one_to_one(source, candidate)
        ng = new.best_one_to_one(source, candidate)
        assert_same(f"synthetic-n{n}-seed{seed}", group_signature(og), group_signature(ng))
        synthetic_equivalence_cases += 1


# ---------------------------------------------------------------------------
# 4. Grouping / boundary behavior
# ---------------------------------------------------------------------------
boundary_cases = []
for s_count, c_count in [(1, 3), (3, 1), (3, 4), (4, 3), (4, 4)]:
    s = [make_assertion(i) | {"id": f"S{i}"} for i in range(s_count)]
    c = [make_assertion(i) | {"id": f"C{i}"} for i in range(c_count)]
    osig = group_signature(old.assertion_groups(s, c))
    nsig = group_signature(new.assertion_groups(s, c))
    assert_same(f"grouping-{s_count}x{c_count}", osig, nsig)
    boundary_cases.append({"source": s_count, "candidate": c_count, "signature": nsig})

# Empty matcher boundary is newly explicit at helper level.
assert new.best_one_to_one([], []) == []


# ---------------------------------------------------------------------------
# 5. Downstream tie-sensitivity case
# ---------------------------------------------------------------------------
base = make_assertion(0)
s1 = dict(base) | {"id": "S1"}
s2 = dict(base) | {"id": "S2"}
c1 = dict(base) | {"id": "C1"}
c2 = dict(base) | {"id": "C2"}

source_graph = {
    "assertions": [s1, s2],
    "relations": [{
        "id": "R1", "type": "PRECEDES", "from": "S1", "to": "S2",
        "criticality": "CRITICAL", "confidence_status": "CERTAIN",
        "evidence": "synthetic tie relation",
    }],
}
candidate_graph = {
    "assertions": [c1, c2],
    "relations": [{
        "id": "R2", "type": "PRECEDES", "from": "C1", "to": "C2",
        "criticality": "CRITICAL", "confidence_status": "CERTAIN",
        "evidence": "synthetic tie relation",
    }],
}
tie_pair = {"pair_id": "SYN-TIE-DOWNSTREAM", "source_graph": source_graph, "candidate_graph": candidate_graph}
assert_same("downstream-tie", old.align_pair(tie_pair), new.align_pair(tie_pair))


# ---------------------------------------------------------------------------
# 6. Synthetic scalability and reproducibility
# ---------------------------------------------------------------------------
scalability = []
for n in SCALABILITY_SIZES:
    source = [make_assertion(i) | {"id": f"S{i:03d}"} for i in range(n)]
    candidate = [make_assertion(n - 1 - i, 1) | {"id": f"C{n - 1 - i:03d}"} for i in range(n)]

    mappings = []
    times = []
    peaks = []
    for repeat in range(2):
        tracemalloc.start()
        t0 = time.perf_counter()
        groups = new.best_one_to_one(source, candidate)
        elapsed = time.perf_counter() - t0
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        mappings.append(group_signature(groups))
        times.append(elapsed)
        peaks.append(peak)

    assert mappings[0] == mappings[1]
    assert max(times) <= MATCHER_TIME_BUDGET_SECONDS, (n, times)
    assert max(peaks) <= PEAK_MEMORY_BUDGET_BYTES, (n, peaks)

    scalability.append({
        "n": n,
        "run_seconds": times,
        "peak_memory_bytes": peaks,
        "reproducible": True,
    })


report = {
    "gate": "AT0_EN_V2_5_SCALABLE_MATCHER_REGRESSION",
    "status": "PASS",
    "factpico_used": False,
    "old_runtime": "AT0-EN V2.4",
    "new_runtime": "AT0-EN V2.5",
    "numeric_policy": new.V2_5_MATCHER_NUMERIC_POLICY,
    "algorithm": new.V2_5_MATCHER_ALGORITHM,
    "b1_pair_count": len(pairs),
    "b1_exact_output_differences": 0,
    "b2_arm_exact_output_differences": 0,
    "b2_metrics": b2_metrics,
    "synthetic_exhaustive_equivalence_cases": synthetic_equivalence_cases,
    "grouping_boundary_cases": boundary_cases,
    "downstream_tie_case": "PASS",
    "scalability": scalability,
    "supported_max_n": SUPPORTED_MAX_N,
    "matcher_time_budget_seconds": MATCHER_TIME_BUDGET_SECONDS,
    "peak_memory_budget_bytes": PEAK_MEMORY_BUDGET_BYTES,
}

REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, sort_keys=True))
