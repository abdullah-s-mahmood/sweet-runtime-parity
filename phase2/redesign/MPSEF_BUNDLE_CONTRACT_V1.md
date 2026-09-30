# MP-SEF BUNDLE CONTRACT V1

Date: 2026-09-30
Status: FROZEN BEFORE FEASIBILITY MEASUREMENT
Parent:
phase2/redesign/MPSEF_PRE_UNION_PROTOCOL_V3.md

## 1. Purpose

This contract prevents false candidate coverage caused by gold-guided or
spatial-only decomposition of proposer outputs.

Reversibility does not imply grammatical, semantic, or factual independence.

## 2. Immutable hypothesis

For every original source x0, each proposer contributes at most one final
hypothesis in the first V3 feasibility cycle:

- P1: final pass-2 output x2;
- P2: final AraBART generated output y.

KEEP is always a separate legal alternative when source integrity is valid.

P1 pass-1 output is provenance only.
No P2 n-best output exists in this cycle.

## 3. Primary executable-bundle rule

For the V3 PRIMARY action space, each final proposer hypothesis is ONE
sentence-level executable bundle.

Therefore, subject to structural/protected-span validity, the primary legal
outputs are:

- KEEP(x0);
- P1_FINAL(x0);
- P2_FINAL(x0).

P1_FINAL and P2_FINAL are mutually exclusive sentence alternatives.

The primary V3 measurement DOES NOT create hybrid sentences by selecting
individual edits from P1 and P2.

This is intentionally conservative. It avoids assuming that:
- non-overlapping edits are grammatically independent;
- edits emitted in one model hypothesis are independently optional;
- a seq2seq rewrite can be factorized safely;
- the subset of edits matching gold is itself a hypothesis proposed by the model.

## 4. Diagnostic component edits

Each final hypothesis must still be aligned from ORIGINAL x0 to final output
and decomposed into diagnostic component edits.

Each component records:
- component_id;
- hypothesis_id;
- original-source span;
- source text;
- replacement text;
- operation family;
- source-to-output alignment evidence;
- proposer-stage provenance;
- protected-span contact;
- ambiguity status;
- reversible inverse where deterministically defined.

Diagnostic components are NOT independently executable in Bundle Contract V1.

They are used only for:
- R_raw target reachability;
- operation-family diagnostics;
- conflict description;
- protected-touch accounting;
- future dependency research.

## 5. P1 provenance

Trace:
x0 -> x1 -> x2

Store:
- pass-1 edit trace;
- pass-2 edit trace;
- x2-to-x0 source anchoring;
- whether pass-2 material acts on text created or modified during pass 1.

Executable P1 bundle:
x0 -> x2 as a whole.

x1 is never an independent candidate in this cycle and cannot be added after
observing weak results.

## 6. P2 provenance

Trace:
x0 -> morph_preprocessed -> GED -> generated y

Store:
- x0;
- morphology-preprocessed text;
- GED labels;
- subword-expanded GED labels;
- final y;
- x0 -> y alignment.

Any surface effect introduced by preprocessing that survives into y remains in
the x0 -> y transaction history.

Executable P2 bundle:
x0 -> y as a whole.

GED is proposal-generation evidence, not independent verification.

## 7. Gold-blind alignment

Source-to-proposer alignment is constructed before target scoring.

Gold/reference data may not:
- split a final bundle;
- remove a wrong component while retaining a correct component;
- invent an edit absent from the proposer;
- alter source offsets;
- choose a favorable competing alignment;
- convert a diagnostic component into an executable action.

Gold is used only after the action space is frozen to score reachable outputs.

## 8. Alignment ambiguity

If deterministic source-to-output alignment has materially different valid
decompositions:
- retain all ambiguity in diagnostics;
- do not use gold to choose;
- the final proposer sentence remains a single executable bundle if the exact
  x0 -> final transformation itself is deterministic and reversible;
- otherwise mark the proposer hypothesis non-executable.

Alignment ambiguity therefore cannot increase the primary action space.

## 9. Bundle equivalence

P1_FINAL and P2_FINAL are textually equivalent if applying each to the same x0
produces the same exact final Unicode string under the frozen comparison
contract.

Equivalent final outputs count as one reachable textual output for candidate
coverage, but both proposer provenance records remain attached.

Agreement is not treated as two independent witnesses.

## 10. Protected-span interaction

A raw final proposer hypothesis may touch a protected span and remain recorded
for risk accounting.

If the frozen protected-invariants contract forbids its execution:
- the hypothesis is PROTECTED_BLOCKED;
- it does not enter the primary executable action space;
- the source case and affected reference targets remain in denominators.

No gold-based partial removal of the protected edit is permitted.

## 11. Failure states

Mandatory hypothesis states include:
- OK;
- ALIGNMENT_AMBIGUOUS;
- ALIGNMENT_FAILED;
- TRUNCATED;
- EMPTY_OUTPUT;
- SOURCE_MISMATCH;
- NONREVERSIBLE;
- PROTECTED_BLOCKED;
- EXECUTION_FAILED.

Failed or blocked cases are never removed from metric denominators.

## 12. Primary and diagnostic action spaces

### A_primary

The primary V3 action space is:
- KEEP;
- whole P1_FINAL if executable;
- whole P2_FINAL if executable.

No intra-hypothesis or cross-proposer edit fusion is allowed.

### A_diagnostic

Diagnostic component reachability may be examined without execution authority.

A_diagnostic exists only to compute R_raw and family diagnostics.

It is not a selector action space.

## 13. Consequence for metrics

Primary R_joint is optimized only over A_primary.

R_raw may examine whether complete reference targets are individually present
within diagnostic proposer components, without claiming those components can be
jointly or independently executed.

Therefore:

R_raw >= R_joint

The gap:
R_raw - R_joint

is explicitly interpreted as apparent coverage that depends on currently
unproven decomposition/fusion.

## 14. Future edit-level fusion

Edit-level fusion is not rejected permanently.

A later version may authorize smaller executable bundles only if, BEFORE
scoring, it freezes:
- a source/proposer-only dependency rule;
- deterministic decomposition;
- exact provenance;
- no-gold validation of that decomposition;
- a new action-space version;
- a new pre-registered measurement plan.

Bundle Contract V1 does not authorize that future step.

## 15. Integrity

- selector training: not authorized;
- hybrid edit-level output: not authorized;
- third proposer: not authorized;
- internal/reserved evaluation: remains closed.
