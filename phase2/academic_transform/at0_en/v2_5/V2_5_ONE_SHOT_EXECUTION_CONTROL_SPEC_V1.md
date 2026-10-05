# ACAD_PASS — V2.5 One-Shot Prediction Execution Control Specification V1

Date: 2026-10-05
Status: FROZEN CONTROL DESIGN V2 / NO FACTPICO EXECUTION

## 1. Purpose

Close the pre-execution integrity requirements without changing matcher semantics, FactPICO gold, thresholds, population, or record IDs.

This revision freezes the actual durable attempt-ledger mechanism requested by the independent reviewer.

## 2. Required execution path

A future authorized FactPICO prediction has TWO inseparable control layers:

1. durable remote claim in the frozen GitHub ledger;
2. local `run_v2_5_one_shot_guard.py` bound to that remote claim identity.

Direct invocation of `run_v2_5_batch.py` is NOT the authorized one-shot procedure.

## 3. Frozen durable ledger

Provider:
`GitHub repository contents`

Repository:
`abdullah-s-mahmood/sweet-runtime-parity`

Dedicated ledger branch:
`factpico-v25-one-shot-ledger`

Authorization ID:
`FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001`

Frozen FactPICO input SHA-256:
`ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`

Canonical REAL claim key:

`claims/real/FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001/ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82/ATTEMPT_CLAIM.json`

This key is unique and fixed.

Choosing another branch/key/directory is NOT a new permissible attempt.

Deleting/cleaning the claim does NOT restore authorization under this protocol.

## 4. Mandatory remote prelaunch ceremony

Every permitted real launch MUST execute these steps in order:

1. Query the exact canonical claim key on branch `factpico-v25-one-shot-ledger`.
2. If the key exists: ABORT before inference. The authorization is consumed.
3. If the key does not exist: atomically create it through GitHub's create-file operation.
4. The remote claim payload MUST bind:
   - authorization ID;
   - runtime `AT0-EN V2.5`;
   - frozen FactPICO input SHA-256;
   - state `CONSUMED_BEFORE_INFERENCE`;
   - canonical provider/repository/branch/key.
5. Fetch the newly created claim and retain:
   - claim content;
   - blob SHA;
   - claim commit SHA.
6. Only then invoke the local one-shot guard with the SAME:
   - authorization ID;
   - durable-ledger provider;
   - durable-ledger key;
   - durable-ledger claim commit SHA.

If any identity differs, launch is forbidden.

## 5. Guard binding

The current guard hard-codes the real FactPICO authorization identity.

For a real 345-record input with the frozen input SHA, it refuses to start unless:

- authorization ID exactly equals:
  `FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001`

- durable provider exactly equals:
  `github:abdullah-s-mahmood/sweet-runtime-parity@factpico-v25-one-shot-ledger`

- durable key exactly equals the canonical REAL key in §3;

- a nonempty durable claim commit SHA is provided.

These values are written into the local `ATTEMPT_CLAIM.json` and `PREDICTION_FREEZE.json`.

The local attempt directory remains an additional control, not the durable source of truth.

## 6. Consume-before-inference semantics

The REMOTE GitHub claim consumes the authorization before inference.

If ChatGPT, the launcher, local process, container, parent process, or batch runner stops after remote claim creation:

`ATTEMPT = CONSUMED`

No automatic restart is permitted.

An incomplete/aborted attempt cannot be silently represented as a complete prediction run.

## 7. Durable-ledger survival test

Synthetic-only durable claim:

Branch:
`factpico-v25-one-shot-ledger`

Key:
`claims/synthetic/SYN-DURABLE-LEDGER-001/ATTEMPT_CLAIM.json`

Creation commit:
`f687cedcb82c543d8d21552db79a2d25a93f7a4e`

Blob SHA observed by a later independent fetch:
`cf03473f29ab3ce3452d133302ccc27672c1278f`

Test sequence:

1. a synthetic claim was created with state `CONSUMED_BEFORE_INFERENCE`;
2. inference was intentionally NOT started, simulating interruption after claim;
3. the initial launcher/tool invocation ended;
4. a later independent GitHub fetch queried the same branch/key;
5. the claim was still present with the same content;
6. the fresh-launch procedure therefore classified the attempt as ALREADY CONSUMED and did not start inference.

Verdict:
`DURABLE_CLAIM_SURVIVAL_AND_FRESH_LAUNCH_REFUSAL = PASS`

The synthetic claim is retained as evidence and must not be deleted.

The REAL claim key remains absent/unconsumed.

## 8. Local output replacement prevention

The batch runner refuses an existing prediction output path.

The local guard:
- requires a previously nonexistent local attempt directory;
- writes local claim metadata;
- invokes the runner once;
- freezes prediction SHA-256 after success;
- refuses reuse of the same local attempt directory.

Regression:
`PASS`

## 9. FactPICO fixed controls

For the eventual separately authorized run:

- runtime: `AT0-EN V2.5`
- prediction input SHA-256: `ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`
- expected count: `345`
- max assertions per side: `128`
- timeout: `60 seconds/record`
- execution: strictly sequential
- retries: `0`
- timeout/crash/out-of-envelope: visible `INVALID_VERIFICATION`

No gold or eligibility data may be available to inference.

Predeclared outer allowance:
at least `20,700 seconds + fixed orchestration overhead`.

## 10. Synthetic test-only fault mechanism

The batch runner accounting-test mechanism is inert unless BOTH:

- `ACAD_PASS_V25_SYNTHETIC_TEST_MODE=1`
- `ACAD_PASS_V25_SYNTHETIC_FAULT_MAP` is present.

It accepts only `SYN-*` IDs and synthetic TIMEOUT/CRASH accounting actions.

The authorized FactPICO environment MUST have both variables absent.

## 11. Prediction freeze before gold

After a successful prediction run:

1. verify exactly one output per input ID and exact order;
2. verify all 345 IDs are unique and exactly match the frozen input;
3. freeze prediction SHA-256;
4. preserve:
   - remote durable claim;
   - remote claim commit/blob identity;
   - local claim;
   - runner stdout/stderr;
   - prediction artifact;
   - prediction freeze manifest;
5. STOP.

Gold join/scoring remains a separate checkpoint.

The prediction artifact MUST NOT be replaced after inspection.

## 12. Failure semantics

If the outer launcher/runner fails after remote claim creation:

- the remote claim remains authoritative;
- attempt remains consumed;
- preserve available evidence;
- do not retry automatically;
- do not create a replacement prediction artifact under the same authorization.

Per-record failures returned normally remain denominator-visible INVALID records.

## 13. Current authorization

This specification and its tests do NOT authorize FactPICO execution.

The REAL durable claim key MUST remain absent until a separate execution authorization is granted.

Current stop:

`FINAL EXECUTION AUTHORIZATION REVIEW`
