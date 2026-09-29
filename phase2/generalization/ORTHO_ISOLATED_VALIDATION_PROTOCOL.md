# Phase 2 — ORTHO_ISOLATED_COMMON_NOUN_V1 Fresh Validation

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE THIRD-SLICE GOLD

## Objective

Validate the frozen ORTHO_ISOLATED_COMMON_NOUN_V1 lane unchanged on a third disjoint QALB-2015 L2 TRAIN slice.

## Fresh population

- Corpus: QALB-2015 L2 TRAIN.
- Recompute and exclude the original 50-line cross-model slice using seed phase2-cross-model-agreement-v1.
- Recompute and exclude the 50-line tri-model slice using seed phase2-trimodel-vote-v1 after excluding the first slice.
- From all remaining raw lines select the 50 lowest SHA-256 values of phase2-ortho-isolated-validation-v1|raw_line.
- QALB15 TEST remains unread.

## Frozen model revisions

- SWEET QALB14: CAMeL-Lab/text-editing-qalb14-nopnx @ 21286e56ce98a86362db540863f91c083b8970f9
- SWEET ZAEBUC: CAMeL-Lab/text-editing-zaebuc-nopnx @ 1da7198cb6eb8ae2de845ee32a3bfa61c186dbeb
- GED QALB14: CAMeL-Lab/camelbert-msa-qalb14-ged-13 @ 447179dc63d186e4bff09a993e90e73ad622d571
- AraBART QALB14: CAMeL-Lab/arabart-qalb14-gec-ged-13 @ 410588a318d988cdcfdbf64cf5745ed4adea0f6a

## Candidate evidence

Create exact single-token substitution UNANIMOUS_3 candidates only when all three frozen voters propose the same source span/base and candidate base, and no existing protected-risk veto fires.

## Frozen ORTHO_ISOLATED_COMMON_NOUN_V1

PASS only if ALL conditions hold:
1. exact UNANIMOUS_3 candidate;
2. equal-length single-character substitution in one of: Arabic alif/hamza set ا/أ/إ/آ; final ى/ي; final ه/ة;
3. reliable CAMeL contextual analyses for source and candidate;
4. source POS == candidate POS == noun;
5. analyzer-normalized lemma identity;
6. identical POS/person/gender/number/aspect/mood/voice/state/case;
7. identical prc0..prc3 and enc0;
8. no other non-KEEP event from any of the three voters within ±2 lexical tokens.

No rule, feature, threshold, POS class, neighborhood radius, or surface family may change during this validation.

## Anti-leakage order

1. Three raw-only voter jobs select the same third slice.
2. Voter outputs are materialized.
3. Exact UNANIMOUS_3 candidates are materialized.
4. ORTHO_ISOLATED_COMMON_NOUN_V1 PASS/REVIEW decisions are materialized and hashed using RAW only.
5. Only then may QALB15 TRAIN corrected text be opened.
6. Exact-gold PASS events count as automatic support.
7. Every non-exact PASS event receives bounded contextual adjudication.
8. No policy modification on this slice.

## Validation criterion

The frozen lane passes this fresh validation only if, after bounded review:
- PASS events >= 10;
- wrong PASS = 0;
- partial PASS = 0;
- unnecessary PASS = 0;
- protected-risk PASS = 0.

If PASS <10: UNPROVEN_LOW_COVERAGE.
Any wrong/partial/unnecessary PASS: DO_NOT_PROMOTE.

Even a clean result remains development-generalization evidence, not production precision. Independent human validation is still required before product auto-apply claims.

## Constraints

- no QALB15 TEST;
- no final sealed benchmark;
- no Phase 3;
- no QALB text persisted;
- no post-result tuning.