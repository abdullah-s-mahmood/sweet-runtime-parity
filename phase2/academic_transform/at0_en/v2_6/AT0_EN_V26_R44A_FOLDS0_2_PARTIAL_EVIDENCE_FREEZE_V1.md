# ACAD_PASS R4.4-A — Folds 0+1+2 Partial Evidence Freeze V1

Date: 2026-10-07
Status: PARTIAL / NON-DECISION / WAIT_FOR FOLDS 3-4 + AGGREGATE

## Identity
Parent run: `37581447046`

Fold 0:
- artifact `11470897504`
- digest `sha256:96b657e8928eb42e0960dcba88e884f3be80968cddfc09f72853386c3ff95db0`
- candidate bank SHA `159b4924a919520fea98c3aacbebb73af0a4d87adf1a1efa0b4933f0550aa4ce`

Fold 1:
- artifact `11478992299`
- digest `sha256:dc4c33d3f6729e96267d1514640bc6d0c05757a6d83217d4ad29f35f403b7318`
- candidate bank SHA `4ed91bb8dbc8cd73a61f7242bd5369d3f2e6b80af107f48756c090c4b9fdf210`

Fold 2:
- job `112661815283`
- artifact `11486853863`
- digest `sha256:3a957b00e1173eda79881435c563febf4c32e1a16f1df22b1e791d850438d8d7`
- candidate bank SHA `11c5e17b5b669c618fb80b0f1ff4a8eb388b8aa2a66d5d79bfe057477803b9b0`

## Fold 2
- gold entities: 377
- candidates: 368
- exact coordinate: 282
- exact typed: 266
- native typed precision: 0.722826087
- native typed recall: 0.705570292
- coordinate precision: 0.766304348
- coordinate recall: 0.748010610
- goldless candidates: 23

Targets:
- NONE 86
- P 42
- I 122
- C 17
- O 101

Taxonomy:
- EXACT_TYPED 266
- SAME_CLASS_WRONG_BOUNDARY 44
- SPURIOUS_NO_OVERLAP 33
- WRONG_TYPE_EXACT_COORD 16
- DIFFERENT_CLASS_WRONG_BOUNDARY 9

Confidence:
- exact-typed B median 0.999086559
- other-candidate B median 0.997322589
- other-candidate B mean 0.946237173

BIO:
- total violation runs 25
- valid source continuation initial-I runs 1
- unmatched/invalid runs 24
- O_TO_I_RUN 19
- CROSS_TYPE_I_RUN 5
- INITIAL_I_RUN 1

## Combined folds 0+1+2 — descriptive only
- gold entities: 1138
- candidates: 1150
- exact coordinate: 842
- exact typed: 805
- NONE: 308
- goldless candidates: 68
- native typed precision: 805/1150 = 0.700000
- native typed recall: 805/1138 ≈ 0.70738
- coordinate precision: 842/1150 ≈ 0.73217
- coordinate recall: 842/1138 ≈ 0.73989

Combined taxonomy:
- EXACT_TYPED 805
- SAME_CLASS_WRONG_BOUNDARY 161
- SPURIOUS_NO_OVERLAP 132
- WRONG_TYPE_EXACT_COORD 37
- DIFFERENT_CLASS_WRONG_BOUNDARY 15

Among the 345 non-exact-typed candidates, 293 are either same-class wrong-boundary or spurious/no-overlap (~84.9%).

Combined typed recall by class:
- P: 128/163 ≈ 0.7853
- I: 330/499 ≈ 0.6613
- C: 44/69 ≈ 0.6377
- O: 303/407 ≈ 0.7445

Combined coordinate recall ceiling by class:
- P: 128/163 ≈ 0.7853
- I: 355/499 ≈ 0.7114
- C: 53/69 ≈ 0.7681
- O: 306/407 ≈ 0.7518

## Cross-fold conclusion
The same two dominant mechanisms recur in all three completed OOF folds:
1. same-class wrong boundary;
2. spurious/no-overlap proposals.

High-confidence non-exact candidates also recur in all three folds. Therefore simple B-confidence thresholding is not a credible primary solution.

The gap between coordinate ceiling and typed recall is especially visible for I and C, supporting a future head that may correct type when coordinates are exact. Boundary repair remains a separate later decision.

## Guards / decision
All reported fold access guards PASS.

NO architecture selection, threshold selection, VERIFY_INTERNAL access, old SELECT use or protected evaluation is authorized from the partial three-fold evidence.

Required next:
`FOLD3 -> FOLD4 -> AGGREGATE -> FULL_OOF_AUDIT -> ADVERSARIAL_REVIEW -> FREEZE_R44B`.
