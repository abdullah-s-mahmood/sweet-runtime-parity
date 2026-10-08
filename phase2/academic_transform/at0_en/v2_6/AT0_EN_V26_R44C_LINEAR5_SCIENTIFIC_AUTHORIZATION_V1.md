# ACAD_PASS — R44C LINEAR5 L2 Scientific Authorization V1

Date: 2026-10-08

**State:** `R44C_LINEAR5_L2_SCIENTIFIC_ATTEMPT_1_AUTHORIZED`

**Attempt ID:** `R44C_LINEAR5_L2_DEV_ATTEMPT_1`

This file authorizes exactly ONE adaptive DEVELOPMENT scientific attempt of the already-frozen and implementation-verified R44C linear protocol.

## Preconditions satisfied

Independent post-R44-B review:
`PROCEED_OTHER_SINGLE_INTERVENTION`

Reconciliation:
`R44C_LINEAR5_L2_RECONCILIATION_ACCEPTED`

Protocol:
`R44C_LINEAR5_L2_PROTOCOL_FROZEN_PREFLIGHT_ONLY`

Authoritative implementation preflight:
- run `37725529491`
- synthetic closure SUCCESS
- frozen-input audit SUCCESS
- combined closure SUCCESS
- scientific attempt consumed = false
- real META scaler computed = false
- real META optimizer created = false
- VERIFY_INTERNAL used = false

Execution freeze:
`R44C_LINEAR5_EXECUTION_FROZEN_AND_AUTHORIZED`

## Authorized work

Exactly five outer folds may run in parallel:
- outer 0
- outer 1
- outer 2
- outer 3
- outer 4

Each uses the same frozen architecture, inputs, objective, scaling, L-BFGS contract, thresholds and gates defined in:
`AT0_EN_V26_R44C_LINEAR5_L2_PROTOCOL_FREEZE_V1.md`
and bound by:
`AT0_EN_V26_R44C_LINEAR5_EXECUTION_FREEZE_V1.md`.

After all five complete successfully:
- execute exactly one aggregate;
- freeze all outputs;
- apply only the frozen four thresholds;
- freeze success OR failure;
- STOP.

## Attempt consumption

The first real optimizer update in any fold consumes:
`R44C_LINEAR5_L2_DEV_ATTEMPT_1`.

No:
- automatic rerun;
- replacement fold;
- new seed;
- lambda change;
- solver change;
- threshold addition;
- calibration;
- boundary repair;
- factorization;
- hard-negative weighting;
- model-family change.

If a mechanical failure occurs after any real optimizer update:
- preserve partial evidence;
- do not retry;
- require explicit adjudication.

## Closed evidence

Still forbidden:
- VERIFY_INTERNAL;
- old SELECT;
- historical/protected tests;
- FactPICO;
- consumed 60-RCT holdout;
- any other protected/final evaluation.

## Scientific interpretation

Any result is:
`ADAPTIVE_NESTED_DEVELOPMENT_EVIDENCE_ONLY`.

A pass nominates this one frozen estimator/threshold for later independent reconciliation.
A fail freezes R44C as failed and invokes the sole fallback:
acquire genuinely fresh independently annotated data under a separately frozen plan.

## Exact next operation

`DISPATCH_R44C_LINEAR5_L2_DEV_ATTEMPT_1_ONCE -> FIVE_FOLDS -> ONE_AGGREGATE -> FREEZE -> STOP`.
