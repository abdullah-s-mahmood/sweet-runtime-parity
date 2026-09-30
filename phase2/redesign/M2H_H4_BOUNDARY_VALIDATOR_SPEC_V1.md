# M2-H H4 Structural Boundary Validator — Specification v1

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION

## Purpose

Validate candidate Arabic word-boundary edits independently of the H1 text-editing model.

Supported operations:
- MERGE: two or more observed tokens should form one orthographic word.
- SPLIT: one observed token should be split into two orthographic words.

H4 is intentionally narrow.
It must prefer REVIEW/ABSTAIN over unsupported correction.

## Inputs

For each candidate:
- sentence tokens;
- exact candidate surface span;
- proposed SPLIT or MERGE operation;
- proposed result;
- sentence context.

The proposed operation may come from H1 or deterministic enumeration, but H4 may not use H1's confidence as validation evidence.

## Independent evidence families

### E1 — Exact structural legality
- proposed surface exists exactly in the sentence;
- operation changes only whitespace/boundary placement;
- no character substitution/deletion/insertion is hidden inside the boundary operation.

If E1 fails: REJECT.

### E2 — Morphological analyzability
Using frozen CAMeL morphology configuration:
- analyze original token(s);
- analyze proposed token(s);
- count valid analyses;
- record POS/clitic features.

This is evidence, not proof.

### E3 — Arabic clitic/boundary constraints
High-precision explicit rules may include:
- conjunction/preposition/article attachment constraints;
- impossible standalone proclitic fragments;
- impossible enclitic fragments;
- known orthographic attachment rules.

Rules must be enumerated and unit-tested before evaluation.

### E4 — Lexical plausibility
For SPLIT:
- both resulting tokens should be independently plausible or licensed by morphology.

For MERGE:
- the merged form should be morphologically/lexically plausible;
- the separated representation should contain evidence of an illegal split rather than merely two rare words.

### E5 — Contextual plausibility (optional subcomponent)
Only if needed after CALIBRATION:
- use a separately frozen language-model or corpus score;
- it must be independent of H1;
- threshold frozen on CALIBRATION only;
- no INTERNAL_EVALUATION tuning.

If no reproducible independent contextual model is selected, E5 remains disabled rather than improvised.

## Candidate generation internal to H4

### SPLIT proposals
For a single observed token:
- enumerate internal split points;
- retain only splits where both sides satisfy minimum Arabic/morphological plausibility;
- reject one-character fragments unless licensed as explicit Arabic clitics.

### MERGE proposals
For adjacent observed tokens:
- concatenate without changing characters;
- retain only if concatenation is morphologically plausible;
- require evidence that the separated tokens reflect an illegal boundary.

## Disposition

- SUPPORTED_BOUNDARY_ERROR
- REJECTED_BOUNDARY_ERROR
- UNCERTAIN_BOUNDARY
- NOT_APPLICABLE

A candidate is SUPPORTED only if:
1. E1 passes;
2. at least two independent non-H1 evidence families support the edit;
3. no hard rule contradicts it;
4. calibration score/decision rule is satisfied.

Otherwise use UNCERTAIN or REJECTED.

## Safety objective

H4 is not optimized for recall first.

Primary feasibility requirements on INTERNAL_EVALUATION, when n>=20 per operation:
- Split precision >=90%;
- Split recall >=70%;
- Merge precision >=90%;
- Merge recall >=70%.

If one operation has n<20:
- report exact counts;
- no broad promotion claim.

Hard stop:
- precision <80% for either sufficiently represented operation.

## Calibration

CALIBRATION may choose:
- rule subset;
- analyzability thresholds;
- optional contextual-score threshold.

After freezing:
- no changes using INTERNAL_EVALUATION.

## Audit outputs

For every boundary decision persist:
- exact span;
- operation;
- original tokens;
- proposed tokens;
- E1-E5 evidence;
- morphology analysis counts/features used;
- triggered explicit rules;
- final disposition;
- software/model versions and hashes.

## License/reproducibility constraint

Do not introduce Farasa as a required production dependency under v1 because its public repository states research-purpose-only licensing.

CAMeL code/data licenses must be separately recorded in the component manifest.

## Non-goals

H4 does not:
- correct spelling substitutions;
- decide full sentence correctness;
- replace H1 candidate generation;
- use LLM confidence;
- infer semantic rewrites;
- validate punctuation.

## Next checkpoint

Before implementation:
1. freeze exact CAMeL package/data versions;
2. enumerate the initial high-precision Arabic boundary rules;
3. verify H1 checkpoint identifiers and hashes;
4. freeze remaining-development split salt;
5. only then run software feasibility.
