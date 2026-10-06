# AT0 EN V2.6 — R4.3 Contextual Typed Pair Diagnostic Design V2

Date: 2026-10-07
Status: FROZEN FOR PREFLIGHT ONLY
Supersedes: `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V1.md` where explicitly amended below.

All V1 architecture, split, negative-generation, ancestry-isolation, H0/H1, evaluation and stop rules remain unchanged except the source BIO semantics in Section 6.

## 1. Why V2 exists

The first no-training TRAIN-only preflight stopped before producing a split because it found examples whose first token is tagged `I-P`, `I-I` or `I-O`.

A direct read-only audit of the exact pinned TRAIN source established:

- source documents = 400;
- within-sequence invalid `I-*` transitions = 0;
- sequence-initial `I-*` cases = 11;
- all 11/11 are immediately preceded, within the SAME `-DOCSTART-` document, by a previous blank-delimited sequence whose last token has the SAME entity type;
- invalid cross-sequence continuation cases = 0.

Counts:
- initial `I-P` = 8;
- initial `I-I` = 2;
- initial `I-O` = 1.

The upstream source reader itself treats blank lines as independent model examples while preserving the supplied `I-*` label; it does not rewrite these starts to `B-*`.

Therefore these are source continuation segments across example boundaries, not arbitrary malformed BIO labels.

## 2. Frozen continuation-segment semantics

Raw labels MUST remain unchanged.

For token-level ancestor training:
- preserve the original initial `I-*` exactly as supplied.

For span-level pair construction and exact segment scoring inside a blank-delimited source example:
- an example-initial `I-X` is treated as the start coordinate of an `X` continuation SEGMENT for that example;
- do NOT rewrite the stored label to `B-X`;
- do NOT join a span across two model examples;
- do NOT join across documents.

This explicitly freezes the same effective segment behavior used by the historical ACAD_PASS `spans_from_tags` logic while making the source convention visible rather than silently normalizing it.

This choice is necessary for comparability with R4.2C/R4.2D and with the established per-example candidate pipeline.

## 3. Revised BIO preflight failure conditions

Preflight MUST stop if any of the following occurs:

1. an `I-X` inside an example follows neither `B-X` nor `I-X`;
2. an example begins with `I-X` but the previous example in the same source document does not end in `B-X` or `I-X`;
3. an initial `I-X` appears in the first example of a source document;
4. the observed continuation inventory differs from the frozen TRAIN audit above;
5. exact coordinate/class collisions exist within one example.

Preflight MUST report the continuation inventory in its evidence.

## 4. No scientific training authorization

This amendment authorizes only correction of the preflight semantics and one replacement no-training TRAIN-only preflight.

It does NOT authorize:
- ancestor training;
- H0/H1 training;
- historical DEV access;
- TEST/other-fold access;
- protected external evaluation.
