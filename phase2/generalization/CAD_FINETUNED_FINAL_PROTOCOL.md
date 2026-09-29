# Phase 2 — Fine-Tuned Arabic CAD Final Feasibility Protocol

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE FINE-TUNING

## Role

This is the final justified sentence-level CAD feasibility escalation in Phase 2.

The preceding frozen-encoder CAD model failed externally:
- AUC 0.5844;
- zero-false-accept threshold retained 0/1,209 positives.

Published CAD fine-tunes BERT rather than relying on fixed embeddings. This protocol tests whether trainable Arabic contextual representations materially change the result without any current-label leakage.

## External data

Exactly the same frozen QALB14 example construction and deterministic samples as CAD_MODEL_FEASIBILITY_PROTOCOL.md:
- train: 4,000 POS_ISOLATED_ORTHO + 4,000 negatives;
- dev: 1,209 positives + 1,209 negatives;
- NEG_ORTHO_SUBEDIT is retained preferentially exactly as previously frozen.

No resampling after model scores.
No QALB15 corrected TRAIN.
No current Phase-2 adjudication labels during training or threshold calibration.

## Model

Base:
- CAMeL-Lab/bert-base-arabic-camelbert-msa
- revision 9c0a8968fc47b06469302963b68caa5ce5e943af

Architecture:
- AutoModelForSequenceClassification, num_labels=2;
- input segment A = target-centered source window;
- input segment B = target-centered candidate window;
- target context radius = +/-12 whitespace words;
- tokenizer max_length = 96 subwords;
- source is always first and candidate second because correction acceptability is directional.

Training:
- all encoder and classifier parameters trainable;
- AdamW;
- learning_rate = 1e-5;
- weight_decay = 0.01;
- epochs = 3;
- batch_size = 16 pairs;
- deterministic seed = 0;
- linear warmup over first 10% of optimizer steps;
- gradient clipping max_norm = 1.0;
- no current-label early stopping;
- final epoch checkpoint is used; QALB14 dev is used only for the frozen acceptance threshold and external reporting.

Runtime:
- Python 3.10
- torch 2.2.2+cpu
- transformers 4.44.2
- numpy <2

## External acceptance threshold

Unchanged safety policy:
1. score the frozen QALB14 DEV sample;
2. M = maximum accept probability among all DEV negatives;
3. threshold = next representable float greater than M.

External criterion, unchanged:
- dev negative false accepts = 0;
- dev positive PASS >= 300/1,209;
- dev positive retention >= 25%.

If external criterion fails:
- STOP this model family;
- do not score current QALB15 consumed labels;
- do not alter threshold, epochs, sample mix, context radius, or model based on the failed result;
- do not spend a fourth QALB15 TRAIN slice;
- Phase 2 Arabic auto-accept remains REVIEW-first.

## Consumed evaluation

Only if external criterion passes:
- score the same already-consumed third-slice 14 and earlier 36 populations;
- freeze probabilities and decisions before labels;
- use the same consumed criteria from CAD_MODEL_FEASIBILITY_PROTOCOL.md:
  - third 14: PASS >=10, supported PASS >=10/12, zero partial/wrong/unnecessary;
  - earlier 36: supported PASS >=24/34, zero partial/wrong/unnecessary;
  - nested strict-V1 19: PASS >=12, zero unsafe.

Only if all three pass may a fourth disjoint QALB15 TRAIN validation be considered.

## Hard stop

No third CAD architecture is authorized from this consumed evidence.

No Phase 3.
No sealed benchmark.
No QALB15 TEST.
No production promotion.
