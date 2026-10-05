# ACAD_PASS — V2.5 One-Shot Prediction Execution Control Specification V1

Date: 2026-10-05
Status: FROZEN CONTROL DESIGN / NO FACTPICO EXECUTION

## 1. Purpose

Close the pre-execution integrity gaps identified by the independent V2.5 pre-prediction review without changing matcher semantics, FactPICO gold, thresholds, population, or record IDs.

## 2. Required execution path

A future authorized FactPICO prediction MUST run through:
`run_v2_5_one_shot_guard.py`

which invokes:
`run_v2_5_batch.py`

exactly once for the claimed attempt.

Direct invocation of the batch runner is not the authorized one-shot procedure.

## 3. Consume-before-inference rule

Before launching inference the guard MUST create a previously nonexistent attempt directory and an exclusive:
`ATTEMPT_CLAIM.json`

with state:
`CONSUMED_BEFORE_INFERENCE`

If the attempt directory already exists, execution MUST refuse to start.

The attempt directory MUST reside on storage whose state survives parent-process failure/cancellation for the duration of the experiment. An ephemeral workspace with no durable preservation is not sufficient for the real one-shot run.

If the parent process is cancelled or crashes after claim creation, that attempt is consumed and MUST NOT be automatically restarted.

## 4. Output replacement prevention

The batch runner MUST refuse to overwrite an existing output path.

The one-shot guard uses a fresh fixed output path inside the newly claimed attempt directory.

After success it freezes prediction SHA-256, input SHA-256, attempt ID, runtime ID and retry count.

A second invocation against the same attempt directory MUST fail.

## 5. FactPICO fixed controls

For the eventual authorized run:
- runtime: `AT0-EN V2.5`
- prediction input SHA-256: `ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`
- expected count: `345`
- max assertions per side: `128`
- timeout: `60 seconds/record`
- execution: strictly sequential
- retries: `0`
- timeout/crash/out-of-envelope: visible `INVALID_VERIFICATION`

No gold or eligibility data may be available to inference.

## 6. Synthetic test-only fault injection

The batch runner test mechanism is inert unless BOTH:
- `ACAD_PASS_V25_SYNTHETIC_TEST_MODE=1`
- `ACAD_PASS_V25_SYNTHETIC_FAULT_MAP` is present.

It accepts only `SYN-*` IDs and only synthetic TIMEOUT/CRASH accounting actions.

The authorized FactPICO command MUST have both variables absent.

## 7. Prediction freeze before gold

After success:
1. verify exactly one output per input ID and exact order;
2. write and freeze prediction SHA-256;
3. preserve runner stdout/stderr and attempt claim;
4. stop.

Gold join/scoring remains a separate checkpoint.

## 8. Failure semantics

If the outer runner fails:
- preserve the consumed attempt directory and evidence;
- record `ABORTED_CONSUMED`;
- do not retry automatically;
- do not create a replacement prediction artifact under the same authorization.

Per-record failures remain denominator-visible INVALID records.

## 9. Current authorization

This specification and tests do NOT authorize FactPICO execution.

Current stop:
`V2.5 ESSENTIAL PRE-EXECUTION CLOSURE / HIGHER-MODEL RE-REVIEW`
