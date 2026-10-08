# ACAD_PASS — R44-B Head Execution Freeze V1

Date: 2026-10-08

**State:** `R44B_HEAD_EXECUTION_FROZEN_AND_AUTHORIZED`

**Scientific attempt ID:** `R44B_B1_DEV_J0J1_ATTEMPT_1`

This document closes the higher-model I1/I2 requirements and authorizes exactly one frozen R44-B DEVELOPMENT J0/J1 execution. It does not authorize VERIFY_INTERNAL, final refitting, calibration fitting, boundary repair, architecture expansion, new thresholds, new seeds, extra epochs, early stopping, or score-driven retry.

## 1. Higher-model adjudication

Independent verdict:
`PROCEED_WITH_NONSCIENTIFIC_IMPLEMENTATION_FIXES_ONLY`.

Durable adjudication:
`AT0_EN_V26_R44B_HIGHER_MODEL_ADJUDICATION_V1.md`.

I2 corrections are already appended to the frozen protocol, review packet, and pre-head adversarial review:
- pair jobs are computationally separable but statistically dependent;
- 10 physical pair fits are fixed-seed fitting equivalence, not independent replication;
- context computation is label-independent although source JSON physically contains tags;
- VERIFY_INTERNAL is historically exposed through parent R4.3 FIT/audits and split-statistic balancing; no R44 candidate-specific verification/tuning has occurred;
- mechanics run 37702502662 called backward on a tiny mixed development sample but made no optimizer/scheduler update and retained no learned state;
- no mechanics model/gradient/RNG continuation may initialize this experiment.

## 2. Frozen upstream inputs

### Nested banks
- run: `37683637815`
- artifact: `11515434193`
- name: `r44b-b1-nested-banks`
- ZIP digest: `sha256:98383b4bec040f19d6e4076fea1a70dcb406366dfd4bd724d1ad2fac6d2018fb`
- state: `R44B_PAIR_AGGREGATE_PASS`
- pair count: 10
- aggregate outer evaluation population: 1,942 candidates

### Immutable context cache
- run: `37683637815`
- artifact: `11510422862`
- name: `r44b-base-context-cache`
- ZIP digest: `sha256:4fdceb511c2067cf81a1ad6c64c039febf99e3c11b9d8baa32b2d73569faa91c`
- context NPY SHA256: `6bb548884cafb2a14e19b7d691b393dcf0ab9b5cc6add14e6ab0a873be33361b`
- context index SHA256: `db9a6bae51a4db38d244e9e0a98f44b5dbfb246f694db5397c6e204cd58881dd`

### Frozen R44 manifest
- run: `37572165532`
- artifact: `11461461773`
- name: `r44-oof-readonly-preflight`
- ZIP digest: `sha256:62f92359aeae66363af756a997dc684eb876784ccb6b2104111662fb3c43ff08`
- canonical manifest SHA256: `799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`

## 3. Authoritative non-scientific executor closure

Final runtime-pinned closure:
- run: `37706030660`
- head SHA: `f3ab4b5e5c1e03a442602084f773a89053d328b7`
- artifact: `11520031556`
- artifact name: `r44b-head-executor-synthetic-closure`
- ZIP digest: `sha256:eabfc44138280cc1909f5f7e686a240953ff9cd3f260633e4ba9e488931eb924`
- state: `R44B_HEAD_EXECUTOR_SYNTHETIC_CLOSURE_PASS`
- scientific data used: false
- scientific head attempt consumed: false

Synthetic closure proved:
- J0 optimizer update / 10 fixed epochs / checkpoint serialization;
- J1 optimizer update / 10 fixed epochs / checkpoint serialization;
- target/taxonomy/goldless mutation cannot change model features;
- NONE rejection;
- type correction;
- wrong-boundary target NONE accounting;
- exact `>=` threshold behavior;
- all-four-class gate;
- lowest passing frozen threshold;
- J0-first precedence;
- J1 escalation only after J0 failure;
- no-pass outcome;
- missing output fails closed;
- duplicate output fails closed;
- duplicate row fails closed;
- nonfinite probability fails closed;
- unnormalized probability fails closed;
- full 5-fold x 2-head synthetic output population validation;
- physical checkpoint tampering fails closed.

Historical non-scientific closure attempts are retained:
- `37704956922`: SUCCESS, superseded simpler closure;
- `37705160972`: SUCCESS, superseded;
- `37705311699`: FAILURE, synthetic JSON literal-backslash-n fixture defect;
- `37705508807`: FAILURE, same fixture lineage;
- `37705640579`: FAILURE, synthetic J1 provenance fixture incorrectly labeled J1 rows as J0;
- `37705932432`: SUCCESS full-validator closure, superseded by exact runtime-pinned closure;
- `37706030660`: authoritative SUCCESS.

None consumed scientific J0/J1 training.

## 4. Executor source identities

Authoritative closure SHA256:

- `d97ef98bbbc0c6ba0d9e875c63f9c1575f45da1009caf8ebff7891d212a6ae53`
  `phase2/academic_transform/at0_en/v2_6/r44b_head_train.py`
- `fcfe9def302d7a87141f4d62df91e395ea2d6bbfadd2f902977b289a38060f84`
  `phase2/academic_transform/at0_en/v2_6/r44b_head_aggregate.py`
- `0dc5fa127ccb336281d0e3adfa3df79f08a85dc831e222411aabf184a34cc4b7`
  `phase2/academic_transform/at0_en/v2_6/r44b_head_synthetic_closure.py`
- `a384f1971df202c0bc3bb5293a1fc365c84e222bc16d6b93f40850b0c7cd98ed`
  `phase2/academic_transform/at0_en/v2_6/r44b_b1_preflight.py`
- `9d93066cf156b7ab4b03282b1c10f96ffe700c196a30e7e406be59eb638ede67`
  `requirements/r44b_head.txt`

Current Git blob identities:
- trainer blob: `45dc713b445f35c8134377f6784b5d1ca0167f86`
- aggregate blob: `e8a64eb16eb9b16f38cb672665d576609dc59a48`
- synthetic closure blob: `0ddd0ca8886bf8a68c64fb3e642e9bed8901ef62`
- J0/J1 architecture/preflight blob: `034202330307e6befe99fa759292cc4b8a07bc2b`
- minimal requirements blob: `0cc0c01329db235cdc65e9af9e6ef7713eb3e0f2`
- scientific workflow blob: `87fd5c85a5f7796b84504a4e4292a97641803c73`

Scientific workflow:
`.github/workflows/r44b_head_scientific.yml`.

## 5. Frozen runtime

- runner: `ubuntu-24.04`
- Python: `3.11.16`
- numpy: `1.26.4`
- torch: `2.2.2`
- safetensors: `0.4.3`
- PYTHONHASHSEED: 44
- deterministic PyTorch algorithms enabled in trainer.

No transformers/accelerate runtime is required by the head executor.

## 6. Frozen scientific fitting contract

For every outer fold k and each head J0/J1:
- fresh process;
- fresh model;
- fresh optimizer;
- fresh scheduler;
- fresh RNG initialization with seed 44;
- training population = only outer-k nested meta rows;
- evaluation population = only frozen outer-k R44-A rows;
- evaluation under `model.eval()` and `torch.no_grad()`;
- ordinary 5-way CE;
- AdamW;
- lr = 1e-3;
- weight decay = 0.01;
- batch = 64;
- epochs = exactly 10;
- linear LR decay, no warmup;
- gradient clip = 1.0;
- final epoch only;
- no early stopping;
- no class weighting;
- no focal loss;
- no hard-negative resampling;
- no calibration fitting.

Expected trainable parameters:
- J0: 584,631
- J1: 667,836.

All 5 folds x 2 heads may execute concurrently because they are computationally separable with immutable inputs and disjoint outputs. They remain statistically dependent development folds.

## 7. Frozen feature allowlist

Only:
- context start;
- context end;
- context interior mean;
- previous context or learned edge vector;
- following context or learned edge vector;
- width;
- B proposed type;
- source-derived section;
- B confidence;
- Boundary start probability;
- Boundary end probability;
- normalized example index;
- normalized span start.

Forbidden as model features:
- target;
- taxonomy;
- goldless flag;
- any gold span/label/tags.

## 8. Probability/output completeness contract

Every final fold/head checkpoint is stored as safetensors.

Every outer candidate receives all five raw probabilities:
`NONE/P/I/C/O`.

Aggregate requirements:
- exactly 1,942 probability rows for J0;
- exactly 1,942 probability rows for J1;
- exact population identity across heads;
- no missing rows;
- no duplicate rows;
- no NaN/Inf/out-of-range probability;
- five probabilities sum to 1 within frozen tolerance;
- physical checkpoint SHA must equal summary SHA;
- probability file SHA must equal summary SHA;
- any violation fails closed.

No failed row/fold may be silently removed.

## 9. Frozen recall denominators

Authoritative gold entity denominators:
- P = 271
- I = 829
- C = 115
- O = 677

They include entities never proposed by B.

Candidate-positive counts MUST NOT replace these denominators.

## 10. Frozen decision rule

Threshold grid only:
`{0.80, 0.85, 0.90, 0.95}`.

Candidate rule:
- `c = argmax p(NONE/P/I/C/O)`;
- if c = NONE: reject;
- otherwise accept iff `p(c) >= threshold`.

Per P/I/C/O:
- precision >= 0.90;
- recall >= 0.20;
- accepted >= 10.

Also:
- macro precision >= 0.90.

For each head choose the LOWEST frozen threshold passing all gates.

Architecture:
1. if J0 passes, nominate J0;
2. else if J1 passes, nominate J1;
3. else freeze `NO_ARCHITECTURE_NOMINATED`.

All comparisons use unrounded values.

## 11. Frozen descriptive diagnostics

Diagnostics never alter selection.

Multiclass Brier:
- mean across all 1,942 candidates of `sum_k (p_k - y_k)^2` over five classes.

ECE:
- top-class correctness/confidence;
- all 1,942 candidates;
- 10 equal-width bins: [0,.1), ... , [.9,1].

Risk/coverage:
- eligible population = candidates whose five-way argmax is non-NONE;
- sorted by predicted-class confidence descending;
- cumulative risk = exact-target error fraction among accepted prefix;
- coverage denominator = all 1,942 candidates.

Per-class candidate AP:
- one-vs-rest candidate-level AP;
- report candidate-positive count;
- report candidate-positive recall ceiling using authoritative gold denominator.

No diagnostic is a new selection criterion.

## 12. One-shot / retry protection

Workflow:
`R44-B frozen J0-J1 DEVELOPMENT attempt 1`.

It requires:
- GitHub workflow `run_number == 1`;
- GitHub `run_attempt == 1`;
- fixed attempt ID `R44B_B1_DEV_J0J1_ATTEMPT_1`.

These guards are repeated inside every scientific head job and aggregate.

Therefore GitHub re-run/re-run-failed attempts cannot silently train again: attempt 2 fails before training.

If attempt 1 has any infrastructure/implementation failure after dispatch:
- preserve every produced artifact/status/log;
- DO NOT auto-rerun;
- STOP for explicit failure adjudication;
- no score-driven replacement is authorized.

## 13. Interpretation boundary

The aggregated result is:
`DEVELOPMENT_MODEL_SELECTION_EVIDENCE_ONLY`.

It may nominate an architecture/threshold but is not an unbiased final generalization estimate.

After aggregate success, freeze complete success OR failure and STOP.

Still forbidden:
- VERIFY_INTERNAL;
- final full-DESIGN refit;
- fitted calibration;
- boundary repair;
- new model family/architecture;
- new thresholds;
- new seed;
- extra epochs;
- adaptive retry.

NEXT AUTHORIZED OPERATION:

`CREATE_ONE_SHOT_TRIGGER -> RUN R44B_B1_DEV_J0J1_ATTEMPT_1 -> AGGREGATE -> FREEZE -> STOP`.
