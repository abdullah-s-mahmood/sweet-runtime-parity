# ACAD_PASS — R44-B Higher-Model Adjudication V1

Date: 2026-10-08
Reviewed project commit: `81f5bc008c80edc01a846a8cc16901e501b991ff`

## Verdict

`PROCEED_WITH_NONSCIENTIFIC_IMPLEMENTATION_FIXES_ONLY`

The frozen R44-B scientific design remains unchanged.

No evidence supports replacing:
- pair-exclusion nesting;
- R44-A frozen outer evaluation rows;
- J0/J1;
- ordinary five-way CE;
- seed 44 / fixed 10 epochs;
- threshold grid `{0.80,0.85,0.90,0.95}`;
- deferred boundary repair.

No calibration fitting is authorized before the first frozen baseline.

## Mandatory closure before first scientific J0/J1 optimizer update

### I1 — scientific executor contract
Implement and freeze:
- `r44b_head_train.py`;
- `r44b_head_aggregate.py`;
- source-free/synthetic end-to-end closure;
- `AT0_EN_V26_R44B_HEAD_EXECUTION_FREEZE_V1.md`;
- `.github/workflows/r44b_head_scientific.yml`.

Required invariants:
- fresh model/optimizer/scheduler/RNG per fold/head;
- meta-only updates;
- eval mode + no-grad prediction;
- canonical manifest hash recomputation;
- pinned runtime/artifact/code identities;
- exactly 1,942 outer probability records per head;
- fail closed on missing/duplicate/nonfinite outputs;
- recall denominators P=271, I=829, C=115, O=677;
- synthetic proof of NONE rejection, type correction, exact-boundary accounting, >= thresholds, all-class gates, lowest-passing threshold and J0-first precedence;
- frozen diagnostic definitions;
- no score-driven retries/checkpoint shopping.

### I2 — interpretation correction
Permanent corrected wording:
- pair jobs are computationally separable but statistically dependent;
- 10 physical fits are fixed-seed fitting equivalence to 20 logical directions, not independent replication;
- cache computation is label-independent, while the source JSON physically contains tags;
- VERIFY_INTERNAL is historically exposed through parent R4.3 FIT/audits and split-statistic use; it has not been used for R44 candidate-specific verification/tuning;
- mechanics run 37702502662 computed gradients on a small mixed development sample but performed no optimizer update or retained learned state;
- mechanics objects/gradients/RNG state may never initialize the scientific run.

## Authorization after closure

If I1 synthetic closure and I2 documentation closure both PASS:
- authorize exactly one frozen DEVELOPMENT J0/J1 experiment across five outer folds;
- maximize safe GitHub concurrency with 5 folds x 2 heads = 10 computational jobs;
- aggregate the complete outputs once;
- apply the deterministic frozen J0-first rule;
- freeze success OR failure.

Then STOP before:
- VERIFY_INTERNAL;
- final refit;
- calibration fitting;
- boundary repair;
- alternative architecture/loss/threshold experiments.

The R44-B nested result is DEVELOPMENT model-selection evidence only, not an unbiased final generalization estimate.
