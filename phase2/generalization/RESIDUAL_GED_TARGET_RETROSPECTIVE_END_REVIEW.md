# Phase 2 — Residual GED Target-Clean Retrospective End Review

Date: 2026-09-29

## Decision

**MIXED: precision improved, but the pre-registered zero-partial safety criterion failed.**

Canonical retrospective run:
- workflow: Phase 2 Residual GED Target Retrospective
- run: 36531699643
- conclusion: SUCCESS
- features frozen before labels: true
- preprocessing: official pinned CAMeLIRA QALB15 TRAIN source
- QALB15 TEST read: false
- QALB text persisted: false

## Preceding evidence

Direct-text consumed diagnostic on the third-slice 14-event ORTHO V1 population:
- GED_TARGET_CLEAN_BOTH PASS: 12/14
- supported PASS: 12/12
- partial PASS: 0/2
- supported retention: 100%
- partial capture: 100%
- status: promising only for preprocessing-faithful replication.

Preprocessing-faithful replication on the same 14 events:
- PASS: 12/14
- supported PASS: 12/12
- partial PASS: 0/2
- supported retention: 100%
- partial capture: 100%
- official preprocessing had already normalized the target to the candidate surface in 14/14 cases.
- therefore the separation was contextual GED evidence, not merely surface-spelling recognition.

## Independent retrospective population

Earlier consumed ORTHO_MORPH_COMMON_NOUN_V1 population:
- total: 36
- historical supported: 34
- historical partial: 2
- historical precision: 34/36 = 94.44%

Frozen GED_TARGET_CLEAN_BOTH result:
- PASS: 29
- REVIEW: 7
- supported PASS: 28
- partial PASS: 1
- wrong PASS: 0
- unnecessary PASS: 0
- PASS precision: 28/29 = 96.55%
- supported retention: 28/34 = 82.35%
- partial capture: 1/2 = 50%
- review burden: 7/36 = 19.44%

Nested strict V1 subset:
- total: 19
- PASS: 14
- supported PASS: 14
- no known unsafe event existed in this subset.

## Magnitude

Versus the unfiltered 36-event ORTHO_MORPH population:
- precision: 94.44% -> 96.55% = +2.11 percentage points
- unsafe partials: 2 -> 1
- accepted coverage: 36 -> 29 = -19.44%
- supported retention: 82.35%

This is a useful ranking/review signal but not a proof-of-safety gate.

## Pre-registered criterion

Required:
- PASS >= 10: PASS
- wrong PASS = 0: PASS
- partial PASS = 0: **FAIL**
- unnecessary PASS = 0: PASS
- nested strict-V1 PASS >= 10: PASS

**Decision: NOT_PROMISING for a fourth disjoint auto-accept validation.**

No fourth QALB15 slice may be spent on this rule.

## Interpretation

Residual target-level GED is materially better than raw structural/morphological acceptance alone, but one partial correction still appears clean under both frozen GED models. The failure is consistent with the central problem observed throughout Phase 2: a locally acceptable target can coexist with an incomplete sentence-level repair.

The target-clean signal should remain available as a review/ranking feature, not as an unattended acceptance proof.

## Next justified research direction

The next diagnostic should move from token-level cleanliness to **sentence-level correction acceptability discrimination**:
- compare source and candidate as a pair;
- judge whether the candidate is a complete and meaning-preserving repair, not merely a locally clean token;
- use a dedicated acceptability/discrimination objective rather than another vote, dependency heuristic, or GED threshold;
- test on consumed evidence first;
- prohibit fresh-slice consumption until a pre-registered consumed-population criterion is met.

No Phase 3. No sealed benchmark.
