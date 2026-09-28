# Phase 2 — Lexical Continuity Diagnostic: End Brainstorm

Date: 2026-09-29

## What failed

- post-edit GED contradiction;
- no-morph-analysis;
- lexeme-disjoint;
- lexeme+root-disjoint.

These layers all rely heavily on token-local lexical/morphological plausibility. The remaining wrong edits can satisfy those plausibility checks.

## Better decomposition

Instead of a universal ACCEPT oracle, partition exact agreements into risk families:

1. orthographic/surface family;
2. inflectional family;
3. clitic/affix family;
4. lexical/derivational family;
5. agreement/case/mood family;
6. ambiguous or multi-operation family.

Then assign different evidence requirements.

## Candidate architecture

exact independent agreement
→ edit-risk family
→ family-specific veto/evidence
→ ACCEPT / REVIEW
→ scientific + semantic verification
→ source-local patch.

Examples:
- simple orthographic same-lexeme edit: may need agreement + source-validity veto;
- inflection/agreement edit: needs syntax/controller evidence;
- lexical/derivational edit: REVIEW by default under Strict Fidelity;
- scientific/protected token: reject/escalate.

## Why this is more promising

The product objective is not to maximize the number of corrections.
It is to maximize **safe automated value** while preserving the author's meaning.

Selective abstention is therefore a feature, not a failure.
