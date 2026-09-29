# Phase 2 — Local-Edit Semantic Backstop Diagnostic

Date: 2026-09-29
Status: PRE-REGISTERED DIAGNOSTIC ON CONSUMED CROSS-MODEL AGREEMENT SLICE

## Continuity

This gate continues ACAD_PASS Phase 2 after Cross-Corpus Independent Edit Agreement, Contextual Contradiction Diagnostic, Lexical Continuity Diagnostic, and Agreement Risk-Family Audit.

It is diagnostic only. No policy may be promoted from this already-consumed 50-line QALB-2015 L2 TRAIN slice.

## Motivation

Exact SWEET NoPnx / AraBART agreement improved the stream, but manual review still found 144 supported corrections, 8 wrong corrections, 6 partial corrections, and 1 unnecessary edit.

GED contradiction, lexical continuity, and simple risk-family rules did not isolate all unsafe cases.

ACAD_PASS already established multilingual bidirectional mDeBERTa NLI as a semantic backstop, but Arabic review burden was historically high. This experiment asks whether local-edit-aware semantic verification can improve unsafe capture without sending most correct local edits to REVIEW.

## Prototype identity

NEW prototype: LOCAL_EDIT_SEMANTIC_BACKSTOP_PROTOTYPE.

It is not claimed to be byte-identical to the earlier ACAD_PASS product verifier because the original product-path implementation files are not present in this repository.

Model: MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7.

The model is independent of SWEET and AraBART.

## Population

Use exactly the already-consumed 159 EXACT_SINGLE_SUB_AGREEMENT accepted events from the frozen cross-model agreement slice.

Reconstruct source/candidate text ephemerally inside CI from pinned QALB-2015 L2 TRAIN raw input and frozen agreement event geometry/output. Do not persist QALB text.

## Runtime semantic views

For every accepted event compute bidirectional NLI on WHOLE SENTENCE and on a LOCAL WINDOW of five lexical source tokens on each side where available.

Also check narrow protected invariants: digit sequence, Latin-token sequence, bracketed numeric citations, and %, =, <, >, ± markers.

## Frozen diagnostic policies

### WHOLE_HISTORICAL_05
REVIEW if either directional entailment probability < 0.50, or either directional contradiction probability >= 0.50, or protected invariants differ. Otherwise PASS.

### LOCAL_HISTORICAL_05
Same historical rule, but on the local window.

### CONTRADICTION_ONLY_05
REVIEW if any whole-sentence or local-window directional contradiction probability >= 0.50, or protected invariants differ. Otherwise PASS.

No other threshold search is allowed on this consumed slice.

## Anti-leakage order

1. Recreate frozen cross-model raw event artifacts.
2. Materialize the same exact-agreement events.
3. Reconstruct source/candidate text from RAW only.
4. Run NLI and protected invariants.
5. Materialize semantic scores and PASS/REVIEW decisions.
6. Hash/freeze runtime output.
7. Only then read PHASE2_CROSS_MODEL_AGREEMENT_RESULTS.json and PHASE2_CROSS_MODEL_AGREEMENT_MANUAL_REVIEW.json.
8. Evaluate decisions.
9. Do not tune these three policies on this population.

## Metrics

For each policy report review count/burden, supported retained / 144, supported false reviews, wrong captured / 8, partial captured / 6, unnecessary captured / 1, total unsafe captured / 15, unsafe residual PASS, and residual PASS precision.

## Pre-registered promising threshold

A policy is PROMISING_FOR_FRESH_VALIDATION only if all hold:
- total unsafe capture >= 50%;
- wrong-correction capture >= 50%;
- supported retention >= 80%;
- review burden <= 25%.

This does NOT promote the policy. It only permits unchanged fresh disjoint validation.

Otherwise: NOT_PROMISING_ON_CONSUMED_SLICE.

## Constraints

- No QALB text committed.
- No QALB-2015 TEST.
- No sealed benchmark.
- No Phase 3.
- No claim that NLI probability is calibrated semantic-risk probability.
- No LLM/reference-free judge as sole oracle.