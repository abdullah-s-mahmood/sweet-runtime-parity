# Phase 2 — Cross-Training Tri-Model Voting End Review

Date: 2026-09-29

## Decision

**WORSENED versus the prior two-model agreement on supported-precision proxy; epistemically IMPROVED.**

The primary UNANIMOUS_3 policy does **not** satisfy its pre-registered promotion contract.

## Fresh disjoint population

- Corpus: QALB-2015 L2 TRAIN.
- Fresh deterministic 50-line raw-only slice excluding the previous 50-line cross-model slice.
- Runtime votes were frozen before gold was opened.
- QALB-2015 TEST remained unread.
- QALB text was not persisted.

## UNANIMOUS_3 result after contextual review

- candidate events: 142
- exact-gold supported: 94
- non-exact events contextually reviewed: 48
- supported correction: 124 total
- supported alternative: 2
- partial correction: 12
- wrong correction: 4
- unnecessary edit: 0
- supported total: 126/142 = **88.73%**
- unsafe total under the frozen contract: 16/142 = **11.27%**

Manual review is same-agent contextual adjudication, not independent human validation.

## Comparison with prior two-model agreement

Prior two-model stream:
- supported: 144/159 = **90.57%**
- unsafe: 15/159 = **9.43%**

Tri-model UNANIMOUS_3:
- supported: 126/142 = **88.73%**
- unsafe: 16/142 = **11.27%**

Descriptive change:
- supported precision: **-1.83 percentage points**
- unsafe rate: **+1.83 percentage points**
- accepted-event count on an equal 50-line slice: 159 -> 142 (**-10.7%**), noting that the slices are different and this is not a causal coverage estimate.

Wrong-only rate improved descriptively:
- prior: 8/159 = 5.03%
- tri-model: 4/142 = 2.82%
- change: **-2.21 pp**

But partial-correction rate worsened:
- prior: 6/159 = 3.77%
- tri-model: 12/142 = 8.45%
- change: **+4.68 pp**

This is the key result: adding a differently trained third voter appears to suppress some clearly wrong edits, but it does not solve incomplete/contextually insufficient repairs.

## Promotion contract

Pre-registered requirements included zero wrong, zero partial, zero unnecessary, and at least 10 accepts.

- minimum accepts: PASS
- zero wrong: FAIL
- zero partial: FAIL
- zero unnecessary: PASS

**Decision: DO_NOT_PROMOTE_UNANIMOUS_3.**

## Failure taxonomy

The 16 unsafe events cover:
- numeral case incompleteness
- lexical number residual
- derivational-form residual
- preposition/surface residual
- determiner construction residual
- title determiner residual
- verb-valency residual
- complementizer context change
- compound numeral incompleteness
- proper-name transliteration incompleteness
- possessive-clitic loss
- preposition lexical residual
- lexical semantic change
- demonstrative-gender residual
- gender-agreement residual
- tense/aspect change

The diversity of these failures is strong evidence that a single additional voter or one global similarity score is unlikely to provide the missing safety boundary.

## Architectural conclusion

Retain multi-model agreement as **candidate evidence**, not as acceptance proof.

The next gate should test a **Contextual Residual-Risk Guard** that routes context-governed edits to REVIEW using independent morphosyntactic/fidelity evidence before any auto-accept lane is considered.

Priority veto families derived from linguistic principles and observed failures:
1. clitic/person/possessive changes;
2. verb tense/aspect/valency changes;
3. prepositions, complementizers, demonstratives and other function words;
4. numerals and case-sensitive forms;
5. proper names/transliteration;
6. noun/adjective gender-number-determiner agreement;
7. lexical/lemma changes.

A narrow pure-orthographic lane may remain viable only when these contextual risk checks do not fire.

## Forecast

Likely progress is now **selective rather than broad**. A high-precision auto-accept lane may be achievable for a subset of orthographic edits, while context-governed Arabic grammar should remain REVIEW-first.

Main blockers:
- context-sensitive morphology and syntax;
- incomplete local repairs that look superficially correct;
- correlated model errors despite training-corpus diversity;
- same-agent adjudication;
- repeated development inspection and overfitting risk.

Do not start Phase 3 and do not consume QALB15 TEST.