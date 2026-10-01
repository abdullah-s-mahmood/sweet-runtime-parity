#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict

SCORER_VERSION = "MPSEF_RJOINT_SCORER_V4_SOURCE_FREE_PRE_GOLD"
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


def _provenance(action):
    return action.get("provenance") or []


def is_keep(action):
    return bool(action.get("keep_semantics", False))


def validate_action_set(action_set, expected_source_sha=None, max_actions=4):
    actions = action_set.get("actions")
    if not isinstance(actions, list):
        raise RuntimeError("ACTION_SET_ACTIONS_MISSING")
    if not (1 <= len(actions) <= max_actions):
        raise RuntimeError(f"ACTION_SET_SIZE_VIOLATION:{len(actions)}")
    if action_set.get("unique_action_count") not in (None, len(actions)):
        raise RuntimeError("ACTION_SET_COUNT_FIELD_MISMATCH")
    keep = [a for a in actions if is_keep(a)]
    if len(keep) != 1:
        raise RuntimeError(f"KEEP_CARDINALITY_VIOLATION:{len(keep)}")
    if expected_source_sha is not None and action_set.get("source_sha256") != expected_source_sha:
        raise RuntimeError("ACTION_SOURCE_IDENTITY_MISMATCH")
    seen = set()
    for a in actions:
        aid = a.get("action_id")
        if not isinstance(aid, str) or not aid:
            raise RuntimeError("ACTION_ID_MISSING")
        if aid in seen:
            raise RuntimeError("DUPLICATE_ACTION_ID")
        seen.add(aid)
        if not isinstance(a.get("output"), str):
            raise RuntimeError("ACTION_OUTPUT_MISSING")
        if not is_keep(a) and not _provenance(a):
            raise RuntimeError("NONKEEP_PROVENANCE_MISSING")
    return True


def eligible_actions(action_set, group):
    if group not in GROUPS:
        raise RuntimeError(f"UNKNOWN_GROUP:{group}")
    out = []
    for action in action_set["actions"]:
        if is_keep(action):
            out.append(action)
            continue
        prov = _provenance(action)
        if group == "ROSTER":
            out.append(action)
        elif group in PROPOSER_IDS:
            pid = PROPOSER_IDS[group]
            if any(p.get("proposer_id") == pid for p in prov):
                out.append(action)
        elif group in FAMILY_IDS:
            fid = FAMILY_IDS[group]
            if any(p.get("family_id") == fid for p in prov):
                out.append(action)
    if not any(is_keep(a) for a in out):
        raise RuntimeError("GROUP_KEEP_MISSING")
    return out


def independent_nonkeep_families(action_set):
    fams = set()
    for a in action_set["actions"]:
        if is_keep(a):
            continue
        for p in _provenance(a):
            fid = p.get("family_id")
            if fid in FAMILY_IDS.values():
                fams.add(fid)
    return fams


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


def score_all_actions(action_set, source, primary_gold, evaluate_fn):
    target_count = len(primary_gold)
    scored = {}
    for action in action_set["actions"]:
        try:
            raw = evaluate_fn(action["output"], source, primary_gold)
            scored[action["action_id"]] = validate_scoring_result(raw, target_count)
        except Exception as exc:
            scored[action["action_id"]] = {
                "error": f"{type(exc).__name__}: {str(exc)[:300]}"
            }
    return scored


def group_action_results(action_set, scored, target_count, group):
    """M04-preserving group aggregation over eligible whole actions."""
    eligible = eligible_actions(action_set, group)
    successful, failures = [], []
    for action in eligible:
        result = scored[action["action_id"]]
        if "error" in result:
            failures.append(action)
        else:
            if result.get("gold") != target_count:
                raise RuntimeError("GROUP_SCORER_DENOMINATOR_MISMATCH")
            successful.append((action, result))
    lower = max((r["correct"] for _, r in successful), default=0)
    upper = target_count if failures else lower
    return {
        "group": group,
        "target_count": target_count,
        "lower": lower,
        "upper": upper,
        "exact": (not failures or lower == upper),
        "successful": successful,
        "failures": failures,
    }


def best_clean_bounds(group_result, target_count):
    known = [
        r["correct"] for _, r in group_result["successful"]
        if r["extra"] == 0
    ]
    lower = max(known, default=0)
    upper = target_count if group_result["failures"] else lower
    return lower, upper


def best_target_subset_bounds(group_result, target_indices):
    idxs = set(target_indices)
    known = []
    for _, r in group_result["successful"]:
        matched = set(r["matched_indices"])
        known.append(sum(i in matched for i in idxs))
    lower = max(known, default=0)
    upper = len(idxs) if group_result["failures"] else lower
    return lower, upper


def whole_action_additional_target_bounds(group_result, other_result, target_indices):
    """M05-preserving one-whole-action exclusivity bounds."""
    fam = set(target_indices)
    if not fam:
        return set(), set()

    other_known = set()
    for _, r in other_result["successful"]:
        other_known |= (set(r["matched_indices"]) & fam)

    def best_successful(g):
        candidates = []
        for a, r in g["successful"]:
            s = (set(r["matched_indices"]) & fam) - other_known
            candidates.append((len(s), str(a.get("action_id", "")), s))
        if not candidates:
            return set()
        candidates.sort(key=lambda x: (-x[0], x[1]))
        return set(candidates[0][2])

    lower = set() if other_result["failures"] else best_successful(group_result)
    upper = (fam - other_known) if group_result["failures"] else best_successful(group_result)
    if not lower.issubset(upper):
        raise RuntimeError("ADDITIONAL_TARGET_BOUNDS_INVALID")
    return lower, upper


def evaluate_sentence_v4(action_set, source, primary_gold, evaluate_fn):
    validate_action_set(action_set)
    scored = score_all_actions(action_set, source, primary_gold, evaluate_fn)
    target_count = len(primary_gold)
    groups = {
        g: group_action_results(action_set, scored, target_count, g)
        for g in GROUPS
    }
    return {"scored": scored, "groups": groups}


def freeze_primary_targets(targets):
    """Source-free helper for already-built target records."""
    primary = [t for t in targets if t.get("scope") != "PUNCTUATION_ONLY"]
    punctuation = [t for t in targets if t.get("scope") == "PUNCTUATION_ONLY"]
    ids = [t.get("target_id") for t in targets]
    if any(not isinstance(x, str) or not x for x in ids):
        raise RuntimeError("TARGET_ID_MISSING")
    if len(set(ids)) != len(ids):
        raise RuntimeError("DUPLICATE_TARGET_ID")
    return primary, punctuation


def score_population_source_free(records, evaluate_fn):
    """Synthetic/pre-gold population aggregator with no project-gold loader."""
    seen = set()
    prepared = []
    for rec in records:
        uid = rec["uid"]
        if uid in seen:
            raise RuntimeError("POPULATION_DUPLICATE_UID")
        seen.add(uid)
        aset = rec["action_set"]
        validate_action_set(aset, rec.get("source_sha256"))
        if aset.get("uid") not in (None, uid):
            raise RuntimeError("POPULATION_ACTION_UID_MISMATCH")
        primary, punctuation = freeze_primary_targets(rec.get("targets", []))
        prepared.append((rec, primary, punctuation))

    totals = {g: [0, 0] for g in GROUPS}
    clean_totals = {g: [0, 0] for g in GROUPS}
    complete = {g: [0, 0] for g in GROUPS}
    scoring_failures = []
    punctuation_count = 0
    primary_count = 0

    for rec, primary, punctuation in prepared:
        primary_count += len(primary)
        punctuation_count += len(punctuation)
        synthetic_gold = list(range(len(primary)))
        ev = evaluate_sentence_v4(
            rec["action_set"], rec["source"], synthetic_gold, evaluate_fn
        )
        for group, gr in ev["groups"].items():
            totals[group][0] += gr["lower"]
            totals[group][1] += gr["upper"]
            clo, chi = best_clean_bounds(gr, len(primary))
            clean_totals[group][0] += clo
            clean_totals[group][1] += chi
            repair_known = bool(primary) and any(
                r["correct"] == len(primary) and r["extra"] == 0
                for _, r in gr["successful"]
            )
            repair_possible = bool(repair_known or (primary and gr["failures"]))
            complete[group][0] += int(repair_known)
            complete[group][1] += int(repair_possible)
            for a in gr["failures"]:
                scoring_failures.append({
                    "uid": rec["uid"],
                    "group": group,
                    "action_id": a["action_id"],
                })

    return {
        "record_id": SCORER_VERSION,
        "uids": len(prepared),
        "primary_target_count": primary_count,
        "punctuation_target_count": punctuation_count,
        "target_recovery_bounds": {
            g: {"lower": v[0], "upper": v[1], "denominator": primary_count}
            for g, v in totals.items()
        },
        "clean_target_recovery_bounds": {
            g: {"lower": v[0], "upper": v[1], "denominator": primary_count}
            for g, v in clean_totals.items()
        },
        "complete_repair_sentence_bounds": {
            g: {"lower": v[0], "upper": v[1], "denominator": len(prepared)}
            for g, v in complete.items()
        },
        "scoring_failures": scoring_failures,
        "source_free": True,
        "project_gold_loaded": False,
        "r_joint_real_computed": False,
    }


def score_population_v4(lev, source_rows, action_sets, gold_by_uid, evaluate_fn=None):
    """Gold-aware scorer core with no gold-loading capability of its own.

    The caller must explicitly supply gold_by_uid after a later authorization.
    The complete target population is frozen before any action is scored.
    """
    from mpsef_rjoint_core_v2 import (
        FAMILIES as ERROR_FAMILIES,
        build_targets,
        evaluate_action_against_gold,
    )

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
    target_ids = set()
    primary_den = 0
    punctuation_den = 0
    family_den = defaultdict(int)
    erroneous_sentences = 0
    clean_sentences = 0

    for uid in uids:
        all_gold = gold_by_uid[uid]
        all_targets = build_targets(uid, all_gold)
        for t in all_targets:
            tid = t["target_id"]
            if tid in target_ids:
                raise RuntimeError(f"DUPLICATE_FROZEN_TARGET_ID:{tid}")
            target_ids.add(tid)

        primary_idx = [
            i for i, t in enumerate(all_targets)
            if t["scope"] != "PUNCTUATION_ONLY"
        ]
        punctuation_idx = [
            i for i, t in enumerate(all_targets)
            if t["scope"] == "PUNCTUATION_ONLY"
        ]
        primary_gold = [all_gold[i] for i in primary_idx]
        targets = [all_targets[i] for i in primary_idx]
        punctuation_targets = [all_targets[i] for i in punctuation_idx]

        primary_den += len(targets)
        punctuation_den += len(punctuation_targets)
        if targets:
            erroneous_sentences += 1
        else:
            clean_sentences += 1
        for t in targets:
            family_den[t["family"]] += 1

        prepared[uid] = {
            "primary_gold": primary_gold,
            "targets": targets,
            "punctuation_targets": punctuation_targets,
        }

    recovery = {g: [0, 0] for g in GROUPS}
    clean_recovery = {g: [0, 0] for g in GROUPS}
    complete = {g: [0, 0] for g in GROUPS}
    error_family = {
        g: {fam: [0, 0] for fam in ERROR_FAMILIES}
        for g in GROUPS
    }
    clean_sentence_activity = {
        g: {"sentences": 0, "nonkeep_scored_with_extra": 0}
        for g in GROUPS
    }
    scoring_failures = []
    sentence_records = []

    for uid in uids:
        src_row = source[uid]
        aset = actions[uid]
        if aset.get("source_sha256") != src_row.get("source_sha256"):
            raise RuntimeError(f"{uid}:ACTION_SOURCE_HASH_MISMATCH")
        validate_action_set(aset, src_row.get("source_sha256"))

        primary_gold = prepared[uid]["primary_gold"]
        targets = prepared[uid]["targets"]
        ev = evaluate_sentence_v4(aset, src_row["source"], primary_gold, evaluate_fn)
        fam_indices = defaultdict(list)
        for idx, t in enumerate(targets):
            fam_indices[t["family"]].append(idx)

        per_sentence = {
            "uid": uid,
            "case_id": src_row.get("case_id"),
            "cluster_id": src_row.get("cluster_id"),
            "primary_target_count": len(targets),
            "punctuation_target_count": len(prepared[uid]["punctuation_targets"]),
            "groups": {},
        }

        for group, gr in ev["groups"].items():
            recovery[group][0] += gr["lower"]
            recovery[group][1] += gr["upper"]
            clo, chi = best_clean_bounds(gr, len(targets))
            clean_recovery[group][0] += clo
            clean_recovery[group][1] += chi

            repair_known = bool(targets) and any(
                r["correct"] == len(targets) and r["extra"] == 0
                for _, r in gr["successful"]
            )
            repair_possible = bool(
                repair_known or (targets and gr["failures"])
            )
            if targets:
                complete[group][0] += int(repair_known)
                complete[group][1] += int(repair_possible)
            else:
                clean_sentence_activity[group]["sentences"] += 1
                clean_sentence_activity[group]["nonkeep_scored_with_extra"] += int(
                    any(
                        not is_keep(a) and r["extra"] > 0
                        for a, r in gr["successful"]
                    )
                )

            for fam in ERROR_FAMILIES:
                lo, hi = best_target_subset_bounds(gr, fam_indices.get(fam, []))
                error_family[group][fam][0] += lo
                error_family[group][fam][1] += hi

            for a in gr["failures"]:
                scoring_failures.append({
                    "uid": uid,
                    "group": group,
                    "action_id": a["action_id"],
                })

            per_sentence["groups"][group] = {
                "lower": gr["lower"],
                "upper": gr["upper"],
                "clean_lower": clo,
                "clean_upper": chi,
                "complete_repair_lower": repair_known,
                "complete_repair_upper": repair_possible,
                "scoring_failure_action_ids": sorted(
                    a["action_id"] for a in gr["failures"]
                ),
            }
        sentence_records.append(per_sentence)

    def interval(pair, den):
        lo, hi = pair
        return {
            "lower_numerator": lo,
            "upper_numerator": hi,
            "denominator": den,
            "lower": (lo / den if den else None),
            "upper": (hi / den if den else None),
            "exact": (lo / den if den and lo == hi else None),
        }

    return {
        "record_id": "MPSEF_RJOINT_V4_REFERENCE_RELATIVE_RESULT",
        "scorer_version": SCORER_VERSION,
        "claim_scope": (
            "DEVELOPMENT_FEASIBILITY / ADAPTIVELY_CONSUMED / "
            "REFERENCE_RELATIVE / NOT_INDEPENDENT_GENERALIZATION"
        ),
        "uids": len(uids),
        "erroneous_sentences": erroneous_sentences,
        "clean_sentences": clean_sentences,
        "primary_target_denominator": primary_den,
        "punctuation_target_denominator": punctuation_den,
        "target_recovery": {
            g: interval(recovery[g], primary_den) for g in GROUPS
        },
        "clean_target_recovery": {
            g: interval(clean_recovery[g], primary_den) for g in GROUPS
        },
        "complete_repair": {
            g: interval(complete[g], erroneous_sentences) for g in GROUPS
        },
        "error_family_target_recovery": {
            g: {
                fam: interval(error_family[g][fam], family_den[fam])
                for fam in ERROR_FAMILIES
            }
            for g in GROUPS
        },
        "error_family_denominators": dict(family_den),
        "clean_sentence_extra_edit_activity": clean_sentence_activity,
        "scoring_failures": scoring_failures,
        "sentence_records": sentence_records,
        "gold_supplied_by_caller": True,
        "gold_loader_embedded": False,
        "selector_trained": False,
        "family_consensus_activated": False,
        "p4_used": False,
    }


def dump_public_shape(obj):
    """JSON-safe compact representation useful for synthetic artifacts."""
    def clean(x):
        if isinstance(x, dict):
            return {k: clean(v) for k, v in x.items() if k not in {"successful", "failures"}}
        if isinstance(x, list):
            return [clean(v) for v in x]
        return x
    return json.loads(json.dumps(clean(obj), ensure_ascii=False))
