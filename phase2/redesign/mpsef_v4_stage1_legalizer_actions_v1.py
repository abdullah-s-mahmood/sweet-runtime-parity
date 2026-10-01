#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from mpsef_executable_actions_legalizer_v1 import (
    alignment_ambiguity_status,
    protection_proof,
    reversibility_proof,
)
from mpsef_v4_b02_m01_m03_stage0 import shadow_protection_diagnostic

VERSION = "MPSEF_V4_STAGE1_LEGALIZER_ACTION_BUILDER_V1"
ACTIONSET_VERSION = "MPSEF_V4_SOURCE_ONLY_ACTION_SET_V2"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"
P1_CANONICAL = "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2"
P1_HISTORICAL = "P1_SWEET_QALB14_NOPNX_ITER2"
P2 = "P2_V2_ARABART_GED_MORPH_WORDALIGNED"
P3 = "P3_V1_SWEET_NOPNX2_PNX1"

FINAL_STATE_ORDER = [
    "SOURCE_IDENTITY_MISMATCH",
    "INPUT_IDENTITY_FAILED",
    "EMPTY_OUTPUT",
    "RUNTIME_IDENTITY_MISMATCH",
    "MODEL_INTERFACE_UNPROVEN",
    "TOKENIZATION_FAILED",
    "WORD_IDENTITY_FAILED",
    "TRUNCATED_OR_LENGTH_UNPROVEN",
    "GENERATION_INCOMPLETE",
    "EXECUTION_FAILED",
    "ALIGNMENT_FAILED",
    "NONREVERSIBLE",
    "PROTECTED_BLOCKED",
    "ALIGNMENT_AMBIGUOUS",
    "PROVENANCE_INCOMPLETE",
    "UNKNOWN_FAILURE",
    "OK",
]


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_json(obj) -> str:
    return sha_text(json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ))


def read_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def choose_final_state(reasons):
    cats = {r.split(":", 1)[0] for r in reasons}
    for state in FINAL_STATE_ORDER:
        if state == "OK":
            return "OK"
        if state in cats:
            return state
    return "UNKNOWN_FAILURE"


def validate_registry(registry):
    if registry.get("registry_namespace") != REGISTRY_NAMESPACE:
        raise RuntimeError("registry namespace mismatch")
    rows = registry.get("proposers")
    if not isinstance(rows, list):
        raise RuntimeError("registry proposers missing")
    by_id = {}
    for r in rows:
        pid = r["proposer_id"]
        if pid in by_id:
            raise RuntimeError(f"duplicate registry proposer: {pid}")
        by_id[pid] = r
    for pid in (P1_CANONICAL, P2, P3):
        if pid not in by_id:
            raise RuntimeError(f"required registry proposer missing: {pid}")
    if by_id[P1_CANONICAL]["family_id"] != by_id[P3]["family_id"]:
        raise RuntimeError("P1/P3 family mismatch")
    if by_id[P3].get("parent_proposer_id") != P1_CANONICAL:
        raise RuntimeError("P3 parent mismatch")
    return by_id


def normalize_p1(historical, man, reg):
    output = historical.get("full_proposer_output")
    raw_state = "OK"
    failures = []
    if not isinstance(output, str) or output == "":
        raw_state = "EMPTY_OUTPUT"
        failures = ["EMPTY_OUTPUT"]
    return {
        "registry_namespace": REGISTRY_NAMESPACE,
        "proposer_id": P1_CANONICAL,
        "proposer_version": reg["proposer_version"],
        "family_id": reg["family_id"],
        "ancestry_id": reg["ancestry_id"],
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
        "raw_execution_state": raw_state,
        "failure_reasons": failures,
        "full_proposer_output": output,
        "output_sha256": historical.get("output_sha256"),
        "trace": {
            "pass1_trace": historical.get("pass1_trace"),
            "pass2_trace": historical.get("pass2_trace"),
            "historical_bundle_id": historical.get("bundle_id"),
            "historical_record_id": historical.get("record_id"),
        },
        "runtime_identity": historical.get("runtime"),
        "source_only": True,
        "gold_reference_consulted": False,
        "quality_scored": False,
        "provenance_complete": True,
    }


def provenance_reasons(prop, reg):
    reasons = []
    pid = prop["proposer_id"]
    source = prop["source"]
    output = prop.get("full_proposer_output")
    trace = prop.get("trace")

    raw = prop.get("raw_execution_state")
    if raw and raw != "OK":
        reasons.append(f"{raw}:RAW_PROPOSER_STATE")
        for r in prop.get("failure_reasons", []):
            reasons.append(f"{raw}:{r}")

    if prop.get("registry_namespace") != REGISTRY_NAMESPACE:
        reasons.append("PROVENANCE_INCOMPLETE:REGISTRY_NAMESPACE")
    if prop.get("proposer_version") != reg["proposer_version"]:
        reasons.append("PROVENANCE_INCOMPLETE:PROPOSER_VERSION")
    if prop.get("family_id") != reg["family_id"]:
        reasons.append("PROVENANCE_INCOMPLETE:FAMILY_ID")
    if prop.get("ancestry_id") != reg["ancestry_id"]:
        reasons.append("PROVENANCE_INCOMPLETE:ANCESTRY_ID")
    if prop.get("source_only") is not True:
        reasons.append("PROVENANCE_INCOMPLETE:SOURCE_ONLY_FALSE")
    if prop.get("gold_reference_consulted") is not False:
        reasons.append("PROVENANCE_INCOMPLETE:GOLD_REFERENCE_FLAG")
    if prop.get("quality_scored") is not False:
        reasons.append("PROVENANCE_INCOMPLETE:QUALITY_SCORED_FLAG")

    if pid == P1_CANONICAL:
        for name in ("pass1_trace", "pass2_trace"):
            t = (trace or {}).get(name)
            if not isinstance(t, dict):
                reasons.append(f"PROVENANCE_INCOMPLETE:MISSING_{name.upper()}")
                continue
            if len(t.get("subwords", [])) != len(t.get("labels", [])):
                reasons.append(
                    f"TRUNCATED_OR_LENGTH_UNPROVEN:{name.upper()}_TOKEN_LABEL_MISMATCH"
                )

    elif pid == P2:
        if not isinstance(trace, dict):
            reasons.append("PROVENANCE_INCOMPLETE:MISSING_P2_TRACE")
        else:
            words = trace.get("morph_words")
            labels = trace.get("word_level_ged_labels")
            identity = trace.get("ged_word_identity_trace")
            word_map = trace.get("gec_word_map")
            generation = trace.get("generation") or {}
            if not isinstance(words, list) or not isinstance(labels, list):
                reasons.append("WORD_IDENTITY_FAILED:MISSING_WORD_LABEL_LISTS")
            elif len(words) != len(labels):
                reasons.append("WORD_IDENTITY_FAILED:WORD_LABEL_COUNT")
            if not isinstance(identity, list) or (
                isinstance(words, list) and len(identity) != len(words)
            ):
                reasons.append("WORD_IDENTITY_FAILED:IDENTITY_TRACE_COUNT")
            if not isinstance(word_map, list) or (
                isinstance(words, list) and len(word_map) != len(words)
            ):
                reasons.append("WORD_IDENTITY_FAILED:GEC_WORD_MAP_COUNT")
            if trace.get("gec_input_length") != trace.get("gec_label_length"):
                reasons.append(
                    "TRUNCATED_OR_LENGTH_UNPROVEN:GEC_CONDITIONING_LENGTH"
                )
            if not generation.get("ged_embedding_hook_calls"):
                reasons.append("MODEL_INTERFACE_UNPROVEN:NO_GED_HOOK_CALL")
            if generation.get("terminal_eos_index") is None:
                reasons.append("GENERATION_INCOMPLETE:NO_TERMINAL_EOS")
            if generation.get("hit_ceiling") is True:
                reasons.append(
                    "TRUNCATED_OR_LENGTH_UNPROVEN:GENERATION_HIT_CEILING"
                )
            if generation.get("decoded_text") != output:
                reasons.append("PROVENANCE_INCOMPLETE:GENERATION_OUTPUT_MISMATCH")

    elif pid == P3:
        parent_hash = prop.get("parent_output_sha256")
        if not parent_hash:
            reasons.append("INPUT_IDENTITY_FAILED:PARENT_HASH_MISSING")
        if prop.get("input_sha256") != parent_hash:
            reasons.append("INPUT_IDENTITY_FAILED:PARENT_INPUT_HASH_MISMATCH")
        if prop.get("parent_proposer_id") != P1_CANONICAL:
            reasons.append("INPUT_IDENTITY_FAILED:PARENT_ID")
        if prop.get("parent_proposer_version") != reg.get(
            "parent_proposer_version"
        ):
            reasons.append("INPUT_IDENTITY_FAILED:PARENT_VERSION")
        if not isinstance(trace, dict):
            reasons.append("PROVENANCE_INCOMPLETE:MISSING_P3_TRACE")
        else:
            if trace.get("parent_output_sha256") != parent_hash:
                reasons.append("INPUT_IDENTITY_FAILED:TRACE_PARENT_HASH")
            if len(trace.get("pnx_subwords", [])) != len(
                trace.get("pnx_labels", [])
            ):
                reasons.append(
                    "TRUNCATED_OR_LENGTH_UNPROVEN:PNX_TOKEN_LABEL_MISMATCH"
                )
            if trace.get("pnx_output") != output:
                reasons.append("PROVENANCE_INCOMPLETE:PNX_OUTPUT_MISMATCH")

    if not isinstance(output, str):
        reasons.append("EXECUTION_FAILED:OUTPUT_NOT_STRING")
    elif output.strip() == "":
        reasons.append("EMPTY_OUTPUT:BLANK_OR_EMPTY")

    return reasons


def legalize_one(man, prop, reg):
    reasons = []

    if prop.get("uid") != man["uid"]:
        reasons.append("SOURCE_IDENTITY_MISMATCH:UID")
    if prop.get("case_id") != man["case_id"]:
        reasons.append("SOURCE_IDENTITY_MISMATCH:CASE_ID")
    if prop.get("cluster_id") != man["cluster_id"]:
        reasons.append("SOURCE_IDENTITY_MISMATCH:CLUSTER_ID")
    if prop.get("source") != man["source"]:
        reasons.append("SOURCE_IDENTITY_MISMATCH:SOURCE_TEXT")
    if prop.get("source_sha256") != man["source_sha256"]:
        reasons.append("SOURCE_IDENTITY_MISMATCH:SOURCE_SHA_FIELD")
    if sha_text(man["source"]) != man["source_sha256"]:
        reasons.append("SOURCE_IDENTITY_MISMATCH:MANIFEST_SOURCE_SHA")

    output = prop.get("full_proposer_output")
    if isinstance(output, str):
        if prop.get("output_sha256") != sha_text(output):
            reasons.append("PROVENANCE_INCOMPLETE:OUTPUT_SHA")
    else:
        output = ""

    reasons.extend(provenance_reasons(prop, reg))

    protection = protection_proof(man["source"], output)
    audit = protection.get("optimal_alignment_audit", {})
    ambiguity = alignment_ambiguity_status(
        man["source"], output, protection
    )

    if audit.get("status") == "ERROR":
        reasons.append(
            "ALIGNMENT_FAILED:" + ",".join(audit.get("reasons", []))
        )
    elif ambiguity.get("status") == "AFFECTS_LEGALITY":
        reasons.append(
            "ALIGNMENT_AMBIGUOUS:" + str(ambiguity.get("reason"))
        )

    # Only classify an ordinary protection-policy block when alignment
    # proof itself was available. Preserve all raw protection reasons either way.
    if protection["status"] != "PASS" and audit.get("status") != "ERROR":
        reasons.append(
            "PROTECTED_BLOCKED:" + ",".join(protection.get("reasons", []))
        )

    reversible = reversibility_proof(
        man["source"], output, man["source_sha256"],
        prop.get("output_sha256", "")
    )
    if reversible["status"] != "PASS":
        reasons.append(
            "NONREVERSIBLE:" + str(reversible.get("reason"))
        )

    shadow = shadow_protection_diagnostic(man["source"], output)

    final_state = choose_final_state(reasons)
    executable = final_state == "OK"

    return {
        **prop,
        "execution_state": final_state,
        "executable": executable,
        "legalizer_status": "PASS" if executable else "FAIL",
        "legalizer_reasons": sorted(set(reasons)),
        "protection_status": protection,
        "protected_touch": protection["status"] != "PASS",
        "protection_reasons": protection.get("reasons", []),
        "alignment_status": ambiguity,
        "reversibility_status": reversible,
        "shadow_protection_diagnostic": shadow,
        "legalizer_version": VERSION,
    }


def action_id(uid, source_sha, output_sha, provenance):
    payload = {
        "actionset_version": ACTIONSET_VERSION,
        "uid": uid,
        "source_sha256": source_sha,
        "output_sha256": output_sha,
        "provenance": sorted(
            (p["proposer_id"], p["proposer_version"])
            for p in provenance
        ),
    }
    return sha_json(payload)


def build_action_set(man, legalized, registry_sha):
    source = man["source"]
    source_sha = man["source_sha256"]

    candidates = [{
        "output": source,
        "output_sha256": source_sha,
        "keep_semantics": True,
        "provenance": [{
            "proposer_id": "KEEP",
            "proposer_version": "SYSTEM",
            "family_id": "KEEP",
            "ancestry_id": "KEEP",
        }],
    }]

    for row in legalized:
        if row["uid"] != man["uid"]:
            raise RuntimeError("cross-UID legalized proposal")
        if not row["executable"]:
            continue
        candidates.append({
            "output": row["full_proposer_output"],
            "output_sha256": row["output_sha256"],
            "keep_semantics": False,
            "provenance": [{
                "proposer_id": row["proposer_id"],
                "proposer_version": row["proposer_version"],
                "family_id": row["family_id"],
                "ancestry_id": row["ancestry_id"],
            }],
        })

    dedup = {}
    order = []
    for c in candidates:
        key = c["output"]  # literal exact-text dedup only
        if key not in dedup:
            dedup[key] = {
                "output": c["output"],
                "output_sha256": c["output_sha256"],
                "keep_semantics": c["keep_semantics"],
                "provenance": list(c["provenance"]),
            }
            order.append(key)
        else:
            dedup[key]["keep_semantics"] = (
                dedup[key]["keep_semantics"] or c["keep_semantics"]
            )
            dedup[key]["provenance"].extend(c["provenance"])

    actions = []
    for key in order:
        d = dedup[key]
        d["provenance"] = sorted(
            d["provenance"],
            key=lambda p: (p["proposer_id"], p["proposer_version"])
        )
        actions.append({
            "action_id": action_id(
                man["uid"], source_sha, d["output_sha256"], d["provenance"]
            ),
            "type": "KEEP" if d["keep_semantics"] else "WHOLE_PROPOSER_OUTPUT",
            "output": d["output"],
            "output_sha256": d["output_sha256"],
            "keep_semantics": d["keep_semantics"],
            "provenance": d["provenance"],
        })

    if sum(1 for a in actions if a["keep_semantics"]) != 1:
        raise RuntimeError("KEEP semantic action count != 1")

    return {
        "record_id": ACTIONSET_VERSION,
        "registry_namespace": REGISTRY_NAMESPACE,
        "registry_sha256": registry_sha,
        "uid": man["uid"],
        "case_id": man["case_id"],
        "cluster_id": man["cluster_id"],
        "source": source,
        "source_sha256": source_sha,
        "raw_action_capacity": 1 + len(legalized),
        "unique_action_count": len(actions),
        "actions": actions,
        "gold_reference_consulted": False,
        "quality_scored": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--p1-proposals", required=True)
    ap.add_argument("--p2-proposals", required=True)
    ap.add_argument("--p3-proposals", required=True)
    ap.add_argument(
        "--out-prefix",
        default="MPSEF_V4_STAGE1_LEGAL_ACTIONS_V1",
    )
    args = ap.parse_args()

    packet_path = Path(args.packet)
    registry_path = Path(args.registry)
    packet = read_jsonl(packet_path)
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    reg_by_id = validate_registry(registry)
    registry_sha = sha_file(registry_path)

    if len(packet) != 128 or len({r["cluster_id"] for r in packet}) != 128:
        raise RuntimeError("Stage1 packet identity mismatch")

    p1hist = {
        r["uid"]: r for r in read_jsonl(Path(args.p1_proposals))
    }
    p2 = {
        r["uid"]: r for r in read_jsonl(Path(args.p2_proposals))
    }
    p3 = {
        r["uid"]: r for r in read_jsonl(Path(args.p3_proposals))
    }

    packet_uids = {r["uid"] for r in packet}
    if not packet_uids.issubset(p1hist):
        raise RuntimeError("P1 historical artifact missing Stage1 UID")
    if set(p2) != packet_uids:
        raise RuntimeError("P2 Stage1 UID set mismatch")
    if set(p3) != packet_uids:
        raise RuntimeError("P3 Stage1 UID set mismatch")

    legalized_rows = []
    action_sets = []
    state_counts = Counter()
    shadow_counts = Counter()

    for man in packet:
        uid = man["uid"]
        raw_rows = [
            normalize_p1(
                p1hist[uid], man, reg_by_id[P1_CANONICAL]
            ),
            p2[uid],
            p3[uid],
        ]
        legal = []
        for prop in raw_rows:
            pid = prop["proposer_id"]
            if pid not in reg_by_id:
                raise RuntimeError(f"unregistered proposer: {pid}")
            row = legalize_one(man, prop, reg_by_id[pid])
            legal.append(row)
            legalized_rows.append(row)
            state_counts[f'{pid}:{row["execution_state"]}'] += 1
            shadow_counts[
                row["shadow_protection_diagnostic"]["shadow_status"]
            ] += 1

        action_sets.append(
            build_action_set(man, legal, registry_sha)
        )

    if len(legalized_rows) != 128 * 3:
        raise RuntimeError("legalized row accounting mismatch")
    if len(action_sets) != 128:
        raise RuntimeError("action-set accounting mismatch")

    legal_path = Path(args.out_prefix + "_PROPOSERS.jsonl")
    action_path = Path(args.out_prefix + "_ACTION_SETS.jsonl")
    legal_path.write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False, sort_keys=True)
            for r in legalized_rows
        ) + "\n",
        encoding="utf-8",
    )
    action_path.write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False, sort_keys=True)
            for r in action_sets
        ) + "\n",
        encoding="utf-8",
    )

    sizes = [r["unique_action_count"] for r in action_sets]
    summary = {
        "record_id": "MPSEF_V4_STAGE1_LEGAL_ACTIONS_V1",
        "builder_version": VERSION,
        "status": "SOURCE_ONLY_LEGAL_ACTIONS_READY",
        "cases": 128,
        "clusters": 128,
        "legalized_proposer_rows": len(legalized_rows),
        "state_counts": dict(sorted(state_counts.items())),
        "shadow_status_counts": dict(sorted(shadow_counts.items())),
        "candidate_set_size": {
            "min": min(sizes),
            "max": max(sizes),
            "mean": sum(sizes) / len(sizes),
        },
        "packet_sha256": sha_file(packet_path),
        "registry_sha256": registry_sha,
        "legalized_rows_sha256": sha_file(legal_path),
        "action_sets_sha256": sha_file(action_path),
        "project_source_loaded": True,
        "project_source_scope": "C_F_STAGE1_SOURCE_ONLY",
        "project_gold_loaded": False,
        "reference_content_used": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "v3_artifacts_modified": False,
    }
    Path(args.out_prefix + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
