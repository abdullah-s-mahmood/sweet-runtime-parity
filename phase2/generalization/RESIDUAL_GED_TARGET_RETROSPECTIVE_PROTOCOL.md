# Phase 2 — Residual GED Target-Clean Retrospective Replication

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE GED FEATURES ON THE REPLICATION POPULATION

## Origin

The frozen preprocessing-faithful diagnostic on the consumed third-slice 14-event ORTHO V1 population found:
- GED_TARGET_CLEAN_BOTH PASS = 12/14;
- supported PASS = 12/12;
- partial PASS = 0/2;
- supported retention = 100%;
- review burden = 14.29%.

The official CAMeLIRA preprocessing had already normalized the target to the candidate surface in 14/14 cases, so the separation is contextual GED evidence rather than merely surface spelling recognition.

This remains hypothesis-generating evidence and must replicate on older consumed data before any fresh slice.

## Replication population

Earlier consumed canonical tri-model slice from run 36517205396.

Primary population:
- the 36 events passed by frozen diagnostic ORTHO_MORPH_COMMON_NOUN_V1;
- historical outcome: 34 supported, 2 partial.

Nested strict V1 subset:
- the 19 events passed by ORTHO_ISOLATED_COMMON_NOUN_V1;
- historical outcome: 19 supported.

No labels may be read during GED feature materialization.

## Frozen rule

GED_TARGET_CLEAN_BOTH PASS iff:
1. reconstruct candidate in the official pinned CAMeLIRA-preprocessed QALB15 TRAIN source representation;
2. target mapping is exact/reliable;
3. QALB14 GED target label == UC;
4. ZAEBUC GED target label == UC.

The ±1 and ±2 windows are descriptive ablations only and cannot replace the target-only primary rule.

No thresholds, score cutoffs, label subsets, model combinations, or windows may be changed during this replication.

## Models

- CAMeL-Lab/camelbert-msa-qalb14-ged-13 @ 447179dc63d186e4bff09a993e90e73ad622d571
- CAMeL-Lab/camelbert-msa-zaebuc-ged-13 @ 40c80685157d65504c942a8730f4f6b11c249679

## Preprocessing

Official pinned CAMeLIRA QALB15 TRAIN source:
CAMeL-Lab/arabic-gec @ 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf
data/gec/camelira_gec/qalb15/qalb15_train.src.txt

QALB15 TEST remains unread.

## Anti-leakage

1. Select 36 and nested 19 from frozen label-blind contextual-guard runtime decisions.
2. Reuse frozen AraBART candidate artifact from run 36517205396.
3. Read QALB15 TRAIN RAW + official CAMeLIRA TRAIN source only.
4. Materialize target GED labels/scores and decisions.
5. Hash and leakage-audit.
6. Only then read existing adjudication labels.
7. No post-result tuning.

## Pre-registered promising criterion

Primary rule is promising enough to justify a fourth disjoint validation only if:
- primary PASS >= 10;
- primary wrong PASS = 0;
- primary partial PASS = 0;
- primary unnecessary PASS = 0;
- nested strict-V1 PASS >= 10.

Passing this criterion still does not authorize production promotion. It only permits pre-registration of a fourth disjoint QALB15 TRAIN validation.

## Constraints

No QALB15 TEST. No sealed benchmark. No Phase 3. No QALB text persistence.
