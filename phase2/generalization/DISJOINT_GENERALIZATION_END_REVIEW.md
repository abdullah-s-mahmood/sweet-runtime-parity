# Phase 2 — ZAEBUC Disjoint Generalization Gate: End Review

Date: 2026-09-28

## Decision

**WORSENED / MODIFY for generalization confidence.**

This is scientifically useful negative evidence: the previously perfect same-development structural rule does not generalize unchanged.

Canonical successful run:
- GitHub Actions: 36471247361
- external corpus: ZAEBUC-v1.0 Arabic DEV
- 33 DEV texts
- ZAEBUC test was not read
- runtime decisions were materialized before gold
- rules were frozen before gold

## Runtime scale

- generator edit events: 695
- gold edit events: 780

## EVENT_STRUCTURAL_TYPED

Development (Nahw/AraBART full-event audit):
- accepted 24
- supported 24
- wrong 0
- precision proxy 100%

Disjoint ZAEBUC DEV:
- accepted 6
- exact-gold supported 5
- contextual manual wrong 1
- supported accepted: 5/6 = 83.33%
- observed wrong accepted: 1/6 = 16.67%

Magnitude:
- precision proxy change: **-16.67 percentage points**
- zero-wrong criterion: FAILED

## EVENT_STRUCTURAL_STRICT

Development:
- accepted 23
- supported 23
- wrong 0
- precision proxy 100%

Disjoint ZAEBUC DEV:
- accepted 3
- exact-gold supported 2
- contextual manual wrong 1
- supported accepted: 2/3 = 66.67%

Magnitude:
- precision proxy change: **-33.33 percentage points**
- zero-wrong criterion: FAILED

Therefore STRICT was not safer on this external slice. Its cost/multiword restrictions did not address the actual missing evidence: syntactic/subject-number context.

## Counterexample

Source context:
`من المهم من المجتمع أن ينشرون الأدلة أو المخاطر ...`

Candidate:
`ينشرون → ينشروا`

Gold:
`ينشرون → ينشر`

Judgment:
WRONG_CORRECTION / MEDIUM

Failure:
**SUBJECT_NUMBER_AGREEMENT_CONTEXT_FAILURE**

Why this matters:
The candidate looks like a plausible five-verbs nun-drop transformation in isolation, but the intended controller/subject is singular `المجتمع`. Character-shape evidence cannot prove agreement.

## Positive generalization evidence

The gate did not collapse completely.

EVENT_STRUCTURAL_TYPED had five exact-gold supported events, including:
- a 3-token coordinated accusative event: `تطور كبير وعميق → تطورا كبيرا وعميقا`
- `عرب → عربا`
- `نفسي → نفسيا`
- `ع → عن`
- `سنن → سنا`

The first three strongly support the hypothesis that bounded final-alif/case realizations generalize better than context-free nun transformations.

However, this gate must not be retuned on ZAEBUC DEV after seeing gold. Any revised policy requires a different untouched development corpus.

## Research interpretation

Recent GEC research on context robustness is directly relevant: subtle context changes can alter correction validity even when a local surface error pattern appears similar. Edit-level voting/evaluation improves granularity, but edit-local evidence does not eliminate the need for syntactic context.

The project therefore learned:
- edit-event representation is necessary but not sufficient;
- narrow surface shape is not always a correctness proof;
- "stricter" thresholds do not substitute for the missing linguistic variable;
- subject/number/governor evidence is required for nun-family auto-acceptance.

## Frozen post-gate decision

Do NOT tune EVENT_STRUCTURAL_TYPED on ZAEBUC DEV.

For the next hypothesis:
- move nun-insertion/deletion/replacement family to REVIEW unless independent syntactic/agreement evidence is available;
- preserve final-alif case/agreement events as a separate candidate family;
- test that revised hypothesis on another untouched development corpus (recommended: QALB-2015 L2 DEV);
- keep ZAEBUC TEST untouched.

No Phase 3.
No final sealed benchmark yet.
