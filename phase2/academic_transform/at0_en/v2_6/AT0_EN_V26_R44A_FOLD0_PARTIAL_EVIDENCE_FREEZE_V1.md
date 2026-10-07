# ACAD_PASS R4.4-A — Fold 0 Partial Evidence Freeze V1

Date: 2026-10-07
Status: PARTIAL / NON-DECISION / WAIT_FOR_ALL_FIVE_FOLDS

## Identity
- Parent run: `37581447046`
- Fold: 0
- Job: `112661815077`
- Conclusion: SUCCESS
- Artifact: `11470897504`
- Artifact digest: `sha256:96b657e8928eb42e0960dcba88e884f3be80968cddfc09f72853386c3ff95db0`
- Candidate bank SHA256: `159b4924a919520fea98c3aacbebb73af0a4d87adf1a1efa0b4933f0550aa4ce`
- Design source SHA256: `f8b49420cb17a5cb3f67f3120f9362b5e6b15fbb148176eab20105790bab1e18`
- R44 manifest SHA256: `799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`

## Upstream models
B_CANDIDATE:
- epochs 10
- steps 1040
- train loss 0.12504862337194098
- model SHA256 `a45220fd96d8a9807894cd2565e0d32e039c651d9e076b42fa1935e916560e3d`

C_BOUNDARY:
- epochs 3
- steps 312
- train loss 0.32405298026517415
- model SHA256 `acd30f754ce626121c2de68b8802ab165d1d69dfb642e1114ad421d5d42dfe5c`

## Held-out outcome
- held-out docs: 52
- gold entities: 384
- candidate rows: 407
- exact-coordinate: 281
- exact-typed: 275
- coordinate precision: 0.6904176904
- coordinate recall: 0.7317708333
- native typed precision: 0.6756756757
- native typed recall: 0.7161458333
- goldless candidates: 21

Targets:
- NONE 126
- P 43
- I 118
- C 17
- O 103

FP / outcome taxonomy:
- EXACT_TYPED 275
- SAME_CLASS_WRONG_BOUNDARY 64
- SPURIOUS_NO_OVERLAP 58
- WRONG_TYPE_EXACT_COORD 6
- DIFFERENT_CLASS_WRONG_BOUNDARY 4

Thus 122/132 non-exact-typed candidates are either same-class wrong-boundary or spurious/no-overlap.

Per-class typed B recall:
- P 43/55 = 0.7818181818
- I 117/169 = 0.6923076923
- C 14/23 = 0.6086956522
- O 101/137 = 0.7372262774

Coordinate recall ceiling:
- P 0.7818181818
- I 0.6982248521
- C 0.7391304348
- O 0.7518248175

## Confidence diagnostic
Exact typed B confidence:
- n 275
- mean 0.9843976775
- median 0.9993239641
- q05 0.9393246412
- q95 0.9996096432

Other B confidence:
- n 132
- mean 0.9019439798
- median 0.9898763597
- q05 0.5562256962
- q95 0.9994200826

Interpretation: many false/non-exact candidates remain extremely high-confidence under B alone; a simple confidence threshold is unlikely to solve the precision problem.

## BIO diagnostics
- total unmatched/invalid runs: 25
- O_TO_I_RUN: 24
- CROSS_TYPE_I_RUN: 1
- valid source-gold initial continuation runs: 0

## Guards
All guards PASS:
- DESIGN-only training
- held-out fold not used for training
- VERIFY_INTERNAL not used
- old R4.3 SELECT not used
- historical DEV not read
- test not read
- other folds not read
- FactPICO not used
- consumed 60-RCT holdout not used
- no downstream head training
- final fixed epoch only

## Decision
NO architecture selection is permitted from Fold 0 alone.

Required next:
`COMPLETE_FOLDS_1_TO_4 -> AGGREGATE -> AUDIT_FULL_OOF_BANK -> ADVERSARIAL_REVIEW -> FREEZE_R44B`.
