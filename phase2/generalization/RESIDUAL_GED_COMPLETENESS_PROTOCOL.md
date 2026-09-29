# Phase 2 — Residual GED Repair-Completeness Diagnostic

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE GED FEATURES ARE COMPARED WITH MANUAL LABELS

## Objective

Test whether residual grammatical-error detection (GED) around an already-applied ORTHO_ISOLATED_COMMON_NOUN_V1 candidate can identify the two fresh-validation partial corrections that survived tri-model voting, morphology identity, neighborhood isolation, post-edit stability, and dependency diagnostics.

This is diagnostic-only on the already-consumed 14-event fresh ORTHO PASS population. No promotion is allowed from this population.

## Models

Frozen GED models:
- CAMeL-Lab/camelbert-msa-qalb14-ged-13 @ 447179dc63d186e4bff09a993e90e73ad622d571
- CAMeL-Lab/camelbert-msa-zaebuc-ged-13 @ 40c80685157d65504c942a8730f4f6b11c249679

Both are token-classification GED-13 models. They are used only as residual-error signals.

## Important preprocessing limitation

Published GED models were trained with contextual morphological preprocessing. This diagnostic intentionally starts as a deployability probe on direct candidate text, matching the repository's earlier GED localization semantics. A positive result would require a preprocessing-faithful replication before any fresh validation.

## Population and candidate reconstruction

- Population: 14 frozen PASS events from run 36520233398.
- Candidate surfaces: reuse frozen AraBART artifact from the same run.
- Source: QALB15 L2 TRAIN RAW only.
- QALB15 TEST remains unread.
- No QALB text may be persisted.

## Frozen policies

After applying the frozen candidate edit, compute first-wordpiece GED labels for each whitespace word.

1. GED_TARGET_CLEAN_BOTH
   - target word is UC under both GED models.

2. GED_WINDOW1_CLEAN_BOTH
   - every word in target ±1 window is UC under both GED models.

3. GED_WINDOW2_CLEAN_BOTH
   - every word in target ±2 window is UC under both GED models.

No score threshold, label subset, window radius, or model combination may change after manual labels are read.

## Anti-leakage order

1. Download frozen AraBART candidate artifact from run 36520233398.
2. Read QALB15 TRAIN RAW only.
3. Reconstruct the 14 candidate sentences.
4. Run both frozen GED models.
5. Materialize label/score summaries, frozen policy decisions, hashes, and leakage audit.
6. Only then read PHASE2_ORTHO_ISOLATED_VALIDATION_MANUAL_REVIEW.json.
7. No post-result tuning.

## Promising criterion

A policy is promising enough to justify preprocessing-faithful replication only if:
- PASS >= 10;
- partial PASS = 0;
- supported retained >= 10/12;
- review burden <= 4/14.

Passing does not authorize promotion or a fourth fresh slice.

## Constraints

- diagnostic-only;
- no QALB15 TEST;
- no sealed benchmark;
- no Phase 3;
- no policy tuning after labels;
- no QALB text persistence.
