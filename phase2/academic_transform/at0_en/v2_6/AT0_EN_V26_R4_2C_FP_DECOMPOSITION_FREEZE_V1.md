# AT0 EN V2.6 R4.2C Dev False-Positive Decomposition Freeze V1

Date: 2026-10-06

## Diagnostic identity

- Run: `37477106239`
- Head SHA: `4c53cb4413cb03330103246092fce9707c66c314`
- Artifact: `11420250305`
- Artifact digest: `sha256:269736b2bfa42d3ca877dad42b26cbb8d0f77bf40de8d56074f9538c196110df`
- Candidate count: 404
- State: `R4_2C_DEV_FP_DECOMPOSITION_COMPLETE`

Guards:
- dev only
- no scientific training
- no test files
- no FactPICO
- no consumed holdout
- no threshold changes

## Global candidate error mechanism

Across all 404 frozen candidates:
- false positives = 134
- same-class wrong-boundary overlap = 70
- different-class exact-boundary = 13
- different-class wrong-boundary overlap = 9
- spurious/no overlap = 42
- individually plausible but jointly invalid boundary-pair candidates = 70
- cross-pair candidates = 3

## Frozen threshold 0.90 decomposition

Accepted = 281
TP = 225
FP = 56
overall accepted precision = 0.8007117438

FP kinds:
- SAME_CLASS_WRONG_BOUNDARY_OVERLAP = 33/56 = 58.93%
- DIFFERENT_CLASS_EXACT_BOUNDARY = 8/56 = 14.29%
- DIFFERENT_CLASS_WRONG_BOUNDARY_OVERLAP = 3/56 = 5.36%
- SPURIOUS_NO_OVERLAP = 12/56 = 21.43%

Critical mechanism:
- `joint_invalid_fp = 48/56 = 85.71%`

Per class at t=0.90:
- P: TP 37, FP 11, joint-invalid FP 11
- I: TP 91, FP 21, joint-invalid FP 15
- C: TP 15, FP 1, joint-invalid FP 1
- O: TP 82, FP 23, joint-invalid FP 21

## Confidence overlap

At t=0.90:
- TP span same-class score mean = 0.9691816711
- FP span same-class score mean = 0.9702529673
- TP R4.2B confidence mean = 0.9957355547
- FP R4.2B confidence mean = 0.9909565385
- TP boundary pair-min mean = 0.9071017950
- FP boundary pair-min mean = 0.7987882388

Interpretation:
The current span type classifier cannot separate true from false candidate spans by confidence. Its FP and TP same-class confidence distributions substantially overlap, and FP mean confidence is slightly higher than TP mean confidence. Confidence-threshold tuning is therefore not an evidence-supported rescue.

The boundary localizer contains useful signal, but independent start/end support does not model whether the two endpoints jointly form a valid entity span.

## Oracle sufficiency check

If the 48 t=0.90 joint-invalid FPs were perfectly rejected while preserving the observed TPs, the remaining theoretical per-class precision would be approximately:
- P = 37/(37+0) = 1.000
- I = 91/(91+6) = 0.938
- C = 15/(15+0) = 1.000
- O = 82/(82+2) = 0.976

This is an oracle diagnostic only, not an achieved result. It shows that the identified invalid-span mechanism is large enough in principle to account for the frozen precision-gate failure.

## Architecture conclusion

`ACCEPT_HARD_NEGATIVE_SPAN_VALIDITY_DIRECTION_FOR_R4_2D_DESIGN`

The next architecture should preserve the strong R4.2C type classifier and add an independent entity-span validity/rejection guard trained on TRAIN-ONLY invalid spans. It must not be trained on dev false positives.

Literature rationale:
- span-level NER literature explicitly models non-entity spans/negative spans;
- two-stage entity-span detection followed by type classification is established;
- hard false-positive span separation has direct precedent.

## Next authorized checkpoint

Design and preflight R4.2D:
`FROZEN_R4_2C + TRAIN_ONLY_HARD_NEGATIVE_SPAN_VALIDITY_GUARD`

Do not start full R4.2D training until the design, negative-generation policy, fixed validity decision rule, and smoke/preflight are frozen.
