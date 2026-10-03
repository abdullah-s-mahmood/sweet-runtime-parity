from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib

PAIR_SHA = "27eaeb6bd6ab1a2b9ef3ff477cfa767c6e8c5526a85dcf9c491f32d8f9ac0460"
CAL_SHA = "40f6c7aa6293b374d4d12d837ed96342d0a8e72d08cc014a115b0be3a54e5a65"

def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(path: pathlib.Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--hhem", required=True)
    ap.add_argument("--deberta", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    pair_path = pathlib.Path(args.pairs)
    cal_path = pathlib.Path(args.calibration)
    h_path = pathlib.Path(args.hhem)
    d_path = pathlib.Path(args.deberta)
    out = pathlib.Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if sha256_file(pair_path) != PAIR_SHA:
        raise RuntimeError("PAIR_MANIFEST_SHA_MISMATCH")
    if sha256_file(cal_path) != CAL_SHA:
        raise RuntimeError("CALIBRATION_SHA_MISMATCH")

    pairs = read_jsonl(pair_path)
    cal = read_jsonl(cal_path)
    h = read_jsonl(h_path)
    d = read_jsonl(d_path)

    if len(pairs) != 462 or len(h) != 462 or len(d) != 462 or len(cal) != 58:
        raise RuntimeError(f"COUNT_MISMATCH pairs={len(pairs)} h={len(h)} d={len(d)} cal={len(cal)}")

    pair_ids = [x["pair_id"] for x in pairs]
    if len(pair_ids) != len(set(pair_ids)):
        raise RuntimeError("DUPLICATE_PAIR_ID")

    hp = {x["pair_id"]: x for x in h}
    dp = {x["pair_id"]: x for x in d}
    if set(hp) != set(pair_ids) or set(dp) != set(pair_ids):
        raise RuntimeError("RAW_SCORE_PAIR_SET_MISMATCH")

    cal_by_id = {x["calibration_id"]: x for x in cal}
    if len(cal_by_id) != 58:
        raise RuntimeError("DUPLICATE_CALIBRATION_ID")

    grouped = collections.defaultdict(list)
    for p in pairs:
        grouped[p["calibration_id"]].append(p)

    features = []
    for calibration_id, row in sorted(cal_by_id.items()):
        group = grouped.get(calibration_id, [])
        if not group:
            raise RuntimeError(f"NO_PAIRS_FOR:{calibration_id}")
        s2c = [p for p in group if p["direction"] == "SOURCE_TO_CANDIDATE"]
        c2s = [p for p in group if p["direction"] == "CANDIDATE_TO_SOURCE"]
        if not s2c or not c2s:
            raise RuntimeError(f"MISSING_DIRECTION:{calibration_id}")
        def vals(items, source, key):
            result = []
            for p in items:
                v = source[p["pair_id"]].get(key)
                if not isinstance(v, (int, float)):
                    raise RuntimeError(f"MISSING_SCORE:{p['pair_id']}:{key}")
                result.append(float(v))
            return result
        feat = {
            "calibration_id": calibration_id,
            "case_id": row["case_id"],
            "gold_label": row["label"],
            "h_s2c_min": min(vals(s2c, hp, "consistency_score")),
            "h_c2s_min": min(vals(c2s, hp, "consistency_score")),
            "e_s2c_min": min(vals(s2c, dp, "entailment_probability")),
            "e_c2s_min": min(vals(c2s, dp, "entailment_probability")),
            "c_s2c_max": max(vals(s2c, dp, "contradiction_probability")),
            "c_c2s_max": max(vals(c2s, dp, "contradiction_probability")),
            "source_to_candidate_pairs": len(s2c),
            "candidate_to_source_pairs": len(c2s),
        }
        features.append(feat)

    if sum(x["gold_label"] == "SAFE" for x in features) != 22:
        raise RuntimeError("SAFE_DENOMINATOR_MISMATCH")
    if sum(x["gold_label"] == "ADVERSARIAL" for x in features) != 36:
        raise RuntimeError("ADVERSARIAL_DENOMINATOR_MISMATCH")

    def verified(f, th, te, tc):
        return (
            f["h_s2c_min"] >= th
            and f["h_c2s_min"] >= th
            and f["e_s2c_min"] >= te
            and f["e_c2s_min"] >= te
            and f["c_s2c_max"] <= tc
            and f["c_c2s_max"] <= tc
        )

    candidates = []
    grid = [i / 20.0 for i in range(1, 20)]
    for th in grid:
        for te in grid:
            for tc in grid:
                safe_pass = sum(verified(f, th, te, tc) for f in features if f["gold_label"] == "SAFE")
                adversarial_pass = sum(verified(f, th, te, tc) for f in features if f["gold_label"] == "ADVERSARIAL")
                if adversarial_pass == 0:
                    candidates.append({
                        "t_h": th,
                        "t_e": te,
                        "t_c": tc,
                        "safe_verified": safe_pass,
                        "adversarial_auto_pass": adversarial_pass,
                        "conservatism": round(th + te - tc, 10),
                    })

    selected = None
    if candidates:
        selected = max(
            candidates,
            key=lambda x: (
                x["safe_verified"],
                x["conservatism"],
                x["t_h"],
                x["t_e"],
                -x["t_c"],
            ),
        )

    selected_rows = []
    scientific_status = "SCIENTIFIC_FAIL"
    if selected is not None:
        for f in features:
            row = dict(f)
            row["semantic_disposition"] = "VERIFIED_FOR_REVIEW" if verified(
                f, selected["t_h"], selected["t_e"], selected["t_c"]
            ) else "REVIEW"
            selected_rows.append(row)
        if selected["safe_verified"] >= 16 and selected["adversarial_auto_pass"] == 0:
            scientific_status = "SCIENTIFIC_PASS"
    else:
        selected_rows = [dict(f, semantic_disposition="REVIEW") for f in features]

    safe_verified = sum(
        x["gold_label"] == "SAFE" and x["semantic_disposition"] == "VERIFIED_FOR_REVIEW"
        for x in selected_rows
    )
    adversarial_auto_pass = sum(
        x["gold_label"] == "ADVERSARIAL" and x["semantic_disposition"] == "VERIFIED_FOR_REVIEW"
        for x in selected_rows
    )

    features_path = out / "PARAGRAPH_SEMANTIC_FEATURES_V1.jsonl"
    features_path.write_text(
        "".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in selected_rows),
        encoding="utf-8",
    )

    search_summary = {
        "grid_values_each_axis": 19,
        "tuples_evaluated": 19 ** 3,
        "eligible_zero_adversarial_tuples": len(candidates),
        "selection_rule_frozen_before_scores": True,
        "selected": selected,
    }
    (out / "THRESHOLD_SEARCH_V1.json").write_text(
        json.dumps(search_summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    summary = {
        "gate": "AT0_EN_V2_4_DEVELOPMENT_SEMANTIC_CALIBRATION_V1",
        "technical_status": "PASS",
        "scientific_status": scientific_status,
        "calibration_population_sha256": sha256_file(cal_path),
        "pair_manifest_sha256": sha256_file(pair_path),
        "hhem_raw_scores_sha256": sha256_file(h_path),
        "deberta_raw_scores_sha256": sha256_file(d_path),
        "paragraphs": 58,
        "safe_total": 22,
        "adversarial_total": 36,
        "safe_verified_for_review": safe_verified,
        "safe_verified_coverage": safe_verified / 22.0,
        "adversarial_auto_pass": adversarial_auto_pass,
        "adversarial_auto_pass_rate": adversarial_auto_pass / 36.0,
        "selected_thresholds": selected,
        "required_safe_verified_min": 16,
        "required_adversarial_auto_pass": 0,
        "confirmation_population_accessed": False,
        "new_generator_inference": False,
        "threshold_protocol_changed_after_scores": False,
    }
    summary_path = out / "SEMANTIC_CALIBRATION_SUMMARY_V1.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
