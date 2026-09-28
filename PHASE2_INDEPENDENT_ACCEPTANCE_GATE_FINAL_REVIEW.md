# Phase 2 — Independent Candidate Acceptance / Reverse Acceptance Gate Review

Date: 2026-09-28

## Decision

**IMPROVED — development evidence only.**

This is not a production or sealed validation claim.

## What improved

### Existing candidate population (79 rows)

The clean rerun of the independent acceptance gate completed successfully.

Best conservative existing-candidate policy:

- EXACT_LOCAL_AGREEMENT
- accepted: 23
- supported: 23
- wrong: 0
- partial: 0
- development supported precision: 100%
- supported coverage within the existing 79-row candidate population: 37.10%

AGREEMENT_PLUS_GED also achieved 22/22 supported but accepted one fewer correction, so GED did not improve precision in this development population.

### New AraBART-only population (67 additional local substitutions)

Raw AraBART-only quality is unsafe for automatic application:

- supported correction: 27
- supported alternative: 2
- partial: 2
- unnecessary: 2
- wrong: 33
- alignment uncertain: 1
- supported/alternative: 29/67 = 43.28%

The target-agnostic STRUCTURAL_TYPED reverse gate improved this stream to:

- accepted: 6
- supported: 6
- wrong: 0
- partial: 0
- high/critical wrong: 0
- development supported precision: 100%
- supported coverage within the AraBART-only supported subset: 20.69%

Accepted IDs:
- AB-5-14
- AB-17-31
- AB-25-48
- AB-28-10
- AB-92-15
- AB-94-32

These are incremental local locations outside the previous 79-row candidate population.

### Combined development evidence

Because the two local candidate populations are disjoint at the recorded local locations:

- previous clean exact-local accepted supported edits: 23
- additional reverse-gate accepted supported edits: 6
- combined development accepted supported edits: 29
- combined accepted wrong edits observed: 0

Relative to the previous 23-edit conservative path, this is +6 supported accepted edits, or +26.1% in absolute accepted useful edits.

Relative to the earlier canonical STRICT_CONSENSUS result of 20 supported accepts, the current evidence path reaches 29 supported accepts, +9 or +45%, while still observing zero accepted wrong edits in development.

Do not interpret these percentages as production accuracy. The population is repeatedly inspected development evidence and clustered by passage.

## Hard-veto refinement

The first reverse-gate implementation broadly classified any internal hamza loss as REJECT. That incorrectly rejected two linguistically acceptable but non-minimal lexical alternatives:

- فأصغي → فاستمع
- ينأَ → يغفل

They should never be auto-applied under Strict Fidelity, but REVIEW is more appropriate than REJECT.

The veto was refined to fire only on pure hamza-seat degradation when the lexical form is otherwise unchanged.

After refinement:

- hard-veto rows: 25
- hard-veto wrong: 24
- hard-veto supported: 0
- no auto-accept decision changed
- STRUCTURAL_TYPED remains 6/6 supported

This is a qualitative triage improvement.

## GED finding

For the AraBART-only structural policy:

- STRUCTURAL_TYPED: 6 accepted, 6 supported
- STRUCTURAL_TYPED_PLUS_GED50: 3 accepted, 3 supported

GED preserved observed precision but cut accepted useful coverage by 50% (6 → 3). Therefore GED remains a soft diagnostic feature and should not be a mandatory gate for this typed structural branch.

## Full AraBART event audit

106 complete AraBART edit events were adjudicated:

- supported correction: 57
- supported alternative: 5
- partial: 7
- unnecessary: 2
- wrong: 35
- supported/alternative: 62/106 = 58.49%

Target-overlap events:
- 46/56 supported/alternative = 82.14%

Non-target events:
- 16/50 supported/alternative = 32.0%
- 31/50 wrong = 62.0%

The runtime system cannot use target overlap as a feature.

The audit also proved that complete edit-event representation is necessary. Multiword events can be valid even when isolated word substitutions appear unsafe, and vice versa.

## Research update

Fresh 2025–2026 evidence remains aligned with the architecture:

- BEA 2026 shows edit-level majority voting can reduce GEC over-correction.
- CLEME2.0 emphasizes separating hit-correction, wrong-correction, under-correction and over-correction.
- ACL 2026 robust multilingual evaluation shows fixed references can underestimate valid alternative corrections; closest-gold/reference diversification is useful for evaluation.
- EMNLP 2025 demonstrates that reference-free and LLM-based GEC metrics can be adversarially unreliable, so they should not become the sole acceptance oracle.

## Current architecture decision

Keep:

SWEET surgical + normalized fallback + AraBART local events
→ alignment/event-quality gate
→ typed candidate evidence
→ independent agreement where available
→ deterministic Arabic validators
→ ACCEPT / REVIEW / REJECT
→ morphology realization
→ scientific integrity locks
→ semantic/fidelity verification
→ exact source-local patch

Do not:
- use full AraBART output directly;
- use GED as a mandatory hard gate;
- auto-accept lexical rewrites;
- use a reference-free/LLM judge as the sole verifier;
- train a learned verifier on this small repeatedly inspected development population;
- create the sealed benchmark yet;
- start Phase 3 yet.

## Next gate

**Phase 2 — Full Edit-Event Acceptance Prototype**

Goal: extend runtime acceptance from one-word local substitutions to complete edit events, especially the 10 COMPLEX events, without using Nahw target positions or human labels at runtime.

Pre-registered priorities:
1. event-boundary/alignment quality;
2. typed case/agreement/mood evidence;
3. lexical-minimality and speech-act veto/review;
4. source-mark preservation;
5. independent generator agreement where available;
6. abstention for unresolved complex events.

Success should mean:
- zero accepted known HIGH/CRITICAL wrong events in development;
- no accepted partial events;
- incremental supported coverage beyond the current 29 accepted useful local edits;
- no reduction in source/scientific safety;
- no use of target or adjudication labels at runtime.

## Forecast

Most likely next improvement will come from typed grammatical event validators and event-level consensus, not from a larger generative model or stricter GED threshold.

Main blockers:
- complex multiword alignment;
- Arabic case/mood realization;
- lexical alternatives that are grammatical but violate minimality;
- small/repeatedly inspected development evidence;
- lack of independent human validation and disjoint sealed evidence.

The current evidence suggests the architecture is progressing in the right direction, but the next meaningful confidence jump requires generalization evidence rather than another round of same-data precision tuning.
