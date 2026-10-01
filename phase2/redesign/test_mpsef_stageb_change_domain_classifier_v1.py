#!/usr/bin/env python3
from __future__ import annotations

import json

from mpsef_stageb_change_domain_classifier_v1 import (
    VERSION,
    CATEGORIES,
    classify_stageb_change,
)


def check(name, parent, final, expected, results):
    got = classify_stageb_change(parent, final)
    if got != expected:
        raise AssertionError(
            f"{name}: expected={expected} got={got} "
            f"parent={parent!r} final={final!r}"
        )
    results[name] = "PASS"


def main():
    results = {}

    check(
        "IDENTICAL",
        "هذا نص",
        "هذا نص",
        "NO_CHANGE_FROM_P1",
        results,
    )
    check(
        "PUNCTUATION_INSERTION_ONLY",
        "هذا نص",
        "هذا نص.",
        "PUNCTUATION_ONLY_FROM_P1",
        results,
    )
    check(
        "BOUNDARY_INSERTION_ONLY",
        "هذاالنص",
        "هذا النص",
        "BOUNDARY_ONLY_FROM_P1",
        results,
    )
    check(
        "LEXICAL_SUBSTITUTION_ONLY",
        "هذا نص",
        "هذا نصر",
        "LEXICAL_ONLY_FROM_P1",
        results,
    )
    check(
        "MIXED_PUNCTUATION_AND_LEXICAL",
        "هذا نص",
        "هذه نص.",
        "MIXED_FROM_P1",
        results,
    )
    check(
        "UNAVAILABLE_P3",
        "هذا نص",
        None,
        "UNAVAILABLE_COMPARISON",
        results,
    )

    # Additional frozen edge cases.
    check(
        "UNAVAILABLE_PARENT",
        None,
        "هذا نص",
        "UNAVAILABLE_COMPARISON",
        results,
    )
    check(
        "EMPTY_STRINGS_ARE_AVAILABLE",
        "",
        "",
        "NO_CHANGE_FROM_P1",
        results,
    )
    check(
        "ARABIC_COMMA_ONLY",
        "نعم",
        "نعم،",
        "PUNCTUATION_ONLY_FROM_P1",
        results,
    )
    check(
        "SPACE_REMOVAL_ONLY",
        "هذا نص",
        "هذانص",
        "BOUNDARY_ONLY_FROM_P1",
        results,
    )
    check(
        "DIACRITIC_IS_LEXICAL_NOT_PUNCT",
        "كتب",
        "كَتب",
        "LEXICAL_ONLY_FROM_P1",
        results,
    )
    check(
        "PUNCT_AND_SPACE_IS_MIXED",
        "هذا نص",
        "هذا  نص.",
        "MIXED_FROM_P1",
        results,
    )

    if tuple(CATEGORIES) != (
        "NO_CHANGE_FROM_P1",
        "PUNCTUATION_ONLY_FROM_P1",
        "BOUNDARY_ONLY_FROM_P1",
        "LEXICAL_ONLY_FROM_P1",
        "MIXED_FROM_P1",
        "UNAVAILABLE_COMPARISON",
    ):
        raise AssertionError("CATEGORY_ORDER_OR_CONTENT_DRIFT")

    summary = {
        "record_id": VERSION + "_SYNTHETIC_TEST_V1",
        "status": "PASS",
        "test_count": len(results),
        "tests": results,
        "historical_stage1_counts_reinterpreted": False,
        "normalization_applied": False,
        "gold_reference_consulted": False,
        "quality_metric_computed": False,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
