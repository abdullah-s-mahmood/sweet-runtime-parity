# AT0-EN V2.6 — V5 Result Freeze and R4.2B Authorization V1

Date: 2026-10-06

## V5 valid completed result

Run: `37372306905`, attempt 2.
Artifact: `11385322641`.
Artifact digest: `sha256:1d52c85a514e56defe471a6690f5367d046f65c93f52659ed94ea3d104ffb7d0`.
Selected model SHA256: `65a790b56e232d847b84a2fd19df86a1fdc87e56eb2a6147e5d6b82fea8ab6d0`.
Summary SHA256: `8506c96636329a85639469072ef85f2ae0de24a885f482ba197258b7db049a6e`.

Training completed validly under early stopping at epoch 6.
Best checkpoint: `checkpoint-788` (epoch 4).
Best exact-entity macro-F1: `0.6841077577026645`.
Selected-model exact micro-F1: `0.665`.

Calibration failed all frozen thresholds.
At threshold 0.95:
- P precision 0.740000; recall 0.685185; accepted 50.
- I precision 0.843137; recall 0.530864; accepted 102.
- C precision 0.941176; recall 0.551724; accepted 17.
- O precision 0.831325; recall 0.469388; accepted 83.
- macro precision 0.838910.

State:
`R4_2_WITNESS_NOT_READY`.

The test boundary remained intact:
EBM test, COVID test, AD test, FactPICO, consumed 60-RCT holdout and opened-30 diagnostic were not used.

## Source-code audit

Pinned source:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO@bc4b878773192f38b2600ec830ca4208b82f7dc0`.

Published/source-code aligned values:
- learning rate 5e-5;
- train batch 8;
- fixed 10 epochs;
- weight decay 0.0;
- warmup steps 0;
- seed 42 in source script;
- eval batch 8;
- no early stopping/best-checkpoint selection in the original execution path.

V5 differed in weight decay, warmup, seed, eval batch and early-stopping/model-selection policy.

## R4.2B preflight

Run: `37408747717`.
Scientific analysis step: SUCCESS.
Artifact-upload step: technical post-analysis failure caused by an escaped upload path; this does not invalidate logged preflight output.

Preflight showed:
- train sentences over hard-truncation budget: 0/1576;
- dev sentences over hard-truncation budget: 0/205;
- train gold entities lost by current truncation: 0/3011;
- dev gold entities lost by current truncation: 0/392;
- maximum source-safe-split sequence: 139 wordpieces.

Therefore sequence truncation is NOT the cause on fold1.

## Authorized next experiment

Exactly one:
`R4_2B_SOURCE_CODE_HYPERPARAMETER_ALIGNED_DEV_ONLY`.

Keep unchanged:
- exact same safe BiomedBERT base identity;
- exact same fold1 train/dev bytes;
- labels;
- learning rate 5e-5;
- train batch 8;
- max sequence length 256;
- frozen calibration thresholds and anti-degeneracy gate;
- all test sets closed.

Change only to source-code alignment:
- seed 42;
- weight decay 0.0;
- warmup steps 0;
- eval batch 8;
- fixed 10 epochs;
- no early stopping;
- no load-best-model-at-end;
- HF AdamW-compatible optimizer on the already validated safe runtime.

If R4.2B still fails the frozen calibration gate, do NOT loosen thresholds.
Next action then becomes dev-only exact-boundary / wrong-type / hallucination error decomposition before any architectural redesign.
