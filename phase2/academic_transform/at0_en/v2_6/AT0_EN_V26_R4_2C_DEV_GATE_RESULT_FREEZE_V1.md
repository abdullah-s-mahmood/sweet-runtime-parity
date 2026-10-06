# AT0 EN V2.6 R4.2C Development Gate Result Freeze V1

Date: 2026-10-06

## Run identity

- Workflow run: `37464774424`
- Trigger/head SHA: `b70d40b3f86738c2cdcb1e7864fd507fd1eedde3`
- Artifact: `11417809920`
- Artifact digest: `sha256:1144116b0f5bc026fa1f96eb2def07e4e640455e011a01b5b8f184732b900218`
- Compact extraction run: `37476218617`
- Compact artifact: `11418688116`
- Compact artifact digest: `sha256:5b04f4c6d4a714241a3b43a6c3106cdb5144339f0497c58436b474e35e75427b`

## Execution classification

The run completed all frozen development training and calibration work.

Final process state:
`COMPLETED_WITH_GATE_FAIL`

Failure class:
`SCIENTIFIC_FROZEN_DEV_CONSENSUS_GATE_FAIL`

This is not a technical failure.

## Model/training evidence

Boundary selected checkpoint:
- epoch 2
- step 394
- eval_loss 0.33189380168914795

Span selected checkpoint:
- epoch 3
- step 567
- eval_accuracy 0.8903061224489796
- eval_macro_f1 0.8962295846794422
- eval_loss 0.19887608289718628

Model hashes:
- boundary: `a56a24572ffd59b93c71e7b68b4ceb63f52ee17e6247fa5f4f857b826de788ae`
- span: `d531a61cf76e38cfec307e53a95382fbf3cb107d4a7b0d3677a1304b7f30b8a0`
- frozen R4.2B: `3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c`
- converted base: `3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68`

Candidate count: 404

## Frozen calibration results

### threshold 0.80
- macro precision 0.8164963348
- P precision/recall/accepted = 0.7708333333 / 0.6851851852 / 48
- I = 0.7833333333 / 0.5802469136 / 120
- C = 0.9411764706 / 0.5517241379 / 17
- O = 0.7706422018 / 0.5714285714 / 109

### threshold 0.85
- macro precision 0.8192846230
- P = 0.7708333333 / 0.6851851852 / 48
- I = 0.7966101695 / 0.5802469136 / 118
- C = 0.9411764706 / 0.5517241379 / 17
- O = 0.7685185185 / 0.5646258503 / 108

### threshold 0.90
- macro precision 0.8254464286
- P = 0.7708333333 / 0.6851851852 / 48
- I = 0.8125 / 0.5617283951 / 112
- C = 0.9375 / 0.5172413793 / 16
- O = 0.7809523810 / 0.5578231293 / 105

### threshold 0.95
- macro precision 0.5917980096
- P = 0.7872340426 / 0.6851851852 / 47
- I = 0.7920792079 / 0.4938271605 / 101
- C = 0.0 / 0.0 / 0
- O = 0.7878787879 / 0.5306122449 / 99

Chosen calibration: null.

## Scientific interpretation

Threshold-only rescue is rejected.

The best macro precision is 0.8254464286 at threshold 0.90, materially below the frozen >=0.90 macro requirement. P, I and O remain below the per-class >=0.90 precision gate; C is already above 0.90 at thresholds 0.80-0.90. At 0.95 C collapses to zero accepted cases, so simply increasing the common confidence threshold is not a defensible rescue.

A structural hypothesis now requires dev-only diagnostic testing:

The independent span classifier was trained only on true gold spans. It was not trained to reject malformed/wrong-boundary candidate spans. The current boundary guard checks candidate start and end probabilities independently at the fixed 0.25 generation threshold. Therefore a wrong candidate may survive when both endpoints look locally plausible even though the pair is not a valid gold-compatible span.

This hypothesis is not yet accepted as fact; it must be measured on the frozen dev outputs before any new training architecture is authorized.

## Guards

- no test files read
- FactPICO not used
- consumed 60-RCT holdout not used
- opened-30 diagnostic not used
- thresholds not changed
- EBM/COVID/AD tests remain closed

## Exact next authorized operation

Run one read-only DEV-ONLY R4.2C false-positive decomposition diagnostic using the frozen R4.2C models and frozen dev set.

The diagnostic must quantify, per class and threshold:
- exact-boundary false positives;
- same-class wrong-boundary false positives;
- different-class exact-boundary false positives;
- boundary endpoint support;
- span-classifier confidence for TP vs FP;
- how many FPs arise from individually plausible but jointly invalid boundary pairs.

Do not retrain or change the frozen gate until this diagnostic is frozen.
