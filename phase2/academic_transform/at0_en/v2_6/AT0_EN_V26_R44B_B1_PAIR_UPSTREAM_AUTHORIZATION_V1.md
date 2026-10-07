# ACAD_PASS — R44-B B1 Pair-Exclusion Upstream Authorization V1

Date: 2026-10-07
Status: AUTHORIZED — 10 PARALLEL PAIR-EXCLUSION UPSTREAM JOBS + LABEL-INDEPENDENT CONTEXT CACHE ONLY

Prerequisites:
- R44-A final run `37581447046`: SUCCESS.
- R44-A full OOF audit `37682327706`: `R44A_FULL_OOF_AUDIT_PASS`.
- R44-B B1 protocol freeze commit `d70f36bd65877ecc903cab485c8123c0e6887092`.
- R44-B B1 preflight run `37682982987`: SUCCESS.
- preflight artifact `11510186523`
- preflight digest `sha256:82e26882fbfef480c478fa51f30ec9444255ace9f763c749e1f8f31e1c19bca9`
- preflight state `R44B_B1_PREFLIGHT_PASS`.
- logical inner fits = 20; unique physical pair fits = 10.
- J0 params = 584631; J1 params = 667836.

## Authorized scientific work
Exactly the 10 unordered excluded pairs:
- 0-1
- 0-2
- 0-3
- 0-4
- 1-2
- 1-3
- 1-4
- 2-3
- 2-4
- 3-4

For pair {a,b}:
- training = DESIGN minus folds a and b;
- B_CANDIDATE and C_BOUNDARY only;
- same frozen R44-A upstream hyperparameters;
- infer separately on held-out side a and side b;
- assign labels only after inference;
- freeze both side candidate banks;
- upload NO model weights.

## Parallel execution
Authorized:
`max-parallel: 10`

Reason:
- all pair jobs use immutable common inputs;
- output namespaces are pair-specific;
- no job consumes another pair result;
- no shared mutable state;
- each pair has a fixed deterministic train set;
- aggregation occurs only after all ten complete.

GitHub may run fewer than ten concurrently if account runner capacity is lower; queueing does not change scientific semantics.

## Authorized technical work in parallel
One label-independent frozen-base context-cache job may run concurrently.
It:
- uses only DESIGN tokens;
- uses immutable converted BiomedBERT;
- performs no supervised training;
- does not use labels to compute representations;
- produces float32 word-level vectors + immutable index/hashes.

## Still NOT authorized
- J0/J1 head training;
- threshold evaluation;
- VERIFY_INTERNAL;
- old SELECT;
- historical DEV/test;
- protected external tests;
- boundary repair;
- architecture escalation.

## Stop
After the 10 pair jobs:
`PAIR_AGGREGATE_AUDIT -> CONTEXT_CACHE_VERIFY -> STOP -> SEPARATE_HEAD_TRAINING_AUTHORIZATION`.
