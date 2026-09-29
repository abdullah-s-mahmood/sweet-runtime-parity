# Residual GED Target-Clean — Brainstorm End

Date: 2026-09-29

| Candidate next move | Decision | Reason |
|---|---|---|
| Spend fourth disjoint slice on GED_TARGET_CLEAN_BOTH | DROP | Retrospective population admitted 1 partial. |
| Tune GED confidence thresholds | PROHIBITED | Post-label overfitting. |
| Require ±1 or ±2 GED-clean window | DROP | Repeatedly collapsed supported retention to 58–67%. |
| Combine CATiB/dependency heuristics post hoc | DROP | Those signals already failed their own pre-registered diagnostics. |
| Add more GEC voters | DROP | Correlated incompleteness already survived three voters. |
| Keep target GED as review/ranking feature | KEEP | Improved precision and captured some partials. |
| Dedicated source-candidate correction acceptability discriminator | RESEARCH NEXT | Directly targets the unresolved sentence-level completeness problem. |
| Independent human verification | KEEP AS PRODUCT-SAFE FALLBACK | Required before production claims and appropriate if automatic proof remains unachievable. |
