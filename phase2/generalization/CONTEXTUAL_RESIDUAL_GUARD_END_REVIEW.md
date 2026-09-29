# Phase 2 — Contextual Residual-Risk Guard End Review

Date: 2026-09-29

## Decision

**IMPROVED strongly as a narrow diagnostic lane; NOT YET GENERALIZATION EVIDENCE.**

Population: the already-consumed 142 UNANIMOUS_3 events.

### Primary — ORTHO_ISOLATED_COMMON_NOUN_V1
- PASS: 19/142 = 13.38%
- REVIEW: 123/142 = 86.62%
- supported PASS: 19
- wrong PASS: 0
- partial PASS: 0
- unnecessary PASS: 0
- PASS precision: **100%**
- status: **ELIGIBLE_FOR_FRESH_VALIDATION**

### Ablation — ORTHO_MORPH_COMMON_NOUN_V1
- PASS: 36
- supported: 34
- partial: 2
- precision: **94.44%**

Neighborhood isolation therefore changed the selected lane from 34/36 supported to 19/19 supported:
- precision: +5.56 percentage points
- accepted events: 36 -> 19 (-47.22%)
- partials: 2 -> 0

### Versus raw UNANIMOUS_3
Raw tri-model: 126/142 supported = 88.73%.
Primary guard PASS lane: 19/19 supported = 100%.
Descriptive selected-lane precision change: **+11.27 percentage points**.
Unsafe selected edits: 16/142 in raw tri-model population versus 0/19 in the guarded PASS lane.

These are selection results on a consumed population, not a production precision estimate and not independent generalization.

## Interpretation

The result supports the hypothesis that a very narrow, isolated, morphology-preserving orthographic lane may be safer than broad model consensus. It also demonstrates that neighborhood isolation is not cosmetic: removing it admitted two partial corrections.

## Next step

Freeze ORTHO_ISOLATED_COMMON_NOUN_V1 byte-for-byte and validate it on a third deterministic 50-line QALB15 L2 TRAIN slice excluding both prior 50-line slices. No rule changes are permitted before that result.

Fresh validation must keep QALB15 TEST unread and persist no licensed QALB text.

## Forecast

If the lane remains zero-unsafe with at least 10 accepted events, confidence in a narrow unattended orthographic path will improve materially, but independent human validation will still be required before production claims. If any wrong or partial correction passes, the lane remains REVIEW-first and the next justified escalation is dependency-aware contextual evidence such as CamelParser2.0.