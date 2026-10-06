# AT0 EN V2.6 R4.2D Span Validity Preflight Freeze V1

Date: 2026-10-06

Run:
`37479013072`

Artifact:
`11419504487`

Digest:
`sha256:576f52d692efc41a93a1b5a6500b6a79040db392a0d06751d1e7f49ca536b863`

State:
`R4_2D_SPAN_VALIDITY_PREFLIGHT_PASS`

Dataset construction:
- VALID positives = 3011
- raw boundary-shift selections = 3011
- unique boundary-shift INVALID = 3011
- raw non-overlap selections = 2531
- unique non-overlap INVALID = 2431
- total unique INVALID = 5442
- total examples = 8453
- positive/negative collisions = 0
- deterministic dataset SHA256 = `6038f5dd905271b27ad7be8f86118aa583f5adc06158b3adcbd9a7f02b724461`

Capacity:
- max wordpieces with specials = 58
- frozen max span width = 64 words

Smoke:
- loss = 0.761030375957489
- finite gradients = true
- one optimizer step succeeded

Frozen component identities:
- R4.2B model = `3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c`
- R4.2C boundary = `a56a24572ffd59b93c71e7b68b4ceb63f52ee17e6247fa5f4f857b826de788ae`
- R4.2C type = `d531a61cf76e38cfec307e53a95382fbf3cb107d4a7b0d3677a1304b7f30b8a0`
- converted base = `3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68`

Guards:
- TRAIN only
- dev not read
- tests not read
- no FactPICO
- no consumed holdout
- no full scientific training

Decision:
`AUTHORIZE_ONE_R4_2D_DEVELOPMENT_TRAINING_AND_FROZEN_DEV_CALIBRATION_RUN`

Frozen validity threshold:
`P(VALID) >= 0.50`

The old R4.2C threshold grid and exact scientific gate remain unchanged.
