# ACAD_PASS — Post-R44-B Independent Reconciliation V1

Date: 2026-10-08

State: `R44C_LINEAR5_L2_RECONCILIATION_ACCEPTED`

## 1. Reviewed higher-model package

Companion deliverables:
- `ACAD_PASS_POST_R44B_INDEPENDENT_REVIEW.md`
- `ACAD_PASS_POST_R44B_REVIEW_2026-10-08.zip`

These are one review package, not independent corroborations.

External verdict:
`PROCEED_OTHER_SINGLE_INTERVENTION`.

Recommended next single intervention:
`R44C_LINEAR5_L2_V1` — one regularized five-way linear verifier on the existing frozen inputs.

The standalone Markdown and ZIP-embedded report are byte-identical:
SHA-256 `7a28aa2a032358252fd55baec0ab7672e4b7259f50a2c66703294fb5c4104649`.

The supplied archive's `audit_frozen_predictions.py` was independently re-executed after upload and completed successfully against the supplied frozen evidence.

## 2. Independent reconciliation of the causal argument

The previous working hypothesis favored factorizing candidate validity from P/I/C/O type.

That hypothesis is now **not selected as the next intervention**.

Key disconfirming evidence:

### 2.1 Five-way CE already contains validity supervision

For:
- (v=1-p_{NONE}),
- (q_c=p_c/v) for c in P/I/C/O,
- (a=1[y != NONE]),

the ordinary five-way CE decomposes exactly:

`CE5 = BCE(validity) + a * CE4(type | valid)`.

Therefore a separate validity head does not introduce a missing target. It changes function class, parameter sharing, weighting and score semantics.

### 2.2 Copy-B is the strongest conditional type baseline on valid coordinates

On the same 1,406 exact-coordinate valid candidates:
- frozen upstream B type: 1,355 / 1,406 = 0.9637268847795164;
- J0 non-NONE argmax: 1,337 / 1,406 = 0.9509246088193457;
- J1 non-NONE argmax: 1,338 / 1,406 = 0.9516358463726885.

J0 fixes 10 B-type errors but corrupts 28 originally correct B types.
J1 fixes 12 but corrupts 29.

Thus the ~95% conditional type result does NOT establish the need for a separate learned type expert.

### 2.3 Oracle validity does not identify the required architecture

Perfectly rejecting target-NONE candidates is a counterfactual diagnostic.
It does not show a learned binary validity head can reproduce oracle behavior, and it does not prove factorization is the narrowest causal intervention.

### 2.4 Overcapacity remains directly evidenced

Frozen outer NLL:
- J0 = 1.210236485360117;
- J1 = 1.3734881421278318.

These contrast sharply with tiny terminal meta-training CE values, while J1 generalizes worse.
This is consistent with overfitting and supports a bounded capacity/regularization test.

It is not proof that capacity alone caused failure.

## 3. Literature reconciliation

PICOX directly supports learning invalid-span rejection and composite negatives, but does not establish binary-validity + four-way-type decomposition for this exact candidate bank.

Selective-classification literature shows confidence-estimator choice can materially affect selective risk, so calibration/scoring explanations remain plausible. This is a reason NOT to overclaim factorization, not a reason to insert calibration into the next bounded experiment.

No reviewed 2024–2026 system establishes superiority under ACAD_PASS's exact P/I/C/O schema, strict exact-coordinate criterion, per-class precision floor and frozen candidate population.

## 4. Accepted narrow next hypothesis

`A_SINGLE_REGULARIZED_LINEAR_JOINT_ESTIMATOR_MAY_GENERALIZE_BETTER_THAN_THE_LARGE_NONLINEAR_HEADS_WHILE_RETAINING_THE_SAME_FIVE_WAY_EVENT_SEMANTICS`.

This is deliberately narrower than:
- factorization;
- boundary repair;
- hard-negative/IoU loss;
- calibration;
- alternative encoder/proposer;
- fresh-data acquisition before one final bounded development test.

## 5. Why this intervention is selected

It changes only the learned estimator capacity/regularization while keeping:
- same pair-exclusion nested banks;
- same outer EVAL candidate identities;
- same frozen contextual information;
- same five-way target;
- same acceptance semantics;
- same four thresholds;
- same original gates.

It removes:
- learned contextual projections;
- hidden nonlinear trunk;
- learned embeddings;
- biaffine interaction;
- dropout.

It therefore tests a coherent low-capacity alternative without simultaneously changing the task decomposition.

## 6. Important limitation

The L2 coefficient 0.01 is a **prospective commitment**, not an empirically optimized or literature-proven optimum.

The next experiment tests the complete frozen estimator:
- representation handling;
- training-only standardization;
- linear capacity;
- explicit L2;
- deterministic convex optimization.

A pass/fail does not isolate a causal effect of parameter count alone.

## 7. Current authorization boundary

This reconciliation authorizes:
1. exact protocol freeze for `R44C_LINEAR5_L2_V1`;
2. implementation-only code;
3. source-free/synthetic preflight;
4. frozen-input identity checks that do not fit on real META_TRAIN.

It does NOT yet authorize:
- a real R44C optimizer update;
- any new scientific score;
- VERIFY_INTERNAL;
- factorized training;
- calibration;
- boundary repair;
- alternate penalty/model/seed.

After synthetic preflight PASS and executor freeze, issue a separate one-shot scientific authorization.

Exact checkpoint:

`POST_R44B_REVIEW_RECONCILED -> FREEZE_R44C_LINEAR5_L2_V1 -> SYNTHETIC_PREFLIGHT_ONLY`.
