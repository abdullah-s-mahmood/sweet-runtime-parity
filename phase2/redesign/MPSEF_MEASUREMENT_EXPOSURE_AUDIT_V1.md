# MP-SEF MEASUREMENT EXPOSURE AUDIT V1

Date: 2026-10-01
Status: FROZEN PROVENANCE RECORD
Scope: R_joint V1 technical measurement attempts only

## Decision

The project must NOT claim that no measurement execution ever began.

Run `36775748058` partially executed the frozen scorer against project reference data before cancellation.

No final metric result was produced or persisted by the scorer in the inspected artifacts/log behavior.

Accordingly:

**V1 TECHNICAL MEASUREMENT ATTEMPT = PARTIALLY EXECUTED / INVALIDATED / NOT A VALID SCIENTIFIC RESULT**

Any corrected future measurement must be described as occurring after an invalidated partial technical execution, not as the untouched first execution of the scorer.

No threshold, C_F membership, P1/P2 proposal artifact, or primary KEEP/P1/P2 action-space membership may be changed as a consequence of this record.

## Attempt A — run 36775239051

- head SHA: `0e9b3d1464d607b7b7f973b1aaf9070aa008ca10`
- job: `110091374061`
- result: FAILURE
- authorization precheck itself passed using the frozen authorization file.
- measurement command received `--authorization ""`.
- process exited with code 1 immediately after measurement-step launch.
- artifact `11124812311` contained only:
  - `MPSEF_RJOINT_MEASUREMENT_V1_PIP_FREEZE.txt` (0 bytes)
  - `MPSEF_RJOINT_MEASUREMENT_V1_SHA256.txt`
- no measurement summary/per-sentence result file was persisted.

Interpretation:
**FAILED BEFORE USEFUL MEASUREMENT EXECUTION.**

## Attempt B — run 36775748058

- head SHA: `584ea9fc651c2bad4a7d0f0a34127fcfde2ffc1f`
- job: `110093086113`
- result: CANCELLED
- measurement step started successfully with the authorization token.
- recorded scorer progress markers:
  - 1/1918
  - 100/1918
  - 200/1918
  - 300/1918
  - 400/1918
  - 500/1918
- operation was cancelled before completion.
- artifact `11133365933` contained only:
  - `MPSEF_RJOINT_MEASUREMENT_V1_PIP_FREEZE.txt` (0 bytes)
  - `MPSEF_RJOINT_MEASUREMENT_V1_SHA256.txt`
- no measurement summary/per-sentence result file was persisted.

Static inspection of the scorer at the attempted revision establishes:
- inside the main loop it prints only `RJOINT_PROGRESS n/1918`;
- aggregate metric values are calculated only after the full loop;
- summary/per-sentence files and printed summary are emitted only after that calculation.

Therefore there is no evidence in the inspected workflow artifacts/log-output contract that a final or partial numerical R_joint metric was emitted to the operator.

However, target scoring computations necessarily occurred internally for the processed prefix before cancellation.

Interpretation:
**PARTIAL TECHNICAL GOLD-AWARE EXECUTION OCCURRED; NO VALID RESULT; NO FINAL/PERSISTED METRIC OUTPUT FOUND.**

## Exposure classification

- reference/gold was loaded by Attempt B: YES
- scoring logic executed on a prefix: YES
- final 1918/1918 measurement completed: NO
- summary result file persisted: NO
- per-sentence result file persisted: NO
- numerical final metric printed by scorer: NO evidence
- valid scientific result exists: NO
- V1 may be represented as untouched premeasurement: NO

## Consequence

All fixes mandated by the independent review must be justified only by:
- contracts;
- source-code audit;
- synthetic counterexamples;
- provenance/integrity defects;
- independently frozen review requirements.

They must NOT use or request numerical outcomes from the invalidated attempts.

The corrected cycle retains:
- C_F membership 1918/764;
- frozen source manifest SHA256 `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`;
- frozen P1 proposal SHA256 `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`;
- frozen P2 proposal SHA256 `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`;
- the >=95% gate.

This record closes the machine-verifiable portion of independent-review finding F01.
