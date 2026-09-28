# Phase 2 — Disjoint Generalization Gate: End Brainstorm

Date: 2026-09-28

## What the failure falsified

Falsified:
"one-character nun-count structural evidence is sufficient for safe auto-acceptance."

Not falsified:
- source-local edit/event architecture;
- final-alif case/agreement events;
- deterministic destructive vetoes;
- review-first handling;
- independent downstream semantic/scientific verification.

## Candidate next hypotheses

### H1 — FINAL_ALIF_EVENT_ONLY
Auto-accept only events where each changed token is a source form plus final alif, under the existing event-boundary restrictions.
Reason: this family survived the current cross-corpus evidence better than nun changes.

### H2 — NUN_CONTEXTUAL
Nun-changing events require one additional independent agreement signal before auto-accept:
- dependency/controller agreement; or
- robust morphosyntactic subject-number evidence; or
- independent generator/event agreement plus syntactic compatibility.

Until such evidence exists: REVIEW.

### H3 — COUNTERFACTUAL AGREEMENT TEST
For any future nun validator, create context perturbations that change the controller number while keeping the local verb form/error template constant. The validator should flip appropriately.

## Rejected shortcuts

- Raising GED threshold: prior evidence shows coverage loss without fixing the missing subject context.
- Lower event_cost threshold: the wrong ZAEBUC event had low cost (0.1667), so cost is not the missing variable.
- Whole-sentence LLM judge: not sufficiently reliable as sole gate and weakens interpretability.
- Tune a lexical exception for `المجتمع`: overfit and scientifically invalid.
- Use ZAEBUC TEST now: preserve it.

## Recommended next gate

**Context-Aware Structural Acceptance — QALB-2015 L2 DEV**

Pre-register before reading QALB15 DEV gold:
1. FINAL_ALIF_EVENT_ONLY candidate policy.
2. NUN family review-only baseline.
3. optional experimental NUN_CONTEXTUAL policy only if its syntactic feature is specified independently of QALB15 gold.
4. frozen runtime → then gold evaluation.
