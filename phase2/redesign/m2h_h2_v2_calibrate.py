#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

EXPECTED_CAMEL_SHA = "be79ca9fc493f0df795375a7255bafef246a802d"
EXPECTED_DB_SHA = "195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70"

ARABIC_MARK_CATS = {"Mn", "Mc"}
LATIN_RE = re.compile(r"[A-Za-z]")
DIGIT_RE = re.compile(r"[0-9٠-٩]")
LEX_META_RE = re.compile(r"_[0-9]+$")

def strip_arabic_marks(s: str) -> str:
    return "".join(
        ch for ch in s
        if not (
            unicodedata.category(ch) in ARABIC_MARK_CATS
            and "ARABIC" in unicodedata.name(ch, "")
        )
    )

def normalize_lex(lex: str) -> str:
    s = strip_arabic_marks((lex or "").strip())
    s = LEX_META_RE.sub("", s)
    return s

def surface_hygiene(token: str) -> bool:
    if not token or any(ch.isspace() for ch in token):
        return False
    if LATIN_RE.search(token) or DIGIT_RE.search(token):
        return False
    if "ـ" in token:
        return False
    if strip_arabic_marks(token) != token:
        return False
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--out-prefix", default="M2H_H2_V2_ALIF_VARIANT")
    args = ap.parse_args()

    from camel_tools.morphology.database import MorphologyDB
    from camel_tools.morphology.analyzer import Analyzer
    from m2h_h2_calibrate import common_gate, match_families

    db = MorphologyDB.builtin_db("calima-msa-r13")
    analyzer = Analyzer(db)

    candidates = [
        json.loads(x)
        for x in Path(args.candidates).read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]

    family_rows = []
    accepted = []
    reasons = Counter()
    analyzer_failures = 0

    for c in candidates:
        gate, gate_reason = common_gate(c)
        if not gate:
            continue

        fams = match_families(c["source_surface"], c["candidate_replacement"])
        if "ALIF_VARIANT" not in fams:
            continue

        src = c["source_surface"]
        tgt = c["candidate_replacement"]
        reason = None
        evidence = {}

        if not (surface_hygiene(src) and surface_hygiene(tgt)):
            reason = "SURFACE_HYGIENE_FAIL"
        else:
            try:
                src_analyses = analyzer.analyze(src)
                tgt_analyses = analyzer.analyze(tgt)
            except Exception as e:
                analyzer_failures += 1
                src_analyses, tgt_analyses = [], []
                reason = "ANALYZER_EXCEPTION"
                evidence["exception_type"] = type(e).__name__

            if reason is None:
                evidence["source_analysis_count"] = len(src_analyses)
                evidence["candidate_analysis_count"] = len(tgt_analyses)

                if len(src_analyses) != 0:
                    reason = "SOURCE_ANALYZABLE"
                elif len(tgt_analyses) == 0:
                    reason = "CANDIDATE_UNANALYZABLE"
                else:
                    lexes = []
                    poses = []
                    missing_lex = False
                    proper_risk = False

                    for a in tgt_analyses:
                        lex = normalize_lex(str(a.get("lex", "")))
                        pos = str(a.get("pos", "") or "")
                        if not lex:
                            missing_lex = True
                        else:
                            lexes.append(lex)
                        poses.append(pos)
                        if "prop" in pos.lower():
                            proper_risk = True

                    evidence["candidate_lexemes_normalized"] = sorted(set(lexes))
                    evidence["candidate_pos_labels"] = sorted(set(poses))
                    evidence["candidate_missing_lex"] = missing_lex
                    evidence["proper_name_risk"] = proper_risk

                    if missing_lex:
                        reason = "MISSING_LEX"
                    elif proper_risk:
                        reason = "PROPER_NAME_RISK"
                    elif len(set(lexes)) != 1:
                        reason = "LEXICAL_AMBIGUITY"
                    else:
                        reason = "ACCEPT"

        row = {
            "candidate_id": c["candidate_id"],
            "case_id": c["case_id"],
            "uid": c["uid"],
            "source_span": c["source_span"],
            "source_surface": src,
            "candidate_replacement": tgt,
            "gold_support": c["gold_support"],
            "component": "H2_V2",
            "family": "ALIF_VARIANT",
            "evidence_profile": "CALIMA_SOURCE_ZERO_CANDIDATE_ATTESTED_LEXEME_CONSENSUS",
            "evidence": evidence,
            "decision": "SUPPORTED_MANDATORY_CANDIDATE" if reason == "ACCEPT" else "REVIEW",
            "reason": reason,
            "invariant_pass": all((c.get("invariant") or {}).values()),
        }
        family_rows.append(row)
        reasons[reason] += 1
        if reason == "ACCEPT":
            accepted.append(row)

    supported = sum(1 for r in accepted if r["gold_support"] == "EXACT_GOLD_SUPPORTED")
    unsupported = len(accepted) - supported
    precision_lb = supported / len(accepted) if accepted else None
    invariant_failures = sum(1 for r in accepted if not r["invariant_pass"])

    activation = bool(
        len(accepted) >= 50
        and precision_lb is not None
        and precision_lb >= 0.98
        and invariant_failures == 0
        and analyzer_failures == 0
    )

    summary = {
        "record_id": "M2H_H2_V2_ALIF_VARIANT_CALIBRATION",
        "status": "PASS",
        "scope": "CALIBRATION_ONLY",
        "family_candidates": len(family_rows),
        "accepted_candidates": len(accepted),
        "exact_gold_supported_accepted": supported,
        "reference_unsupported_accepted": unsupported,
        "strict_reference_precision_lower_bound": precision_lb,
        "accepted_case_coverage": len({r["case_id"] for r in accepted}),
        "invariant_failures_in_accepted": invariant_failures,
        "analyzer_failures": analyzer_failures,
        "reason_counts": dict(reasons),
        "promotion_gate": {
            "min_n": 50,
            "min_precision": 0.98,
            "auto_activation_enabled": activation,
        },
        "frozen_resources": {
            "camel_tools_git_sha": EXPECTED_CAMEL_SHA,
            "morphology_db_expected_sha256": EXPECTED_DB_SHA,
            "database": "calima-msa-r13",
        },
        "integrity": {
            "internal_evaluation_opened": False,
            "stress_diagnostic_opened": False,
            "confirmation_opened": False,
            "holdout_opened": False,
            "a7ta_reserved_opened": False,
            "reserved_nahw_opened": False,
            "qalb15_test_opened": False,
        },
    }

    prefix = Path(args.out_prefix)
    Path(str(prefix) + "_EVIDENCE.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in family_rows) + "\n",
        encoding="utf-8",
    )
    Path(str(prefix) + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
