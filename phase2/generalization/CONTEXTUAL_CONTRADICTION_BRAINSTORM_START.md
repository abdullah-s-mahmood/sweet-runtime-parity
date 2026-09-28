# Phase 2 — Contextual Contradiction Veto: Brainstorm Start

Date: 2026-09-29

## Candidate negative evidence

| Evidence | Role | Initial decision |
|---|---|---|
| Post-edit GED still flags edited token | Contradiction / residual-error evidence | TEST FIRST |
| Candidate has no contextual morphology analysis | Malformed repair evidence | TEST FIRST |
| noun_prop/backoff morphology fallback | Weak lexical-validity warning | DIAGNOSTIC ONLY |
| Dependency controller/agreement mismatch | Syntax contradiction | NEXT IF NEEDED |
| Preposition/complement frame mismatch | Lexico-syntactic contradiction | NEXT IF NEEDED |
| Masked-LM candidate rank | Contextual lexical plausibility | WATCH; never sole oracle |
| Third GEC generator agreement | Additional positive evidence | LATER |
| LLM judge | Reference-free semantic opinion | DO NOT USE AS SOLE VETO |

## Design principle

Positive evidence proposes.
Negative independent evidence can veto or escalate to REVIEW.

The system should prefer:
**high supported retention + high unsafe capture**
over artificially maximizing precision by reviewing almost everything.

A diagnostic is useful only if it catches multiple wrong/partial events while preserving most supported agreements.
