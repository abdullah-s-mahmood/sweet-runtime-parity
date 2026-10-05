# AT0-EN V2.6 R4.2 — Run 3 Invalid Numeric Training State Freeze V1

Date: 2026-10-05
Status: INVALID TRAINING STATE / NOT A SCIENTIFIC PERFORMANCE RESULT

## Run identity

Run:
`37345588682`

Artifact:
`11363597185`

Artifact digest:
`sha256:412daf3ed4f1463e3ae03633f4c39981c553ef6b3e6c54c55a37bfea6f5971b6`

Summary canonical pre-hash:
`f4fc1b3420df38640cc6eb955863b2195aa37209c9c20c3e6bc8e5f9c5478bae`

Selected model SHA-256:
`71aba1841db1ea8e17eb9feeabcba2919f55b4a968ac57c7106c8e3a2c0b3ba0`

## Observed output

Mechanical state written by the trainer:
`R4_2_WITNESS_NOT_READY`

Raw dev metrics:
- macro F1 = 0
- micro F1 = 0
- all P/I/C/O precision and recall = 0
- no calibration threshold accepted any entity
- train_loss = 0.0

These values MUST NOT be interpreted as model performance because the model state is numerically invalid.

## Critical invalidity evidence

The loading log shows that direct:
`AutoModelForTokenClassification.from_pretrained(base_flax, from_flax=True)`
did not map the Flax base checkpoint into the token-classification architecture correctly.

The log reports:
- a large set of Flax BERT base weights as unused;
- a large set of PyTorch BERT base weights as newly initialized.

Independent artifact inspection then established:
- tensors total = 199
- tensors containing non-finite values = 199
- parameter values total = 108,898,569
- non-finite parameter values = 108,898,569
- non-finite fraction = 1.0

Thus the saved model is entirely NaN.

Additional evidence:
- checkpoint-197 model SHA = selected model SHA
- checkpoint-591 model SHA = selected model SHA
- train_loss = 0.0

The run did execute optimizer/trainer steps, but it did not produce a valid finite learned model.

## Scientific classification

`INVALID_TRAINING_STATE_DUE_TO_BASE_CHECKPOINT_CONVERSION_PATH`

This is NOT:
- evidence that BiomedBERT fails PICO extraction;
- evidence that the frozen calibration criteria are too strict;
- authorization to loosen calibration thresholds;
- authorization to inspect EBM/COVID/AD tests.

## Leakage guards preserved

- FactPICO used: FALSE
- consumed 60-RCT holdout used: FALSE
- opened 30-RCT diagnostic used: FALSE
- EBM/COVID/AD test files read by trainer: FALSE

## Corrective direction

Before any new full training:
1. load the official Flax checkpoint into `BertModel` / base architecture first;
2. assert all base parameters finite;
3. save the converted base as safetensors;
4. initialize `BertForTokenClassification` from that converted base;
5. assert only the classification head is newly initialized;
6. run a tiny train-only smoke batch;
7. require finite non-zero loss, finite gradients, parameter change after one optimizer step, and all parameters finite after the step;
8. discard smoke weights.

Only after this technical smoke PASS may another full train+calibration run be authorized.

Hugging Face reference basis:
- official documentation explicitly demonstrates `BertModel.from_pretrained(..., from_flax=True)`;
- token classification is defined as a classification head over the pretrained BERT hidden states.

No test-set inference is authorized.
