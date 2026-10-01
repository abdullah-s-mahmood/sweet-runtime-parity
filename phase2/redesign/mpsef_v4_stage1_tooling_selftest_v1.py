#!/usr/bin/env python3
from __future__ import annotations

import json

from mpsef_v4_stage1_legalizer_actions_v1 import (
    P1_CANONICAL,
    P2,
    P3,
    build_action_set,
    legalize_one,
    normalize_p1,
    sha_text,
    validate_registry,
)
from mpsef_v4_stage1_diversity_v1 import (
    nearest_rank,
    unique_levenshtein_components,
)

VERSION = "MPSEF_V4_STAGE1_TOOLING_SELFTEST_V1"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"


def registry():
    return {
        "registry_namespace": REGISTRY_NAMESPACE,
        "proposers": [
            {
                "proposer_id": P1_CANONICAL,
                "proposer_version": "P1_FROZEN_V1",
                "family_id": "SWEET_QALB14",
                "ancestry_id": "SWEET_NOPNX_ITER2",
                "parent_proposer_id": None,
                "parent_proposer_version": None,
            },
            {
                "proposer_id": P2,
                "proposer_version": "P2_V2_1",
                "family_id": "SEQ2SEQ_GED_MORPH",
                "ancestry_id": "ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR",
                "parent_proposer_id": None,
                "parent_proposer_version": None,
            },
            {
                "proposer_id": P3,
                "proposer_version": "P3_V1_1",
                "family_id": "SWEET_QALB14",
                "ancestry_id": "P1_CONTROL_PLUS_PNX1",
                "parent_proposer_id": P1_CANONICAL,
                "parent_proposer_version": "P1_FROZEN_V1",
            },
        ],
    }


def p2_raw(man, output, state="OK"):
    return {
        "registry_namespace": REGISTRY_NAMESPACE,
        "proposer_id": P2,
        "proposer_version": "P2_V2_1",
        "family_id": "SEQ2SEQ_GED_MORPH",
        "ancestry_id": "ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR",
        "uid": man["uid"],
        "case_id": man["case_id"],
        "cluster_id": man["cluster_id"],
        "source": man["source"],
        "source_sha256": man["source_sha256"],
        "input_text": man["source"],
        "input_sha256": man["source_sha256"],
        "parent_proposer_id": None,
        "parent_proposer_version": None,
        "parent_output_sha256": None,
        "raw_execution_state": state,
        "failure_reasons": [] if state == "OK" else ["SYNTHETIC_FAILURE"],
        "full_proposer_output": output,
        "output_sha256": sha_text(output),
        "trace": {
            "morph_words": ["نص"],
            "word_level_ged_labels": ["UC"],
            "ged_word_identity_trace": [{"morph_word_index": 0}],
            "gec_word_map": [{"morph_word_index": 0}],
            "gec_input_length": 3,
            "gec_label_length": 3,
            "generation": {
                "ged_embedding_hook_calls": [{"output_shape": [1,3,2]}],
                "terminal_eos_index": 2,
                "hit_ceiling": False,
                "decoded_text": output,
            },
        },
        "source_only": True,
        "gold_reference_consulted": False,
        "quality_scored": False,
        "provenance_complete": True,
    }


def p3_raw(man, parent, output):
    ph = sha_text(parent)
    return {
        "registry_namespace": REGISTRY_NAMESPACE,
        "proposer_id": P3,
        "proposer_version": "P3_V1_1",
        "family_id": "SWEET_QALB14",
        "ancestry_id": "P1_CONTROL_PLUS_PNX1",
        "uid": man["uid"],
        "case_id": man["case_id"],
        "cluster_id": man["cluster_id"],
        "source": man["source"],
        "source_sha256": man["source_sha256"],
        "input_text": parent,
        "input_sha256": ph,
        "parent_proposer_id": P1_CANONICAL,
        "parent_proposer_version": "P1_FROZEN_V1",
        "parent_output_sha256": ph,
        "raw_execution_state": "OK",
        "failure_reasons": [],
        "full_proposer_output": output,
        "output_sha256": sha_text(output),
        "trace": {
            "parent_output_sha256": ph,
            "pnx_subwords": ["x"],
            "pnx_labels": ["UC"],
            "pnx_output": output,
        },
        "source_only": True,
        "gold_reference_consed": False,
        "gold_reference_consulted": False,
        "quality_scored": False,
        "provenance_complete": True,
    }


def main():
    tests = {}
    reg = registry()
    by_id = validate_registry(reg)
    reg_sha = "1" * 64

    man = {
        "uid": "SYN-1",
        "case_id": "SYN-C1",
        "cluster_id": "SYN-K1",
        "source": "النص هنا",
    }
    man["source_sha256"] = sha_text(man["source"])

    p1out = "النص جيد هنا"
    p1hist = {
        "uid": man["uid"],
        "case_id": man["case_id"],
        "cluster_id": man["cluster_id"],
        "source": man["source"],
        "source_version_hash": man["source_sha256"],
        "proposer_id": "P1_SWEET_QALB14_NOPNX_ITER2",
        "full_proposer_output": p1out,
        "output_sha256": sha_text(p1out),
        "bundle_id": "SYN",
        "record_id": "SYN-P1",
        "pass1_trace": {
            "subwords": ["x"], "labels": ["UC"], "output": p1out,
        },
        "pass2_trace": {
            "subwords": ["x"], "labels": ["UC"], "output": p1out,
        },
        "runtime": {},
    }

    lp1 = legalize_one(
        man, normalize_p1(p1hist, man, by_id[P1_CANONICAL]),
        by_id[P1_CANONICAL],
    )
    lp2 = legalize_one(
        man, p2_raw(man, "النص ممتاز هنا"), by_id[P2]
    )
    lp3 = legalize_one(
        man, p3_raw(man, p1out, p1out), by_id[P3]
    )
    assert all(x["execution_state"] == "OK" for x in (lp1, lp2, lp3))
    aset = build_action_set(man, [lp1, lp2, lp3], reg_sha)
    assert aset["unique_action_count"] == 3
    sweet = [a for a in aset["actions"] if a["output"] == p1out][0]
    assert {
        x["proposer_id"] for x in sweet["provenance"]
    } == {P1_CANONICAL, P3}
    tests["DEDUP_AND_MULTI_PROVENANCE"] = "PASS"

    bad_p2 = legalize_one(
        man, p2_raw(man, "لن يستخدم", state="EXECUTION_FAILED"),
        by_id[P2],
    )
    assert bad_p2["execution_state"] == "EXECUTION_FAILED"
    a2 = build_action_set(man, [lp1, bad_p2, lp3], reg_sha)
    assert all(
        P2 not in {x["proposer_id"] for x in a["provenance"]}
        for a in a2["actions"]
    )
    tests["FAILED_PROPOSER_NO_ACTION"] = "PASS"

    bad_p3 = p3_raw(man, p1out, p1out + "،")
    bad_p3["input_sha256"] = sha_text("wrong")
    lbad3 = legalize_one(man, bad_p3, by_id[P3])
    assert lbad3["execution_state"] == "INPUT_IDENTITY_FAILED"
    tests["P3_PARENT_IDENTITY_FAIL_CLOSED"] = "PASS"

    manp = {
        "uid": "SYN-2",
        "case_id": "SYN-C2",
        "cluster_id": "SYN-K2",
        "source": "كما ورد [1] هنا",
    }
    manp["source_sha256"] = sha_text(manp["source"])
    mut = p2_raw(manp, "كما ورد [2] هنا")
    lmut = legalize_one(manp, mut, by_id[P2])
    assert lmut["execution_state"] in {
        "PROTECTED_BLOCKED", "ALIGNMENT_AMBIGUOUS"
    }
    assert lmut["executable"] is False
    tests["PROTECTED_MUTATION_FAIL_CLOSED"] = "PASS"

    unique = unique_levenshtein_components("abc", "axc")
    assert unique["status"] == "UNIQUE"
    ambiguous = unique_levenshtein_components("aa", "a")
    assert ambiguous["status"] == "AMBIGUOUS"
    tests["COMPONENT_ALIGNMENT_UNCERTAINTY"] = "PASS"

    assert nearest_rank([1,2,3,4,5], 0.95) == 5
    tests["NEAREST_RANK_P95"] = "PASS"

    result = {
        "record_id": VERSION,
        "status": "PASS",
        "tests": tests,
        "test_count": len(tests),
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
