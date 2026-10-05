# ACAD_PASS — FactPICO V2.5 Prospective Prediction Execution Freeze V1

Date: 2026-10-05
Status: PREDICTIONS_FROZEN / STOP BEFORE GOLD JOIN

## 1. Authorization

Authorization ID:
`FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001`

Authorized action:
`ONE PROSPECTIVE AT0-EN V2.5 FACTPICO PREDICTION RUN + IMMUTABLE PREDICTION ARTIFACT FREEZE`

No authorization existed for gold join or scoring.

## 2. Successful one-shot execution

GitHub Actions run:
`37318062175`

Workflow:
`.github/workflows/factpico_v25_one_authorized_execution.yml`

Run head:
`066d606e311136c5020ba800c3872b054c11e6da`

Execution checkout:
`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

Run conclusion:
`SUCCESS`

Job:
`one-shot`

Job ID:
`111789731999`

## 3. Frozen input identity

FactPICO source ZIP SHA-256:
`ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`

Prediction input SHA-256:
`ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`

Prediction input count:
`345`

Unique record IDs:
`345`

Input schema:
`record_id / source_text / candidate_text only`

Input identity verification:
`PASS`

Gold SHA verification during deterministic rebuild:
`6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`

Eligibility SHA verification:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

Before inference, the build directory and source ZIP were removed and only the frozen prediction input remained available to the runtime.

## 4. Runtime identity

Runtime:
`AT0-EN V2.5`

Matcher SHA-256:
`ac36409cd32c9a759a3e962ee6a86aa30d0a52299f2a19ccc8206d7b54e248ea`

Batch runner SHA-256:
`7a3383e6108272b641e8f4bcda553a5d97aad7a873616341c3493d425fec6def`

One-shot guard SHA-256:
`574d0c0a1222435069eee48534e2d4e04ca72f6d538bf3c5c334a683304bb6d2`

Committed adapter SHA-256:
`3b0698772630a17d6d05fdf7197f5faa79b22212332ae785b069318bda4cd5b0`

Synthetic controls:
`ABSENT`

Timeout:
`60 seconds per record`

Max assertions per side:
`128`

Retry count:
`0`

Execution:
`STRICTLY SEQUENTIAL`

## 5. Durable attempt consumption

Canonical ledger branch:
`factpico-v25-one-shot-ledger`

Canonical real claim key:
`claims/real/FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001/ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82/ATTEMPT_CLAIM.json`

Pre-claim query:
`ABSENT / HTTP 404`

Remote claim creation commit:
`6387516d84e9ba1109d387dcc4bde715ce2ac16b`

Remote claim blob SHA:
`a1d7bb2df60e55db8f914550858c2accadad1390`

Claim state:
`CONSUMED_BEFORE_INFERENCE`

Read-back equality:
`PASS`

The real authorization is permanently:
`CONSUMED`

No rerun is permitted.

## 6. Prediction freeze

Prediction artifact:
`FACTPICO_V25_PREDICTIONS.jsonl`

Prediction count:
`345`

Unique prediction IDs:
`345`

Exact input/prediction ID order:
`PASS`

Prediction SHA-256:
`925c8a073f4304fe751af072c1d1b8fc64455104e8ed2f23a88c3fc3e6ad496b`

Guard state:
`PREDICTIONS_FROZEN`

Runner stderr:
`EMPTY`

Guard stderr:
`EMPTY`

## 7. Unscored prediction outcome distribution

These are runtime outcomes only, NOT gold-based performance metrics:

- `PASS_CANDIDATE = 0`
- `REJECT = 37`
- `REVIEW = 308`
- `INVALID_VERIFICATION = 0`

Total:
`345`

This distribution MUST NOT be interpreted as accuracy, recall, precision, specificity, F1, calibration, or H1 performance before an explicitly authorized gold join and scoring checkpoint.

## 8. Immutable GitHub artifact

Artifact ID:
`11348646367`

Artifact name:
`factpico-v25-one-prospective-prediction-frozen`

Artifact ZIP size:
`358556 bytes`

Artifact ZIP SHA-256 digest:
`eb68ab179bc17af1105a63ae1ff2f3fc76a4449bffd74a40a76a775319743daa`

Artifact contains 17 files including:
- local `ATTEMPT_CLAIM.json`;
- `PREDICTION_FREEZE.json`;
- frozen predictions;
- runner stdout/stderr;
- remote-claim create/readback evidence;
- execution freeze evidence;
- prediction SHA file;
- stop-boundary evidence.

## 9. Stop boundary

`GOLD_JOIN_PERFORMED = FALSE`

`SCORING_PERFORMED = FALSE`

`STOP_BEFORE_GOLD_JOIN = TRUE`

FactPICO prediction is now:
`RUN_ONCE / COMPLETE / FROZEN`

Gold join:
`NOT_RUN`

Scoring:
`NOT_RUN`

H1 FactPICO performance:
`NOT_YET_MEASURED`

## 10. Negative / provenance evidence preserved

The historical adapter documented-SHA mismatch remains preserved in:
`FACTPICO_ADAPTER_COMMITTED_IDENTITY_RECONCILIATION_V1.md`

It did not alter input identity or prediction execution.

A redundant post-execution launcher created during continuity recovery was removed after discovering the already completed canonical one-shot:
removal commit:
`fc5068dcd8edfa6e84bca420f6a356874176826a`

No second inference run occurred.

## 11. Current exact checkpoint

`FACTPICO V2.5 POST-PREDICTION / PRE-GOLD AUTHORIZATION REVIEW`

Only a separately authorized future checkpoint may permit:
- loading the frozen gold artifact;
- joining gold to the immutable prediction artifact by frozen record IDs;
- computing predeclared FactPICO H1 metrics;
- interpreting performance.

Until then:
`NO GOLD JOIN / NO SCORING / NO RERUN / NO ADAPTATION`
