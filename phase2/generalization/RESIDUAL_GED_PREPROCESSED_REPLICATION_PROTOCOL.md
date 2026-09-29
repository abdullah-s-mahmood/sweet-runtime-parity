# Phase 2 — Residual GED Preprocessing-Faithful Replication

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE PREPROCESSED GED FEATURES ARE COMPARED WITH MANUAL LABELS

## Trigger

The direct-text diagnostic on the consumed 14-event ORTHO V1 PASS population found:
- GED_TARGET_CLEAN_BOTH: 12 PASS, 12/12 supported, 0/2 partial PASS;
- GED_WINDOW1/2_CLEAN_BOTH: 8 PASS, 8/8 supported, but failed retention/review-burden criterion.

The direct-text protocol explicitly required a preprocessing-faithful replication before further use because the frozen GED models were trained with CAMeLIRA/contextual morphological preprocessing.

## Objective

Test whether the promising target-only separation survives when GED input is reconstructed from the official pinned CAMeLIRA-preprocessed QALB15 TRAIN source representation.

This remains a consumed-population diagnostic. No promotion and no fresh fourth slice are allowed from this replication alone.

## Frozen population and models

Population:
- same 14 frozen ORTHO_ISOLATED_COMMON_NOUN_V1 PASS events from run 36520233398.

Models unchanged:
- CAMeL-Lab/camelbert-msa-qalb14-ged-13 @ 447179dc63d186e4bff09a993e90e73ad622d571
- CAMeL-Lab/camelbert-msa-zaebuc-ged-13 @ 40c80685157d65504c942a8730f4f6b11c249679

Official preprocessing source:
- CAMeL-Lab/arabic-gec @ 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf
- data/gec/camelira_gec/qalb15/qalb15_train.src.txt

QALB15 TEST remains unread.

## Candidate reconstruction

For each frozen event:
1. use the raw line only to recover the target whitespace-word index;
2. align raw whitespace tokens to the official CAMeLIRA-preprocessed TRAIN line;
3. require an unambiguous target mapping;
4. construct the post-edit preprocessed candidate by replacing the mapped target with the candidate surface only when necessary;
5. if the official preprocessing already maps the source target to the same candidate surface, preserve that official preprocessed token;
6. do not use corrected TRAIN or manual labels during feature materialization.

Because CAMeLIRA preprocessing itself may normalize the candidate target, this replication can falsify the direct-text separation.

## Frozen policies

No policy changes:
- GED_TARGET_CLEAN_BOTH
- GED_WINDOW1_CLEAN_BOTH
- GED_WINDOW2_CLEAN_BOTH

The promising criterion is unchanged:
- PASS >= 10;
- partial PASS = 0;
- supported retained >= 10/12;
- review burden <= 4/14.

## Anti-leakage order

1. Reuse frozen ORTHO and AraBART artifacts.
2. Read QALB15 TRAIN RAW and official CAMeLIRA-preprocessed TRAIN source only.
3. Materialize mapping + GED decisions and hash them.
4. Leakage audit.
5. Only then read consumed manual labels.
6. No post-result tuning.

## Decision contract

- If GED_TARGET_CLEAN_BOTH remains promising under preprocessing-faithful input, it becomes eligible for retrospective replication on an earlier consumed population before any fourth disjoint slice.
- If it fails, close the residual-GED target-clean hypothesis and do not consume a fresh slice.

No Phase 3. No sealed benchmark.
