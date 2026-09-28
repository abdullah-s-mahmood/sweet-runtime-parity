# Phase 2 — Cross-Model Agreement Risk-Family Audit

Date: 2026-09-29
Status: PRE-REGISTERED EXPLORATORY AUDIT

## Purpose

Two generic contradiction layers failed to isolate unsafe exact cross-model agreements:
- post-edit GED: 1/8 wrong captured;
- lexeme-disjoint morphology: 0/8 wrong captured.

Instead of searching for another universal oracle, this audit partitions the frozen 159 exact single-token agreements into mutually exclusive **surface transformation risk families**.

The family assignment is gold-blind and label-blind.
Human/gold labels are read only after family assignments are frozen.

This audit is exploratory on the already consumed cross-corpus slice and cannot promote a runtime policy.

## Frozen input

Cross-model agreement artifact from workflow run 36484171517.
Primary population:
EXACT_SINGLE_SUB_AGREEMENT == ACCEPT (159 events).

## Exclusive family taxonomy and priority

For source/candidate base forms:

1. HAMZA_ONLY
   - forms become identical after normalizing Arabic hamza seats.

2. TA_MARBUTA_HA_ONLY
   - only final ة <-> ه differs.

3. ALIF_MAQSURA_YA_ONLY
   - only final ى <-> ي differs.

4. WAW_ALIF_ONLY
   - only terminal differentiating-alif shape differs after final و.

5. FINAL_ALIF_OTHER
   - only a final ا is added/removed, excluding WAW_ALIF_ONLY.

6. NUN_ONLY
   - Levenshtein distance 1 and the sole insertion/deletion is ن.

7. PREFIX_ONE_CHAR
   - one character is added/removed at the beginning.

8. SUFFIX_ONE_CHAR_OTHER
   - one character is added/removed at the end, excluding families above.

9. SINGLE_CHAR_SUBSTITUTION_OTHER
   - same length, exactly one substituted character.

10. MULTI_CHAR_OR_OTHER
   - everything else.

No word identities or word-specific rules are used.

## Metrics

For every family:
- total events;
- supported corrections;
- supported alternatives;
- wrong;
- partial;
- unnecessary;
- HIGH/CRITICAL wrong;
- supported precision.

## Pre-registered candidate-family criterion

A family may be nominated for a **fresh disjoint validation only** if:
- total events >= 10;
- wrong == 0;
- partial == 0;
- unnecessary == 0.

A family failing any criterion remains REVIEW-oriented.

No family is promoted to auto-accept from this audit.

## Interpretation

If one or more families qualify:
- freeze the exact family definition;
- test unchanged on a fresh external slice before any promotion.

If no family qualifies:
- local surface selectivity is insufficient;
- proceed to parser/context-sensitive contradiction evidence.

## Prohibitions

- no QALB TEST;
- no threshold tuning after labels;
- no merging families after seeing their quality;
- no lexical blacklists;
- no Phase 3;
- no final sealed benchmark.
