#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import signal
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mpsef_rjoint_core_v2 import (
    FAMILY_MAP_VERSION,
    MATCHING_VERSION,
    evaluate_action_against_gold,
    import_m2,
)
from mpsef_rjoint_score_v4_2 import (
    PUNCTUATION_POLICY_VERSION,
    RESULT_SCHEMA_VERSION,
    score_population_v4_2,
    validate_action_set,
    validate_measurement_identity_contract,
)
from mpsef_cf_gold_projection_v2 import (
    EXPECTED_CAL_UID_SHA,
    VERSION as GOLD_PROJECTION_VERSION,
    project_loaded,
)
from process_progress_v1 import update_state

VERSION = "MPSEF_RJOINT_V4_2_PRODUCTION_WRAPPER_V1"
EXPERIMENT_ID = "MPSEF-RJOINT-V4_2-CF1918-20261002-A"
AUTH_RECORD_ID = "MPSEF_RJOINT_V4_2_SINGLE_RUN_AUTHORIZATION_V1"
ACTION_SCORING_TIMEOUT_SECONDS = 60

PROVENANCE_SIGNATURES = {
    "KEEP": {
        "proposer_version": "SYSTEM",
        "family_id": "KEEP",
        "ancestry_id": "KEEP",
    },
    "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2": {
        "proposer_version": "P1_FROZEN_V1",
        "family_id": "SWEET_QALB14",
        "ancestry_id": "SWEET_NOPNX_ITER2",
    },
    "P2_V2_ARABART_GED_MORPH_WORDALIGNED": {
        "proposer_version": "P2_V2_1",
        "family_id": "SEQ2SEQ_GED_MORPH",
        "ancestry_id": "ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR",
    },
    "P3_V1_SWEET_NOPNX2_PNX1": {
        "proposer_version": "P3_V1_1",
        "family_id": "SWEET_QALB14",
        "ancestry_id": "P1_CONTROL_PLUS_PNX1",
    },
}


def sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_jsonl(path):
    return [
        json.loads(x)
        for x in Path(path).read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def canonical_list_digest(values):
    return sha_text("\n".join(sorted(values)) + "\n")


def uid_cluster_map_digest(rows):
    pairs = sorted((r["uid"], r["cluster_id"]) for r in rows)
    return sha_text("\n".join(f"{u}\t{c}" for u, c in pairs) + "\n")


def provenance_signature_digest():
    return sha_text(json.dumps(
        PROVENANCE_SIGNATURES,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ))


def git_revision(root):
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
    ).strip()


def require_authorization(auth_path, input_lock_path):
    auth = read_json(auth_path)
    if auth.get("record_id") != AUTH_RECORD_ID:
        raise RuntimeError("AUTH_RECORD_ID_MISMATCH")
    if auth.get("experiment_id") != EXPERIMENT_ID:
        raise RuntimeError("AUTH_EXPERIMENT_ID_MISMATCH")
    if auth.get("decision") != "AUTHORIZE_DEVELOPMENT_ONLY_RJOINT_V4_2_SINGLE_RUN":
        raise RuntimeError("AUTH_DECISION_MISMATCH")
    if auth.get("measurement_authorized") is not True:
        raise RuntimeError("MEASUREMENT_NOT_AUTHORIZED")
    if auth.get("gold_access_allowed_after_claim") is not True:
        raise RuntimeError("GOLD_ACCESS_NOT_AUTHORIZED")
    if auth.get("consumption_claimed_before_gold_access") is not True:
        raise RuntimeError("CONSUMPTION_CLAIM_MISSING")
    if auth.get("single_run_only") is not True:
        raise RuntimeError("SINGLE_RUN_BOUNDARY_MISSING")
    if auth.get("input_lock_sha256") != sha256_file(input_lock_path):
        raise RuntimeError("AUTH_INPUT_LOCK_SHA_MISMATCH")
    return auth


def validate_population(source_rows, action_sets, lock):
    expected_cases = int(lock["population_cases"])
    expected_clusters = int(lock["population_clusters"])
    if len(source_rows) != expected_cases or len(action_sets) != expected_cases:
        raise RuntimeError("POPULATION_CASE_COUNT_MISMATCH")

    src = {}
    for row in source_rows:
        uid = row.get("uid")
        if not uid or uid in src:
            raise RuntimeError("SOURCE_UID_DUPLICATE_OR_MISSING")
        if row.get("role") != "C_F":
            raise RuntimeError(f"{uid}:SOURCE_ROLE_MISMATCH")
        if row.get("source_sha256") != sha_text(row.get("source", "")):
            raise RuntimeError(f"{uid}:SOURCE_TEXT_SHA_MISMATCH")
        src[uid] = row

    aset_by_uid = {}
    for row in action_sets:
        uid = row.get("uid")
        if not uid or uid in aset_by_uid:
            raise RuntimeError("ACTION_UID_DUPLICATE_OR_MISSING")
        aset_by_uid[uid] = row

    if set(src) != set(aset_by_uid):
        raise RuntimeError("SOURCE_ACTION_UID_SET_MISMATCH")

    clusters = {r["cluster_id"] for r in source_rows}
    if len(clusters) != expected_clusters:
        raise RuntimeError("POPULATION_CLUSTER_COUNT_MISMATCH")

    uid_sha = canonical_list_digest(src)
    cluster_sha = canonical_list_digest(clusters)
    pair_sha = uid_cluster_map_digest(source_rows)
    if uid_sha != lock["population_uid_sha256"]:
        raise RuntimeError("POPULATION_UID_SHA_MISMATCH")
    if cluster_sha != lock["population_cluster_sha256"]:
        raise RuntimeError("POPULATION_CLUSTER_SHA_MISMATCH")
    if pair_sha != lock["uid_cluster_map_sha256"]:
        raise RuntimeError("UID_CLUSTER_MAP_SHA_MISMATCH")
    if provenance_signature_digest() != lock["provenance_signature_map_sha256"]:
        raise RuntimeError("PROVENANCE_SIGNATURE_MAP_SHA_MISMATCH")

    for uid, row in aset_by_uid.items():
        s = src[uid]
        for key in ("case_id", "cluster_id", "source_sha256"):
            if row.get(key) != s.get(key):
                raise RuntimeError(f"{uid}:ACTION_{key.upper()}_MISMATCH")
        validate_action_set(row, s["source_sha256"])
        for action in row["actions"]:
            for p in action.get("provenance") or []:
                pid = p.get("proposer_id")
                if pid not in PROVENANCE_SIGNATURES:
                    raise RuntimeError(f"{uid}:UNKNOWN_PROPOSER:{pid}")
                exp = PROVENANCE_SIGNATURES[pid]
                for key in ("proposer_version", "family_id", "ancestry_id"):
                    if p.get(key) != exp[key]:
                        raise RuntimeError(
                            f"{uid}:PROVENANCE_BINDING_MISMATCH:{pid}:{key}"
                        )

    return {
        "cases": len(source_rows),
        "clusters": len(clusters),
        "population_uid_sha256": uid_sha,
        "population_cluster_sha256": cluster_sha,
        "uid_cluster_map_sha256": pair_sha,
        "provenance_signature_map_sha256": provenance_signature_digest(),
    }


def validate_pre_gold_inputs(
    *,
    input_lock,
    source_manifest,
    action_sets,
    dependency_lock,
    scorer_path,
    core_path,
    wrapper_path,
    upstream_root,
):
    checks = {
        "source_manifest_sha256": sha256_file(source_manifest),
        "action_set_sha256": sha256_file(action_sets),
        "dependency_lock_sha256": sha256_file(dependency_lock),
        "scorer_sha256": sha256_file(scorer_path),
        "core_sha256": sha256_file(core_path),
        "wrapper_sha256": sha256_file(wrapper_path),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "arabic_gec_revision": git_revision(upstream_root),
    }
    for key, actual in checks.items():
        expected = input_lock.get(key)
        if actual != expected:
            raise RuntimeError(f"PRE_GOLD_IDENTITY_MISMATCH:{key}")

    source_rows = read_jsonl(source_manifest)
    action_rows = read_jsonl(action_sets)
    pop = validate_population(source_rows, action_rows, input_lock)

    if MATCHING_VERSION != input_lock["matching_version"]:
        raise RuntimeError("MATCHING_VERSION_MISMATCH")
    if FAMILY_MAP_VERSION != input_lock["family_map_version"]:
        raise RuntimeError("FAMILY_MAP_VERSION_MISMATCH")
    if PUNCTUATION_POLICY_VERSION != input_lock["punctuation_policy_version"]:
        raise RuntimeError("PUNCTUATION_POLICY_VERSION_MISMATCH")
    if RESULT_SCHEMA_VERSION != input_lock["result_schema_version"]:
        raise RuntimeError("RESULT_SCHEMA_VERSION_MISMATCH")
    if GOLD_PROJECTION_VERSION != input_lock["gold_projection_version"]:
        raise RuntimeError("GOLD_PROJECTION_VERSION_MISMATCH")
    if EXPECTED_CAL_UID_SHA != input_lock["calibration_uid_sha256"]:
        raise RuntimeError("CALIBRATION_UID_LOCK_MISMATCH")

    return source_rows, action_rows, pop, checks


class ActionScoringTimeout(TimeoutError):
    pass


def _alarm_handler(signum, frame):
    raise ActionScoringTimeout(
        f"action scoring exceeded frozen {ACTION_SCORING_TIMEOUT_SECONDS}s limit"
    )


def make_timed_evaluator(lev):
    def evaluate(output, source, gold):
        old_handler = signal.getsignal(signal.SIGALRM)
        try:
            signal.signal(signal.SIGALRM, _alarm_handler)
            signal.setitimer(signal.ITIMER_REAL, ACTION_SCORING_TIMEOUT_SECONDS)
            return evaluate_action_against_gold(lev, output, source, gold)
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old_handler)
    return evaluate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--authorization", required=True)
    ap.add_argument("--input-lock", required=True)
    ap.add_argument("--dependency-lock", required=True)
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--action-sets", required=True)
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--full-gold-m2", required=True)
    ap.add_argument("--upstream-root", required=True)
    ap.add_argument(
        "--state-file",
        default="MPSEF_RJOINT_V4_2_PRODUCTION_PROGRESS.json",
    )
    ap.add_argument(
        "--out-prefix",
        default="MPSEF_RJOINT_V4_2_DEVELOPMENT_MEASUREMENT_V1",
    )
    args = ap.parse_args()

    wrapper_path = Path(__file__).resolve()
    root = wrapper_path.parent
    scorer_path = root / "mpsef_rjoint_score_v4_2.py"
    core_path = root / "mpsef_rjoint_core_v2.py"

    # Authorization is checked before any gold file is opened or hashed.
    auth = require_authorization(args.authorization, args.input_lock)
    lock = read_json(args.input_lock)
    if lock.get("status") != "FROZEN_READY_FOR_SINGLE_RUN_AUTHORIZATION":
        raise RuntimeError("INPUT_LOCK_NOT_READY")
    if lock.get("experiment_id") != EXPERIMENT_ID:
        raise RuntimeError("INPUT_LOCK_EXPERIMENT_MISMATCH")
    if auth.get("claim_scope") != lock.get("claim_scope"):
        raise RuntimeError("AUTH_CLAIM_SCOPE_MISMATCH")

    state_path = Path(args.state_file)
    update_state(
        state_path, VERSION, "VALIDATING_PRE_GOLD_IDENTITIES",
        0, int(lock["population_cases"]),
    )

    source_rows, action_rows, pop, checks = validate_pre_gold_inputs(
        input_lock=lock,
        source_manifest=args.source_manifest,
        action_sets=args.action_sets,
        dependency_lock=args.dependency_lock,
        scorer_path=scorer_path,
        core_path=core_path,
        wrapper_path=wrapper_path,
        upstream_root=args.upstream_root,
    )

    # Gold/reference bytes are touched only after authorization + all pre-gold
    # identities above have passed.
    gold_sha = sha256_file(args.full_gold_m2)
    if gold_sha != lock["gold_sha256"]:
        raise RuntimeError("GOLD_SHA_MISMATCH")

    calibration = read_jsonl(args.calibration)
    cal_uid_sha = sha_text("\n".join(r["uid"] for r in calibration) + "\n")
    if cal_uid_sha != lock["calibration_uid_sha256"]:
        raise RuntimeError("CALIBRATION_UID_SHA_MISMATCH")

    actual_identity = {
        "source_manifest_sha256": checks["source_manifest_sha256"],
        "action_set_sha256": checks["action_set_sha256"],
        "scorer_sha256": checks["scorer_sha256"],
        "core_sha256": checks["core_sha256"],
        "matching_version": MATCHING_VERSION,
        "family_map_version": FAMILY_MAP_VERSION,
        "punctuation_policy_version": PUNCTUATION_POLICY_VERSION,
        "population_uid_sha256": pop["population_uid_sha256"],
        "gold_sha256": gold_sha,
        "python_version": checks["python_version"],
        "dependency_lock_sha256": checks["dependency_lock_sha256"],
        "result_schema_version": RESULT_SCHEMA_VERSION,
    }
    expected_identity = {
        key: lock[key] for key in actual_identity
    }
    validate_measurement_identity_contract(actual_identity, expected_identity)

    update_state(
        state_path, VERSION, "AUTHORIZED_GOLD_PROJECTION",
        0, int(lock["population_cases"]),
        message="authorization and all input identities verified",
    )

    m2, lev = import_m2(args.upstream_root)
    full_sources, full_gold = m2.load_annotation(str(args.full_gold_m2))
    projected = project_loaded(
        calibration, source_rows, full_sources, full_gold
    )
    gold_by_uid = {row["uid"]: row["gold"] for row in projected}
    projection_bytes = (
        "\n".join(json.dumps(x, ensure_ascii=False) for x in projected) + "\n"
    ).encode("utf-8")
    projection_sha = hashlib.sha256(projection_bytes).hexdigest()

    timed_evaluate = make_timed_evaluator(lev)

    def progress(processed, total, uid):
        update_state(
            state_path, VERSION, "SCORING_FROZEN_V4_2_ACTION_SETS",
            processed, total,
            message=f"last_uid={uid}; metric values omitted from progress state",
        )
        if processed == 1 or processed % 25 == 0 or processed == total:
            print(f"RJOINT_V4_2_PROGRESS {processed}/{total}", flush=True)

    result = score_population_v4_2(
        lev,
        source_rows,
        action_rows,
        gold_by_uid,
        evaluate_fn=timed_evaluate,
        frozen_identity=actual_identity,
        expected_identity=expected_identity,
        progress_callback=progress,
    )

    sentence_records = result.pop("sentence_records")
    result.update({
        "status": "MEASUREMENT_COMPLETE",
        "wrapper_version": VERSION,
        "experiment_id": EXPERIMENT_ID,
        "claim_scope": lock["claim_scope"],
        "population_cases": pop["cases"],
        "population_clusters": pop["clusters"],
        "population_cluster_sha256": pop["population_cluster_sha256"],
        "uid_cluster_map_sha256": pop["uid_cluster_map_sha256"],
        "provenance_signature_map_sha256":
            pop["provenance_signature_map_sha256"],
        "wrapper_sha256": checks["wrapper_sha256"],
        "gold_projection_version": GOLD_PROJECTION_VERSION,
        "gold_projection_in_memory_sha256": projection_sha,
        "consumption_claimed_before_gold_access": True,
        "single_run_only": True,
        "measurement_authorized": True,
        "selector_trained": False,
        "family_consensus_activated": False,
        "p4_used": False,
        "llm_judge_used": False,
        "reserved_sets_opened": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
    })

    prefix = Path(args.out_prefix)
    summary_path = Path(str(prefix) + "_SUMMARY.json")
    sentence_path = Path(str(prefix) + "_PER_SENTENCE.jsonl")
    summary_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    sentence_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in sentence_records)
        + "\n",
        encoding="utf-8",
    )

    update_state(
        state_path, VERSION, "COMPLETE",
        int(lock["population_cases"]), int(lock["population_cases"]),
        status="COMPLETED",
        message="development-only measurement outputs written",
    )
    print(json.dumps({
        "status": "MEASUREMENT_COMPLETE",
        "experiment_id": EXPERIMENT_ID,
        "summary_sha256": sha256_file(summary_path),
        "per_sentence_sha256": sha256_file(sentence_path),
        "gold_projection_in_memory_sha256": projection_sha,
    }, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
