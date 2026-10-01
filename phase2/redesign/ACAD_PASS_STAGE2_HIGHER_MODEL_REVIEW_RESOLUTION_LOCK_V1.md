# ACAD_PASS STAGE2 HIGHER-MODEL REVIEW RESOLUTION LOCK V1

Date: 2026-10-01
Reviewer verdict: MODIFY
Blockers: 0
Major findings accepted: M01, M02, M03, M04
Minor findings accepted: N01, N02
P4: UPHOLD_DEFER
P2 budget: KEEP 240 min
P3 budget: KEEP 90 min

## Resolution

All six findings are accepted as technically valid.

### M01 — ACCEPTED
Reason:
Stage1-function replay alone does not prove the production Stage2 orchestration path is identical.

Resolution:
Production-bound adapter replay is mandatory. Same adapter identity must serve replay and full-C_F execution. Existing B01 tests must traverse the production P2 adapter.

### M02 — ACCEPTED
Reason:
The current P2 Stage1 exception handler emits a minimal failure row and can discard already-established intermediate evidence.

Resolution:
Stage2 P2 uses an incremental stage ledger and preserves partial traces/evidence on failure. UNKNOWN is explicit.

No Stage1 artifact is rewritten.

### M03 — ACCEPTED
Reason:
Family provenance removal and Stage-B classifier semantics require exact preregistration to prevent post-hoc interpretation.

Resolution:
Exact family leave-one-out semantics and MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1 are frozen in Amendment A1.

### M04 — ACCEPTED
Reason:
run_with_progress_watchdog_v1.py:
- cannot compute stale duration before a progress timestamp exists;
- after SIGTERM it can wait indefinitely;
- does not guarantee process-tree kill;
- does not itself guarantee partial terminal-record preservation.

Resolution:
Stage2 requires a new watchdog version plus durable partial-record semantics. Historical watchdog remains unchanged as evidence.

### N01 — ACCEPTED
Cluster bins are presence counts and may overlap.

### N02 — ACCEPTED
Measured per-UID latency, allocated batch time and end-to-end runtime are separate metrics with frozen N/A eligibility.

## P4

Decision remains:
`DEFER BEFORE SOURCE-ONLY STAGE2`

This review found no reason to reopen the roster before source-only scaling.

## Resource budgets

P2:
- 240 minutes
- heartbeat <=60 s
- actual-progress stale threshold 600 s
- hard-kill grace 30 s

P3:
- 90 minutes
- same watchdog semantics

## Current authorization

Stage2 full-C_F execution:
`NOT YET AUTHORIZED TO RUN`

Next mandatory engineering work:
1. Stage2 production adapters;
2. watchdog V2;
3. P2 partial-evidence failure handling;
4. Stage-B classifier V1 tests;
5. Stage2 input lock;
6. production-bound replay;
7. B01 adapter replay.

After those PASS:
Stage2 full-C_F source-only execution may begin without another higher-model review unless a new blocker/major semantic change appears.
