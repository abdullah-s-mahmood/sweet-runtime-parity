# Cross-Training Tri-Model Voting — Brainstorm Start

Date: 2026-09-29

| Idea | Decision | Reason |
|---|---|---|
| 3/3 exact edit unanimity | TEST PRIMARY | Strongest architecture+training evidence available without QALB15 leakage. |
| AraBART + either SWEET | TEST SECONDARY | Preserves cross-architecture evidence and may improve coverage. |
| Two SWEET agreement | DIAGNOSTIC | Same architecture family; correlated failure risk. |
| AraBART-ZAEBUC vote | DROP FOR QALB15 | QALB15 appears in training data; contaminated evaluation. |
| mDeBERTa NLI gate | DROP AS PRIMARY | Diagnostic failed preregistered thresholds. |
| More NLI threshold tuning | DROP | Consumed-slice overfitting. |
| Meta-classifier over previous labels | DROP | Small/repeatedly inspected evidence. |
| Fresh raw slice before gold | REQUIRED | Generalization and anti-leakage. |

## Expected outcomes

- If 3/3 is clean with usable coverage, it becomes a candidate for later broader validation.
- If 3/3 still contains unsafe edits, model agreement is too correlated to support unattended Arabic auto-apply at this stage.
- If 3/3 is clean but very sparse, preserve it as a narrow auto-accept lane and route the rest to review.