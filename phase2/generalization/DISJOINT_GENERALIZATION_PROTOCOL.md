# Phase 2 — Disjoint Generalization Gate Protocol

Date: 2026-09-28
Status: PRE-REGISTERED BEFORE READING ZAEBUC DEV GOLD CONTENT

## Purpose

Test whether the frozen Arabic AraBART edit-event acceptance rules generalize beyond the repeatedly inspected Nahw passages.

This is still Phase 2. It is NOT the final sealed benchmark and does not authorize Phase 3.

## Why Nahw cannot supply this gate

Current Nahw development uses 41 passage IDs.
SEALED_EXCLUSION_AUDIT reserves 59 other passage IDs.
41 + 59 = all 100 Nahw passages.

Therefore no unused Nahw passage exists for a disjoint generalization slice without touching previously reserved/sealed identifiers.

## External corpus

Source repository:
CAMeL-Lab/arabic-gec

Pinned upstream branch/commit will be recorded by the workflow.

Corpus:
ZAEBUC-v1.0 Arabic GEC

License:
CC BY-NC-SA 4.0 (from data/gec/ZAEBUC-v1.0/LICENCE.txt)

Selected split:
**Arabic DEV only**

Use:
- data/gec/ZAEBUC-v1.0/data/ar/dev/dev.sent.raw
- gold only after decisions are frozen:
  - dev.sent.cor and/or data/m2edits/zaebuc/zaebuc_dev.m2

Do NOT read/use ZAEBUC test in this gate.

## Model under test

Keep the existing independent second-generator stack frozen:
- GED: CAMeL-Lab/camelbert-msa-qalb14-ged-13
- GEC: CAMeL-Lab/arabart-qalb14-gec-ged-13
- same pinned runtime strategy already used by the Independent Candidate Acceptance Gate.

Rationale:
the QALB14-specific generator evaluated on ZAEBUC gives cross-corpus / learner-domain generalization evidence.

No fine-tuning on ZAEBUC.

## Frozen runtime acceptance rules

Do not alter these using ZAEBUC gold.

### EVENT_STRUCTURAL_TYPED
ACCEPT only complete edit events where:
- source and output token counts align;
- primitive operations are substitution-only;
- each aligned token pair is one of:
  - exactly one nun inserted,
  - exactly one nun deleted,
  - exactly one final alif appended;
- event_cost <= 0.60;
- no narrow ta-marbuta->ha or alif-maqsura->ya destructive veto.

### EVENT_STRUCTURAL_STRICT
- single-token structural event requires event_cost <= 0.25;
- multiword event must be <=2 tokens and every token must be final-alif addition;
- same destructive veto.

All hamza, lexical, speech-act, tense/person, split/merge, INS/DEL events remain REVIEW in this gate.

## Anti-leakage ordering

1. Fetch raw DEV input.
2. Run the frozen QALB14 generator.
3. Align raw -> generator output into complete edit events.
4. Materialize frozen runtime decisions.
5. Persist hashes/decisions.
6. Only then read ZAEBUC DEV gold.
7. Evaluate accepted events.
8. No threshold/rule tuning after seeing results in this gate.

## Primary metrics

For each frozen policy:
- accepted event count;
- exact-gold-supported accepted events;
- accepted events conflicting with gold;
- unmatched-to-gold accepted events -> REVIEW_REQUIRED_FOR_ALTERNATIVE (not automatically wrong);
- gold-edit recovery among structural families;
- sentence/essay cluster distribution;
- accepted event family breakdown.

## Critical safety criterion

The gate FAILS / MODIFY if an accepted event is demonstrably wrong relative to source+gold, especially HIGH/CRITICAL drift.

Unmatched accepted alternatives must not be automatically counted as correct or wrong without adjudication.

## Data handling

Do not commit the full external corpus into our repository.
Persist only:
- upstream identifiers/hashes;
- compact derived event evidence where license permits;
- aggregate results;
- small necessary excerpts for counterexamples.

Do not create or consume a final sealed benchmark here.
