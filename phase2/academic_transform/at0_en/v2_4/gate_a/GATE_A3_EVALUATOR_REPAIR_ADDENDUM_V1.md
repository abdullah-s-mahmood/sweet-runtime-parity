# AT0-EN V2.4 Gate A3 — Evaluator Repair Addendum V1

Date: 2026-10-03
Status: EVALUATOR-CONTRACT REPAIR / EXTRACTOR FROZEN

## First-score provenance

Run:
`37143592151`

Artifact:
`11281531213`

Artifact SHA-256:
`a03c184f4bb8b0ee02888760e8fe34f1cdb7b04c4c2d7cf03ab82c3a6db6ca37`

Frozen first-score summary:
`phase2/academic_transform/at0_en/v2_4/gate_a/results/GATE_A3_FIRST_SCORE_V1_FROZEN.json`

First score:
`FAIL_CRITICAL_SILENT_ERROR`

The only alleged critical silent error was:
`EN12-AS-001`

Observed extraction:
- source meaning preserved as: evaluation includes three traffic densities
- subject concept: correct
- predicate: correct
- object concepts: correct
- polarity: correct
- modality: correct
- causality: correct
- extraction status: CERTAIN
- mismatch: assertion type `RELATIONAL` vs gold `SCOPE`

## Evaluator-contract mismatch

The frozen A3 scoring contract defines critical silent error through critical semantic failures such as:
- wrong critical predicate or role binding;
- wrong polarity/modality/causality;
- ignored critical context dependency;
- unsupported assertion;
- critical overmerge/omission.

It does NOT preregister `assertion_type` disagreement alone as sufficient to constitute a critical silent scientific error.

The V1 scorer incorrectly promoted every error on a CRITICAL gold assertion into a critical silent error, including an isolated assertion-type classification mismatch.

This makes the first critical-silent-error classification broader than the preregistered construct.

## Repair rule

The extractor remains frozen at:

`32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`

No extractor tuning is authorized.

The repaired evaluator will:
1. continue counting assertion-type mismatch as an extraction/classification error;
2. continue including it in certain-precision and field-accuracy diagnostics;
3. NOT classify assertion-type mismatch alone as a critical silent scientific error;
4. classify a CERTAIN prediction as a critical silent error only when its errors include a preregistered critical semantic failure:
   - FALSE_ADDITION
   - critical OVERMERGE / OVERSPLIT
   - SLOT_PREDICATE
   - SLOT_POLARITY
   - SLOT_MODALITY
   - SLOT_CAUSALITY
   - SLOT_SUBJECT_TERMS
   - SLOT_OBJECT_TERMS
   - SLOT_POPULATION
   - SLOT_TIME
   - SLOT_BASELINE
   - SLOT_SCOPE

No threshold is changed.

## Interpretation rule

The original first score remains preserved as evaluator negative evidence.

The repaired rerun is the canonical A3 score only because the evaluator is being brought into conformance with the pre-registered A3 construct while the extractor, development reference, slot reference, alignment logic, and thresholds remain fixed.
