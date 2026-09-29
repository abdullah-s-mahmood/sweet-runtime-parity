# Phase 2 — Post-Edit Stability & Morphological Identity End Review

Date: 2026-09-29

## Canonical repaired run

- Workflow: Phase 2 Post-Edit Morphology Environment Repair
- Run: 36522179119
- Conclusion: SUCCESS
- Reused frozen second-pass artifacts from failed-environment run 36519213784
- Only runtime environment changed; diagnostic policies and thresholds were unchanged
- QALB15 TEST read: no
- QALB text persisted: no
- Leakage audit: PASS

## Population

Consumed 142 UNANIMOUS_3 events from canonical tri-model run 36517205396:
- supported: 126
- unsafe: 16
  - partial: 12
  - wrong: 4
- HIGH wrong: 3

No promotion is allowed from this population.

## Results

### POST_EDIT_TARGET_STABLE_ALL3
- PASS: 139
- REVIEW: 3
- supported retained: 124/126 = 98.41%
- unsafe captured: 1/16 = 6.25%
- wrong captured: 0/4 = 0%
- HIGH wrong captured: 0/3
- residual PASS precision: 89.21%
- status: NOT_PROMISING_ON_CONSUMED_SLICE

### POST_EDIT_WINDOW1_STABLE_ALL3
- PASS: 138
- REVIEW: 4
- supported retained: 123/126 = 97.62%
- unsafe captured: 1/16 = 6.25%
- wrong captured: 0/4 = 0%
- HIGH wrong captured: 0/3
- residual PASS precision: 89.13%
- status: NOT_PROMISING_ON_CONSUMED_SLICE

### MORPH_IDENTITY_SAFE
- PASS: 127
- REVIEW: 15
- supported retained: 115/126 = 91.27%
- unsafe captured: 4/16 = 25.00%
- wrong captured: 2/4 = 50.00%
- HIGH wrong captured: 2/3
- residual PASS precision: 90.55%
- status: NOT_PROMISING_ON_CONSUMED_SLICE

### TARGET_STABLE_AND_MORPH_SAFE
- PASS: 125
- REVIEW: 17
- supported retained: 113/126 = 89.68%
- unsafe captured: 4/16 = 25.00%
- wrong captured: 2/4 = 50.00%
- HIGH wrong captured: 2/3
- residual PASS precision: 90.40%
- status: NOT_PROMISING_ON_CONSUMED_SLICE

## Pre-registered promising criterion

Required:
- unsafe capture >=50%
- wrong capture >=75%
- all HIGH wrong captured
- supported retention >=80%
- review burden <=30%

No tested policy meets the capture requirements.

**fresh_validation_allowed_for = []**

## Decision

**MIXED/WORSENED as a candidate safety gate; IMPROVED epistemically.**

Post-edit fixed-point stability is too weak because shared/local errors can remain stable across the same model family after the first correction pass. Morphological identity has modest discriminatory value but misses most unsafe events.

Do not spend a fresh disjoint slice on any of these policies.

Next justified diagnostic: dependency/governor compatibility, targeting the syntactic completeness failure that survived voting, orthographic isolation, post-edit stability, and morphology identity.
