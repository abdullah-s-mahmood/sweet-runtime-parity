# Phase 2 — Cross-Model Agreement Risk-Family Audit: End Review

Date: 2026-09-29

## Decision

**MIXED / NO FAMILY QUALIFIED FOR FRESH PROMOTION VALIDATION.**

The audit completed successfully on the already consumed 159-event EXACT_SINGLE_SUB_AGREEMENT population. Family assignment was frozen before prior manual labels were loaded.

## Pre-registered nomination rule

A family could advance to a fresh disjoint validation only if:
- total events >= 10;
- wrong == 0;
- partial == 0;
- unnecessary == 0.

## Results

- ALIF_MAQSURA_YA_ONLY: 35/36 supported, 1 partial, 97.22% supported precision.
- FINAL_ALIF_OTHER: 8/10 supported, 1 wrong, 1 unnecessary, 80.0%.
- HAMZA_ONLY: 79/87 supported, 6 wrong, 2 partial, including 1 HIGH wrong, 90.80%.
- MULTI_CHAR_OR_OTHER: 12/14 supported, 2 partial, 85.71%.
- NUN_ONLY: 1/1 supported, but too small.
- SINGLE_CHAR_SUBSTITUTION_OTHER: 6/6 supported, but too small.
- SUFFIX_ONE_CHAR_OTHER: 2/2 supported, but too small.
- TA_MARBUTA_HA_ONLY: 0/2 supported; 1 wrong + 1 partial.
- WAW_ALIF_ONLY: 1/1 supported, but too small.

**Candidate families for fresh validation: NONE.**

## Interpretation

Surface transformation family improves diagnosis but does not provide a sufficiently large zero-unsafe auto-accept family on this population.

The strongest large family, ALIF_MAQSURA_YA_ONLY, is promising but still contains a partial correction. Under Strict Fidelity it therefore cannot be promoted from this consumed slice.

HAMZA_ONLY is especially important: despite being superficially orthographic, it contains multiple wrong edits and one HIGH-severity wrong event. Therefore "orthographic-looking" cannot be treated as synonymous with semantic safety.

## Comparison with previous diagnostics

- exact SWEET + AraBART agreement: 144/159 supported = 90.57%.
- post-edit GED veto: wrong capture 1/8; weak.
- lexeme-disjoint veto: wrong capture 0/8; weak.
- risk-family audit: no large family satisfies the zero-unsafe nomination contract.

This sequence materially reduces the plausibility of a universal token-local acceptance oracle.

## Architecture implication

Return to the permanent ACAD_PASS architecture:

candidate generation
→ independent edit agreement
→ risk typing
→ Scientific Integrity Guard
→ independent Semantic Fidelity verification
→ ACCEPT / REVIEW / REJECT
→ selective repair
→ re-verification
→ source-local patch.

Arabic GEC should generate and rank candidate edits. It should not be forced to prove semantic equivalence by itself.

## Next question

Can the **existing independent ACAD_PASS semantic-verification stack** add useful safety to high-quality Arabic proofreading edits without sending essentially all valid morphology/syntax corrections to REVIEW?

This question must be answered using the already established verifier evidence and implementation before introducing a new parser architecture.

No Phase 3.
No QALB TEST.
No final sealed benchmark.
