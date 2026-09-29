# Phase 2 — Cross-Training Tri-Model Edit Voting Gate

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE FRESH QALB15 TRAIN GOLD

## Motivation

Exact two-model agreement (SWEET QALB14 + AraBART QALB14) improved the stream to 144 supported / 159 accepted, but 15 unsafe edits remained. Morphology, GED, lexical continuity, simple risk families, and multilingual semantic NLI did not provide a promotable cleanup layer.

Recent Arabic GEC and edit-level voting research supports testing multi-system agreement rather than another global score.

## Fresh population

Corpus: QALB-2015 L2 TRAIN.

Use a NEW raw-only 50-line deterministic slice:
1. Recompute the previously consumed 50 line IDs using seed phase2-cross-model-agreement-v1.
2. Exclude those IDs.
3. For remaining raw lines compute SHA-256(phase2-trimodel-vote-v1|raw_line).
4. Select the 50 lowest hashes.
5. Gold is unavailable to all model/vote jobs.

QALB-2015 TEST remains unread.

## Model voters

### V1 — SWEET_QALB14
- CAMeL-Lab/text-editing-qalb14-nopnx
- edit-tag architecture (AraBERTv02 based),
- trained on QALB-2014,
- MIT.

### V2 — SWEET_ZAEBUC
- CAMeL-Lab/text-editing-zaebuc-nopnx
- same edit-tag architecture family but different training corpus,
- model card describes ZAEBUC training,
- MIT.

### V3 — ARABART_QALB14
- CAMeL-Lab/arabart-qalb14-gec-ged-13
- seq2seq AraBART + morphology/GED pipeline,
- trained on QALB-2014,
- MIT.

## Explicit exclusion

Do NOT use CAMeL-Lab/arabart-zaebuc-gec-ged-13 in this QALB15 gate. Its public model card describes fine-tuning data that include QALB-2015, so using it would contaminate a QALB15 generalization test.

## Event unit

Single-source-token substitution events only for this gate.

Every vote must match exactly on:
- original line ID/hash;
- source lexical span;
- source canonical/base token;
- candidate canonical/base token.

Protected scientific-risk veto from the existing cross-model helper remains active.

## Frozen policies

### UNANIMOUS_3 — primary high-precision candidate
ACCEPT only if all three voters propose the same exact single-token substitution and no protected veto fires.

### ARABART_PLUS_ANY_SWEET — secondary
ACCEPT if ARABART_QALB14 and at least one SWEET voter propose the same exact single-token substitution, with no protected veto.

### BOTH_SWEETS — diagnostic only
Measure exact agreement of the two SWEET models. It is not eligible for promotion because architecture-family errors may be correlated.

## Anti-leakage order

1. All three model jobs independently select the same fresh raw slice.
2. All three materialize raw-only edit events.
3. Voting job verifies identical line IDs/hashes.
4. Vote decisions are materialized and hashed.
5. Only then is QALB15 TRAIN corrected text opened.
6. Exact gold matches count as automatic support.
7. Every non-exact accepted event requires bounded contextual adjudication.
8. No policy is modified on this slice.

## Promotion criterion

UNANIMOUS_3 may advance only if:
- accepted events >= 10;
- zero wrong corrections after contextual review;
- zero partial corrections;
- zero unnecessary edits;
- no protected-risk event accepted.

ARABART_PLUS_ANY_SWEET is evaluated under the same zero-unsafe requirement but is secondary.

If accepted <10: UNPROVEN_LOW_COVERAGE.

Any wrong/partial accepted event: MODIFY / DO_NOT_PROMOTE.

## Constraints

- no QALB text committed;
- no QALB15 TEST;
- no final sealed benchmark;
- no Phase 3;
- no learned meta-classifier trained on this slice.