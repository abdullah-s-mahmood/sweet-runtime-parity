# ACAD_PASS — PERMANENT BOOTSTRAP / CROSS-CHAT CONTRACT

Version: 1
Date established: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

## Purpose

The user uses one reusable new-chat bootstrap prompt.

THE USER MUST NOT NEED TO EDIT THAT PROMPT AFTER EVERY CHECKPOINT.

Project continuity is the repository's responsibility, not the reusable prompt's responsibility.

## Permanent rule

A new conversation MUST recover the actual current ACAD_PASS state from durable GitHub evidence.

Never treat:
- the reusable prompt's historical anchor;
- ChatGPT memory;
- an old pasted checkpoint;
- a branch name remembered from a prior chat

as automatically current.

## Required recovery order

1. Discover the actual active ACAD_PASS branch from recent coherent ACAD_PASS commit lineage.
2. Read:
   - `ACAD_PASS_CHAT_HANDOFF.md`
   - `ACAD_PASS_MASTER_CONTINUITY.md`
   - latest end of `RESUME_HERE.md`
3. Immediately read:
   - `ACAD_PASS_LATEST_STATE.md`
   - `ACAD_PASS_LIVE_PROGRESS.md`
4. Follow every authoritative checkpoint/freeze/review/manifest referenced from `ACAD_PASS_LATEST_STATE.md`.
5. Search the active branch for evidence newer than those pointers before mutating or rerunning anything.
6. Resolve conflicts using immutable-result / completed-run / protocol-closure / latest-snapshot / continuity authority order.
7. Continue the single exact next authorized sequential operation.

## Repository update obligation

After EVERY material checkpoint, the working conversation MUST update:

Mandatory:
- `ACAD_PASS_LATEST_STATE.md`
- `ACAD_PASS_CHAT_HANDOFF.md`
- `ACAD_PASS_LIVE_PROGRESS.md`

When materially appropriate:
- `ACAD_PASS_MASTER_CONTINUITY.md`
- `RESUME_HERE.md`

The update must include:
- active branch;
- current HEAD or checkpoint commit;
- latest authoritative freeze/review/result;
- latest run/artifact IDs and digests;
- what passed;
- what failed;
- consumed attempts/resources;
- protected/forbidden resources;
- current process readiness;
- latest actual scientific performance;
- exact next authorized operation.

## Pointer semantics

`ACAD_PASS_LATEST_STATE.md` is a small navigation pointer, not the scientific authority itself.

If it conflicts with:
1. immutable result/freeze artifacts;
2. completed GitHub Actions artifacts;
3. later protocol/closure records;

then the stronger durable evidence wins and the pointer must be repaired.

## Reusable prompt invariance

The user's existing reusable ACAD_PASS bootstrap prompt is intentionally stable.

DO NOT require the user to:
- paste a newer branch name;
- edit checkpoint percentages;
- insert new run IDs;
- replace the bootstrap anchor;
- maintain a different prompt for every new conversation.

All moving state belongs in GitHub durable files.

If a new chat is started with the reusable prompt, the correct behavior is:
`DISCOVER -> VERIFY -> READ LATEST POINTER -> SEARCH NEWER EVIDENCE -> CONTINUE`.

## Failure resilience

UI or conversation interruption never implies GitHub scientific failure.

On recovery:
- inspect durable GitHub run state;
- do not automatically rerun;
- preserve failed/partial evidence;
- continue only from the exact authorized boundary.

## Scientific execution rule

All ACAD_PASS operations remain strictly sequential.

No scientifically or technically dependent operation may execute concurrently.

No scientific fit starts merely because implementation is technically possible.

## Current bootstrap invariant

This contract itself is permanent and should not need version changes merely because ACAD_PASS advances.

Only change it if the continuity architecture itself changes.
