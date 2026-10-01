#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import time
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

from process_progress_v1 import update_state
from mpsef_executable_actions_legalizer_v1 import (
    protection_proof,
    reversibility_proof,
)
from mpsef_v4_b02_m01_m03_stage0 import shadow_protection_diagnostic

VERSION = "MPSEF_V4_STAGE1_SOURCE_ONLY_ANALYSIS_V1"
ACTIONSET_VERSION = "MPSEF_V4_SOURCE_ONLY_ACTION_SET_V2"
REGISTRY_NAMESPACE = "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A"

EXPECTED_PACKET_SHA = "8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1"
EXPECTED_P1_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P2_SHA = "df89c7dc2c7f177b3c4ca02e8df8a291b6de917a81246c5258f1f66652e1f69e"
EXPECTED_P3_SHA = "69720287154071611a0e0d0af2a6689ef6ed5242acf374fb945de70013a16083"
EXPECTED_REGISTRY_SHA = "b448650c571f6c93dffe4825417e4f65d6a8cd02e33bd9551728ceac2b242b1a"
EXPECTED_CASES = 128

PROPOSERS = {
    "P1": {
        "proposer_id": "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2",
        "proposer_version": "P1_FROZEN_V1",
        "family_id": "SWEET_QALB14",
        "ancestry_id": "SWEET_NOPNX_ITER2",
    },
    "P2": {
        "proposer_id": "P2_V2_ARABART_GED_MORPH_WORDALIGNED",
        "proposer_version": "P2_V2_1",
        "family_id": "SEQ2SEQ_GED_MORPH",
        "ancestry_id": "ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR",
    },
    "P3": {
        "proposer_id": "P3_V1_SWEET_NOPNX2_PNX1",
        "proposer_version": "P3_V1_1",
        "family_id": "SWEET_QALB14",
        "ancestry_id": "P1_CONTROL_PLUS_PNX1",
    },
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def load_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def quantile_nearest_rank(values, q=0.95):
    if not values:
        return None
    vals = sorted(values)
    rank = max(1, math.ceil(q * len(vals)))
    return vals[rank - 1]


def stats(values):
    if not values:
        return {
            "n": 0, "mean": None, "median": None,
            "p95_nearest_rank": None, "max": None,
        }
    return {
        "n": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "p95_nearest_rank": quantile_nearest_rank(values),
        "max": max(values),
    }


def components(source: str, output: str):
    sm = SequenceMatcher(a=source, b=output, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        out.append({
            "op": tag.upper(),
            "source_start": i1,
            "source_end": i2,
            "output_start": j1,
            "output_end": j2,
            "source_text": source[i1:i2],
            "output_text": output[j1:j2],
        })
    return out


def component_key(c):
    return (
        c["op"],
        int(c["source_start"]),
        int(c["source_end"]),
        c["output_text"],
    )


def alignment_state(protection):
    audit = protection.get("optimal_alignment_audit", {})
    reasons = audit.get("reasons", [])
    if audit.get("status") == "ERROR":
        if any("WORK_BUDGET_EXCEEDED" in x for x in reasons):
            return "BUDGET_EXCEEDED"
        return "FAILED"
    if audit.get("ambiguity_affects_legality"):
        return "AMBIGUOUS"
    return "UNIQUE"


def normalize_p1(row, packet_row):
    return {
        "key": "P1",
        "uid": row["uid"],
        "case_id": row["case_id"],
        "cluster_id": row["cluster_id"],
        "source": row["source"],
        "source_sha256": row["source_version_hash"],
        "output": row.get("full_proposer_output"),
        "output_sha256": row.get("output_sha256"),
        "raw_execution_state": (
            "OK" if isinstance(row.get("full_proposer_output"), str)
            and row.get("full_proposer_output") != "" else "EMPTY_OUTPUT"
        ),
        "raw_failure_reasons": (
            [] if isinstance(row.get("full_proposer_output"), str)
            and row.get("full_proposer_output") != ""
            else ["P1_EMPTY_OUTPUT"]
        ),
        "runtime_seconds": None,
        "original": row,
    }


def normalize_p2(row, packet_row):
    return {
        "key": "P2",
        "uid": row["uid"],
        "case_id": row["case_id"],
        "cluster_id": row["cluster_id"],
        "source": row["source"],
        "source_sha256": row["source_sha256"],
        "output": row.get("full_proposer_output"),
        "output_sha256": row.get("output_sha256"),
        "raw_execution_state": row.get("execution_state", "UNKNOWN_FAILURE"),
        "raw_failure_reasons": row.get("failure_reasons", []),
        "runtime_seconds": row.get("runtime_seconds"),
        "original": row,
    }


def normalize_p3(row, packet_row):
    return {
        "key": "P3",
        "uid": row["uid"],
        "case_id": row["case_id"],
        "cluster_id": row["cluster_id"],
        "source": row["source"],
        "source_sha256": row["source_sha256"],
        "output": row.get("full_proposer_output"),
        "output_sha256": row.get("output_sha256"),
        "raw_execution_state": row.get("execution_state", "UNKNOWN_FAILURE"),
        "raw_failure_reasons": row.get("failure_reasons", []),
        "runtime_seconds": row.get("runtime_seconds"),
        "original": row,
    }


def identity_check(rec, packet_row):
    reasons = []
    if rec["uid"] != packet_row["uid"]:
        reasons.append("UID_MISMATCH")
    if rec["case_id"] != packet_row["case_id"]:
        reasons.append("CASE_ID_MISMATCH")
    if rec["cluster_id"] != packet_row["cluster_id"]:
        reasons.append("CLUSTER_ID_MISMATCH")
    if rec["source"] != packet_row["source"]:
        reasons.append("SOURCE_TEXT_MISMATCH")
    if rec["source_sha256"] != packet_row["source_sha256"]:
        reasons.append("SOURCE_SHA_FIELD_MISMATCH")
    if sha_text(packet_row["source"]) != packet_row["source_sha256"]:
        reasons.append("PACKET_SOURCE_SHA_INVALID")

    if isinstance(rec["output"], str):
        if rec["output_sha256"] != sha_text(rec["output"]):
            reasons.append("OUTPUT_SHA_MISMATCH")
    elif rec["raw_execution_state"] == "OK":
        reasons.append("OK_WITHOUT_OUTPUT")

    if rec["key"] == "P3":
        o = rec["original"]
        if o.get("input_sha256") != o.get("parent_output_sha256"):
            reasons.append("P3_PARENT_INPUT_SHA_MISMATCH")
    return reasons


def legalize(rec, packet_row):
    identity_reasons = identity_check(rec, packet_row)
    output = rec["output"]
    source = packet_row["source"]

    legal_reasons = list(identity_reasons)
    protection = None
    shadow = None
    reversible = None
    comps = []
    astate = "NOT_APPLICABLE"

    if rec["raw_execution_state"] != "OK":
        legal_reasons.append(
            "RAW_EXECUTION_STATE:" + str(rec["raw_execution_state"])
        )

    if not isinstance(output, str) or output == "":
        legal_reasons.append("EMPTY_OR_MISSING_OUTPUT")
    else:
        protection = protection_proof(source, output)
        astate = alignment_state(protection)
        comps = components(source, output)
        if protection["status"] != "PASS":
            legal_reasons.extend(
                "PROTECTION:" + x for x in protection.get("reasons", [])
            )
            shadow = shadow_protection_diagnostic(source, output)
        reversible = reversibility_proof(
            source,
            output,
            packet_row["source_sha256"],
            rec["output_sha256"],
        )
        if reversible["status"] != "PASS":
            legal_reasons.append(
                "REVERSIBILITY:" + str(reversible.get("reason"))
            )

    legal = (
        rec["raw_execution_state"] == "OK"
        and not identity_reasons
        and isinstance(output, str)
        and output != ""
        and protection is not None
        and protection["status"] == "PASS"
        and reversible is not None
        and reversible["status"] == "PASS"
    )

    return {
        "legal": legal,
        "legal_reasons": sorted(set(legal_reasons)),
        "identity_reasons": identity_reasons,
        "protection": protection,
        "shadow": shadow,
        "reversibility": reversible,
        "alignment_state": astate,
        "components": comps,
    }


def action_identity(uid, source_sha, output_sha, provenance):
    prov = sorted(
        (p["proposer_id"], p["proposer_version"])
        for p in provenance
    )
    payload = {
        "version": ACTIONSET_VERSION,
        "uid": uid,
        "source_sha256": source_sha,
        "output_sha256": output_sha,
        "provenance": prov,
    }
    return sha_text(json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ))


def build_action_set(packet_row, legalized_by_key):
    source = packet_row["source"]
    source_sha = packet_row["source_sha256"]

    by_output = {
        source: {
            "output": source,
            "output_sha256": source_sha,
            "keep_semantics": True,
            "provenance": [{
                "proposer_id": "KEEP",
                "proposer_version": "SYSTEM",
                "family_id": "KEEP",
                "ancestry_id": "KEEP",
            }],
        }
    }

    raw_legal_proposers = []
    for key in ("P1", "P2", "P3"):
        item = legalized_by_key[key]
        if not item["legalization"]["legal"]:
            continue
        raw_legal_proposers.append(key)
        output = item["normalized"]["output"]
        meta = PROPOSERS[key]
        prov = {
            "proposer_id": meta["proposer_id"],
            "proposer_version": meta["proposer_version"],
            "family_id": meta["family_id"],
            "ancestry_id": meta["ancestry_id"],
        }
        if output not in by_output:
            by_output[output] = {
                "output": output,
                "output_sha256": sha_text(output),
                "keep_semantics": output == source,
                "provenance": [prov],
            }
        else:
            by_output[output]["provenance"].append(prov)
            if output == source:
                by_output[output]["keep_semantics"] = True

    actions = []
    for output, d in by_output.items():
        d["provenance"] = sorted(
            d["provenance"],
            key=lambda p: (p["proposer_id"], p["proposer_version"])
        )
        actions.append({
            "action_id": action_identity(
                packet_row["uid"],
                source_sha,
                d["output_sha256"],
                d["provenance"],
            ),
            "output": d["output"],
            "output_sha256": d["output_sha256"],
            "keep_semantics": d["keep_semantics"],
            "provenance": d["provenance"],
            "family_ids": sorted({
                p["family_id"] for p in d["provenance"]
                if p["family_id"] != "KEEP"
            }),
        })

    actions.sort(key=lambda a: (
        0 if a["keep_semantics"] else 1,
        a["output_sha256"],
    ))
    return {
        "record_id": ACTIONSET_VERSION,
        "uid": packet_row["uid"],
        "case_id": packet_row["case_id"],
        "cluster_id": packet_row["cluster_id"],
        "source_sha256": source_sha,
        "max_raw_action_capacity": 4,
        "raw_legal_proposer_count": len(raw_legal_proposers),
        "unique_action_count": len(actions),
        "actions": actions,
    }


def action_set_without(action_set, proposer_key):
    pid = PROPOSERS[proposer_key]["proposer_id"]
    outputs = []
    for a in action_set["actions"]:
        kept_prov = [
            p for p in a["provenance"]
            if p["proposer_id"] != pid
        ]
        keep_semantics = a["keep_semantics"]
        if keep_semantics:
            kept_prov = [p for p in kept_prov if p["proposer_id"] != pid]
        if keep_semantics or kept_prov:
            outputs.append(a["output"])
    return set(outputs)


def pairwise_summary(rows_by_uid, a, b):
    all_n = len(rows_by_uid)
    state = Counter()
    raw_equal = 0
    raw_diff = 0
    legal_equal = 0
    legal_diff = 0
    component_j = []
    component_equal = 0
    component_den = 0
    align_states = Counter()

    for uid, recs in rows_by_uid.items():
        ra = recs[a]
        rb = recs[b]
        ea = ra["normalized"]["raw_execution_state"] == "OK"
        eb = rb["normalized"]["raw_execution_state"] == "OK"
        la = ra["legalization"]["legal"]
        lb = rb["legalization"]["legal"]

        state[
            ("E" if ea else "F") + ("E" if eb else "F")
        ] += 1

        if ea and eb:
            if ra["normalized"]["output"] == rb["normalized"]["output"]:
                raw_equal += 1
            else:
                raw_diff += 1

        if la and lb:
            if ra["normalized"]["output"] == rb["normalized"]["output"]:
                legal_equal += 1
            else:
                legal_diff += 1

        if ea and eb:
            sa = ra["legalization"]["alignment_state"]
            sb = rb["legalization"]["alignment_state"]
            align_states[f"{sa}|{sb}"] += 1
            if sa == "UNIQUE" and sb == "UNIQUE":
                ca = {
                    component_key(x)
                    for x in ra["legalization"]["components"]
                }
                cb = {
                    component_key(x)
                    for x in rb["legalization"]["components"]
                }
                union = ca | cb
                if not union:
                    j = 1.0
                else:
                    j = len(ca & cb) / len(union)
                component_j.append(j)
                component_den += 1
                if ca == cb:
                    component_equal += 1

    joint_raw = raw_equal + raw_diff
    joint_legal = legal_equal + legal_diff
    return {
        "D_all": all_n,
        "raw_execution_matrix": {
            "both_executable": state["EE"],
            f"{a}_only_executable": state["EF"],
            f"{b}_only_executable": state["FE"],
            "neither_executable": state["FF"],
        },
        "D_joint_raw_exec": joint_raw,
        "raw_exact_equal": raw_equal,
        "raw_exact_different": raw_diff,
        "raw_equality_rate": (
            raw_equal / joint_raw if joint_raw else None
        ),
        "D_joint_legal": joint_legal,
        "legal_exact_equal": legal_equal,
        "legal_exact_different": legal_diff,
        "legal_equality_rate": (
            legal_equal / joint_legal if joint_legal else None
        ),
        "component_alignment_state_pairs": dict(align_states),
        "D_component_unique_pair": component_den,
        "component_exact_set_equality": component_equal,
        "component_exact_set_equality_rate": (
            component_equal / component_den if component_den else None
        ),
        "component_jaccard": stats(component_j),
    }


def burden_summary(items):
    char_ratios = []
    abs_char_delta = []
    abs_token_delta = []
    comp_counts = []
    for item in items:
        n = item["normalized"]
        if n["raw_execution_state"] != "OK":
            continue
        src = n["source"]
        out = n["output"]
        if not isinstance(out, str):
            continue
        char_ratios.append(
            len(out) / len(src) if len(src) else None
        )
        abs_char_delta.append(abs(len(out) - len(src)))
        abs_token_delta.append(
            abs(len(out.split()) - len(src.split()))
        )
        comp_counts.append(len(item["legalization"]["components"]))
    char_ratios = [x for x in char_ratios if x is not None]
    return {
        "output_input_char_ratio": stats(char_ratios),
        "absolute_character_delta": stats(abs_char_delta),
        "absolute_token_delta": stats(abs_token_delta),
        "component_count": stats(comp_counts),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--p1", required=True)
    ap.add_argument("--p2", required=True)
    ap.add_argument("--p3", required=True)
    ap.add_argument("--out-prefix", default="MPSEF_V4_STAGE1")
    ap.add_argument("--progress-state", default="MPSEF_V4_STAGE1_ANALYSIS_PROGRESS.json")
    args = ap.parse_args()

    paths = {
        "packet": Path(args.packet),
        "P1": Path(args.p1),
        "P2": Path(args.p2),
        "P3": Path(args.p3),
    }
    expected = {
        "packet": EXPECTED_PACKET_SHA,
        "P1": EXPECTED_P1_SHA,
        "P2": EXPECTED_P2_SHA,
        "P3": EXPECTED_P3_SHA,
    }
    for key, p in paths.items():
        got = sha_bytes(p.read_bytes())
        if got != expected[key]:
            raise RuntimeError(f"{key}_SHA_MISMATCH:{got}")

    packet = load_jsonl(paths["packet"])
    p1 = load_jsonl(paths["P1"])
    p2 = load_jsonl(paths["P2"])
    p3 = load_jsonl(paths["P3"])

    if len(packet) != EXPECTED_CASES:
        raise RuntimeError(f"PACKET_COUNT_MISMATCH:{len(packet)}")
    if len({r["uid"] for r in packet}) != EXPECTED_CASES:
        raise RuntimeError("PACKET_DUPLICATE_UID")

    packet_by_uid = {r["uid"]: r for r in packet}
    p1_by_uid = {r["uid"]: r for r in p1}
    p2_by_uid = {r["uid"]: r for r in p2}
    p3_by_uid = {r["uid"]: r for r in p3}

    if set(p2_by_uid) != set(packet_by_uid):
        raise RuntimeError("P2_UID_SET_MISMATCH")
    if set(p3_by_uid) != set(packet_by_uid):
        raise RuntimeError("P3_UID_SET_MISMATCH")
    if not set(packet_by_uid).issubset(set(p1_by_uid)):
        raise RuntimeError("P1_MISSING_STAGE1_UID")

    progress_path = Path(args.progress_state)
    update_state(
        progress_path,
        "MPSEF_V4_STAGE1_SOURCE_ONLY_ANALYSIS_V1",
        "LEGALIZE_AND_BUILD",
        0,
        EXPECTED_CASES,
        status="RUNNING",
        message="starting source-only legality/dedup/diversity analysis",
    )

    rows_by_uid = {}
    proposer_rows_out = []
    action_sets = []
    failures = []
    started = time.monotonic()

    for idx, packet_row in enumerate(packet, start=1):
        uid = packet_row["uid"]
        normalized = {
            "P1": normalize_p1(p1_by_uid[uid], packet_row),
            "P2": normalize_p2(p2_by_uid[uid], packet_row),
            "P3": normalize_p3(p3_by_uid[uid], packet_row),
        }

        # P3 must bind to exact frozen P1 parent output for the same UID.
        if p3_by_uid[uid].get("parent_output_sha256") != p1_by_uid[uid].get("output_sha256"):
            raise RuntimeError(f"P3_PARENT_SHA_NOT_P1:{uid}")
        if p3_by_uid[uid].get("input_sha256") != p1_by_uid[uid].get("output_sha256"):
            raise RuntimeError(f"P3_INPUT_SHA_NOT_P1:{uid}")

        recs = {}
        for key in ("P1", "P2", "P3"):
            leg = legalize(normalized[key], packet_row)
            recs[key] = {
                "normalized": normalized[key],
                "legalization": leg,
            }

            meta = PROPOSERS[key]
            outrow = {
                "record_id": "MPSEF_V4_STAGE1_PROPOSER_ROW_V2",
                "registry_namespace": REGISTRY_NAMESPACE,
                "registry_sha256": EXPECTED_REGISTRY_SHA,
                "uid": uid,
                "case_id": packet_row["case_id"],
                "cluster_id": packet_row["cluster_id"],
                "source_sha256": packet_row["source_sha256"],
                "proposer_key": key,
                "proposer_id": meta["proposer_id"],
                "proposer_version": meta["proposer_version"],
                "family_id": meta["family_id"],
                "ancestry_id": meta["ancestry_id"],
                "raw_execution_state": normalized[key]["raw_execution_state"],
                "raw_failure_reasons": normalized[key]["raw_failure_reasons"],
                "output_sha256": normalized[key]["output_sha256"],
                "changed_vs_source": (
                    isinstance(normalized[key]["output"], str)
                    and normalized[key]["output"] != packet_row["source"]
                ),
                "legal": leg["legal"],
                "legal_reasons": leg["legal_reasons"],
                "alignment_state": leg["alignment_state"],
                "component_count": len(leg["components"]),
                "protection_status": (
                    leg["protection"]["status"]
                    if leg["protection"] is not None else None
                ),
                "protection_reasons": (
                    leg["protection"].get("reasons", [])
                    if leg["protection"] is not None else []
                ),
                "shadow_status": (
                    leg["shadow"].get("shadow_status")
                    if leg["shadow"] is not None else None
                ),
                "shadow_causes": (
                    leg["shadow"].get("causes", [])
                    if leg["shadow"] is not None else []
                ),
                "source_only": True,
                "gold_reference_consulted": False,
                "quality_scored": False,
            }
            proposer_rows_out.append(outrow)
            if not leg["legal"]:
                failures.append({
                    "uid": uid,
                    "case_id": packet_row["case_id"],
                    "cluster_id": packet_row["cluster_id"],
                    "proposer_key": key,
                    "proposer_id": meta["proposer_id"],
                    "raw_execution_state": normalized[key]["raw_execution_state"],
                    "legal_reasons": leg["legal_reasons"],
                })

        rows_by_uid[uid] = recs
        action_sets.append(build_action_set(packet_row, recs))

        update_state(
            progress_path,
            "MPSEF_V4_STAGE1_SOURCE_ONLY_ANALYSIS_V1",
            "LEGALIZE_AND_BUILD",
            idx,
            EXPECTED_CASES,
            message=f"uid={uid}",
        )

    # Per-proposer summaries.
    proposer_summary = {}
    for key in ("P1", "P2", "P3"):
        items = [rows_by_uid[uid][key] for uid in packet_by_uid]
        raw_ok = sum(
            x["normalized"]["raw_execution_state"] == "OK"
            for x in items
        )
        legal = sum(x["legalization"]["legal"] for x in items)
        protection_blocked = sum(
            x["legalization"]["protection"] is not None
            and x["legalization"]["protection"]["status"] != "PASS"
            for x in items
        )
        ordinal_only = sum(
            x["legalization"]["shadow"] is not None
            and "GLOBAL_ORDINAL_ONLY_CHANGED"
            in x["legalization"]["shadow"].get("causes", [])
            for x in items
        )
        shadow_would_pass = sum(
            x["legalization"]["shadow"] is not None
            and x["legalization"]["shadow"].get("shadow_status")
            == "V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY"
            for x in items
        )
        reason_presence = Counter()
        shadow_presence = Counter()
        align = Counter()
        for x in items:
            align[x["legalization"]["alignment_state"]] += 1
            if x["legalization"]["protection"] is not None:
                for r in x["legalization"]["protection"].get("reasons", []):
                    reason_presence[r.split(":", 1)[0]] += 1
            if x["legalization"]["shadow"] is not None:
                for r in x["legalization"]["shadow"].get("causes", []):
                    shadow_presence[r] += 1

        runtime_vals = [
            float(x["normalized"]["runtime_seconds"])
            for x in items
            if isinstance(x["normalized"]["runtime_seconds"], (int, float))
        ]

        proposer_summary[key] = {
            "D_all": EXPECTED_CASES,
            "raw_executable": raw_ok,
            "raw_execution_failure": EXPECTED_CASES - raw_ok,
            "legal": legal,
            "nonlegal": EXPECTED_CASES - legal,
            "protection_blocked": protection_blocked,
            "global_ordinal_only_diagnostic": ordinal_only,
            "shadow_would_pass_local_only": shadow_would_pass,
            "alignment_states": dict(align),
            "protection_reason_presence": dict(reason_presence),
            "shadow_cause_presence": dict(shadow_presence),
            "runtime_seconds_per_row": stats(runtime_vals),
            "change_burden": burden_summary(items),
        }

    # Marginal contribution and candidate-set summaries.
    marginal = {
        k: {
            "uid_count": 0,
            "cluster_count": 0,
            "total_unique_legal_outputs": 0,
            "keep_only_reduction_uid_count": 0,
            "keep_only_reduction_cluster_count": 0,
        }
        for k in ("P1", "P2", "P3")
    }
    marginal_clusters = {k: set() for k in marginal}
    keep_clusters = {k: set() for k in marginal}
    candidate_counts = []
    all_nonkeep_uid = 0
    all_nonkeep_clusters = set()

    all_total_unique_actions = 0
    for aset in action_sets:
        uid = aset["uid"]
        cluster = aset["cluster_id"]
        full_outputs = {a["output"] for a in aset["actions"]}
        candidate_counts.append(len(full_outputs))
        all_total_unique_actions += len(full_outputs)
        if len(full_outputs) > 1:
            all_nonkeep_uid += 1
            all_nonkeep_clusters.add(cluster)

        for key in ("P1", "P2", "P3"):
            without = action_set_without(aset, key)
            delta = len(full_outputs) - len(without)
            if delta > 0:
                marginal[key]["uid_count"] += 1
                marginal[key]["total_unique_legal_outputs"] += delta
                marginal_clusters[key].add(cluster)
            if len(without) == 1 and len(full_outputs) > 1:
                marginal[key]["keep_only_reduction_uid_count"] += 1
                keep_clusters[key].add(cluster)

    leave_one_out = {}
    for key in ("P1", "P2", "P3"):
        total_actions = 0
        nonkeep_uid = 0
        nonkeep_clusters = set()
        for aset in action_sets:
            outs = action_set_without(aset, key)
            total_actions += len(outs)
            if len(outs) > 1:
                nonkeep_uid += 1
                nonkeep_clusters.add(aset["cluster_id"])
        leave_one_out[key] = {
            "all_total_unique_actions_sum": all_total_unique_actions,
            "without_total_unique_actions_sum": total_actions,
            "delta_unique_actions_sum": all_total_unique_actions - total_actions,
            "all_uid_with_nonkeep": all_nonkeep_uid,
            "without_uid_with_nonkeep": nonkeep_uid,
            "delta_uid_with_nonkeep": all_nonkeep_uid - nonkeep_uid,
            "all_clusters_with_nonkeep": len(all_nonkeep_clusters),
            "without_clusters_with_nonkeep": len(nonkeep_clusters),
            "delta_clusters_with_nonkeep": (
                len(all_nonkeep_clusters) - len(nonkeep_clusters)
            ),
        }
        marginal[key]["cluster_count"] = len(marginal_clusters[key])
        marginal[key]["keep_only_reduction_cluster_count"] = len(keep_clusters[key])

    hist = Counter(candidate_counts)
    candidate_summary = {
        "D_all": EXPECTED_CASES,
        "mean": statistics.mean(candidate_counts),
        "median": statistics.median(candidate_counts),
        "p95_nearest_rank": quantile_nearest_rank(candidate_counts),
        "max": max(candidate_counts),
        "histogram": {
            "1": hist[1],
            "2": hist[2],
            "3": hist[3],
            "4": hist[4],
            ">4": sum(v for k, v in hist.items() if k > 4),
        },
        "uids_with_nonkeep_legal_candidate": all_nonkeep_uid,
        "clusters_with_nonkeep_legal_candidate": len(all_nonkeep_clusters),
    }

    pairwise = {
        "P1_P2": pairwise_summary(rows_by_uid, "P1", "P2"),
        "P1_P3": pairwise_summary(rows_by_uid, "P1", "P3"),
        "P2_P3": pairwise_summary(rows_by_uid, "P2", "P3"),
    }

    p3_special = {
        "raw_stage_b_domain_counts": dict(Counter(
            p3_by_uid[uid].get("stage_b_domain_from_p1", "UNKNOWN")
            for uid in packet_by_uid
        )),
        "raw_exact_equal_to_p1": sum(
            p3_by_uid[uid].get("full_proposer_output")
            == p1_by_uid[uid].get("full_proposer_output")
            for uid in packet_by_uid
        ),
        "legal_p3_and_nonlegal_p1": sum(
            rows_by_uid[uid]["P3"]["legalization"]["legal"]
            and not rows_by_uid[uid]["P1"]["legalization"]["legal"]
            for uid in packet_by_uid
        ),
        "legal_p1_and_nonlegal_p3": sum(
            rows_by_uid[uid]["P1"]["legalization"]["legal"]
            and not rows_by_uid[uid]["P3"]["legalization"]["legal"]
            for uid in packet_by_uid
        ),
    }

    legalizer_seconds = time.monotonic() - started

    # Write artifacts.
    prefix = args.out_prefix
    proposer_path = Path(prefix + "_PROPOSER_ROWS_V2.jsonl")
    proposer_path.write_text(
        "\n".join(
            json.dumps(x, ensure_ascii=False, sort_keys=True)
            for x in proposer_rows_out
        ) + "\n",
        encoding="utf-8",
    )
    action_path = Path(prefix + "_SOURCE_ONLY_ACTION_SETS_V2.jsonl")
    action_path.write_text(
        "\n".join(
            json.dumps(x, ensure_ascii=False, sort_keys=True)
            for x in action_sets
        ) + "\n",
        encoding="utf-8",
    )
    failure_path = Path(prefix + "_FAILURES_V1.jsonl")
    failure_path.write_text(
        "\n".join(
            json.dumps(x, ensure_ascii=False, sort_keys=True)
            for x in failures
        ) + ("\n" if failures else ""),
        encoding="utf-8",
    )

    summary = {
        "record_id": VERSION,
        "status": "PASS",
        "packet_sha256": EXPECTED_PACKET_SHA,
        "registry_sha256": EXPECTED_REGISTRY_SHA,
        "proposal_input_sha256": {
            "P1": EXPECTED_P1_SHA,
            "P2": EXPECTED_P2_SHA,
            "P3": EXPECTED_P3_SHA,
        },
        "cases": EXPECTED_CASES,
        "clusters": len({r["cluster_id"] for r in packet}),
        "proposer_summary": proposer_summary,
        "source_only_legal_marginal_contribution": marginal,
        "source_only_leave_one_proposer_out": leave_one_out,
        "candidate_set_size": candidate_summary,
        "pairwise_output_diagnostics": pairwise,
        "p3_specific": p3_special,
        "analysis_runtime_seconds": legalizer_seconds,
        "proposer_rows_sha256": sha_bytes(proposer_path.read_bytes()),
        "action_sets_sha256": sha_bytes(action_path.read_bytes()),
        "failures_sha256": sha_bytes(failure_path.read_bytes()),
        "project_source_loaded": True,
        "project_source_scope": "FROZEN_STAGE1_128_ONLY",
        "gold_reference_consulted": False,
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "quality_claimed": False,
        "human_correctness_selection": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
        "reserved_data_opened": False,
    }

    summary_path = Path(prefix + "_DIVERSITY_SUMMARY_V1.json")
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    runtime_path = Path(prefix + "_RUNTIME_V1.json")
    runtime_path.write_text(
        json.dumps({
            "record_id": "MPSEF_V4_STAGE1_RUNTIME_V1",
            "analysis_runtime_seconds": legalizer_seconds,
            "P1_per_row_runtime": "UNAVAILABLE_IN_HISTORICAL_FROZEN_P1_ARTIFACT",
            "P2_per_row_runtime_summary": proposer_summary["P2"]["runtime_seconds_per_row"],
            "P3_incremental_pnx_per_row_runtime_summary": proposer_summary["P3"]["runtime_seconds_per_row"],
            "hardware_comparison_warning": "runner-level times originate from separate workflows; use as engineering cost evidence, not controlled benchmark",
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    update_state(
        progress_path,
        "MPSEF_V4_STAGE1_SOURCE_ONLY_ANALYSIS_V1",
        "COMPLETE",
        EXPECTED_CASES,
        EXPECTED_CASES,
        status="COMPLETE",
        message="Stage1 source-only legality/dedup/diversity analysis complete",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
