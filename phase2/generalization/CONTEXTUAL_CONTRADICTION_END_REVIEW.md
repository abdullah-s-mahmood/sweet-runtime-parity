# Phase 2 — Contextual Contradiction Diagnostic: End Review

Date: 2026-09-29

## Decision

**WORSENED / WEAK_OR_UNHELPFUL as a contradiction veto.**

The diagnostic ran successfully on the already consumed 159-event EXACT_SINGLE_SUB_AGREEMENT stream.

This is not an independent generalization estimate. Runtime contradiction features were materialized before prior manual labels were loaded.

## Pre-registered interpretation thresholds

PROMISING_SIGNAL required:
- wrong capture >= 50% (at least 4/8), and
- supported retention >= 90%.

STRONG_SIGNAL required:
- wrong capture >= 75% (at least 6/8), and
- supported retention >= 90%.

## GED_CONTRADICTION

- REVIEW: 9
- KEEP_ACCEPT: 150
- supported retained: 136/144 = 94.44%
- wrong captured: 1/8 = 12.5%
- total unsafe captured: 1/15 = 6.67%
- wrong remaining in KEEP_ACCEPT: 7
- partial remaining: 6
- unnecessary remaining: 1
- residual KEEP_ACCEPT supported precision: 136/150 = 90.67%

Decision:
**WEAK_OR_UNHELPFUL**.

It preserves enough supported edits but fails badly on the primary purpose: detecting wrong agreements.

## GED_OR_NO_MORPH

Results are identical:
- supported retention: 94.44%
- wrong capture: 12.5%
- unsafe capture: 6.67%
- residual precision: 90.67%

The no-contextual-morph-analysis condition added no useful separation on this population.

## Interpretation

Post-edit GED is strongly correlated with the same local correction behavior already represented in the generator stack. It is not sufficiently orthogonal to detect the semantic/lexical/contextual failure families exposed by cross-model agreement.

The failures that remain include:
- lexical selection;
- semantic verb drift;
- derivational form;
- preposition/complement choice;
- gender/agreement;
- incomplete malformed-word repair.

Several of these can produce a locally fluent and morphologically analyzable token, so residual-error detection alone is structurally incapable of catching them reliably.

## Comparison with previous stage

Cross-model agreement before this veto:
- 144/159 supported = 90.57%
- 8 wrong, 6 partial, 1 unnecessary.

After GED_CONTRADICTION:
- 136/150 supported = 90.67%
- 7 wrong, 6 partial, 1 unnecessary.

Precision improvement:
**+0.10 percentage points**.

Cost:
- 8 supported edits sent to REVIEW;
- only 1 wrong edit removed.

This is not a useful trade-off.

## Research interpretation

Recent GEC robustness evidence shows that contextual changes can flip correction validity, so a token-local residual detector is not expected to solve context-dependent failures.

Arabic edit-level ensembles remain useful as positive evidence, but the project now needs an orthogonal verifier that explicitly represents lexical identity and syntactic context.

CamelParser2.0 and the newer CAMeL dependency-parser ecosystem provide dependency, POS and rich morphology suitable for a veto layer, but parser output must remain evidence rather than an oracle.

## Frozen status after this diagnostic

- exact SWEET + AraBART agreement: STRONG_POSITIVE_EVIDENCE / not auto-accept proof
- post-edit GED contradiction: DROP as promotion veto; may remain diagnostic metadata
- no-morph-analysis veto: DROP as promotion veto
- noun_prop/backoff: diagnostic only
- NUN surface rules: REVIEW_ONLY
- generic final-alif rules: REVIEW_ONLY
- WAW_ALIF morphology recovery: REVIEW_ONLY
- no Phase 3
- no final sealed benchmark

## Next technical direction

**Phase 2 — Lexical + Syntactic Contradiction Diagnostic**

First test generic Strict-Fidelity negative evidence:
1. candidate/source lexical-analysis continuity;
2. lemma/root/derivational change risk;
3. preposition/content-word change family;
4. dependency-based controller/agreement contradictions;
5. candidate/source parse stability.

Use these only to veto/escalate exact-agreement edits.

Do not train or tune a learned classifier on the current 159 events.
Any promising generic veto must be frozen and evaluated on a fresh disjoint population before promotion.
