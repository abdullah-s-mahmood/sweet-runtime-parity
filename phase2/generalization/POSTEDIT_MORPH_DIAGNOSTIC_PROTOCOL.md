# Phase 2 — Post-Edit Stability & Morphological Identity Diagnostic

Date: 2026-09-29
Status: PRE-REGISTERED DIAGNOSTIC ON CONSUMED TRI-MODEL UNANIMOUS_3 POPULATION

## Motivation

Tri-model 3/3 exact edit agreement on a fresh QALB-2015 L2 TRAIN slice produced 142 accepted events, but contextual adjudication found 126 supported and 16 unsafe (12 partial + 4 wrong). More voting therefore did not create a safe unattended lane.

The residual failures fall into two broad classes:
1. incomplete repairs that may be detectable by re-running the correction stack after applying accepted edits;
2. hidden lexical/morphosyntactic identity changes (lemma/POS/person/tense/number/gender/clitic) that can look like local spelling edits.

This diagnostic tests those two properties independently and jointly.

## Population

Exactly the 142 consumed UNANIMOUS_3 accepted events from the canonical Tri-Model V2 run 36517205396.
These events occur on 43 unique QALB-2015 L2 TRAIN lines.

No policy may be promoted from this consumed population.

## Reproducibility optimization

Reuse the frozen first-pass voter artifacts from canonical run 36517205396 instead of rerunning the first pass.
Reconstruct jointly corrected lines ephemerally inside CI by applying all UNANIMOUS_3 accepted single-token substitutions on each affected raw line.

No QALB text may be committed.

## Signal A — post-edit stability

After all unanimous edits are jointly applied to an affected line, rerun the same three frozen voters:
- SWEET QALB14 NoPnx
- SWEET ZAEBUC NoPnx
- AraBART QALB14.

For each original accepted target:

### POST_EDIT_TARGET_STABLE_ALL3
PASS only if none of the three second-pass voters proposes any edit event overlapping the original target lexical token.

### POST_EDIT_WINDOW1_STABLE_ALL3
PASS only if none of the three second-pass voters proposes an edit event touching the original target token or either immediate lexical neighbor (target ±1).

These are completeness/stability signals, not correctness proofs.

## Signal B — contextual morphological identity

Use CAMeL BERT contextual disambiguation on:
- the original raw line;
- the jointly corrected line.

At each accepted target, compare the top contextual analyses of the corresponding whitespace token.

### MORPH_IDENTITY_SAFE
PASS only if both analyses exist and the following identity fields agree after diacritic/tatweel removal from lexical lemma:
- lex
- pos
- per
- asp
- vox
- gen
- num
- prc0, prc1, prc2, prc3
- enc0.

Fields cas, mod, and stt are deliberately excluded from identity equality because legitimate grammar correction may intentionally alter case, mood, or state.

Missing/ambiguous analysis => REVIEW.

This is intentionally conservative. It tests identity preservation; it does not claim morphology alone proves correctness.

## Joint policy

### TARGET_STABLE_AND_MORPH_SAFE
PASS only when both POST_EDIT_TARGET_STABLE_ALL3 and MORPH_IDENTITY_SAFE pass.

## Anti-leakage order

1. Download frozen first-pass artifacts from canonical run 36517205396.
2. Re-materialize the frozen UNANIMOUS_3 votes.
3. Reconstruct jointly corrected lines from RAW only.
4. Run second-pass voters and contextual morphology.
5. Materialize all stability/morphology features and PASS/REVIEW decisions.
6. Hash/freeze runtime evidence.
7. Only then read PHASE2_TRIMODEL_VOTING_RESULTS.json and PHASE2_TRIMODEL_VOTING_MANUAL_REVIEW.json.
8. Evaluate capture/retention.
9. Do not tune these policies on this population.

## Pre-registered promising criterion

A policy is PROMISING_FOR_FRESH_VALIDATION only if all conditions hold:
- total unsafe capture >= 50% (>=8 of 16);
- wrong-correction capture >= 75% (>=3 of 4);
- all HIGH-severity wrong events captured;
- supported retention >= 80% (>=101 of 126);
- review burden <= 30%.

Meeting this criterion does not authorize production or promotion. It only permits the unchanged policy to be tested on a fresh disjoint raw-only slice.

## Constraints

- No QALB-2015 TEST.
- No final sealed benchmark.
- No Phase 3.
- No training on the 142 labels.
- No threshold search after evaluation.
- No QALB text persistence.
- Review remains a first-class outcome.