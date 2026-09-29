# Phase 2 — Residual GED Target-Clean Retrospective Replication

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE GED FEATURES ARE COMPARED WITH HISTORICAL LABELS

## Trigger

Two consumed-population diagnostics on the 14 fresh ORTHO_ISOLATED_COMMON_NOUN_V1 PASS events found the same target-only separation:

- direct-text GED_TARGET_CLEAN_BOTH: 12 PASS, 12/12 supported, 0/2 partial;
- preprocessing-faithful GED_TARGET_CLEAN_BOTH: 12 PASS, 12/12 supported, 0/2 partial.

The preprocessing-faithful replication used the official pinned CAMeLIRA QALB15 TRAIN source representation and therefore removes the main direct-text preprocessing objection.

## Objective

Retrospectively replicate the frozen GED_TARGET_CLEAN_BOTH rule on an earlier consumed population before spending any fourth disjoint QALB15 TRAIN slice.

## Population

Primary population:
- 36 historical events for which frozen ORTHO_MORPH_COMMON_NOUN_V1 == PASS in PHASE2_CONTEXTUAL_RESIDUAL_GUARD_FEATURES.jsonl.
- Historical label distribution is known from prior closed evidence: 34 supported, 2 partial.
- Labels MUST NOT be read by the feature materializer.

Nested strict population:
- 19 of those 36 also satisfy ORTHO_ISOLATED_COMMON_NOUN_V1 == PASS.
- Historical closed evidence: 19 supported, 0 unsafe.
- Used only as a retention sanity check.

## Models and preprocessing

Frozen models:
- CAMeL-Lab/camelbert-msa-qalb14-ged-13 @ 447179dc63d186e4bff09a993e90e73ad622d571
- CAMeL-Lab/camelbert-msa-zaebuc-ged-13 @ 40c80685157d65504c942a8730f4f6b11c249679

Official preprocessing source:
- CAMeL-Lab/arabic-gec @ 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf
- data/gec/camelira_gec/qalb15/qalb15_train.src.txt

Candidate artifact:
- canonical earlier tri-model run 36517205396
- artifact trimodel-arabart-q14

QALB15 TEST remains unread.

## Frozen rule

GED_TARGET_CLEAN_BOTH PASS iff the candidate target word is labeled UC by both frozen GED models under preprocessing-faithful candidate reconstruction.

No window rule, probability threshold, score calibration, label subset, third model, or dependency feature may be added during this replication.

## Target mapping

1. Recover the source target whitespace-word index from the frozen lexical span.
2. Align raw QALB15 TRAIN whitespace tokens to the official CAMeLIRA-preprocessed TRAIN source line.
3. If token counts match, use the same whitespace index.
4. Otherwise use deterministic SequenceMatcher blocks and accept only a unique one-to-one target mapping.
5. Ambiguous or non-one-to-one mapping => REVIEW / mapping_reliable=false.
6. If preprocessing already equals the candidate surface, retain the official token; otherwise replace only the mapped target token.

## Anti-leakage order

1. Select the 36 and nested 19 events using only frozen runtime decisions.
2. Download the frozen AraBART candidate artifact.
3. Read QALB15 TRAIN RAW plus official CAMeLIRA-preprocessed TRAIN source only.
4. Materialize target mapping, GED labels/scores, frozen PASS/REVIEW decisions, and hashes.
5. Leakage audit.
6. Only then read prior automatic/manual adjudication labels.
7. No post-result tuning.

## Pre-registered criterion for a fourth fresh slice

Primary 36-event population must satisfy all:
- PASS >= 28;
- partial PASS = 0;
- wrong PASS = 0;
- unnecessary PASS = 0;
- supported retained >= 28/34;
- REVIEW <= 8/36.

Nested strict-V1 subset:
- accepted >= 15/19;
- unsafe accepted = 0.

If any criterion fails:
- close GED_TARGET_CLEAN_BOTH as insufficient for fresh-slice promotion testing;
- do not consume a fourth slice.

If all criteria pass:
- rule becomes eligible for byte-for-byte freeze and fourth disjoint raw-only validation;
- still no production promotion.

## Constraints

No Phase 3.
No sealed benchmark.
No QALB15 TEST.
No rule tuning after labels.
No QALB text persistence.
