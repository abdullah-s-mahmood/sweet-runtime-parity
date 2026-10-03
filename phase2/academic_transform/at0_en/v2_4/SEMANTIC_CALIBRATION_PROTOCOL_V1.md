# AT0-EN V2.4 — Semantic Calibration and Threshold Selection Protocol V1

Date: 2026-10-03
Status: FROZEN BEFORE ANY SEMANTIC SCORE

## Scope

This protocol applies only to the already-consumed DEVELOPMENT calibration population. It does not open or define confirmation results.

Semantic witnesses:
- HHEM-2.1-Open: support/consistency score
- DeBERTa NLI: entailment / neutral / contradiction probabilities

Both witnesses score the exact same frozen pair manifest.

## Pair directions

For each source assertion:
- premise = candidate paragraph
- hypothesis = frozen source assertion
- direction = SOURCE_TO_CANDIDATE
- purpose = detect omission, contradiction or semantic weakening of source content

For each deterministic candidate claim unit:
- premise = immutable source paragraph
- hypothesis = candidate claim unit
- direction = CANDIDATE_TO_SOURCE
- purpose = detect unsupported additions or contradictions

No pair is generated or removed after semantic scores are observed.

## Per-paragraph aggregate features

From every pair belonging to a paragraph record:
- H_s2c_min = minimum HHEM consistency score over SOURCE_TO_CANDIDATE
- H_c2s_min = minimum HHEM consistency score over CANDIDATE_TO_SOURCE
- E_s2c_min = minimum DeBERTa entailment probability over SOURCE_TO_CANDIDATE
- E_c2s_min = minimum DeBERTa entailment probability over CANDIDATE_TO_SOURCE
- C_s2c_max = maximum DeBERTa contradiction probability over SOURCE_TO_CANDIDATE
- C_c2s_max = maximum DeBERTa contradiction probability over CANDIDATE_TO_SOURCE

No mean score can override a failing minimum/maximum witness.

## Semantic VERIFIED_FOR_REVIEW rule

A paragraph is semantic VERIFIED_FOR_REVIEW at threshold tuple (T_H, T_E, T_C) only when all hold:

- H_s2c_min >= T_H
- H_c2s_min >= T_H
- E_s2c_min >= T_E
- E_c2s_min >= T_E
- C_s2c_max <= T_C
- C_c2s_max <= T_C

Otherwise semantic disposition is REVIEW.

The semantic layer does NOT issue SEMANTIC_REJECT in V2.4 calibration. Deterministic protected-invariant contradictions may still produce HARD_REJECT outside this threshold rule.

## Frozen threshold search

Grid:
- T_H = 0.05, 0.10, ..., 0.95
- T_E = 0.05, 0.10, ..., 0.95
- T_C = 0.05, 0.10, ..., 0.95

For every tuple compute:
- adversarial auto-pass count/rate
- safe VERIFIED_FOR_REVIEW count/coverage

Eligible tuples must have:
- adversarial auto-pass count = 0

Among eligible tuples:
1. maximize safe VERIFIED_FOR_REVIEW count;
2. tie-break by higher (T_H + T_E - T_C), i.e. more conservative support/contradiction boundary;
3. then higher T_H;
4. then higher T_E;
5. then lower T_C.

If no eligible tuple exists, calibration FAILS.

## Calibration viability gate

To justify freezing thresholds for a future untouched confirmation population:
- adversarial auto-pass = 0 / 36
- safe VERIFIED_FOR_REVIEW coverage >= 70% (at least 16 / 22)
- no missing semantic score
- no witness/runtime/hash mismatch

If calibration fails, do not create confirmation merely to seek a better result. Return for redesign.

## Confirmation boundary

Only after calibration thresholds are locked may a new untouched confirmation population be constructed/frozen.

Confirmation target remains:
- critical unsafe auto-pass = 0
- overall adversarial unsafe auto-pass <= 5%
- safe VERIFIED_FOR_REVIEW coverage >= 70%
- safe hard-reject <= 10%

No threshold changes are allowed after confirmation is opened.

## Non-authorized interpretations

- HHEM high score alone is not scientific correctness.
- DeBERTa entailment alone is not scientific correctness.
- A semantic VERIFIED_FOR_REVIEW outcome is not automatic application approval.
- REVIEW is not failure; it is abstention under insufficient evidence.
