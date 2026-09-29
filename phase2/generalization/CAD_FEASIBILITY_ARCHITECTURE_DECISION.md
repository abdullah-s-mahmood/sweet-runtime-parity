# Phase 2 — CAD Feasibility Architecture Decision

Date: 2026-09-29

## Evidence

The QALB14 data probe passed by a large margin:
- train POS_ISOLATED_ORTHO: 23,565
- train negatives: 26,672
- dev POS_ISOLATED_ORTHO: 1,209
- dev negatives: 1,415

The CAD literature supports source/candidate sentence-pair discrimination. The original 2024 CAD paper uses BERT sentence encodings, mean pooling, and comparison features trained from GEC corpora. GRECO 2023 independently supports reference-free correction quality estimation but is English/DeBERTa based and is not used directly for Arabic.

## Selected feasibility architecture

Encoder:
- CAMeL-Lab/bert-base-arabic-camelbert-msa
- revision: 9c0a8968fc47b06469302963b68caa5ce5e943af
- frozen during feasibility training

Input:
- source and candidate target-centered windows
- maximum 12 whitespace words on each side of target
- each window encoded independently
- tokenizer truncation max_length=64 subwords

Sentence representation:
- mean pooling over non-padding encoder hidden states

Pair features:
- candidate_mean - source_mean
- abs(candidate_mean - source_mean)
- candidate_mean * source_mean

Classifier:
- StandardScaler
- LogisticRegression
- L2 regularization, C=1.0
- class_weight=balanced
- random_state=0
- max_iter=2000

Rationale:
- frozen encoder makes the first experiment computationally bounded and prevents current-label fine-tuning;
- target-centered context reduces dilution from unrelated distant learner errors;
- directional delta allows the classifier to model source->candidate repair;
- absolute/product features provide comparison information analogous to sentence-pair quality estimation.

This is a feasibility model, not the final CAD architecture.
