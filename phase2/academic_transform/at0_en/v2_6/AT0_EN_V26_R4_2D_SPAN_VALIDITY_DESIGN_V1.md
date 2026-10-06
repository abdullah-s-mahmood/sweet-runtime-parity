# AT0 EN V2.6 R4.2D Hard-Negative Span Validity Guard — Design V1

Date: 2026-10-06

## 1. Motivation

R4.2C completed training but failed the frozen development precision gate.

At frozen threshold 0.90:
- TP = 225
- FP = 56
- 48/56 FP = 85.71% are individually boundary-supported but jointly invalid span pairs
- 33/56 FP = 58.93% are same-class wrong-boundary overlaps
- type-confidence does not separate TP from FP: mean same-class score TP=0.96918 vs FP=0.97025

Therefore confidence tuning of the existing type classifier is rejected.

## 2. Literature-supported design principle

Span-based NER literature provides direct precedent for explicitly modeling non-entity/invalid spans rather than training only on gold entity spans.

Relevant evidence:
- Tang et al., 2023, Boundary Offset Prediction Network for NER, Findings of EMNLP, DOI 10.18653/v1/2023.findings-emnlp.989: explicitly addresses non-entity spans and span-boundary relationships.
- Wei & Li, 2023, ScdNER, EMNLP: uses a first-stage binary classifier to decide whether a token sequence is an entity before type classification.
- Jia et al., 2021, JMIR Medical Informatics, PMID 34125076: uses negative sampling in a span-level medical NER model.

R4.2D applies the narrowest version of this principle to the observed ACAD_PASS failure.

## 3. Frozen architecture

R4.2D =
`FROZEN_R4_2B_CANDIDATE_GENERATOR
 + FROZEN_R4_2C_BOUNDARY_LOCALIZER
 + FROZEN_R4_2C_TYPE_CLASSIFIER
 + NEW_TRAIN_ONLY_HARD_NEGATIVE_SPAN_VALIDITY_GUARD`

Only the new validity guard is trained in R4.2D.

The frozen R4.2B, R4.2C boundary model and R4.2C type model MUST NOT be retrained for this checkpoint.

## 4. Validity task

Binary labels:
- VALID = 1
- INVALID = 0

Model:
- `BertForSequenceClassification(num_labels=2)`
- initialized independently from the same verified safe BiomedBERT base used by R4.2C
- no pickle weights
- final weights safetensors

Training hyperparameters:
- seed = 42
- learning rate = 2e-5
- weight decay = 0.01
- batch size = 16
- epochs = 3
- linear LR scheduler
- warmup_steps = 0
- max_grad_norm = 1.0
- dynamic padding
- maximum source span width = 64 words

No early stopping.
Use the fixed final epoch-3 validity model; do not select a validity checkpoint by frozen-dev consensus performance.

## 5. TRAIN-ONLY positive construction

Use the exact pinned source-aligned R4.2C TRAIN split after the already frozen empty-surface normalization.

Positive examples:
- every exact gold P/I/C/O entity span
- label VALID

No dev candidate or dev false positive may enter validity training.

## 6. TRAIN-ONLY hard-negative construction

For each gold positive span `[s,e)` in sentence `i`, construct at most two INVALID training examples.

### A. One boundary-shift hard negative

Candidate pool, in this frozen order:
1. `[s-1,e)`
2. `[s+1,e)`
3. `[s,e-1)`
4. `[s,e+1)`

A candidate is eligible only if:
- indices are inside the sentence;
- `end > start`;
- width <= 64 words;
- it is not exactly any gold entity span in that sentence.

From eligible candidates choose exactly one using deterministic seed-42 SHA256 selection keyed by:
`sentence_index | type | s | e | seed`.

If no eligible candidate exists, omit this negative for that positive.

### B. One length-matched non-overlap negative

Let `w=e-s`.
Enumerate all sentence spans of width `w` that:
- are not exact gold entity spans;
- do not overlap any gold entity span;
- satisfy width <=64.

Choose exactly one by deterministic seed-42 SHA256 selection using the same positive key plus the string `NON_OVERLAP`.

If none exists, omit this negative.

### Deduplication

Deduplicate INVALID spans by `(sentence_index,start,end)`.
A span is never allowed to be both VALID and INVALID.

No dev-derived hard-negative mining is allowed.

## 7. Fixed inference rule

For each frozen R4.2B candidate, retain the complete frozen R4.2C acceptance logic:
- R4.2B confidence >= t
- frozen independent boundary start support >= 0.25
- frozen independent boundary end support >= 0.25
- frozen same-class type confidence >= t
- no other class confidence >= t

with the existing frozen:
`t in {0.80,0.85,0.90,0.95}`.

Add exactly one new requirement:
- `P(VALID) >= 0.50`

The validity threshold 0.50 is FIXED prospectively.
There is no validity-threshold sweep.

## 8. Frozen scientific gate

Unchanged from R4.2C:
- exact span + exact class scoring only
- per-class precision >=0.90
- per-class recall >=0.20
- accepted >=10 per class
- macro precision >=0.90

No threshold relaxation.

## 9. Stop boundary

If no frozen threshold passes:
`STOP_AND_ANALYZE_R4_2D_DEV_ONLY_FAILURE`

If one frozen threshold passes:
`STOP_AND_REQUEST_EXTERNAL_TEST_AUTHORIZATION`

Do not open EBM/COVID/AD test sets during design, preflight, smoke, training, or frozen-dev calibration.

## 10. Preflight requirements before training

Must freeze:
- exact positive count
- exact hard-boundary negative count
- exact non-overlap negative count
- deduplicated INVALID count
- zero positive/negative collisions
- deterministic dataset digest
- tokenization capacity
- smoke finite loss/gradients for the validity model
- frozen model identities for R4.2B and R4.2C components

Only after all preflight/smoke requirements pass is one R4.2D development training + frozen-dev calibration run authorized.
