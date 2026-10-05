# ACAD_PASS — FactPICO V5 Execution Identity Amendment V3

Date: 2026-10-05
Status: FINAL PRE-AUTHORIZATION EXECUTION IDENTITY / NO FACTPICO EXECUTION

Supersedes:
`FACTPICO_V5_EXECUTION_IDENTITY_AMENDMENT_V2.md`

## 1. Scientific contract unchanged

Unchanged:
- FactPICO archive;
- 345-record population;
- source/candidate texts;
- record IDs;
- V5 eligibility;
- thresholds;
- source clustering;
- input/gold hashes;
- scoring protocol;
- claim boundary.

FactPICO remains:
`SOURCE-BOUNDED CRITICAL RCT/PICO FIDELITY SUBGATE`

not complete H1.

## 2. Final runtime / regression identity

Runtime:
`AT0-EN V2.5`

Final execution-control closure:
`V2_5_FINAL_EXECUTION_CONTROL_CLOSURE_V1.md`

Final successful regression:
- run `37312305371`
- head `659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`
- artifact `11345959688`
- artifact ZIP SHA-256 `f3510bd4cacdb40a70d6b37d6d9f6fac24a9d77285462723f1e0738eb374a701`

Frozen implementation hashes:
- matcher:
  `ac36409cd32c9a759a3e962ee6a86aa30d0a52299f2a19ccc8206d7b54e248ea`
- batch runner:
  `7a3383e6108272b641e8f4bcda553a5d97aad7a873616341c3493d425fec6def`
- one-shot guard:
  `574d0c0a1222435069eee48534e2d4e04ca72f6d538bf3c5c334a683304bb6d2`
- one-shot control spec:
  `a615988ff14b64307576b367da593175c742f8c9a6e7928fc195f9811c21afed`
- regression test:
  `81fb84f28668804b95844adc32a3d7743061e89aa69bec2a2c89129b57b4d471`
- regression report:
  `b2248f62724e3d9a7a30f34bb42ff97e287bc608e9852e78bf13fcee63fc3a2a`

## 3. Frozen FactPICO artifacts

Prediction input SHA-256:
`ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`

Separate gold SHA-256:
`6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`

Eligibility SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

Count:
`345`

## 4. Durable attempt identity

Provider:
`github:abdullah-s-mahmood/sweet-runtime-parity@factpico-v25-one-shot-ledger`

Authorization ID:
`FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001`

Canonical REAL claim key:

`claims/real/FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001/ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82/ATTEMPT_CLAIM.json`

The remote claim must be atomically created before inference.

If it already exists:
`ABORT — ATTEMPT ALREADY CONSUMED`

The real claim key is currently:
`ABSENT / UNCONSUMED`

## 5. Final execution policy

If separately authorized:

1. verify exact input SHA;
2. require exactly 345 unique IDs in frozen order;
3. verify real durable claim key absent;
4. atomically create real remote claim;
5. fetch remote claim and retain commit/blob identity;
6. launch local one-shot guard bound to:
   - authorization ID;
   - durable provider;
   - durable key;
   - remote claim commit SHA;
7. synthetic-test environment variables absent;
8. strictly sequential execution;
9. zero retries;
10. 60 s/record;
11. max 128 assertions/side;
12. exactly one output per ID;
13. all INVALID outcomes visible;
14. no gold or eligibility labels available to inference;
15. no result-adaptive resource/parameter changes;
16. freeze prediction SHA and evidence;
17. STOP before gold join.

Cancellation/crash after remote claim creation consumes the attempt.

No alternate key/path/provider may reset it.

## 6. Exposure

FactPICO prediction:
`NOT_RUN`

FactPICO profiling/timing:
`NOT_RUN`

FactPICO scoring:
`NOT_RUN`

Gold join:
`NOT_RUN`

## 7. Authorization boundary

This amendment does NOT itself authorize execution.

Current checkpoint:

`FINAL EXECUTION AUTHORIZATION REVIEW`

Maximum possible approval:

`ONE PROSPECTIVE AT0-EN V2.5 FACTPICO PREDICTION RUN + IMMUTABLE PREDICTION ARTIFACT FREEZE ONLY`

Gold join/scoring remains separate.
