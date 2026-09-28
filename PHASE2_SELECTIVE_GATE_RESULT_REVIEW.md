# Phase 2 — Selective Surgical Gate Result Review

Date: 2026-09-28

Status: DEVELOPMENT ONLY. Not sealed. No production threshold is frozen.

Canonical successful run:
- Workflow: Phase 2 Selective Surgical Gate
- Run: 36445972385 (#7)
- Head SHA at run start: 2f812db411278eb23bd10d2ec0e3c3355df96593
- Queue persistence commit: a6fae75c70460eef70af792e6f0d99de79d017b3

## Established results

### Primary operation-aware gate
Runtime-observable policy:
- non-space INSERT: allow
- REPLACE: allow only if NoPnx top-1 confidence >= 0.80
- DELETE: abstain
- other/unsafe operations: abstain

Development proxy using the previously adjudicated 60 surgical edits:
- retained edits: 38
- supported: 37
- wrong: 0
- partial: 1
- unnecessary: 0
- supported precision proxy: 97.37%
- changed passages: 26/41
- automated exact target recoveries: 28/150

Passage burden proxy:
- AUTO_ACCEPT_CANDIDATE: 25/41
- REVIEW_REQUIRED: 1/41
- REJECT: 0/41
- UNCHANGED: 15/41

Important: this is not independent re-adjudication. The proxy reuses prior same-agent edit labels, so the new selective outputs must be adjudicated before any freeze.

### Comparison with prior surgical NoPnx1
Prior surgical adjudication:
- 60 applied edits
- 49 supported
- 7 wrong
- 2 partial
- 2 unnecessary
- 22 AUTO_ACCEPT_CANDIDATE passages
- 7 REJECT
- 4 REVIEW_REQUIRED
- 8 UNCHANGED

The operation-aware gate removes every previously observed wrong applied edit in retrospective development analysis while retaining 37 supported edits.

### Scientific authored stress
Primary operation-aware gate:
- protected spans exact: 12/12
- whole source exactly unchanged: 12/12
- [UNK] outputs: 0/12

This improves the prior surgical NoPnx1 stress result from 11/12 exact-source unchanged to 12/12. These are project-authored fidelity probes, not human-gold GEC accuracy.

## Arabic GED feasibility

Two public CAMeLBERT GED-13 models were tested as deployable localization signals without using Nahw gold targets as model input.

ZAEBUC GED-13:
- published target locations detected: 99/150 = 66.0%
- source words flagged non-UC: 220/1931 = 11.39%

QALB14 GED-13:
- published target locations detected: 79/150 = 52.67%
- source words flagged non-UC: 187/1931 = 9.68%

Hard GED gating did not improve the already-high operation-aware precision proxy:

- operation-aware: 37/38 supported, 28 automated exact recoveries
- + ZAEBUC GED hard gate: 30/31 supported, 24 exact recoveries
- + QALB14 GED hard gate: 25/26 supported, 21 exact recoveries
- GED union: 31/32 supported, 24 exact recoveries
- GED intersection: 24/25 supported, 21 exact recoveries

Interpretation:
GED is useful as a localization signal, but in this direct-source feasibility configuration it is not justified as a hard acceptance gate. It removes supported corrections while adding no observed wrong-edit reduction beyond the operation-aware policy.

Method limitation:
The EMNLP 2023 GED/GEC setup used contextual morphological preprocessing. This probe deliberately used direct source text for a bounded deployability test, so it is not a reproduction of the full published GED pipeline.

## Reversible normalization probe

Among 98 prior TOKENIZER_UNK_WORD hazards:
- tokenizable after internal combining-mark/tatweel removal: 98/98
- still [UNK]: 0/98
- delivered source changes: 0
- corrections applied in this probe: 0

This is a strong feasibility signal for a reversible normalized model view, but tokenizability is not correction safety. The normalized view must not be delivered directly, and future edits must round-trip to exact original source offsets.

## What improved vs the previous checkpoint

Improved:
1. wrong applied edits in the retrospective gate proxy: 7 -> 0.
2. retained supported-edit precision proxy: 81.67% -> 97.37%.
3. rejected passage proxy: 7 -> 0.
4. scientific exact-source unchanged: 11/12 -> 12/12.
5. unknown-token output remains 0.
6. selective adjudication queue now exists with prior labels omitted from Pass 1.

Worsened / trade-off:
1. automated exact target recovery falls from surgical 32 flags to 28 under operation-aware selectivity.
2. hard GED gating reduces target recovery further to 21-24 without improving the zero-wrong proxy.
3. coverage remains the principal unresolved problem; precision-first gating cannot recover the many missed Nahw corrections.

## Epistemic caution

The prior surgical automated 32 exact flags contained five false exact flags on adjudication, so 32 vs 28 is not a final quality comparison. The selective queue must be linguistically adjudicated before judging the true target-coverage loss.

## Current gate conclusion

The operation-aware policy is the strongest candidate for the next adjudication.

GED should remain a secondary signal / diagnostic, not a hard gate in its current direct-source form.

Reversible normalization is the strongest new technical opportunity for recovering tokenizer-limited coverage, but it must be tested with exact source projection and safety locks before any edit is accepted.
