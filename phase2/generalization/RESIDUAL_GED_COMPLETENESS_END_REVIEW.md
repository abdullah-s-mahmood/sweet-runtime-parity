# Residual GED Completeness — Direct-Text Diagnostic End Review

Date: 2026-09-29

Canonical successful run: 36530908345

## Result

GED_TARGET_CLEAN_BOTH:
- PASS: 12/14
- REVIEW: 2/14
- supported PASS: 12/12
- partial PASS: 0/2
- supported retention: 100%
- partial capture: 100%
- review burden: 14.29%
- status: PROMISING_FOR_PREPROCESSING_FAITHFUL_REPLICATION

GED_WINDOW1_CLEAN_BOTH and GED_WINDOW2_CLEAN_BOTH:
- PASS: 8/14
- supported PASS: 8
- partial PASS: 0
- supported retention: 66.67%
- review burden: 42.86%
- status: NOT_PROMISING

## Interpretation

This is a strong diagnostic separation on a very small consumed population, but it is not yet reliable evidence because the GED models were evaluated on direct candidate text while their published setup used contextual morphological preprocessing.

Decision: proceed only to preprocessing-faithful replication of the frozen target-clean rule and its already-frozen ablations. No fresh fourth slice yet.
