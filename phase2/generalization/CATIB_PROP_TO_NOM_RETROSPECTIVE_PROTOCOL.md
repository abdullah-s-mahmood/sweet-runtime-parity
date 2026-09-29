# Phase 2 — CATIB_PROP_TO_NOM_EVIDENCE_V1 Retrospective Replication

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE CATiB FEATURES ON THE REPLICATION POPULATION

## Origin of hypothesis

On the consumed third-slice 14-event V1 population, post-hoc dependency feature analysis found:
- source CATiB PROP to candidate NOM in 10/12 supported;
- PROP to NOM in 0/2 partial.

This is hypothesis-generating evidence only.

## Replication population

Earlier consumed canonical tri-model slice from run 36517205396.

Primary retrospective population:
- the 36 events that frozen diagnostic ORTHO_MORPH_COMMON_NOUN_V1 passed;
- known historical outcome: 34 supported, 2 partial.

Nested strict V1 subset:
- 19 events passed ORTHO_ISOLATED_COMMON_NOUN_V1;
- historical outcome: 19 supported.

The CATiB feature materializer MUST NOT read those labels.

## Frozen hypothesis

CATIB_PROP_TO_NOM_EVIDENCE_V1 PASS iff:
1. source and candidate parser mapping are reliable;
2. source target baseword CATiB POS == PROP;
3. candidate target baseword CATiB POS == NOM.

No dependency-relation, head, distance, threshold, or other feature may be added during this replication.

## Parser

- CAMeL-Lab/camel_parser
- commit 66f29f7e34e3b5b38780d08bd56cf481635bf1c6
- CATiB
- preprocessed_text
- explicit per-whitespace-word parser-token span mapping validated by the completed smoke protocol.

## Anti-leakage order

1. Reuse frozen 142-event contextual-guard feature file to select the 36 label-free runtime decisions.
2. Reuse frozen tri-model AraBART candidate artifacts from run 36517205396.
3. Read QALB15 TRAIN RAW only.
4. Materialize CATiB source/candidate POS and frozen PROP-to-NOM decisions.
5. Hash and leakage-audit the features.
6. Only then read prior adjudication labels.
7. No post-result rule modification.

## Pre-registered promising criterion

The hypothesis is promising enough to justify a genuinely fresh fourth-slice validation only if:
- accepted events on the 36-event population >= 10;
- accepted wrong = 0;
- accepted partial = 0;
- accepted unnecessary = 0;
- strict V1 subset accepted events >= 10.

Passing this criterion is retrospective evidence only. It does not authorize promotion.

QALB15 TEST remains unread. No sealed benchmark. No Phase 3.
