"""Second-pass development diagnostics for targeted correction recovery.

This intentionally does NOT treat Nahw one-target references as fully corrected passages.
It relaxes the first-pass alignment rule: the published target itself may be recovered even
when adjacent context is also edited.
"""
import argparse, json, difflib, collections
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

STAGES = {
    "nopnx_iteration_1": lambda r: r["nopnx_iteration_1"]["output"],
    "nopnx_iteration_2": lambda r: r["nopnx_iteration_2"]["output"],
    "pnx_only": lambda r: r["pnx_only"]["output"],
    "full": lambda r: r["full_pnx_iteration_1"]["output"],
}

def equal_coverage(ref, out, a, b):
    """Return number of target-reference characters covered by equal alignment blocks."""
    if a == b:
        return 0
    sm = difflib.SequenceMatcher(None, ref, out, autojunk=False)
    covered = 0
    blocks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            continue
        ov1, ov2 = max(a, i1), min(b, i2)
        if ov1 < ov2:
            covered += ov2 - ov1
            blocks.append((i1, i2, j1, j2))
    return covered, blocks

def approximate_output_pos(ref, out, pos):
    sm = difflib.SequenceMatcher(None, ref, out, autojunk=False)
    last_i = last_j = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if i1 <= pos <= i2:
            if tag == "equal":
                return j1 + max(0, min(pos - i1, j2 - j1))
            if i2 > i1:
                frac = (pos - i1) / (i2 - i1)
                return round(j1 + frac * (j2 - j1))
            return j1
        last_i, last_j = i2, j2
    return last_j + max(0, pos - last_i)

def classify(row, out):
    src = row["source"]
    ref = row["reference"]
    err = row["target_error"]
    corr = row["target_correction"]
    a = row["target_start"]
    b = a + len(corr)

    if out == src:
        return "UNCHANGED_SOURCE"

    if corr:
        covered, _ = equal_coverage(ref, out, a, b)
        if covered == len(corr):
            return "RECOVERED_EXACT_ALIGNED"

        predicted = approximate_output_pos(ref, out, a)
        radius = max(16, len(corr) * 3)
        lo, hi = max(0, predicted - radius), min(len(out), predicted + len(corr) + radius)
        local = out[lo:hi]
        if corr in local:
            return "RECOVERED_EXACT_LOCAL"
    else:
        # Generic deletion target support if future cases contain empty correction strings.
        predicted = approximate_output_pos(src, out, row["target_start"])
        radius = max(16, len(err) * 3)
        local = out[max(0, predicted-radius):min(len(out), predicted+radius)]
        if err not in local:
            return "RECOVERED_DELETION_LOCAL"

    predicted_src = approximate_output_pos(src, out, row["target_start"])
    radius = max(16, len(err) * 3, len(corr) * 3)
    local_src = out[max(0, predicted_src-radius):min(len(out), predicted_src+max(len(err),len(corr))+radius)]
    if err and err in local_src:
        return "ERROR_PRESERVED_LOCAL"
    return "TARGET_CHANGED_OTHER"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=ROOT/"artifacts/OFFICIAL_DEVELOPMENT_RAW.jsonl")
    ap.add_argument("--output", type=Path, default=ROOT/"artifacts/TARGET_RECOVERY_V2.json")
    args = ap.parse_args()

    rows = [json.loads(x) for x in args.raw.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 150
    assert len({x["passage_id"] for x in rows}) == 41

    cases = []
    summaries = {}
    for row in rows:
        item = {
            "case_id": row["case_id"],
            "target_id": row["target_id"],
            "passage_id": row["passage_id"],
            "category_hint": row["category_hint"],
            "target_error": row["target_error"],
            "target_correction": row["target_correction"],
            "stages": {},
        }
        for name, getout in STAGES.items():
            out = getout(row)
            item["stages"][name] = {
                "state": classify(row, out),
                "output_changed_from_source": out != row["source"],
                "output_exact_single_target_reference": out == row["reference"],
            }
        cases.append(item)

    for name in STAGES:
        states = collections.Counter(x["stages"][name]["state"] for x in cases)
        recovered = sum(v for k,v in states.items() if k.startswith("RECOVERED_"))
        changed = sum(x["stages"][name]["output_changed_from_source"] for x in cases)
        exact_ref = sum(x["stages"][name]["output_exact_single_target_reference"] for x in cases)
        by_cat = {}
        for cat in sorted({x["category_hint"] for x in cases}):
            subset = [x for x in cases if x["category_hint"] == cat]
            cat_states = collections.Counter(x["stages"][name]["state"] for x in subset)
            cat_recovered = sum(v for k,v in cat_states.items() if k.startswith("RECOVERED_"))
            by_cat[cat] = {
                "n": len(subset),
                "recovered": cat_recovered,
                "recovery_rate": cat_recovered/len(subset) if subset else None,
                "states": dict(cat_states),
            }
        summaries[name] = {
            "n_targets": len(cases),
            "n_passages": 41,
            "states": dict(states),
            "recovered": recovered,
            "targeted_recovery_rate": recovered/len(cases),
            "output_changed_from_source_targets": changed,
            "exact_single_target_reference_matches": exact_ref,
            "by_category_hint": by_cat,
        }

    # Stage contribution comparisons.
    gains = {
        "iteration2_gained_targets_over_iteration1": [],
        "iteration2_lost_targets_vs_iteration1": [],
        "full_gained_targets_over_nopnx2": [],
        "full_lost_targets_vs_nopnx2": [],
    }
    def isrec(state): return state.startswith("RECOVERED_")
    for x in cases:
        r1 = isrec(x["stages"]["nopnx_iteration_1"]["state"])
        r2 = isrec(x["stages"]["nopnx_iteration_2"]["state"])
        rf = isrec(x["stages"]["full"]["state"])
        if r2 and not r1: gains["iteration2_gained_targets_over_iteration1"].append(x["case_id"])
        if r1 and not r2: gains["iteration2_lost_targets_vs_iteration1"].append(x["case_id"])
        if rf and not r2: gains["full_gained_targets_over_nopnx2"].append(x["case_id"])
        if r2 and not rf: gains["full_lost_targets_vs_nopnx2"].append(x["case_id"])

    output = {
        "status": "DEVELOPMENT_DIAGNOSTIC_V2_NOT_FINAL_ADJUDICATION",
        "metric": "TARGETED_CORRECTION_RECOVERY",
        "cluster_unit": "passage_id",
        "important_limit": "One-target Nahw references are not fully corrected passages; exact-reference match is diagnostic only.",
        "summaries": summaries,
        "stage_contribution": gains,
        "cases": cases,
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

    compact = {
        name: {
            "recovered": s["recovered"],
            "rate": round(s["targeted_recovery_rate"], 6),
            "states": s["states"],
            "by_category": {k: {"n":v["n"],"recovered":v["recovered"],"rate":round(v["recovery_rate"],6)} for k,v in s["by_category_hint"].items()},
        } for name,s in summaries.items()
    }
    print(json.dumps({"summary_v2": compact, "stage_contribution": gains}, ensure_ascii=False))

if __name__ == "__main__":
    main()
