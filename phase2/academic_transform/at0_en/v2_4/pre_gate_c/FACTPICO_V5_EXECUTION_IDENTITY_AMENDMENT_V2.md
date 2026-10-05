# ACAD_PASS — FactPICO V5 Execution Identity Amendment V2

Date: 2026-10-05
Status: RUNTIME/EXECUTION-CONTROL IDENTITY AMENDMENT ONLY / NO GOLD CHANGE / NO FACTPICO EXECUTION

Supersedes for future execution identity:
`FACTPICO_V5_EXECUTION_IDENTITY_AMENDMENT_V1.md`

## 1. Scientific contract unchanged

Unchanged:
- FactPICO archive;
- 345-record prediction universe;
- source/candidate texts;
- record IDs;
- V5 eligibility classes;
- PICO/Results/Added-Information interpretation;
- SAFE_STRICT_CONTROL membership;
- ERROR_STRICT membership;
- thresholds;
- source clustering;
- input/gold hashes;
- prediction/gold separation;
- scoring protocol;
- claim boundary.

FactPICO remains:
`SOURCE-BOUNDED CRITICAL RCT/PICO FIDELITY SUBGATE`

not complete H1.

## 2. Future execution identity

Runtime:
`AT0-EN V2.5`

Current runtime freeze:
`phase2/academic_transform/at0_en/v2_5/AT0_EN_V2_5_RUNTIME_FREEZE_V2.md`

Final regression run:
`37289569561`

Head:
`29e3abe5ccb708cb88d94ae00630eaa0fdc2b123`

Artifact:
`11335647986`

Artifact digest:
`sha256:61d82aa30de89e84aa5bc0433bdfa528259269c0b3630648df5c0d4c95573b63`

## 3. Frozen FactPICO artifacts

Prediction input SHA-256:
`ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`

Separate gold SHA-256:
`6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`

Eligibility SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

Record count:
`345`

No artifact is regenerated because of the runtime/control changes.

## 4. Frozen external execution policy

For a future separately authorized prediction run:

- use `run_v2_5_one_shot_guard.py`;
- expected input SHA exactly as above;
- expected count `345`;
- max assertions/side `128`;
- per-record timeout `60 s`;
- strictly sequential;
- retry count `0`;
- timeout/crash/out-of-envelope -> visible `INVALID_VERIFICATION`;
- synthetic test mode/environment MUST be absent;
- output path must not exist;
- attempt ledger must be claimed before inference;
- attempt ledger storage must survive parent cancellation/failure;
- cancellation/crash after claim consumes the attempt;
- no automatic restart;
- predictions must be hashed/frozen before any gold join;
- a second attempt or output replacement under the same authorization is forbidden.

## 5. Synthetic regression budget distinction

The internal matcher regression criterion is:
`30 s`
for the supported synthetic max-shape checks.

This is NOT the external record timeout.

External per-record timeout remains:
`60 s`

The 30 s value was selected from synthetic evidence only and before any FactPICO runtime profiling.

## 6. Prediction replacement protection

Batch runner refuses an existing output path.

One-shot guard:
- claims attempt before inference;
- writes frozen prediction hash after success;
- refuses reuse of the attempt directory.

This closes the prediction-replacement risk identified by the independent reviewer, subject to the real attempt directory being durably preserved.

## 7. Exposure

FactPICO prospective prediction:
`NOT_RUN`

No FactPICO extraction/count/timing/prediction/scoring was used to create this amendment.

## 8. Authorization

This amendment does NOT authorize FactPICO execution.

Current stop:
`FINAL HIGHER-MODEL PRE-PREDICTION RE-REVIEW`

Maximum possible next authorization, if independently approved:
`ONE PROSPECTIVE AT0-EN V2.5 FACTPICO PREDICTION RUN + IMMUTABLE PREDICTION ARTIFACT FREEZE ONLY`

Gold join/scoring remains separate.
