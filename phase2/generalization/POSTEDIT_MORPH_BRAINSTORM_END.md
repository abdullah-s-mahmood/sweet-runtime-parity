# Post-Edit Stability & Morphological Identity — Brainstorm End

Date: 2026-09-29

| Idea | Decision | Evidence |
|---|---|---|
| Target fixed-point as V2 gate | DROP | Captured 1/16 unsafe, 0/4 wrong. |
| +/-1 fixed-point | DROP | Same unsafe capture; slightly more false review. |
| Morph identity alone | KEEP AS AUXILIARY ONLY | Captured 4/16 unsafe, 2/4 wrong; insufficient alone. |
| Fixed-point + morphology | DROP AS PRIMARY | No better unsafe capture than morphology alone. |
| Increase fixed-point window | DROP FOR NOW | Would be post-result tuning and lacks causal justification. |
| Add more voters | DROP | Correlated consensus already falsified. |
| Dependency/governor compatibility | TEST NEXT | Directly targets valency/preposition/controller and local syntactic incompleteness. |
| Human review | KEEP | Remains required for residual uncertainty. |

## Next diagnostic

**DEPENDENCY_GOVERNOR_COMPLETENESS_V1**

Consumed evidence only first; no promotion.

The diagnostic should compare source and candidate sentence parses without reading labels and materialize only hash/category features. Candidate signals should include:
- target dependency relation;
- head relation and head POS/category;
- immediate dependent relation multiset;
- preposition/case-marker attachment around the target;
- whether the target edit changes attachment structure unexpectedly;
- whether the candidate leaves a locally anomalous governor/complement configuration detectable by parser disagreement or relation change.

Do not invent a gold-based rule. First establish parser runtime and feature stability, then freeze a small interpretable rule before reading consumed labels.
