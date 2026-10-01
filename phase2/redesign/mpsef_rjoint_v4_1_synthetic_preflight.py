#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mpsef_rjoint_score_v4_1 import (
    FAMILY_IDS,
    GROUPS,
    PROPOSER_IDS,
    PUNCTUATION_POLICY_VERSION,
    classify_reference_state,
    eligible_actions,
    gate_95,
    independent_nonkeep_families,
    interval,
    score_all_actions,
    score_population_v4_1,
    validate_action_set,
    validate_measurement_identity_contract,
)

VERSION = "MPSEF_RJOINT_V4_1_SOURCE_FREE_SYNTHETIC_PREFLIGHT_V1"


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def prov(key):
    if key == "P1":
        return {
            "proposer_id": PROPOSER_IDS["P1"],
            "proposer_version": "P1_FROZEN_V1",
            "family_id": FAMILY_IDS["SWEET"],
            "ancestry_id": "SWEET_NOPNX_ITER2",
        }
    if key == "P2":
        return {
            "proposer_id": PROPOSER_IDS["P2"],
            "proposer_version": "P2_V2_1",
            "family_id": FAMILY_IDS["SEQ2SEQ"],
            "ancestry_id": "P2",
        }
    if key == "P3":
        return {
            "proposer_id": PROPOSER_IDS["P3"],
            "proposer_version": "P3_V1_1",
            "family_id": FAMILY_IDS["SWEET"],
            "ancestry_id": "P3",
        }
    raise KeyError(key)


def action(aid, output, keys=(), keep=False):
    return {
        "action_id": aid,
        "output": output,
        "output_sha256": sha(output),
        "keep_semantics": keep,
        "provenance": (
            [{
                "proposer_id": "KEEP",
                "proposer_version": "SYSTEM",
                "family_id": "KEEP",
                "ancestry_id": "KEEP",
            }]
            if keep else [prov(k) for k in keys]
        ),
        "family_ids": sorted({prov(k)["family_id"] for k in keys}),
    }


def aset(source, actions, uid="SYNTH:1", cluster="C1", source_sha=None):
    return {
        "record_id": "SYNTH_ACTION_SET",
        "uid": uid,
        "case_id": uid,
        "cluster_id": cluster,
        "source_sha256": source_sha or sha(source),
        "unique_action_count": len(actions),
        "actions": actions,
    }


def fake_eval(score_map, failures=()):
    failures = set(failures)

    def fn(output, source, gold):
        if output in failures:
            raise RuntimeError("SYNTHETIC_SCORING_FAILURE")
        matched, proposed = score_map.get(output, ([], 0))
        return {
            "matched_indices": list(matched),
            "correct": len(matched),
            "proposed": proposed,
            "gold": len(gold),
            "extra": proposed - len(matched),
        }

    return fn


def source_row(uid, source, cluster="C1"):
    return {
        "uid": uid,
        "case_id": uid,
        "cluster_id": cluster,
        "source": source,
        "source_sha256": sha(source),
    }


def check(name, fn, results):
    try:
        fn()
        results.append({"name": name, "status": "PASS"})
    except Exception as exc:
        results.append({
            "name": name,
            "status": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
        })


def base_objects():
    source = "انا احب العلم"
    keep = action("K", source, keep=True)
    p1 = action("A1", "أنا احب العلم", ("P1",))
    p2 = action("A2", "انا أحب العلم", ("P2",))
    p3 = action("A3", "أنا أحب العلم", ("P3",))
    return source, keep, p1, p2, p3


def main():
    source, keep, p1, p2, p3 = base_objects()
    results = []

    check("T01_KEEP_ONLY", lambda: (
        validate_action_set(aset(source, [keep]))
    ), results)

    check("T02_KEEP_PLUS_P1", lambda: (
        None if len(eligible_actions(aset(source, [keep, p1]), "P1")) == 2
        and len(eligible_actions(aset(source, [keep, p1]), "P2")) == 1
        else (_ for _ in ()).throw(AssertionError("group leakage"))
    ), results)

    check("T03_KEEP_PLUS_P2", lambda: (
        None if len(eligible_actions(aset(source, [keep, p2]), "P2")) == 2
        and len(eligible_actions(aset(source, [keep, p2]), "SEQ2SEQ")) == 2
        else (_ for _ in ()).throw(AssertionError("P2 grouping"))
    ), results)

    check("T04_KEEP_PLUS_P3", lambda: (
        None if len(eligible_actions(aset(source, [keep, p3]), "P3")) == 2
        and len(eligible_actions(aset(source, [keep, p3]), "SWEET")) == 2
        else (_ for _ in ()).throw(AssertionError("P3 grouping"))
    ), results)

    check("T05_FULL_FOUR_ACTION_SET", lambda: (
        None if len(eligible_actions(aset(source, [keep, p1, p2, p3]), "ROSTER")) == 4
        else (_ for _ in ()).throw(AssertionError("four actions"))
    ), results)

    dup = action("ADUP", "أنا احب العلم", ("P1", "P3"))
    check("T06_P1_P3_LITERAL_DEDUP_PROVENANCE", lambda: (
        None if len(dup["provenance"]) == 2
        and len(eligible_actions(aset(source, [keep, dup]), "P1")) == 2
        and len(eligible_actions(aset(source, [keep, dup]), "P3")) == 2
        else (_ for _ in ()).throw(AssertionError("dedup provenance"))
    ), results)

    check("T07_P1_P3_DIFFERENT_SAME_FAMILY", lambda: (
        None if independent_nonkeep_families(aset(source, [keep, p1, p3]))
        == {FAMILY_IDS["SWEET"]}
        else (_ for _ in ()).throw(AssertionError("same family"))
    ), results)

    cross = action("ACROSS", "أنا احب العلم", ("P1", "P2"))
    check("T08_CROSS_FAMILY_EXACT_AGREEMENT", lambda: (
        None if independent_nonkeep_families(aset(source, [keep, cross]))
        == {FAMILY_IDS["SWEET"], FAMILY_IDS["SEQ2SEQ"]}
        else (_ for _ in ()).throw(AssertionError("cross-family provenance"))
    ), results)

    def t09():
        a = aset(source, [keep, p1])
        scored = score_all_actions(
            a, source, [1, 2, 3],
            fake_eval({}, failures={source, p1["output"]}),
        )
        from mpsef_rjoint_score_v4_1 import group_results
        g = group_results(a, scored, [0, 1, 2], "P1")
        assert (g["lower"], g["upper"]) == (0, 3)
    check("T09_M04_ALL_ACTIONS_FAIL_INTERVAL", t09, results)

    def t10():
        a = aset(source, [keep, p1])
        scored = score_all_actions(
            a, source, [1, 2, 3],
            fake_eval({source: ([0], 1)}, failures={p1["output"]}),
        )
        from mpsef_rjoint_score_v4_1 import group_results
        g = group_results(a, scored, [0, 1, 2], "P1")
        assert (g["lower"], g["upper"]) == (1, 3)
    check("T10_M04_SUCCESS_PLUS_FAILURE_INTERVAL", t10, results)

    def t11():
        from mpsef_rjoint_score_v4_1 import best_subset_whole_action
        g = {
            "successful": [
                ({"action_id": "A"}, {"matched_indices": [0], "extra": 0}),
                ({"action_id": "B"}, {"matched_indices": [1], "extra": 0}),
            ],
            "failures": [],
        }
        assert best_subset_whole_action(g, [0, 1]) == (1, 1)
    check("T11_M05_BOUNDARY_WHOLE_ACTION_HELPER", t11, results)

    check("T12_P1_CANNOT_CONSUME_P2_EXCLUSIVE", lambda: (
        None if len(eligible_actions(aset(source, [keep, p2]), "P1")) == 1
        else (_ for _ in ()).throw(AssertionError("proposer leakage"))
    ), results)

    check("T13_SWEET_CAN_USE_P1_OR_P3", lambda: (
        None if len(eligible_actions(aset(source, [keep, p1, p3]), "SWEET")) == 3
        else (_ for _ in ()).throw(AssertionError("sweet family"))
    ), results)

    check("T14_P1_P3_ONE_INDEPENDENT_FAMILY", lambda: (
        None if len(independent_nonkeep_families(aset(source, [keep, p1, p3]))) == 1
        else (_ for _ in ()).throw(AssertionError("double family vote"))
    ), results)

    def t15():
        a = aset(source, [keep, p1, p2])
        scored = score_all_actions(
            a, source, [1, 2],
            fake_eval({
                source: ([], 0),
                p1["output"]: ([0], 1),
                p2["output"]: ([1], 1),
            }),
        )
        from mpsef_rjoint_score_v4_1 import group_results
        g = group_results(a, scored, [0, 1], "ROSTER")
        assert g["lower"] == 1
    check("T15_ROSTER_NO_SYNTHETIC_FUSION", t15, results)

    check("T16_ZERO_TARGET_SENTENCE", lambda: (
        None if interval([0, 0], 0)["exact"] is None
        else (_ for _ in ()).throw(AssertionError("zero target interval"))
    ), results)

    check("T17_ALL_REFERENCE_CLEAN_CLASS", lambda: (
        None if classify_reference_state(0, 0) == "ALL_REFERENCE_CLEAN"
        else (_ for _ in ()).throw(AssertionError())
    ), results)

    check("T18_PUNCTUATION_SEPARATION_CLASS", lambda: (
        None if classify_reference_state(0, 2) == "PUNCTUATION_ONLY_REFERENCE"
        and classify_reference_state(1, 1) == "PRIMARY_ERROR_PRESENT"
        else (_ for _ in ()).throw(AssertionError())
    ), results)

    def t19():
        a = aset(source, [keep, p1])
        scored = score_all_actions(
            a, source, [1],
            fake_eval({source: ([], 0)}, failures={p1["output"]}),
        )
        assert "error" in scored["A1"]
    check("T19_SCORING_ERROR_EVIDENCE_PRESERVED", t19, results)

    def t20():
        bad = aset(source, [keep], source_sha="BAD")
        try:
            validate_action_set(bad, sha(source))
        except RuntimeError as exc:
            assert "ACTION_SOURCE_IDENTITY_MISMATCH" in str(exc)
            return
        raise AssertionError("identity mismatch did not fail closed")
    check("T20_ACTION_IDENTITY_FAIL_CLOSED", t20, results)

    def t21():
        uid = "PUNCT_PRIMARY"
        src = "خطا"
        k = action("K21", src, keep=True)
        both = action("B21", "خطأ.", ("P1",))
        rows = [source_row(uid, src)]
        sets = [aset(src, [k, both], uid=uid)]
        gold = {
            uid: [
                (0, 1, "خطا", ["خطأ"]),
                (1, 1, "", ["."]),
            ]
        }
        out = score_population_v4_1(
            None, rows, sets, gold,
            evaluate_fn=fake_eval({
                src: ([], 0),
                both["output"]: ([0, 1], 2),
            }),
        )
        p = out["PRIMARY_CLEAN_RECOVERY"]["P1"]
        assert p["lower_numerator"] == 1
        assert out["PUNCTUATION_RECOVERY"]["P1"]["lower_numerator"] == 1
    check("T21_SUPPORTED_PUNCT_NOT_EXTRA", t21, results)

    def t22():
        uid = "PUNCT_ONLY"
        src = "نص"
        k = action("K22", src, keep=True)
        punct = action("P22", "نص.", ("P1",))
        out = score_population_v4_1(
            None,
            [source_row(uid, src)],
            [aset(src, [k, punct], uid=uid)],
            {uid: [(1, 1, "", ["."])]},
            evaluate_fn=fake_eval({
                src: ([], 0),
                punct["output"]: ([0], 1),
            }),
        )
        assert out["primary_target_denominator"] == 0
        assert out["punctuation_target_denominator"] == 1
        assert out["PUNCTUATION_RECOVERY"]["P1"]["lower_numerator"] == 1
    check("T22_PUNCTUATION_RECOVERY_SEPARATE", t22, results)

    def t23():
        assert classify_reference_state(0, 0) == "ALL_REFERENCE_CLEAN"
        assert classify_reference_state(0, 1) == "PUNCTUATION_ONLY_REFERENCE"
        assert classify_reference_state(1, 0) == "PRIMARY_ERROR_PRESENT"
    check("T23_REFERENCE_STATE_PARTITION", t23, results)

    def t24():
        uid = "BOUNDARY"
        src = "ab cd"
        k = action("K24", src, keep=True)
        split = action("S24", "a b cd", ("P1",))
        merge = action("M24", "ab c d", ("P3",))
        rows = [source_row(uid, src)]
        sets = [aset(src, [k, split, merge], uid=uid)]
        gold = {
            uid: [
                (0, 1, "ab", ["a b"]),
                (1, 2, "cd", ["c d"]),
            ]
        }
        out = score_population_v4_1(
            None, rows, sets, gold,
            evaluate_fn=fake_eval({
                src: ([], 0),
                split["output"]: ([0], 1),
                merge["output"]: ([1], 1),
            }),
        )
        route = out["WEAK_ROUTE_FAMILY_EVIDENCE"]["BOUNDARY_ROUTE"]
        assert route["SWEET"]["lower_numerator"] == 1
        assert route["ROSTER"]["lower_numerator"] == 1
        assert route["target_denominator"] == 2
    check("T24_BOUNDARY_POPULATION_ONE_WHOLE_ACTION", t24, results)

    def t25():
        rows, sets, gold = [], [], {}
        for i in range(2):
            uid = f"ADD:{i}"
            src = f"ab{i}"
            k = action(f"K25{i}", src, keep=True)
            sweet = action(f"S25{i}", f"a b{i}", ("P1",))
            seq = action(f"Q25{i}", f"ab{i}", ("P2",))
            rows.append(source_row(uid, src, cluster=f"C{i}"))
            sets.append(aset(src, [k, sweet, seq], uid=uid, cluster=f"C{i}"))
            gold[uid] = [(0, 1, src, [f"a b{i}"])]
        score_map = {}
        for s in sets:
            for a in s["actions"]:
                if any(p.get("family_id") == FAMILY_IDS["SWEET"] for p in a["provenance"]):
                    score_map[a["output"]] = ([0], 1)
                else:
                    score_map[a["output"]] = ([], 0)
        out = score_population_v4_1(
            None, rows, sets, gold,
            evaluate_fn=fake_eval(score_map),
        )
        route = out["WEAK_ROUTE_FAMILY_EVIDENCE"]["BOUNDARY_ROUTE"]
        assert route["SWEET_additional_targets_lower"] == 2
        assert route["SWEET_additional_clusters_lower"] == 2
    check("T25_M05_ADDITIONAL_TARGET_CLUSTER_EVIDENCE", t25, results)

    def t26():
        assert gate_95(interval([19, 19], 20)) == "PASS_CANDIDATE_AVAILABILITY"
        assert gate_95(interval([18, 18], 20)) == "FAIL_CANDIDATE_AVAILABILITY"
        assert gate_95(interval([18, 19], 20)) == "INCONCLUSIVE_INTERVAL_CROSSES_GATE"
    check("T26_ROSTER_95_GATE_INTEGER_SEMANTICS", t26, results)

    def t27():
        keys = {
            "source_manifest_sha256": "A",
            "action_set_sha256": "B",
            "scorer_sha256": "C",
            "core_sha256": "D",
            "matching_version": "E",
            "family_map_version": "F",
            "punctuation_policy_version": PUNCTUATION_POLICY_VERSION,
            "population_uid_sha256": "G",
            "gold_sha256": "H",
            "python_version": "3.10",
            "dependency_lock_sha256": "I",
            "result_schema_version": "J",
        }
        actual = dict(keys)
        expected = dict(keys)
        validate_measurement_identity_contract(actual, expected)
        actual["gold_sha256"] = "WRONG"
        try:
            validate_measurement_identity_contract(actual, expected)
        except RuntimeError as exc:
            assert "IDENTITY_MISMATCH:gold_sha256" in str(exc)
            return
        raise AssertionError("identity mismatch accepted")
    check("T27_PRODUCTION_IDENTITY_CONTRACT_FAIL_CLOSED", t27, results)

    passed = sum(r["status"] == "PASS" for r in results)
    summary = {
        "record_id": VERSION,
        "status": "PASS" if passed == 27 else "FAIL",
        "test_count": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "source_free": True,
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "real_r_joint_computed": False,
        "selector_trained": False,
        "family_consensus_activated": False,
        "tests": results,
    }
    Path("MPSEF_RJOINT_V4_1_SYNTHETIC_PREFLIGHT_V1.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
