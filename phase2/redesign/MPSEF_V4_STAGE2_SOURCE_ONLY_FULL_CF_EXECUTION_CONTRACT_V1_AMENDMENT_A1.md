# MP-SEF V4 STAGE2 SOURCE-ONLY FULL-C_F EXECUTION CONTRACT V1 — AMENDMENT A1

Date: 2026-10-01
Status: FROZEN / MANDATORY BEFORE STAGE2 EXECUTION
Applies to: MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_EXECUTION_CONTRACT_V1.md
Reason: Higher-model adversarial review verdict MODIFY
Stage1 closure: IMMUTABLE / UNAFFECTED

This amendment governs all Stage2 execution semantics below. Where it conflicts with V1, this amendment controls.

## A1. M01 — Production-bound replay gate

The Parity32 replay gate MUST execute through the exact production Stage2 runner/adapter that will process the full 1,918-case C_F population.

It is NOT sufficient for a replay harness to import Stage1 inference functions directly while production uses a different wrapper/orchestration path.

Before full-C_F execution, freeze one production adapter identity per proposer:

- P2 Stage2 production adapter implementation SHA256;
- P3 Stage2 production adapter implementation SHA256;
- workflow SHA256;
- runtime-lock / pip-freeze SHA256;
- model/config/tokenizer identities;
- registry SHA256;
- C_F manifest SHA256;
- P1 frozen parent artifact SHA256 where applicable;
- authoritative legalizer/protection/aligner identities used after proposal generation.

The exact same adapter entry point and semantic configuration MUST be used for:

1. frozen Parity32 replay;
2. B01 synthetic boundary/failure replay where applicable;
3. full-C_F production execution.

Any code/config/dependency/model/tokenizer/registry/baseline-artifact change after replay invalidates replay and requires replay again before production.

No increase in Parity32 size is required.

### P2 required replay

Through the production adapter:
- exact frozen 32 UIDs;
- fresh vs repeat = 32/32;
- fresh vs reordered = 32/32;
- fresh vs frozen Stage1 trace/output = 32/32;
- true model batch remains N/A unless production implementation introduces a true model-call batch.

Additionally run the existing B01 synthetic/boundary/failure suite through the production P2 adapter.

### P3 required replay

Through the production adapter:
- single vs batch = 32/32;
- batch vs reversed = 32/32;
- batch vs repeat = 32/32;
- batch vs frozen Stage1 trace = 32/32;
- output vs frozen Stage1 output = 32/32;
- exact frozen P1 parent identity = 32/32.

## A2. M02 — P2 failed-row evidence preservation

P2 Stage2 rows MUST preserve partial evidence already established before a failure.

The production adapter MUST maintain a stage ledger with the following canonical stages:

1. SOURCE_IDENTITY
2. MORPH_ANALYSIS
3. GED_TOKENIZATION
4. GED_WORD_IDENTITY
5. GED_INFERENCE
6. GEC_PROJECTION
7. GEC_TOKENIZATION
8. GENERATION
9. OUTPUT_DECODE

For every row, each stage status is exactly one of:

- PASS
- FAIL
- NOT_REACHED
- UNKNOWN

Required failed-row fields:

- failure_stage;
- stage_status map;
- failure_reasons[];
- completed identity maps/hashes available before failure;
- morph words if successfully established;
- GED labels/segments/word-identity trace if successfully established;
- GEC word map/input-id hash/GED-label-id hash if successfully established;
- generation config identity;
- generated token IDs if any were returned before failure;
- generation token count when known;
- terminal EOS evidence when known;
- generation ceiling evidence when known;
- decoder-prefix/EOS evidence when known;
- model-interface/hook-call evidence when known.

Unavailable evidence MUST be represented as UNKNOWN / null with reason; it MUST NOT be fabricated, defaulted to PASS, or inferred from absence.

A failed row remains:
- in D_all;
- non-executable unless its frozen terminal semantics explicitly say otherwise;
- in the final artifact.

No exception handler may replace a partially completed evidence record with a minimal generic failure row.

## A3. M03 — Family leave-one-out semantics

For SOURCE_ONLY_LEAVE_ONE_FAMILY_OUT:

Removing family F means:

1. remove only provenance entries belonging to F;
2. for an action supported by multiple families, retain the action if any non-removed family provenance remains;
3. KEEP is always retained;
4. an exact-source proposer output is KEEP-equivalent and MUST NOT count as a non-KEEP family action;
5. provenance from the surviving family remains attached to the retained action.

Family-aware non-KEEP diagnostics operate only on legal actions whose output is literally different from source.

P1 and P3 remain one family:
`SWEET_QALB14`

P2 remains:
`SEQ2SEQ_GED_MORPH`

## A4. M03 — Frozen Stage-B change-domain classifier

Stage2 MUST use a versioned classifier:
`MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1`

Comparison:
exact P1 parent output -> P3 final output.

Categories are exactly:
- NO_CHANGE_FROM_P1
- PUNCTUATION_ONLY_FROM_P1
- BOUNDARY_ONLY_FROM_P1
- LEXICAL_ONLY_FROM_P1
- MIXED_FROM_P1
- UNAVAILABLE_COMPARISON

Classifier precedence:

1. If P1 parent or P3 final is unavailable -> UNAVAILABLE_COMPARISON.
2. If strings are exactly equal -> NO_CHANGE_FROM_P1.
3. Compute deterministic SequenceMatcher edit opcodes with autojunk=false.
4. Classify all changed characters into:
   - SPACE: Unicode whitespace;
   - PUNCT: Unicode general category beginning with P;
   - LEXICAL: every other changed character.
5. If changed classes == {PUNCT} -> PUNCTUATION_ONLY_FROM_P1.
6. If changed classes == {SPACE} -> BOUNDARY_ONLY_FROM_P1.
7. If changed classes == {LEXICAL} -> LEXICAL_ONLY_FROM_P1.
8. Any multi-class changed set -> MIXED_FROM_P1.

No normalization occurs before comparison.

Historical Stage1 counts remain historical and MUST NOT be silently reinterpreted. Stage2 reports classifier version explicitly.

Synthetic preflight examples MUST include at minimum:
- identical string -> NO_CHANGE;
- punctuation insertion only -> PUNCTUATION_ONLY;
- whitespace split/join only -> BOUNDARY_ONLY;
- Arabic letter substitution only -> LEXICAL_ONLY;
- punctuation + lexical change -> MIXED;
- missing P3 output -> UNAVAILABLE_COMPARISON.

## A5. M04 — Watchdog and termination semantics

The Stage2 watchdog MUST NOT reuse V1 stale semantics unchanged.

A new versioned watchdog is required.

At child launch initialize:

- launch_monotonic_time;
- last_actual_progress_monotonic_time = launch_monotonic_time;
- last_observed_processed = 0 or the explicitly validated initial processed count;
- independent liveness heartbeat timestamp.

Definitions:

### Liveness heartbeat

A heartbeat confirms the watchdog/child process is alive.

It MUST NOT reset the actual-progress stale timer.

### Actual progress

Actual progress means a validated monotonic increase in durable completed work, e.g.:
- processed UID terminal-record count;
- validated replay work-unit completion.

Changing only stage text, heartbeat, ETA, or log output does NOT count as actual progress.

### Stale rule

If actual durable progress does not increase for 600 seconds:

1. classify run as STALE_PENDING_TERMINATION;
2. send SIGTERM to the child process group;
3. wait at most 30 seconds;
4. if any child/process-tree member remains, send SIGKILL to the process group;
5. return non-zero.

The child MUST run in its own process group/session so descendants are terminated too.

### Partial artifact preservation

Production runners MUST persist completed terminal UID records incrementally using an append-safe or atomic checkpoint scheme.

On interruption:
- completed UIDs remain COMPLETED records;
- a UID started but lacking a terminal durable record is ABORTED;
- never-attempted UIDs are NOT_ATTEMPTED;
- partial artifact and run-state artifact are uploaded with if: always().

No interrupted run may claim COMPLETE.

### Completion gate

COMPLETE is allowed only if:

- exactly 1,918 unique C_F UIDs have terminal durable records;
- no duplicate UID;
- zero ABORTED;
- zero NOT_ATTEMPTED;
- source/registry/runtime identities validate;
- final artifact hash validation passes.

### Resume semantics

No silent resume.

A resumed run requires:
- explicit resume mode;
- frozen partial artifact identity;
- validation of completed records;
- a new run identifier linked to the prior run;
- no replacement or mutation of historical partial evidence.

If resume is not separately frozen before need arises, the default response to interruption is a fresh full rerun after triage, preserving the interrupted artifact.

## A6. N01 — Cluster histogram semantics

For every Stage2 cluster-level histogram bin:

`cluster_count(bin) = number of distinct cluster_id values containing at least one UID that qualifies for that bin`

Cluster bins MAY overlap.

Unless a particular metric is explicitly constructed as mutually exclusive, cluster-bin counts MUST NOT be summed or described as a partition of the 764 clusters.

UID histograms and cluster-presence histograms are reported separately.

## A7. N02 — Measurement eligibility and N/A rules

All burden/runtime metrics MUST state eligible-row denominator.

### Burden eligibility

Character/token/component burden requires:
- proposer terminal output available;
- output is a string;
- required source/output alignment state available for component metrics.

Missing output:
N/A, not zero.

Zero input character length:
- output/input character ratio = N/A;
- absolute character delta may still be measured if output exists.

### Runtime eligibility

Distinguish:

- MEASURED_PER_UID_LATENCY:
  independently timed UID execution.

- ALLOCATED_BATCH_TIME:
  batch wall time divided/allocated across UIDs.

- END_TO_END_RUN_TIME:
  complete workflow/runner wall time.

These fields MUST NOT be pooled into one latency distribution.

If runtime is unavailable, report N/A.

p50/p95 use the frozen nearest-rank rule and include only eligible measured values for that named metric.

## A8. Governing status

This amendment changes Stage2 execution semantics only.

Unchanged and still authoritative:
- Stage1 closure lock;
- Stage1 frozen proposer outputs;
- Stage1 parity remediation artifacts;
- V4 registry/action-set contract except where this amendment adds Stage2-specific execution semantics;
- source-only scientific boundary.

Stage2 full-C_F inference remains BLOCKED until:

1. production adapters exist;
2. versioned watchdog passes synthetic tests;
3. P2 partial-failure evidence schema passes synthetic failure injection;
4. Stage-B classifier synthetic tests pass;
5. Stage2 input lock freezes all executable identities;
6. production-bound Parity32 replay passes;
7. P2 B01 boundary/failure replay through production adapter passes.

Only then may 1,918-case P2/P3 production execution begin.
