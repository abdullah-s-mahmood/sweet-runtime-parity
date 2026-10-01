#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import time
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import mpsef_v4_stage1_source_only_analysis_v1 as base
from process_progress_v1 import update_state

VERSION = "MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_ANALYSIS_V1"
ACTIONSET_VERSION = "MPSEF_V4_STAGE2_SOURCE_ONLY_ACTION_SET_V1"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"
STAGE_B_VERSION = "MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1"

EXPECTED_SOURCE_SHA = "051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_P1_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P2_SHA = "87dd3600293b215172f5a75dc7485915013963aa3e661310ea1adac08b9ddba7"
EXPECTED_P3_SHA = "02f9bd2555b1b9f350665179dcd96dd6accf532355a269b38ef4d099ea25d4ec"
EXPECTED_REGISTRY_SHA = "b448650c571f6c93dffe4825417e4f65d6a8cd02e33bd9551728ceac2b242b1a"
EXPECTED_CASES = 1918
EXPECTED_CLUSTERS = 764

FAMILIES = ("SWEET_QALB14", "SEQ2SEQ_GED_MORPH")
STAGE_B_CATEGORIES = (
    "NO_CHANGE_FROM_P1",
    "PUNCTUATION_ONLY_FROM_P1",
    "BOUNDARY_ONLY_FROM_P1",
    "LEXICAL_ONLY_FROM_P1",
    "MIXED_FROM_P1",
    "UNAVAILABLE_COMPARISON",
)

# Reuse the exact frozen Stage1 legalizer/action-set semantics, but give
# Stage2 action identities their own version namespace.
base.ACTIONSET_VERSION = ACTIONSET_VERSION


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def nearest_rank(values, q=0.95):
    return base.quantile_nearest_rank(values, q)


def stat(values):
    return base.stats(values)


def distinct_cluster_count(rows, predicate):
    return len({r["cluster_id"] for r in rows if predicate(r)})


def histogram_uid_cluster(rows, category_fn, categories):
    uid = Counter()
    clusters = {c: set() for c in categories}
    for row in rows:
        cat = category_fn(row)
        if cat not in uid and cat not in clusters:
            raise RuntimeError(f"UNKNOWN_HISTOGRAM_CATEGORY:{cat}")
        uid[cat] += 1
        clusters[cat].add(row["cluster_id"])
    return {
        "uid_counts": {c: uid[c] for c in categories},
        "cluster_presence_counts": {c: len(clusters[c]) for c in categories},
        "cluster_bins_may_overlap": True,
        "cluster_semantics": (
            "distinct cluster_id values containing at least one qualifying UID"
        ),
    }


def remove_family(action_set, family_id):
    retained = []
    for action in action_set["actions"]:
        if action["keep_semantics"]:
            retained.append({
                "output": action["output"],
                "keep_semantics": True,
                "provenance": [
                    p for p in action["provenance"]
                    if p.get("family_id") != family_id
                ],
            })
            continue
        kept = [
            p for p in action["provenance"]
            if p.get("family_id") != family_id
        ]
        if kept:
            retained.append({
                "output": action["output"],
                "keep_semantics": False,
                "provenance": kept,
            })
    return retained


def nonkeep_actions(actions):
    return [a for a in actions if not a["keep_semantics"]]


def family_set_for_action_set(action_set):
    fam = set()
    for action in action_set["actions"]:
        if action["keep_semantics"]:
            continue
        fam.update(
            p["family_id"]
            for p in action["provenance"]
            if p.get("family_id") in FAMILIES
        )
    return fam


def family_availability_state(fams):
    if not fams:
        return "NONE"
    if fams == {"SWEET_QALB14"}:
        return "SWEET_ONLY"
    if fams == {"SEQ2SEQ_GED_MORPH"}:
        return "SEQ2SEQ_GED_MORPH_ONLY"
    if fams == set(FAMILIES):
        return "BOTH_FAMILIES"
    raise RuntimeError(f"UNEXPECTED_FAMILY_SET:{sorted(fams)}")


def family_diagnostics(action_sets):
    per_uid = []
    cross_uids = set()
    cross_clusters = set()
    total_shared_actions = 0
    family_action_count = Counter()
    family_uid = {f: set() for f in FAMILIES}
    family_clusters = {f: set() for f in FAMILIES}

    for aset in action_sets:
        fams = family_set_for_action_set(aset)
        state = family_availability_state(fams)
        per_uid.append({
            "uid": aset["uid"],
            "cluster_id": aset["cluster_id"],
            "family_count": len(fams),
            "availability_state": state,
        })
        for action in aset["actions"]:
            if action["keep_semantics"]:
                continue
            af = {
                p["family_id"] for p in action["provenance"]
                if p.get("family_id") in FAMILIES
            }
            for fam in af:
                family_action_count[fam] += 1
                family_uid[fam].add(aset["uid"])
                family_clusters[fam].add(aset["cluster_id"])
            if af == set(FAMILIES):
                total_shared_actions += 1
                cross_uids.add(aset["uid"])
                cross_clusters.add(aset["cluster_id"])

    count_hist = histogram_uid_cluster(
        per_uid,
        lambda r: str(r["family_count"]),
        ("0", "1", "2"),
    )
    state_hist = histogram_uid_cluster(
        per_uid,
        lambda r: r["availability_state"],
        ("NONE", "SWEET_ONLY", "SEQ2SEQ_GED_MORPH_ONLY", "BOTH_FAMILIES"),
    )

    leave_out = {}
    all_unique = sum(len(a["actions"]) for a in action_sets)
    all_nonkeep_uid = sum(bool(nonkeep_actions(a["actions"])) for a in action_sets)
    all_nonkeep_clusters = {
        a["cluster_id"] for a in action_sets if nonkeep_actions(a["actions"])
    }

    for fam in FAMILIES:
        without_total = 0
        becoming_keep_uid = 0
        becoming_keep_clusters = set()
        retained_other_uid = 0
        retained_other_clusters = set()
        for aset in action_sets:
            full_nonkeep = nonkeep_actions(aset["actions"])
            kept = remove_family(aset, fam)
            kept_nonkeep = nonkeep_actions(kept)
            without_total += len(kept)
            if full_nonkeep and not kept_nonkeep:
                becoming_keep_uid += 1
                becoming_keep_clusters.add(aset["cluster_id"])
            if kept_nonkeep:
                retained_other_uid += 1
                retained_other_clusters.add(aset["cluster_id"])
        leave_out[fam] = {
            "all_total_unique_legal_actions_sum": all_unique,
            "without_family_total_unique_legal_actions_sum": without_total,
            "delta_unique_legal_actions_sum": all_unique - without_total,
            "all_uids_with_nonkeep": all_nonkeep_uid,
            "all_clusters_with_nonkeep": len(all_nonkeep_clusters),
            "uids_becoming_keep_only": becoming_keep_uid,
            "clusters_becoming_keep_only": len(becoming_keep_clusters),
            "uids_retaining_nonkeep_from_other_family": retained_other_uid,
            "clusters_retaining_nonkeep_from_other_family": len(retained_other_clusters),
        }

    return {
        "SOURCE_ONLY_INDEPENDENT_NONKEEP_FAMILY_COUNT": count_hist,
        "SOURCE_ONLY_FAMILY_AVAILABILITY_STATE": state_hist,
        "SOURCE_ONLY_CROSS_FAMILY_EXACT_OUTPUT_AGREEMENT": {
            "uid_count": len(cross_uids),
            "cluster_count": len(cross_clusters),
            "total_shared_actions": total_shared_actions,
            "interpretation": "exact whole-output agreement only; not correctness",
        },
        "SOURCE_ONLY_LEAVE_ONE_FAMILY_OUT": leave_out,
        "SOURCE_ONLY_FAMILY_DOMINANCE_DIAGNOSTICS": {
            fam: {
                "legal_nonkeep_action_occurrences": family_action_count[fam],
                "uids_with_at_least_one_nonkeep_action": len(family_uid[fam]),
                "clusters_with_at_least_one_nonkeep_action": len(family_clusters[fam]),
            }
            for fam in FAMILIES
        },
        "family_availability_uid_rows": per_uid,
    }


def burden_with_eligibility(items):
    char_ratio = []
    char_delta = []
    token_delta = []
    component_count = []
    output_eligible = 0
    component_eligible = 0

    for item in items:
        n = item["normalized"]
        out = n.get("output")
        src = n.get("source")
        if not isinstance(out, str) or not isinstance(src, str):
            continue
        output_eligible += 1
        if len(src) > 0:
            char_ratio.append(len(out) / len(src))
        char_delta.append(abs(len(out) - len(src)))
        token_delta.append(abs(len(out.split()) - len(src.split())))
        if item["legalization"].get("alignment_state") == "UNIQUE":
            component_eligible += 1
            component_count.append(len(item["legalization"]["components"]))

    return {
        "eligibility": {
            "output_string_rows": output_eligible,
            "char_ratio_rows_nonzero_source": len(char_ratio),
            "component_rows_unique_alignment": component_eligible,
        },
        "output_input_char_ratio": stat(char_ratio),
        "absolute_character_delta": stat(char_delta),
        "absolute_whitespace_token_delta": stat(token_delta),
        "component_count_unique_alignment_only": stat(component_count),
        "missing_output_is_na_not_zero": True,
    }


def direct_burden(source_texts, output_texts):
    ratios, chars, toks, comps = [], [], [], []
    eligible = 0
    for src, out in zip(source_texts, output_texts):
        if not isinstance(src, str) or not isinstance(out, str):
            continue
        eligible += 1
        if src:
            ratios.append(len(out) / len(src))
        chars.append(abs(len(out) - len(src)))
        toks.append(abs(len(out.split()) - len(src.split())))
        sm = SequenceMatcher(a=src, b=out, autojunk=False)
        comps.append(sum(tag != "equal" for tag, *_ in sm.get_opcodes()))
    return {
        "eligible_rows": eligible,
        "output_input_char_ratio": stat(ratios),
        "absolute_character_delta": stat(chars),
        "absolute_whitespace_token_delta": stat(toks),
        "sequence_matcher_component_count": stat(comps),
    }


def reason_matrix(items):
    raw = Counter()
    legal = Counter()
    for item in items:
        for r in item["normalized"].get("raw_failure_reasons", []):
            raw[r.split(":", 1)[0]] += 1
        for r in item["legalization"].get("legal_reasons", []):
            legal[r.split(":", 1)[0]] += 1
    return {"raw_failure_reason_presence": dict(raw), "legal_reason_presence": dict(legal)}


def runtime_summary(items, metric_type):
    vals = [
        float(x["normalized"]["runtime_seconds"])
        for x in items
        if isinstance(x["normalized"].get("runtime_seconds"), (int, float))
    ]
    return {
        "measurement_type": metric_type,
        "eligible_rows": len(vals),
        "ineligible_rows": EXPECTED_CASES - len(vals),
        "statistics": stat(vals) if vals else None,
    }


def proposer_summary_for(key, rows_by_uid):
    items = [rows_by_uid[uid][key] for uid in rows_by_uid]
    raw_valid = sum(not base.identity_check(x["normalized"], {
        "uid": x["normalized"]["uid"],
        "case_id": x["normalized"]["case_id"],
        "cluster_id": x["normalized"]["cluster_id"],
        "source": x["normalized"]["source"],
        "source_sha256": x["normalized"]["source_sha256"],
    }) for x in items)
    executable = sum(x["normalized"]["raw_execution_state"] == "OK" for x in items)
    legal = sum(x["legalization"]["legal"] for x in items)
    protection_blocked = sum(
        x["legalization"]["protection"] is not None
        and x["legalization"]["protection"]["status"] != "PASS"
        for x in items
    )
    changed = sum(
        isinstance(x["normalized"].get("output"), str)
        and x["normalized"]["output"] != x["normalized"]["source"]
        for x in items
    )
    rows = [
        {
            "cluster_id": x["normalized"]["cluster_id"],
            "raw_valid": not x["legalization"]["identity_reasons"],
            "executable": x["normalized"]["raw_execution_state"] == "OK",
            "failed": x["normalized"]["raw_execution_state"] != "OK",
            "legal": x["legalization"]["legal"],
            "protection_blocked": (
                x["legalization"]["protection"] is not None
                and x["legalization"]["protection"]["status"] != "PASS"
            ),
            "changed": (
                isinstance(x["normalized"].get("output"), str)
                and x["normalized"]["output"] != x["normalized"]["source"]
            ),
        }
        for x in items
    ]
    runtime_type = (
        "UNAVAILABLE"
        if key == "P1"
        else ("MEASURED_PER_UID_LATENCY" if key == "P2" else "ALLOCATED_BATCH_TIME")
    )
    return {
        "D_all": EXPECTED_CASES,
        "D_raw_valid": raw_valid,
        "D_exec": executable,
        "failed": EXPECTED_CASES - executable,
        "D_legal": legal,
        "nonlegal": EXPECTED_CASES - legal,
        "protection_blocked": protection_blocked,
        "changed_vs_source": changed,
        "cluster_presence_counts": {
            state: distinct_cluster_count(rows, lambda r, s=state: r[s])
            for state in (
                "raw_valid", "executable", "failed", "legal",
                "protection_blocked", "changed"
            )
        },
        "alignment_states": dict(Counter(
            x["legalization"]["alignment_state"] for x in items
        )),
        "failure_reason_matrix": reason_matrix(items),
        "burden": burden_with_eligibility(items),
        "runtime": runtime_summary(items, runtime_type) if key != "P1" else {
            "measurement_type": "UNAVAILABLE",
            "eligible_rows": 0,
            "ineligible_rows": EXPECTED_CASES,
            "statistics": None,
        },
    }


def proposer_level_diagnostics(action_sets):
    marginal = {
        k: {
            "uid_count": 0,
            "cluster_count": 0,
            "total_unique_legal_outputs": 0,
            "keep_only_reduction_uid_count": 0,
            "keep_only_reduction_cluster_count": 0,
        }
        for k in ("P1", "P2", "P3")
    }
    marginal_clusters = {k: set() for k in marginal}
    keep_clusters = {k: set() for k in marginal}
    all_total = 0
    all_nonkeep_uid = 0
    all_nonkeep_clusters = set()
    sizes = []

    for aset in action_sets:
        full = {a["output"] for a in aset["actions"]}
        all_total += len(full)
        sizes.append({
            "uid": aset["uid"],
            "cluster_id": aset["cluster_id"],
            "size": len(full),
        })
        if len(full) > 1:
            all_nonkeep_uid += 1
            all_nonkeep_clusters.add(aset["cluster_id"])
        for key in ("P1", "P2", "P3"):
            without = base.action_set_without(aset, key)
            delta = len(full) - len(without)
            if delta > 0:
                marginal[key]["uid_count"] += 1
                marginal[key]["total_unique_legal_outputs"] += delta
                marginal_clusters[key].add(aset["cluster_id"])
            if len(without) == 1 and len(full) > 1:
                marginal[key]["keep_only_reduction_uid_count"] += 1
                keep_clusters[key].add(aset["cluster_id"])

    leave = {}
    for key in ("P1", "P2", "P3"):
        without_total = 0
        nonkeep_uid = 0
        nonkeep_clusters = set()
        for aset in action_sets:
            outs = base.action_set_without(aset, key)
            without_total += len(outs)
            if len(outs) > 1:
                nonkeep_uid += 1
                nonkeep_clusters.add(aset["cluster_id"])
        leave[key] = {
            "all_total_unique_actions_sum": all_total,
            "without_total_unique_actions_sum": without_total,
            "delta_unique_actions_sum": all_total - without_total,
            "all_uid_with_nonkeep": all_nonkeep_uid,
            "without_uid_with_nonkeep": nonkeep_uid,
            "delta_uid_with_nonkeep": all_nonkeep_uid - nonkeep_uid,
            "all_clusters_with_nonkeep": len(all_nonkeep_clusters),
            "without_clusters_with_nonkeep": len(nonkeep_clusters),
            "delta_clusters_with_nonkeep": len(all_nonkeep_clusters) - len(nonkeep_clusters),
        }
        marginal[key]["cluster_count"] = len(marginal_clusters[key])
        marginal[key]["keep_only_reduction_cluster_count"] = len(keep_clusters[key])

    size_hist = histogram_uid_cluster(
        sizes, lambda r: str(r["size"]), ("1", "2", "3", "4")
    )
    vals = [r["size"] for r in sizes]
    size_hist.update({
        "mean": statistics.mean(vals),
        "median": statistics.median(vals),
        "p95_nearest_rank": nearest_rank(vals),
        "max": max(vals),
    })
    return marginal, leave, size_hist


def p2_full_diagnostics(p2_rows):
    stage_counts = defaultdict(Counter)
    segment_counts = []
    total_wordpieces = 0
    exact_identity_rows = 0
    hook_positive = 0
    reason_presence = Counter()

    for row in p2_rows:
        for stage, status in row.get("stage_status", {}).items():
            stage_counts[stage][status] += 1
        if isinstance(row.get("ged_segment_count"), int):
            segment_counts.append(row["ged_segment_count"])
        segments = row.get("ged_segments")
        if isinstance(segments, list):
            for seg in segments:
                for wr in seg.get("word_records", []):
                    s = wr.get("ged_wordpiece_start")
                    e = wr.get("ged_wordpiece_end")
                    if isinstance(s, int) and isinstance(e, int) and e >= s:
                        total_wordpieces += e - s
        trace = row.get("ged_word_identity_trace")
        mwc = row.get("morph_word_count")
        if isinstance(trace, list) and isinstance(mwc, int) and len(trace) == mwc:
            exact_identity_rows += 1
        if isinstance(row.get("ged_embedding_hook_call_count"), int) and row["ged_embedding_hook_call_count"] > 0:
            hook_positive += 1
        for reason in row.get("failure_reasons", []):
            reason_presence[reason.split(":", 1)[-1].split(":", 1)[0]] += 1

    def reason_contains(token):
        return sum(
            1 for row in p2_rows
            if any(token in r for r in row.get("failure_reasons", []))
        )

    return {
        "D_all": EXPECTED_CASES,
        "stage_status_counts": {k: dict(v) for k, v in stage_counts.items()},
        "ged_segment_count": stat(segment_counts),
        "total_ged_wordpieces_from_word_spans": total_wordpieces,
        "rows_with_exact_ged_word_identity_trace_count": exact_identity_rows,
        "rows_with_positive_ged_embedding_hook_count": hook_positive,
        "zero_token_word_failures": reason_contains("ZERO_TOKEN_WORD"),
        "single_word_over_budget_failures": reason_contains("SINGLE_WORD_OVER_BUDGET"),
        "unknown_or_unmapped_label_failures": (
            reason_contains("UNKNOWN_GED_LABEL") + reason_contains("UNMAPPED")
        ),
        "gec_input_too_long_failures": reason_contains("INPUT_TOO_LONG"),
        "generation_eos_or_ceiling_failures": (
            reason_contains("EOS") + reason_contains("GENERATION_CEILING")
        ),
        "failure_reason_presence": dict(reason_presence),
    }


def self_test():
    source = "نص"
    aset = {
        "uid": "S1",
        "cluster_id": "C1",
        "actions": [
            {
                "output": source,
                "keep_semantics": True,
                "provenance": [{"proposer_id": "KEEP", "family_id": "KEEP"}],
            },
            {
                "output": "نص أ",
                "keep_semantics": False,
                "provenance": [
                    {"proposer_id": "P1", "family_id": "SWEET_QALB14"},
                    {"proposer_id": "P2", "family_id": "SEQ2SEQ_GED_MORPH"},
                ],
            },
            {
                "output": "نص ب",
                "keep_semantics": False,
                "provenance": [
                    {"proposer_id": "P3", "family_id": "SWEET_QALB14"},
                ],
            },
        ],
    }
    no_sweet = remove_family(aset, "SWEET_QALB14")
    assert {a["output"] for a in no_sweet} == {source, "نص أ"}
    shared = [a for a in no_sweet if a["output"] == "نص أ"][0]
    assert shared["provenance"] == [
        {"proposer_id": "P2", "family_id": "SEQ2SEQ_GED_MORPH"}
    ]
    no_seq = remove_family(aset, "SEQ2SEQ_GED_MORPH")
    assert {a["output"] for a in no_seq} == {source, "نص أ", "نص ب"}
    assert family_set_for_action_set(aset) == set(FAMILIES)

    keep_equiv = {
        "uid": "S2",
        "cluster_id": "C2",
        "actions": [
            {
                "output": source,
                "keep_semantics": True,
                "provenance": [
                    {"proposer_id": "KEEP", "family_id": "KEEP"},
                    {"proposer_id": "P1", "family_id": "SWEET_QALB14"},
                ],
            }
        ],
    }
    assert family_set_for_action_set(keep_equiv) == set()
    print(json.dumps({
        "record_id": VERSION + "_SELF_TEST",
        "status": "PASS",
        "tests": 5,
        "project_source_loaded": False,
        "project_gold_loaded": False,
    }, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--source-manifest")
    ap.add_argument("--p1")
    ap.add_argument("--p2")
    ap.add_argument("--p3")
    ap.add_argument("--out-prefix", default="MPSEF_V4_STAGE2")
    ap.add_argument("--progress-state", default="MPSEF_V4_STAGE2_ANALYSIS_PROGRESS.json")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return
    for name in ("source_manifest", "p1", "p2", "p3"):
        if not getattr(args, name):
            raise SystemExit(f"--{name.replace('_','-')} required")

    paths = {
        "source": Path(args.source_manifest),
        "P1": Path(args.p1),
        "P2": Path(args.p2),
        "P3": Path(args.p3),
    }
    expected = {
        "source": EXPECTED_SOURCE_SHA,
        "P1": EXPECTED_P1_SHA,
        "P2": EXPECTED_P2_SHA,
        "P3": EXPECTED_P3_SHA,
    }
    for key, path in paths.items():
        got = sha_file(path)
        if got != expected[key]:
            raise RuntimeError(f"{key}_SHA_MISMATCH:{got}")

    source_rows = load_jsonl(paths["source"])
    p1 = load_jsonl(paths["P1"])
    p2 = load_jsonl(paths["P2"])
    p3 = load_jsonl(paths["P3"])

    if len(source_rows) != EXPECTED_CASES:
        raise RuntimeError(f"SOURCE_COUNT_MISMATCH:{len(source_rows)}")
    if len({r["uid"] for r in source_rows}) != EXPECTED_CASES:
        raise RuntimeError("SOURCE_DUPLICATE_UID")
    if len({r["cluster_id"] for r in source_rows}) != EXPECTED_CLUSTERS:
        raise RuntimeError("SOURCE_CLUSTER_COUNT_MISMATCH")
    if any(r.get("role") != "C_F" for r in source_rows):
        raise RuntimeError("NON_CF_SOURCE_ROW")

    source_by = {r["uid"]: r for r in source_rows}
    p1_by = {r["uid"]: r for r in p1}
    p2_by = {r["uid"]: r for r in p2}
    p3_by = {r["uid"]: r for r in p3}
    expected_uids = set(source_by)
    if set(p1_by) != expected_uids:
        raise RuntimeError("P1_UID_SET_MISMATCH")
    if set(p2_by) != expected_uids:
        raise RuntimeError("P2_UID_SET_MISMATCH")
    if set(p3_by) != expected_uids:
        raise RuntimeError("P3_UID_SET_MISMATCH")

    for uid in expected_uids:
        if p3_by[uid].get("stage_b_classifier_version") != STAGE_B_VERSION:
            raise RuntimeError(f"P3_STAGE_B_CLASSIFIER_VERSION_MISMATCH:{uid}")
        if p3_by[uid].get("parent_output_sha256") != p1_by[uid].get("output_sha256"):
            raise RuntimeError(f"P3_PARENT_SHA_NOT_P1:{uid}")
        if p3_by[uid].get("input_sha256") != p1_by[uid].get("output_sha256"):
            raise RuntimeError(f"P3_INPUT_SHA_NOT_P1:{uid}")
        if p3_by[uid].get("input_text") != p1_by[uid].get("full_proposer_output"):
            raise RuntimeError(f"P3_INPUT_TEXT_NOT_P1:{uid}")

    progress = Path(args.progress_state)
    update_state(
        progress, VERSION, "LEGALIZE_AND_BUILD", 0, EXPECTED_CASES,
        status="RUNNING",
        message="starting Stage2 full-C_F source-only analysis",
    )

    rows_by_uid = {}
    proposer_rows = []
    action_sets = []
    failures = []
    started = time.monotonic()

    for idx, srcrow in enumerate(source_rows, start=1):
        uid = srcrow["uid"]
        normalized = {
            "P1": base.normalize_p1(p1_by[uid], srcrow),
            "P2": base.normalize_p2(p2_by[uid], srcrow),
            "P3": base.normalize_p3(p3_by[uid], srcrow),
        }
        recs = {}
        for key in ("P1", "P2", "P3"):
            leg = base.legalize(normalized[key], srcrow)
            recs[key] = {"normalized": normalized[key], "legalization": leg}
            meta = base.PROPOSERS[key]
            proposer_rows.append({
                "record_id": "MPSEF_V4_STAGE2_PROPOSER_ROW_V1",
                "registry_namespace": REGISTRY_NAMESPACE,
                "registry_sha256": EXPECTED_REGISTRY_SHA,
                "uid": uid,
                "case_id": srcrow["case_id"],
                "cluster_id": srcrow["cluster_id"],
                "source_sha256": srcrow["source_sha256"],
                "proposer_key": key,
                "proposer_id": meta["proposer_id"],
                "proposer_version": meta["proposer_version"],
                "family_id": meta["family_id"],
                "ancestry_id": meta["ancestry_id"],
                "raw_execution_state": normalized[key]["raw_execution_state"],
                "raw_failure_reasons": normalized[key]["raw_failure_reasons"],
                "output_sha256": normalized[key]["output_sha256"],
                "changed_vs_source": (
                    isinstance(normalized[key]["output"], str)
                    and normalized[key]["output"] != srcrow["source"]
                ),
                "legal": leg["legal"],
                "legal_reasons": leg["legal_reasons"],
                "alignment_state": leg["alignment_state"],
                "component_count": len(leg["components"]),
                "protection_status": (
                    leg["protection"]["status"] if leg["protection"] else None
                ),
                "protection_reasons": (
                    leg["protection"].get("reasons", []) if leg["protection"] else []
                ),
                "shadow_status": (
                    leg["shadow"].get("shadow_status") if leg["shadow"] else None
                ),
                "shadow_causes": (
                    leg["shadow"].get("causes", []) if leg["shadow"] else []
                ),
                "source_only": True,
                "gold_reference_consulted": False,
                "quality_scored": False,
            })
            if not leg["legal"]:
                failures.append({
                    "uid": uid,
                    "case_id": srcrow["case_id"],
                    "cluster_id": srcrow["cluster_id"],
                    "proposer_key": key,
                    "proposer_id": meta["proposer_id"],
                    "raw_execution_state": normalized[key]["raw_execution_state"],
                    "legal_reasons": leg["legal_reasons"],
                })

        rows_by_uid[uid] = recs
        action_sets.append(base.build_action_set(srcrow, recs))
        update_state(
            progress, VERSION, "LEGALIZE_AND_BUILD", idx, EXPECTED_CASES,
            status="RUNNING", message=f"uid={uid}",
        )

    proposer_summary = {
        key: proposer_summary_for(key, rows_by_uid)
        for key in ("P1", "P2", "P3")
    }
    marginal, leave_proposer, action_size = proposer_level_diagnostics(action_sets)
    family = family_diagnostics(action_sets)

    pairwise = {
        "P1_P2": base.pairwise_summary(rows_by_uid, "P1", "P2"),
        "P1_P3": base.pairwise_summary(rows_by_uid, "P1", "P3"),
        "P2_P3": base.pairwise_summary(rows_by_uid, "P2", "P3"),
    }

    stage_b_counts = Counter(
        p3_by[uid].get("stage_b_domain_from_p1", "UNAVAILABLE_COMPARISON")
        for uid in expected_uids
    )
    unknown_stage_b = set(stage_b_counts) - set(STAGE_B_CATEGORIES)
    if unknown_stage_b:
        raise RuntimeError(f"UNKNOWN_STAGE_B_CATEGORIES:{sorted(unknown_stage_b)}")

    p3_parent_burden = direct_burden(
        [p1_by[uid].get("full_proposer_output") for uid in expected_uids],
        [p3_by[uid].get("full_proposer_output") for uid in expected_uids],
    )

    family_uid_path = Path(args.out_prefix + "_FAMILY_UID_ROWS_V1.jsonl")
    family_uid_path.write_text(
        "\n".join(
            json.dumps(x, ensure_ascii=False, sort_keys=True)
            for x in family.pop("family_availability_uid_rows")
        ) + "\n",
        encoding="utf-8",
    )

    proposer_path = Path(args.out_prefix + "_PROPOSER_ROWS_V1.jsonl")
    proposer_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in proposer_rows) + "\n",
        encoding="utf-8",
    )
    action_path = Path(args.out_prefix + "_LEGAL_ACTION_SETS_V1.jsonl")
    action_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in action_sets) + "\n",
        encoding="utf-8",
    )
    failure_path = Path(args.out_prefix + "_FAILURES_V1.jsonl")
    failure_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in failures)
        + ("\n" if failures else ""),
        encoding="utf-8",
    )

    analysis_seconds = time.monotonic() - started

    diversity = {
        "record_id": VERSION,
        "status": "PASS",
        "cases": EXPECTED_CASES,
        "clusters": EXPECTED_CLUSTERS,
        "source_manifest_sha256": EXPECTED_SOURCE_SHA,
        "registry_namespace": REGISTRY_NAMESPACE,
        "registry_sha256": EXPECTED_REGISTRY_SHA,
        "proposal_input_sha256": {
            "P1": EXPECTED_P1_SHA,
            "P2": EXPECTED_P2_SHA,
            "P3": EXPECTED_P3_SHA,
        },
        "proposer_summary": proposer_summary,
        "SOURCE_ONLY_LEGAL_MARGINAL_CONTRIBUTION": marginal,
        "SOURCE_ONLY_KEEP_ONLY_REDUCTION": {
            k: {
                "uid_count": marginal[k]["keep_only_reduction_uid_count"],
                "cluster_count": marginal[k]["keep_only_reduction_cluster_count"],
            }
            for k in ("P1", "P2", "P3")
        },
        "SOURCE_ONLY_LEAVE_ONE_PROPOSER_OUT": leave_proposer,
        "action_set_size": action_size,
        "pairwise_output_diagnostics": pairwise,
        "p3_stage_b": {
            "classifier_version": STAGE_B_VERSION,
            "counts_D_all": {c: stage_b_counts[c] for c in STAGE_B_CATEGORIES},
            "P1_to_P3_change_burden": p3_parent_burden,
            "source_to_P3_change_burden": proposer_summary["P3"]["burden"],
        },
        "p2_full_population_diagnostics": p2_full_diagnostics(p2),
        "analysis_runtime_seconds": analysis_seconds,
        "project_source_loaded": True,
        "project_source_scope": "FROZEN_STAGE2_FULL_CF_1918_ONLY",
        "gold_reference_consulted": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "family_consensus_activated": False,
        "quality_claimed": False,
        "reserved_data_opened": False,
    }

    family_summary = {
        "record_id": "MPSEF_V4_STAGE2_FAMILY_SUMMARY_V1",
        "status": "PASS",
        "cases": EXPECTED_CASES,
        "clusters": EXPECTED_CLUSTERS,
        "families": list(FAMILIES),
        **family,
        "gold_reference_consulted": False,
        "quality_claimed": False,
    }

    runtime = {
        "record_id": "MPSEF_V4_STAGE2_RUNTIME_V1",
        "analysis_runtime_seconds": analysis_seconds,
        "P1": proposer_summary["P1"]["runtime"],
        "P2": proposer_summary["P2"]["runtime"],
        "P3": proposer_summary["P3"]["runtime"],
        "rule": "runtime types are not pooled",
        "hardware_comparison_warning": (
            "P2/P3 timings originate from separate workflows; engineering cost only"
        ),
    }

    diversity_path = Path(args.out_prefix + "_DIVERSITY_SUMMARY_V1.json")
    family_path = Path(args.out_prefix + "_FAMILY_SUMMARY_V1.json")
    runtime_path = Path(args.out_prefix + "_RUNTIME_V1.json")
    diversity_path.write_text(json.dumps(diversity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    family_path.write_text(json.dumps(family_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    runtime_path.write_text(json.dumps(runtime, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    update_state(
        progress, VERSION, "COMPLETE", EXPECTED_CASES, EXPECTED_CASES,
        status="COMPLETE",
        message="Stage2 full-C_F source-only legalizer/diversity/family analysis complete",
    )

    print(json.dumps({
        "record_id": VERSION,
        "status": "PASS",
        "cases": EXPECTED_CASES,
        "clusters": EXPECTED_CLUSTERS,
        "legal": {k: proposer_summary[k]["D_legal"] for k in ("P1","P2","P3")},
        "action_set_size": action_size,
        "family_availability": family_summary["SOURCE_ONLY_FAMILY_AVAILABILITY_STATE"],
        "stage_b_counts": diversity["p3_stage_b"]["counts_D_all"],
        "analysis_runtime_seconds": analysis_seconds,
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
