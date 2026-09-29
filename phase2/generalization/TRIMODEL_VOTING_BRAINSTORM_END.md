# Tri-Model Voting — End Brainstorm

Date: 2026-09-29

| Idea | Decision | Why |
|---|---|---|
| 3/3 exact voting alone | DROP as auto-accept | 126/142 supported; 12 partial + 4 wrong. |
| 2/3 voting | DROP for promotion | Superset of known unsafe 3/3 events. |
| Add a fourth similar GEC voter | DEFER / low priority | More voters do not guarantee independence; contamination/training overlap is hard to control. |
| More NLI threshold tuning | DROP | Semantic backstop already failed operating-point criteria. |
| More GED/lexical filters | DROP as sole gate | Prior diagnostics captured too few unsafe edits. |
| Character-family whitelist | DROP as primary | Initial-hamza and hamza-only families still contain partial/wrong outcomes. |
| Post-edit fixed-point test | HIGH-PRIORITY PROTOTYPE | Direct test for incomplete repair; supported by iterative/multi-pass GEC literature. |
| Contextual morphology identity preservation | HIGH-PRIORITY PROTOTYPE | Targets clitic/person/tense/lemma drift hidden inside local edits. |
| Fixed-point + morphology conjunction | TEST | Complementary signals: completeness + identity preservation. |
| Train meta-classifier on current labels | DROP | Repeatedly inspected and too small. |
| Expand fresh disjoint evidence after diagnostic | INTEGRATE | Required before any policy freeze. |
| Human REVIEW lane | INTEGRATE | Still required for context-sensitive grammar. |

## Candidate next policies to pre-register

Diagnostic only on consumed data:

1. POST_EDIT_ALL3_STABLE — PASS only when all three frozen voters make no new edit overlapping the original target after all unanimous edits are applied to the line.
2. MORPH_IDENTITY_SAFE — PASS only when source/candidate analyses preserve lemma/POS/core features expected for an orthographic correction; REVIEW on lemma/POS/person/tense/number/gender/clitic drift or ambiguous analysis.
3. STABLE_AND_MORPH_SAFE — conjunction of 1 and 2.

The goal is not to maximize recall. The falsifiable question is whether either signal removes residual partial/wrong edits while retaining a useful supported lane.