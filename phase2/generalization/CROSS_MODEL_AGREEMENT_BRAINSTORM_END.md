# Phase 2 — Cross-Model Agreement End Brainstorm

Date: 2026-09-29

## Core lesson

Independent agreement is **high-value evidence but not proof**.

Two different systems can share:
- training/corpus biases;
- common orthographic priors;
- the same local-context blind spot;
- the same plausible-but-wrong lexical repair.

The next improvement should therefore be **orthogonal negative evidence**, not a third generator that simply votes with the first two.

## Highest-value next hypotheses

### 1. Contextual contradiction veto — PRIORITY 1
Try to detect when an agreed edit conflicts with:
- grammatical controller/subject;
- complement/preposition frame;
- source lexical validity;
- derivational family;
- local semantic role.

Use it only to veto or review.

### 2. Error-family selective promotion — PRIORITY 2
The agreement stream should be partitioned by edit family.
Orthographic hamza/alif/ya fixes may have different risk from lexical or case/mood edits.
Do not report one aggregate precision as if all edit families are equally safe.

### 3. Counterfactual falsification — PRIORITY 3
For each accepted family, construct paired contexts where the same token-level edit becomes:
- correct;
- wrong;
- ambiguous.
A safe verifier should abstain when context changes the answer.

### 4. Third-model evidence — LATER
A third independent generator may improve consensus, but only after measuring correlation of failure modes. Three correlated systems can still make the same error.

## Avoid

- another same-data threshold sweep;
- word-specific blacklists;
- treating gold mismatch automatically as wrong;
- treating exact agreement automatically as correct;
- reference-free LLM scoring as the sole judge;
- Phase 3 before a disjoint veto test.
