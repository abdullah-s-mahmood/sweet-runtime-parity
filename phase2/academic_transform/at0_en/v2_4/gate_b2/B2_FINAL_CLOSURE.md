# AT0-EN V2.4 — Gate B2 Final Closure

Date: 2026-10-03
Status: CLOSED / PASS_B2_EXTRACTED_DEVELOPMENT / GATE B COMPLETE

## Canonical repaired revalidation

Run:
`37150199075`

Trigger commit:
`6d8a38c9befb8729c093efaeca1feb7a67e47942`

Artifact:
- id: `11283159352`
- SHA-256: `08b9d7a31a611b4fe0d6e8cd25deaffc8f254950c7173cc68666164ed0c23aec`

Result:
`PASS_B2_EXTRACTED_DEVELOPMENT`

No model inference occurred.

## Four-arm result

### GG — Gold -> Gold
- pair accuracy: 12/12 = 100%
- safe acceptance: 5/5 = 100%
- adversarial acceptance: 0/6
- REVIEW preservation: 100%

### GE — Gold -> Extracted
- pair accuracy: 11/12 = 91.67%
- safe acceptance: 4/5 = 80%
- adversarial acceptance: 0/6
- REVIEW preservation: 100%
- only mismatch: B1-P01

### EG — Extracted -> Gold
- pair accuracy: 11/12 = 91.67%
- safe acceptance: 4/5 = 80%
- adversarial acceptance: 0/6
- REVIEW preservation: 100%
- only mismatch: B1-P01

### EE — Extracted -> Extracted
- pair accuracy: 12/12 = 100%
- safe acceptance: 5/5 = 100%
- adversarial acceptance: 0/6
- REVIEW preservation: 100%
- faithful false rejection: 0
- critical uncertainty promotion: 0

## Representation audit

Independent per-side structural/evidence audit:
- sides: 24
- checks: 102
- failures: 0
- all sides PASS

The audit checks:
- frozen A1 anchor/provenance preservation;
- exact assertion evidence;
- explicit value-binding support;
- explicit equation coefficient-to-symbol support;
- explicit citation relation support;
- explicit PRECEDES support;
- explicit DISTINCT_FROM support.

## Improvement versus canonical first B2

EE:
- pair accuracy: 33.33% -> 100% = **+66.67 pp**
- safe acceptance: 0% -> 100% = **+100 pp**
- adversarial acceptance: 0% -> 0% = **no safety regression**

GE:
- pair accuracy: 41.67% -> 91.67% = **+50 pp**
- safe acceptance: 0% -> 80% = **+80 pp**

EG:
- pair accuracy: 50% -> 91.67% = **+41.67 pp**
- safe acceptance: 20% -> 80% = **+60 pp**

GG:
- remains 100%.

## Shared-error safeguard review

Because EE reached 100% while GE and EG each remained 91.67%, the required shared-error safeguard was triggered.

Review file:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_2_SHARED_ERROR_REVIEW_P01.md`

Review commit:
`4e0ec1001487dbf7375429e562b793f7d78ea9c3`

Finding:
`CANONICALIZATION_FIXTURE_MISMATCH / NOT_SHARED_SEMANTIC_ERROR`

B1-P01 contains relation evidence:
`The findings concern different subsystems.`

The frozen B2 raw-text derivation appends relation evidence as standalone text.
The relation-aware extractor therefore emits:
- the critical semantic limitation;
- the critical DISTINCT_FROM relation;
- one extra MATERIAL assertion supported by that standalone evidence sentence.

This extra MATERIAL assertion is present on both extracted sides but not in the human-correct gold graphs.

Therefore:
- EE passes with a redundant but text-supported representation;
- GE/EG see a gold-vs-extracted representation mismatch;
- no critical meaning loss, false relation, shared omission, or unsupported evidence was found.

No repair was made after this review.
GE and EG remain reported at 91.67%.

## Prototype evidence

Final relation-aware prototype:
- 17/17 principle/red-team regressions PASS

Authentic academic qualitative check:
- 5 excerpts
- CERTAIN: 5
- AMBIGUOUS: 0
- unsupported invented relations: 0

This authentic check is qualitative development evidence only and is not a benchmark.

## Research interpretation

Recent scientific-information-extraction and claim-verification literature continues to show:
- full-text entity/relation extraction remains difficult;
- high within-dataset scores do not guarantee transfer;
- final verdict correctness alone is insufficient without faithful evidence/rationale alignment;
- development-set success must not be represented as generalization.

Therefore B2 is a development-stage PASS only.

## Frozen B2 progression gates

All passed:
- adversarial acceptance = 0/6
- dangerous critical false preserve = 0
- critical uncertainty promotion = 0
- ambiguous pair remains REVIEW
- safe acceptance >=4/5
- pair accuracy >=11/12
- faithful false rejection <=1/5
- GG remains 100%
- representation audit clean

## Strong-adoption ledger

### Extracted-graph pair accuracy
Current measured development result:
**100% EE**

Strong-adoption target:
**>=95%**

Status:
target exceeded on current synthetic development set only.

### Authentic in-domain safe automatic acceptance
Current:
**NOT YET MEASURED as a benchmark**

Strong-adoption target:
**>=90%**

### Automatic-PASS selective precision end-to-end
Current:
**NOT YET MEASURED**

Strong-adoption target:
**>=99%**

### Adversarial automatic acceptance
Current measured B2:
**0%**

Strong-adoption target:
**0%**

### Critical silent scientific errors
Current measured development evidence:
**0 observed**

Strong-adoption target:
**0**

### Human-correct alignment
Current:
**100%**

Target:
**100%**

### Ambiguity preservation
Current B2:
**100%**

Target:
**100%**

## Cumulative V2.4 ledger

- V2.3 end-to-end baseline: 37.5% escape / 25% safe acceptance / BOTH_FAIL
- Gate 0: 326/326 contract checks PASS
- A1: 100% precision / 100% recall / 35/35 provenance
- A2: 100% structural representation; decimal defects 5 -> 0
- A3: 100% coverage / 100% critical coverage / 0% false additions / 88% atomicity / 92.86% certain precision / 87.5% error-abstention / 0 critical silent errors
- A4: GO alignment development
- B1 first: 83.33% FAIL
- B1.1: 100% on all human-correct alignment hard gates
- B2 first EE: 33.33% / 0% safe acceptance / MIXED_B2_REPAIR_REQUIRED
- B2.2 EE: 100% / 100% safe acceptance / 0 adversarial acceptance / PASS_B2_EXTRACTED_DEVELOPMENT
- GE and EG: 91.67% each, preserved as visible diagnostic evidence

## Completion

Gate B2:
**100% COMPLETE**

Gate B overall:
**100% COMPLETE**

Whole ACAD_PASS planning estimate:
**approximately 33% ±5%**

The increase reflects completion of the full V2.4 extraction/alignment development gate, not product readiness.

## Exact next authorized checkpoint

`AT0-EN V2.4 PRE-GATE-C — PIPELINE FREEZE + END-TO-END HOLDOUT PROTOCOL`

Purpose:
- freeze the complete verifier pipeline identity;
- freeze Gate C protocol, denominators, outcomes, safety/usability metrics and audit rules;
- define authentic end-to-end evaluation material without opening/labeling the untouched holdout before pipeline freeze;
- preserve prediction-first / label-second execution;
- obtain focused higher-model review because Gate C benchmark design is a high-stakes construct-validity decision.

Only after pipeline/protocol freeze may Gate C create/open a new untouched holdout.

Not authorized in this closure:
- new untouched holdout execution
- live transformation generation
- HW1-EN
- production readiness claims
