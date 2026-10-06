# ACAD_PASS — R4.2C Source-Aligned Recovery Smoke Freeze V1

Date: 2026-10-06
Status: RECOVERY SMOKE PASS / NO SCIENTIFIC TRAINING

## 1. Background

The first authorized R4.2C development training attempt:
- run `37451685278`
- failed before the first training unit
- exact error: `RuntimeError: boundary truncation: 54 != 55`

Read-only diagnosis proved:
- no train/dev sentence exceeds frozen max_length 256;
- max encoded train/dev length is 141 wordpieces with specials;
- the pinned raw train file contains 17 zero-length surface-token rows across 12 sentences;
- the pinned source preprocessing filters tokenized-empty rows before training.

Recovery record:
`AT0_EN_V26_R4_2C_PRETRAIN_EMPTY_TOKEN_RECOVERY_V1.md`

Trainer correction commit:
`a74f064b473a5065886afb39926369305532b778`

## 2. Recovery smoke

Run:
`37455086281`

Conclusion:
`SUCCESS`

Artifact:
`11409796452`

Artifact digest:
`sha256:fd53c2eac731e7eb023f83efb2a646c76052fd5f99e7868648e0d5485551aae9`

Trainer SHA-256:
`56b2d77d548c3980700664e58557b33bc0dbde66f99bdff529812fe301e95ca8`

Smoke-result SHA-256:
`57da2eb93574f09d7d84efd800c885863567db3455195595b61a81e77a174a94`

Converted safe-base SHA-256:
`3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68`

R4.2B model SHA-256:
`3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c`

## 3. Full alignment guard

PASS:
- train sentences: 1576/1576
- dev sentences: 205/205
- full token-alignment guard: PASS

Source-aligned zero-length normalization:
- train removed rows = 17
- dev removed rows = 0
- train tag counts:
  - O = 5
  - I-I = 5
  - I-P = 6
  - I-O = 1

These counts exactly match the frozen raw-file audit.

## 4. Optimizer smoke

Boundary loss:
`1.8232231140136719`
finite.

Span-classifier loss:
`0.6865816712379456`
finite.

Exact scorer fixtures:
`PASS`

Both modules performed the smoke optimizer step with no scientific full training.

## 5. Guards

Confirmed:
- scientific_training_performed = false
- test_files_read = false
- FactPICO used = false
- consumed holdout used = false

Frozen scientific protocol remains unchanged:
- max sequence length = 256
- boundary lr/batch/epochs/weight decay unchanged
- span lr/batch/epochs/weight decay unchanged
- boundary generation threshold .25 unchanged
- final calibration grid unchanged
- exact gate unchanged

## 6. Decision

Classification:
`TECHNICAL_RECOVERY_VALIDATED`

The prior run `37451685278` did not produce a scientific training result and did not complete any scientific training unit.

The corrected implementation is now mechanically ready.

Exact next authorized checkpoint:
`ONE REPLACEMENT R4.2C DEVELOPMENT TRAINING + FROZEN-DEV CALIBRATION RUN`

After that run:
STOP before any EBM/COVID/AD test inference.

No FactPICO.
No consumed 60-RCT holdout.
No threshold relaxation.
