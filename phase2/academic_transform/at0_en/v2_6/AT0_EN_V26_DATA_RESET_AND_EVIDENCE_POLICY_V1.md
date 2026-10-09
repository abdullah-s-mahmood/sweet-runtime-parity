# ACAD_PASS — Data Reset and Evidence Policy V1

Date: 2026-10-08

State:
`POLICY_REVIEWED_WITH_SUPERSEDING_FEDERATION_CONDITIONS`

Purpose:
define exactly what may and may not be "reset" when rebuilding ACAD_PASS from the best methods discovered so far.

This file does NOT authorize model training.

## 1. Core rule

A computational reset CAN erase:
- model weights;
- optimizer state;
- checkpoints;
- fitted calibrators;
- cached predictions;
- stochastic training history.

A scientific reset CANNOT erase:
- the fact that a dataset was inspected;
- the fact that its labels influenced architecture/model/loss/threshold choices;
- prior score knowledge;
- manual error analysis;
- post-hoc feature decisions;
- published benchmark knowledge.

Therefore previously exposed data cannot become genuinely untouched prospective evidence merely by retraining from zero.

## 2. Correct use of previously exposed data

Previously exposed datasets may be promoted to:
`TRAIN/DEVELOPMENT_ONLY`

They can legitimately be:
- merged;
- reprocessed from raw sources;
- relabeled only through already-published human gold;
- used for representation learning;
- used for weak/semi-supervised learning;
- used for fixed cross-validation;
- used for ablation/mechanistic analysis.

They may NOT be described as:
- fresh test;
- prospective unseen validation;
- independent final evaluation
if they previously influenced ACAD_PASS decisions.

## 3. Valid "from-scratch" final rebuild

A valid final rebuild can:

1. freeze one complete method before external evaluation;
2. delete all learned ACAD_PASS weights/checkpoints;
3. rebuild features/candidates from raw source text;
4. train from random/pretrained initialization using every authorized TRAIN/DEV corpus;
5. choose all hyperparameters only through frozen development protocol;
6. emit immutable predictions for external benchmark(s);
7. join external gold exactly once under a frozen scoring script.

This yields valid external evidence if the external benchmark did not influence model selection under the claimed protocol.

## 4. Public benchmark evidence

A public dataset does NOT need to be secret to support a benchmark claim.

If:
- official train/dev/test splits are preserved;
- test labels are not used for tuning;
- the evaluation script is fixed;
- no post-test model/threshold selection is performed;
- comparator systems use the same task definition/metric,

then performance can be reported as a valid benchmark result.

However it is a:
`PUBLIC_BENCHMARK_RESULT`

not automatically:
`PROSPECTIVE_INDEPENDENT_CLINICAL_VALIDATION`.

## 5. Multi-corpus evidence hierarchy

Preferred hierarchy without new local expert annotation:

### Level A — official public human-gold test sets
Use official held-out test sets of published human-annotated corpora.
Purpose:
head-to-head comparison with published systems.

### Level B — leave-one-corpus-out generalization
For corpus D_k:
- train/fix on all other authorized corpora;
- evaluate exactly once on D_k;
- repeat across corpora using one frozen global procedure.

Purpose:
test distribution/domain generalization.

Corpus folds are not independent patient/trial replicates.
Report corpus-specific and pooled descriptive metrics.

### Level C — external rich-schema transfer tests
Use human-annotated resources whose schema differs from flat P/I/C/O, such as TrialSieve or C-TrO, only through a prospectively frozen mapping or auxiliary-task evaluation.

Do not call mapped labels direct native PICO gold without validating construct compatibility.

### Level D — genuinely prospective fresh evaluation
Requires a future source not used in development, whether newly annotated or a later independently published human-gold corpus.

This is strongest but is NOT required to build or compare a high-performing system now.

## 6. ACAD_PASS historical data classification

All data used in:
- R4.x;
- R44;
- R44B;
- R44C;
- FactPICO;
- consumed 60-RCT holdout;
- old SELECT;
- current DESIGN;
- any opened diagnostic set

must remain:
`EXPOSED_DEVELOPMENT_EVIDENCE`

unless a dataset-specific provenance audit proves otherwise.

VERIFY_INTERNAL remains protected and is not automatically reclassified by this policy.

## 7. Historical method knowledge may be retained

The following are method knowledge, not test labels, and may be retained prospectively:

- strict source/runtime parity;
- immutable provenance and manifests;
- document-level split isolation;
- pair-exclusion/cross-fitting when stacking predictions;
- exact population preservation;
- full-gold recall denominators;
- fail-closed missing/duplicate/nonfinite handling;
- Title + Methods focus where task construct matches;
- separate P/I/C/O target when native gold supports it;
- explicit invalid-span/NONE modeling;
- calibration diagnostics separated from ranking claims;
- reproducible exact-span evaluation;
- one-shot external scoring;
- no score-driven retry.

## 8. Historical architecture evidence

### Large nonlinear J0/J1 heads
Observed:
near-zero training loss but worse DEVELOPMENT generalization.

Policy:
do not automatically retain as default final verifier.

### R44C linear five-way verifier
Observed at t=.95:
- macro precision 0.8767348592080204;
- P 0.8918918918918919;
- I 0.8171091445427728;
- C 0.9318181818181818;
- O 0.8661202185792349;
- FP 130 versus J0 189;
- outer NLL 0.9456049077876719 versus J0 1.210236485360117.

Policy:
retain low-capacity regularization as an evidence-backed baseline/principle.
Do not assume the exact R44C model is globally optimal.

### Boundary/validity burden
R44C t=.95:
123/130 accepted FPs were target-NONE boundary/spurious groups.

Policy:
future architecture review must explicitly address span validity/boundary quality.

### I/C role burden
I remains the weakest high-confidence precision class.

Policy:
future training review must explicitly consider I/C role supervision and comparator-rich resources.

## 9. Reset claim language

Allowed:
"We retrained the final frozen pipeline from scratch using only the authorized training/development federation and evaluated once on the prespecified external benchmark."

Not allowed:
"We forgot earlier experiments, therefore previously used datasets became unseen again."

## 10. Current next step

Before any rebuild:
create and independently review:
`PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL`.

No training is authorized by this policy draft.


## 11. 2026-10-09 federation-review clarification

The public-human-gold federation review confirmed the reset principle and added stricter per-fit evidence rules.

Previously exposed records may be reused for TRAIN/DEVELOPMENT only where the task/schema use is explicitly authorized.

A public benchmark test is eligible for an independent campaign claim only after:
- exact official split membership is frozen;
- record/trial-family aliases are audited;
- no held-out family appears in native, auxiliary, weak, prompt-example, calibration or cached-learned-feature streams for that fit;
- test text/labels do not feed score-driven model selection;
- preprocessing and scoring are frozen and gold-independent.

Official test membership must be preserved.
If training-side aliases are removed for decontamination, the result is labeled a `DECONTAMINATED_MATCHED_PROTOCOL`, not a literal reproduction of the original training condition.

If a test record itself was previously exposed to ACAD_PASS, the corresponding official benchmark score is descriptive for this project, not a new independent claim.

Historical aggregate paper scores are method knowledge.
Identifiable labeled examples are record-level exposure.

This policy therefore authorizes from-scratch retraining on exposed development evidence but never erases scientific exposure.
