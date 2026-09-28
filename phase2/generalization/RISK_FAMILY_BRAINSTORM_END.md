# Phase 2 — Risk-Family Audit: End Brainstorm

Date: 2026-09-29

## What changed

We now have three negative results against token-local universal safety:

1. GED residual-error detection did not isolate the wrong agreements.
2. lexical/root continuity did not isolate them.
3. surface risk family did not yield a sufficiently large zero-unsafe family.

This is not evidence that Arabic proofreading is failing as a whole. It is evidence that **candidate correctness and semantic safety are separate responsibilities**.

## Best next architecture

Use Arabic GEC for:
- candidate generation;
- edit-event representation;
- independent agreement;
- operation/risk typing.

Use the already existing ACAD_PASS verification layers for:
- protected scientific information;
- semantic drift;
- claim/role/condition/causality changes;
- review escalation.

## Important warning

Do not simply apply the old global Arabic mDeBERTa threshold and call the problem solved.

Prior ACAD_PASS evidence showed that the frozen semantic verifier can be overly sensitive to real Arabic morphology/syntax corrections and can create a very high review burden.

Therefore the next experiment should be **local-edit semantic backstop integration**, with review burden measured explicitly.

## Decision paths

If the existing semantic verifier:
- catches unsafe agreed edits while retaining a useful fraction of safe edits → integrate as backstop and validate on fresh evidence;
- flags nearly all safe edits → redesign the semantic verifier interface for local proofreading rather than adding more GEC heuristics;
- misses the known semantic/lexical wrong edits → semantic layer itself requires redesign before unattended Arabic auto-accept can advance.
