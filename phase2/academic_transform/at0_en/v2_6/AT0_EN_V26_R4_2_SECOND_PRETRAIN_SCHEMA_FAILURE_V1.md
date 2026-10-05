# AT0-EN V2.6 R4.2 — Second Pre-Training Schema Failure Freeze V1

Date: 2026-10-05
Status: PRE-TRAINING SCHEMA FAILURE / NO MODEL TRAINING OR INFERENCE

Run:
`37344000700`

Artifact:
`11359976305`

Artifact digest:
`sha256:7a7256ae8eac5f675f60e8483d83636f46a8ad27397669e63215752a98134ceb`

Failure:
`RuntimeError: unknown label 'B-C'`

Observed before any model load/training:
- EBM-NLPmod train labels contain B-C and I-C.
- EBM-NLPmod dev labels contain B-C and I-C.
- Comparator C is a first-class annotation category in the published PICO dataset.

Exact train token-label counts:
- O 28394
- B-P 426 / I-P 3919
- B-I 1326 / I-I 2977
- B-C 181 / I-C 292
- B-O 1067 / I-O 2905

Exact dev token-label counts:
- O 3404
- B-P 54 / I-P 452
- B-I 161 / I-I 362
- B-C 29 / I-C 25
- B-O 147 / I-O 389

Scientific boundary:
- model base weights loaded: NO
- training: NOT STARTED
- calibration inference: NOT STARTED
- test inference: NOT RUN

Classification:
`PRE_TRAINING_LABEL_SCHEMA_CONTRACT_DEFECT`

The failure is preserved and does not consume a scientific training attempt.
