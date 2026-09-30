# ACAD_PASS LONG-PROCESS MONITORING CONTRACT V1

Date: 2026-09-30
Status: ACTIVE / MANDATORY FOR NEW LONG-RUNNING PROCESSES

## Purpose

Every new long-running or computationally expensive process must expose both:

1. **progress state** — how much work has completed;
2. **independent liveness/stall observation** — whether the process is still alive and whether actual progress is still changing.

A workflow-level `in_progress` state alone is not sufficient.

## Required components

### Progress state helper

`phase2/redesign/process_progress_v1.py`

Each long process must periodically update a JSON state file containing:

- process_id
- status
- stage
- processed
- total
- percent
- started_at
- heartbeat_at
- last_progress_at
- rate_per_min
- eta_seconds
- message

The state file is written atomically.

### Independent watchdog

`phase2/redesign/run_with_progress_watchdog_v1.py`

The watchdog must launch the child process and independently monitor the state file.

It records:

- whether the child PID is still alive;
- the latest processed/total percentage;
- time since last real progress;
- current stage;
- return code.

On GitHub Actions it should publish a commit status context at intervals using the workflow `GITHUB_TOKEN`.

The published description should distinguish:

- alive + progressing;
- alive but stale;
- completed;
- failed.

## Default cadence

Recommended defaults:

- child progress update: every batch or at least every 30–60 seconds;
- watchdog poll: every 20 seconds;
- externally published status: every 60 seconds;
- default stale threshold: 600 seconds unless a process-specific threshold is justified.

## Stall semantics

A process is NOT considered stalled merely because it is slow.

A process becomes suspicious/stale when:

- child PID remains alive; AND
- processed count does not increase for longer than the frozen stale threshold.

A process is failed when:

- child exits non-zero; OR
- workflow/runtime reports a hard failure.

The watchdog must not automatically kill a stale process unless `--kill-on-stale` was explicitly frozen for that process before execution.

## Percentage semantics

The numerator and denominator must be defined before execution.

Examples:

- dataset cases processed / total cases;
- batches completed / total batches;
- files processed / total files;
- experiments completed / total experiments.

Do not invent a misleading percentage for an operation whose total work is unknown.

## GitHub observability

New long-running workflows should grant only the extra permission required for live status publication:

`statuses: write`

No broader write permission should be added solely for monitoring.

The status context name must identify the process, for example:

`acad-pass/mpsef-p2-cf`

This enables live inspection through the commit-status API even when GitHub job log blobs are not yet available.

## Scientific integrity

Monitoring code must never:

- read gold/reference content merely to calculate progress;
- change model output;
- change selection/order based on intermediate quality;
- modify frozen gates;
- trigger post-result tuning.

Monitoring is operational instrumentation only.

## Applicability

This contract applies to all new long-running ACAD_PASS workflows from this checkpoint onward.

Existing completed artifacts do not need to be rerun solely to add monitoring.

If an existing active run was started without this instrumentation, do not inject code into it mid-process; either let it finish or restart only if there is independent evidence of failure/stall.
