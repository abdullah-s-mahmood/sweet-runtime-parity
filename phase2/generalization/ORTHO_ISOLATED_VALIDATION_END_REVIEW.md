# Phase 2 — ORTHO_ISOLATED_COMMON_NOUN_V1 Fresh Validation End Review

Date: 2026-09-29

## Canonical run

- Workflow: Phase 2 ORTHO Isolated Fresh Validation
- Run: 36520233398
- Conclusion: SUCCESS
- Population: third disjoint deterministic 50-line QALB-2015 L2 TRAIN slice
- Rule frozen before gold: yes
- QALB15 TEST read: no
- QALB text persisted: no
- Leakage audit: PASS

## Frozen runtime result

- exact tri-model unanimous raw candidates after protected-risk veto: 175
- ORTHO_ISOLATED_COMMON_NOUN_V1 PASS: 14
- REVIEW: 161
- PASS rate over unanimous candidates: 8.00%
- minimum PASS requirement (>=10): met

## Gold comparison and bounded contextual review

Automatic comparison:
- exact-gold supported: 8
- non-exact requiring bounded contextual review: 6

Contextual review of the six non-exact PASS events:
- supported correction: 3
- supported alternative: 1
- partial correction: 2
- wrong correction: 0
- unnecessary edit: 0

Final:
- supported: 12/14 = 85.71%
- unsafe partial: 2/14 = 14.29%
- wrong: 0
- unnecessary: 0

## Decision

**WORSENED as an auto-accept lane; IMPROVED epistemically.**

The pre-registered contract required zero wrong, zero partial, and zero unnecessary PASS events. The lane fails because two PASS events were only partial corrections.

**DO_NOT_PROMOTE_ORTHO_ISOLATED_COMMON_NOUN_V1.**

No rule changes are permitted on this consumed validation slice.

## Magnitude versus prior consumed diagnostic

Prior consumed diagnostic:
- 19/19 supported = 100%
- unsafe = 0/19

Fresh disjoint validation:
- 12/14 supported = 85.71%
- partial = 2/14 = 14.29%

Descriptive selected-lane precision change:
- **-14.29 percentage points**

This comparison is across different populations and is not a causal estimate, but it is sufficient to falsify the claim that V1 is a zero-unsafe unattended lane.

## Failure pattern

The two unsafe PASS events share a key property: the proposed character-level orthographic repair is locally plausible and morphology-preserving, but the surrounding construction still requires a broader lexical/syntactic repair. Therefore:
- tri-model unanimity is insufficient;
- morphology identity is insufficient;
- ±2 edit-neighborhood isolation is insufficient;
- local orthographic correctness does not prove repair completeness.

## Scientific consequence

Keep the lane REVIEW-first. Do not tune the V1 morphology fields, POS class, neighborhood radius, surface families, or thresholds on this slice.

The next justified hypothesis must add independent evidence for **contextual repair completeness**, not merely stronger local agreement.

Independent human validation remains required before any future production auto-apply claim.
