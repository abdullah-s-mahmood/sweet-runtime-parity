# Phase 2 — Contextual Contradiction Diagnostic: End Brainstorm

Date: 2026-09-29

## What the failed diagnostic taught us

The remaining problem is not residual grammatical-error detection.

Two generators can agree on a correction, and post-edit GED can also consider the edited token acceptable, while the edit is still wrong because of:
- lexical meaning;
- derivational choice;
- complement/preposition frame;
- controller agreement;
- missing material outside the local token.

Therefore another detector trained on similar local signals is unlikely to provide the orthogonality we need.

## Priority order

### 1. Lexical continuity veto — test first
Under Strict Fidelity, an auto-applied proofreading edit should normally preserve the intended lexeme.

Measure:
- source lexical analyses;
- candidate lexical analyses;
- lemma/root overlap;
- source-valid/candidate-valid but disjoint-lemma changes;
- candidate lexical invalidity/backoff.

Use disjoint-lemma change as REVIEW evidence, not proof of error.

### 2. Parser-assisted contradiction — next
Use dependency structure to test:
- verb/controller number/gender/person;
- adjective/noun agreement where explicit;
- preposition/complement attachment;
- candidate parse instability.

Never let the parser be the sole correctness oracle.

### 3. Error-family selectivity
Do not demand one acceptance rule for all corrections.
Orthographic same-lexeme edits can eventually receive a different acceptance contract from lexical/derivational edits.

### 4. Counterfactual pairs
For every promoted family, build paired contexts where the same surface edit is correct, wrong or ambiguous.

## Avoid

- GED probability threshold sweeps;
- using the nine GED-reviewed cases to hand-code exceptions;
- word blacklists;
- a third correlated GEC vote as the only solution;
- LLM judge as sole verifier;
- QALB TEST;
- Phase 3.
