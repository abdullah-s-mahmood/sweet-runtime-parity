# ACAD_PASS — Federation D0–D4 Architecture Synthetic Preflight Freeze V1

Date: 2026-10-09

State:
`FEDERATION_D0_D4_ARCHITECTURE_SYNTHETIC_PREFLIGHT_PASS`

Run:
`37891265928`

Artifact:
`11598720182`

Digest:
`sha256:57c5825ef18557769007d974bf9205516e333148b38aa61a6e3ebf3cba6728e5`

Scientific data used:
`FALSE`

Scientific encoder loaded:
`FALSE`

Scientific training performed:
`FALSE`

Torch:
`2.2.2+cu121`

Synthetic fixture:
- batch = 2
- sequence length = 12
- hidden size = 768

## D0

Native BIO head:
- trainable params = 6,921
- all gradient params finite = yes
- fixed BIO-valid Viterbi decoding = PASS
- synthetic loss = 2.498213052749634

No learned CRF transitions.

## D1

Native four-class typed span head:
- trainable params = 393,728
- score tensor = [2,4,12,12]
- all gradients finite
- synthetic loss = 4.539668560028076

## D2

Native BIO + human auxiliary heads:
- native params = 6,921
- auxiliary params = 4,921,600
- native and auxiliary gradients finite
- auxiliary loss weight = 0.25
- synthetic total loss = 3.550454616546631

## D3

Native span + human auxiliary heads:
- native params = 393,728
- auxiliary params = 4,921,600
- native and auxiliary gradients finite
- auxiliary weight = 0.25
- synthetic loss = 5.695857524871826

## D4

ModernBERT-family native span-head mechanics:
- head params = 393,728
- gradients finite
- same frozen span-head mechanics as D1
- synthetic loss = 4.538258075714111

## D5

`CANCELED_NO_OFFICIAL_SEMANTIC_TYPE_LABELS`

No replacement arm.

## Determinism

Seeded head initialization reproducibility:
PASS.

## Interpretation

The frozen D0-D4 head/loss/decoding mechanics execute and backpropagate without numerical or structural failure before loading any scientific encoder.

This closes architecture mechanics only.

The first scientific fit still requires:
- GPU runtime qualification;
- immutable per-fit data/runtime hash binding;
- final pre-fit closure review.

No scientific attempt is consumed by this preflight.
