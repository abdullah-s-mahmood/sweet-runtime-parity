# AT0 EN V2.6 R4.2D Development Gate Result Freeze V1

Date: 2026-10-06

## Run identity

- Workflow run: `37479970741`
- Head SHA: `fb3644e2f01189a0f5c0c676fa0f26d4d8ef2116`
- Artifact: `11422811514`
- Artifact digest: `sha256:7fd6cf920ff98bb19770a8a55efaae35ce73c11a5e4bf5a122b732238bc951e7`

## Execution classification

Final state:
`COMPLETED_WITH_GATE_FAIL`

Failure class:
`SCIENTIFIC_FROZEN_DEV_R4_2D_GATE_FAIL`

This is not a technical failure.

Training completed:
- epochs = 3/3
- global_step = 1587/1587
- train_loss = 0.2592304684
- validity model SHA256 = `14a70d925cfff7959cba4afa4a10b8f30413961eaea24ba308754dfc6d36f146`

## Frozen calibration

Best macro precision remained at threshold 0.90:

- macro precision = 0.8239836029
- P precision/recall/accepted = 0.7708333333 / 0.6851851852 / 48
- I = 0.8018867925 / 0.5246913580 / 106
- C = 0.9375 / 0.5172413793 / 16
- O = 0.7857142857 / 0.5238095238 / 98
- chosen calibration = null

Compared with R4.2C at threshold 0.90:
- R4.2C macro precision = 0.8254464286
- R4.2D macro precision = 0.8239836029
- delta = -0.0014628257 (-0.1463 percentage points)

At threshold 0.90:
- R4.2C accepted/TP/FP = 281 / 225 / 56
- R4.2D accepted/TP/FP = 268 / 214 / 54
- R4.2D removed 13 accepted candidates, but only 2 were FP and 11 were TP.

Therefore the validity guard worsened selectivity.

## Critical diagnostic evidence

At threshold 0.90, among R4.2D accepted candidates:
- TP validity score mean = 0.9537864043
- FP validity score mean = 0.9662910192

Thus the content-only validity classifier assigns, on average, slightly higher VALID confidence to false positives than to true positives.

Interpretation:
the current validity task learned entity-likeness rather than exact joint boundary validity. This is consistent with its input containing only the candidate span tokens. A one-token boundary shift can retain nearly the same semantic content as the gold span, while the surrounding contextual evidence needed to judge the exact boundary is absent.

## Guards

- no external test files read
- FactPICO not used
- consumed 60-RCT holdout not used
- dev false positives not used for validity training
- old threshold grid unchanged
- validity threshold fixed at 0.50
- frozen R4.2B and R4.2C identities unchanged

## Decision

`REJECT_CONTENT_ONLY_SPAN_VALIDITY_GUARD`

Do not tune its threshold on dev and do not rerun the same architecture.

## Next architecture direction

Design/preflight only:

`R4_2E = FROZEN_R4_2C + TRAIN_ONLY_JOINT_BOUNDARY_PAIR_VALIDATOR`

The validator should use contextual start/end representations from the frozen R4.2C boundary encoder and explicitly score the start/end pair jointly, rather than classify the candidate span content alone.

No full R4.2E training is authorized until its design and preflight are frozen.
