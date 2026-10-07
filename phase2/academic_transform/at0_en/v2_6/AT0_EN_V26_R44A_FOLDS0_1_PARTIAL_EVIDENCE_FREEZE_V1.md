# ACAD_PASS R4.4-A — Folds 0+1 Partial Evidence Freeze V1

Date: 2026-10-07
Status: PARTIAL / NON-DECISION / WAIT_FOR FOLDS 2-4 + AGGREGATE

## Identity
Parent run: `37581447046`

Fold 0:
- job `112661815077`
- artifact `11470897504`
- digest `sha256:96b657e8928eb42e0960dcba88e884f3be80968cddfc09f72853386c3ff95db0`
- candidate bank SHA `159b4924a919520fea98c3aacbebb73af0a4d87adf1a1efa0b4933f0550aa4ce`

Fold 1:
- job `112661815333`
- artifact `11478992299`
- digest `sha256:dc4c33d3f6729e96267d1514640bc6d0c05757a6d83217d4ad29f35f403b7318`
- candidate bank SHA `4ed91bb8dbc8cd73a61f7242bd5369d3f2e6b80af107f48756c090c4b9fdf210`

## Combined observed totals (descriptive only)
- gold entities: 761
- native candidate rows: 782
- exact-coordinate candidates: 560
- exact-typed candidates: 539
- target NONE: 222
- goldless candidates: 45

Descriptive aggregate rates from the two completed folds:
- native typed precision = 539 / 782 = 0.6893
- native typed recall = 539 / 761 = 0.7083
- coordinate precision = 560 / 782 = 0.7161
- coordinate recall = 560 / 761 = 0.7359

Combined taxonomy:
- EXACT_TYPED = 539
- SAME_CLASS_WRONG_BOUNDARY = 117
- SPURIOUS_NO_OVERLAP = 99
- WRONG_TYPE_EXACT_COORD = 21
- DIFFERENT_CLASS_WRONG_BOUNDARY = 6

Thus 216/243 non-exact-typed candidates are either same-class wrong-boundary or spurious/no-overlap.

## Cross-fold consistency
Fold 0:
- typed precision 0.6757
- typed recall 0.7161
- wrong-boundary 64
- spurious 58
- goldless candidates 21

Fold 1:
- typed precision 0.7040
- typed recall 0.7003
- wrong-boundary 53
- spurious 41
- goldless candidates 24

The same major error mechanisms recur independently in both folds.

## Confidence pattern
Fold 0 other-candidate median B confidence = 0.9898763597.
Fold 1 other-candidate median B confidence = 0.9778778553.

Therefore high-confidence false/non-exact candidates persist across both completed folds. B-confidence thresholding alone is unlikely to resolve the precision problem.

## BIO diagnostics
Fold 0:
- 25 unmatched/invalid runs: 24 O_TO_I + 1 CROSS_TYPE_I.

Fold 1:
- 26 unmatched/invalid runs: 24 O_TO_I + 2 INITIAL_I.
- valid source-gold initial continuation runs = 0.

Combined unmatched/invalid runs = 51.

## Decision
NO architecture or threshold selection from these two folds alone.

Current evidence strengthens:
1. need for realistic OOF negative supervision;
2. contextual verifier / rejection capability;
3. later bounded boundary-repair branch if the same mechanism persists in folds 2-4.

Required next:
`FOLD2 -> FOLD3 -> FOLD4 -> AGGREGATE -> FULL_OOF_AUDIT -> ADVERSARIAL_REVIEW -> FREEZE_R44B`.

No VERIFY_INTERNAL, old SELECT, DEV, test, other folds, FactPICO or protected data are authorized.
