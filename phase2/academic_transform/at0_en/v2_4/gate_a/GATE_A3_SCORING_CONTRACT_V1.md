# AT0-EN V2.4 — Gate A3 Extractor Validation Contract V1

Date: 2026-10-03
Status: FROZEN PRE-SCORE / DEVELOPMENT-ONLY

## Scope

A3 evaluates the already-frozen A2 source extractor against the existing six-case development reference.

No extractor tuning is permitted before the first A3 score.

This is development validation, not untouched-holdout evidence.

The project has already inspected A2 outputs qualitatively during A2 red-team. Therefore A3 must not be described as blind or independent evaluation.

## Bound extractor

A2 source assertion extractor SHA-256:
`32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`

Canonical schema SHA-256:
`df986f759a114bd86525b84f00f8d2f362d71bb31546441992291d21c5ebd69f`

Development reference:
`phase2/academic_transform/at0_en/v2_4/gate0/GATE0_DEV_REFERENCE_V1.jsonl`

## Evaluation principles

1. Exact string equality is NOT the primary claim-alignment metric.
2. Evidence/provenance spans provide the deterministic alignment backbone.
3. One prediction may align to multiple gold assertions and vice versa.
4. Such many-to-many alignment is reported explicitly and contributes to atomicity/split-merge diagnostics.
5. Semantic slot scoring is performed only for fields with explicit pre-scored gold annotations.
6. No embedding, NLI, LLM judge, or learned semantic scorer is used in the A3 scoring program.
7. A correct-looking aggregate score cannot hide a critical silent error.

## Metrics

### A. Claim-set coverage and focus
- gold assertion coverage: gold assertions aligned to at least one extracted assertion / all gold assertions
- critical gold coverage
- false-addition rate: extracted assertions aligned to no gold assertion / extracted assertions
- uncovered gold IDs
- unaligned extracted IDs

Alignment uses source evidence-span overlap/containment, not proposition-string similarity.

### B. Atomicity / split-merge
- one-to-one extracted assertions
- overmerged extracted assertions: one extracted assertion aligned to >1 gold assertion
- oversplit gold assertions: one gold assertion aligned to >1 extracted assertion
- atomic one-to-one rate

Overmerge is not automatically a semantic error if qualifiers remain recoverable, but it is an atomicity failure for source-claim extraction.

### C. Explicit semantic-slot fidelity
A fixed A3 slot-reference supplement defines only fields that are materially scorable:
- expected normalized predicate class
- expected polarity
- expected modality
- expected causality
- required population/time/baseline where material
- context-dependency/coreference expectation
- selected critical subject/object concepts

Slot accuracy is scored only on gold assertions with an unambiguous one-to-one alignment.
Overmerged assertions are not given semantic-slot credit by averaging across gold claims.

### D. Context/decontextualization detection
For gold assertions explicitly marked context-dependent:
- detection recall = aligned predictions that record a relevant unresolved/context dependency
- false context alarm rate on gold assertions marked context-independent

A2 is not required to resolve all context; correct abstention/detection is acceptable.

### E. Abstention calibration diagnostic
Each aligned prediction is classified after gold comparison as:
- CLEAN
- ERROR_OR_ATOMICITY_FAILURE

Then report:
- certain precision = CLEAN predictions marked CERTAIN / all CERTAIN predictions
- silent error rate = erroneous predictions marked CERTAIN / all predictions
- error-abstention recall = erroneous predictions marked UNCERTAIN/AMBIGUOUS / all erroneous predictions
- unnecessary abstention rate = CLEAN predictions marked UNCERTAIN/AMBIGUOUS / all CLEAN predictions

These are diagnostics, not probability calibration.

### F. Critical silent error gate
A critical silent error is any `CERTAIN` prediction with:
- critical gold assertion omitted through that alignment;
- wrong critical predicate/role binding;
- wrong polarity/modality/causality where explicitly annotated;
- critical context dependency silently ignored;
- unsupported assertion with no gold alignment;
- an overmerge that collapses multiple critical gold assertions and loses their separability.

A3 cannot receive a readiness PASS if any critical silent error is observed.

## A3 result classes

- `PASS_DEVELOPMENT`: zero observed critical silent errors and extractor diagnostics meet the pre-registered development thresholds.
- `MIXED_REPAIR_REQUIRED`: no catastrophic contract failure, but thresholds fail or non-silent extraction errors are material.
- `FAIL_CRITICAL_SILENT_ERROR`: at least one critical silent error is observed.
- `INVALID_EVALUATION`: scorer/reference integrity is insufficient for a valid A3 judgment.

## Pre-registered development thresholds

These thresholds are diagnostic and do not authorize end-to-end verification:

- critical gold assertion coverage: >= 95%
- overall gold assertion coverage: >= 90%
- false-addition rate: <= 10%
- atomic one-to-one rate: >= 75%
- certain precision: >= 90%
- error-abstention recall: >= 80%
- critical silent errors: **0**

If critical silent errors > 0, the result is `FAIL_CRITICAL_SILENT_ERROR` regardless of aggregate metrics.

No threshold may be weakened after viewing the A3 score.

## Stop rule

After the first A3 score:
- freeze all metrics and failures;
- do not silently tune and overwrite the first score;
- any extractor repair creates a versioned development iteration;
- Gate A4 interprets readiness only after preserving the original A3 result.

No candidate-text alignment, live generation, HW1-EN, or untouched holdout is authorized in A3.
