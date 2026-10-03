# ACAD_PASS WORKING PROTOCOL V1

Date: 2026-10-01
Status: ACTIVE / CROSS-CHAT WORKING AGREEMENT

This file preserves the user's working-style agreements for ACAD_PASS so that a new conversation can resume without relying on chat memory alone.

## 1. Authority and resumption order

At the start of any new ACAD_PASS conversation:

1. Read `RESUME_HERE.md`.
2. Read `ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md`.
3. Read this file.
4. Inspect the latest relevant closure locks, manifests, artifacts, workflow runs, and hashes.
5. Treat frozen repository evidence as authoritative if chat memory conflicts with it.
6. Do not restart or regenerate a completed/frozen stage unless a later frozen record explicitly authorizes it.

## 2. Execution ordering

- Tool/repository/process operations must be SEQUENTIAL ONLY.
- Never run independent operations in parallel.
- Multiple sequential operations in one response are allowed.
- For ordinary work, 2-4 meaningful sequential operations per response is a good default.
- More sequential operations are allowed when they are short and low-risk.
- For heavy/long-running operations, prefer only 1-2 major processes in the response.

## 3. Long-running process polling

When a launched process is still running:

- Inspect actual progress, not only the outer workflow state.
- Prefer watchdog/commit-status progress such as `progress=x/total`.
- Poll at most 3 times in the current response.
- Use roughly 20 seconds between checks when practical.
- If the process is still running after the third check, STOP POLLING.
- Leave the process running.
- Wait for the user to say `أكمل` before checking again.
- Do not create open-ended polling loops.

If progress is measurable:
- report current `x/total`;
- state whether actual progress is occurring or a stall is suspected;
- report remaining work as `total-x` units and, when useful, the recent observed processing rate without converting it into a promised future completion time.

If no new checkpoint occurred:
- do not repeat unchanged Stage/system completion percentages or unchanged long-term estimates.

## 4. Mandatory checkpoint reporting

After EVERY meaningful checkpoint, architecture decision, substantive `أكمل` cycle, or review that changes evidence/state, end with a compact progress report containing ALL of the following unless literally unchanged:

- classification versus the previous comparable checkpoint: `IMPROVED`, `WORSENED`, `MIXED`, or `NOT COMPARABLE`;
- what improved and what worsened/new risks appeared;
- magnitude of change in exact counts, percentages, percentage points, hashes, gates, or other comparable evidence whenever available;
- if no defensible numeric delta exists, explicitly say `NOT QUANTIFIABLE FROM COMPARABLE EVIDENCE` rather than inventing a number;
- engineering completion estimate for the CURRENT STAGE, with the denominator/basis stated (for example, closed gates / total planned gates);
- engineering completion estimate for ACAD_PASS AS A WHOLE, clearly labeled as approximate and based on the current frozen architecture;
- remaining gate/work-unit count for the current stage and for the whole system where a meaningful count exists;
- main blockers, risks, and factors that could increase or reduce the remaining work;
- realistic next-step forecast in terms of gates/work units and decision dependencies.

Do NOT provide wall-clock hours/days for future work. Use remaining gates/work units instead. For an already-running external process, report observed progress only; do not promise a future delivery time.

Do not report fake precision. Engineering completion percentages are planning estimates, not scientific/model-quality probabilities. If the architecture changes materially, revise the estimate and explain why.

## 5. Failure handling

- Preserve every meaningful failure and its evidence.
- Diagnose and classify the failure BEFORE changing the architecture or repair path.
- Distinguish implementation/runtime/provenance failures from scientific/model-quality failures.
- Prefer a separate repair batch after diagnosis unless the defect is a trivial validation/assertion mismatch.
- Never hide a failed run by silently rerunning.
- Do not silently resume partial outputs unless the frozen contract explicitly allows resume semantics.
- Maintain completed / aborted / not_attempted accounting for interruptible production runs.

## 6. Scientific integrity boundaries

- Frozen historical evidence is immutable.
- Do not weaken gates after seeing results.
- Do not regenerate frozen populations merely to improve outcomes.
- Do not use new gold/reference data unless explicitly authorized by the current frozen gate.
- Do not compute `R_joint` before explicit authorization.
- Do not train/activate a learned selector before explicit authorization.
- Do not activate family consensus before explicit authorization.
- Do not use a hidden LLM judge as a substitute for preregistered evidence.
- P1 and P3 are one SWEET family for family-support interpretation.
- Current independent P2 family is `SEQ2SEQ_GED_MORPH`.
- Follow the latest `RESUME_HERE.md` for current phase-specific scientific boundaries.

## 7. Research and architecture decisions

At the START and END of every substantive phase/iteration, and at substantive architecture gates:

- perform fresh deep research when external evidence can materially improve the decision;
- perform maximum-effort brainstorming/red-team analysis;
- explicitly challenge whether the current path should be KEEP / REPAIR / REPLACE / ADD / DEFER;
- at the end, compare the new evidence against the state at phase start and record what improved, worsened, remained unresolved, and why;
- compare KEEP / REPAIR / REPLACE / ADD / DEFER where relevant;
- do not assume an earlier architectural decision remains optimal after new evidence;
- distinguish literature evidence from project-source evidence and from engineering inference.

Higher-model consultation:
- use it only when it can materially improve an architecture/semantic gate;
- conserve limited higher-model usage;
- never claim a higher-model consultation unless it actually occurred;
- if no higher-model endpoint is available, prepare a focused low-token review prompt for the user instead of pretending a consultation happened.

## 8. Resume and ledger discipline

Update `RESUME_HERE.md` and `ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md` after meaningful checkpoints such as:

- success/failure that changes state;
- architecture decision;
- new frozen gate/contract;
- important manifest/hash/artifact identity;
- stage transition;
- new next-action sequence.

Do NOT update them for trivial status checks or unchanged polling.

`RESUME_HERE.md` is a living execution checkpoint, not a narrative history.
The ledger preserves evolution, rationale, failures, repairs, and comparative interpretation.

## 9. Communication style

- Default response language: Arabic, with English identifiers/technical terms isolated clearly.
- Keep Arabic layout RTL-friendly.
- Avoid wide Markdown tables unless specifically useful.
- Do not over-explain unchanged status.
- When the user says `أكمل`, continue from the exact frozen checkpoint using tools/evidence, not by merely describing what should happen.
- Do not ask the user to repeat information already available.
- If a required external/file artifact is genuinely unavailable and blocks correctness, request only the exact missing item.
- Do not promise background/asynchronous delivery or future work outside the current tool execution.

## 10. Protocol self-maintenance

This file is a living cross-chat working agreement.

Whenever the user and assistant establish, refine, or replace a working-style rule that may materially affect future ACAD_PASS execution, this file MUST be updated at the same meaningful checkpoint.

Examples include:
- execution ordering;
- polling cadence or limits;
- ETA/reporting rules;
- what information should or should not be repeated;
- failure-handling procedure;
- research/brainstorming gates;
- higher-model consultation rules;
- resume/ledger discipline;
- user-preferred communication behavior.

Rules:
- do not rely only on chat memory for a new persistent agreement;
- preserve superseded rules in Git history rather than silently erasing the historical record;
- the latest committed version of this file is authoritative for working-style behavior unless the user explicitly changes a rule in the current conversation;
- if the user changes a rule, apply it immediately in the current conversation and update this file at the next meaningful repository checkpoint.

## 10. Current ACAD_PASS execution philosophy

The system vision remains:

Transform → Protect → Verify → Drift → Repair/Escalate → Review → Preserve → Deliver

Prefer the strongest defensible system over preserving an old architecture.
Scientific defensibility, reproducibility, provenance, fail-closed behavior, and document fidelity take precedence over attractive but weakly-supported metrics.


## 11. Protocol maintenance and response-size control

- This file is the canonical cross-chat working-style agreement.
- Whenever the user and assistant agree on a new persistent working rule, update this file at the next meaningful checkpoint.
- Do not leave durable working agreements only in chat history.
- A new conversation should not duplicate all working rules in its opening prompt; it should instruct the assistant to read this file together with `RESUME_HERE.md` and the ledger.
- To reduce UI/runtime recovery issues, prefer shorter tool batches and shorter progress messages.
- Avoid very long chains of repository/tool operations in one response when the task can be safely checkpointed.
- Preserve the existing max-3 polling rule for long-running processes.


## 2026-10-03 amendment — English-first, delegation, and serialized execution

1. Active product R&D is English-first. Shared Core must remain language-independent; Arabic active research is frozen and preserved for a future Language Pack.
2. Human-quality academic transformation is the primary product objective. GEC is supporting Verify/Repair.
3. The higher model is a scarce strategic resource. Use it for architecture, benchmark/experiment design, difficult synthesis, red-team brainstorming, frozen-result review, and major strategic/scientific decisions. Delegate routine research collection, coding, GitHub changes, tests, experiment execution under frozen contracts, metrics, and documentation to the implementation agent.
4. After a higher-model execution packet is issued, the higher model waits for returned evidence rather than implementing routine work itself.
5. Escalate early only for architecture changes, scientific-contract changes, evaluation-population changes, safety-gate changes, protected-data boundary changes, critical evidence loss, or unexpected results that threaten inference validity.
6. Tool/process orchestration must be strictly sequential. Do not run independent tool operations in parallel. Multiple operations are allowed only when awaited in deterministic sequence. This rule is permanent for ACAD_PASS continuity and is intended to reduce recovery/stream interruption problems as well as preserve auditability.
7. Never infer human-writing quality, scientific fidelity, detector robustness, document fidelity, or commercial usefulness from engineering pass rates.
