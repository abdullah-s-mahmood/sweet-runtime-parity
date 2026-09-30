#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

INFLECT_FEATS = (
    "asp", "cas", "form_gen", "form_num", "gen",
    "mod", "num", "per", "rat", "stt", "vox",
)
CLITIC_FEATS = ("prc3", "prc2", "prc1", "prc0", "enc0")

def token_char_spans(source: str):
    return [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"\S+", source)]

def map_areta_raw_annotations(source: str, annotations):
    """Sequential exact/whitespace-flexible mapping of ARETA raw side to source token spans."""
    src_spans = token_char_spans(source)
    cursor = 0
    mapped = []

    for ann in annotations:
        raw = ann.get("raw", "")
        if not raw:
            mapped.append(None)
            continue

        pos = source.find(raw, cursor)
        end = None

        if pos >= 0:
            end = pos + len(raw)
        else:
            pieces = raw.split()
            if not pieces:
                mapped.append(None)
                continue
            pat = r"\s+".join(re.escape(p) for p in pieces)
            m = re.search(pat, source[cursor:])
            if m is None:
                mapped.append(None)
                continue
            pos = cursor + m.start()
            end = cursor + m.end()

        ids = [
            i for i, (a, b, _) in enumerate(src_spans)
            if not (b <= pos or a >= end)
        ]
        if not ids:
            mapped.append(None)
            continue

        mapped.append({
            "source_span": [min(ids), max(ids) + 1],
            "char_span": [pos, end],
        })
        cursor = end

    return mapped

def retain_lexical(analyses):
    out = []
    for a in analyses:
        if str(a.get("source", "")) != "lex":
            continue
        if not str(a.get("lex", "")).strip():
            continue
        if not str(a.get("pos", "")).strip():
            continue
        out.append(a)
    return out

def one_token(s: str) -> bool:
    return bool(s) and len(s.split()) == 1

def pair_evidence(src_a, tgt_a, has_mt: bool):
    changed = {}
    for feat in INFLECT_FEATS:
        sv = src_a.get(feat)
        tv = tgt_a.get(feat)
        if sv != tv:
            changed[feat] = [sv, tv]

    clitic_changed = {}
    for feat in CLITIC_FEATS:
        sv = src_a.get(feat)
        tv = tgt_a.get(feat)
        if sv != tv:
            clitic_changed[feat] = [sv, tv]

    if clitic_changed:
        return {
            "status": "OUTSIDE_INFLECTION",
            "changed_features": changed,
            "changed_clitics": clitic_changed,
        }

    if not changed:
        return {
            "status": "EMPTY_GRAMMATICAL_DIFFERENCE",
            "changed_features": {},
            "changed_clitics": {},
        }

    names = set(changed)
    if has_mt:
        valid = "asp" in names
    else:
        valid = bool(names - {"asp"})

    return {
        "status": "VALID" if valid else "OUTSIDE_INFLECTION",
        "changed_features": changed,
        "changed_clitics": {},
        "signature": sorted(names),
    }

def evaluate_candidate(analyzer, candidate, codes):
    src = candidate["source_surface"]
    tgt = candidate["candidate_replacement"]

    if not one_token(src) or not one_token(tgt):
        return "REVIEW_OUTSIDE_INFLECTION", {
            "reason": "MULTI_TOKEN_SURFACE",
        }

    if not all((candidate.get("invariant") or {}).values()):
        return "REVIEW_OUTSIDE_INFLECTION", {
            "reason": "CANDIDATE_INVARIANT_FAILURE",
        }

    src_all = analyzer.analyze(src)
    tgt_all = analyzer.analyze(tgt)
    src_analyses = retain_lexical(src_all)
    tgt_analyses = retain_lexical(tgt_all)

    evidence = {
        "source_analysis_count_all": len(src_all),
        "candidate_analysis_count_all": len(tgt_all),
        "source_analysis_count_lex": len(src_analyses),
        "candidate_analysis_count_lex": len(tgt_analyses),
    }

    if not src_analyses or not tgt_analyses:
        evidence["reason"] = "MISSING_RETAINED_LEXICAL_ANALYSIS"
        return "REVIEW_UNANALYZABLE", evidence

    pairs = []
    for sa in src_analyses:
        for ta in tgt_analyses:
            if sa.get("lex") == ta.get("lex") and sa.get("pos") == ta.get("pos"):
                p = pair_evidence(sa, ta, has_mt=("MT" in codes))
                p["lex"] = sa.get("lex")
                p["pos"] = sa.get("pos")
                pairs.append(p)

    evidence["same_lex_pos_pair_count"] = len(pairs)
    if not pairs:
        evidence["reason"] = "NO_SHARED_EXACT_LEX_POS"
        return "REVIEW_NO_STABLE_LEMMA_POS", evidence

    statuses = Counter(p["status"] for p in pairs)
    signatures = {
        tuple(p.get("signature", []))
        for p in pairs if p["status"] == "VALID"
    }
    evidence["pair_status_counts"] = dict(statuses)
    evidence["valid_changed_feature_signatures"] = [list(s) for s in sorted(signatures)]
    evidence["shared_lex_pos_identities"] = sorted({
        (str(p["lex"]), str(p["pos"])) for p in pairs
    })

    if statuses.get("EMPTY_GRAMMATICAL_DIFFERENCE", 0) > 0:
        evidence["reason"] = "EMPTY_AND_OR_MORPHOLOGY_PATH_AMBIGUITY"
        return "REVIEW_AMBIGUOUS", evidence

    if statuses.get("OUTSIDE_INFLECTION", 0) > 0:
        evidence["reason"] = "DISALLOWED_OR_CLITIC_CHANGING_PAIR_EXISTS"
        return "REVIEW_AMBIGUOUS", evidence

    if statuses.get("VALID", 0) == 0:
        evidence["reason"] = "NO_ALLOWED_INFLECTIONAL_PATH"
        return "REVIEW_OUTSIDE_INFLECTION", evidence

    if len(signatures) != 1:
        evidence["reason"] = "MULTIPLE_CHANGED_FEATURE_SIGNATURES"
        return "REVIEW_AMBIGUOUS", evidence

    evidence["reason"] = "CONSENSUS_COMPATIBLE_INFLECTIONAL_PATH"
    return "SUPPORTED_MORPHOLOGY_PROXY", evidence

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--areta-enrichment", required=True)
    ap.add_argument("--h1-inference", required=True)
    ap.add_argument("--h1-candidates", required=True)
    ap.add_argument("--out-prefix", default="M2H_H3_CALIBRATION_V1")
    args = ap.parse_args()

    from camel_tools.morphology.database import MorphologyDB
    from camel_tools.morphology.analyzer import Analyzer

    db = MorphologyDB.builtin_db("calima-msa-r13")
    analyzer = Analyzer(db, backoff="NONE")

    areta = {}
    for line in Path(args.areta_enrichment).read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            areta[r["case_id"]] = r

    inference = {}
    for line in Path(args.h1_inference).read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            inference[r["case_id"]] = r

    candidates = []
    candidate_by_span = defaultdict(list)
    for line in Path(args.h1_candidates).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        c = json.loads(line)
        candidates.append(c)
        candidate_by_span[(c["case_id"], tuple(c["source_span"]))].append(c)

    annotation_counts = Counter()
    code_counts = Counter()
    nominated = []
    decision_counts = Counter()
    supported_rows = []

    for case_id, arow in areta.items():
        source = inference[case_id]["source"]
        annotations = arow["token_annotations"]
        mappings = map_areta_raw_annotations(source, annotations)

        for idx, ann in enumerate(annotations):
            codes = sorted(set(ann.get("codes", [])) & {"MI", "MT"})
            if not codes:
                continue

            annotation_counts["mi_mt_annotations"] += 1
            for code in codes:
                code_counts[f"{code}_annotations"] += 1

            mapping = mappings[idx]
            if mapping is None:
                annotation_counts["mapping_failures"] += 1
                continue

            annotation_counts["mapped_annotations"] += 1
            span = tuple(mapping["source_span"])
            exact_candidates = candidate_by_span.get((case_id, span), [])

            if not exact_candidates:
                annotation_counts["mapped_without_h1_candidate"] += 1
                continue

            annotation_counts["mapped_with_h1_candidate"] += 1

            for c in exact_candidates:
                annotation_counts["nominated_candidates"] += 1
                for code in codes:
                    code_counts[f"{code}_nominated_candidates"] += 1

                disposition, evidence = evaluate_candidate(analyzer, c, codes)
                decision_counts[disposition] += 1

                out = {
                    "candidate_id": c["candidate_id"],
                    "case_id": case_id,
                    "uid": c["uid"],
                    "source_span": c["source_span"],
                    "source_surface": c["source_surface"],
                    "candidate_replacement": c["candidate_replacement"],
                    "areta_nomination_codes": codes,
                    "gold_support": c["gold_support"],
                    "component": "H3",
                    "disposition": disposition,
                    "evidence": evidence,
                    "areta_correct_used_for_decision": False,
                    "h1_confidence_used": False,
                    "invariant_pass": all((c.get("invariant") or {}).values()),
                }
                nominated.append(out)
                if disposition == "SUPPORTED_MORPHOLOGY_PROXY":
                    supported_rows.append(out)

    exact_nominated = [
        r for r in nominated
        if r["gold_support"] == "EXACT_GOLD_SUPPORTED"
    ]
    unsupported_nominated = [
        r for r in nominated
        if r["gold_support"] == "REFERENCE_UNSUPPORTED"
    ]
    exact_supported = [
        r for r in supported_rows
        if r["gold_support"] == "EXACT_GOLD_SUPPORTED"
    ]
    unsupported_supported = [
        r for r in supported_rows
        if r["gold_support"] == "REFERENCE_UNSUPPORTED"
    ]

    recall = (
        len(exact_supported) / len(exact_nominated)
        if exact_nominated else None
    )
    precision_proxy = (
        len(exact_supported) / len(supported_rows)
        if supported_rows else None
    )

    supported_cases = {r["case_id"] for r in supported_rows}
    fp_cases = {
        r["case_id"] for r in unsupported_supported
    }
    fp_case_rate = (
        len(fp_cases) / len(supported_cases)
        if supported_cases else None
    )

    recall_evaluable = len(exact_nominated) >= 20
    fp_evaluable = len(supported_cases) >= 20
    component_supported = bool(
        recall_evaluable
        and fp_evaluable
        and recall is not None
        and recall >= 0.70
        and fp_case_rate is not None
        and fp_case_rate <= 0.10
    )

    summary = {
        "record_id": "M2H_H3_MORPHOLOGY_CALIBRATION_V1",
        "status": "PASS",
        "role": "DEVELOPMENT_PROXY",
        "scope": "CALIBRATION_ONLY",
        "annotation_mapping": {
            **dict(annotation_counts),
            **dict(code_counts),
        },
        "candidate_metrics": {
            "nominated_candidates": len(nominated),
            "exact_reference_supported_nominated": len(exact_nominated),
            "reference_unsupported_nominated": len(unsupported_nominated),
            "supported_morphology_proxy": len(supported_rows),
            "exact_reference_supported_h3_supported": len(exact_supported),
            "reference_unsupported_h3_supported": len(unsupported_supported),
            "supported_cases": len(supported_cases),
            "false_positive_proxy_cases": len(fp_cases),
            "decision_counts": dict(decision_counts),
        },
        "quality_proxy": {
            "candidate_recall": recall,
            "supported_candidate_precision_proxy": precision_proxy,
            "false_positive_case_rate_proxy": fp_case_rate,
            "reference_unsupported_is_proof_of_error": False,
        },
        "frozen_targets": {
            "recall_min": 0.70,
            "false_positive_case_rate_max": 0.10,
            "recall_evaluable": recall_evaluable,
            "false_positive_rate_evaluable": fp_evaluable,
            "component_supported": component_supported,
        },
        "resource_contract": {
            "database": "calima-msa-r13",
            "backoff": "NONE",
            "default_normalization": True,
            "areta_correct_used_for_decision": False,
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
        },
    }

    prefix = Path(args.out_prefix)
    Path(str(prefix) + "_DECISIONS.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in nominated) + ("\n" if nominated else ""),
        encoding="utf-8",
    )
    Path(str(prefix) + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
