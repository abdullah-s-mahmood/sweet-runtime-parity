#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mpsef_rjoint_score_v4 import (
    FAMILY_IDS,
    PROPOSER_IDS,
    best_target_subset_bounds,
    eligible_actions,
    evaluate_sentence_v4,
    freeze_primary_targets,
    independent_nonkeep_families,
    score_population_source_free,
    whole_action_additional_target_bounds,
)

VERSION = "MPSEF_RJOINT_V4_SOURCE_FREE_SYNTHETIC_PREFLIGHT_V1"


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def prov(key):
    if key == "P1":
        return {"proposer_id": PROPOSER_IDS["P1"], "proposer_version": "P1_FROZEN_V1", "family_id": FAMILY_IDS["SWEET"], "ancestry_id": "SWEET_NOPNX_ITER2"}
    if key == "P2":
        return {"proposer_id": PROPOSER_IDS["P2"], "proposer_version": "P2_V2_1", "family_id": FAMILY_IDS["SEQ2SEQ"], "ancestry_id": "P2"}
    if key == "P3":
        return {"proposer_id": PROPOSER_IDS["P3"], "proposer_version": "P3_V1_1", "family_id": FAMILY_IDS["SWEET"], "ancestry_id": "P3"}
    raise KeyError(key)


def action(aid, output, keys=(), keep=False):
    return {
        "action_id": aid,
        "output": output,
        "output_sha256": sha(output),
        "keep_semantics": keep,
        "provenance": ([{"proposer_id": "KEEP", "proposer_version": "SYSTEM", "family_id": "KEEP", "ancestry_id": "KEEP"}] if keep else [prov(k) for k in keys]),
        "family_ids": sorted({prov(k)["family_id"] for k in keys}),
    }


def aset(source, actions, uid="SYNTH:1", source_sha=None):
    return {
        "record_id": "SYNTH_ACTION_SET",
        "uid": uid,
        "case_id": uid,
        "cluster_id": "C1",
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


def target(tid, scope="LINGUISTIC"):
    return {"target_id": tid, "scope": scope, "family": "SUBSTITUTE"}


def check(name, fn, results):
    try:
        fn()
        results.append({"name": name, "status": "PASS"})
    except Exception as exc:
        results.append({"name": name, "status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})


def main():
    source = "انا احب العلم"
    keep = action("K", source, keep=True)
    p1 = action("A1", "أنا احب العلم", ("P1",))
    p2 = action("A2", "انا أحب العلم", ("P2",))
    p3 = action("A3", "أنا أحب العلم", ("P3",))
    results = []

    check("T01_KEEP_ONLY", lambda: (
        (lambda ev: (_ for _ in ()).throw(AssertionError()) if any(ev["groups"][g]["lower"] != 0 for g in ev["groups"]) else None)(
            evaluate_sentence_v4(aset(source, [keep]), source, [0], fake_eval({source: ([], 0)}))
        )
    ), results)

    check("T02_KEEP_PLUS_P1", lambda: (
        (lambda ev: (
            None if ev["groups"]["P1"]["lower"] == 1 and ev["groups"]["SWEET"]["lower"] == 1 and ev["groups"]["P2"]["lower"] == 0 else (_ for _ in ()).throw(AssertionError("group leakage"))
        ))(evaluate_sentence_v4(aset(source, [keep, p1]), source, [0], fake_eval({source: ([],0), p1["output"]: ([0],1)})))
    ), results)

    check("T03_KEEP_PLUS_P2", lambda: (
        (lambda ev: None if ev["groups"]["P2"]["lower"] == 1 and ev["groups"]["SEQ2SEQ"]["lower"] == 1 and ev["groups"]["P1"]["lower"] == 0 else (_ for _ in ()).throw(AssertionError("P2 grouping")))(
            evaluate_sentence_v4(aset(source, [keep, p2]), source, [0], fake_eval({source:([],0), p2["output"]:([0],1)}))
        )
    ), results)

    check("T04_KEEP_PLUS_P3", lambda: (
        (lambda ev: None if ev["groups"]["P3"]["lower"] == 1 and ev["groups"]["SWEET"]["lower"] == 1 and ev["groups"]["P1"]["lower"] == 0 else (_ for _ in ()).throw(AssertionError("P3 grouping")))(
            evaluate_sentence_v4(aset(source, [keep, p3]), source, [0], fake_eval({source:([],0), p3["output"]:([0],1)}))
        )
    ), results)

    check("T05_FULL_FOUR_ACTION_SET", lambda: (
        (lambda ev: None if ev["groups"]["ROSTER"]["lower"] == 2 and len(eligible_actions(aset(source,[keep,p1,p2,p3]), "ROSTER")) == 4 else (_ for _ in ()).throw(AssertionError("four actions")))(
            evaluate_sentence_v4(aset(source,[keep,p1,p2,p3]), source, [0,1], fake_eval({source:([],0),p1["output"]:([0],1),p2["output"]:([1],1),p3["output"]:([0,1],2)}))
        )
    ), results)

    dup = action("ADUP", "أنا احب العلم", ("P1","P3"))
    check("T06_P1_P3_LITERAL_DEDUP_PROVENANCE", lambda: (
        None if len(dup["provenance"]) == 2 and len(eligible_actions(aset(source,[keep,dup]),"P1")) == 2 and len(eligible_actions(aset(source,[keep,dup]),"P3")) == 2 else (_ for _ in ()).throw(AssertionError("dedup provenance"))
    ), results)

    check("T07_P1_P3_DIFFERENT_SAME_FAMILY", lambda: (
        None if independent_nonkeep_families(aset(source,[keep,p1,p3])) == {FAMILY_IDS["SWEET"]} and len(eligible_actions(aset(source,[keep,p1,p3]),"SWEET")) == 3 else (_ for _ in ()).throw(AssertionError("same family"))
    ), results)

    cross = action("ACROSS", "أنا احب العلم", ("P1","P2"))
    check("T08_CROSS_FAMILY_EXACT_AGREEMENT", lambda: (
        None if independent_nonkeep_families(aset(source,[keep,cross])) == {FAMILY_IDS["SWEET"],FAMILY_IDS["SEQ2SEQ"]} and len(eligible_actions(aset(source,[keep,cross]),"SWEET")) == 2 and len(eligible_actions(aset(source,[keep,cross]),"SEQ2SEQ")) == 2 else (_ for _ in ()).throw(AssertionError("cross family"))
    ), results)

    check("T09_M04_ALL_ACTIONS_FAIL_INTERVAL", lambda: (
        (lambda ev: None if ev["groups"]["P1"]["lower"] == 0 and ev["groups"]["P1"]["upper"] == 3 else (_ for _ in ()).throw(AssertionError("M04")))(
            evaluate_sentence_v4(aset(source,[keep,p1]), source, [0,1,2], fake_eval({}, failures={source,p1["output"]}))
        )
    ), results)

    check("T10_M04_SUCCESS_PLUS_FAILURE_INTERVAL", lambda: (
        (lambda ev: None if ev["groups"]["P1"]["lower"] == 1 and ev["groups"]["P1"]["upper"] == 3 else (_ for _ in ()).throw(AssertionError("conservative interval")))(
            evaluate_sentence_v4(aset(source,[keep,p1]), source, [0,1,2], fake_eval({source:([0],1)}, failures={p1["output"]}))
        )
    ), results)

    def t11():
        a = action("SPLIT_A","x",("P1",)); b = action("MERGE_B","y",("P1",))
        g = {"successful":[(a,{"matched_indices":[0],"correct":1,"proposed":1,"gold":2,"extra":0}),(b,{"matched_indices":[1],"correct":1,"proposed":1,"gold":2,"extra":0})],"failures":[]}
        lo,hi = best_target_subset_bounds(g,[0,1])
        assert (lo,hi)==(1,1), (lo,hi)
        other = {"successful":[],"failures":[]}
        alo,ahi = whole_action_additional_target_bounds(g,other,[0,1])
        assert len(alo)==1 and len(ahi)==1
    check("T11_M05_BOUNDARY_WHOLE_ACTION", t11, results)

    check("T12_P1_CANNOT_CONSUME_P2_EXCLUSIVE", lambda: (
        (lambda ev: None if ev["groups"]["P1"]["lower"] == 0 and ev["groups"]["P2"]["lower"] == 2 else (_ for _ in ()).throw(AssertionError("proposer leakage")))(
            evaluate_sentence_v4(aset(source,[keep,p2]), source, [0,1], fake_eval({source:([],0),p2["output"]:([0,1],2)}))
        )
    ), results)

    check("T13_SWEET_CAN_USE_P1_OR_P3", lambda: (
        (lambda ev: None if ev["groups"]["SWEET"]["lower"] == 2 and ev["groups"]["P1"]["lower"] == 1 and ev["groups"]["P3"]["lower"] == 2 else (_ for _ in ()).throw(AssertionError("sweet family")))(
            evaluate_sentence_v4(aset(source,[keep,p1,p3]), source, [0,1], fake_eval({source:([],0),p1["output"]:([0],1),p3["output"]:([0,1],2)}))
        )
    ), results)

    check("T14_P1_P3_ONE_INDEPENDENT_FAMILY", lambda: (
        None if len(independent_nonkeep_families(aset(source,[keep,p1,p3]))) == 1 else (_ for _ in ()).throw(AssertionError("double family vote"))
    ), results)

    check("T15_ROSTER_NO_SYNTHETIC_FUSION", lambda: (
        (lambda ev: None if ev["groups"]["ROSTER"]["lower"] == 1 else (_ for _ in ()).throw(AssertionError("synthetic fusion")))(
            evaluate_sentence_v4(aset(source,[keep,p1,p2]), source, [0,1], fake_eval({source:([],0),p1["output"]:([0],1),p2["output"]:([1],1)}))
        )
    ), results)

    check("T16_ZERO_TARGET_SENTENCE", lambda: (
        (lambda ev: None if all(ev["groups"][g]["lower"]==0 and ev["groups"][g]["upper"]==0 for g in ev["groups"]) else (_ for _ in ()).throw(AssertionError("zero target")))(
            evaluate_sentence_v4(aset(source,[keep,p1]), source, [], fake_eval({source:([],0),p1["output"]:([],1)}))
        )
    ), results)

    def t17():
        rec = {"uid":"CLEAN","cluster_id":"C","source":source,"source_sha256":sha(source),"action_set":aset(source,[keep,p1],uid="CLEAN"),"targets":[]}
        out = score_population_source_free([rec], fake_eval({source:([],0),p1["output"]:([],1)}))
        assert out["primary_target_count"]==0
        assert out["complete_repair_sentence_bounds"]["ROSTER"]["lower"]==0
        assert len(rec["action_set"]["actions"])==2
    check("T17_CLEAN_SENTENCE_UNNECESSARY_ACTIVITY", t17, results)

    def t18():
        primary,punc = freeze_primary_targets([target("L"),target("P","PUNCTUATION_ONLY")])
        assert len(primary)==1 and len(punc)==1 and primary[0]["target_id"]=="L"
    check("T18_PUNCTUATION_SEPARATION", t18, results)

    def t19():
        ev = evaluate_sentence_v4(aset(source,[keep,p1]), source, [0,1], fake_eval({source:([],0)}, failures={p1["output"]}))
        assert "error" in ev["scored"]["A1"]
        assert [a["action_id"] for a in ev["groups"]["P1"]["failures"]] == ["A1"]
    check("T19_SCORING_ERROR_EVIDENCE_PRESERVED", t19, results)

    def t20():
        rec = {"uid":"MISMATCH","cluster_id":"C","source":source,"source_sha256":sha(source),"action_set":aset(source,[keep],uid="MISMATCH",source_sha="BAD"),"targets":[target("L")]}
        try:
            score_population_source_free([rec], fake_eval({source:([],0)}))
        except RuntimeError as exc:
            assert "ACTION_SOURCE_IDENTITY_MISMATCH" in str(exc)
            return
        raise AssertionError("identity mismatch did not fail closed")
    check("T20_POPULATION_ACTION_IDENTITY_FAIL_CLOSED", t20, results)

    passed = sum(r["status"]=="PASS" for r in results)
    summary = {
        "record_id": VERSION,
        "status": "PASS" if passed == 20 else "FAIL",
        "test_count": len(results),
        "passed": passed,
        "failed": len(results)-passed,
        "source_free": True,
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "real_r_joint_computed": False,
        "selector_trained": False,
        "family_consensus_activated": False,
        "tests": results,
    }
    Path("MPSEF_RJOINT_V4_SYNTHETIC_PREFLIGHT_V1.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if summary["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
