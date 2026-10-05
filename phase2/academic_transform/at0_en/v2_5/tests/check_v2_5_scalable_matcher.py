#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import pathlib
import random
import subprocess
import tempfile
import time
import tracemalloc
import sys
from collections import Counter
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
V25 = HERE.parent
AT0 = V25.parent
V24 = AT0 / "v2_4"

OLD_ALIGNER = V24 / "gate_b1" / "b1_aligner.py"
NEW_ALIGNER = V25 / "gate_b1" / "b1_aligner.py"
B1_PAIRS = V24 / "gate_b1" / "B1_HUMAN_CORRECT_GRAPH_PAIRS_V1.jsonl"
B2_RAW = V24 / "gate_b2" / "B2_RAW_TEXT_PAIRS_V1.jsonl"
B2_EXTRACTOR = V24 / "gate_b2" / "b2_2_relation_aware_extractor.py"
RUNNER = V25 / "run_v2_5_batch.py"
ONE_SHOT_GUARD = V25 / "run_v2_5_one_shot_guard.py"

OUT = HERE / "results"
OUT.mkdir(parents=True, exist_ok=True)
REPORT = OUT / "V2_5_SCALABLE_MATCHER_REGRESSION_REPORT.json"

SCALABILITY_SIZES = [9, 10, 12, 16, 32, 64, 128]
SUPPORTED_MAX_N = 128
MATCHER_TIME_BUDGET_SECONDS = 30.0
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
runner = loadmod("v25_runner", RUNNER)

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


def candidate_index_tuple(groups, candidate):
    by_id = {x["id"]: i for i, x in enumerate(candidate)}
    return tuple(by_id[cg[0]["id"]] for _, cg in groups)


def exact_objective_for_perm(source, candidate, perm):
    return (
        -sum(new.owner_incompatible(s, candidate[j]) for s, j in zip(source, perm)),
        sum(
            (new.exact_jacc(new.owner_tokens(s["subject"]), new.owner_tokens(candidate[j]["subject"]))
             for s, j in zip(source, perm)),
            Fraction(0, 1),
        ),
        sum(
            (new.exact_assertion_similarity(s, candidate[j]) for s, j in zip(source, perm)),
            Fraction(0, 1),
        ),
    )


def exact_oracle(source, candidate):
    best = None
    all_rows = []
    for perm in itertools.permutations(range(len(source))):
        obj = exact_objective_for_perm(source, candidate, perm)
        all_rows.append((obj, perm))
        if best is None or obj > best[0]:
            best = (obj, perm)
    return best, all_rows


def serial_objective(obj):
    return [obj[0], str(obj[1]), str(obj[2])]


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
synthetic_objective_checked_cases = 0
legacy_float_vs_exact_discrepancies = []
for n in range(2, 7):
    # Full tie: content-identical assertions with distinct occurrence IDs.
    source = [make_assertion(0) | {"id": f"S{i:03d}"} for i in range(n)]
    candidate = [make_assertion(0) | {"id": f"C{i:03d}"} for i in range(n)]
    old_groups = old.best_one_to_one(source, candidate)
    new_groups = new.best_one_to_one(source, candidate)
    assert_same(f"full-tie-n{n}", group_signature(old_groups), group_signature(new_groups))
    (best_obj, best_perm), _ = exact_oracle(source, candidate)
    new_perm = candidate_index_tuple(new_groups, candidate)
    old_perm = candidate_index_tuple(old_groups, candidate)
    assert new_perm == best_perm
    if old_perm != best_perm:
        legacy_float_vs_exact_discrepancies.append({"case": f"full-tie-n{n}", "old": old_perm, "exact": best_perm})
    synthetic_equivalence_cases += 1
    synthetic_objective_checked_cases += 1

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
        (best_obj, best_perm), _ = exact_oracle(source, candidate)
        new_perm = candidate_index_tuple(ng, candidate)
        old_perm = candidate_index_tuple(og, candidate)
        assert new_perm == best_perm
        if old_perm != best_perm:
            legacy_float_vs_exact_discrepancies.append({
                "case": f"synthetic-n{n}-seed{seed}",
                "old": old_perm,
                "exact": best_perm,
                "exact_objective": serial_objective(best_obj),
            })
        synthetic_equivalence_cases += 1
        synthetic_objective_checked_cases += 1


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


# ---------------------------------------------------------------------------
# 7. Guardrail / failure-path mechanics
# ---------------------------------------------------------------------------
timeout_status, _ = runner.run_child_command(
    [sys.executable, "-c", "import time; time.sleep(2)"],
    "",
    0.05,
)
assert timeout_status == "TIMEOUT"

crash_status, crash_diag = runner.run_child_command(
    [sys.executable, "-c", "import sys; sys.exit(7)"],
    "",
    2.0,
)
assert crash_status == "CRASH"
assert crash_diag and "EXIT_7" in crash_diag

sample_raw = raws[sorted(raws)[0]]
sample_record = {
    "record_id": "SYN-GUARDED-VALID",
    "source_text": sample_raw["source_text"],
    "candidate_text": sample_raw["candidate_text"],
}
guarded = runner.guarded_process_record(
    sample_record,
    timeout_seconds=10.0,
    max_assertions_per_side=128,
)
assert guarded["record_id"] == sample_record["record_id"]
assert guarded["predicted_outcome"] in {"PASS_CANDIDATE", "REJECT", "REVIEW"}
assert guarded["invalid_reason"] is None

empty_invalid = runner.guarded_process_record(
    {"record_id": "SYN-EMPTY", "source_text": "", "candidate_text": "A valid sentence."},
    timeout_seconds=2.0,
    max_assertions_per_side=128,
)
assert empty_invalid["predicted_outcome"] == "INVALID_VERIFICATION"
assert empty_invalid["invalid_reason"] == "EMPTY_SOURCE_TEXT"

out_of_envelope_checked = False
for pid in sorted(raws):
    raw = raws[pid]
    sg = ra.relation_aware_extract(raw["source_text"], f"{pid}-SRC-ENV")
    cg = ra.relation_aware_extract(raw["candidate_text"], f"{pid}-CAND-ENV")
    if max(len(sg["assertions"]), len(cg["assertions"])) > 1:
        rec = {"record_id": f"SYN-ENV-{pid}", "source_text": raw["source_text"], "candidate_text": raw["candidate_text"]}
        env_invalid = runner.process_record(rec, max_assertions_per_side=1)
        assert env_invalid["predicted_outcome"] == "INVALID_VERIFICATION"
        assert env_invalid["invalid_reason"] == "ASSERTION_COUNT_OUT_OF_SUPPORTED_ENVELOPE"
        out_of_envelope_checked = True
        break
assert out_of_envelope_checked


# ---------------------------------------------------------------------------
# 8. Characterized objective-boundary cases
# ---------------------------------------------------------------------------
def simple_assertion(aid, subject, obj):
    a = make_assertion(0)
    a["id"] = aid
    a["predicate"] = "MEASURE"
    a["subject"] = subject
    a["object"] = obj
    a["bindings"] = {"value": "1", "unit": "mg"}
    a["time"] = ["day zero"]
    a["population"] = ["cohort alpha"]
    a["baseline"] = ["baseline alpha"]
    a["scope"] = ["scope alpha"]
    a["polarity"] = "POSITIVE"
    a["causality"] = "NON_CAUSAL"
    a["modality"] = "ASSERTED"
    return a


characterized_objective_cases = []

pc_source = [
    simple_assertion("PCS0", "group A", "metric x"),
    simple_assertion("PCS1", "group B", "metric y"),
]
pc_candidate = [
    simple_assertion("PCC0", "group B", "metric x"),
    simple_assertion("PCC1", "group A", "metric y"),
]
(pc_best, pc_path), _ = exact_oracle(pc_source, pc_candidate)
assert pc_path == (1, 0)
assert pc_best[0] == 0
assert exact_objective_for_perm(pc_source, pc_candidate, (0, 1))[0] == -2
assert candidate_index_tuple(new.best_one_to_one(pc_source, pc_candidate), pc_candidate) == pc_path
characterized_objective_cases.append({
    "name": "priority_conflict",
    "selected_path": pc_path,
    "objective": serial_objective(pc_best),
})

pt_source = [
    simple_assertion("PTS0", "group A", "metric alpha"),
    simple_assertion("PTS1", "group A", "metric beta"),
]
pt_candidate = [
    simple_assertion("PTC0", "group A", "metric beta"),
    simple_assertion("PTC1", "group A", "metric alpha"),
]
(pt_best, pt_path), _ = exact_oracle(pt_source, pt_candidate)
pt_alt = exact_objective_for_perm(pt_source, pt_candidate, (0, 1))
assert pt_path == (1, 0)
assert pt_best[:2] == pt_alt[:2]
assert pt_best[2] > pt_alt[2]
assert candidate_index_tuple(new.best_one_to_one(pt_source, pt_candidate), pt_candidate) == pt_path
characterized_objective_cases.append({
    "name": "partial_tie_first_two_priorities",
    "selected_path": pt_path,
    "objective": serial_objective(pt_best),
    "alternative_objective": serial_objective(pt_alt),
})

common = [f"tok_{i:03d}" for i in range(100)]
obj_a = " ".join(common + ["extra_a"])
obj_b = " ".join(common + ["extra_b"])
nt_source = [
    simple_assertion("NTS0", "group A", obj_a),
    simple_assertion("NTS1", "group A", obj_b),
]
nt_candidate = [
    simple_assertion("NTC0", "group A", obj_b),
    simple_assertion("NTC1", "group A", obj_a),
]
(nt_best, nt_path), _ = exact_oracle(nt_source, nt_candidate)
nt_alt = exact_objective_for_perm(nt_source, nt_candidate, (0, 1))
nt_gap = nt_best[2] - nt_alt[2]
assert nt_path == (1, 0)
assert nt_best[:2] == nt_alt[:2]
assert Fraction(0, 1) < nt_gap <= Fraction(1, 10)
assert candidate_index_tuple(new.best_one_to_one(nt_source, nt_candidate), nt_candidate) == nt_path
characterized_objective_cases.append({
    "name": "near_tie_semantic",
    "selected_path": nt_path,
    "objective": serial_objective(nt_best),
    "alternative_objective": serial_objective(nt_alt),
    "semantic_gap": str(nt_gap),
})

ft_source = [simple_assertion(f"FTS{i}", "group A", "same metric") for i in range(3)]
ft_candidate = [simple_assertion(f"FTC{i}", "group A", "same metric") for i in range(3)]
(ft_best, ft_path), ft_rows = exact_oracle(ft_source, ft_candidate)
assert len({row[0] for row in ft_rows}) == 1
assert ft_path == (0, 1, 2)
assert candidate_index_tuple(new.best_one_to_one(ft_source, ft_candidate), ft_candidate) == ft_path
characterized_objective_cases.append({
    "name": "full_tie_tie_policy",
    "selected_path": ft_path,
    "objective": serial_objective(ft_best),
})

for name, src, cand in [
    ("priority_conflict", pc_source, pc_candidate),
    ("partial_tie", pt_source, pt_candidate),
    ("near_tie", nt_source, nt_candidate),
    ("full_tie", ft_source, ft_candidate),
]:
    old_path = candidate_index_tuple(old.best_one_to_one(src, cand), cand)
    exact_path = exact_oracle(src, cand)[0][1]
    if old_path != exact_path:
        legacy_float_vs_exact_discrepancies.append({"case": name, "old": old_path, "exact": exact_path})


# ---------------------------------------------------------------------------
# 9. Fresh-process reproducibility + mixed-batch accounting
# ---------------------------------------------------------------------------
clean_env = os.environ.copy()
clean_env.pop("ACAD_PASS_V25_SYNTHETIC_TEST_MODE", None)
clean_env.pop("ACAD_PASS_V25_SYNTHETIC_FAULT_MAP", None)

fresh_process_reproducibility = "NOT_RUN"
mixed_batch_failure_accounting = "NOT_RUN"
output_overwrite_refusal = "NOT_RUN"
one_shot_guard_status = "NOT_RUN"

with tempfile.TemporaryDirectory(prefix="acad_pass_v25_") as td_raw:
    td = pathlib.Path(td_raw)
    selected_raw = [raws[k] for k in sorted(raws)[:2]]
    fresh_records = [
        {
            "record_id": f"SYN-FRESH-{i+1}",
            "source_text": row["source_text"],
            "candidate_text": row["candidate_text"],
        }
        for i, row in enumerate(selected_raw)
    ]
    fresh_input = td / "fresh.jsonl"
    fresh_input.write_text(
        "".join(json.dumps(x, sort_keys=True) + "\n" for x in fresh_records),
        encoding="utf-8",
    )

    def runner_cmd(out_path, input_path=fresh_input, expected_count=2, timeout="10"):
        return [
            sys.executable, str(RUNNER),
            "--input", str(input_path),
            "--output", str(out_path),
            "--expected-count", str(expected_count),
            "--timeout-seconds", timeout,
            "--max-assertions-per-side", "128",
        ]

    out1 = td / "fresh1.jsonl"
    out2 = td / "fresh2.jsonl"
    p1 = subprocess.run(runner_cmd(out1), text=True, capture_output=True, env=clean_env, check=False)
    p2 = subprocess.run(runner_cmd(out2), text=True, capture_output=True, env=clean_env, check=False)
    assert p1.returncode == 0, p1.stderr
    assert p2.returncode == 0, p2.stderr
    assert out1.read_bytes() == out2.read_bytes()
    fresh_process_reproducibility = "PASS"

    overwrite = subprocess.run(runner_cmd(out1), text=True, capture_output=True, env=clean_env, check=False)
    assert overwrite.returncode != 0
    assert "Refusing to overwrite existing prediction output" in (overwrite.stderr + overwrite.stdout)
    output_overwrite_refusal = "PASS"

    mixed_records = [
        {**fresh_records[0], "record_id": "SYN-OK-1"},
        {**fresh_records[0], "record_id": "SYN-TIMEOUT"},
        {**fresh_records[1], "record_id": "SYN-CRASH"},
        {**fresh_records[1], "record_id": "SYN-OK-2"},
    ]
    mixed_input = td / "mixed.jsonl"
    mixed_input.write_text(
        "".join(json.dumps(x, sort_keys=True) + "\n" for x in mixed_records),
        encoding="utf-8",
    )
    mixed_output = td / "mixed_out.jsonl"
    fault_env = clean_env.copy()
    fault_env["ACAD_PASS_V25_SYNTHETIC_TEST_MODE"] = "1"
    fault_env["ACAD_PASS_V25_SYNTHETIC_FAULT_MAP"] = json.dumps({
        "SYN-TIMEOUT": "TIMEOUT",
        "SYN-CRASH": "CRASH",
    }, sort_keys=True)
    mixed = subprocess.run(
        runner_cmd(mixed_output, mixed_input, 4, "10"),
        text=True, capture_output=True, env=fault_env, check=False,
    )
    assert mixed.returncode == 0, mixed.stderr
    mixed_rows = rows(mixed_output)
    assert [x["record_id"] for x in mixed_rows] == [x["record_id"] for x in mixed_records]
    assert len(mixed_rows) == 4
    by_id = {x["record_id"]: x for x in mixed_rows}
    assert by_id["SYN-TIMEOUT"]["predicted_outcome"] == "INVALID_VERIFICATION"
    assert by_id["SYN-TIMEOUT"]["invalid_reason"] == "RECORD_TIMEOUT"
    assert by_id["SYN-CRASH"]["predicted_outcome"] == "INVALID_VERIFICATION"
    assert by_id["SYN-CRASH"]["invalid_reason"] == "CHILD_PROCESS_CRASH"
    assert by_id["SYN-OK-1"]["predicted_outcome"] != "INVALID_VERIFICATION"
    assert by_id["SYN-OK-2"]["predicted_outcome"] != "INVALID_VERIFICATION"
    mixed_batch_failure_accounting = "PASS"

    guard_input_sha = hashlib.sha256(fresh_input.read_bytes()).hexdigest()
    attempt_dir = td / "attempt"
    guard_cmd = [
        sys.executable, str(ONE_SHOT_GUARD),
        "--input", str(fresh_input),
        "--attempt-dir", str(attempt_dir),
        "--attempt-id", "SYN-ONE-SHOT-001",
        "--runner", str(RUNNER),
        "--timeout-seconds", "10",
        "--max-assertions-per-side", "128",
        "--expected-input-sha256", guard_input_sha,
        "--expected-count", "2",
    ]
    g1 = subprocess.run(guard_cmd, text=True, capture_output=True, env=clean_env, check=False)
    assert g1.returncode == 0, g1.stderr
    assert (attempt_dir / "ATTEMPT_CLAIM.json").exists()
    assert (attempt_dir / "FACTPICO_V25_PREDICTIONS.jsonl").exists()
    assert (attempt_dir / "PREDICTION_FREEZE.json").exists()
    freeze = json.loads((attempt_dir / "PREDICTION_FREEZE.json").read_text(encoding="utf-8"))
    frozen_predictions = attempt_dir / "FACTPICO_V25_PREDICTIONS.jsonl"
    assert freeze["prediction_sha256"] == hashlib.sha256(frozen_predictions.read_bytes()).hexdigest()
    g2 = subprocess.run(guard_cmd, text=True, capture_output=True, env=clean_env, check=False)
    assert g2.returncode != 0
    assert "Attempt directory already exists" in (g2.stderr + g2.stdout)
    one_shot_guard_status = "PASS"


# ---------------------------------------------------------------------------
# 10. Maximum-tie and near-envelope unequal-count shapes
# ---------------------------------------------------------------------------
max_shape_results = []

tie_n = 128
tie_source = [simple_assertion(f"MTS{i:03d}", "group A", "same metric") for i in range(tie_n)]
tie_candidate = [simple_assertion(f"MTC{i:03d}", "group A", "same metric") for i in range(tie_n)]
tie_times = []
tie_peaks = []
for tie_repeat in range(3):
    tracemalloc.start()
    t0 = time.perf_counter()
    tie_groups = new.best_one_to_one(tie_source, tie_candidate)
    tie_elapsed = time.perf_counter() - t0
    _, tie_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"MAX_TIE_128_REPEAT_{tie_repeat+1}_SECONDS={tie_elapsed:.6f}")
    print(f"MAX_TIE_128_REPEAT_{tie_repeat+1}_TRACEMALLOC_BYTES={tie_peak}")
    assert candidate_index_tuple(tie_groups, tie_candidate) == tuple(range(tie_n))
    assert tie_elapsed <= MATCHER_TIME_BUDGET_SECONDS
    assert tie_peak <= PEAK_MEMORY_BUDGET_BYTES
    tie_times.append(tie_elapsed)
    tie_peaks.append(tie_peak)
max_shape_results.append({
    "shape": "128x128_full_tie",
    "run_seconds": tie_times,
    "max_seconds": max(tie_times),
    "tracemalloc_peak_bytes": max(tie_peaks),
    "status": "PASS",
})

for s_count, c_count in [(127, 128), (128, 127)]:
    src = [make_assertion(i) | {"id": f"US{i:03d}"} for i in range(s_count)]
    cand = [make_assertion(i) | {"id": f"UC{i:03d}"} for i in range(c_count)]
    t0 = time.perf_counter()
    groups = new.assertion_groups(src, cand)
    elapsed = time.perf_counter() - t0
    assert elapsed <= MATCHER_TIME_BUDGET_SECONDS
    if s_count < c_count:
        assert len(groups[-1][1]) == 2
    else:
        assert len(groups[-1][0]) == 2
    max_shape_results.append({
        "shape": f"{s_count}x{c_count}_unequal_prefix",
        "seconds": elapsed,
        "status": "PASS",
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
    "synthetic_objective_checked_cases": synthetic_objective_checked_cases,
    "characterized_objective_cases": characterized_objective_cases,
    "legacy_float_vs_exact_discrepancies": legacy_float_vs_exact_discrepancies,
    "grouping_boundary_cases": boundary_cases,
    "fresh_process_reproducibility": fresh_process_reproducibility,
    "mixed_batch_failure_accounting": mixed_batch_failure_accounting,
    "output_overwrite_refusal": output_overwrite_refusal,
    "one_shot_guard": one_shot_guard_status,
    "max_shape_results": max_shape_results,
    "downstream_tie_case": "PASS",
    "scalability": scalability,
    "supported_max_n": SUPPORTED_MAX_N,
    "guardrail_tests": {"timeout": "PASS", "crash": "PASS", "valid_child": "PASS", "empty_input": "PASS", "out_of_envelope": "PASS", "retry_count": 0},
    "matcher_time_budget_seconds": MATCHER_TIME_BUDGET_SECONDS,
    "peak_memory_budget_bytes": PEAK_MEMORY_BUDGET_BYTES,
}

REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, sort_keys=True))
