#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

FAMILIES = [
    "HAMZA_ALIF_SEAT",
    "ALIF_MAQSURA_YA",
    "TA_MARBUTA_HA",
    "ALIF_VARIANT",
    "SINGLE_ARABIC_LETTER_ORTHOGRAPHIC",
    "DIACRITIC_ONLY",
    "TATWEEL_ONLY",
]

HAMZA_SEAT = set("ءأإؤئ")
ALIF_VARIANTS = set("ا أ إ آ ٱ".split())
ALIF_VARIANTS = set().union(*[set(x) for x in ALIF_VARIANTS])
TATWEEL = "ـ"

def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s or "")

def is_arabic_cp(ch: str) -> bool:
    cp = ord(ch)
    return (
        0x0600 <= cp <= 0x06FF
        or 0x0750 <= cp <= 0x077F
        or 0x08A0 <= cp <= 0x08FF
        or 0xFB50 <= cp <= 0xFDFF
        or 0xFE70 <= cp <= 0xFEFF
    )

def is_arabic_letter(ch: str) -> bool:
    return is_arabic_cp(ch) and unicodedata.category(ch).startswith("L")

def is_arabic_mark(ch: str) -> bool:
    return (
        is_arabic_cp(ch)
        and unicodedata.category(ch) in {"Mn", "Mc"}
        and unicodedata.name(ch, "").startswith("ARABIC")
    )

def strip_arabic_marks(s: str) -> str:
    return "".join(ch for ch in s if not is_arabic_mark(ch))

def single_substitution(src: str, tgt: str):
    src, tgt = nfc(src), nfc(tgt)
    if len(src) != len(tgt) or src == tgt:
        return None
    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(src, tgt)) if a != b]
    return diffs[0] if len(diffs) == 1 else None

def common_gate(c):
    src = nfc(c.get("source_surface", ""))
    tgt = nfc(c.get("candidate_replacement", ""))
    if not src or not tgt:
        return False, "EMPTY_SIDE"
    if " " in src or " " in tgt:
        return False, "WHITESPACE_OR_MULTI_TOKEN"
    if c.get("derived_operation") in {"PURE_SPLIT", "PURE_MERGE", "INSERT", "DELETE", "REPLACE_BLOCK"}:
        return False, "NON_LOCAL_OPERATION"
    if not c.get("contains_arabic", False):
        return False, "NO_ARABIC"
    inv = c.get("invariant") or {}
    if not all(inv.values()):
        return False, "EXTRACTION_INVARIANT"
    return True, None

def match_families(src: str, tgt: str):
    src, tgt = nfc(src), nfc(tgt)
    out = []
    sub = single_substitution(src, tgt)

    if sub:
        _, a, b = sub
        pair = {a, b}
        if a in HAMZA_SEAT and b in HAMZA_SEAT:
            out.append("HAMZA_ALIF_SEAT")
        if pair == {"ى", "ي"}:
            out.append("ALIF_MAQSURA_YA")
        if pair == {"ة", "ه"}:
            out.append("TA_MARBUTA_HA")
        if a in ALIF_VARIANTS and b in ALIF_VARIANTS and (a in {"ا","آ","ٱ"} or b in {"ا","آ","ٱ"}):
            out.append("ALIF_VARIANT")
        if is_arabic_letter(a) and is_arabic_letter(b):
            out.append("SINGLE_ARABIC_LETTER_ORTHOGRAPHIC")

    if src != tgt and strip_arabic_marks(src) == strip_arabic_marks(tgt):
        out.append("DIACRITIC_ONLY")

    if src != tgt and src.replace(TATWEEL, "") == tgt.replace(TATWEEL, ""):
        out.append("TATWEEL_ONLY")

    return out

def load_areta(path: Path | None):
    if path is None:
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        out[r["case_id"]] = sorted(set(r.get("areta_codes", [])))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--areta-enrichment")
    ap.add_argument("--out-prefix", default="M2H_H2_CALIBRATION_V1")
    args = ap.parse_args()

    candidates = [json.loads(x) for x in Path(args.candidates).read_text(encoding="utf-8").splitlines() if x.strip()]
    areta = load_areta(Path(args.areta_enrichment) if args.areta_enrichment else None)

    metrics = {
        f: {
            "candidates": 0,
            "exact_gold_supported": 0,
            "reference_unsupported": 0,
            "case_ids": set(),
            "invariant_violations": 0,
        } for f in FAMILIES
    }

    disposition_rows = []
    out_of_scope = Counter()
    family_overlap = Counter()

    for c in candidates:
        gate, reason = common_gate(c)
        families = []
        if gate:
            families = match_families(c["source_surface"], c["candidate_replacement"])
        else:
            out_of_scope[reason] += 1

        family_overlap[len(families)] += 1

        for f in families:
            m = metrics[f]
            m["candidates"] += 1
            m["case_ids"].add(c["case_id"])
            if c.get("gold_support") == "EXACT_GOLD_SUPPORTED":
                m["exact_gold_supported"] += 1
            else:
                m["reference_unsupported"] += 1
            if not all((c.get("invariant") or {}).values()):
                m["invariant_violations"] += 1

        disposition_rows.append({
            "candidate_id": c["candidate_id"],
            "case_id": c["case_id"],
            "uid": c["uid"],
            "source_span": c["source_span"],
            "source_surface": c["source_surface"],
            "candidate_replacement": c["candidate_replacement"],
            "derived_operation": c["derived_operation"],
            "gold_support": c["gold_support"],
            "h2_common_gate": gate,
            "h2_gate_reason": reason,
            "h2_families": families,
            "areta_codes": areta.get(c["case_id"], []),
            "disposition": (
                "REVIEW_DIAGNOSTIC_ONLY"
                if any(f in {"DIACRITIC_ONLY", "TATWEEL_ONLY"} for f in families)
                else ("FAMILY_ELIGIBLE_FOR_METRIC" if families else "OUT_OF_SCOPE")
            ),
        })

    fam_summary = {}
    for f, m in metrics.items():
        n = m["candidates"]
        lower = (m["exact_gold_supported"] / n) if n else None
        diagnostic_only = f in {"DIACRITIC_ONLY", "TATWEEL_ONLY"}
        enabled = bool(
            n > 0
            and not diagnostic_only
            and lower is not None
            and lower >= 0.98
            and m["invariant_violations"] == 0
        )
        fam_summary[f] = {
            "candidates": n,
            "exact_gold_supported": m["exact_gold_supported"],
            "reference_unsupported": m["reference_unsupported"],
            "strict_reference_precision_lower_bound": lower,
            "case_coverage": len(m["case_ids"]),
            "candidate_coverage": n / len(candidates) if candidates else None,
            "invariant_violations": m["invariant_violations"],
            "diagnostic_only": diagnostic_only,
            "auto_promotion_enabled": enabled,
            "promotion_reason": (
                "ENABLED_CONSERVATIVE_LOWER_BOUND"
                if enabled
                else (
                    "DIAGNOSTIC_ONLY"
                    if diagnostic_only
                    else ("NO_CANDIDATES" if n == 0 else "LOWER_BOUND_BELOW_98_OR_INVARIANT_FAILURE")
                )
            )
        }

    summary = {
        "record_id": "M2H_H2_CALIBRATION_V1",
        "status": "PASS",
        "scope": "CALIBRATION_ONLY",
        "input_candidates": len(candidates),
        "families": fam_summary,
        "out_of_scope_reasons": dict(out_of_scope),
        "family_match_count_distribution": {str(k): v for k, v in sorted(family_overlap.items())},
        "areta_attached": bool(areta),
        "scientific_interpretation": {
            "precision_metric_role": "CONSERVATIVE_SINGLE_REFERENCE_LOWER_BOUND",
            "reference_unsupported_is_automatically_wrong": False,
            "h1_confidence_used": False,
        },
        "integrity": {
            "internal_evaluation_opened": False,
            "stress_diagnostic_opened": False,
            "confirmation_opened": False,
            "holdout_opened": False,
            "a7ta_reserved_opened": False,
            "reserved_nahw_opened": False,
            "qalb15_test_opened": False,
        }
    }

    prefix = Path(args.out_prefix)
    Path(str(prefix) + "_DECISIONS.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in disposition_rows) + "\n",
        encoding="utf-8"
    )
    Path(str(prefix) + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
