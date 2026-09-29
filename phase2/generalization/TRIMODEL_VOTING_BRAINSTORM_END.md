# Cross-Training Tri-Model Voting — Brainstorm End

Date: 2026-09-29

| Idea | Decision | Evidence |
|---|---|---|
| Promote UNANIMOUS_3 | DROP | 4 wrong + 12 partial among 142 accepted events. |
| Keep adding more GEC voters | DEPRIORITIZE | Third voter did not improve supported precision on the fresh slice. |
| Treat exact gold only as safe | DROP | Valid alternative corrections exist; fixed-reference evaluation is incomplete. |
| Re-tune vote thresholds on this slice | DROP | Would overfit the inspected population. |
| Context-sensitive residual-risk guard | TEST NEXT | All 16 unsafe cases are contextual/structural residuals. |
| Morphology only as correctness oracle | DROP | Earlier gates already falsified this. |
| Dependency/morphology/context features as veto evidence | TEST | Matches the observed failure taxonomy: valency, agreement, clitics, prepositions, numerals, tense/aspect. |
| Pure orthographic high-confidence lane | TEST AS SUBSET | Many supported cases are local orthographic normalization, but context guards are still needed. |
| Human REVIEW for context-governed edits | KEEP | Current evidence does not support unattended auto-apply for these families. |
| QALB15 TEST | KEEP SEALED | Not needed yet. |

## Next hypothesis

A narrow acceptance lane may be defensible if exact multi-model agreement is combined with independent context-sensitive vetoes. The next gate must test veto features, not another generator ensemble.