# ACAD_PASS R4.4-A — Folds 0+1+2+3 Partial Evidence Freeze V1

Date: 2026-10-07
Status: PARTIAL / NON-DECISION / WAIT_FOR FOLD 4 + AGGREGATE

Parent run: `37581447046`

Fold 3:
- job `112661815321`
- artifact `11497847716`
- digest `sha256:4b034d73422602f5f34b741fc8a3b0c5c7902ae4da09ba8013a588c10a1d4fcc`
- candidate bank SHA `6b1b3b0f5a2da8057c1fe140361e9df953899af254aca2cd2d3cd24d65397c58`
- gold 377
- candidates 410
- exact coordinate 283
- exact typed 277
- native typed precision 0.6756097561
- native typed recall 0.7347480106
- NONE 127
- same-class wrong-boundary 50
- spurious/no-overlap 64
- wrong-type exact-coordinate 6
- different-class wrong-boundary 13
- goldless candidates 26
- other-candidate median B confidence 0.9912028313
- BIO unmatched/invalid runs 34
- all access/protection guards PASS.

Combined folds 0-3 descriptive evidence:
- gold 1515
- candidates 1560
- exact coordinate 1125
- exact typed 1082
- target NONE 435
- goldless candidates 94
- native typed precision 1082/1560 = 0.6935897436
- native typed recall 1082/1515 = 0.7141914191
- coordinate precision 1125/1560 = 0.7211538462
- coordinate recall 1125/1515 = 0.7425742574

Combined taxonomy:
- EXACT_TYPED 1082
- SAME_CLASS_WRONG_BOUNDARY 211
- SPURIOUS_NO_OVERLAP 196
- WRONG_TYPE_EXACT_COORD 43
- DIFFERENT_CLASS_WRONG_BOUNDARY 28

There are 478 non-exact-typed candidates; 407 are either same-class wrong-boundary or spurious/no-overlap = 85.15%.

Cross-fold conclusion:
- dominant error mechanism repeats in all four completed OOF folds;
- high-confidence false/non-exact candidates repeat in all four;
- simple B-confidence thresholding is not a credible primary fix;
- a contextual rejection verifier is strongly motivated;
- bounded boundary repair remains a separate conditional branch after full aggregate.

NO architecture selection or protected evaluation is authorized yet.

Required next:
`FOLD4 -> AGGREGATE -> FULL_OOF_AUDIT -> ADVERSARIAL_REVIEW -> FREEZE_R44B`.
