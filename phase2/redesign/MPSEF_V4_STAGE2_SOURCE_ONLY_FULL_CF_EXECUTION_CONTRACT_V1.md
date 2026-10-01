# MP-SEF V4 STAGE2 SOURCE-ONLY FULL-C_F EXECUTION CONTRACT V1

Date: 2026-10-01
Status: FROZEN FOR INDEPENDENT/HIGHER-MODEL REVIEW BEFORE EXECUTION
Stage: V4 Stage2
Gold/reference use: FORBIDDEN
R_joint: FORBIDDEN
Selector training: FORBIDDEN

## 1. Purpose

Scale the already protocol-complete Stage1 source-only engineering/diversity analysis from the deterministic 128-case packet to the full frozen C_F population without introducing linguistic-quality evaluation.

Stage2 measures:
- execution completeness;
- provenance stability;
- protection/legalization behavior;
- literal action diversity;
- proposer redundancy;
- architecture-family availability;
- resource cost;
- full-population source-only failure modes.

Stage2 does NOT measure:
- correction correctness;
- precision;
- recall;
- F-score;
- R_joint;
- complete repair;
- safe repair;
- human preference;
- selector accuracy.

## 2. Canonical full-C_F identity

Canonical source manifest:
`MPSEF_CF_SOURCE_MANIFEST_V1`

Frozen evidence:
- cases: 1,918
- clusters: 764
- role: C_F
- source manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- protected detector:
  `MPSEF_PROTECTED_DETECTOR_V1`
- reference content used: false
- gold edit content used: false

Historical P1 lock:
`MPSEF_P1_CF_PROPOSAL_LOCK_V1.md`

C_F manifest builder role digest:
`85a5dcb1b26a9773ea0ef7e04bb42e8e56dde5d44f1e63fcbe54141dbcb47dfc`

Any mismatch in case count, cluster count, role digest, manifest SHA, UID set, cluster set, or source SHA is a hard Stage2 BLOCK.

## 3. Frozen roster

Registry namespace:
`MPSEF-V4-CANDIDATE-REGISTRY-20261001-A`

Authorized actions:
- KEEP
- P1_CONTROL_SWEET_QALB14_NOPNX_ITER2
- P2_V2_ARABART_GED_MORPH_WORDALIGNED
- P3_V1_SWEET_NOPNX2_PNX1

Architecture families:
- KEEP: system action, not a model family
- SWEET_QALB14: P1 + P3
- SEQ2SEQ_GED_MORPH: P2_V2

P1 and P3 MUST NOT count as two independent family votes.

P4:
DEFERRED for Stage2 execution, but mandatory to reconsider after Stage2 source-only evidence.

## 4. Artifact reuse and new execution

### P1

Do NOT rerun P1.

Reuse exact frozen full-C_F proposal artifact:
- run: 36765798233
- artifact: 11123050529
- artifact digest:
  `sha256:e4020418ca2f2793d4bb79bc766e26838398fb9affba6d0f1c704255cd5aed46`
- proposal JSONL SHA256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- cases: 1,918/1,918

P1 runtime identity:
- model revision:
  `21286e56ce98a86362db540863f91c083b8970f9`
- weight SHA256:
  `9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d`
- text-editing revision:
  `4d552ca3ae98029550f27fc52aa1b22883e16e61`

### P2_V2

Generate a new full-C_F source-only artifact using the exact Stage1/B01-corrected P2_V2 semantics.

No fallback to historical defective P2 is permitted.

Every UID must preserve:
- source identity;
- morph-word identity;
- segment identity;
- first-wordpiece GED semantics;
- label identity;
- GEC input identity;
- generation completion/EOS state;
- complete failure reasons.

### P3_V1

Generate a new full-C_F source-only artifact.

P3 input MUST be the exact frozen P1 output for the same UID.

Do not rerun P1 inside P3.

Required identity:
`P3_input_sha256 == P1_frozen_output_sha256`

Failure:
`P3_PARENT_OUTPUT_IDENTITY_MISMATCH`

## 5. Stage2 runner replay gate

Any new Stage2 P2 or P3 runner MUST pass the already frozen Stage1 Parity32 population before full-C_F execution.

Parity32 manifest SHA:
`384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e`

P2 Stage2 runner replay must reproduce:
- fresh_vs_repeat: 32/32
- fresh_vs_reordered: 32/32
- fresh_vs_frozen_trace_output: 32/32

P2 true model-call batch remains:
`NOT_APPLICABLE_SINGLE_CASE_MODEL_CALL_IMPLEMENTATION`

P3 Stage2 runner replay must reproduce:
- single_vs_batch: 32/32
- batch_vs_reversed: 32/32
- batch_vs_repeat: 32/32
- batch_vs_frozen_trace: 32/32
- batch_output_vs_frozen_output: 32/32
- parent_identity: 32/32

A Stage2 runner that fails replay does not proceed to 1,918 cases.

## 6. Denominators

All summaries declare numerator and named denominator.

### D_all
All 1,918 C_F UIDs.

Failures remain in D_all.

### D_raw_valid_j
Rows with valid source/runtime/provenance identity before model execution-state filtering.

### D_exec_j
Rows executable under proposer j.

### D_legal_j
Rows with a complete legal whole output after authoritative protection/reversibility legalizer.

### D_joint_exec_jk
Rows executable under both j and k.

### D_joint_legal_jk
Rows legal under both j and k.

### D_family_nonkeep_f
UIDs with at least one legal non-KEEP action carrying architecture family f.

No denominator may silently exclude failures.

## 7. Terminal state accounting

Every proposer must produce exactly one terminal state for every UID.

Required:
`sum(state_counts_j) == 1918`

Unknown conditions are fail-closed.

No failure may be represented as empty output for agreement or deduplication.

No failed UID is dropped.

## 8. Legal action-set semantics

Every UID begins with KEEP.

Only complete legal whole outputs enter the action set.

Literal whole-output equality is exact:
- no Unicode normalization;
- no whitespace normalization;
- no Arabic-letter folding;
- no punctuation stripping.

Maximum raw action capacity remains:
`1 + 3 = 4`

Dedup retains all provenance.

A larger edit is not considered more diverse, better, or worse merely because it differs more from source.

## 9. Authoritative protection

Use the frozen V4 authoritative source-only legalizer/protection stack.

Shadow diagnostics may be reported but MUST NOT rescue a blocked action.

Required source-only diagnostics include:
- protected entity changed;
- separator/linkage changed;
- local attachment changed;
- global ordinal-only disagreement;
- citation movement;
- unit/number/percent linkage;
- alignment ambiguity;
- proof-budget exceeded;
- other frozen reason codes.

Protection failure is not called a linguistic false positive.

## 10. Core full-population diagnostics

### 10.1 Per-proposer engineering

For P1/P2/P3:
- D_all;
- raw-valid;
- executable;
- failed;
- legal;
- protection-blocked;
- changed-vs-source;
- alignment-state counts;
- failure-reason matrix;
- cluster counts for each state;
- runtime/resource summaries.

### 10.2 Action-set size

For every UID report:
`|L_i|` where KEEP is always present.

Histogram:
- 1 action;
- 2 actions;
- 3 actions;
- 4 actions.

Report UID and cluster counts.

### 10.3 Legal marginal contribution

Preserve the frozen Stage1 definition:
`SOURCE_ONLY_LEGAL_MARGINAL_CONTRIBUTION`

Report for each proposer:
- UIDs with MC>0;
- clusters with MC>0;
- total unique legal outputs contributed.

This is not recall.

### 10.4 KEEP-only reduction

Preserve:
`SOURCE_ONLY_KEEP_ONLY_REDUCTION`

Report UID and cluster counts.

This is not correction coverage.

### 10.5 Leave-one-proposer-out

Preserve:
`SOURCE_ONLY_LEAVE_ONE_PROPOSER_OUT`

Report:
- unique legal actions;
- UIDs/clusters with >=1 non-KEEP legal action;
- deltas after removing each proposer.

No quality terminology.

## 11. New Stage2 family-aware diagnostics

These metrics are frozen before Stage2 output inspection.

### 11.1 Independent non-KEEP family count

For each UID, count distinct architecture families among legal non-KEEP actions after whole-output dedup:

Allowed count:
- 0
- 1
- 2

P1 and P3 both map to SWEET_QALB14.

Name:
`SOURCE_ONLY_INDEPENDENT_NONKEEP_FAMILY_COUNT`

Report histogram by UID and distinct cluster.

### 11.2 Family availability state

Classify each UID:
- NONE
- SWEET_ONLY
- SEQ2SEQ_GED_MORPH_ONLY
- BOTH_FAMILIES

Name:
`SOURCE_ONLY_FAMILY_AVAILABILITY_STATE`

This is architecture availability, not correctness support.

### 11.3 Cross-family exact output agreement

Count legal non-KEEP whole outputs whose retained provenance contains both independent families.

Name:
`SOURCE_ONLY_CROSS_FAMILY_EXACT_OUTPUT_AGREEMENT`

Report UID count, cluster count, and total shared actions.

Do not interpret exact agreement as correctness.

### 11.4 Family leave-one-out

Remove all provenance/actions from one architecture family at a time.

Report:
- UIDs/clusters becoming KEEP-only;
- change in unique legal action count;
- UIDs/clusters retaining a non-KEEP action from the other family.

Name:
`SOURCE_ONLY_LEAVE_ONE_FAMILY_OUT`

### 11.5 Family dominance diagnostics

Report only descriptive counts:
- legal non-KEEP actions supplied by each family;
- UIDs/clusters where only one family supplies any non-KEEP action;
- UIDs/clusters where both families supply at least one non-KEEP action.

Do not label a family BEST/WORST/STRONG/WEAK from these counts.

## 12. Pairwise/component diagnostics

For P1-P2, P1-P3, P2-P3 report:
- D_all execution-state matrix;
- D_joint_exec exact equality/difference;
- D_joint_legal exact equality/difference;
- component exact-set equality;
- component Jaccard only when both alignments are UNIQUE;
- alignment-state pair matrix.

Non-computable alignments are N/A, never forced to zero similarity.

## 13. Change-burden diagnostics

For each proposer:
- output/input character ratio;
- absolute character delta;
- absolute whitespace-token delta;
- component count;
- p50;
- p95 nearest-rank;
- max.

For P3 additionally:
- P1 -> P3 change burden;
- source -> P3 change burden;
- Stage-B domain counts:
  - NO_CHANGE;
  - PUNCTUATION_ONLY;
  - BOUNDARY_ONLY;
  - LEXICAL_ONLY;
  - MIXED.

These are over-edit/anomaly diagnostics only.

Recent GEC literature motivates explicit over-correction/minimal-edit monitoring, but Stage2 will not infer semantic correctness from burden alone.

## 14. P2_V2 full-population diagnostics

For D_all report:
- morphology success/failure;
- GED tokenization success/failure;
- zero-token-word failures;
- single-word-over-budget failures;
- GED segment count;
- total GED wordpieces;
- exact word-identity coverage;
- unknown/unmapped label failures;
- GEC tokenization failures;
- GEC input-too-long failures;
- generation incomplete/ceiling/EOS failures;
- model-interface proof status.

The historical defective P2 pipeline is never used as fallback.

## 15. Runtime/resource budget

Stage2 is an engineering scale-up.

Hardware class:
GitHub-hosted Ubuntu 22.04 CPU unless a separately frozen amendment changes it before execution.

P1:
artifact reuse only; no inference budget.

P2_V2:
- workflow timeout: 240 minutes;
- heartbeat: <=60 seconds during active inference;
- stale threshold: 600 seconds;
- kill-on-stale: true.

Rationale:
Stage1 P2_V2 CPU runtime was ~581 s for 128 cases; simple linear scaling to 1,918 is ~145 minutes before setup/variance. A 240-minute ceiling provides engineering margin without hiding pathological stalls.

P3_V1:
- workflow timeout: 90 minutes;
- heartbeat <=60 seconds;
- stale threshold: 600 seconds;
- kill-on-stale: true.

Stage2 legalizer/diversity analysis:
- workflow timeout: 60 minutes;
- heartbeat <=60 seconds when applicable;
- stale threshold: 600 seconds.

Timeout/OOM/stale:
`ENGINEERING_FAIL_PENDING_TRIAGE`

No linguistic inference may be drawn.

## 16. Required Stage2 artifacts

Before proposer execution:
- `MPSEF_V4_STAGE2_INPUT_LOCK_V1.md`
- exact C_F manifest identity/hashes;
- Stage2 runner implementation hashes;
- replay-gate artifact.

After P2:
- full P2 proposal JSONL;
- P2 summary;
- P2 progress;
- environment freeze;
- SHA256 ledger.

After P3:
- full P3 proposal JSONL;
- P3 summary;
- P3 progress;
- environment freeze;
- SHA256 ledger.

After analysis:
- `MPSEF_V4_STAGE2_PROPOSER_ROWS_V1.jsonl`
- `MPSEF_V4_STAGE2_LEGAL_ACTION_SETS_V1.jsonl`
- `MPSEF_V4_STAGE2_DIVERSITY_SUMMARY_V1.json`
- `MPSEF_V4_STAGE2_FAMILY_SUMMARY_V1.json`
- `MPSEF_V4_STAGE2_FAILURES_V1.jsonl`
- `MPSEF_V4_STAGE2_RUNTIME_V1.json`
- `MPSEF_V4_STAGE2_SHA256.txt`
- final Stage2 result lock.

## 17. Full-population redundancy rule

A proposer may be considered source-only redundant only if the full 1,918-case population demonstrates all of:

1. zero unique legal whole-output contribution;
2. no distinct legal failure profile needed by the architecture;
3. another proposer supplies the same legal behavior;
4. retained proposer is equal or cheaper under frozen resource accounting.

This is redundancy elimination, not a correctness judgment.

No proposer is dropped mid-Stage2.

## 18. P4 reconsideration after Stage2

P4 review is mandatory after Stage2.

Stage2 may strengthen the case for P4 if source-only evidence shows:
- architecture-family availability is highly one-sided;
- BOTH_FAMILIES availability is limited;
- family leave-one-out collapses non-KEEP availability for many UIDs/clusters;
- full-population diversity is materially less robust than Stage1 descriptive evidence suggested;
- a current proposer becomes full-population redundant;
- a new reproducible third-family checkpoint becomes available.

No Stage2 source-only statistic proves that P4 would improve correctness.

A P4 training/integration decision requires a new frozen record.

## 19. Stage2 stop conditions

Stop and triage before continuing if:
- C_F manifest identity mismatch;
- registry identity mismatch;
- Stage2 runner fails frozen Parity32 replay;
- P1 parent identity mismatch for P3;
- model/runtime identity mismatch;
- unknown silent truncation;
- UID loss/duplication;
- provenance incomplete;
- heartbeat stale timeout;
- artifact hash inconsistency.

Do not repair and continue silently in the same evidence record.

## 20. Research-informed safeguards

Fresh 2025-2026 GEC literature reinforces:
- heterogeneous system outputs can improve combination quality;
- over-correction remains a central failure mode;
- voting/combination can trade precision against recall;
- multiple valid references/corrections complicate quality measurement;
- edit-level validity and minimal-edit behavior should not be conflated with literal reference matching.

Therefore Stage2 freezes source-only structural diagnostics and does not introduce an automated linguistic judge.

## 21. Authorization boundary

This contract authorizes only:
1. Stage2 input-lock materialization;
2. Stage2 runner replay preflight;
3. full-C_F P2_V2 source-only execution;
4. full-C_F P3_V1 source-only execution using frozen P1 parent;
5. source-only legalizer/dedup/diversity/family analysis.

It does NOT authorize:
- gold/reference opening;
- R_joint;
- correctness scoring;
- LLM-as-judge;
- JELV deployment;
- human correctness adjudication;
- learned selector;
- consensus activation;
- Stage3.

## 22. Review gate

This contract MUST receive an independent/higher-model architecture review before Stage2 execution.

Allowed review verdicts:
- PROCEED
- MODIFY
- BLOCK

Any BLOCKER/MAJOR finding that alters execution semantics requires a new contract version or explicit amendment before running 1,918-case proposer inference.
