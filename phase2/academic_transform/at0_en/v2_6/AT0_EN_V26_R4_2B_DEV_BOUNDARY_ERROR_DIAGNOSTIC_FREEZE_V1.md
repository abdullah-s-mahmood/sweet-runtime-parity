# AT0-EN V2.6 R4.2B DEV-ONLY BOUNDARY ERROR DIAGNOSTIC FREEZE V1

Date: 2026-10-06
Timezone for user-facing reporting: Asia/Baghdad (UTC+3)

## Frozen source evidence

- R4.2B training run: `37409097042`
- R4.2B artifact: `11397202598`
- R4.2B artifact digest: `sha256:45d204d5f073aa5ecc5944dc49bee88be5bb677e0160b8c17720f2250de6fa71`
- Selected model SHA-256: `3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c`
- Frozen dev SHA-256: `3b12534fedec35660587e6a5084b0b8ff11267c1da4a2f5afe9aa16c4941340a`
- Dev-only diagnostic run: `37445035553`
- Diagnostic artifact: `11402997860`
- Diagnostic artifact digest: `sha256:6718d7007ed8b16f9644a33879e540ebadd26bcdbb248f98f21d5a74c8e0f5b1`

Guards remained true:
- no training in diagnostic
- no threshold change
- no EBM/COVID/AD test read
- no FactPICO
- no consumed 60-RCT holdout
- no opened-30 diagnostic

## R4.2B final dev performance

- entity-level micro precision: 0.6683168317
- entity-level micro recall: 0.6887755102
- entity-level micro F1: 0.6783919598
- macro F1: 0.6917395606
- macro precision: 0.6975931529

The source paper for this PICO dataset reports approximately 0.833 token-level micro F1 and 0.712 entity-level micro F1 on EBM-NLPmod. Our single-fold dev result is therefore not a total extraction collapse; the dominant deficit is exact-span reliability under ACAD_PASS's much stricter selective-precision requirement.

## Exact error decomposition

Predicted entities: 404
- EXACT_CORRECT: 270 (66.83%)
- BOUNDARY_ERROR_SAME_TYPE: 70 (17.33%)
- SPURIOUS: 42 (10.40%)
- TYPE_ERROR_EXACT_BOUNDARY: 13 (3.22%)
- TYPE_AND_BOUNDARY_ERROR: 9 (2.23%)

Gold entities: 392
- EXACT_MATCH: 270
- BOUNDARY_ERROR_SAME_TYPE: 64
- OMITTED: 42
- TYPE_ERROR_EXACT_BOUNDARY: 13
- TYPE_AND_BOUNDARY_ERROR: 3

Token-level collapsed P/I/C/O diagnostic:
- micro precision: 0.8425617078
- micro recall: 0.7801111797
- micro F1: 0.8101347017

This confirms a large gap between token recognition and exact-span correctness.

## High-confidence failure mechanism at the frozen 0.95 threshold

Total accepted predictions at >=0.95: 326
- exact correct: 249
- incorrect: 77

High-confidence error breakdown:
- same-type boundary errors: 47 / 77 = 61.04%
- spurious spans: 18 / 77 = 23.38%
- exact-boundary wrong-type errors: 9 / 77 = 11.69%
- type+boundary errors: 3 / 77 = 3.90%

Thus 59 / 77 = 76.62% of high-confidence errors are boundary/type-consistency errors.

Per class at 0.95:
- C: 14/15 exact, precision 93.33%, recall 48.28%; 1 boundary error
- I: 103/132 exact, precision 78.03%, recall 63.58%; errors = 14 boundary + 7 spurious + 6 exact-type + 2 type+boundary
- O: 92/127 exact, precision 72.44%, recall 62.59%; errors = 24 boundary + 8 spurious + 3 exact-type
- P: 40/52 exact, precision 76.92%, recall 74.07%; errors = 8 boundary + 3 spurious + 1 type+boundary

Representative failure pattern:
the model often predicts a semantically plausible subspan but not the annotation-exact phrase, e.g. truncating or extending P/I/O spans. Many such errors have min-token confidence above 0.999.

## Calibration conclusion

The original frozen global threshold set {0.80, 0.85, 0.90, 0.95} correctly produced NOT_READY.

A dense dev-only diagnostic found:
- no single global threshold can satisfy precision >=0.90, recall >=0.20, accepted >=10 for every P/I/C/O class simultaneously
- very high class-specific thresholds can satisfy the empirical gate on this already-observed dev split
- however, sentence-cluster bootstrap stability is inadequate for treating threshold-only redesign as robust evidence

Best observed bootstrap gate-pass rates for high class-specific thresholds were approximately:
- P: 0.68
- I: 0.50
- C: 0.71
- O: 0.73

Therefore:
`REJECT_THRESHOLD_ONLY_RESCUE`

Do not retroactively alter R4.2B thresholds or reinterpret its failure.

## Architecture decision

Decision:
`R4_2C_INDEPENDENT_BOUNDARY_AND_TYPE_AGREEMENT_GUARD`

Keep the frozen R4.2B BIO token classifier as a candidate generator.

Add an independent span-oriented verifier whose explicit tasks are:
1. exact start/end boundary validation
2. P/I/C/O type validation

Candidate acceptance rule:
- candidate generator predicts span/type
- independent boundary/type verifier must agree on exact span and type
- disagreement or insufficient confidence -> REVIEW
- verifier can never promote a critical contradiction or override existing fail-closed rules

Preferred architecture direction:
- biomedical encoder
- direct start/end or span-pair boundary scoring
- separate span type classification
- no hand-written dev-specific boundary heuristics
- no generic threshold relaxation

Theoretical diagnostic ceiling at threshold 0.95 if boundary/type errors were conservatively rejected while spurious errors remained:
- C precision: 100%
- I precision: 103/(103+7) = 93.64%
- O precision: 92/(92+8) = 92.00%
- P precision: 40/(40+3) = 93.02%

This is not a measured R4.2C result. It only establishes that boundary/type validation targets the correct error mass.

## Research support

- The original PICO paper reports the substantial token-vs-entity exact-span performance gap and uses exact span matching at entity level.
- Region-dependent/class-aware calibration literature shows that class imbalance can distort token-classification confidence, but calibration alone does not correct wrong boundaries.
- Recent biomedical/span NER literature supports explicit boundary detection plus span/category classification when boundary errors dominate sequence-labeling failures.

## Exact next authorized checkpoint

`R4_2C_TRAIN_ONLY_SPAN_GUARD_DESIGN_AND_PREFLIGHT`

Before any new scientific training:
1. inspect frozen TRAIN only for entity-span length/type distributions
2. freeze span candidate generation, negative sampling, boundary/type loss, and confidence definition
3. keep current dev as calibration/evaluation only
4. keep EBM/COVID/AD tests, FactPICO, consumed holdout, and opened-30 diagnostic closed
5. run a mechanics/preflight test only
6. only then authorize one R4.2C training run

Quality delta vs R4.2B:
- scientific model performance: unchanged
- diagnosis: materially improved
- dominant failure mechanism now quantified
- threshold-only rescue rejected
- architecture target narrowed from generic calibration repair to boundary/type agreement verification
