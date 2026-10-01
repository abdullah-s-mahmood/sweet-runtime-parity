# Revalidation trigger: fail-closed workflow with pipefail.
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import unicodedata
from difflib import SequenceMatcher

from mpsef_executable_actions_legalizer_v1 import (
    boundary_guard,
    derived_spans,
    protected_signature,
    protection_proof,
)

VERSION = "MPSEF_V4_B02_M01_M03_STAGE0_V1"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"
ACTIONSET_VERSION = "MPSEF_V4_SOURCE_ONLY_ACTION_SET_V2"

P1 = "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2"
P2 = "P2_V2_ARABART_GED_MORPH_WORDALIGNED"
P3 = "P3_V1_SWEET_NOPNX2_PNX1"

EXECUTABLE_STATES = {"OK"}
KNOWN_STATES = {
    "OK",
    "SOURCE_IDENTITY_MISMATCH",
    "INPUT_IDENTITY_FAILED",
    "EMPTY_OUTPUT",
    "EXECUTION_FAILED",
    "TOKENIZATION_FAILED",
    "WORD_IDENTITY_FAILED",
    "TRUNCATED_OR_LENGTH_UNPROVEN",
    "GENERATION_INCOMPLETE",
    "ALIGNMENT_FAILED",
    "ALIGNMENT_AMBIGUOUS",
    "NONREVERSIBLE",
    "PROTECTED_BLOCKED",
    "PROVENANCE_INCOMPLETE",
    "RUNTIME_IDENTITY_MISMATCH",
    "MODEL_INTERFACE_UNPROVEN",
    "UNKNOWN_FAILURE",
}


class Stage0Error(RuntimeError):
    pass


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_json(obj) -> str:
    raw = json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return sha_text(raw)


def canonical_registry():
    return [
        {
            "registry_namespace": REGISTRY_NAMESPACE,
            "proposer_id": P1,
            "proposer_version": "P1_FROZEN_V1",
            "family_id": "SWEET_QALB14",
            "ancestry_id": "SWEET_NOPNX_ITER2",
            "role": "FROZEN_CONTROL",
            "parent_proposer_id": None,
            "parent_proposer_version": None,
            "source_input": "ORIGINAL_SOURCE",
            "source_only": True,
            "gold_reference_allowed": False,
        },
        {
            "registry_namespace": REGISTRY_NAMESPACE,
            "proposer_id": P2,
            "proposer_version": "P2_V2_1",
            "family_id": "SEQ2SEQ_GED_MORPH",
            "ancestry_id": "ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR",
            "role": "HETEROGENEOUS_CANDIDATE",
            "parent_proposer_id": None,
            "parent_proposer_version": None,
            "source_input": "ORIGINAL_SOURCE",
            "source_only": True,
            "gold_reference_allowed": False,
        },
        {
            "registry_namespace": REGISTRY_NAMESPACE,
            "proposer_id": P3,
            "proposer_version": "P3_V1_1",
            "family_id": "SWEET_QALB14",
            "ancestry_id": "P1_CONTROL_PLUS_PNX1",
            "role": "OPTIONAL_PUNCTUATION_FULLCORRECTION_EXTENSION",
            "parent_proposer_id": P1,
            "parent_proposer_version": "P1_FROZEN_V1",
            "source_input": "EXACT_P1_PARENT_OUTPUT",
            "source_only": True,
            "gold_reference_allowed": False,
        },
    ]


def validate_registry(registry):
    seen = set()
    for rec in registry:
        if rec.get("registry_namespace") != REGISTRY_NAMESPACE:
            raise Stage0Error("B02_REGISTRY_NAMESPACE_MISMATCH")
        key = (rec.get("proposer_id"), rec.get("proposer_version"))
        if key in seen:
            raise Stage0Error("B02_DUPLICATE_PROPOSER_ID_VERSION")
        seen.add(key)
        if rec.get("gold_reference_allowed") is not False:
            raise Stage0Error("B02_GOLD_REFERENCE_NOT_FORBIDDEN")
        if rec.get("source_only") is not True:
            raise Stage0Error("B02_SOURCE_ONLY_NOT_FROZEN")

    by_id = {r["proposer_id"]: r for r in registry}
    for required in (P1, P2, P3):
        if required not in by_id:
            raise Stage0Error(f"B02_REQUIRED_PROPOSER_MISSING:{required}")

    if by_id[P1]["family_id"] != by_id[P3]["family_id"]:
        raise Stage0Error("M01_P1_P3_FAMILY_MISMATCH")
    if by_id[P3]["parent_proposer_id"] != P1:
        raise Stage0Error("M01_P3_PARENT_MISMATCH")
    return by_id


def proposal(
    proposer_id,
    source,
    output,
    *,
    state="OK",
    version=None,
    parent_output_sha256=None,
    input_text=None,
):
    versions = {
        P1: "P1_FROZEN_V1",
        P2: "P2_V2_1",
        P3: "P3_V1_1",
    }
    text_in = source if input_text is None else input_text
    return {
        "registry_namespace": REGISTRY_NAMESPACE,
        "proposer_id": proposer_id,
        "proposer_version": version or versions.get(proposer_id, "UNKNOWN"),
        "uid": "SYN-UID",
        "case_id": "SYN-CASE",
        "cluster_id": "SYN-CLUSTER",
        "source": source,
        "source_sha256": sha_text(source),
        "input_text": text_in,
        "input_sha256": sha_text(text_in),
        "parent_output_sha256": parent_output_sha256,
        "full_proposer_output": output,
        "output_sha256": sha_text(output),
        "execution_state": state,
        "failure_reasons": [] if state == "OK" else [f"SYNTHETIC:{state}"],
        "source_only": True,
        "gold_reference_consulted": False,
        "quality_scored": False,
    }


def action_identity(uid, source_sha, output_sha, provenance):
    prov = sorted(
        (x["proposer_id"], x["proposer_version"]) for x in provenance
    )
    return sha_json(
        {
            "version": ACTIONSET_VERSION,
            "uid": uid,
            "source_sha256": source_sha,
            "output_sha256": output_sha,
            "provenance": prov,
        }
    )


def build_action_set(
    source,
    proposal_rows,
    registry,
    *,
    registry_sha_expected=None,
    supplied_experiment_namespace=None,
):
    by_id = validate_registry(registry)
    actual_registry_sha = sha_json(registry)

    if (
        registry_sha_expected is not None
        and registry_sha_expected != actual_registry_sha
    ):
        raise Stage0Error("B02_REGISTRY_SHA_MISMATCH")

    if supplied_experiment_namespace is not None:
        if "V3" in supplied_experiment_namespace or "RJOINT_V2" in supplied_experiment_namespace:
            raise Stage0Error("B02_V3_AUTHORIZATION_ID_REJECTED")
        if not supplied_experiment_namespace.startswith("MPSEF-V4"):
            raise Stage0Error("B02_UNKNOWN_EXPERIMENT_NAMESPACE")

    seen_rows = set()
    failure_rows = []
    candidates = []

    keep_prov = [{
        "proposer_id": "KEEP",
        "proposer_version": "SYSTEM",
        "family_id": "KEEP",
        "ancestry_id": "KEEP",
    }]
    candidates.append({
        "type": "KEEP",
        "output": source,
        "output_sha256": sha_text(source),
        "provenance": keep_prov,
        "keep_semantics": True,
    })

    for row in proposal_rows:
        pid = row.get("proposer_id")
        ver = row.get("proposer_version")
        if pid not in by_id:
            raise Stage0Error(f"B02_UNREGISTERED_PROPOSER:{pid}")
        if ver != by_id[pid]["proposer_version"]:
            raise Stage0Error(f"B02_PROPOSER_VERSION_MISMATCH:{pid}")
        key = (pid, ver)
        if key in seen_rows:
            raise Stage0Error(f"B02_DUPLICATE_PROPOSER_ROW:{pid}:{ver}")
        seen_rows.add(key)

        state = row.get("execution_state")
        if state not in KNOWN_STATES:
            raise Stage0Error(f"B02_UNKNOWN_EXECUTION_STATE:{state}")

        if row.get("source_sha256") != sha_text(source):
            raise Stage0Error(f"B02_SOURCE_IDENTITY_MISMATCH:{pid}")

        if pid == P3:
            parent_hash = row.get("parent_output_sha256")
            if not parent_hash:
                raise Stage0Error("B02_P3_PARENT_OUTPUT_HASH_MISSING")
            if row.get("input_sha256") != parent_hash:
                raise Stage0Error("B02_P3_PARENT_OUTPUT_IDENTITY_MISMATCH")

        if state not in EXECUTABLE_STATES:
            failure_rows.append({
                "proposer_id": pid,
                "proposer_version": ver,
                "execution_state": state,
            })
            continue

        output = row.get("full_proposer_output")
        if not isinstance(output, str):
            raise Stage0Error(f"B02_OUTPUT_NOT_STRING:{pid}")

        meta = by_id[pid]
        candidates.append({
            "type": pid,
            "output": output,
            "output_sha256": sha_text(output),
            "provenance": [{
                "proposer_id": pid,
                "proposer_version": ver,
                "family_id": meta["family_id"],
                "ancestry_id": meta["ancestry_id"],
            }],
            "keep_semantics": False,
        })

    # Literal exact-string dedup. KEEP-equivalent text retains KEEP semantics.
    dedup = {}
    order = []
    for cand in candidates:
        key = cand["output"]
        if key not in dedup:
            dedup[key] = {
                "output": cand["output"],
                "output_sha256": cand["output_sha256"],
                "provenance": list(cand["provenance"]),
                "keep_semantics": bool(cand["keep_semantics"]),
            }
            order.append(key)
        else:
            dedup[key]["provenance"].extend(cand["provenance"])
            dedup[key]["keep_semantics"] = (
                dedup[key]["keep_semantics"] or cand["keep_semantics"]
            )

    actions = []
    uid = "SYN-UID"
    source_sha = sha_text(source)
    for key in order:
        d = dedup[key]
        d["provenance"] = sorted(
            d["provenance"],
            key=lambda x: (x["proposer_id"], x["proposer_version"]),
        )
        actions.append({
            "action_id": action_identity(
                uid, source_sha, d["output_sha256"], d["provenance"]
            ),
            "output": d["output"],
            "output_sha256": d["output_sha256"],
            "provenance": d["provenance"],
            "keep_semantics": d["keep_semantics"],
        })

    if sum(1 for a in actions if a["keep_semantics"]) != 1:
        raise Stage0Error("B02_KEEP_SEMANTICS_NOT_EXACTLY_ONE")

    return {
        "record_id": ACTIONSET_VERSION,
        "registry_sha256": actual_registry_sha,
        "raw_action_count": len(candidates),
        "max_raw_action_capacity": 1 + len(registry),
        "unique_action_count": len(actions),
        "actions": actions,
        "failure_rows": failure_rows,
    }


def architecture_family_support(action):
    return {
        p["family_id"]
        for p in action["provenance"]
        if p["family_id"] != "KEEP"
    }


def char_class(ch):
    if ch.isspace():
        return "SPACE"
    cat = unicodedata.category(ch)
    if cat.startswith("P"):
        return "PUNCT"
    return "LEXICAL"


def classify_change_domain(a: str, b: str):
    if a == b:
        return "NO_CHANGE"
    sm = SequenceMatcher(a=a, b=b, autojunk=False)
    classes = set()
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        for ch in a[i1:i2] + b[j1:j2]:
            classes.add(char_class(ch))
    if classes == {"SPACE"}:
        return "BOUNDARY_ONLY"
    if classes == {"PUNCT"}:
        return "PUNCTUATION_ONLY"
    if classes == {"LEXICAL"}:
        return "LEXICAL_ONLY"
    return "MIXED"


def nearest_nonspace_left(text: str, pos: int):
    tokens = list(re.finditer(r"\S+", text[:pos]))
    return tokens[-1].group(0) if tokens else None


def nearest_nonspace_right(text: str, pos: int):
    m = re.search(r"\S+", text[pos:])
    return m.group(0) if m else None


def local_signature(text: str, s: int, e: int):
    bg = boundary_guard(text, s, e)
    return {
        "left_gap": bg["left_gap"],
        "right_gap": bg["right_gap"],
        "left_token": nearest_nonspace_left(text, s),
        "right_token": nearest_nonspace_right(text, e),
    }


def shadow_protection_diagnostic(source: str, output: str):
    proof = protection_proof(source, output)
    reasons = list(proof.get("reasons", []))
    result = {
        "v3_status": proof["status"],
        "v3_reasons": reasons,
        "shadow_status": None,
        "causes": [],
        "global_ordinal_only_indices": [],
    }

    if proof["status"] == "PASS":
        result["shadow_status"] = "V3_PASS_SHADOW_PASS"
        return result

    if any("ALIGNMENT_WORK_BUDGET_EXCEEDED" in x for x in reasons):
        result["causes"] = ["ALIGNMENT_BUDGET_EXCEEDED"]
        result["shadow_status"] = "SHADOW_INCONCLUSIVE"
        return result

    src_spans = proof["source_spans"]
    out_spans = proof["output_spans"]
    signature_changed = protected_signature(src_spans) != protected_signature(out_spans)

    # A material protected-signature change is directly observable and is
    # stronger than alignment-only uncertainty for shadow-policy purposes.
    # Keep alignment uncertainty as secondary evidence, but never let it turn
    # a known protected-entity mutation into a local-pass/inconclusive case.
    if signature_changed:
        result["causes"].append("ENTITY_TEXT_CHANGED")
        if any(
            ("MULTIPLE_OPTIMAL" in x)
            or ("NONCONTIGUOUS" in x)
            or ("NO_OPTIMAL_EXACT_MATCH" in x)
            for x in reasons
        ):
            result["causes"].append("ALIGNMENT_AMBIGUOUS")
        result["causes"] = sorted(set(result["causes"]))
        if len(result["causes"]) > 1:
            result["causes"].append("MULTIPLE_CAUSES")
        result["shadow_status"] = "V3_BLOCKED_SHADOW_BLOCKED"
        return result

    if any(
        ("MULTIPLE_OPTIMAL" in x)
        or ("NONCONTIGUOUS" in x)
        or ("NO_OPTIMAL_EXACT_MATCH" in x)
        for x in reasons
    ):
        result["causes"] = ["ALIGNMENT_AMBIGUOUS"]
        result["shadow_status"] = "SHADOW_INCONCLUSIVE"
        return result

    audit = proof["optimal_alignment_audit"]
    attachment_categories = {
        "CITATION_DOI",
        "CODE_LATIN_TECHNICAL",
        "NUMBER_UNIT_COUPLED",
        "PERCENT_COUPLED",
        "URL_EMAIL",
        "DOCUMENT_STRUCTURE",
        "EQUATION_FORMULA",
    }

    for idx, span in enumerate(src_spans):
        mapped = (
            audit["mapped_spans"][idx]
            if idx < len(audit.get("mapped_spans", []))
            else None
        )
        if not mapped or not mapped.get("mapping_unique_contiguous"):
            continue
        j, k = mapped["output_start"], mapped["output_end"]
        if output[j:k] != span["text"]:
            if "ENTITY_TEXT_CHANGED" not in result["causes"]:
                result["causes"].append("ENTITY_TEXT_CHANGED")
            continue

        sg = local_signature(source, span["source_start"], span["source_end"])
        og = local_signature(output, j, k)

        if sg["left_gap"] != og["left_gap"] or sg["right_gap"] != og["right_gap"]:
            result["causes"].append("LOCAL_SEPARATOR_CHANGED")

        local_anchor_changed = (
            sg["left_token"] != og["left_token"]
            or sg["right_token"] != og["right_token"]
        )
        if local_anchor_changed and span["category"] in attachment_categories:
            result["causes"].append("LOCAL_ATTACHMENT_CHANGED")
            if span["category"] == "CITATION_DOI":
                result["causes"].append("CITATION_MOVEMENT")
            if span["category"] == "NUMBER_UNIT_COUPLED":
                result["causes"].append("NUMBER_UNIT_LINKAGE_CHANGED")
            if span["category"] == "PERCENT_COUPLED":
                result["causes"].append("PERCENT_LINKAGE_CHANGED")
            if span["category"] == "DOCUMENT_STRUCTURE":
                result["causes"].append("DOCUMENT_STRUCTURE_LINKAGE_CHANGED")

        ordinal_reason = f"PROTECTED_ATTACHMENT_ORDINAL_CHANGED:{idx}"
        if ordinal_reason in reasons:
            if (
                not local_anchor_changed
                and sg["left_gap"] == og["left_gap"]
                and sg["right_gap"] == og["right_gap"]
                and protected_signature(src_spans) == protected_signature(out_spans)
            ):
                result["causes"].append("GLOBAL_ORDINAL_ONLY_CHANGED")
                result["global_ordinal_only_indices"].append(idx)

    result["causes"] = sorted(set(result["causes"]))
    non_global = [
        x for x in result["causes"] if x != "GLOBAL_ORDINAL_ONLY_CHANGED"
    ]

    # V3 can also emit low-level optimal-path reasons even when the only
    # higher-level policy disagreement is global ordinal. We require that any
    # such raw reasons do not indicate protected-char mutation.
    mutation_reasons = [
        x for x in reasons
        if "DELETE_PROTECTED" in x
        or "SUBSTITUTE_PROTECTED" in x
        or "INSERT_AT_PROTECTED_BOUNDARY" in x
    ]

    if (
        result["global_ordinal_only_indices"]
        and not non_global
        and not mutation_reasons
    ):
        result["shadow_status"] = "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY"
    else:
        result["shadow_status"] = "V3_BLOCKED_SHADOW_BLOCKED"

    if len(result["causes"]) > 1:
        result["causes"].append("MULTIPLE_CAUSES")
    return result


def self_test():
    results = {}

    def ok(name, fn):
        fn()
        results[name] = "PASS"

    def expect_fail(name, fn, contains):
        try:
            fn()
        except Stage0Error as e:
            if contains not in str(e):
                raise AssertionError(f"{name}: wrong failure {e}")
            results[name] = "PASS"
            return
        raise AssertionError(f"{name}: expected Stage0Error containing {contains}")

    registry = canonical_registry()
    reg_by_id = validate_registry(registry)
    registry_sha = sha_json(registry)
    source = "نص أصلي"

    # ---------------- B02 ----------------

    def b02_s01():
        rows = [
            proposal(P1, source, source, state="EXECUTION_FAILED"),
            proposal(P2, source, source, state="EXECUTION_FAILED"),
            proposal(
                P3,
                source,
                source,
                state="EXECUTION_FAILED",
                parent_output_sha256=sha_text(source),
                input_text=source,
            ),
        ]
        a = build_action_set(source, rows, registry)
        assert a["unique_action_count"] == 1
        assert a["actions"][0]["keep_semantics"]
        assert len(a["failure_rows"]) == 3
    ok("B02-S01_KEEP_ONLY_ALL_FAIL", b02_s01)

    def b02_s02():
        a = build_action_set(
            source,
            [proposal(P2, source, source + " مصحح")],
            registry,
        )
        assert a["unique_action_count"] == 2
    ok("B02-S02_KEEP_PLUS_ONE", b02_s02)

    def b02_s03():
        p1out = source + " أ"
        rows = [
            proposal(P1, source, p1out),
            proposal(P2, source, source + " ب"),
            proposal(
                P3,
                source,
                source + " ج",
                parent_output_sha256=sha_text(p1out),
                input_text=p1out,
            ),
        ]
        a = build_action_set(source, rows, registry)
        assert a["raw_action_count"] == 4
        assert a["max_raw_action_capacity"] == 4
    ok("B02-S03_RAW_CAPACITY_FOUR", b02_s03)

    def b02_s04():
        p1out = source + " موحد"
        a = build_action_set(
            source,
            [
                proposal(P1, source, p1out),
                proposal(
                    P3,
                    source,
                    p1out,
                    parent_output_sha256=sha_text(p1out),
                    input_text=p1out,
                ),
            ],
            registry,
        )
        same = [x for x in a["actions"] if x["output"] == p1out][0]
        pids = {p["proposer_id"] for p in same["provenance"]}
        assert pids == {P1, P3}
        assert len(architecture_family_support(same)) == 1
    ok("B02-S04_P1_P3_DEDUP_MULTI_PROVENANCE", b02_s04)

    def b02_s05():
        a = build_action_set(
            source,
            [proposal(P1, source, source)],
            registry,
        )
        assert a["unique_action_count"] == 1
        keep = a["actions"][0]
        assert keep["keep_semantics"]
        pids = {p["proposer_id"] for p in keep["provenance"]}
        assert {"KEEP", P1}.issubset(pids)
    ok("B02-S05_PROPOSER_EQUALS_KEEP", b02_s05)

    def b02_s06():
        out = source + " X"
        a = build_action_set(
            source,
            [
                proposal(P1, source, out),
                proposal(P2, source, out),
            ],
            registry,
        )
        x = [z for z in a["actions"] if z["output"] == out][0]
        assert {p["family_id"] for p in x["provenance"]} == {
            "SWEET_QALB14", "SEQ2SEQ_GED_MORPH"
        }
    ok("B02-S06_IDENTICAL_TEXT_DIFFERENT_ANCESTRY", b02_s06)

    def b02_s07():
        a = build_action_set(
            source,
            [
                proposal(P1, source, source + " X"),
                proposal(P2, source, source + "  X"),
            ],
            registry,
        )
        assert a["unique_action_count"] == 3
    ok("B02-S07_WHITESPACE_DIFFERENCE_NOT_DEDUP", b02_s07)

    expect_fail(
        "B02-S08_P3_PARENT_HASH_REQUIRED",
        lambda: build_action_set(
            source, [proposal(P3, source, source + "!", parent_output_sha256=None)],
            registry
        ),
        "P3_PARENT_OUTPUT_HASH_MISSING",
    )

    expect_fail(
        "B02-S09_P3_INPUT_PARENT_MISMATCH",
        lambda: build_action_set(
            source,
            [proposal(
                P3,
                source,
                source + "!",
                parent_output_sha256=sha_text("parent"),
                input_text="different",
            )],
            registry,
        ),
        "P3_PARENT_OUTPUT_IDENTITY_MISMATCH",
    )

    expect_fail(
        "B02-S10_UNREGISTERED_PROPOSER",
        lambda: build_action_set(
            source,
            [proposal("P999", source, source + "!")],
            registry,
        ),
        "UNREGISTERED_PROPOSER",
    )

    def duplicate_registry():
        bad = list(registry) + [dict(registry[0])]
        validate_registry(bad)
    expect_fail(
        "B02-S11_DUPLICATE_REGISTRY_ID_VERSION",
        duplicate_registry,
        "DUPLICATE_PROPOSER_ID_VERSION",
    )

    expect_fail(
        "B02-S12_UNKNOWN_EXECUTION_STATE",
        lambda: build_action_set(
            source,
            [proposal(P2, source, source + "!", state="MYSTERY")],
            registry,
        ),
        "UNKNOWN_EXECUTION_STATE",
    )

    def b02_s13():
        a = build_action_set(
            source,
            [proposal(P2, source, source + "!", state="EXECUTION_FAILED")],
            registry,
        )
        assert len(a["failure_rows"]) == 1
        assert a["unique_action_count"] == 1
    ok("B02-S13_FAILURE_RETAINED_NO_ACTION", b02_s13)

    def b02_s14():
        out = source + " X"
        a1 = build_action_set(source, [proposal(P1, source, out)], registry)
        a2 = build_action_set(
            source,
            [proposal(P1, source, out), proposal(P2, source, out)],
            registry,
        )
        id1 = [a["action_id"] for a in a1["actions"] if a["output"] == out][0]
        id2 = [a["action_id"] for a in a2["actions"] if a["output"] == out][0]
        assert id1 != id2
    ok("B02-S14_PROVENANCE_CHANGES_ACTION_ID", b02_s14)

    expect_fail(
        "B02-S15_V3_AUTHORIZATION_REJECTED",
        lambda: build_action_set(
            source, [], registry,
            supplied_experiment_namespace="MPSEF-V3-RJOINT_V2"
        ),
        "V3_AUTHORIZATION_ID_REJECTED",
    )

    expect_fail(
        "B02-S16_REGISTRY_SHA_MISMATCH",
        lambda: build_action_set(
            source, [], registry, registry_sha_expected="0" * 64
        ),
        "REGISTRY_SHA_MISMATCH",
    )

    def roster_mismatch():
        reduced = [x for x in registry if x["proposer_id"] != P3]
        validate_registry(reduced)
    expect_fail(
        "B02-S17_FROZEN_ROSTER_MISMATCH",
        roster_mismatch,
        "REQUIRED_PROPOSER_MISSING",
    )

    # ---------------- M01 ----------------

    def m01_family_ceiling():
        out = source + " X"
        a = build_action_set(
            source,
            [
                proposal(P1, source, out),
                proposal(
                    P3,
                    source,
                    out,
                    parent_output_sha256=sha_text(out),
                    input_text=out,
                ),
            ],
            registry,
        )
        action = [x for x in a["actions"] if x["output"] == out][0]
        assert architecture_family_support(action) == {"SWEET_QALB14"}
    ok("M01-S01_P1_P3_ONE_FAMILY_SUPPORT", m01_family_ceiling)

    def m01_parent_exact():
        p1out = "النص المصحح [1]"
        p3 = proposal(
            P3,
            "النص [1]",
            "النص المصحح، [1]",
            parent_output_sha256=sha_text(p1out),
            input_text=p1out,
        )
        a = build_action_set("النص [1]", [p3], registry)
        assert a["unique_action_count"] == 2
    ok("M01-S02_P3_EXACT_PARENT_INPUT", m01_parent_exact)

    def m01_original_source_protection():
        original = "النص [1] هنا"
        p1out = "النص الجيد [1] هنا"
        p3bad = "النص الجيد [2] هنا"
        proof = protection_proof(original, p3bad)
        assert proof["status"] == "FAIL"
        # Passing/identity of the P1 parent is irrelevant to the final P3 proof.
        assert protection_proof(original, original)["status"] == "PASS"
        assert sha_text(p1out) != sha_text(p3bad)
    ok("M01-S03_P3_PROTECTED_FROM_ORIGINAL_SOURCE", m01_original_source_protection)

    def m01_domains():
        assert classify_change_domain("نص", "نص") == "NO_CHANGE"
        assert classify_change_domain("نص.", "نص،") == "PUNCTUATION_ONLY"
        assert classify_change_domain("ياولد", "يا ولد") == "BOUNDARY_ONLY"
        assert classify_change_domain("ولد", "بنت") == "LEXICAL_ONLY"
        assert classify_change_domain("ولد.", "بنت،") == "MIXED"
    ok("M01-S04_CHANGE_DOMAIN_CLASSIFIER", m01_domains)

    # ---------------- M03 ----------------

    def m03_s01():
        src = "قبل هذا النص [1] هنا"
        out = "كلمة قبل هذا النص [1] هنا"
        d = shadow_protection_diagnostic(src, out)
        assert d["v3_status"] == "FAIL", d
        assert d["shadow_status"] == "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY", d
        assert "GLOBAL_ORDINAL_ONLY_CHANGED" in d["causes"], d
    ok("M03-S01_DISTANT_INSERT_CITATION_GLOBAL_ORDINAL", m03_s01)

    def m03_s02():
        src = "قبل الجرعة 5 mg يوميا"
        out = "كلمة قبل الجرعة 5 mg يوميا"
        d = shadow_protection_diagnostic(src, out)
        assert d["v3_status"] == "FAIL", d
        assert d["shadow_status"] == "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY", d
    ok("M03-S02_DISTANT_INSERT_UNIT_GLOBAL_ORDINAL", m03_s02)

    def m03_s03():
        src = "كما ورد [1] هنا الآن"
        out = "كما ورد هنا [1] الآن"
        d = shadow_protection_diagnostic(src, out)
        assert d["shadow_status"] != "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY", d
        assert (
            "LOCAL_ATTACHMENT_CHANGED" in d["causes"]
            or "CITATION_MOVEMENT" in d["causes"]
            or "ALIGNMENT_AMBIGUOUS" in d["causes"]
        ), d
    ok("M03-S03_CITATION_MOVEMENT_NOT_ORDINAL_ONLY", m03_s03)

    def m03_s04():
        d = shadow_protection_diagnostic(
            "الجرعة 5 mg يوميا",
            "الجرعة 6 mg يوميا",
        )
        assert d["shadow_status"] != "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY", d
        assert "ENTITY_TEXT_CHANGED" in d["causes"], d
    ok("M03-S04_ENTITY_TEXT_CHANGE", m03_s04)

    def m03_s05():
        src = "الجرعة 5 mg ثم 10 mg يوميا"
        out = "الجرعة 5 mg ثم يوميا 10 mg"
        d = shadow_protection_diagnostic(src, out)
        assert d["shadow_status"] != "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY", d
        assert (
            "LOCAL_ATTACHMENT_CHANGED" in d["causes"]
            or "ALIGNMENT_AMBIGUOUS" in d["causes"]
        ), d
    ok("M03-S05_LOCAL_LINKAGE_CHANGE", m03_s05)

    def m03_s06():
        src = "النص [1] هنا"
        out = "النص[1] هنا"
        d = shadow_protection_diagnostic(src, out)
        assert d["shadow_status"] != "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY", d
        assert "LOCAL_SEPARATOR_CHANGED" in d["causes"], d
    ok("M03-S06_LOCAL_SEPARATOR_CHANGE", m03_s06)

    def m03_s07():
        src = "A [1] [1] B"
        out = "A [1] B"
        d = shadow_protection_diagnostic(src, out)
        assert d["shadow_status"] != "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY", d
        assert (
            "ALIGNMENT_AMBIGUOUS" in d["causes"]
            or "ENTITY_TEXT_CHANGED" in d["causes"]
        ), d
    ok("M03-S07_AMBIGUITY_NO_LOCAL_PASS", m03_s07)

    def m03_s08():
        src = ("كلمة " * 150) + "[1]"
        out = "جديدة " + src
        d = shadow_protection_diagnostic(src, out)
        assert d["shadow_status"] == "SHADOW_INCONCLUSIVE", d
        assert d["causes"] == ["ALIGNMENT_BUDGET_EXCEEDED"], d
    ok("M03-S08_ALIGNMENT_BUDGET_INCONCLUSIVE", m03_s08)

    def m03_s09():
        d = shadow_protection_diagnostic(
            "النص [1] هنا",
            "النص[2] هنا",
        )
        assert d["shadow_status"] != "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY", d
        assert len([x for x in d["causes"] if x != "MULTIPLE_CAUSES"]) >= 1
    ok("M03-S09_MULTICAUSE_NOT_LOCAL_PASS", m03_s09)

    def m03_s10():
        d = shadow_protection_diagnostic("النص [1] هنا", "النص [1] هنا")
        assert d["v3_status"] == "PASS"
        assert d["shadow_status"] == "V3_PASS_SHADOW_PASS"
    ok("M03-S10_IDENTITY_PASS", m03_s10)

    b02 = [k for k in results if k.startswith("B02-")]
    m01 = [k for k in results if k.startswith("M01-")]
    m03 = [k for k in results if k.startswith("M03-")]

    summary = {
        "record_id": VERSION,
        "status": "PASS",
        "contract_results": {
            "B02": {"status": "PASS", "tests": len(b02)},
            "M01": {"status": "PASS", "tests": len(m01)},
            "M03": {"status": "PASS", "tests": len(m03)},
        },
        "tests": results,
        "test_count": len(results),
        "registry_namespace": REGISTRY_NAMESPACE,
        "registry_sha256": registry_sha,
        "project_source_loaded": False,
        "project_gold_loaded": False,
        "project_metric_computed": False,
        "quality_claimed": False,
        "v3_artifacts_modified": False,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if not args.self_test:
        raise SystemExit("SOURCE_FREE_STAGE0_ONLY; use --self-test")
    self_test()


if __name__ == "__main__":
    main()
