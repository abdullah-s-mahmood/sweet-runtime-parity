# ACAD_PASS — PICOX Four-Class Adapted Comparator Freeze V1

Date: 2026-10-09

State:
`PICOX_ADAPTED_COMPARATOR_RECIPE_FROZEN_PENDING_RUNTIME_AND_ADAPTER_PREFLIGHT`

Scientific fitting:
`NOT_AUTHORIZED`

Upstream source:
`WengLab-InformaticsResearch/PICOX@f3351c4786bf197efacfcefc1c1e66c36c245842`

Pinned notebook Git blobs:
- boundary train: `c60340fafe8d957e80f2a6eeaef38f116381b8c3`
- boundary inference: `f43a5ae1cf0d6566f1ae0c652cb6de583f4b482b`
- span train: `d71792113aac25741786e337161ec4dc7a276fb1`
- span inference: `89ff6b3ba06d600fbe286e531c2fbf876bf16e40`
- evaluation: `5eaae616eac61c71222e7a5bb68771d5caca6d07`

## 1. Verified upstream behavior

The public PICOX implementation uses:
- base model `microsoft/BiomedNLP-PubMedBERT-large-uncased-abstract`;
- P/I/O only, not separate C;
- boundary detector labels OUT/START/END/BOTH/IN;
- boundary training:
  - learning rate 5e-5;
  - 3 epochs;
  - weight decay .01;
  - epoch evaluation/save;
- span classifier:
  - multi-label sigmoid;
  - learning rate 2e-5;
  - batch size 16;
  - 3 epochs;
  - weight decay .01;
  - threshold .5;
- candidate spans are the Cartesian product of predicted starts and ends with start<=end;
- same-class NMS suppresses overlapping spans at IoU>0;
- published inference notebook sweeps boundary threshold:
  `{.20,.25,.30,.35,.40,.45,.50}`.

Important ambiguities/defects:
1. upstream task has no separate comparator C;
2. upstream boundary threshold sweep is executed on TEST in the notebook and cannot be copied into our confirmatory comparison;
3. span training reports best checkpoint `1510`, while span inference hard-codes checkpoint `3020`;
4. boundary inference hard-codes checkpoint `4599`;
5. upstream evaluation/task definitions are not strict four-class occurrence-level P/I/C/O.

Therefore the upstream published number is NOT a direct primary comparator score for ACAD_PASS.

## 2. Allowed adaptation

The comparator must preserve the PICOX architectural idea:
`BOUNDARY_DETECTOR -> START_END_CANDIDATES -> MULTILABEL_SPAN_CLASSIFIER`.

Only the following adaptations are allowed:

1. native labels become P/I/C/O;
2. preprocessing uses the same gold-independent ACAD_PASS source-compatible text pipeline used by the candidate system;
3. exact document/family training exclusions are identical to the candidate comparison cell;
4. scoring uses the frozen ACAD_PASS strict occurrence-level exact four-class scorer;
5. test-time threshold tuning is removed;
6. checkpoints are prospectively final-epoch only.

No extra:
- verifier;
- calibration model;
- LLM;
- ensemble;
- hard-negative mining;
- seed search;
- architecture sweep.

## 3. Boundary model

Encoder:
`microsoft/BiomedNLP-PubMedBERT-large-uncased-abstract`
with exact revision to be pinned in runtime closure.

Task:
five boundary labels:
- OUT
- START
- END
- BOTH
- IN

Training:
- full encoder fine-tuning;
- AdamW;
- LR 5e-5;
- weight decay .01;
- exactly 3 epochs;
- final epoch only;
- no early stopping;
- no best-checkpoint selection;
- same seed as corresponding comparison fit;
- batch size = upstream TrainingArguments default unless runtime closure proves an explicit upstream value; if unresolved before first fit, comparator is BLOCKED rather than guessed.

## 4. Boundary threshold

Prospective DEVELOPMENT-only grid copied from upstream code:
`{0.20,0.25,0.30,0.35,0.40,0.45,0.50}`

For each comparison training regime/seed:
- compute all seven boundary candidate populations on the authorized DEVELOPMENT partition only;
- run the frozen span classifier on each population;
- score with strict exact four-class micro-F1;
- choose maximum DEVELOPMENT micro-F1;
- tie -> higher boundary threshold.

Freeze chosen threshold before external TEST inference.

No TEST label or TEST metric may influence threshold selection.

## 5. Span classifier

Encoder:
same pinned PubMedBERT-large checkpoint family.

Inputs:
the exact token sequence between a predicted START and END inclusive.

Outputs:
four independent sigmoid channels:
P/I/C/O.

Training positives:
gold typed spans from authorized training data.

Training negatives:
PICOX-style synthesized/candidate non-entity spans generated solely from authorized training data under the upstream candidate-construction logic, adapted only to four labels.

Training:
- AdamW;
- LR 2e-5;
- per-device train batch 16;
- per-device eval batch 16;
- exactly 3 epochs;
- weight decay .01;
- final epoch only;
- no early stopping;
- no best-checkpoint selection.

Span class decision threshold:
`0.50`
fixed globally.

## 6. NMS

To remain faithful to upstream PICOX:
- same-class NMS is retained;
- overlap criterion `IoU > 0`;
- same-class overlapping candidate retention follows the upstream implementation's span-length rule.

Because this behavior may suppress legitimate overlapping same-class gold, report:
- pre-NMS strict metrics;
- post-NMS strict metrics.

Primary adapted-comparator result:
`POST_NMS`
because that matches upstream inference behavior.

Do not tune NMS.

## 7. Four-class semantics

Native P/I/C/O labels come only from corpora that natively distinguish them.

No:
- original EBM control subtype -> C promotion;
- TrialSieve NonStudyDrug -> C promotion;
- DISTANT-CTO intervention semantic type -> C promotion;
- C-TrO arm membership -> C promotion.

Auxiliary data streams for data-matched PICOX comparison are admitted only where the comparator can consume them without changing its two-stage architecture and where the governing external cell explicitly requires data matching.

If exact data matching is impossible without a new architecture:
report that comparator cell as `NOT_DATA_MATCHABLE` rather than inventing a new PICOX.

## 8. Seeds and attempts

External comparison seeds:
`44,45,46`

Every two-stage PICOX fit consumes:
- one boundary training stage;
- one span-classifier training stage.

No replacement attempt after scientific result visibility.

## 9. Scoring

Primary:
strict occurrence-level exact P/I/C/O micro-F1 using:
`federation_strict_scorer.py`

Also report:
- per-class exact P/R/F1;
- macro F1;
- boundary-only error decomposition;
- wrong-type decomposition;
- candidate recall before span classification;
- pre/post NMS counts.

Published PICOX P/I/O or merged-I/C metrics remain literature context only.

## 10. Comparator claim

Allowed:
`ADAPTED_PICOX_FOUR_CLASS_MATCHED_PROTOCOL`

Not allowed:
`EXACT_REPRODUCTION_OF_PUBLISHED_PICOX_SCORE`

A direct superiority claim is permitted only against this prospectively frozen adapted comparator under the same:
- benchmark;
- train/test exclusions;
- strict scorer;
- seeds;
- test protection.

## 11. Blocking conditions

Block PICOX comparator before fitting if any remains unresolved:
- PubMedBERT-large exact model revision;
- upstream-compatible batch/runtime behavior;
- source adapter;
- training negative-span construction;
- per-fit dataset manifest;
- DEVELOPMENT threshold selection implementation.

Blocked PICOX does not authorize substitution by an easier comparator after seeing ACAD_PASS results.
