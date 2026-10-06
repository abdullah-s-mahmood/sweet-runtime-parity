# ACAD_PASS AT0-EN V2.6 — R4.3 Train-Only Contextual Typed Pair Diagnostic Design V1

Date: 2026-10-07
Status: DESIGN FROZEN BEFORE PREFLIGHT; NO TRAINING AUTHORIZED

## 1. Independent-review decision

Senior architecture review verdict:
`RUN_ONE_MORE_TRAIN_ONLY_DIAGNOSTIC_BEFORE_ARCHITECTURE_SELECTION`.

Do not proceed directly to the previously proposed R4.2E or a full R4.3 architecture.

The purpose is one bounded comparison:

- H0: contextual typed MLP verifier
- H1: the identical contextual typed verifier plus an explicit class-specific biaffine start/end interaction

Everything except the pair-interaction mechanism must be held fixed.

## 2. Critical correction to prior interpretation

The R4.2C diagnostic field `joint_invalid_fp` must NOT be interpreted as 48 literal cross-entity start/end pairings.

At t=0.90:
- accepted FP = 56
- different-class exact-boundary FP = 8
- `joint_invalid_fp = 48` means the other accepted errors passed the independent 0.25 endpoint support checks yet were not exact gold boundaries.
- actual `gold_boundary_cross_pair` count was only 3 across all 404 candidates.

Therefore the evidence supports three live hypotheses rather than proving a single pair-interaction defect:

H0a. missing outside context;
H0b. negative-distribution mismatch;
H1. explicit endpoint interaction adds value beyond identical contextual inputs.

R4.2D also established that cropped candidate content alone is inadequate at its frozen operating point.

## 3. Data boundary

Use ONLY the pinned fold1 TRAIN file:

`BIDS-Xu-Lab/section_specific_annotation_of_PICO@bc4b878773192f38b2600ec830ca4208b82f7dc0`

Expected raw TRAIN SHA256:
`6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`

Do NOT read:
- the historical fold1 dev for this diagnostic;
- fold1 test;
- any EBM/COVID/AD external test;
- FactPICO;
- the consumed 60-RCT holdout;
- any other fold as replacement training data.

### Document isolation

The pinned CoNLL TRAIN contains explicit `-DOCSTART-` boundaries but does not carry explicit PMID values in the serialized file.

For this diagnostic:
- a document is the complete block between successive `-DOCSTART-` markers;
- exact token-sequence duplicate documents are grouped together before splitting;
- duplicate groups may never cross FIT/SELECT;
- sentence boundaries remain inside their owning document.

Do not invent PMID identities.

The preflight must STOP if document grouping cannot be reconstructed deterministically.

## 4. TRAIN-internal FIT/SELECT split

Create exactly one deterministic approximate 80/20 split using seed 42 at duplicate-document-group level.

The selection objective is prospective and fixed:
1. target 20% of document groups for SELECT;
2. preserve class presence and approximate gold span counts P/I/C/O;
3. preserve approximate total document/token mass;
4. deterministic ties by SHA256 of `seed|group_hash`.

The splitter may use gold labels because both partitions are within TRAIN, but may not inspect model predictions.

Freeze:
- document counts;
- duplicate-group counts;
- group membership;
- sentence/token counts;
- P/I/C/O span counts;
- FIT and SELECT content digests;
- split-manifest digest.

No redraw after any model result.

## 5. Ancestor isolation

Existing global R4.2B/R4.2C artifacts are references only and MUST NOT generate SELECT features or predictions.

After a later explicit training authorization, construct FIT-only replicas from the verified safe base:

### B candidate generator
Source-aligned R4.2B protocol:
- BiomedBERT base revision `d673b8835373c6fa116d6d8006b33d48734e305d`
- BIO P/I/C/O token classifier
- fixed 10 epochs
- learning rate 5e-5
- weight decay 0.0
- batch 8
- seed 42
- linear scheduler
- no early stopping
- final epoch checkpoint

### C boundary localizer
- OUT/START/END/BOTH/IN
- fixed 3 epochs
- learning rate 5e-5
- weight decay 0.01
- batch 8
- seed 42
- final epoch checkpoint
- boundary feasibility threshold 0.25

### C cropped-span type verifier
- exact gold FIT spans only
- P/I/C/O independent sigmoid formulation retained for legacy-C consensus
- fixed 3 epochs
- learning rate 2e-5
- weight decay 0.01
- batch 16
- seed 42
- final epoch checkpoint

IMPORTANT:
No epoch/checkpoint choice may be made from SELECT.
All three ancestors are trained only on FIT and frozen before H0/H1 training/evaluation.

## 6. Native candidate population

H0/H1 verify only native BIO proposals emitted by the FIT-only B replica.

Candidate coordinates:
`[start,end)`, width 1–64 words.

They do not create or repair spans in this diagnostic.

All SELECT gold entities remain in recall denominators even if B failed to propose them.

Candidate-ceiling recall must be reported per class.

## 7. Shared contextual feature extractor

Use the FIT-only frozen C boundary encoder on the COMPLETE normalized sentence.

For each candidate `[s,e)`, derive first-wordpiece contextual vectors:

- start = h_s
- end = h_(e-1)
- interior = mean(h_s ... h_(e-1))
- previous = h_(s-1), or a learned sentence-edge vector if s=0
- next = h_e, or a learned sentence-edge vector if e=len(sentence)
- learned width embedding, dimension 16, width bucket = exact width clipped at 64

Project each contextual vector independently to 128 dimensions before composition.

Encoder weights stay frozen during H0/H1 training.

## 8. Shared labels

One 5-way softmax:
`NONE / P / I / C / O`

For any candidate coordinate:
- exact gold P/I/C/O coordinate -> that class;
- otherwise -> NONE.

An exact gold coordinate of another class is NEVER relabeled NONE.

This diagnostic assumes the current flat single-label representation. Preflight must STOP if identical coordinates have incompatible labels.

## 9. H0 — contextual MLP

Shared feature vector:
`[start128 ; end128 ; interior128 ; previous128 ; next128 ; width16]`

Then:
- Linear -> 128
- GELU
- dropout 0.1
- Linear -> 5 logits

Loss:
multiclass cross entropy.

## 10. H1 — contextual MLP + biaffine endpoint term

H1 contains the identical H0 feature path and head.

Additionally, for each class k:
`b_k = start128^T U_k end128`

The five biaffine terms are added to H0's five logits before softmax.

No other architectural difference is permitted.

Report exact H0/H1 trainable parameter counts and their difference.

## 11. Head training protocol

For BOTH H0 and H1:
- same examples;
- same FIT-only frozen features;
- seed 42;
- AdamW;
- learning rate 0.001;
- weight decay 0.01;
- batch 64 candidate pairs;
- fixed 10 epochs;
- linear LR decay;
- warmup 0;
- gradient clipping 1.0;
- dropout 0.1;
- final epoch checkpoint;
- no encoder unfreezing;
- no early stopping;
- no seed shopping.

## 12. Frozen FIT-only negative construction

For every exact FIT gold span, construct deterministically, when available:

### A. Up to two local boundary perturbations
Enumerate candidate perturbations with each boundary shifted by 1 or 2 words, including one-boundary and two-boundary variants.

Eligibility:
- inside same sentence;
- end > start;
- width <=64;
- not an exact gold coordinate.

Choose at most two by deterministic SHA256 keyed by:
`seed|document_group|sentence|gold_type|s|e|LOCAL`.

### B. One composite negative
Build candidates using a start boundary from one gold entity and an end boundary from a DIFFERENT gold entity in the same sentence when the resulting span is valid and not exact gold.

Include same-class and different-class source-entity combinations.

Choose at most one deterministically.

### C. One native erroneous FIT-model proposal
After the FIT-only B replica is frozen, use at most one of its exact-span/class errors associated with the local document/sentence/gold neighborhood.

Do not mine SELECT.

If no eligible erroneous proposal exists, use one deterministic length-matched non-overlap background span as fallback.

### Labeling and deduplication
- exact gold coordinate -> true P/I/C/O class;
- all other selected coordinates -> NONE;
- deduplicate by document/sentence/start/end;
- retain provenance: GOLD, LOCAL, COMPOSITE, FIT_MODEL_ERROR, BACKGROUND_FALLBACK;
- hash the full deterministic training-example manifest.

## 13. Inference rule on SELECT

Retain the FIT-only legacy-C consensus requirements:

For threshold t in the pre-existing grid:
`{0.80,0.85,0.90,0.95}`

A native B proposal is automatically accepted only if:
1. B proposal confidence >= t;
2. start boundary support >=0.25;
3. end boundary support >=0.25;
4. width <=64;
5. cropped C type verifier same-class probability >=t;
6. no other cropped-C type probability >=t;
7. H0/H1 pair head top class equals the B proposal class;
8. H0/H1 top-class probability >=t.

Else REVIEW.

There is NO second pair-head threshold and no class-specific rescue threshold.

## 14. Scientific diagnostic gate on SELECT

Use the unchanged exact gate:
- exact span AND exact class;
- per-class precision >=0.90;
- per-class recall >=0.20;
- accepted >=10 per class;
- macro precision >=0.90.

Select the LOWEST t in the existing grid that passes all criteria for each head.

If neither H0 nor H1 passes:
`STOP_AFTER_TRAIN_INTERNAL_DIAGNOSTIC_FAIL`

If exactly one passes:
nominate that head.

If both pass:
prefer H0 unless H1 improves macro recall by >=0.02 absolute while preserving every gate.

This tie-break is frozen before results.

Also report, diagnostic only:
- native candidate ceiling;
- TP retention;
- FP rejection;
- class support;
- results at the prespecified approximately 80% baseline-TP-retention operating comparison;
- document-cluster bootstrap or Wilson uncertainty where valid.

These diagnostics do not replace the gate.

## 15. Preflight requirements BEFORE any training

The current authorized operation is PRE-FLIGHT ONLY.

Must establish:
- deterministic document boundaries;
- duplicate-document grouping;
- one immutable FIT/SELECT manifest;
- sufficient P/I/C/O support in both partitions;
- no duplicate group across partitions;
- exact coordinate-label consistency;
- cropped gold surface-token conflict audit across contexts;
- planned local/composite/background negative counts using gold only;
- zero gold/NONE coordinate collisions;
- tokenization alignment and maximum contextual length;
- H0/H1 tensor-shape and finite forward/backward smoke on discarded synthetic/mock features only;
- exact parameter counts;
- access guards proving historical DEV/test/FactPICO/60-RCT were not read.

No ancestor or head scientific training may occur in preflight.

## 16. Development-history rule

The historical fold1 DEV is now exposed development/regression evidence, not an independent architecture-selection benchmark.

After this TRAIN-only H0/H1 diagnostic and a separately frozen model/protocol, any later use of historical DEV must be explicitly labeled a regression/readiness check, not fresh model selection.

Protected external tests remain closed until separate authorization.

## 17. Stop boundary

After design + preflight:
STOP.

Return:
- split feasibility;
- exact counts/digests;
- collision/duplicate audit;
- negative-construction feasibility;
- H0/H1 mechanics;
- any blockers.

Do NOT train FIT ancestors or H0/H1 until a separate authorization checkpoint.
