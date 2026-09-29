# Phase 2 — External Arabic CAD Feasibility Model Protocol

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE MODEL TRAINING AND BEFORE CURRENT-LABEL EVALUATION

## Objective

Test whether a leakage-free Arabic source/candidate discriminator trained only on QALB14 gold-grounded local-completeness examples can separate locally complete orthographic repairs from partial repairs in the already-consumed QALB15 Phase-2 evidence.

No current QALB15 adjudication label may influence:
- training data;
- feature construction;
- classifier parameters;
- threshold calibration.

## External data

Pinned CAMeL-Lab/arabic-gec commit:
8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

Training:
- QALB-2014 L1 TRAIN source/gold only.

Calibration:
- QALB-2014 L1 DEV source/gold only.

No QALB14 TEST is required.
No QALB15 corrected data is used for training/calibration.
QALB15 TEST remains unread.

## Example construction

Use CAD_QALB14_LOCAL_COMPLETENESS_V1 exactly as frozen by PHASE2_CAD_DATA_FEASIBILITY.json.

Training sample:
- 4,000 POS_ISOLATED_ORTHO examples selected by lowest deterministic example hash;
- all available NEG_ORTHO_SUBEDIT examples up to 2,000 (723 observed);
- fill remaining negative slots to 4,000 with lowest-hash NEG_NEARBY_RESIDUAL;
- total training target = 8,000 balanced examples.

Dev calibration sample:
- use all 1,209 positive examples;
- include all 45 NEG_ORTHO_SUBEDIT examples;
- add the lowest-hash NEG_NEARBY_RESIDUAL examples until total negatives = 1,209;
- total dev target = 2,418 balanced examples.

No resampling after model scores are known.

## Model

Architecture is frozen in CAD_FEASIBILITY_ARCHITECTURE_DECISION.md.

Runtime pins:
- Python 3.10
- torch 2.2.2+cpu
- transformers 4.44.2
- scikit-learn 1.5.2
- numpy <2
- joblib 1.4.2

## Threshold calibration

After fitting on QALB14 TRAIN:
1. score the frozen QALB14 DEV sample;
2. let M be the maximum probability among all DEV negatives;
3. acceptance threshold = next representable float greater than M;
4. therefore DEV negative false accepts must equal zero by construction.

External feasibility criterion:
- DEV negative false accepts = 0;
- DEV positive PASS >= 300/1209;
- DEV positive retention >= 25%.

If this fails, stop before current QALB15 label evaluation.

## Current consumed evaluation

Only if external feasibility passes:
- materialize scores/decisions for the already-consumed third-slice 14 ORTHO_ISOLATED_COMMON_NOUN_V1 PASS events;
- materialize scores/decisions for the earlier consumed 36 ORTHO_MORPH_COMMON_NOUN_V1 PASS events and mark the nested strict-V1 19;
- current source/candidate text may be used to produce features but may not be persisted;
- all probabilities and PASS/REVIEW decisions are frozen and hashed before labels are opened.

Primary consumed criterion for further work:

Third-slice 14:
- PASS >= 10;
- partial PASS = 0;
- wrong/unnecessary PASS = 0;
- supported PASS >= 10/12.

Earlier 36:
- partial PASS = 0;
- wrong/unnecessary PASS = 0;
- supported PASS >= 24/34.

Nested strict V1 19:
- PASS >= 12/19;
- unsafe PASS = 0.

All three conditions must pass before any fourth disjoint QALB15 TRAIN slice can be considered.

## Decision contract

If external calibration passes but consumed criteria fail:
- do not tune threshold on current labels;
- record failure;
- a later fully fine-tuned CAD model would require a separate pre-registration and justification.

If all consumed criteria pass:
- freeze the feasibility model and threshold byte-for-byte;
- only then consider pre-registering a fourth disjoint raw-only QALB15 TRAIN validation.

No Phase 3.
No sealed benchmark.
No QALB15 TEST.
No production promotion.
