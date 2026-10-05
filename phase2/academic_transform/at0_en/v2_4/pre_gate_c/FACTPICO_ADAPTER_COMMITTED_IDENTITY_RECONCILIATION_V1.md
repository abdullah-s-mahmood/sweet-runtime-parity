# ACAD_PASS — FactPICO Adapter Committed-Identity Reconciliation V1

Date: 2026-10-05
Status: PROVENANCE RECONCILIATION / NO SCIENTIFIC OR RUNTIME CHANGE

## 1. Discovery

During the authorized preflight on the immutable execution checkout:

`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

the committed FactPICO adapter bytes did NOT match the previously documented SHA-256:

`ab128309261eeffdb734464f2a2fef52cef4ce37bdb3b9654317d6b5bba0b7e1`

The SHA-256 of the adapter bytes actually committed in Git is:

`3b0698772630a17d6d05fdf7197f5faa79b22212332ae785b069318bda4cd5b0`

File:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/factpico_h1_adapter_v5.py`

## 2. Git history verification

Git compare from the adapter implementation commit:

`c36aef499fe28c83b80f1d7a9f296deefa309d2d`

to the immutable execution checkout:

`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

shows NO modification of `factpico_h1_adapter_v5.py`.

Therefore the mismatch is classified as a historical documented-hash/provenance inconsistency, not a post-freeze code mutation.

## 3. Output identity verification

User-supplied FactPICO ZIP:
- size: 2,232,398 bytes
- SHA-256:
  `ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`
- ZIP integrity: PASS

Local deterministic rebuild using the committed adapter logic reproduced:
- prediction input count: 345
- prediction input SHA-256:
  `ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`
- gold SHA-256:
  `6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`
- eligibility SHA-256:
  `d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`
- prediction/gold ID alignment: PASS
- prediction input gold leakage: NONE

## 4. GitHub Actions authorized preflight

Successful preflight run:
`37317413838`

Head:
`fa1ffb4f37e44dec04d29061ba95c5091ee3a46a`

The job checked out the immutable execution commit `659b61...` and verified:
- V2.5 matcher SHA: PASS
- batch runner SHA: PASS
- one-shot guard SHA: PASS
- committed adapter SHA: `3b069877...`
- exact public FactPICO ZIP SHA: PASS
- regenerated prediction input SHA/count/schema: PASS
- no real claim created
- no inference started

Preflight artifact:
`11348064811`

Artifact digest:
`sha256:c3786ba8c6516d959e0f22f075e289868b9765b7aa72c49fe5607a547b4e69e4`

## 5. Interpretation

Scientific contract:
`UNCHANGED`

V2.5 runtime/matcher:
`UNCHANGED`

FactPICO population/gold/eligibility/thresholds:
`UNCHANGED`

Frozen prediction input identity:
`UNCHANGED`

The old adapter SHA remains preserved as historical negative/provenance evidence and MUST NOT be silently erased.

Canonical committed adapter SHA for execution-provenance purposes is now:
`3b0698772630a17d6d05fdf7197f5faa79b22212332ae785b069318bda4cd5b0`

## 6. Attempt state

Real FactPICO attempt:
`UNCONSUMED`

Prediction:
`NOT_RUN`

Gold join:
`NOT_RUN`

Scoring:
`NOT_RUN`

## 7. Next checkpoint

`VERIFY CANONICAL REAL CLAIM ABSENT -> ATOMIC REMOTE CLAIM -> ONE AUTHORIZED PREDICTION RUN -> IMMUTABLE FREEZE -> STOP BEFORE GOLD JOIN`
