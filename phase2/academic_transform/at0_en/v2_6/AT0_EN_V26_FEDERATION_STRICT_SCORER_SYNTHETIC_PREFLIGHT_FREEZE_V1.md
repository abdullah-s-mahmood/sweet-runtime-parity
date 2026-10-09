# ACAD_PASS — Federation Strict Scorer Synthetic Preflight Freeze V1

Date: 2026-10-09

State:
`FEDERATION_STRICT_SCORER_SYNTHETIC_PREFLIGHT_PASS`

Run:
`37879727833`

Artifact:
`11594166539`

Digest:
`sha256:1ca17f8f0403d405195d776d93d6e97a6e893b48de4ab48953d712c1096fa32d`

Scientific/benchmark data used:
`FALSE`

Verified:
- occurrence-coordinate typed exact matching;
- repeated equal surface strings remain separate by coordinate;
- both-empty contributes zero TP;
- wrong type = FP for predicted class + FN for gold class;
- boundary mismatch = FP + FN;
- duplicate prediction fails closed;
- nonfinite score fails closed;
- invalid coordinate fails closed;
- unknown document fails closed;
- threshold grid is exactly {.80,.85,.90,.95};
- synthetic pass fixture selects .95;
- synthetic no-pass fixture returns NO_HIGH_PRECISION_MODE_NOMINATED;
- paired family-cluster bootstrap is deterministic at seed 4404.

Synthetic exact fixture:
- TP=3
- FP=2
- FN=2
- micro P/R/F1=0.6/0.6/0.6.

This closes scorer MECHANICS only.
Real benchmark scoring remains prohibited until benchmark eligibility and full protocol closure.
