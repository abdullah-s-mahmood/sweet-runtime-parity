# AT0-EN V2.6 R4.2 — Pre-Training PICO Schema and Published-Setting Correction V1

Date: 2026-10-05
Status: FROZEN BEFORE FIRST MODEL TRAINING / INFERENCE

## Why correction is allowed

Both prior launches terminated before:
- base-model loading;
- training;
- calibration inference;
- any test inference.

Therefore no empirical model result has been observed and no result-driven tuning is possible.

## Source-schema correction

The pinned EBM-NLPmod train/dev files contain nine BIO labels:
`O, B-P, I-P, B-I, I-I, B-C, I-C, B-O, I-O`.

The published section-specific PICO work explicitly treats:
- P = Population
- I = Intervention
- C = Comparator
- O = Outcome

R4.2 label schema is corrected to preserve Comparator as an independent first-class class.

## Published-setting correction

Before first training, external literature review of the exact source paper established its reported best PubMedBERT NER setting:
- learning rate = 5e-5
- train batch size = 8
- epochs = 10

Therefore the project adopts the published setting rather than the earlier provisional 2e-5 setting.

Frozen after this correction:
- learning rate = 5e-5
- train batch size = 8
- eval batch size = 16
- gradient accumulation = 1
- maximum epochs = 10
- max sequence length = 256
- seed = 20261005
- weight decay = 0.01
- warmup ratio = 0.10
- early stopping patience = 2
- best checkpoint metric = entity-level macro F1

No further hyperparameter changes are authorized based on project training, dev, test, holdout, or FactPICO results.

## Corrected calibration anti-degeneracy contract

Classes:
`P, I, C, O`

Candidate entity-confidence thresholds:
`0.80, 0.85, 0.90, 0.95`

Choose the LOWEST threshold satisfying all:
1. per-class precision >= 0.90 for P, I, C, O;
2. per-class recall >= 0.20 for P, I, C, O;
3. accepted predictions >= 10 for each P, I, C, O;
4. macro precision across P/I/C/O >= 0.90.

If none qualifies:
`R4_2_WITNESS_NOT_READY`

No test set may influence threshold selection.

## Leakage and safety boundaries

Unchanged:
- FactPICO forbidden;
- consumed 60-RCT holdout forbidden;
- opened 30-RCT diagnostic forbidden for fitting/calibration;
- test sets remain unopened by trainer;
- witness cannot independently create PASS_CANDIDATE;
- deterministic contradictions remain non-overridable.
