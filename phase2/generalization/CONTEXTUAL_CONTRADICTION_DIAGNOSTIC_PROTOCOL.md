# Phase 2 — Contextual Contradiction Veto Diagnostic

Date: 2026-09-29
Status: PRE-REGISTERED DIAGNOSTIC

## Scope

This diagnostic follows the completed Cross-Corpus Independent Edit Agreement Gate.

It does **not** re-label exact agreement as safe.
It asks whether cheap, context-sensitive negative evidence can identify unsafe edits inside the 159-event EXACT_SINGLE_SUB_AGREEMENT stream.

This is a development diagnostic on an already consumed QALB15 TRAIN slice. It is not an independent generalization estimate and cannot authorize production promotion.

## Frozen input

Use the already frozen cross-model agreement runtime artifact from:
- workflow run: 36484171517
- artifact: phase2-cross-model-agreement-internal
- artifact digest: sha256:13b13418725ae124a96b5847d80323d7de5738d1efbea487d293bd7583a77399
- agreement features SHA-256: d66a5ab3c6b9e1527b7a1a59ddce0f843a864281e70106cacd58d00315741c4c

Primary population:
EXACT_SINGLE_SUB_AGREEMENT == ACCEPT (159 events).

No QALB TEST.

## Negative evidence

After applying each frozen agreed edit to its original raw sentence:

1. Run frozen QALB14 GED on the candidate sentence.
2. Run contextual CAMeL BERT morphological disambiguation on the candidate sentence.

### GED_CONTRADICTION
VETO_TO_REVIEW if any edited token is still predicted by GED as a non-UC error class.

No score threshold is tuned.

### GED_OR_NO_MORPH
VETO_TO_REVIEW if:
- GED_CONTRADICTION, or
- an edited candidate token has no contextual morphology analysis.

### BACKOFF_DIAGNOSTIC
Record whether the top contextual morphology analysis is a backoff / noun_prop fallback.
This is diagnostic only and is not a promotion policy because genuine proper nouns may trigger it.

## Evaluation order

1. Download the frozen agreement artifact.
2. Read QALB15 TRAIN raw only.
3. Materialize GED/morph contradiction flags.
4. Hash/freeze runtime diagnostic features.
5. Only then load the already completed hash-only manual review labels.
6. Measure:
   - wrong-event capture (8 known wrong in primary stream);
   - partial/unnecessary capture;
   - supported-event retention (144 known supported in primary stream).

## Interpretation

This is useful only if it provides strong separation without destroying the 144 supported agreements.

Even a strong result here must be tested unchanged on a new disjoint slice before any auto-accept promotion.

Do not:
- tune GED probability thresholds;
- add word-specific exception lists;
- use gold/QALB corrected text in runtime;
- use QALB TEST;
- start Phase 3.


## Pre-registered diagnostic interpretation thresholds

These thresholds are fixed before the diagnostic result is inspected:

- **STRONG_SIGNAL**:
  - wrong-correction capture >= 75% (at least 6 of the 8 known wrong events), and
  - supported-event retention >= 90% (at least 130 of 144 supported events).

- **PROMISING_SIGNAL**:
  - wrong-correction capture >= 50% (at least 4 of 8), and
  - supported-event retention >= 90%.

- **WEAK_OR_UNHELPFUL**:
  - wrong-correction capture < 50%, or
  - supported-event retention < 90%.

Secondary reporting:
- unsafe capture across WRONG + PARTIAL + UNNECESSARY;
- precision of the residual KEEP_ACCEPT stream.

Even STRONG_SIGNAL does not authorize auto-accept because this is the already consumed 50-line cross-corpus slice. A promising/strong veto must be frozen and retested unchanged on a fresh disjoint population.
