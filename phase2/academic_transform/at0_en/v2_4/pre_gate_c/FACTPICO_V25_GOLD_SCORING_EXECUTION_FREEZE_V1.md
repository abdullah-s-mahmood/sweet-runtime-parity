# ACAD_PASS — FactPICO V2.5 Gold Join and Frozen Scoring Execution V1

Date: 2026-10-05
Status: SCORED / RESULTS FROZEN / STOP BEFORE INTERPRETATION

## 1. Authorization

Independent verdict:
`A. AUTHORIZE_ONE_DETERMINISTIC_FACTPICO_GOLD_JOIN_AND_FROZEN_SCORING_RUN`

Authorized scope was limited to:
- one deterministic exact-record-ID gold join;
- one scoring execution under H1 FactPICO Hard-Gold Contract V5;
- immutable result freeze;
- STOP before interpretation.

No prediction rerun, adaptive retry, runtime/matcher change, threshold/gold/population change, Gate C opening, or Arabic-track work was authorized.

## 2. Pre-gold scorer/config freeze

Freeze workflow:
`FactPICO V2.5 scoring code freeze only`

Freeze run:
`37324968724`

Freeze commit:
`e173187708b95bb0377af2b67f18aa91a66f8285`

Scorer:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/factpico_v25_score_frozen.py`

Scorer SHA-256:
`00df8950ffb3d0ee48925c98ad976e1a940e68069a937396d4b28fdd5923d7fb`

Scoring config:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_H1_SCORING_CONFIG_V1.json`

Config SHA-256:
`bf2c47d0d2b7121c64168d62fc8f51669c22579f5827b6d3e4d0a4f20d304322`

Gold opened during this freeze:
`FALSE`

Scoring performed during this freeze:
`FALSE`

Frozen bootstrap procedure:
- whole-source cluster bootstrap;
- source order = lexicographic source_cluster_id;
- 10,000 resamples;
- seed = 20261004;
- deterministic index generator = `SHA256_COUNTER_MOD_N_V1`;
- percentile method = `TYPE7_LINEAR_INTERPOLATION`;
- CI = 2.5th / 97.5th percentiles.

## 3. One authorized scoring execution

GitHub Actions run:
`37325138336`

Workflow:
`.github/workflows/factpico_v25_one_authorized_scoring.yml`

Workflow commit:
`75494091d8cef50abc0ab752e6deb2fd70eccd0f`

Job ID:
`111813845387`

Conclusion:
`SUCCESS`

Gold-join executions:
`1`

Scoring executions:
`1`

Prediction rerun:
`FALSE`

Adaptive change:
`FALSE`

## 4. Frozen identities

Prediction artifact ID:
`11348646367`

Prediction artifact ZIP SHA-256:
`eb68ab179bc17af1105a63ae1ff2f3fc76a4449bffd74a40a76a775319743daa`

Prediction SHA-256:
`925c8a073f4304fe751af072c1d1b8fc64455104e8ed2f23a88c3fc3e6ad496b`

Gold SHA-256:
`6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`

Eligibility SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

Exact record-ID join:
`PASS / 345 OF 345`

## 5. Hard safety gate

Population:
`ERROR_STRICT = 149 records / 83 sources`

Unsafe event:
`PASS_CANDIDATE`

Unsafe PASS records:
`0`

Unsafe PASS sources:
`0`

Safety gate:
`PASS`

One-sided exact 95% source-level zero-event upper bound:
`0.03544956814588507 = 3.5449568%`

This bound is benchmark-specific only.

## 6. Negative utility gate

Population:
`ERROR_STRICT`

Success event:
`REJECT`

Observed outcomes:
- REJECT = 16
- REVIEW = 133
- PASS_CANDIDATE = 0
- INVALID_VERIFICATION = 0

Pair-micro REJECT:
`0.10738255033557047 = 10.7383%`

95% whole-source bootstrap CI:
`[5.7971%, 16.2338%]`

Source-macro REJECT:
`0.09437751004016064 = 9.4378%`

95% whole-source bootstrap CI:
`[4.8193%, 14.8594%]`

Frozen threshold:
`75%`

Pair gate:
`FAIL`

Source gate:
`FAIL`

Negative utility gate:
`FAIL`

## 7. Positive anti-degeneracy gate

Population:
`SAFE_STRICT_CONTROL = 34 records / 33 sources`

Success event:
`PASS_CANDIDATE`

Observed outcomes:
- PASS_CANDIDATE = 0
- REJECT = 6
- REVIEW = 28
- INVALID_VERIFICATION = 0

Pair-micro PASS:
`0.0 = 0%`

95% whole-source bootstrap CI:
`[0%, 0%]`

Source-macro PASS:
`0.0 = 0%`

95% whole-source bootstrap CI:
`[0%, 0%]`

Frozen threshold:
`75%`

Pair gate:
`FAIL`

Source gate:
`FAIL`

Positive anti-degeneracy gate:
`FAIL`

## 8. Diagnostic classes

INTERMEDIATE:
- records = 153
- REJECT = 14
- REVIEW = 139
- PASS_CANDIDATE = 0
- INVALID = 0

N_A_SOURCE_DIAGNOSTIC:
- records = 9
- REJECT = 1
- REVIEW = 8
- PASS_CANDIDATE = 0
- INVALID = 0

All 345 joined rows are preserved in the frozen scoring artifact.

## 9. Frozen decision

Mechanical V5 scoring decision:
`H1_FULL_PASS_NOT_ACHIEVED`

This is a FactPICO source-bounded critical RCT/PICO fidelity subgate result only.

It does NOT by itself establish:
- complete H1 failure across all constructs;
- universal academic-document failure;
- production readiness or non-readiness;
- the correct repair strategy.

Those interpretations are explicitly deferred to the next independent checkpoint.

## 10. Result identities

Joined rows SHA-256:
`144b778ae9ea1ee2c511dca862f1f0fe937e9b922d0e64df94eb0174c4f0e10f`

Scoring summary SHA-256:
`301d9f6fc0f2ca9b92493b314c63aceab2febb33318e823f3f1211cbb2cc8859`

Diagnostics SHA-256:
`5759d5e4f1d57f96225c9dd381154f8298f475a959fa37390a5faf43a0ac2ea8`

Frozen scoring artifact:
- artifact ID: `11351451888`
- artifact name: `factpico-v25-one-gold-scoring-frozen`
- ZIP size: `40909 bytes`
- ZIP SHA-256: `105534207a4566c38d76174e9cd263244b87e37358b6007c76502bc250d67e77`

## 11. Stop boundary

`RESULTS_FROZEN = TRUE`

`INTERPRETATION_PERFORMED = FALSE`

`STOP_BEFORE_INTERPRETATION = TRUE`

No prediction rerun or scoring rerun is permitted under this authorization.

## 12. Current exact checkpoint

`FACTPICO V2.5 POST-SCORING INDEPENDENT INTERPRETATION / NEXT-DECISION REVIEW`
