#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import statistics
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

VERSION = "MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2"
EXPECTED_CASES = 1918
EXPECTED_CLUSTERS = 764
EXPECTED_MANIFEST_SHA = "051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_P1_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P2_SHA = "87dd3600293b215172f5a75dc7485915013963aa3e661310ea1adac08b9ddba7"
EXPECTED_P3_SHA = "02f9bd2555b1b9f350665179dcd96dd6accf532355a269b38ef4d099ea25d4ec"
EXPECTED_ANALYSIS_ARTIFACT_DIGEST = "d773c8b65f607e06ce811d44d7e18deaf49c0da0c17428122d2258b043f82c4b"
EXPECTED_ANALYSIS_SUMMARY_SHA = "00e8d48a42edf129d4fdcf46a02624cec1f893e9c27f23880d156957d0e9bcac"
EXPECTED_PROPOSER_ROWS_SHA = "6ff90a0b9ee0201d72caba144474b50e34ccb22796bd2f161e4b104c0aaea42d"
EXPECTED_ACTION_SETS_SHA = "e38393abb36734d3882e29a78f3b33c80718791957b9b8c0c6e8a8ab77f6e138"
EXPECTED_FAILURES_SHA = "48cfd2c2574fa56411f1899c15ba1d5a84671eb43e3b875652192384c3081fa9"
EXPECTED_RUNTIME_SHA = "a2811fff2b8952f9c1714eb913a532592e4d7ccc688305f67ed288019f85f236"
FAMILIES = ("SWEET_QALB14", "SEQ2SEQ_GED_MORPH")
STAGE_B_CATEGORIES = (
    "NO_CHANGE_FROM_P1",
    "PUNCTUATION_ONLY_FROM_P1",
    "BOUNDARY_ONLY_FROM_P1",
    "LEXICAL_ONLY_FROM_P1",
    "MIXED_FROM_P1",
    "UNAVAILABLE_COMPARISON",
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def nearest_rank(values, q=0.95):
    if not values:
        return None
    vals = sorted(values)
    return vals[max(1, math.ceil(q * len(vals))) - 1]


def stats(values):
    if not values:
        return {
            "n": 0,
            "mean": None,
            "median": None,
            "p95_nearest_rank": None,
            "max": None,
        }
    return {
        "n": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "p95_nearest_rank": nearest_rank(values),
        "max": max(values),
    }


def components(source: str, output: str):
    sm = SequenceMatcher(a=source, b=output, autojunk=False)
    return [
        {
            "op": tag.upper(),
            "source_start": i1,
            "source_end": i2,
            "output_start": j1,
            "output_end": j2,
            "source_text": source[i1:i2],
            "output_text": output[j1:j2],
        }
        for tag, i1, i2, j1, j2 in sm.get_opcodes()
        if tag != "equal"
    ]


def burden(pairs):
    ratios, char_delta, token_delta, comp_count = [], [], [], []
    for src, out in pairs:
        if not isinstance(src, str) or not isinstance(out, str):
            continue
        if len(src):
            ratios.append(len(out) / len(src))
        char_delta.append(abs(len(out) - len(src)))
        token_delta.append(abs(len(out.split()) - len(src.split())))
        comp_count.append(len(components(src, out)))
    return {
        "eligible_rows": len(char_delta),
        "output_input_char_ratio": stats(ratios),
        "absolute_character_delta": stats(char_delta),
        "absolute_whitespace_token_delta": stats(token_delta),
        "component_count": stats(comp_count),
    }


def cluster_presence(rows, predicate):
    return len({r["cluster_id"] for r in rows if predicate(r)})


def family_action_info(action_set):
    source_sha = action_set["source_sha256"]
    nonkeep = [
        a
        for a in action_set["actions"]
        if not a.get("keep_semantics", False)
        and a.get("output_sha256") != source_sha
    ]
    fams = set()
    shared = []
    action_counts = Counter()
    for a in nonkeep:
        af = {
            p.get("family_id")
            for p in a.get("provenance", [])
            if p.get("family_id") in FAMILIES
        }
        fams |= af
        for f in af:
            action_counts[f] += 1
        if set(FAMILIES).issubset(af):
            shared.append(a)
    if not fams:
        state = "NONE"
    elif fams == {"SWEET_QALB14"}:
        state = "SWEET_ONLY"
    elif fams == {"SEQ2SEQ_GED_MORPH"}:
        state = "SEQ2SEQ_GED_MORPH_ONLY"
    else:
        state = "BOTH_FAMILIES"
    return fams, state, shared, action_counts


def stage_status_counts(p2_rows, stage):
    c = Counter(
        (r.get("stage_status") or {}).get(stage, "UNKNOWN")
        for r in p2_rows
    )
    return {
        k: c.get(k, 0)
        for k in ("PASS", "FAIL", "NOT_REACHED", "UNKNOWN")
    }


def p2_diagnostics(p2_rows):
    failure_reasons = Counter()
    for r in p2_rows:
        for reason in r.get("failure_reasons", []) or []:
            failure_reasons[reason.split(":", 1)[0]] += 1

    ged_segments = [
        r.get("ged_segment_count")
        for r in p2_rows
        if isinstance(r.get("ged_segment_count"), int)
    ]
    ged_wordpieces = []
    for r in p2_rows:
        total = 0
        valid = False
        for seg in r.get("ged_segments") or []:
            if isinstance(seg.get("content_wordpieces"), int):
                total += seg["content_wordpieces"]
                valid = True
        if valid:
            ged_wordpieces.append(total)

    exact_word_identity = sum(
        r.get("stage_status", {}).get("GED_WORD_IDENTITY") == "PASS"
        for r in p2_rows
    )
    zero_token = sum(
        any("ZERO_TOKEN" in x for x in (r.get("failure_reasons") or []))
        for r in p2_rows
    )
    over_budget = sum(
        any("OVER_BUDGET" in x for x in (r.get("failure_reasons") or []))
        for r in p2_rows
    )
    unknown_label = sum(
        any(
            "LABEL" in x and ("UNKNOWN" in x or "UNMAPPED" in x)
            for x in (r.get("failure_reasons") or [])
        )
        for r in p2_rows
    )
    input_too_long = sum(
        any(
            "INPUT_TOO_LONG" in x
            for x in (r.get("failure_reasons") or [])
        )
        for r in p2_rows
    )
    generation_incomplete = sum(
        r.get("execution_state") != "OK"
        for r in p2_rows
    )
    generation_ceiling = sum(
        bool(r.get("generation_hit_ceiling"))
        for r in p2_rows
    )
    terminal_eos_known = sum(
        r.get("terminal_eos_index") is not None
        for r in p2_rows
    )
    interface_ok = sum(
        (r.get("ged_embedding_hook_call_count") or 0) > 0
        for r in p2_rows
    )

    return {
        "D_all": len(p2_rows),
        "canonical_stage_status_counts": {
            stage: stage_status_counts(p2_rows, stage)
            for stage in (
                "SOURCE_IDENTITY",
                "MORPH_ANALYSIS",
                "GED_TOKENIZATION",
                "GED_WORD_IDENTITY",
                "GED_INFERENCE",
                "GEC_PROJECTION",
                "GEC_TOKENIZATION",
                "GENERATION",
                "OUTPUT_DECODE",
            )
        },
        "morphology_success": sum(
            r.get("stage_status", {}).get("MORPH_ANALYSIS") == "PASS"
            for r in p2_rows
        ),
        "morphology_failure": sum(
            r.get("stage_status", {}).get("MORPH_ANALYSIS") == "FAIL"
            for r in p2_rows
        ),
        "ged_tokenization_success": sum(
            r.get("stage_status", {}).get("GED_TOKENIZATION") == "PASS"
            for r in p2_rows
        ),
        "ged_tokenization_failure": sum(
            r.get("stage_status", {}).get("GED_TOKENIZATION") == "FAIL"
            for r in p2_rows
        ),
        "zero_token_word_failures": zero_token,
        "single_word_over_budget_failures": over_budget,
        "ged_segment_count": stats(ged_segments),
        "total_ged_wordpieces": stats(ged_wordpieces),
        "exact_word_identity_coverage": {
            "numerator": exact_word_identity,
            "denominator": len(p2_rows),
            "rate": exact_word_identity / len(p2_rows),
        },
        "unknown_or_unmapped_label_failures": unknown_label,
        "gec_tokenization_failures": sum(
            r.get("stage_status", {}).get("GEC_TOKENIZATION") == "FAIL"
            for r in p2_rows
        ),
        "gec_input_too_long_failures": input_too_long,
        "generation_incomplete_or_unproven": generation_incomplete,
        "generation_ceiling_rows": generation_ceiling,
        "terminal_eos_evidence_available": terminal_eos_known,
        "model_interface_proof_rows": interface_ok,
        "failure_reason_uid_presence": dict(failure_reasons),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis-dir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--p1", required=True)
    ap.add_argument("--p2", required=True)
    ap.add_argument("--p3", required=True)
    ap.add_argument("--out-dir", default=".")
    args = ap.parse_args()

    ad = Path(args.analysis_dir)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest_path, p1_path, p2_path, p3_path = map(
        Path,
        (args.manifest, args.p1, args.p2, args.p3),
    )

    expected_files = {
        manifest_path: EXPECTED_MANIFEST_SHA,
        p1_path: EXPECTED_P1_SHA,
        p2_path: EXPECTED_P2_SHA,
        p3_path: EXPECTED_P3_SHA,
        ad / "MPSEF_V4_STAGE2_FULL_CF_DIVERSITY_SUMMARY_V1.json":
            EXPECTED_ANALYSIS_SUMMARY_SHA,
        ad / "MPSEF_V4_STAGE2_FULL_CF_PROPOSER_ROWS_V2.jsonl":
            EXPECTED_PROPOSER_ROWS_SHA,
        ad / "MPSEF_V4_STAGE2_FULL_CF_SOURCE_ONLY_ACTION_SETS_V2.jsonl":
            EXPECTED_ACTION_SETS_SHA,
        ad / "MPSEF_V4_STAGE2_FULL_CF_FAILURES_V1.jsonl":
            EXPECTED_FAILURES_SHA,
        ad / "MPSEF_V4_STAGE2_FULL_CF_RUNTIME_V1.json":
            EXPECTED_RUNTIME_SHA,
    }
    for path, expected in expected_files.items():
        got = sha_file(path)
        if got != expected:
            raise RuntimeError(
                f"FROZEN_INPUT_SHA_MISMATCH:{path.name}:{got}"
            )

    manifest = load_jsonl(manifest_path)
    p1 = load_jsonl(p1_path)
    p2 = load_jsonl(p2_path)
    p3 = load_jsonl(p3_path)
    proposer_rows = load_jsonl(
        ad / "MPSEF_V4_STAGE2_FULL_CF_PROPOSER_ROWS_V2.jsonl"
    )
    action_sets = load_jsonl(
        ad / "MPSEF_V4_STAGE2_FULL_CF_SOURCE_ONLY_ACTION_SETS_V2.jsonl"
    )
    base_summary = json.loads(
        (
            ad / "MPSEF_V4_STAGE2_FULL_CF_DIVERSITY_SUMMARY_V1.json"
        ).read_text(encoding="utf-8")
    )

    for name, rows in (
        ("manifest", manifest),
        ("p1", p1),
        ("p2", p2),
        ("p3", p3),
        ("action_sets", action_sets),
    ):
        if (
            len(rows) != EXPECTED_CASES
            or len({r["uid"] for r in rows}) != EXPECTED_CASES
        ):
            raise RuntimeError(f"{name.upper()}_COUNT_OR_UID_FAILURE")
    if len({r["cluster_id"] for r in manifest}) != EXPECTED_CLUSTERS:
        raise RuntimeError("CLUSTER_COUNT_MISMATCH")
    if len(proposer_rows) != EXPECTED_CASES * 3:
        raise RuntimeError("PROPOSER_ROW_COUNT_MISMATCH")

    by_prop = defaultdict(list)
    for r in proposer_rows:
        by_prop[r["proposer_key"]].append(r)

    identity_reasons = {
        "UID_MISMATCH",
        "CASE_ID_MISMATCH",
        "CLUSTER_ID_MISMATCH",
        "SOURCE_TEXT_MISMATCH",
        "SOURCE_SHA_FIELD_MISMATCH",
        "PACKET_SOURCE_SHA_INVALID",
        "OUTPUT_SHA_MISMATCH",
        "OK_WITHOUT_OUTPUT",
        "P3_PARENT_INPUT_SHA_MISMATCH",
    }

    proposer_protocol = {}
    for key in ("P1", "P2", "P3"):
        rows = by_prop[key]
        raw_valid = sum(
            not any(
                x in identity_reasons
                for x in r.get("legal_reasons", [])
            )
            for r in rows
        )
        changed = sum(bool(r.get("changed_vs_source")) for r in rows)
        raw_ok = sum(
            r.get("raw_execution_state") == "OK"
            for r in rows
        )
        legal = sum(bool(r.get("legal")) for r in rows)
        blocked = sum(
            r.get("protection_status") not in (None, "PASS")
            for r in rows
        )
        raw_reasons, legal_reasons = Counter(), Counter()
        for r in rows:
            for x in r.get("raw_failure_reasons") or []:
                raw_reasons[x.split(":", 1)[0]] += 1
            for x in r.get("legal_reasons") or []:
                legal_reasons[x.split(":", 1)[0]] += 1

        proposer_protocol[key] = {
            "D_all": EXPECTED_CASES,
            "D_raw_valid": raw_valid,
            "D_exec": raw_ok,
            "D_legal": legal,
            "failed": EXPECTED_CASES - raw_ok,
            "protection_blocked": blocked,
            "changed_vs_source": changed,
            "uid_state_counts": {
                "raw_valid": raw_valid,
                "executable": raw_ok,
                "failed": EXPECTED_CASES - raw_ok,
                "legal": legal,
                "nonlegal": EXPECTED_CASES - legal,
                "protection_blocked": blocked,
                "changed_vs_source": changed,
            },
            "cluster_presence_counts": {
                "raw_valid": cluster_presence(
                    rows,
                    lambda r: not any(
                        x in identity_reasons
                        for x in r.get("legal_reasons", [])
                    ),
                ),
                "executable": cluster_presence(
                    rows,
                    lambda r: r.get("raw_execution_state") == "OK",
                ),
                "failed": cluster_presence(
                    rows,
                    lambda r: r.get("raw_execution_state") != "OK",
                ),
                "legal": cluster_presence(
                    rows,
                    lambda r: bool(r.get("legal")),
                ),
                "nonlegal": cluster_presence(
                    rows,
                    lambda r: not bool(r.get("legal")),
                ),
                "protection_blocked": cluster_presence(
                    rows,
                    lambda r: (
                        r.get("protection_status") not in (None, "PASS")
                    ),
                ),
                "changed_vs_source": cluster_presence(
                    rows,
                    lambda r: bool(r.get("changed_vs_source")),
                ),
            },
            "raw_failure_reason_uid_presence": dict(raw_reasons),
            "legal_reason_uid_presence": dict(legal_reasons),
            "cluster_histogram_semantics":
                "distinct cluster_id with >=1 qualifying UID; "
                "state/reason bins may overlap",
        }

    family_count_uid = Counter()
    availability_uid = Counter()
    family_count_clusters = defaultdict(set)
    availability_clusters = defaultdict(set)
    shared_uids, shared_clusters, shared_actions = set(), set(), 0
    legal_nonkeep_actions_by_family = Counter()
    only_family_uid = Counter()
    only_family_clusters = defaultdict(set)

    for aset in action_sets:
        fams, state, shared, action_counts = family_action_info(aset)
        family_count_uid[len(fams)] += 1
        family_count_clusters[len(fams)].add(aset["cluster_id"])
        availability_uid[state] += 1
        availability_clusters[state].add(aset["cluster_id"])
        if shared:
            shared_uids.add(aset["uid"])
            shared_clusters.add(aset["cluster_id"])
            shared_actions += len(shared)
        for f, n in action_counts.items():
            legal_nonkeep_actions_by_family[f] += n
        if state == "SWEET_ONLY":
            only_family_uid["SWEET_QALB14"] += 1
            only_family_clusters["SWEET_QALB14"].add(
                aset["cluster_id"]
            )
        elif state == "SEQ2SEQ_GED_MORPH_ONLY":
            only_family_uid["SEQ2SEQ_GED_MORPH"] += 1
            only_family_clusters["SEQ2SEQ_GED_MORPH"].add(
                aset["cluster_id"]
            )

    family_summary = {
        "record_id": "MPSEF_V4_STAGE2_FAMILY_SUMMARY_V1",
        "status": "PASS",
        "cases": EXPECTED_CASES,
        "clusters": EXPECTED_CLUSTERS,
        "families": list(FAMILIES),
        "p1_p3_same_family": True,
        "SOURCE_ONLY_INDEPENDENT_NONKEEP_FAMILY_COUNT": {
            "uid_histogram": {
                str(i): family_count_uid[i]
                for i in (0, 1, 2)
            },
            "cluster_presence_histogram": {
                str(i): len(family_count_clusters[i])
                for i in (0, 1, 2)
            },
            "cluster_histogram_semantics":
                "distinct cluster_id with >=1 qualifying UID per bin; "
                "bins may overlap",
        },
        "SOURCE_ONLY_FAMILY_AVAILABILITY_STATE": {
            "uid_counts": {
                k: availability_uid[k]
                for k in (
                    "NONE",
                    "SWEET_ONLY",
                    "SEQ2SEQ_GED_MORPH_ONLY",
                    "BOTH_FAMILIES",
                )
            },
            "cluster_presence_counts": {
                k: len(availability_clusters[k])
                for k in (
                    "NONE",
                    "SWEET_ONLY",
                    "SEQ2SEQ_GED_MORPH_ONLY",
                    "BOTH_FAMILIES",
                )
            },
            "cluster_histogram_semantics":
                "distinct cluster_id with >=1 qualifying UID per state; "
                "bins may overlap",
        },
        "SOURCE_ONLY_CROSS_FAMILY_EXACT_OUTPUT_AGREEMENT": {
            "uid_count": len(shared_uids),
            "cluster_count": len(shared_clusters),
            "total_shared_actions": shared_actions,
            "interpretation_boundary":
                "literal legal non-KEEP output agreement only; "
                "not correctness evidence",
        },
        "SOURCE_ONLY_LEAVE_ONE_FAMILY_OUT":
            base_summary["source_only_leave_one_family_out"],
        "family_dominance_diagnostics": {
            "legal_nonkeep_action_family_provenance_counts":
                dict(legal_nonkeep_actions_by_family),
            "uids_only_one_family_supplies_nonkeep":
                dict(only_family_uid),
            "clusters_only_one_family_supplies_nonkeep": {
                f: len(only_family_clusters[f])
                for f in FAMILIES
            },
            "uids_both_families_supply_nonkeep":
                availability_uid["BOTH_FAMILIES"],
            "clusters_both_families_supply_nonkeep":
                len(availability_clusters["BOTH_FAMILIES"]),
        },
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "family_consensus_activated": False,
    }

    p1_by = {r["uid"]: r for r in p1}
    p3_by = {r["uid"]: r for r in p3}
    p1p3_pairs = [
        (
            p1_by[uid].get("full_proposer_output"),
            p3_by[uid].get("full_proposer_output"),
        )
        for uid in p1_by
    ]
    p3_parent_burden = burden(p1p3_pairs)

    stage_b_uid = Counter(
        p3_by[uid].get(
            "stage_b_domain_from_p1",
            "UNAVAILABLE_COMPARISON",
        )
        for uid in p3_by
    )
    stage_b_cluster = {
        cat: len(
            {
                p3_by[uid]["cluster_id"]
                for uid in p3_by
                if p3_by[uid].get(
                    "stage_b_domain_from_p1",
                    "UNAVAILABLE_COMPARISON",
                ) == cat
            }
        )
        for cat in STAGE_B_CATEGORIES
    }

    augmented = dict(base_summary)
    augmented["record_id"] = "MPSEF_V4_STAGE2_DIVERSITY_SUMMARY_V1"
    augmented["protocol_completion_version"] = VERSION
    augmented["derived_from_analysis_run"] = 36923877787
    augmented["derived_from_analysis_artifact_id"] = 11192953283
    augmented["derived_from_analysis_artifact_digest"] = (
        "sha256:" + EXPECTED_ANALYSIS_ARTIFACT_DIGEST
    )
    augmented["per_proposer_protocol_diagnostics"] = proposer_protocol
    augmented["family_summary_file"] = (
        "MPSEF_V4_STAGE2_FAMILY_SUMMARY_V1.json"
    )
    augmented["p2_full_population_diagnostics"] = p2_diagnostics(p2)
    augmented.setdefault("p3_specific", {})[
        "p1_to_p3_change_burden"
    ] = p3_parent_burden
    augmented["p3_specific"]["stage_b_classifier_version"] = (
        "MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1"
    )
    augmented["p3_specific"][
        "stage_b_domain_uid_counts_all_categories"
    ] = {
        cat: stage_b_uid[cat]
        for cat in STAGE_B_CATEGORIES
    }
    augmented["p3_specific"][
        "stage_b_domain_cluster_presence_all_categories"
    ] = stage_b_cluster
    augmented["scientific_boundary"] = {
        "source_only": True,
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "family_consensus_activated": False,
    }

    copies = {
        ad / "MPSEF_V4_STAGE2_FULL_CF_PROPOSER_ROWS_V2.jsonl":
            out / "MPSEF_V4_STAGE2_PROPOSER_ROWS_V1.jsonl",
        ad / "MPSEF_V4_STAGE2_FULL_CF_SOURCE_ONLY_ACTION_SETS_V2.jsonl":
            out / "MPSEF_V4_STAGE2_LEGAL_ACTION_SETS_V1.jsonl",
        ad / "MPSEF_V4_STAGE2_FULL_CF_FAILURES_V1.jsonl":
            out / "MPSEF_V4_STAGE2_FAILURES_V1.jsonl",
        ad / "MPSEF_V4_STAGE2_FULL_CF_RUNTIME_V1.json":
            out / "MPSEF_V4_STAGE2_RUNTIME_V1.json",
    }
    for src, dst in copies.items():
        shutil.copyfile(src, dst)

    diversity_path = out / "MPSEF_V4_STAGE2_DIVERSITY_SUMMARY_V1.json"
    diversity_path.write_text(
        json.dumps(augmented, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    family_path = out / "MPSEF_V4_STAGE2_FAMILY_SUMMARY_V1.json"
    family_path.write_text(
        json.dumps(family_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    protocol_summary = {
        "record_id": VERSION,
        "status": "PASS",
        "historical_analysis_run_preserved": 36923877787,
        "historical_analysis_artifact_id": 11192953283,
        "historical_analysis_artifact_digest":
            "sha256:" + EXPECTED_ANALYSIS_ARTIFACT_DIGEST,
        "protocol_gaps_closed": [
            "EXACT_REQUIRED_ARTIFACT_FILENAMES",
            "FAMILY_SUMMARY_ARTIFACT",
            "INDEPENDENT_NONKEEP_FAMILY_COUNT",
            "FAMILY_AVAILABILITY_STATE",
            "CROSS_FAMILY_EXACT_OUTPUT_AGREEMENT",
            "FAMILY_DOMINANCE_DIAGNOSTICS",
            "PER_PROPOSER_CLUSTER_STATE_COUNTS",
            "PER_PROPOSER_FAILURE_REASON_MATRICES",
            "P2_FULL_POPULATION_DIAGNOSTICS",
            "P1_TO_P3_CHANGE_BURDEN",
            "STAGE_B_ALL_FROZEN_CATEGORIES",
        ],
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "family_consensus_activated": False,
    }
    protocol_path = out / "MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2.json"
    protocol_path.write_text(
        json.dumps(protocol_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    required = [
        out / "MPSEF_V4_STAGE2_PROPOSER_ROWS_V1.jsonl",
        out / "MPSEF_V4_STAGE2_LEGAL_ACTION_SETS_V1.jsonl",
        diversity_path,
        family_path,
        out / "MPSEF_V4_STAGE2_FAILURES_V1.jsonl",
        out / "MPSEF_V4_STAGE2_RUNTIME_V1.json",
        protocol_path,
    ]
    ledger = out / "MPSEF_V4_STAGE2_SHA256.txt"
    ledger.write_text(
        "".join(
            f"{sha_file(p)}  {p.name}\n"
            for p in required
        ),
        encoding="utf-8",
    )

    assert sum(family_count_uid.values()) == EXPECTED_CASES
    assert sum(availability_uid.values()) == EXPECTED_CASES
    assert (
        set(family_summary["SOURCE_ONLY_LEAVE_ONE_FAMILY_OUT"])
        == set(FAMILIES)
    )
    assert (
        augmented["p3_specific"]["stage_b_classifier_version"]
        == "MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1"
    )
    assert (
        augmented["scientific_boundary"]["gold_reference_consulted"]
        is False
    )
    assert augmented["scientific_boundary"]["r_joint_computed"] is False
    assert (
        len(load_jsonl(out / "MPSEF_V4_STAGE2_PROPOSER_ROWS_V1.jsonl"))
        == EXPECTED_CASES * 3
    )
    assert (
        len(load_jsonl(out / "MPSEF_V4_STAGE2_LEGAL_ACTION_SETS_V1.jsonl"))
        == EXPECTED_CASES
    )
    print(
        json.dumps(
            protocol_summary,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
