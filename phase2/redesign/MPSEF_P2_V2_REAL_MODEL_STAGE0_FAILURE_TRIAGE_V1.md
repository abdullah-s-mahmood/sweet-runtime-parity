# MP-SEF P2_V2 REAL-MODEL STAGE0 FAILURE TRIAGE V1

Date: 2026-10-01
Run: `36864163724`
Head SHA: `976d31d5de310a18bbff2a4d15e6d0f32981234b`
Conclusion: FAILURE

## Observed failure

The real-model Stage0 workflow reached model acquisition and runtime setup successfully, then failed before GED model inference with:

`AttributeError: 'BertTokenizerFast' object has no attribute 'cls_token_type_id'`

Failure location:

`mpsef_p2_v2_real_model_stage0.py -> build_ged_segments()`

The runner attempted:

`token_type_ids=[tokenizer.cls_token_type_id]`

## Classification

Primary:
`IMPLEMENTATION / RUNTIME INTERFACE`

Not:
- MODEL/CANDIDATE QUALITY;
- SCIENTIFIC LIMIT;
- GEC QUALITY;
- GED ACCURACY;
- GOLD/REFERENCE FAILURE.

## Reproducibility

Reproduced in GitHub Actions run:
`36864163724`

Python:
3.9.25

Tokenizer class observed by the Stage0 implementation:
`BertTokenizerFast`

The failure is deterministic for a tokenizer object that does not expose the non-standard `cls_token_type_id` attribute.

## Root cause

The Stage0 runner assumed a tokenizer attribute that is not part of the required public tokenizer interface.

For a single-sequence BERT input, token type IDs are segment IDs and are conventionally all zeros.

The current code already uses zero for:
- normal wordpieces;
- SEP.

Only CLS incorrectly depended on `tokenizer.cls_token_type_id`.

Therefore the correct narrow repair is to use segment ID 0 consistently for the entire single-sequence GED segment, or omit token_type_ids when the model supports default zeros.

For reproducibility and explicit traceability, P2_V2 Stage0 will keep token_type_ids and set them to zero for every token in the single input sequence.

## Scope

Affected:
real-model Stage0 GED segment construction.

Not affected:
- frozen P2 V1 artifacts;
- synthetic B01 identity tests;
- P1;
- P3;
- V3 legalizer/scorer history;
- any gold/reference data.

No project source or project gold was loaded by the failed real-model Stage0.

## Confidence

Root-cause confidence:
**HIGH**

The traceback points directly to an absent tokenizer attribute before model inference.

## Repairability

`CURRENT_CYCLE_PRE_GOLD`

The repair is allowed because:
- Stage0 is pre-project-source and pre-gold;
- no successful real-model Stage0 artifact has been frozen;
- the change corrects an implementation-interface assumption;
- it does not change linguistic thresholds or measurement policy.

## Safe next action

1. replace CLS token type ID with explicit 0;
2. assert `len(token_type_ids) == len(input_ids)`;
3. rerun real-model Stage0 only;
4. if another failure appears, triage it before further edits;
5. do not advance to Stage1 until real-model Stage0 passes all required identity/provenance checks.

## Historical artifact

Failed-run artifact:
- id: `11162703948`
- ZIP digest:
  `sha256:72ad108428a88822903bafebaacc0300323e8b7404eaf35c074820c82ff0d6d6`

The artifact lacks the result JSON because execution failed before result creation; it preserves environment/hash evidence only.
