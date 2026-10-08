# ACAD_PASS — R44C LINEAR5 L2 Execution Freeze V1

Date: 2026-10-08

**State:** `R44C_LINEAR5_EXECUTION_FROZEN_AND_AUTHORIZED`

**Scientific attempt ID:** `R44C_LINEAR5_L2_DEV_ATTEMPT_1`

This file closes the implementation-only preflight for the single post-R44-B intervention selected by independent review and reconciliation. It freezes the exact executor that may be used by a later separate one-shot scientific authorization.

It does NOT itself trigger a scientific run.

## 1. Scientific basis

Post-R44-B independent verdict:
`PROCEED_OTHER_SINGLE_INTERVENTION`.

Selected intervention:
one regularized five-way linear estimator on the unchanged frozen R44 candidate population.

Reconciliation:
`AT0_EN_V26_R44C_LINEAR5_RECONCILIATION_V1.md`

Frozen scientific protocol:
`AT0_EN_V26_R44C_LINEAR5_L2_PROTOCOL_FREEZE_V1.md`

No factorized validity/type heads, boundary repair, calibration, hard-negative weighting, alternate penalty, seed comparison, threshold expansion or new data are part of R44C.

## 2. Frozen upstream evidence

Nested banks:
- run `37683637815`
- artifact `11515434193`
- name `r44b-b1-nested-banks`
- digest `sha256:98383b4bec040f19d6e4076fea1a70dcb406366dfd4bd724d1ad2fac6d2018fb`

Immutable context cache:
- run `37683637815`
- artifact `11510422862`
- name `r44b-base-context-cache`
- digest `sha256:4fdceb511c2067cf81a1ad6c64c039febf99e3c11b9d8baa32b2d73569faa91c`
- context NPY SHA256 `6bb548884cafb2a14e19b7d691b393dcf0ab9b5cc6add14e6ab0a873be33361b`
- context index SHA256 `db9a6bae51a4db38d244e9e0a98f44b5dbfb246f694db5397c6e204cd58881dd`

Frozen R44 manifest:
- run `37572165532`
- artifact `11461461773`
- name `r44-oof-readonly-preflight`
- digest `sha256:62f92359aeae66363af756a997dc684eb876784ccb6b2104111662fb3c43ff08`
- canonical manifest SHA256 `799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`

R44-A candidate bank SHA256:
`6f20f12e8bcb814067f689f5acc27918b98de93e6e88dd1ebb53d7689bc1d946`

## 3. Authoritative implementation preflight

Authoritative preflight run:
- `37725529491`
- head SHA `da82e68a796139fa67bec2f858d99dc604754473`
- workflow run number 3
- run attempt 1

All authoritative jobs:
- source-free synthetic closure: SUCCESS
- frozen-input structural audit: SUCCESS
- implementation preflight closure: SUCCESS

Artifacts:

### Synthetic preflight
- artifact ID `11527033325`
- name `r44c-linear5-synthetic-preflight`
- digest `sha256:0797f900bfc01f769098b945d3bf9968d26a19d78b696b6f0a163679a158480d`
- state `R44C_LINEAR5_SYNTHETIC_PREFLIGHT_PASS`
- scientific data used = false
- scientific attempt consumed = false

Verified synthetic mechanics include:
- feature dimension = 3918
- parameter count = 19,595
- raw feature dtype float32
- scaled fitting dtype float64
- exactly 3,845 scaled coordinates
- zero-variance masking
- analytic-vs-autograd weight gradient max error `1.1102230246251565e-16`
- analytic-vs-autograd bias gradient max error `2.0816681711721685e-17`
- explicit L2 excludes bias
- persistent L-BFGS convergence
- synthetic convergence in 28 optimizer steps
- final synthetic grad infinity norm `3.5202448075803694e-07`
- forced nonconvergence = FAIL_CLOSED
- checkpoint/scaler serialization round-trip
- five-fold synthetic complete-population validation
- logits/log-probabilities/probabilities consistency
- physical checkpoint tamper = FAIL_CLOSED
- threshold >= behavior
- NONE-first tie order

### Frozen-input structural audit
- artifact ID `11527950745`
- name `r44c-linear5-frozen-input-preflight`
- digest `sha256:4b7cc1eadac2989784af900c08502ca1f433b1084c8a8af33e3b37302cc990dd`
- state `R44C_LINEAR5_FROZEN_INPUT_PREFLIGHT_PASS`
- audited rows = 9,613
- aggregate EVAL rows = 1,942
- max candidate width = 45
- feature dimension = 3918
- scaler statistics computed = false
- optimizer created = false
- model created = false
- scientific attempt consumed = false
- VERIFY_INTERNAL used = false
- protected data used = false

Frozen input file SHA256:
- input report `bac826929bd5473089abde6642aef467a72190217a6294432841976a4f0c74c9`

Verified outer identities:
- outer 0: META 1567, EVAL 407
- outer 1: META 1519, EVAL 375
- outer 2: META 1499, EVAL 368
- outer 3: META 1535, EVAL 410
- outer 4: META 1551, EVAL 382

### Combined implementation closure
- artifact ID `11527138040`
- name `r44c-linear5-implementation-preflight`
- digest `sha256:b3286ec5308d413dbc8c1c6a1705688c09464a958b3793022d8a76e32499521d`
- state `R44C_LINEAR5_IMPLEMENTATION_PREFLIGHT_PASS`
- real META scaler computed = false
- real META optimizer created = false
- scientific attempt consumed = false
- VERIFY_INTERNAL used = false

## 4. Authoritative executor source SHA256

These exact byte identities were recorded by the successful authoritative synthetic preflight:

- `4ce21d1afde0aac77cd2b6044798ef1d8e4a3e87591e2177f4ec8664e806ba61`
  `phase2/academic_transform/at0_en/v2_6/r44c_linear5_train.py`

- `66f2a31f9d54492678a4c43f7fc6f46887515ff8395e1649d11578c3d241fafa`
  `phase2/academic_transform/at0_en/v2_6/r44c_linear5_aggregate.py`

- `a1a22f12c98f0e9911a3eead7cdb06691a4e814800d8bc2a82419cd69279845e`
  `phase2/academic_transform/at0_en/v2_6/r44c_linear5_synthetic_preflight.py`

- `7748840cd91e0bba4355f8d50ef860e68a18e656ce4c2c8b33c1cb906b87de02`
  `phase2/academic_transform/at0_en/v2_6/r44c_linear5_input_preflight.py`

- `7b04765c72fc54a043ea3ceaebdfd12c93e5ed8da3a67bb6c7d582d06cf68d7c`
  `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R44C_LINEAR5_L2_PROTOCOL_FREEZE_V1.md`

- `9d93066cf156b7ab4b03282b1c10f96ffe700c196a30e7e406be59eb638ede67`
  `requirements/r44c_linear5.txt`

Current Git blob identities at authoritative preflight head:
- trainer blob `b7845403c9d230773c3c2dedb36460cecfe232f9`
- aggregate blob `8dd5f95edcf1f43dc9384e01da621afaacfd0967`
- synthetic preflight blob `9d187c22b7d410ec02870f8899b2ef2093b2ce2a`
- input preflight blob `1e242f63a7b5c9645360cee453fcfaa62ab7600a`
- protocol blob `a60f06c982dac5cc8bdfd0eb1ddd5990bcb9e6a1`
- requirements blob `0cc0c01329db235cdc65e9af9e6ef7713eb3e0f2`

Scientific workflow created after preflight:
- `.github/workflows/r44c_linear5_scientific.yml`
- creation commit `9a2018c7dbad920068506c66b3c3aa8637d63fcd`
- workflow blob `c252646f64110a9460e88a2ab63a5e04e1ba7ab4`

The scientific workflow is not part of the model-fitting function and has not yet been dispatched.

## 5. Preflight negative evidence retained

Non-scientific preflight run `37725085094`:
- synthetic fixture failure: missing target field in a gate-test fixture;
- input audit failure: output-directory ownership mismatch;
- no scientific data fit;
- no real META scaler;
- no real META optimizer;
- no R44C attempt consumed.

Non-scientific preflight run `37725269768`:
- synthetic closure SUCCESS;
- input audit still failed on output-directory ownership;
- closure skipped;
- no scientific attempt consumed.

Corrections were implementation-only:
- added synthetic fixture targets;
- hardened output-directory ownership;
- strengthened aggregate schedule/input/numeric identity checks;
- aligned synthetic fixtures with hardened logit/log-probability/probability consistency.

No scientific threshold, model family, feature set, L2 coefficient, solver, seed, population or gate changed in response to those failures.

## 6. Frozen scientific execution contract

A separately authorized scientific run may execute exactly five outer-fold fits in parallel.

For each outer k:
- training = frozen outer-k META_TRAIN only;
- fold-local scaler fitted from META_TRAIN only;
- EVAL feature interface strips target/taxonomy/goldless and other gold-derived metadata;
- exactly one five-way linear model;
- 3918 features;
- 19,595 parameters;
- zero initialization;
- explicit L2 coefficient .01 on W only;
- full-batch deterministic L-BFGS;
- numerical convergence at first finite `||grad||_inf <= 1e-6`;
- maximum 1000 persistent optimizer steps;
- nonconvergence is mechanical failure with no salvaged scientific score;
- output checkpoint/scaler/logits/log-probabilities/probabilities frozen before target join;
- aggregator alone rejoins frozen EVAL DEVELOPMENT targets;
- exactly 1,942 unique aggregate outputs required.

## 7. One-shot protection

Scientific workflow:
`R44C LINEAR5 L2 DEVELOPMENT attempt 1`

Attempt ID:
`R44C_LINEAR5_L2_DEV_ATTEMPT_1`

The workflow repeats guards:
- GitHub `run_number == 1`
- GitHub `run_attempt == 1`
- exact attempt ID

Any GitHub re-run attempt therefore fails before a scientific fold fit.

The first real optimizer update consumes the R44C attempt.

If any mechanical failure occurs after the first real optimizer update:
- preserve all partial artifacts/status/logs;
- do not auto-rerun;
- stop for explicit adjudication.

## 8. Frozen scientific decision

Thresholds only:
`{0.80,0.85,0.90,0.95}`

Five-way argmax class order:
`NONE,P,I,C,O`

Acceptance:
- reject if argmax NONE;
- otherwise accept iff predicted-class joint probability >= threshold.

Select the LOWEST frozen threshold passing all gates.

Per P/I/C/O:
- precision >= .90
- recall >= .20
- accepted >= 10

Macro precision:
- >= .90

Gold recall denominators:
- P=271
- I=829
- C=115
- O=677

No passing threshold:
`R44C_LINEAR5_L2_SCIENTIFIC_FAIL`.

## 9. Interpretation and sole fallback

Any result is:
`ADAPTIVE_NESTED_DEVELOPMENT_EVIDENCE_ONLY`.

VERIFY_INTERNAL remains closed.

If R44C fails scientifically, the sole predeclared fallback is:
`STOP_FURTHER_MODEL_THRESHOLD_LOSS_ADAPTATION_ON_DESIGN_AND_ACQUIRE_GENUINELY_FRESH_INDEPENDENTLY_ANNOTATED_DATA_UNDER_A_SEPARATELY_FROZEN_PLAN`.

Do not automatically launch factorization, calibration, boundary repair, hard-negative weighting or another model.

## 10. Current boundary

Implementation closure is complete.

A separate scientific authorization is still required before dispatch.

Exact checkpoint:
`R44C_LINEAR5_EXECUTOR_FROZEN -> SEPARATE_ONE_SHOT_AUTHORIZATION_REQUIRED`.
