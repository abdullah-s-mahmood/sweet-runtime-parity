#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib

from mpsef_rjoint_core_v2 import (
    FAMILIES as ERROR_FAMILIES,
    FAMILY_MAP_VERSION,
    MATCHING_VERSION,
    build_targets,
    evaluate_action_against_gold,
)

SCORER_VERSION = "MPSEF_RJOINT_SCORER_V4_2_FULL_REFERENCE_PROJECTION_HARDENED"
PUNCTUATION_POLICY_VERSION = "MPSEF_V4_1_FULL_REFERENCE_PRIMARY_PROJECTION_V1"
RESULT_SCHEMA_VERSION = "MPSEF_RJOINT_V4_2_RESULT_SCHEMA_V1"

PROPOSER_IDS = {
    "P1": "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2",
    "P2": "P2_V2_ARABART_GED_MORPH_WORDALIGNED",
    "P3": "P3_V1_SWEET_NOPNX2_PNX1",
}
FAMILY_IDS = {
    "SWEET": "SWEET_QALB14",
    "SEQ2SEQ": "SEQ2SEQ_GED_MORPH",
}
GROUPS = ("P1", "P2", "P3", "SWEET", "SEQ2SEQ", "ROSTER")
WEAK_ROUTES = {
    "INSERT_ROUTE": frozenset({"INSERT"}),
    "BOUNDARY_ROUTE": frozenset({"SPLIT", "MERGE"}),
}


def is_keep(action):
    return bool(action.get("keep_semantics", False))


def provenance(action):
    return action.get("provenance") or []


def _sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_action_set(action_set, expected_source_sha=None, max_actions=4):
    actions = action_set.get("actions")
    if not isinstance(actions, list):
        raise RuntimeError("ACTION_SET_ACTIONS_MISSING")
    if not (1 <= len(actions) <= max_actions):
        raise RuntimeError(f"ACTION_SET_SIZE_VIOLATION:{len(actions)}")
    if action_set.get("unique_action_count") not in (None, len(actions)):
        raise RuntimeError("ACTION_SET_COUNT_FIELD_MISMATCH")

    keeps = [a for a in actions if is_keep(a)]
    if len(keeps) != 1:
        raise RuntimeError(f"KEEP_CARDINALITY_VIOLATION:{len(keeps)}")
    keep_output = keeps[0].get("output")
    if not isinstance(keep_output, str):
        raise RuntimeError("KEEP_OUTPUT_MISSING")

    source_sha = action_set.get("source_sha256")
    if source_sha != _sha_text(keep_output):
        raise RuntimeError("KEEP_OUTPUT_SOURCE_SHA_MISMATCH")
    if expected_source_sha is not None and source_sha != expected_source_sha:
        raise RuntimeError("ACTION_SOURCE_IDENTITY_MISMATCH")

    seen_ids = set()
    seen_outputs = set()
    for action in actions:
        aid = action.get("action_id")
        if not isinstance(aid, str) or not aid:
            raise RuntimeError("ACTION_ID_MISSING")
        if aid in seen_ids:
            raise RuntimeError("DUPLICATE_ACTION_ID")
        seen_ids.add(aid)

        output = action.get("output")
        if not isinstance(output, str):
            raise RuntimeError("ACTION_OUTPUT_MISSING")
        if output in seen_outputs:
            raise RuntimeError("DUPLICATE_LITERAL_OUTPUT")
        seen_outputs.add(output)

        if action.get("output_sha256") != _sha_text(output):
            raise RuntimeError("ACTION_OUTPUT_SHA_MISMATCH")

        if not is_keep(action):
            if output == keep_output:
                raise RuntimeError("NONKEEP_KEEP_EQUIVALENT_OUTPUT")
            prov = provenance(action)
            if not prov:
                raise RuntimeError("NONKEEP_PROVENANCE_MISSING")
            prov_keys = [
                (p.get("proposer_id"), p.get("proposer_version"))
                for p in prov
            ]
            if len(set(prov_keys)) != len(prov_keys):
                raise RuntimeError("DUPLICATE_PROVENANCE_ENTRY")
            expected_families = sorted({
                p.get("family_id") for p in prov
                if p.get("family_id") not in (None, "KEEP")
            })
            if "family_ids" in action and sorted(action.get("family_ids") or []) != expected_families:
                raise RuntimeError("ACTION_FAMILY_IDS_MISMATCH")
    return True


def eligible_actions(action_set, group):
    if group not in GROUPS:
        raise RuntimeError(f"UNKNOWN_GROUP:{group}")
    selected = []
    for action in action_set["actions"]:
        if is_keep(action):
            selected.append(action)
            continue
        prov = provenance(action)
        if group == "ROSTER":
            selected.append(action)
        elif group in PROPOSER_IDS:
            pid = PROPOSER_IDS[group]
            if any(p.get("proposer_id") == pid for p in prov):
                selected.append(action)
        else:
            fid = FAMILY_IDS[group]
            if any(p.get("family_id") == fid for p in prov):
                selected.append(action)
    if not any(is_keep(a) for a in selected):
        raise RuntimeError("GROUP_KEEP_MISSING")
    return selected


def independent_nonkeep_families(action_set):
    out = set()
    allowed = set(FAMILY_IDS.values())
    for action in action_set["actions"]:
        if is_keep(action):
            continue
        for p in provenance(action):
            fid = p.get("family_id")
            if fid in allowed:
                out.add(fid)
    return out


def validate_scoring_result(result, target_count):
    if not isinstance(result, dict):
        raise RuntimeError("SCORER_RESULT_NON_DICT")
    required = {"matched_indices", "correct", "proposed", "gold", "extra"}
    if not required.issubset(result):
        raise RuntimeError("SCORER_RESULT_FIELDS_MISSING")
    matched = result["matched_indices"]
    if not isinstance(matched, list) or any(not isinstance(i, int) for i in matched):
        raise RuntimeError("SCORER_MATCHED_INDICES_MALFORMED")
    if len(set(matched)) != len(matched):
        raise RuntimeError("SCORER_DUPLICATE_TARGET_CREDIT")
    if any(i < 0 or i >= target_count for i in matched):
        raise RuntimeError("SCORER_TARGET_INDEX_OUT_OF_RANGE")
    if result["gold"] != target_count:
        raise RuntimeError("SCORER_DENOMINATOR_MISMATCH")
    if result["correct"] != len(matched):
        raise RuntimeError("SCORER_CORRECT_COUNT_MISMATCH")
    if result["proposed"] < result["correct"]:
        raise RuntimeError("SCORER_PROPOSED_LT_CORRECT")
    if result["extra"] != result["proposed"] - result["correct"]:
        raise RuntimeError("SCORER_EXTRA_MISMATCH")
    return result


def score_all_actions(action_set, source, all_gold, evaluate_fn):
    scored = {}
    n = len(all_gold)
    for action in action_set["actions"]:
        try:
            raw = evaluate_fn(action["output"], source, all_gold)
            scored[action["action_id"]] = validate_scoring_result(raw, n)
        except Exception as exc:
            scored[action["action_id"]] = {
                "error": f"{type(exc).__name__}: {str(exc)[:300]}"
            }
    return scored


def group_results(action_set, scored, subset_indices, group):
    subset = set(subset_indices)
    eligible = eligible_actions(action_set, group)
    successful, failures = [], []
    for action in eligible:
        result = scored[action["action_id"]]
        if "error" in result:
            failures.append(action)
        else:
            successful.append((action, result))

    recovered = []
    recovered_clean = []
    for action, result in successful:
        matched = set(result["matched_indices"])
        count = len(matched & subset)
        recovered.append((action, result, count))
        if result["extra"] == 0:
            recovered_clean.append((action, result, count))

    lower = max((x[2] for x in recovered), default=0)
    upper = len(subset) if failures else lower
    clean_lower = max((x[2] for x in recovered_clean), default=0)
    clean_upper = len(subset) if failures else clean_lower

    complete_known = any(
        subset.issubset(set(result["matched_indices"])) and result["extra"] == 0
        for _, result in successful
    )
    complete_possible = bool(complete_known or (subset and failures))

    return {
        "group": group,
        "subset_count": len(subset),
        "lower": lower,
        "upper": upper,
        "clean_lower": clean_lower,
        "clean_upper": clean_upper,
        "complete_known": complete_known,
        "complete_possible": complete_possible,
        "successful": successful,
        "failures": failures,
    }


def all_reference_complete_bounds(action_set, scored, all_target_indices, group):
    subset = set(all_target_indices)
    eligible = eligible_actions(action_set, group)
    successful, failures = [], []
    for action in eligible:
        result = scored[action["action_id"]]
        if "error" in result:
            failures.append(action)
        else:
            successful.append((action, result))
    known = any(
        subset.issubset(set(result["matched_indices"])) and result["extra"] == 0
        for _, result in successful
    )
    possible = bool(known or (subset and failures))
    return known, possible


def best_subset_whole_action(group_result, subset_indices):
    subset = set(subset_indices)
    values = []
    for action, result in group_result["successful"]:
        matched = set(result["matched_indices"])
        values.append((len(matched & subset), str(action.get("action_id", ""))))
    lower = max((x[0] for x in values), default=0)
    upper = len(subset) if group_result["failures"] else lower
    return lower, upper


def whole_action_additional_target_bounds(group_result, other_result, subset_indices):
    subset = set(subset_indices)
    if not subset:
        return set(), set()

    other_known = set()
    for _, result in other_result["successful"]:
        other_known |= (set(result["matched_indices"]) & subset)

    candidates = []
    for action, result in group_result["successful"]:
        exclusive = (set(result["matched_indices"]) & subset) - other_known
        candidates.append(
            (len(exclusive), str(action.get("action_id", "")), exclusive)
        )

    if candidates:
        candidates.sort(key=lambda x: (-x[0], x[1]))
        best = set(candidates[0][2])
    else:
        best = set()

    lower = set() if other_result["failures"] else best
    upper = (subset - other_known) if group_result["failures"] else best
    if not lower.issubset(upper):
        raise RuntimeError("ADDITIONAL_TARGET_BOUNDS_INVALID")
    return lower, upper


def interval(pair, denominator):
    lo, hi = pair
    return {
        "lower_numerator": lo,
        "upper_numerator": hi,
        "denominator": denominator,
        "lower": None if denominator == 0 else lo / denominator,
        "upper": None if denominator == 0 else hi / denominator,
        "exact": None if denominator == 0 or lo != hi else lo / denominator,
    }


def difference_interval(a, b):
    if a["denominator"] != b["denominator"]:
        raise RuntimeError("INTERVAL_DENOMINATOR_MISMATCH")
    den = a["denominator"]
    if den == 0:
        return {"lower": None, "upper": None, "exact": None, "denominator": 0}
    lo = max(0.0, a["lower"] - b["upper"])
    hi = max(0.0, a["upper"] - b["lower"])
    return {
        "lower": lo,
        "upper": hi,
        "exact": lo if abs(lo - hi) < 1e-15 else None,
        "denominator": den,
    }


def gate_95(iv):
    den = iv["denominator"]
    if den == 0:
        return "INCONCLUSIVE_NO_TARGETS"
    lo = iv["lower_numerator"]
    hi = iv["upper_numerator"]
    if 20 * lo >= 19 * den:
        return "PASS_CANDIDATE_AVAILABILITY"
    if 20 * hi < 19 * den:
        return "FAIL_CANDIDATE_AVAILABILITY"
    return "INCONCLUSIVE_INTERVAL_CROSSES_GATE"


def classify_reference_state(primary_count, punctuation_count):
    if primary_count > 0:
        return "PRIMARY_ERROR_PRESENT"
    if punctuation_count > 0:
        return "PUNCTUATION_ONLY_REFERENCE"
    return "ALL_REFERENCE_CLEAN"


def validate_measurement_identity_contract(actual, expected):
    required = (
        "source_manifest_sha256",
        "action_set_sha256",
        "scorer_sha256",
        "core_sha256",
        "matching_version",
        "family_map_version",
        "punctuation_policy_version",
        "population_uid_sha256",
        "gold_sha256",
        "python_version",
        "dependency_lock_sha256",
        "result_schema_version",
    )
    for key in required:
        if key not in actual or key not in expected:
            raise RuntimeError(f"IDENTITY_FIELD_MISSING:{key}")
        if actual[key] != expected[key]:
            raise RuntimeError(f"IDENTITY_MISMATCH:{key}")
    return True


def score_population_v4_2(
    lev,
    source_rows,
    action_sets,
    gold_by_uid,
    *,
    evaluate_fn=None,
    frozen_identity=None,
):
    if evaluate_fn is None:
        def evaluate_fn(output, source, gold):
            return evaluate_action_against_gold(lev, output, source, gold)

    source = {}
    for row in source_rows:
        uid = row["uid"]
        if uid in source:
            raise RuntimeError(f"DUPLICATE_SOURCE_UID:{uid}")
        source[uid] = row

    actions = {}
    for row in action_sets:
        uid = row["uid"]
        if uid in actions:
            raise RuntimeError(f"DUPLICATE_ACTION_UID:{uid}")
        actions[uid] = row

    uids = sorted(source)
    if set(uids) != set(actions) or set(uids) != set(gold_by_uid):
        raise RuntimeError("POPULATION_IDENTITY_MISMATCH")

    prepared = {}
    all_target_ids = set()
    primary_den = 0
    punctuation_den = 0
    all_den = 0
    family_den = Counter()
    route_den = Counter()
    reference_state_counts = Counter()
    primary_error_sentences = 0
    all_error_sentences = 0

    for uid in uids:
        all_gold = gold_by_uid[uid]
        targets = build_targets(uid, all_gold)
        for target in targets:
            tid = target["target_id"]
            if tid in all_target_ids:
                raise RuntimeError(f"DUPLICATE_FROZEN_TARGET_ID:{tid}")
            all_target_ids.add(tid)

        primary_idx = [
            i for i, t in enumerate(targets)
            if t["scope"] != "PUNCTUATION_ONLY"
        ]
        punctuation_idx = [
            i for i, t in enumerate(targets)
            if t["scope"] == "PUNCTUATION_ONLY"
        ]
        family_idx = defaultdict(list)
        for i in primary_idx:
            family_idx[targets[i]["family"]].append(i)

        route_idx = {}
        for route, members in WEAK_ROUTES.items():
            route_idx[route] = [
                i for i in primary_idx
                if targets[i]["family"] in members
            ]

        primary_den += len(primary_idx)
        punctuation_den += len(punctuation_idx)
        all_den += len(targets)
        for fam, idxs in family_idx.items():
            family_den[fam] += len(idxs)
        for route, idxs in route_idx.items():
            route_den[route] += len(idxs)

        state = classify_reference_state(len(primary_idx), len(punctuation_idx))
        reference_state_counts[state] += 1
        primary_error_sentences += int(bool(primary_idx))
        all_error_sentences += int(bool(targets))

        prepared[uid] = {
            "all_gold": all_gold,
            "targets": targets,
            "primary_idx": primary_idx,
            "punctuation_idx": punctuation_idx,
            "family_idx": family_idx,
            "route_idx": route_idx,
            "reference_state": state,
        }

    primary_bounds = {g: [0, 0] for g in GROUPS}
    primary_clean_bounds = {g: [0, 0] for g in GROUPS}
    punctuation_bounds = {g: [0, 0] for g in GROUPS}
    primary_complete = {g: [0, 0] for g in GROUPS}
    all_complete = {g: [0, 0] for g in GROUPS}
    family_bounds = {
        g: {fam: [0, 0] for fam in ERROR_FAMILIES}
        for g in GROUPS
    }
    route_bounds = {
        g: {route: [0, 0] for route in WEAK_ROUTES}
        for g in ("SWEET", "SEQ2SEQ", "ROSTER")
    }
    route_add = {
        side: {
            route: {
                "target_lower": set(),
                "target_upper": set(),
                "cluster_lower": set(),
                "cluster_upper": set(),
            }
            for route in WEAK_ROUTES
        }
        for side in ("SWEET", "SEQ2SEQ")
    }
    scoring_failures = []
    clean_activity = Counter()
    punctuation_only_activity = Counter()
    sentence_records = []

    for uid in uids:
        src = source[uid]
        aset = actions[uid]
        if aset.get("source_sha256") != src.get("source_sha256"):
            raise RuntimeError(f"{uid}:ACTION_SOURCE_HASH_MISMATCH")
        if aset.get("uid") != uid:
            raise RuntimeError(f"{uid}:ACTION_UID_MISMATCH")
        validate_action_set(aset, src.get("source_sha256"))

        p = prepared[uid]
        scored = score_all_actions(aset, src["source"], p["all_gold"], evaluate_fn)
        groups = {}
        for g in GROUPS:
            groups[g] = group_results(aset, scored, p["primary_idx"], g)
            pg = groups[g]
            primary_bounds[g][0] += pg["lower"]
            primary_bounds[g][1] += pg["upper"]
            primary_clean_bounds[g][0] += pg["clean_lower"]
            primary_clean_bounds[g][1] += pg["clean_upper"]

            punct = group_results(aset, scored, p["punctuation_idx"], g)
            punctuation_bounds[g][0] += punct["lower"]
            punctuation_bounds[g][1] += punct["upper"]

            if p["primary_idx"]:
                primary_complete[g][0] += int(pg["complete_known"])
                primary_complete[g][1] += int(pg["complete_possible"])

            if p["targets"]:
                known, possible = all_reference_complete_bounds(
                    aset, scored, range(len(p["targets"])), g
                )
                all_complete[g][0] += int(known)
                all_complete[g][1] += int(possible)

            for fam in ERROR_FAMILIES:
                lo, hi = best_subset_whole_action(pg, p["family_idx"].get(fam, []))
                family_bounds[g][fam][0] += lo
                family_bounds[g][fam][1] += hi

            for action in pg["failures"]:
                scoring_failures.append({
                    "uid": uid,
                    "group": g,
                    "action_id": action["action_id"],
                })

        for g in ("SWEET", "SEQ2SEQ", "ROSTER"):
            for route, idxs in p["route_idx"].items():
                lo, hi = best_subset_whole_action(groups[g], idxs)
                route_bounds[g][route][0] += lo
                route_bounds[g][route][1] += hi

        for side, other in (("SWEET", "SEQ2SEQ"), ("SEQ2SEQ", "SWEET")):
            for route, idxs in p["route_idx"].items():
                lo_set, hi_set = whole_action_additional_target_bounds(
                    groups[side], groups[other], idxs
                )
                for i in lo_set:
                    route_add[side][route]["target_lower"].add(p["targets"][i]["target_id"])
                for i in hi_set:
                    route_add[side][route]["target_upper"].add(p["targets"][i]["target_id"])
                if lo_set:
                    route_add[side][route]["cluster_lower"].add(src.get("cluster_id"))
                if hi_set:
                    route_add[side][route]["cluster_upper"].add(src.get("cluster_id"))

        if p["reference_state"] == "ALL_REFERENCE_CLEAN":
            for g in GROUPS:
                clean_activity[g] += int(any(
                    not is_keep(action) and result["extra"] > 0
                    for action, result in groups[g]["successful"]
                ))
        elif p["reference_state"] == "PUNCTUATION_ONLY_REFERENCE":
            for g in GROUPS:
                punctuation_only_activity[g] += int(any(
                    len(set(result["matched_indices"]) & set(p["punctuation_idx"])) > 0
                    for _, result in groups[g]["successful"]
                ))

        sentence_records.append({
            "uid": uid,
            "case_id": src.get("case_id"),
            "cluster_id": src.get("cluster_id"),
            "reference_state": p["reference_state"],
            "all_target_count": len(p["targets"]),
            "primary_target_count": len(p["primary_idx"]),
            "punctuation_target_count": len(p["punctuation_idx"]),
            "scoring_failure_action_ids": sorted({
                item["action_id"] for item in scoring_failures if item["uid"] == uid
            }),
        })

    primary_intervals = {
        g: interval(primary_bounds[g], primary_den) for g in GROUPS
    }
    primary_clean_intervals = {
        g: interval(primary_clean_bounds[g], primary_den) for g in GROUPS
    }
    punctuation_intervals = {
        g: interval(punctuation_bounds[g], punctuation_den) for g in GROUPS
    }

    route_summary = {}
    for route in WEAK_ROUTES:
        d = route_den[route]
        roster_iv = interval(route_bounds["ROSTER"][route], d)
        sweet_iv = interval(route_bounds["SWEET"][route], d)
        seq_iv = interval(route_bounds["SEQ2SEQ"][route], d)
        route_summary[route] = {
            "target_denominator": d,
            "members": sorted(WEAK_ROUTES[route]),
            "SWEET": sweet_iv,
            "SEQ2SEQ": seq_iv,
            "ROSTER": roster_iv,
            "SWEET_gain_vs_SEQ2SEQ": difference_interval(roster_iv, seq_iv),
            "SEQ2SEQ_gain_vs_SWEET": difference_interval(roster_iv, sweet_iv),
            "SWEET_additional_targets_lower": len(route_add["SWEET"][route]["target_lower"]),
            "SWEET_additional_targets_upper": len(route_add["SWEET"][route]["target_upper"]),
            "SWEET_additional_clusters_lower": len(route_add["SWEET"][route]["cluster_lower"]),
            "SWEET_additional_clusters_upper": len(route_add["SWEET"][route]["cluster_upper"]),
            "SEQ2SEQ_additional_targets_lower": len(route_add["SEQ2SEQ"][route]["target_lower"]),
            "SEQ2SEQ_additional_targets_upper": len(route_add["SEQ2SEQ"][route]["target_upper"]),
            "SEQ2SEQ_additional_clusters_lower": len(route_add["SEQ2SEQ"][route]["cluster_lower"]),
            "SEQ2SEQ_additional_clusters_upper": len(route_add["SEQ2SEQ"][route]["cluster_upper"]),
            "whole_action_semantics": True,
        }

    result = {
        "record_id": RESULT_SCHEMA_VERSION,
        "scorer_version": SCORER_VERSION,
        "matching_version": MATCHING_VERSION,
        "family_map_version": FAMILY_MAP_VERSION,
        "punctuation_policy_version": PUNCTUATION_POLICY_VERSION,
        "claim_scope": (
            "DEVELOPMENT / ADAPTIVELY_CONSUMED / REFERENCE_RELATIVE / "
            "NOT_INDEPENDENT_GENERALIZATION"
        ),
        "uids": len(uids),
        "reference_state_counts": dict(reference_state_counts),
        "primary_target_denominator": primary_den,
        "punctuation_target_denominator": punctuation_den,
        "all_reference_target_denominator": all_den,
        "PRIMARY_RECOVERY": primary_intervals,
        "PRIMARY_CLEAN_RECOVERY": primary_clean_intervals,
        "PUNCTUATION_RECOVERY": punctuation_intervals,
        "PRIMARY_COMPLETE_REPAIR": {
            g: interval(primary_complete[g], primary_error_sentences)
            for g in GROUPS
        },
        "ALL_REFERENCE_COMPLETE_REPAIR": {
            g: interval(all_complete[g], all_error_sentences)
            for g in GROUPS
        },
        "ERROR_FAMILY_PRIMARY_RECOVERY": {
            g: {
                fam: interval(family_bounds[g][fam], family_den[fam])
                for fam in ERROR_FAMILIES
            }
            for g in GROUPS
        },
        "error_family_denominators": dict(family_den),
        "WEAK_ROUTE_FAMILY_EVIDENCE": route_summary,
        "ROSTER_PRIMARY_CANDIDATE_AVAILABILITY_GATE_95":
            gate_95(primary_intervals["ROSTER"]),
        "ALL_REFERENCE_CLEAN_candidate_activity_uid_counts": dict(clean_activity),
        "PUNCTUATION_ONLY_REFERENCE_supported_activity_uid_counts":
            dict(punctuation_only_activity),
        "scoring_failures": scoring_failures,
        "sentence_records": sentence_records,
        "reference_supported_wording": {
            "matched": "REFERENCE_SUPPORTED",
            "extra": "REFERENCE_UNSUPPORTED_EXTRA",
            "warning": (
                "REFERENCE_UNSUPPORTED_EXTRA is not equivalent to "
                "LINGUISTICALLY_WRONG"
            ),
        },
        "selector_trained": False,
        "family_consensus_activated": False,
        "p4_used": False,
        "gold_loader_embedded": False,
    }
    if frozen_identity is not None:
        result["frozen_identity"] = dict(frozen_identity)
    return result
