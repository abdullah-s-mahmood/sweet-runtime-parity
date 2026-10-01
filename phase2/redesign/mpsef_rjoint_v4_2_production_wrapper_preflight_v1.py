#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from mpsef_rjoint_core_v2 import FAMILY_MAP_VERSION, MATCHING_VERSION
from mpsef_rjoint_score_v4_2 import (
    PUNCTUATION_POLICY_VERSION,
    RESULT_SCHEMA_VERSION,
)
from mpsef_cf_gold_projection_v2 import EXPECTED_CAL_UID_SHA, VERSION as GOLD_PROJECTION_VERSION
from mpsef_rjoint_v4_2_production_wrapper_v1 import (
    AUTH_RECORD_ID,
    EXPERIMENT_ID,
    PROVENANCE_SIGNATURES,
    canonical_list_digest,
    provenance_signature_digest,
    require_authorization,
    sha256_file,
    sha_text,
    uid_cluster_map_digest,
    validate_population,
    validate_pre_gold_inputs,
)

VERSION = "MPSEF_RJOINT_V4_2_PRODUCTION_WRAPPER_PREFLIGHT_V1"


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


def expect_error(fn, token):
    try:
        fn()
    except RuntimeError as exc:
        assert token in str(exc), (token, str(exc))
        return
    raise AssertionError(f"expected failure containing {token}")


def source_row(uid, cluster, text):
    return {
        "uid": uid,
        "case_id": f"CASE-{uid}",
        "cluster_id": cluster,
        "role": "C_F",
        "source": text,
        "source_sha256": sha_text(text),
    }


def action_set(row, proposer="P1_CONTROL_SWEET_QALB14_NOPNX_ITER2"):
    source = row["source"]
    keep = {
        "action_id": f"K-{row['uid']}",
        "output": source,
        "output_sha256": sha_text(source),
        "keep_semantics": True,
        "provenance": [{
            "proposer_id": "KEEP",
            "proposer_version": "SYSTEM",
            "family_id": "KEEP",
            "ancestry_id": "KEEP",
        }],
        "family_ids": [],
    }
    actions = [keep]
    if proposer:
        sig = PROVENANCE_SIGNATURES[proposer]
        out = source + " x"
        actions.append({
            "action_id": f"A-{row['uid']}",
            "output": out,
            "output_sha256": sha_text(out),
            "keep_semantics": False,
            "provenance": [{
                "proposer_id": proposer,
                "proposer_version": sig["proposer_version"],
                "family_id": sig["family_id"],
                "ancestry_id": sig["ancestry_id"],
            }],
            "family_ids": [sig["family_id"]],
        })
    return {
        "record_id": "SYNTH_ACTION_SET",
        "uid": row["uid"],
        "case_id": row["case_id"],
        "cluster_id": row["cluster_id"],
        "source_sha256": row["source_sha256"],
        "unique_action_count": len(actions),
        "actions": actions,
    }


def tiny_lock(rows):
    uids = [r["uid"] for r in rows]
    clusters = sorted({r["cluster_id"] for r in rows})
    return {
        "population_cases": len(rows),
        "population_clusters": len(clusters),
        "population_uid_sha256": canonical_list_digest(uids),
        "population_cluster_sha256": canonical_list_digest(clusters),
        "uid_cluster_map_sha256": uid_cluster_map_digest(rows),
        "provenance_signature_map_sha256": provenance_signature_digest(),
    }


def write_jsonl(path, rows):
    Path(path).write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n",
        encoding="utf-8",
    )


def main():
    results = []
    rows = [source_row("u1", "c1", "نص"), source_row("u2", "c2", "علم")]
    sets = [action_set(r) for r in rows]
    lock = tiny_lock(rows)

    check("W01_PROVENANCE_SIGNATURE_DIGEST_FROZEN", lambda: (
        None if provenance_signature_digest()
        == "18561c75c397821c34e3dc06214bb4f64cc5ff8d6757f61835cbe9e6808befbd"
        else (_ for _ in ()).throw(AssertionError("signature digest drift"))
    ), results)

    check("W02_VALID_POPULATION_ACCEPTED", lambda: validate_population(rows, sets, lock), results)

    bad_count = dict(lock)
    bad_count["population_cases"] = 3
    check("W03_CASE_COUNT_MISMATCH_REJECTED", lambda: expect_error(
        lambda: validate_population(rows, sets, bad_count),
        "POPULATION_CASE_COUNT_MISMATCH",
    ), results)

    bad_cluster = dict(lock)
    bad_cluster["population_clusters"] = 1
    check("W04_CLUSTER_COUNT_MISMATCH_REJECTED", lambda: expect_error(
        lambda: validate_population(rows, sets, bad_cluster),
        "POPULATION_CLUSTER_COUNT_MISMATCH",
    ), results)

    bad_sets = json.loads(json.dumps(sets))
    bad_sets[0]["cluster_id"] = "wrong"
    check("W05_SOURCE_ACTION_IDENTITY_REJECTED", lambda: expect_error(
        lambda: validate_population(rows, bad_sets, lock),
        "ACTION_CLUSTER_ID_MISMATCH",
    ), results)

    bad_prov = json.loads(json.dumps(sets))
    bad_prov[0]["actions"][1]["provenance"][0]["family_id"] = "SEQ2SEQ_GED_MORPH"
    bad_prov[0]["actions"][1]["family_ids"] = ["SEQ2SEQ_GED_MORPH"]
    check("W06_PROPOSER_FAMILY_BINDING_REJECTED", lambda: expect_error(
        lambda: validate_population(rows, bad_prov, lock),
        "PROVENANCE_BINDING_MISMATCH",
    ), results)

    bad_source = json.loads(json.dumps(rows))
    bad_source[0]["source"] = "tampered"
    check("W07_SOURCE_TEXT_SHA_REJECTED", lambda: expect_error(
        lambda: validate_population(bad_source, sets, lock),
        "SOURCE_TEXT_SHA_MISMATCH",
    ), results)

    bad_uid_lock = dict(lock)
    bad_uid_lock["population_uid_sha256"] = "bad"
    check("W08_UID_DIGEST_REJECTED", lambda: expect_error(
        lambda: validate_population(rows, sets, bad_uid_lock),
        "POPULATION_UID_SHA_MISMATCH",
    ), results)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        lockp = td / "lock.json"
        lockp.write_text(json.dumps({"safe": True}) + "\n", encoding="utf-8")
        auth = {
            "record_id": AUTH_RECORD_ID,
            "experiment_id": EXPERIMENT_ID,
            "decision": "AUTHORIZE_DEVELOPMENT_ONLY_RJOINT_V4_2_SINGLE_RUN",
            "measurement_authorized": True,
            "gold_access_allowed_after_claim": True,
            "consumption_claimed_before_gold_access": True,
            "single_run_only": True,
            "input_lock_sha256": sha256_file(lockp),
        }
        authp = td / "auth.json"
        authp.write_text(json.dumps(auth) + "\n", encoding="utf-8")
        check("W09_AUTHORIZATION_LOCK_BINDING_ACCEPTED", lambda: require_authorization(authp, lockp), results)

        denied = dict(auth)
        denied["measurement_authorized"] = False
        deniedp = td / "denied.json"
        deniedp.write_text(json.dumps(denied) + "\n", encoding="utf-8")
        check("W10_UNAUTHORIZED_GOLD_GATE_REJECTED", lambda: expect_error(
            lambda: require_authorization(deniedp, lockp),
            "MEASUREMENT_NOT_AUTHORIZED",
        ), results)

        wrong = dict(auth)
        wrong["input_lock_sha256"] = "wrong"
        wrongp = td / "wrong.json"
        wrongp.write_text(json.dumps(wrong) + "\n", encoding="utf-8")
        check("W11_AUTH_INPUT_LOCK_MISMATCH_REJECTED", lambda: expect_error(
            lambda: require_authorization(wrongp, lockp),
            "AUTH_INPUT_LOCK_SHA_MISMATCH",
        ), results)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        sourcep = td / "source.jsonl"
        actionp = td / "actions.jsonl"
        dep = td / "dep.txt"
        write_jsonl(sourcep, rows)
        write_jsonl(actionp, sets)
        dep.write_text("locked\n", encoding="utf-8")

        upstream = td / "upstream"
        upstream.mkdir()
        subprocess.check_call(["git", "-C", str(upstream), "init", "-q"])
        subprocess.check_call(["git", "-C", str(upstream), "config", "user.email", "preflight@example.invalid"])
        subprocess.check_call(["git", "-C", str(upstream), "config", "user.name", "preflight"])
        (upstream / "README").write_text("x\n", encoding="utf-8")
        subprocess.check_call(["git", "-C", str(upstream), "add", "README"])
        subprocess.check_call(["git", "-C", str(upstream), "commit", "-q", "-m", "fixture"])
        rev = subprocess.check_output(
            ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True
        ).strip()

        numpy_version = importlib.metadata.version("numpy")
        editdistance_version = importlib.metadata.version("editdistance")

        def write_dep(path, numpy_value=None, network_policy="forbidden"):
            numpy_value = numpy_version if numpy_value is None else numpy_value
            Path(path).write_text(
                "\n".join([
                    "MPSEF_RJOINT_V4_2_DEPENDENCY_LOCK_SYNTH",
                    f"python_major_minor={sys.version_info.major}.{sys.version_info.minor}",
                    f"arabic_gec_revision={rev}",
                    f"numpy={numpy_value}",
                    f"editdistance={editdistance_version}",
                    f"network_download_during_measurement={network_policy}",
                    "model_inference_during_measurement=forbidden",
                ]) + "\n",
                encoding="utf-8",
            )

        write_dep(dep)

        here = Path(__file__).resolve().parent
        wrapperp = here / "mpsef_rjoint_v4_2_production_wrapper_v1.py"
        scorerp = here / "mpsef_rjoint_score_v4_2.py"
        corep = here / "mpsef_rjoint_core_v2.py"
        full_lock = {
            **lock,
            "source_manifest_sha256": sha256_file(sourcep),
            "action_set_sha256": sha256_file(actionp),
            "dependency_lock_sha256": sha256_file(dep),
            "scorer_sha256": sha256_file(scorerp),
            "core_sha256": sha256_file(corep),
            "wrapper_sha256": sha256_file(wrapperp),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
            "arabic_gec_revision": rev,
            "matching_version": MATCHING_VERSION,
            "family_map_version": FAMILY_MAP_VERSION,
            "punctuation_policy_version": PUNCTUATION_POLICY_VERSION,
            "result_schema_version": RESULT_SCHEMA_VERSION,
            "gold_projection_version": GOLD_PROJECTION_VERSION,
            "calibration_uid_sha256": EXPECTED_CAL_UID_SHA,
        }

        check("W12_FULL_PRE_GOLD_IDENTITY_ACCEPTED", lambda: validate_pre_gold_inputs(
            input_lock=full_lock,
            source_manifest=sourcep,
            action_sets=actionp,
            dependency_lock=dep,
            scorer_path=scorerp,
            core_path=corep,
            wrapper_path=wrapperp,
            upstream_root=upstream,
        ), results)

        bad = dict(full_lock)
        bad["scorer_sha256"] = "wrong"
        check("W13_SCORER_SHA_MISMATCH_REJECTED", lambda: expect_error(
            lambda: validate_pre_gold_inputs(
                input_lock=bad,
                source_manifest=sourcep,
                action_sets=actionp,
                dependency_lock=dep,
                scorer_path=scorerp,
                core_path=corep,
                wrapper_path=wrapperp,
                upstream_root=upstream,
            ),
            "PRE_GOLD_IDENTITY_MISMATCH:scorer_sha256",
        ), results)

        bad = dict(full_lock)
        bad["provenance_signature_map_sha256"] = "wrong"
        check("W14_PROVENANCE_MAP_LOCK_MISMATCH_REJECTED", lambda: expect_error(
            lambda: validate_pre_gold_inputs(
                input_lock=bad,
                source_manifest=sourcep,
                action_sets=actionp,
                dependency_lock=dep,
                scorer_path=scorerp,
                core_path=corep,
                wrapper_path=wrapperp,
                upstream_root=upstream,
            ),
            "PROVENANCE_SIGNATURE_MAP_SHA_MISMATCH",
        ), results)

        bad_dep_version = td / "dep_bad_version.txt"
        write_dep(bad_dep_version, numpy_value="0.0.0")
        bad = dict(full_lock)
        bad["dependency_lock_sha256"] = sha256_file(bad_dep_version)
        check("W15_RUNTIME_PACKAGE_VERSION_MISMATCH_REJECTED", lambda: expect_error(
            lambda: validate_pre_gold_inputs(
                input_lock=bad,
                source_manifest=sourcep,
                action_sets=actionp,
                dependency_lock=bad_dep_version,
                scorer_path=scorerp,
                core_path=corep,
                wrapper_path=wrapperp,
                upstream_root=upstream,
            ),
            "DEPENDENCY_VERSION_MISMATCH:numpy",
        ), results)

        bad_dep_policy = td / "dep_bad_policy.txt"
        write_dep(bad_dep_policy, network_policy="allowed")
        bad = dict(full_lock)
        bad["dependency_lock_sha256"] = sha256_file(bad_dep_policy)
        check("W16_RUNTIME_POLICY_MISMATCH_REJECTED", lambda: expect_error(
            lambda: validate_pre_gold_inputs(
                input_lock=bad,
                source_manifest=sourcep,
                action_sets=actionp,
                dependency_lock=bad_dep_policy,
                scorer_path=scorerp,
                core_path=corep,
                wrapper_path=wrapperp,
                upstream_root=upstream,
            ),
            "DEPENDENCY_POLICY_MISMATCH:network_download",
        ), results)


    passed = sum(x["status"] == "PASS" for x in results)
    summary = {
        "record_id": VERSION,
        "status": "PASS" if passed == 16 else "FAIL",
        "test_count": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "source_free": True,
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "real_r_joint_computed": False,
        "tests": results,
    }
    out = Path("MPSEF_RJOINT_V4_2_PRODUCTION_WRAPPER_PREFLIGHT_V1.json")
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
