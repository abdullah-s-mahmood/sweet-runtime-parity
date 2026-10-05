# AT0-EN V2.6 R4.2 — Safe Flax Base-Load Smoke Freeze V1

Date: 2026-10-05
Status: PASS / TECHNICAL PRECONDITION SATISFIED / NO DEV OR TEST INFERENCE

Run:
`37354833183`

Artifact:
`11363823244`

Artifact digest:
`sha256:3b3ba1d741b0e7e4201e3b49686c83b853a28eccdb55170fb0d4476376dbb976`

Canonical smoke pre-hash:
`8a25b643a1b3603c141a432166dab3e52020d8f95845175463d24715c73ecbca`

Converted base safetensors SHA-256:
`3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68`

## Smoke result

The corrected path:
`official Flax checkpoint -> BertModel -> safetensors -> BertForTokenClassification`
passed every pre-training validity condition.

Observed:
- base parameter values: 109,482,240
- non-finite base parameter tensors: 0
- token-classification parameter values: 108,898,569
- non-finite token-classification tensors before update: 0
- supervised word labels in smoke batch: 344
- supervised entity word labels: 107
- finite positive pre-step loss: 2.950093984603882
- tensors with non-zero gradients: 199
- probe parameter changed after optimizer step: TRUE
- non-finite parameter tensors after optimizer step: 0

Probe:
`bert.encoder.layer.0.attention.self.query.weight`

## Leakage guards

- training sentences used: 8
- dev used: FALSE
- EBM/COVID/AD test used: FALSE
- FactPICO used: FALSE
- consumed 60-RCT holdout used: FALSE
- smoke weights discarded: TRUE

## Decision

`SAFE_BASE_CONVERSION_PATH_VALIDATED`

Authorized next:
- update the full R4.2 trainer to use this exact conversion path;
- preserve all frozen P/I/C/O labels, published hyperparameters, calibration thresholds and anti-degeneracy conditions;
- execute one full train+EBM-dev calibration attempt;
- STOP before EBM/COVID/AD test inference.

Not authorized:
- threshold relaxation;
- hyperparameter tuning from project results;
- test-set inspection;
- FactPICO or consumed-holdout reuse.
