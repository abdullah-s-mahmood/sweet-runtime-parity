# MP-SEF SOURCE-ONLY PROPOSER DIVERSITY PROTOCOL V1

Date: 2026-10-01
Status: PRE-RUN FREEZE
Scope: P1 control + P2_V2 + P3_V1
Gold/reference use: FORBIDDEN

## 1. Objective

Determine whether new proposer families add real, reproducible, source-only candidate diversity and provenance value before any new gold-aware measurement.

This protocol does NOT measure linguistic correctness.

## 2. Candidate systems

### P1_CONTROL
Frozen family:
`P1_SWEET_QALB14_NOPNX_ITER2`

Role:
historical/current control.

### P2_V2
Repaired heterogeneous Seq2Seq++ / AraBART + GED/morphology proposer.

Role:
architecturally distinct candidate generator.

### P3_V1
`SWEET_QALB14_NOPNX_ITER2 -> SWEET_QALB14_PNX_ITER1`

Role:
published text-editing cascade extension.

## 3. Population sequence

Stage 0 — synthetic only:
- no project sentence population;
- alignment, truncation, parity and failure-injection tests.

Stage 1 — small source-only parity packet:
- selected deterministically from C_F UID hashes before outputs are inspected;
- no gold/reference;
- used only to establish reproducibility and P1 parity where required.

Stage 2 — full C_F source-only diversity:
- permitted only after Stage 0/1 PASS and independent architecture review;
- 1,918 cases / 764 clusters;
- no project gold.

## 4. Hard engineering gates

A proposer may enter Stage 2 only if all applicable gates pass:

1. exact model/tokenizer/runtime identities frozen;
2. deterministic/source-only input identity PASS;
3. batch-vs-single parity PASS on preregistered packet;
4. no silent UID loss;
5. no duplicate UID;
6. no silent token/label truncation;
7. unknown truncation never executable;
8. output hash recorded for every row;
9. failure rows retained rather than dropped;
10. protected/legalizer path fails closed;
11. repeated-run output parity PASS on preregistered packet;
12. no gold/reference access.

These are non-negotiable.

## 5. Source-only metrics

For every proposer:

- total rows;
- execution success;
- explicit failure-state counts;
- empty outputs;
- changed-vs-source count;
- protected-touch count;
- legalizer-executable count;
- truncation/ceiling count;
- runtime total and per sentence;
- candidate output SHA distribution;
- provenance-completeness count.

For each pair of proposers:

- exact-output agreement count;
- exact-output disagreement count;
- unique-to-A output count;
- unique-to-B output count;
- source→output component overlap;
- source→output component disagreement;
- protected-touch disagreement;
- legalizer-state disagreement;
- output-length difference distribution.

For the full candidate pool:

- unique whole outputs per sentence;
- distribution of candidate-set size;
- mean/median/p95/max candidate-set size;
- sentences with only KEEP;
- sentences with exactly one non-KEEP candidate;
- sentences with >=2 distinct non-KEEP candidates;
- exact duplicate hypotheses after dedup;
- proposer provenance retained after dedup.

## 6. Edit/component diversity

Component diversity is diagnostic only.

For each source-output pair, derive source-anchored components using the frozen source-only alignment contract.

Report pairwise:

- exact component-set equality;
- intersection size;
- union size;
- Jaccard similarity where union >0;
- boundary-touch overlap;
- punctuation-only component overlap;
- non-punctuation component overlap;
- mixed/protected-region overlap.

Do NOT use any reference to decide whether a component is correct.

## 7. Architectural independence labels

Before source-only results are seen, classify proposer relationships:

- P1 vs P2_V2: HETEROGENEOUS
  - text-edit tagging vs autoregressive Seq2Seq+GED/morphology.

- P1 vs P3_V1: RELATED / CASCADE EXTENSION
  - same NoPnx base, plus punctuation stage.

- P2_V2 vs P3_V1: HETEROGENEOUS.

These labels must be used when interpreting consensus support.

Two correlated variants must not be counted as two fully independent evidence families merely because they are separate model calls.

## 8. Consensus feasibility diagnostics

No consensus output is executable under V3.

For a possible V4 only, report source-only hypothetical support structure:

- edits supported by P1 and P2_V2;
- edits supported by P1 and P3_V1;
- edits supported by P2_V2 and P3_V1;
- edits supported by all three;
- edits proposed by only one family;
- conflicts/overlaps that cannot be merged deterministically.

This is DIAGNOSTIC ONLY.

No V4 consensus output may be generated for primary measurement until a separate consensus contract is reviewed and frozen.

## 9. Retention criteria

No proposer is retained merely because a publication reports strong benchmark performance.

Retention requires:

### Mandatory
- all engineering gates pass;
- provenance is complete;
- no new unbounded safety channel;
- source-only legalizer integration is possible.

### Comparative
The proposer must provide at least one defensible value:
- architecturally distinct candidate outputs;
- distinct legalizable candidate coverage;
- materially different failure profile;
- lower runtime for comparable candidate behavior;
- a published complementary role that is reproduced source-only in ACAD_PASS.

No arbitrary correctness inference may be made from source-only diversity.

A numeric diversity threshold is deliberately NOT frozen in V1 because no ACAD_PASS source-only diversity distribution has yet been observed.

Before Stage 2 full-C_F execution, an independent review must decide whether a numeric retention threshold is methodologically justified.

## 10. Failure triage

Every failure follows:
`ACAD_PASS_FAILURE_TRIAGE_CONTRACT_V1.md`

Required:
- observed failure;
- reproducibility;
- root cause;
- scope;
- confidence;
- repairability;
- current-cycle vs next-version action.

## 11. Output artifacts

Stage 1 must produce:

- `MPSEF_PROPOSER_DIVERSITY_STAGE1_ROWS.jsonl`
- `MPSEF_PROPOSER_DIVERSITY_STAGE1_SUMMARY.json`
- `MPSEF_PROPOSER_DIVERSITY_STAGE1_FAILURES.jsonl`
- `MPSEF_PROPOSER_DIVERSITY_STAGE1_SHA256.txt`

Stage 2, if authorized, must use new explicit artifact names and hashes.

## 12. Scientific boundary

Forbidden during this protocol:

- R_joint;
- precision/recall/F-score;
- correctness scoring;
- complete-repair scoring;
- selector training;
- gold-aware retention;
- opening INTERNAL/STRESS/reserved populations.

## 13. Next gate

Independent higher-model architecture review must inspect:

- V1 frozen evidence;
- P2 failure/root cause;
- P2_V2 specification;
- P3_V1 specification;
- this diversity protocol;
- fresh literature evidence.

Only after review may source-only prototypes proceed beyond synthetic/small parity work.
