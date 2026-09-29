# Post-Edit Stability & Morphological Identity — Brainstorm Start

Date: 2026-09-29

| Idea | Decision | Reason |
|---|---|---|
| Target fixed-point across all three voters | TEST | Directly targets incomplete local repair. |
| ±1 lexical-window fixed-point | TEST | Captures nearby residual repair at the cost of more REVIEW. |
| Contextual morphology identity | TEST | Targets lemma/POS/person/tense/number/gender/clitic drift. |
| Strict equality of case/mood/state | DROP | Legitimate grammar correction can alter them. |
| Morphology alone as correctness oracle | DROP | Already falsified earlier in Phase 2. |
| Stability alone as correctness oracle | DROP | A fluent wrong edit can be a stable fixed point. |
| Stability + morphology conjunction | TEST | Complementary completeness and identity evidence. |
| Train classifier on current features/labels | DROP | Consumed and too small; leakage/overfit risk. |
| Tune window size or feature list after results | DROP | Would invalidate the diagnostic. |
| Fresh disjoint validation if promising | REQUIRED | Only path toward policy freeze. |