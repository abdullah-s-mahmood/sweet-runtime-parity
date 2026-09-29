# Contextual Residual-Risk Guard — Brainstorm End

Date: 2026-09-29

| Idea | Decision | Evidence |
|---|---|---|
| ORTHO_ISOLATED_COMMON_NOUN_V1 | FREEZE FOR FRESH VALIDATION | 19/19 supported, 0 unsafe on consumed diagnostic. |
| ORTHO_MORPH_COMMON_NOUN_V1 without isolation | DROP | 34/36 supported; 2 partials passed. |
| ORTHO_ISOLATED_NOUN_ADV_V1 | DO NOT SEPARATELY ADVANCE | Same 19 events as primary; no incremental coverage. |
| Relax neighborhood isolation | DROP | Isolation removed both observed partials at cost of coverage. |
| Add lexical exception lists | DROP | Would overfit inspected cases. |
| Tune morph feature set | DROP FOR V1 | Freeze exact current implementation before disjoint validation. |
| Add CamelParser2.0 now | DEFER | First test whether current narrow lane generalizes unchanged. |
| Consume QALB15 TEST | PROHIBITED | Fresh TRAIN slice remains available. |

Next falsification question: does the exact frozen primary lane retain zero unsafe edits on a third disjoint QALB15 TRAIN slice?