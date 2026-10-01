#!/usr/bin/env python3
from __future__ import annotations

import difflib
import unicodedata

VERSION = "MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1"

CATEGORIES = (
    "NO_CHANGE_FROM_P1",
    "PUNCTUATION_ONLY_FROM_P1",
    "BOUNDARY_ONLY_FROM_P1",
    "LEXICAL_ONLY_FROM_P1",
    "MIXED_FROM_P1",
    "UNAVAILABLE_COMPARISON",
)


def _char_class(ch: str) -> str:
    if ch.isspace():
        return "SPACE"
    if unicodedata.category(ch).startswith("P"):
        return "PUNCT"
    return "LEXICAL"


def classify_stageb_change(parent_output, p3_output) -> str:
    """
    Frozen Stage-B classifier.

    Comparison is exact P1 parent output -> P3 final output.
    No normalization is performed.
    """
    if parent_output is None or p3_output is None:
        return "UNAVAILABLE_COMPARISON"

    if not isinstance(parent_output, str) or not isinstance(p3_output, str):
        return "UNAVAILABLE_COMPARISON"

    if parent_output == p3_output:
        return "NO_CHANGE_FROM_P1"

    classes = set()
    sm = difflib.SequenceMatcher(
        a=parent_output,
        b=p3_output,
        autojunk=False,
    )
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        for ch in parent_output[i1:i2] + p3_output[j1:j2]:
            classes.add(_char_class(ch))

    if classes == {"PUNCT"}:
        return "PUNCTUATION_ONLY_FROM_P1"
    if classes == {"SPACE"}:
        return "BOUNDARY_ONLY_FROM_P1"
    if classes == {"LEXICAL"}:
        return "LEXICAL_ONLY_FROM_P1"

    # Any multi-class edit set is MIXED. An empty changed-class set should
    # be unreachable for unequal strings, but fails closed as MIXED rather
    # than inventing a new semantic category.
    return "MIXED_FROM_P1"
