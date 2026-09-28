# Phase 2 — ZAEBUC Disjoint Generalization Interim Decision

Date: 2026-09-28

## Decision

**MIXED / materially worse than same-data development precision.**

The full-event architecture remains useful, but the generic structural auto-accept rule does **not** generalize safely as currently defined.

### ZAEBUC DEV

Frozen runtime decisions were materialized before gold.

EVENT_STRUCTURAL_TYPED:
- accepted: 6
- exact gold supported: 5
- contextual wrong after bounded review: 1
- observed supported precision after review: 5/6 = 83.33%

EVENT_STRUCTURAL_STRICT:
- accepted: 3
- exact gold supported: 2
- contextual wrong after bounded review: 1
- observed supported precision after review: 2/3 = 66.67%

Failure:
"ينشرون → ينشروا" was accepted from its one-nun-deletion surface shape, but the source subject is singular ("المجتمع"). The gold correction is "ينشر", not plural "ينشروا".

This falsifies the assumption that one-nun insertion/deletion is safe from local surface structure alone.

## Immediate architecture change

- NUN_INSERT / NUN_DELETE: **REVIEW_ONLY** until explicit syntactic subject/mood evidence exists.
- Generic FINAL_ALIF_ADD: not yet promotable. It conflates:
  1. accusative/tanwin alif, which is syntactically context-sensitive;
  2. differentiating alif after plural waw, which is primarily orthographic.

The second family deserves a separate fresh disjoint validation.

## Why this is progress despite worse precision

The gate did its job: it falsified a rule that looked perfect on the repeatedly inspected Nahw development set before it could be promoted.

The project is epistemically improved, while the candidate auto-accept policy itself is worsened/invalidated.

Do not tune thresholds to recover the failed nun rule.
