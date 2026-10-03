# AT0-EN V2.4 — Gate B2 Extracted-Graph Alignment Degradation Protocol V1

Date: 2026-10-03
Status: FROZEN PRE-IMPLEMENTATION / DEVELOPMENT-ONLY

## Purpose

B2 measures how much of the B1 human-correct alignment performance is lost when source and/or candidate graphs are produced by the frozen extraction pipeline.

B2 is a degradation-attribution experiment, not an untouched holdout.

## Frozen baselines

Human-correct B1 baseline:
- pair outcomes: 12/12 = 100%
- critical alignment coverage: 22/22 = 100%
- critical alignment-status accuracy: 100%
- adversarial acceptance: 0
- faithful false rejection: 0
- uncertainty preservation: 100%
- evidence-trace completeness: 100%

Frozen aligner SHA-256:
`289d2898c89850f691d52313a1d2a2b12b37cef6b674549215579caedf84cd42`

Frozen source assertion extractor SHA-256:
`32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`

Frozen B1 human-correct pair set SHA-256:
`29f3790859c8da6baf65db8b0fb372bc881e25d8e3d1e76b9c67b74d49944dca`

## Four-arm attribution design

### GG — Gold source -> Gold candidate
Historical B1.1 baseline.
No new inference required.
Expected pair accuracy: 100%.

### GE — Gold source -> Extracted candidate
Measures candidate-extraction degradation while holding source representation correct.

### EG — Extracted source -> Gold candidate
Measures source-extraction degradation while holding candidate representation correct.

### EE — Extracted source -> Extracted candidate
Primary integrated extraction+alignment development arm.

Results from all four arms must be reported separately.
No aggregate may hide which side introduced the error.

## Raw-text derivation

B2 raw source/candidate texts are derived deterministically from the frozen B1 graphs.

For each side:
1. append assertion evidence strings in graph order;
2. append relation evidence strings in graph order;
3. exact duplicate evidence strings may be removed while preserving first occurrence;
4. no semantic rewriting is allowed.

This preserves the semantic material exposed to the human-correct graph while avoiding a new generation model.

## Extraction policy

The same frozen A2 source assertion extractor is applied independently to:
- source raw text;
- candidate raw text.

Candidate extraction receives no source graph, source text, expected mapping, expected outcome, or gold label.

No extractor tuning occurs before the first B2 score.

## Bridge policy

A deterministic bridge converts A2 extraction output to the B1 alignment graph schema.

The bridge may:
- rename fields;
- carry direct subject/predicate/object;
- carry polarity, modality, causality, time, population, baseline, scope;
- map CERTAIN/UNCERTAIN/AMBIGUOUS directly;
- carry exact evidence spans;
- convert anchors explicitly owned by an extracted assertion into mechanical binding fields.

The bridge MUST NOT:
- infer missing relations;
- invent citation, equation, procedure-order, or ownership edges;
- resolve coreference not resolved by the extractor;
- rewrite assertion semantics;
- use B1 gold mappings or expected outcomes;
- repair an extraction because the expected answer is known.

Because the frozen A2 extractor emits zero semantic graph relations, absent relations remain absent in B2 extracted graphs. This is intentional degradation evidence, not a bridge defect.

## Arm scoring

Each arm uses the same frozen B1.1 aligner.

Expected pair outcomes remain the frozen B1 outcomes:
- PASS_CANDIDATE: 5
- REJECT: 6
- REVIEW: 1

Primary B2 readiness is based on EE.
GE and EG diagnose which extraction side causes degradation.

## Pre-registered EE hard safety gates

1. Material adversarial acceptance:
   **0/6 required**

2. Dangerous critical false-preserve:
   **0 required**

3. Ambiguous pair:
   must remain **REVIEW**

4. Critical uncertainty promotion:
   **0 required**

No usability score may compensate for a safety-gate failure.

## Pre-registered EE usability gates

1. Faithful safe-pair acceptance:
   at least **4/5 = 80%**

2. Pair-level expected outcome:
   at least **11/12 = 91.67%**

3. Faithful false rejection:
   at most **1/5**

These thresholds allow at most one conservative safe failure while permitting no dangerous adversarial acceptance.

## Degradation metrics

Always report against GG=100%:

- pair-outcome degradation in percentage points;
- faithful-safe-acceptance degradation;
- adversarial-safety degradation;
- REVIEW preservation;
- GE vs GG;
- EG vs GG;
- EE vs GG;
- EE vs GE and EG to identify interaction effects.

Do not describe different-arm differences as causal beyond this fixed synthetic development set.

## Result classes

- `PASS_B2_EXTRACTED_DEVELOPMENT`:
  all safety and usability gates pass.

- `MIXED_B2_REPAIR_REQUIRED`:
  safety passes, but one or more usability gates fail.

- `FAIL_B2_SAFETY`:
  any adversarial acceptance, dangerous critical false preserve, uncertainty promotion, or ambiguous-pair PASS occurs.

- `INVALID_B2_EVALUATION`:
  fixture/bridge/scorer integrity invalidates the comparison.

## Stop rule

After first B2 score:
- freeze all four arms and degradation metrics;
- preserve failures before any repair;
- do not tune extractor, bridge, or aligner before freezing the first result;
- any later repair is versioned.

## Scope exclusions

B2 does NOT authorize:
- live generation;
- HW1-EN;
- untouched holdout;
- production claims;
- authentic integrated-document validity claims.

Authentic academic text remains scheduled after a diagnosable extracted-graph alignment prototype.
