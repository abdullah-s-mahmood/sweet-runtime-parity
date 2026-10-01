#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from mpsef_v4_b02_m01_m03_stage0 import classify_change_domain

VERSION = "MPSEF_V4_STAGE1_DIVERSITY_ANALYZER_V1"
PROPOSERS = (
    "P1_CONTROL_SWEET_QALB14_NOPNX_ITER2",
    "P2_V2_ARABART_GED_MORPH_WORDALIGNED",
    "P3_V1_SWEET_NOPNX2_PNX1",
)
FAMILY = {
    PROPOSERS[0]: "SWEET_QALB14",
    PROPOSERS[1]: "SEQ2SEQ_GED_MORPH",
    PROPOSERS[2]: "SWEET_QALB14",
}
MAX_ALIGNMENT_CELLS = 500000


def read_jsonl(path: Path):
    return [
        json.loads(x)
        for x in path.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def safe_div(n, d):
    return None if d == 0 else n / d


def nearest_rank(values, q):
    if not values:
        return None
    s = sorted(values)
    rank = max(1, math.ceil(q * len(s)))
    return s[rank - 1]


def stats(values):
    if not values:
        return {
            "n": 0, "mean": None, "median": None,
            "p95": None, "max": None,
        }
    s = sorted(values)
    n = len(s)
    median = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    return {
        "n": n,
        "mean": sum(s) / n,
        "median": median,
        "p95": nearest_rank(s, 0.95),
        "max": max(s),
    }


def unique_levenshtein_components(source: str, output: str):
    n, m = len(source), len(output)
    cells = (n + 1) * (m + 1)
    if cells > MAX_ALIGNMENT_CELLS:
        return {"status": "BUDGET_EXCEEDED", "components": None}

    dist = [[0] * (m + 1) for _ in range(n + 1)]
    ways = [[0] * (m + 1) for _ in range(n + 1)]
    ways[0][0] = 1

    for i in range(1, n + 1):
        dist[i][0] = i
        ways[i][0] = 1
    for j in range(1, m + 1):
        dist[0][j] = j
        ways[0][j] = 1

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sub_cost = 0 if source[i - 1] == output[j - 1] else 1
            choices = [
                (dist[i - 1][j] + 1, i - 1, j, "D"),
                (dist[i][j - 1] + 1, i, j - 1, "I"),
                (dist[i - 1][j - 1] + sub_cost, i - 1, j - 1,
                 "M" if sub_cost == 0 else "S"),
            ]
            best = min(x[0] for x in choices)
            dist[i][j] = best
            count = 0
            for cost, pi, pj, _ in choices:
                if cost == best:
                    count = min(2, count + ways[pi][pj])
            ways[i][j] = count

    if ways[n][m] != 1:
        return {
            "status": "AMBIGUOUS",
            "components": None,
            "edit_distance": dist[n][m],
        }

    # Unique global path: backtrack the sole optimal predecessor at each cell.
    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        candidates = []
        if i > 0 and dist[i][j] == dist[i - 1][j] + 1:
            candidates.append((i - 1, j, "D"))
        if j > 0 and dist[i][j] == dist[i][j - 1] + 1:
            candidates.append((i, j - 1, "I"))
        if i > 0 and j > 0:
            cost = 0 if source[i - 1] == output[j - 1] else 1
            if dist[i][j] == dist[i - 1][j - 1] + cost:
                candidates.append((
                    i - 1, j - 1, "M" if cost == 0 else "S"
                ))
        # ways[n][m]==1 implies exactly one predecessor lies on a full optimal
        # path. Use predecessor path-count to select it.
        full = [
            (pi, pj, op)
            for pi, pj, op in candidates
            if ways[pi][pj] == 1
        ]
        if len(full) != 1:
            return {
                "status": "AMBIGUOUS",
                "components": None,
                "edit_distance": dist[n][m],
            }
        pi, pj, op = full[0]
        ops.append((pi, pj, i, j, op))
        i, j = pi, pj
    ops.reverse()

    components = []
    block = None
    for pi, pj, ni, nj, op in ops:
        if op == "M":
            if block is not None:
                components.append(block)
                block = None
            continue

        if block is None:
            block = {
                "source_start": pi,
                "source_end": ni,
                "output_start": pj,
                "output_end": nj,
            }
        else:
            block["source_end"] = ni
            block["output_end"] = nj

    if block is not None:
        components.append(block)

    out = []
    for b in components:
        ss, se = b["source_start"], b["source_end"]
        os, oe = b["output_start"], b["output_end"]
        if ss == se:
            op = "INSERT"
        elif os == oe:
            op = "DELETE"
        else:
            op = "REPLACE"
        out.append({
            "op": op,
            "source_start": ss,
            "source_end": se,
            "replacement": output[os:oe],
        })

    return {
        "status": "UNIQUE",
        "components": out,
        "edit_distance": dist[n][m],
    }


def comp_set(alignment):
    return {
        (
            c["op"], c["source_start"], c["source_end"], c["replacement"]
        )
        for c in alignment["components"]
    }


def index(rows, key):
    out = {}
    for r in rows:
        k = r[key]
        if k in out:
            raise RuntimeError(f"duplicate {key}: {k}")
        out[k] = r
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--legalized-proposers", required=True)
    ap.add_argument("--action-sets", required=True)
    ap.add_argument("--p2-summary", required=True)
    ap.add_argument("--p3-summary", required=True)
    ap.add_argument(
        "--out",
        default="MPSEF_V4_STAGE1_DIVERSITY_SUMMARY_V1.json",
    )
    args = ap.parse_args()

    packet = read_jsonl(Path(args.packet))
    legal = read_jsonl(Path(args.legalized_proposers))
    actions = read_jsonl(Path(args.action_sets))
    p2_summary = json.loads(Path(args.p2_summary).read_text(encoding="utf-8"))
    p3_summary = json.loads(Path(args.p3_summary).read_text(encoding="utf-8"))

    if len(packet) != 128 or len({r["cluster_id"] for r in packet}) != 128:
        raise RuntimeError("packet identity mismatch")

    man = index(packet, "uid")
    aset = index(actions, "uid")
    by_prop = {p: {} for p in PROPOSERS}
    for r in legal:
        p = r["proposer_id"]
        if p not in by_prop:
            raise RuntimeError(f"unexpected proposer: {p}")
        if r["uid"] in by_prop[p]:
            raise RuntimeError(f"duplicate proposer UID: {p}:{r['uid']}")
        by_prop[p][r["uid"]] = r

    for p in PROPOSERS:
        if set(by_prop[p]) != set(man):
            raise RuntimeError(f"proposer population mismatch: {p}")

    per_proposer = {}
    alignments = {p: {} for p in PROPOSERS}
    for p in PROPOSERS:
        state_counts = Counter()
        shadow_counts = Counter()
        changed = legal_n = protected_n = 0
        length_ratios = []
        component_counts = []
        align_states = Counter()
        clusters_legal = set()

        for uid, r in by_prop[p].items():
            state_counts[r["execution_state"]] += 1
            shadow_counts[
                r["shadow_protection_diagnostic"]["shadow_status"]
            ] += 1
            src = man[uid]["source"]
            out = r.get("full_proposer_output") or ""
            changed += int(out != src)
            legal_n += int(r["executable"])
            protected_n += int(r["execution_state"] == "PROTECTED_BLOCKED")
            if r["executable"]:
                clusters_legal.add(man[uid]["cluster_id"])
            length_ratios.append(
                None if len(src) == 0 else len(out) / len(src)
            )
            al = unique_levenshtein_components(src, out)
            alignments[p][uid] = al
            align_states[al["status"]] += 1
            if al["status"] == "UNIQUE":
                component_counts.append(len(al["components"]))

        finite_ratios = [x for x in length_ratios if x is not None]
        per_proposer[p] = {
            "family_id": FAMILY[p],
            "state_counts_D_all": dict(sorted(state_counts.items())),
            "execution_success_count": state_counts["OK"],
            "execution_success_rate_D_all": safe_div(state_counts["OK"], 128),
            "legal_executable_count": legal_n,
            "legal_executable_rate_D_all": safe_div(legal_n, 128),
            "legal_executable_clusters": len(clusters_legal),
            "changed_vs_source_count_D_all": changed,
            "changed_vs_source_rate_D_all": safe_div(changed, 128),
            "protected_blocked_count_D_all": protected_n,
            "protected_blocked_rate_D_all": safe_div(protected_n, 128),
            "shadow_status_counts_D_all": dict(sorted(shadow_counts.items())),
            "alignment_state_counts_D_all": dict(sorted(align_states.items())),
            "output_source_char_ratio": stats(finite_ratios),
            "unique_alignment_component_count": stats(component_counts),
        }

    # Candidate sets reconstructed from legal rows, matching exact whole-output
    # dedup semantics.
    all_outputs = {}
    output_by_prop = {}
    for uid in man:
        output_by_prop[uid] = {}
        source = man[uid]["source"]
        values = {source}
        for p in PROPOSERS:
            r = by_prop[p][uid]
            if r["executable"]:
                values.add(r["full_proposer_output"])
                output_by_prop[uid][p] = r["full_proposer_output"]
        all_outputs[uid] = values

    candidate_sizes = [len(all_outputs[u]) for u in man]
    histogram = Counter(candidate_sizes)

    marginal = {}
    leave_one_out = {}
    for p in PROPOSERS:
        uid_positive = 0
        positive_clusters = set()
        total_unique_outputs = 0
        keep_only_reduction = 0
        keep_only_clusters = set()
        sizes_without = []
        nonkeep_with = nonkeep_without = 0
        cluster_with = set()
        cluster_without = set()

        for uid in man:
            src = man[uid]["source"]
            allset = all_outputs[uid]
            without = {src}
            for q in PROPOSERS:
                if q == p:
                    continue
                if q in output_by_prop[uid]:
                    without.add(output_by_prop[uid][q])

            mc = len(allset) - len(without)
            if mc > 0:
                uid_positive += 1
                positive_clusters.add(man[uid]["cluster_id"])
                total_unique_outputs += mc

            if len(without) == 1 and len(allset) > 1:
                keep_only_reduction += 1
                keep_only_clusters.add(man[uid]["cluster_id"])

            sizes_without.append(len(without))
            if len(allset) > 1:
                nonkeep_with += 1
                cluster_with.add(man[uid]["cluster_id"])
            if len(without) > 1:
                nonkeep_without += 1
                cluster_without.add(man[uid]["cluster_id"])

        marginal[p] = {
            "uids_with_positive_marginal_contribution": uid_positive,
            "clusters_with_positive_marginal_contribution": len(
                positive_clusters
            ),
            "total_unique_legal_outputs_contributed": total_unique_outputs,
            "keep_only_reduction_uids": keep_only_reduction,
            "keep_only_reduction_clusters": len(keep_only_clusters),
        }
        leave_one_out[p] = {
            "candidate_set_size_without": stats(sizes_without),
            "uids_with_nonkeep_all": nonkeep_with,
            "uids_with_nonkeep_without": nonkeep_without,
            "clusters_with_nonkeep_all": len(cluster_with),
            "clusters_with_nonkeep_without": len(cluster_without),
        }

    # Pairwise exact-output and component diagnostics.
    pairwise = {}
    pairs = [
        (PROPOSERS[0], PROPOSERS[1]),
        (PROPOSERS[0], PROPOSERS[2]),
        (PROPOSERS[1], PROPOSERS[2]),
    ]
    for a, b in pairs:
        matrix = Counter()
        joint_exec = []
        equal = 0
        jaccards = []
        comp_equal = 0
        comp_den = 0
        component_state = Counter()

        for uid in man:
            ra, rb = by_prop[a][uid], by_prop[b][uid]
            ea, eb = ra["executable"], rb["executable"]
            matrix[
                "BOTH_EXEC" if ea and eb
                else "A_ONLY_EXEC" if ea
                else "B_ONLY_EXEC" if eb
                else "NEITHER_EXEC"
            ] += 1
            if not (ea and eb):
                continue
            joint_exec.append(uid)
            equal += int(
                ra["full_proposer_output"] == rb["full_proposer_output"]
            )

            aa, ab = alignments[a][uid], alignments[b][uid]
            state = f'{aa["status"]}|{ab["status"]}'
            component_state[state] += 1
            if aa["status"] != "UNIQUE" or ab["status"] != "UNIQUE":
                continue
            ca, cb = comp_set(aa), comp_set(ab)
            union = ca | cb
            j = 1.0 if not union else len(ca & cb) / len(union)
            jaccards.append(j)
            comp_equal += int(ca == cb)
            comp_den += 1

        name = f"{a}__VS__{b}"
        pairwise[name] = {
            "architecture_relation": (
                "RELATED_SAME_FAMILY"
                if FAMILY[a] == FAMILY[b]
                else "HETEROGENEOUS"
            ),
            "D_all_state_matrix": dict(sorted(matrix.items())),
            "D_joint_exec": len(joint_exec),
            "exact_output_equal_count_D_joint_exec": equal,
            "exact_output_equal_rate_D_joint_exec": safe_div(
                equal, len(joint_exec)
            ),
            "exact_output_different_count_D_joint_exec": (
                len(joint_exec) - equal
            ),
            "component_alignment_pair_states": dict(
                sorted(component_state.items())
            ),
            "component_comparable_denominator": comp_den,
            "component_exact_set_equal_count": comp_equal,
            "component_exact_set_equal_rate": safe_div(comp_equal, comp_den),
            "component_jaccard": stats(jaccards),
        }

    # P3 marginal domain relative to source and exact P1 parent.
    p3_domains_from_p1 = Counter()
    p3_domains_from_source = Counter()
    for uid in man:
        p1 = by_prop[PROPOSERS[0]][uid]
        p3 = by_prop[PROPOSERS[2]][uid]
        if p1.get("full_proposer_output") is not None and p3.get(
            "full_proposer_output"
        ) is not None:
            p3_domains_from_p1[
                classify_change_domain(
                    p1["full_proposer_output"],
                    p3["full_proposer_output"],
                )
            ] += 1
            p3_domains_from_source[
                classify_change_domain(
                    man[uid]["source"],
                    p3["full_proposer_output"],
                )
            ] += 1

    # Confirm stored action-set sizes match reconstructed exact-text candidate sets.
    mismatches = []
    stored_sizes = []
    for uid in man:
        if uid not in aset:
            raise RuntimeError(f"missing action set: {uid}")
        stored = aset[uid]["unique_action_count"]
        rebuilt = len(all_outputs[uid])
        stored_sizes.append(stored)
        if stored != rebuilt:
            mismatches.append({
                "uid": uid, "stored": stored, "rebuilt": rebuilt
            })
    if mismatches:
        raise RuntimeError(
            f"candidate-set reconstruction mismatch: {mismatches[:3]}"
        )

    summary = {
        "record_id": "MPSEF_V4_STAGE1_DIVERSITY_SUMMARY_V1",
        "analyzer_version": VERSION,
        "status": "SOURCE_ONLY_DIVERSITY_READY",
        "denominators": {
            "D_all_uids": 128,
            "D_all_clusters": 128,
        },
        "architecture_families": {
            "SWEET_QALB14": [PROPOSERS[0], PROPOSERS[2]],
            "SEQ2SEQ_GED_MORPH": [PROPOSERS[1]],
            "independent_family_count": 2,
        },
        "per_proposer": per_proposer,
        "candidate_set_size": {
            **stats(candidate_sizes),
            "histogram": {
                str(k): histogram[k] for k in sorted(histogram)
            },
            "stored_action_set_size": stats(stored_sizes),
        },
        "marginal_legal_contribution": marginal,
        "source_only_leave_one_proposer_out": leave_one_out,
        "pairwise": pairwise,
        "p3_change_domain": {
            "relative_to_P1_parent": dict(
                sorted(p3_domains_from_p1.items())
            ),
            "relative_to_original_source": dict(
                sorted(p3_domains_from_source.items())
            ),
        },
        "runtime_evidence": {
            "P1": {
                "status": "FROZEN_HISTORICAL_OUTPUT_REUSED",
                "stage1_inference_rerun": False,
            },
            "P2_V2": {
                "elapsed_seconds": p2_summary.get("elapsed_seconds"),
                "state_counts": p2_summary.get("state_counts"),
            },
            "P3_V1": {
                "elapsed_seconds_incremental_pnx": p3_summary.get(
                    "elapsed_seconds"
                ),
                "parity_n": p3_summary.get("parity_n"),
                "parity_match": p3_summary.get("parity_match"),
            },
        },
        "project_source_loaded": True,
        "project_source_scope": "C_F_STAGE1_SOURCE_ONLY",
        "project_gold_loaded": False,
        "reference_content_used": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "selector_trained": False,
        "v4_consensus_generated": False,
        "retention_decision_made": False,
        "internal_evaluation_opened": False,
        "stress_diagnostic_opened": False,
        "reserved_data_opened": False,
    }

    Path(args.out).write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "record_id": summary["record_id"],
        "status": summary["status"],
        "independent_family_count": 2,
        "candidate_set_size": summary["candidate_set_size"],
        "project_gold_loaded": False,
        "quality_metric_computed": False,
        "r_joint_computed": False,
        "retention_decision_made": False,
    }, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
