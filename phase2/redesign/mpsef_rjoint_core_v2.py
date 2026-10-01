#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib
import string
import sys
import unicodedata
from pathlib import Path

MATCHING_VERSION = "MPSEF_RJOINT_M2_EVALUATION_MATCH_V2"
FAMILY_MAP_VERSION = "MPSEF_TARGET_FAMILY_MAP_V2"

UNICODE_PUNCT_SYMBOL = frozenset(
    chr(i) for i in range(0x110000)
    if unicodedata.category(chr(i))[0] in {"P", "S"}
)
PNX_SET = frozenset(string.punctuation) | UNICODE_PUNCT_SYMBOL

FAMILIES = ("INSERT", "DELETE", "SPLIT", "MERGE", "SUBSTITUTE", "COMPLEX")

def norm(s):
    return " ".join((s or "").strip().split())

def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def pnx_chars(s):
    return "".join(ch for ch in (s or "") if ch in PNX_SET)

def lexical_chars(s):
    return "".join(
        ch for ch in (s or "")
        if ch not in PNX_SET and not ch.isspace()
    )

def lexical_tokens(s):
    out = []
    for raw in (s or "").split():
        cleaned = "".join(ch for ch in raw if ch not in PNX_SET)
        if cleaned:
            out.append(cleaned)
    return out

def target_scope(original, correction):
    pchg = pnx_chars(original) != pnx_chars(correction)
    lexical_changed = lexical_chars(original) != lexical_chars(correction)
    boundary_changed = lexical_tokens(original) != lexical_tokens(correction)
    linguistic_changed = lexical_changed or boundary_changed

    if pchg and not linguistic_changed:
        return "PUNCTUATION_ONLY"
    if pchg and linguistic_changed:
        return "MIXED_PUNCT_LINGUISTIC"
    return "LINGUISTIC"

def target_family(start, end, original, correction):
    src = lexical_tokens(original)
    cor = lexical_tokens(correction)

    if start == end and correction:
        return "INSERT"
    if start < end and not correction:
        return "DELETE"

    if start < end and len(src) == 1 and len(cor) > 1 and "".join(src) == "".join(cor):
        return "SPLIT"
    if start < end and len(src) > 1 and len(cor) == 1 and "".join(src) == "".join(cor):
        return "MERGE"
    if start < end and correction and len(src) == len(cor):
        return "SUBSTITUTE"
    return "COMPLEX"

def import_m2(upstream_root):
    sys.path.insert(0, str(Path(upstream_root).resolve()))
    m2 = importlib.import_module("gec.utils.m2scorer.m2scorer")
    lev = importlib.import_module("gec.utils.m2scorer.levenshtein")
    return m2, lev

def evaluation_edit_seq_m2(lev, candidate, source, gold, max_unchanged_words=2):
    """Gold-aware M2 path selection used ONLY for evaluation.

    This function MUST NOT be called by the source-only legalizer and MUST NOT
    create, delete, split, repair, or reclassify executable actions.
    """
    ct, st = candidate.split(), source.split()
    l1, b1 = lev.levenshtein_matrix(st, ct, 1, 1, 1)
    l2, b2 = lev.levenshtein_matrix(st, ct, 1, 1, 2)
    v1, e1, d1, x1 = lev.edit_graph(l1, b1)
    v2, e2, d2, x2 = lev.edit_graph(l2, b2)
    V, E, dist, edits = lev.merge_graph(v1, v2, e1, e2, d1, d2, x1, x2)
    V, E, dist, edits = lev.transitive_arcs(
        V, E, dist, edits, max_unchanged_words, False
    )
    local = lev.set_weights(E, dist, edits, gold, False, False)
    return lev.best_edit_seq_bf(V, E, local, edits, False)

def matched_indices(lev, edit_seq, gold):
    out = []
    last = 0
    for e in reversed(edit_seq):
        for i in range(last, len(gold)):
            if lev.matchEdit(e, gold[i], False):
                out.append(i)
                last = i + 1
                break
    return out

def evaluate_action_against_gold(lev, action_output, source, gold):
    seq = evaluation_edit_seq_m2(lev, action_output, source, gold, 2)
    matched = matched_indices(lev, seq, gold)
    return {
        "matched_indices": matched,
        "correct": len(matched),
        "proposed": len(seq),
        "gold": len(gold),
        "extra": len(seq) - len(matched),
    }

def build_targets(uid, gold):
    out = []
    for idx, (start, end, original, corrections) in enumerate(gold):
        if len(corrections) != 1:
            raise RuntimeError(f"{uid}: expected one correction alternative")
        correction = corrections[0]
        scope = target_scope(original, correction)
        family = target_family(start, end, original, correction)
        tid = sha_text(
            f"{uid}\t{idx}\t{start}\t{end}\t{original}\t{correction}\t{MATCHING_VERSION}"
        )
        out.append({
            "target_id": tid,
            "gold_index": idx,
            "start": start,
            "end": end,
            "original": original,
            "correction": correction,
            "scope": scope,
            "family": family,
        })
    return out

def safe_div(a, b):
    return None if b == 0 else a / b

def self_test(upstream_root=None):
    # F06 regression tests.
    assert "a" not in PNX_SET and "m" not in PNX_SET and "p" not in PNX_SET
    assert target_scope("m", "a!") == "MIXED_PUNCT_LINGUISTIC"
    assert target_scope("ياولد", "يا ولد،") == "MIXED_PUNCT_LINGUISTIC"
    assert target_family(0, 1, "ياولد", "يا ولد،") == "SPLIT"
    assert target_scope("", ".") == "PUNCTUATION_ONLY"
    assert target_scope("نص", "نص ،") == "PUNCTUATION_ONLY"
    assert target_family(0, 2, "يا بطل", "يابطل") == "MERGE"

    if upstream_root is not None:
        _, lev = import_m2(upstream_root)
        source = "انا احب العلم"
        gold = [(0, 1, "انا", ["أنا"]), (3, 3, "", ["."])]
        targets = build_targets("SYNTH", gold)
        keep = [i for i, t in enumerate(targets) if t["scope"] != "PUNCTUATION_ONLY"]
        assert keep == [0]
        sg = [gold[i] for i in keep]
        ok = evaluate_action_against_gold(lev, "أنا احب العلم", source, sg)
        bad = evaluate_action_against_gold(lev, source, source, sg)
        assert ok["correct"] == 1 and ok["extra"] == 0
        assert bad["correct"] == 0 and bad["proposed"] == 0
    return True

if __name__ == "__main__":
    self_test(None)
    print("MPSEF_RJOINT_CORE_V2_SELF_TEST_OK")
