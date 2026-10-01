#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

VERSION = "MPSEF_V4_STAGE2_INPUT_LOCK_V1"

EXPECTED_CF_SHA = "051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_P1_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_CASES = 1918
EXPECTED_CLUSTERS = 764
EXPECTED_REGISTRY_SHA = "b448650c571f6c93dffe4825417e4f65d6a8cd02e33bd9551728ceac2b242b1a"
EXPECTED_PARITY32_MANIFEST_SHA = "384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e"

P2_REPLAY_ARTIFACT = {
    "run_id": 36894512600,
    "artifact_id": 11179398082,
    "digest": "sha256:b35b8614d0a9ab4e444b650db2c9027d2b2f59e3e8c44a9b16be8a9da02e1b5e",
}
P3_REPLAY_ARTIFACT = {
    "run_id": 36897419883,
    "artifact_id": 11180560530,
    "digest": "sha256:67a271032ccd7bef0614634dd01b1b1292eb98799d81f2c57fea9b6aeb331c8c",
}

P2_MODEL_IDENTITIES = {
    "arabic_gec_upstream_revision": "8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf",
    "ged_revision": "447179dc63d186e4bff09a993e90e73ad622d571",
    "gec_revision": "410588a318d988cdcfdbf64cf5745ed4adea0f6a",
    "ged_weight_sha256": "23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f",
    "gec_weight_sha256": "5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f",
    "morphology_db_sha256": "195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70",
    "disambig_model_sha256": "a1a22431cdc0934151e4039abbd7890f06ba7c1f914ca71a90eba218401ae539",
}
P3_MODEL_IDENTITIES = {
    "text_editing_revision": "4d552ca3ae98029550f27fc52aa1b22883e16e61",
    "pnx_revision": "a162d77269ab6ff556d2c58c5dff8b967c1f649e",
    "pnx_weight_sha256": "d98d683f9ef1738c27f5031c99483d93e9f73c4116c158a97a678270c84fd262",
    "pnx_config_sha256": "2b65052e89f8a44585e3618febf7b65593db109e475f7569ac5d4a96799350f0",
}

AUTHORITATIVE_FILES = [
    "phase2/redesign/mpsef_p2_v2_stage2_production_adapter_v1.py",
    "phase2/redesign/mpsef_p3_v1_stage2_production_adapter_v1.py",
    "phase2/redesign/run_with_progress_watchdog_v2.py",
    "phase2/redesign/mpsef_stageb_change_domain_classifier_v1.py",
    "phase2/redesign/mpsef_executable_actions_legalizer_v1.py",
    "phase2/redesign/mpsef_v4_b02_m01_m03_stage0.py",
    "phase2/redesign/mpsef_build_cf_source_manifest_v1.py",
    "phase2/redesign/MPSEF_V4_CANDIDATE_REGISTRY_ACTIONSET_CONTRACT_V2.md",
    "phase2/redesign/MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_EXECUTION_CONTRACT_V1.md",
    "phase2/redesign/MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_EXECUTION_CONTRACT_V1_AMENDMENT_A1.md",
    "phase2/redesign/MPSEF_PROTECTED_INVARIANTS_CONTRACT_V1.md",
    "phase2/redesign/MPSEF_SOURCE_ONLY_LEGALIZER_LOCK_V1R1.md",
    "phase2/redesign/MPSEF_SHADOW_PROTECTION_DIAGNOSTICS_CONTRACT_V1.md",
    "phase2/redesign/MPSEF_P2_V2_STAGE2_M01_PRODUCTION_BOUND_REPLAY_CLOSURE_LOCK_V1.md",
    "phase2/redesign/MPSEF_P3_V1_STAGE2_PRODUCTION_BOUND_REPLAY_CLOSURE_LOCK_V1.md",
    ".github/workflows/phase2-mpsef-v4-stage2-input-lock-v1.yml",
]


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cf-manifest", required=True)
    ap.add_argument("--p1-proposals", required=True)
    ap.add_argument("--p2-runtime-freeze", required=True)
    ap.add_argument("--p3-runtime-freeze", required=True)
    ap.add_argument("--p2-replay-json", required=True)
    ap.add_argument("--p3-replay-json", required=True)
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    root = Path(args.repo_root)
    cf_path = Path(args.cf_manifest)
    p1_path = Path(args.p1_proposals)

    if sha_file(cf_path) != EXPECTED_CF_SHA:
        raise RuntimeError("STAGE2_INPUT_LOCK_CF_SHA_MISMATCH")
    if sha_file(p1_path) != EXPECTED_P1_SHA:
        raise RuntimeError("STAGE2_INPUT_LOCK_P1_SHA_MISMATCH")

    cf = load_jsonl(cf_path)
    if len(cf) != EXPECTED_CASES:
        raise RuntimeError(f"STAGE2_INPUT_LOCK_CF_CASES:{len(cf)}")
    if len({r["uid"] for r in cf}) != EXPECTED_CASES:
        raise RuntimeError("STAGE2_INPUT_LOCK_CF_UID_UNIQUENESS_FAIL")
    if len({r["cluster_id"] for r in cf}) != EXPECTED_CLUSTERS:
        raise RuntimeError("STAGE2_INPUT_LOCK_CF_CLUSTER_COUNT_FAIL")
    if any(r.get("role") != "C_F" for r in cf):
        raise RuntimeError("STAGE2_INPUT_LOCK_NON_CF_ROW")
    forbidden = {"reference", "gold", "edits", "operations", "corrected", "target"}
    if any(forbidden & set(r) for r in cf):
        raise RuntimeError("STAGE2_INPUT_LOCK_FORBIDDEN_REFERENCE_FIELD")

    p2_replay = load_json(Path(args.p2_replay_json))
    p3_replay = load_json(Path(args.p3_replay_json))

    expected_p2_counts = {
        "fresh_vs_repeat": 32,
        "fresh_vs_reordered": 32,
        "fresh_vs_frozen_trace_output": 32,
    }
    if p2_replay.get("status") != "PASS" or p2_replay.get("counts") != expected_p2_counts:
        raise RuntimeError("STAGE2_INPUT_LOCK_P2_REPLAY_FAIL")
    if p2_replay.get("manifest_sha256") != EXPECTED_PARITY32_MANIFEST_SHA:
        raise RuntimeError("STAGE2_INPUT_LOCK_P2_MANIFEST_FAIL")
    if p2_replay.get("production_adapter_cli_used") is not True:
        raise RuntimeError("STAGE2_INPUT_LOCK_P2_NOT_PRODUCTION_CLI")

    expected_p3_counts = {
        "single_vs_batch": 32,
        "batch_vs_reversed": 32,
        "batch_vs_repeat": 32,
        "batch_vs_frozen_trace": 32,
        "batch_output_vs_frozen_output": 32,
        "parent_identity": 32,
    }
    if p3_replay.get("status") != "PASS" or p3_replay.get("counts") != expected_p3_counts:
        raise RuntimeError("STAGE2_INPUT_LOCK_P3_REPLAY_FAIL")
    if p3_replay.get("manifest_sha256") != EXPECTED_PARITY32_MANIFEST_SHA:
        raise RuntimeError("STAGE2_INPUT_LOCK_P3_MANIFEST_FAIL")
    if p3_replay.get("production_adapter_cli_used") is not True:
        raise RuntimeError("STAGE2_INPUT_LOCK_P3_NOT_PRODUCTION_CLI")
    if p3_replay.get("p1_rerun") is not False or p3_replay.get("exact_frozen_p1_parent_reused") is not True:
        raise RuntimeError("STAGE2_INPUT_LOCK_P3_PARENT_BINDING_FAIL")

    missing = [p for p in AUTHORITATIVE_FILES if not (root / p).is_file()]
    if missing:
        raise RuntimeError(f"STAGE2_INPUT_LOCK_AUTHORITATIVE_FILES_MISSING:{missing}")
    file_hashes = {p: sha_file(root / p) for p in AUTHORITATIVE_FILES}

    p2_runtime_sha = sha_file(Path(args.p2_runtime_freeze))
    p3_runtime_sha = sha_file(Path(args.p3_runtime_freeze))

    payload = {
        "record_id": VERSION,
        "status": "PASS",
        "git_commit": os.environ.get("GITHUB_SHA"),
        "branch": os.environ.get("GITHUB_REF_NAME"),
        "population": {
            "role": "C_F",
            "cases": EXPECTED_CASES,
            "clusters": EXPECTED_CLUSTERS,
            "manifest_sha256": EXPECTED_CF_SHA,
            "protected_detector_version": "MPSEF_PROTECTED_DETECTOR_V1",
            "reference_content_used": False,
            "gold_edit_content_used": False,
        },
        "registry": {
            "namespace": "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A",
            "sha256": EXPECTED_REGISTRY_SHA,
            "families": {
                "P1": "SWEET_QALB14",
                "P2_V2": "SEQ2SEQ_GED_MORPH",
                "P3_V1": "SWEET_QALB14",
            },
        },
        "frozen_p1": {
            "proposal_sha256": EXPECTED_P1_SHA,
            "artifact_run_id": 36765798233,
            "artifact_id": 11123050529,
            "artifact_digest": "sha256:e4020418ca2f2793d4bb79bc766e26838398fb9affba6d0f1c704255cd5aed46",
            "rerun_authorized": False,
        },
        "p2": {
            "model_identities": P2_MODEL_IDENTITIES,
            "runtime_freeze_sha256": p2_runtime_sha,
            "replay": P2_REPLAY_ARTIFACT,
            "replay_counts": expected_p2_counts,
        },
        "p3": {
            "model_identities": P3_MODEL_IDENTITIES,
            "runtime_freeze_sha256": p3_runtime_sha,
            "replay": P3_REPLAY_ARTIFACT,
            "replay_counts": expected_p3_counts,
            "p1_rerun": False,
            "exact_frozen_p1_parent_reused": True,
        },
        "authoritative_file_sha256": file_hashes,
        "watchdog": {
            "version": "ACAD_PASS_PROGRESS_WATCHDOG_V2",
            "stale_seconds": 600,
            "term_grace_seconds": 30,
            "liveness_does_not_reset_progress": True,
        },
        "stage_b_classifier": {
            "version": "MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1",
            "synthetic_run_id": 36896359794,
            "synthetic_artifact_id": 11179965356,
            "synthetic_artifact_digest": "sha256:fcf23c9ba6e5ac4b86241400b4b6be6590d9b09d37ce2407dc5a78b58686ad5f",
            "synthetic_tests": 12,
        },
        "scientific_boundary": {
            "source_only": True,
            "gold_reference_allowed": False,
            "r_joint_allowed": False,
            "quality_metric_allowed": False,
            "selector_training_allowed": False,
            "consensus_activation_allowed": False,
        },
        "full_cf_execution_authorized_by_this_record": True,
        "authorization_scope": [
            "P2_V2_FULL_CF_SOURCE_ONLY_PROPOSALS",
            "P3_V1_FULL_CF_SOURCE_ONLY_PROPOSALS",
            "SOURCE_ONLY_LEGALIZER_DIVERSITY_FAMILY_ANALYSIS",
        ],
    }

    Path(args.out_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md = [
        "# MP-SEF V4 STAGE2 INPUT LOCK V1",
        "",
        "Status: PASS / FROZEN EXECUTION INPUT LOCK",
        "",
        f"- Git commit: {payload['git_commit']}",
        f"- C_F: {EXPECTED_CASES} UIDs / {EXPECTED_CLUSTERS} clusters",
        f"- C_F manifest SHA256: {EXPECTED_CF_SHA}",
        f"- P1 proposal SHA256: {EXPECTED_P1_SHA}",
        f"- Registry SHA256: {EXPECTED_REGISTRY_SHA}",
        f"- P2 runtime-freeze SHA256: {p2_runtime_sha}",
        f"- P3 runtime-freeze SHA256: {p3_runtime_sha}",
        "",
        "## Production-bound replay",
        "",
        "- P2: 32/32 repeat, 32/32 reorder, 32/32 frozen trace/output.",
        "- P3: all six required comparisons 32/32; exact frozen P1 parent reused; P1 not rerun.",
        "",
        "## Scientific boundary",
        "",
        "- source-only: true",
        "- gold/reference: forbidden",
        "- R_joint: forbidden",
        "- quality metric: forbidden",
        "- learned selector: forbidden",
        "- consensus activation: forbidden",
        "",
        "## Authorization",
        "",
        "This lock authorizes only P2/P3 full-C_F source-only proposals and source-only legalizer/diversity/family analysis.",
        "Any semantic change to an authoritative hashed file/runtime/model/registry/baseline invalidates this lock.",
        "",
        "Machine-readable identities are in MPSEF_V4_STAGE2_INPUT_LOCK_V1.json.",
    ]
    Path(args.out_md).write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps({
        "record_id": VERSION,
        "status": "PASS",
        "cases": EXPECTED_CASES,
        "clusters": EXPECTED_CLUSTERS,
        "cf_manifest_sha256": EXPECTED_CF_SHA,
        "p1_proposal_sha256": EXPECTED_P1_SHA,
        "p2_runtime_freeze_sha256": p2_runtime_sha,
        "p3_runtime_freeze_sha256": p3_runtime_sha,
        "authoritative_file_count": len(file_hashes),
        "full_cf_execution_authorized_by_this_record": True,
        "gold_reference_allowed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
