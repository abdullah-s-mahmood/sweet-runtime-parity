# AT0-EN V2.6 — R4 Internal Holdout Result Freeze V1

Date: 2026-10-05
Status: INTERNAL HOLDOUT CONSUMED / R4.1B HOLDOUT GATE NOT PASSED / R4.2 TRIGGERED

## Execution identity

Workflow:
`AT0 EN V2.6 R4 ONE internal holdout open`

Run:
`37340581937`

Trigger head:
`e9e0b4aead491e02c9534980ab69c6f31b17e865`

Artifact:
`11358256711`

Artifact digest:
`sha256:808bce1258ccb2493385d81681b83bc2dbca010b0697f46909a84ab3db27f98c`

Result canonical SHA-256:
`750e0b11de8f1f4ceb88ef68b55a970d5a92a06957ae0ed77480130d802a63eb`

State:
`HOLDOUT_CONSUMED_AND_EVALUATED`

## Integrity / overlap

Holdout documents: 60
FactPICO frozen source hashes checked: 115
FactPICO overlap: 0

All 60 PICO-Corpus Git blob identities passed before extraction.

No FactPICO rerun occurred.
No external validation occurred.
No post-open threshold changes occurred.

## Frozen criteria and observed result

| Criterion | Frozen requirement | Observed | Result |
|---|---:|---:|---|
| short evidence <=3 chars | 0 | 2 | FAIL |
| empty documents | 0 | 0 | PASS |
| >128 assertions/doc | 0 | 0 | PASS |
| unresolved predicate rate | <=40% | 300/715 = 41.9580% | FAIL |
| non-CERTAIN rate | <=45% | 304/715 = 42.5175% | PASS |
| documents with non-CERTAIN <=50% | >=80% | 49/60 = 81.6667% | PASS |

Overall:
`FAIL_INTERNAL_HOLDOUT_GATE`

## Interpretation

This is a narrow development holdout failure, not an external scientific performance claim.

Positive evidence:
- 0 FactPICO overlap.
- 4/6 holdout criteria passed.
- non-CERTAIN criterion passed with 2.4825 percentage-point margin.
- document-level criterion passed with 1.6667 percentage-point margin.
- no empty representations.
- no assertion-envelope overflow.

Remaining gaps:
- unresolved rate exceeded threshold by 1.9580 percentage points.
- two <=3-character evidence fragments remain.

## Mandatory next path

Per the preregistered R4 design:
- do NOT rerun this 60-RCT holdout;
- do NOT tune R4.1B against holdout text;
- do NOT loosen thresholds;
- preserve this failure;
- transition to R4.2 architecture design for an auxiliary biomedical extraction witness or weak-supervision layer;
- preserve deterministic provenance and fail-closed fusion;
- freeze any model identity/calibration/evaluation protocol before inference.

The 60-RCT holdout is now permanently classified as:
`CONSUMED_INTERNAL_DEVELOPMENT_HOLDOUT`
