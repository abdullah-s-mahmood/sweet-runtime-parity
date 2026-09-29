# Phase 2 — Local-Edit Semantic Backstop End Review

Date: 2026-09-29

## Decision

**MIXED — epistemic improvement, no promotable acceptance-policy improvement.**

The diagnostic successfully falsified the assumption that generic multilingual NLI can clean the exact-agreement stream at commercially acceptable review burden.

Canonical fast diagnostic run: 36514904529 (SUCCESS).

## Baseline population

159 exact SWEET NoPnx / AraBART single-substitution agreements:
- supported correction: 138
- supported alternative: 6
- total supported: 144
- wrong correction: 8
- partial correction: 6
- unnecessary edit: 1
- total unsafe: 15

Baseline exact-agreement supported precision before semantic backstop: 144/159 = 90.57%.

## WHOLE_HISTORICAL_05

- PASS: 1
- REVIEW: 158
- review burden: 99.37%
- unsafe captured: 15/15 = 100%
- wrong captured: 8/8 = 100%
- supported retained: 1/144 = 0.69%
- residual PASS precision: 100%
- status: NOT_PROMISING_ON_CONSUMED_SLICE

Interpretation: semantic recall is high only because essentially everything is reviewed. This is not a useful automatic proofreading gate.

## LOCAL_HISTORICAL_05

- PASS: 133
- REVIEW: 26
- review burden: 16.35%
- unsafe captured: 2/15 = 13.33%
- wrong captured: 2/8 = 25%
- partial captured: 0/6
- unnecessary captured: 0/1
- supported retained: 120/144 = 83.33%
- residual PASS precision: 120/133 = 90.23%
- status: NOT_PROMISING_ON_CONSUMED_SLICE

Interpretation: review burden is acceptable, but unsafe capture is far below the pre-registered threshold and residual precision is slightly worse than the unfiltered 90.57% baseline.

## CONTRADICTION_ONLY_05

- PASS: 157
- REVIEW: 2
- review burden: 1.26%
- unsafe captured: 0/15
- wrong captured: 0/8
- supported retained: 142/144 = 98.61%
- residual PASS precision: 142/157 = 90.45%
- status: NOT_PROMISING_ON_CONSUMED_SLICE

Interpretation: contradiction-only NLI preserves coverage but provides no safety gain and falsely reviews two supported edits.

## Magnitude versus previous stage

Product-policy quality did not improve:
- best previous exact-agreement baseline: 90.57% supported precision at zero added semantic-review burden;
- local NLI: 90.23% residual precision with 16.35% review burden;
- contradiction-only: 90.45% residual precision with 1.26% review burden;
- whole NLI: 100% residual precision only by reviewing 99.37% of the stream.

Therefore the semantic backstop is not promoted.

## What this gate proves

1. Whole-sentence NLI is too conservative for minimal Arabic grammar edits under the historical 0.5 entailment rule.
2. Local-window NLI increases sensitivity but still misses most wrong/partial edits.
3. High contradiction probability is rare for these local grammatical errors; contradiction-only veto is ineffective.
4. Generic semantic equivalence is the wrong abstraction for many local grammatical-correction validity errors.
5. ACAD_PASS should keep semantic verification downstream for scientific/meaning-changing risk, but it should not use generic NLI as the primary Arabic GEC acceptance oracle.

## Architecture decision

Keep the broader ACAD_PASS semantic verifier for scientific integrity and semantic drift after linguistic editing.

Do NOT promote any of these NLI policies into Arabic proofreading acceptance.

Do NOT tune additional NLI thresholds on this consumed slice.

## Next evidence direction

Shift from generic semantic scoring to **multi-system edit evidence**.

Best next falsifiable direction:
**Cross-Training Multi-System Edit Voting Gate**.

Candidate system pool:
- SWEET QALB14 NoPnx (edit tagging, QALB14 training);
- SWEET ZAEBUC NoPnx (edit tagging, different training corpus);
- AraBART QALB14 + GED (seq2seq/morph pipeline, QALB14 training);
- AraBART ZAEBUC + GED (seq2seq/morph pipeline, different training corpus).

Test on a fresh deterministic QALB15 L2 TRAIN slice excluding the consumed 50 lines.

Pre-register:
- 4/4 exact edit unanimity;
- 3/4 exact edit majority with at least one SWEET and one AraBART vote;
- cross-training cross-architecture agreement;
- protected scientific vetoes.

Gold is opened only after votes are frozen.

No QALB15 TEST, no final sealed benchmark, no Phase 3.