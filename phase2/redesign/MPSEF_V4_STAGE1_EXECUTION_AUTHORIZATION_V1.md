# MP-SEF V4 STAGE1 EXECUTION AUTHORIZATION V1

Date: 2026-10-01
Authorization type: SOURCE-ONLY / DESCRIPTIVE / PRE-GOLD
Status: AUTHORIZED FOR ONE INITIAL STAGE1 EXECUTION

## 1. Authorized objective

Execute the frozen Stage1 source-only architecture study on:

- 128 C_F UIDs;
- 128 distinct C_F clusters;
- deterministic packet membership selected before proposer outputs;
- P1_CONTROL;
- P2_V2;
- optional P3_V1;
- generic V4 source-only legalizer/action builder;
- source-only diversity diagnostics.

The execution is intended to measure engineering/provenance behavior and candidate diversity only.

## 2. Preconditions satisfied

### Source-free Stage0

Canonical lock:
`MPSEF_V4_PRE_STAGE1_STAGE0_CLOSURE_LOCK_V1.md`

Evidence includes:
- B01 synthetic: 20/20 PASS;
- B01 real-model: PASS;
- B02: 17/17 PASS;
- M01: 4/4 PASS;
- M03: 10/10 PASS;
- M04/M05 scorer V3 synthetic: PASS.

### Independent architecture review remediation

The independent review verdict was:
`MODIFY BEFORE IMPLEMENTATION`

All two BLOCKER design issues and the relevant MAJOR pre-Stage1 issues were addressed in the versioned redesign lane.

### Fresh research re-baseline

Canonical decision:
`ACAD_PASS_PRE_STAGE1_FRESH_RESEARCH_REBASELINE_V2.md`

Frozen roster decision:
- P1: KEEP;
- P2_V2: PROCEED;
- P3_V1: OPTIONAL / PROCEED;
- P4: DEFER;
- V4 consensus: DEFER;
- learned selector: DEFER;
- general LLM primary proposer: DEFER.

### Stage1 tooling preflight

Lock:
`MPSEF_V4_STAGE1_TOOLING_PREFLIGHT_LOCK_V1.md`

Run:
`36873418291`

Result:
- workflow orchestration PASS;
- tooling compilation PASS;
- 6/6 synthetic integration tests PASS;
- project source loaded: false;
- project gold loaded: false.

## 3. Authorized workflow

`.github/workflows/phase2-mpsef-v4-stage1-v1.yml`

Required sequential chain:

`freeze -> p2 -> p3 -> finalize`

No parallel proposer execution is authorized.

The registry produced by the workflow MUST bind the exact trigger commit via `github.sha`.

## 4. Authorized data access

Allowed:

- frozen source-only C_F manifest;
- exact 128-UID / 128-cluster deterministic Stage1 packet derived from it;
- frozen historical P1 source-only proposal artifact;
- frozen/open model weights and runtime dependencies needed for P2_V2/P3.

Forbidden:

- gold/reference corrections;
- target edits;
- QALB correction/reference content for Stage1 scoring;
- INTERNAL_EVALUATION;
- STRESS_DIAGNOSTIC;
- reserved Nahw IDs;
- A7'ta reserve;
- QALB15 TEST;
- any sealed benchmark;
- any hidden correctness label used for proposer retention.

## 5. Authorized outputs

Allowed source-only outputs:

- frozen proposer registry;
- packet manifest and hashes;
- raw P2_V2 proposals;
- raw P3_V1 proposals;
- legalized proposer states;
- exact whole-output action sets;
- candidate-set size;
- exact-output diversity;
- legal marginal contribution;
- KEEP-only reduction;
- source-only leave-one-proposer-out;
- component overlap only where alignment is provably unique;
- M03 shadow protection diagnostics;
- runtime/resource/progress evidence.

## 6. Explicitly forbidden computations/actions

This authorization does NOT permit:

- R_joint;
- correctness scoring;
- precision;
- recall;
- F-score;
- complete-repair scoring;
- safe-repair scoring;
- gold-aware proposer retention;
- selector training;
- learned edit selection;
- V4 consensus generation;
- Stage2;
- protection relaxation;
- modification of historical V3 artifacts.

## 7. Failure rule

The workflow is fail-closed.

Because jobs use explicit sequential dependencies:

- failure in freeze prevents P2;
- failure in P2 prevents P3;
- failure in P3 prevents finalize;
- failure in final legalizer/analyzer prevents Stage1 completion.

No automatic rerun after failure is authorized.

Every failure requires:
1. root-cause analysis;
2. reproducibility;
3. scope;
4. confidence;
5. repairability;
6. source-only safe next action;
7. a versioned repair before any rerun.

## 8. Stage1 interpretation rule

A successful Stage1 is NOT a model-quality PASS.

It can support only source-only conclusions such as:

- proposer execution/provenance readiness;
- legal candidate diversity;
- redundancy;
- protection burden;
- architecture-family overlap;
- runtime cost.

It cannot support:
- which proposer is linguistically best;
- whether an edit is correct;
- whether R_joint will pass;
- whether gold-aware measurement should automatically begin.

## 9. Required post-Stage1 gate

After successful Stage1:

1. freeze all Stage1 artifacts/hashes;
2. report IMPROVED / WORSENED / MIXED versus pre-Stage1 expectations;
3. report exact source-only magnitude changes;
4. report new risks/blockers;
5. perform architecture re-baseline:
   - retain/modify/drop P2_V2;
   - retain/defer P3;
   - decide whether P4 research is required;
   - decide whether V4 consensus remains deferred;
6. perform fresh targeted research/brainstorming if Stage1 changes the architecture question;
7. update `RESUME_HERE.md` and `ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md`;
8. do not open new gold without a separately frozen authorization.

## 10. Trigger identity

The commit created by this authorization file is the execution commit.

The Stage1 registry MUST record that exact commit SHA.

If the workflow checks out a different commit or registry binding differs:
STOP before proposer execution.
