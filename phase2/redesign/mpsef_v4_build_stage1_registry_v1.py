#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

VERSION = "MPSEF_V4_STAGE1_REGISTRY_BUILDER_V1"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"
REGISTRY_SCHEMA_VERSION = "MPSEF_V4_PROPOSER_REGISTRY_V2"

P1_MODEL_REV = "21286e56ce98a86362db540863f91c083b8970f9"
P1_WEIGHT_SHA = "9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d"
TEXT_EDITING_REV = "4d552ca3ae98029550f27fc52aa1b22883e16e61"

P2_UPSTREAM_REV = "8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
P2_GED_REV = "447179dc63d186e4bff09a993e90e73ad622d571"
P2_GEC_REV = "410588a318d988cdcfdbf64cf5745ed4adea0f6a"
P2_GED_WEIGHT_SHA = "23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f"
P2_GEC_WEIGHT_SHA = "5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f"
P2_MORPH_DB_SHA = "195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70"
P2_DISAMBIG_WEIGHT_SHA = "a1a22431cdc0934151e4039abbd7890f06ba7c1f914ca71a90eba218401ae539"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def sha_json(obj) -> str:
    return sha_bytes(json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8"))


def required_file(path: str) -> Path:
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise RuntimeError(f"required file missing: {path}")
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pnx-identity", required=True)
    ap.add_argument("--stage1-workflow", required=True)
    ap.add_argument(
        "--out", default="MPSEF_V4_PROPOSER_REGISTRY_V2.json"
    )
    args = ap.parse_args()

    pnx = json.loads(
        Path(args.pnx_identity).read_text(encoding="utf-8")
    )
    required_pnx = {
        "repo_id",
        "revision",
        "weight_sha256",
        "config_sha256",
        "tokenizer_identity_sha256",
    }
    missing = sorted(required_pnx - set(pnx))
    if missing:
        raise RuntimeError(f"missing Pnx identity fields: {missing}")
    if pnx["repo_id"] != "CAMeL-Lab/text-editing-qalb14-pnx":
        raise RuntimeError("unexpected Pnx repo_id")
    for k in ("revision", "weight_sha256", "config_sha256", "tokenizer_identity_sha256"):
        value = str(pnx[k])
        if len(value) != 64 and k != "revision":
            raise RuntimeError(f"invalid Pnx hash: {k}")
        if k == "revision" and len(value) != 40:
            raise RuntimeError("Pnx revision is not a 40-char commit SHA")

    workflow_path = required_file(args.stage1_workflow)
    workflow_sha = sha_file(workflow_path)

    files = {
        "p1_historical_runner": required_file(
            "phase2/redesign/mpsef_p1_cf_proposals_v1.py"
        ),
        "p2_stage1_runner": required_file(
            "phase2/redesign/mpsef_p2_v2_stage1_proposals_v1.py"
        ),
        "p3_stage1_runner": required_file(
            "phase2/redesign/mpsef_p3_v1_stage1_proposals_v1.py"
        ),
        "packet_builder": required_file(
            "phase2/redesign/mpsef_v4_build_stage1_packet_v1.py"
        ),
        "legalizer_action_builder": required_file(
            "phase2/redesign/mpsef_v4_stage1_legalizer_actions_v1.py"
        ),
        "diversity_analyzer": required_file(
            "phase2/redesign/mpsef_v4_stage1_diversity_v1.py"
        ),
        "b01_contract": required_file(
            "phase2/redesign/MPSEF_P2_V2_WORD_IDENTITY_CONTRACT_V1.md"
        ),
        "b02_contract": required_file(
            "phase2/redesign/MPSEF_V4_CANDIDATE_REGISTRY_ACTIONSET_CONTRACT_V2.md"
        ),
        "m01_contract": required_file(
            "phase2/redesign/MPSEF_P3_V1_ROLE_AMENDMENT_V2.md"
        ),
        "m02_contract": required_file(
            "phase2/redesign/MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V2.md"
        ),
        "m03_contract": required_file(
            "phase2/redesign/MPSEF_SHADOW_PROTECTION_DIAGNOSTICS_CONTRACT_V1.md"
        ),
        "research_rebaseline": required_file(
            "phase2/redesign/ACAD_PASS_PRE_STAGE1_FRESH_RESEARCH_REBASELINE_V2.md"
        ),
    }
    file_hashes = {k: sha_file(v) for k, v in files.items()}

    p1_runtime = {
        "python": "3.10",
        "torch": "1.12.1+cpu",
        "transformers": "4.30.0",
        "huggingface_hub": "0.16.4",
        "sentencepiece": "0.1.99",
        "numpy": "1.23.5",
        "text_editing_revision": TEXT_EDITING_REV,
    }
    p2_runtime = {
        "python": "3.9",
        "torch": "1.11.0+cpu",
        "transformers_modified": "4.22.2",
        "numpy": "1.23.5",
        "camel_tools": "1.4.1",
        "datasets": "2.5.1",
        "sentencepiece": "0.1.99",
        "protobuf": "3.20.3",
        "huggingface_hub": "0.10.1",
        "tokenizers": "0.12.1",
        "arabic_gec_revision": P2_UPSTREAM_REV,
    }
    p3_runtime = dict(p1_runtime)

    proposers = [
        {
            "registry_namespace": REGISTRY_NAMESPACE,
            "proposer_id": "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2",
            "proposer_version": "P1_FROZEN_V1",
            "family_id": "SWEET_QALB14",
            "ancestry_id": "SWEET_NOPNX_ITER2",
            "role": "FROZEN_CONTROL",
            "parent_proposer_id": None,
            "parent_proposer_version": None,
            "source_input": "ORIGINAL_SOURCE",
            "implementation_sha256": file_hashes["p1_historical_runner"],
            "workflow_sha256": workflow_sha,
            "runtime_lock_sha256": sha_json(p1_runtime),
            "runtime_lock": p1_runtime,
            "model_identities": {
                "repo_id": "CAMeL-Lab/text-editing-qalb14-nopnx",
                "revision": P1_MODEL_REV,
                "weight_sha256": P1_WEIGHT_SHA,
                "upstream_text_editing_revision": TEXT_EDITING_REV,
            },
            "tokenizer_identities": {
                "bound_to_model_revision": P1_MODEL_REV,
            },
            "source_only": True,
            "gold_reference_allowed": False,
            "enabled_stage": "STAGE1",
            "status": "STAGE1_AUTHORIZED",
        },
        {
            "registry_namespace": REGISTRY_NAMESPACE,
            "proposer_id": "P2_V2_ARABART_GED_MORPH_WORDALIGNED",
            "proposer_version": "P2_V2_1",
            "family_id": "SEQ2SEQ_GED_MORPH",
            "ancestry_id": "ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR",
            "role": "HETEROGENEOUS_CANDIDATE",
            "parent_proposer_id": None,
            "parent_proposer_version": None,
            "source_input": "ORIGINAL_SOURCE",
            "implementation_sha256": file_hashes["p2_stage1_runner"],
            "workflow_sha256": workflow_sha,
            "runtime_lock_sha256": sha_json(p2_runtime),
            "runtime_lock": p2_runtime,
            "model_identities": {
                "ged_repo_id": "CAMeL-Lab/camelbert-msa-qalb14-ged-13",
                "ged_revision": P2_GED_REV,
                "ged_weight_sha256": P2_GED_WEIGHT_SHA,
                "gec_repo_id": "CAMeL-Lab/arabart-qalb14-gec-ged-13",
                "gec_revision": P2_GEC_REV,
                "gec_weight_sha256": P2_GEC_WEIGHT_SHA,
                "arabic_gec_revision": P2_UPSTREAM_REV,
                "morphology_db_sha256": P2_MORPH_DB_SHA,
                "disambig_weight_sha256": P2_DISAMBIG_WEIGHT_SHA,
            },
            "tokenizer_identities": {
                "bound_to_ged_revision": P2_GED_REV,
                "bound_to_gec_revision": P2_GEC_REV,
            },
            "source_only": True,
            "gold_reference_allowed": False,
            "enabled_stage": "STAGE1",
            "status": "STAGE1_AUTHORIZED",
        },
        {
            "registry_namespace": REGISTRY_NAMESPACE,
            "proposer_id": "P3_V1_SWEET_NOPNX2_PNX1",
            "proposer_version": "P3_V1_1",
            "family_id": "SWEET_QALB14",
            "ancestry_id": "P1_CONTROL_PLUS_PNX1",
            "role": "OPTIONAL_PUNCTUATION_FULLCORRECTION_EXTENSION",
            "parent_proposer_id": "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2",
            "parent_proposer_version": "P1_FROZEN_V1",
            "source_input": "EXACT_P1_PARENT_OUTPUT",
            "implementation_sha256": file_hashes["p3_stage1_runner"],
            "workflow_sha256": workflow_sha,
            "runtime_lock_sha256": sha_json(p3_runtime),
            "runtime_lock": p3_runtime,
            "model_identities": {
                **pnx,
                "upstream_text_editing_revision": TEXT_EDITING_REV,
            },
            "tokenizer_identities": {
                "tokenizer_identity_sha256": pnx["tokenizer_identity_sha256"],
                "bound_to_model_revision": pnx["revision"],
            },
            "source_only": True,
            "gold_reference_allowed": False,
            "enabled_stage": "STAGE1",
            "status": "STAGE1_AUTHORIZED",
        },
    ]

    registry = {
        "record_id": REGISTRY_SCHEMA_VERSION,
        "builder_version": VERSION,
        "registry_namespace": REGISTRY_NAMESPACE,
        "status": "STAGE1_REGISTRY_FROZEN",
        "stage": "STAGE1_SOURCE_ONLY",
        "workflow_sha256": workflow_sha,
        "proposers": proposers,
        "architecture_family_map": {
            "SWEET_QALB14": [
                "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2",
                "P3_V1_SWEET_NOPNX2_PNX1",
            ],
            "SEQ2SEQ_GED_MORPH": [
                "P2_V2_ARABART_GED_MORPH_WORDALIGNED",
            ],
        },
        "independent_family_count": 2,
        "file_hashes": file_hashes,
        "source_only": True,
        "gold_reference_allowed": False,
        "quality_metric_allowed": False,
        "r_joint_allowed": False,
        "selector_training_allowed": False,
        "consensus_generation_allowed": False,
    }

    out = Path(args.out)
    out.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "record_id": registry["record_id"],
        "status": registry["status"],
        "registry_sha256": sha_file(out),
        "proposer_count": len(proposers),
        "independent_family_count": 2,
        "gold_reference_allowed": False,
        "r_joint_allowed": False,
    }, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
