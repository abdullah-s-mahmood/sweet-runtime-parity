# ORTHO_ISOLATED Fresh Validation — Brainstorm End

Date: 2026-09-29

## Observed failure

V1 admitted two partial corrections despite:
- exact 3/3 model agreement;
- protected-risk vetoes;
- noun-to-noun contextual morphology;
- lemma identity;
- selected morphology identity;
- clitic identity;
- no other proposed edit within +/-2 lexical tokens.

The missing property is **repair completeness in sentence context**.

## Candidate next hypotheses

| Hypothesis | Decision | Reason |
|---|---|---|
| Increase voter count | DROP | Correlated agreement already failed as correctness proof. |
| Relax/tune V1 morphology for coverage | PROHIBITED | Would tune on consumed gold and move in the wrong safety direction. |
| Expand isolation radius | DIAGNOSTIC ONLY | May catch some residual repairs but is heuristic and can over-reject. |
| Post-edit fixed-point stability | TEST | A locally plausible partial repair may trigger further edits after application. |
| Dependency/governor compatibility | TEST | Directly targets preposition/valency and syntactic-governor residuals. |
| Sentence-level semantic/NLI gate | DEFER | Prior evidence showed weak fit as a sole local acceptance oracle. |
| Human review for residuals | KEEP | Remains first-class and mandatory for uncertain cases. |

## Recommended next gate

**CONTEXTUAL_REPAIR_COMPLETENESS_V2 diagnostic**, first on consumed evidence only.

Candidate evidence components:
1. V1 must already PASS.
2. Apply the candidate in sentence context.
3. Re-run frozen correction voters and test local fixed-point stability.
4. Add dependency/governor evidence for the target and immediate syntactic head/dependent relation.
5. Reject auto-accept if the candidate leaves a target-adjacent syntactic repair signal or changes governing relation incompatibly.
6. Materialize all diagnostic evidence before consulting consumed labels.

No promotion from the consumed population.

Only if the diagnostic captures both known partials while retaining a useful supported subset should a byte-frozen V2 be pre-registered and evaluated on a **fourth disjoint untouched QALB15 TRAIN slice**.

QALB15 TEST remains unread. No sealed benchmark. No Phase 3.
