# Phase 2 — FINAL_ALIF Generalization Validation Protocol

Date: 2026-09-28
Status: PRE-REGISTERED BEFORE READING ZAEBUC TRAIN GOLD CONTENT

## Trigger

ZAEBUC DEV falsified context-free auto-acceptance of nun-changing structural edits:
`ينشرون -> ينشروا` was structurally plausible but contextually wrong because the controller was singular.

Do not tune on ZAEBUC DEV.

## Hypothesis

**FINAL_ALIF_EVENT_ONLY**

A narrower event family may generalize better:
- equal source/output token count;
- substitution-only event;
- every changed token output equals the normalized source token plus one final `ا`;
- event_cost <= 0.60;
- at most 3 changed tokens in one contiguous event;
- no word-boundary changes;
- no nun-family acceptance;
- no hamza/lexical acceptance.

This is intended to capture bounded accusative/case/agreement surface realization such as noun/adjective chains.

Comparator:
**FINAL_ALIF_SINGLE_ONLY**
- same rule but exactly one changed token and event_cost <= 0.25.

## Validation population

ZAEBUC-v1.0 Arabic TRAIN, but only a deterministic raw-only 30-line slice.

Selection happens before gold is read:
- normalize only line boundaries (strip outer whitespace);
- compute SHA-256 of `phase2-final-alif-v1|<raw-line>`;
- take the 30 lowest hashes;
- retain original line indices for later gold pairing.

Why:
- disjoint from the already consumed DEV split;
- does not consume ZAEBUC TEST;
- sample selection is independent of gold/error content.

## Runtime order

1. read TRAIN raw only;
2. select 30 lines by hash;
3. run frozen QALB14 GED+AraBART generator;
4. align complete edit events;
5. materialize FINAL_ALIF policies;
6. persist runtime hashes/decisions in artifact;
7. only then read matching TRAIN corrected lines;
8. compare accepted events to gold;
9. manually adjudicate non-exact accepted events;
10. do not tune this policy on the same slice.

## Success criterion

CONTINUE only if:
- no demonstrably wrong accepted event;
- no accepted partial event;
- useful exact-gold support is non-zero;
- multiword accepted events, if any, remain coherent;
- source/scientific downstream guards remain required.

Any accepted demonstrably wrong event => MODIFY.

## Nun family

All nun-changing events remain REVIEW in this gate.

A future NUN_CONTEXTUAL prototype may use dependency/controller/number evidence; CamelParser2.0 is a research candidate because it exposes dependencies plus rich morphology. It is not integrated in this gate.

## Legal/data

ZAEBUC-v1.0 is CC BY-NC-SA 4.0.
Do not commit full corpus text.
Persist compact aggregate evidence and bounded accepted-event excerpts only.
ZAEBUC TEST remains unread.
