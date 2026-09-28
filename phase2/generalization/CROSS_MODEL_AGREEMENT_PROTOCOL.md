# Phase 2 — Cross-Corpus Independent Edit Agreement Gate

Date: 2026-09-28
Status: PRE-REGISTERED BEFORE READING QALB-2015 L2 TRAIN GOLD CONTENT

## Motivation

Repeated local structural rules generalized poorly because local character/morphology evidence can miss controller, agreement, clitic, or syntactic context.

The strongest existing development signal remains **independent exact correction agreement**:
- SWEET NoPnx1 proposes a source-local edit;
- independent AraBART proposes the same edit at the same source location;
- neither model is treated as a correctness oracle by itself.

This gate tests whether that idea generalizes on a fresh cross-corpus population.

## External corpus

Source repository:
CAMeL-Lab/arabic-gec

Pinned upstream commit:
8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

Corpus:
QALB-2015 L2 TRAIN

Raw input:
data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids

Gold, opened only after agreement decisions are materialized:
data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.cor.no_ids

License:
internal research/evaluation only; no redistribution.

QALB-2015 TEST remains unread.

## Fresh deterministic population

Use a raw-only 50-line slice:
1. strip only outer whitespace;
2. compute SHA-256("phase2-cross-model-agreement-v1|" + raw_line);
3. take the 50 lowest hashes;
4. retain original line IDs and raw-line hashes;
5. selection is performed independently by the SWEET and AraBART jobs and must match exactly;
6. no corrected/gold text is read during selection or generation.

This TRAIN population is disjoint from the consumed QALB-2015 L2 DEV gate.

## Frozen generators

### SWEET

Official CAMeL-Lab text-editing runtime:
- upstream code: CAMeL-Lab/text-editing
- commit: 4d552ca3ae98029550f27fc52aa1b22883e16e61
- model: CAMeL-Lab/text-editing-zaebuc-nopnx
- official weight SHA-256: 584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6
- Python 3.10
- torch 1.12.1+cpu
- transformers 4.30.0
- official gec.tag.rewrite
- **NoPnx iteration 1 only** for agreement, matching the existing surgical/independent-candidate evidence path.

No punctuation model is used in this gate.

### AraBART

Frozen independent stack:
- GED: CAMeL-Lab/camelbert-msa-qalb14-ged-13
- GEC: CAMeL-Lab/arabart-qalb14-gec-ged-13
- CAMeL-Lab/arabic-gec pinned commit above
- same runtime used by the completed Independent Candidate Acceptance and generalization gates.

## Event representation

Each model output is aligned independently to the same raw source using the already established base-letter word alignment:
- Arabic combining marks/tatweel/punctuation ignored for alignment identity;
- original event boundaries retained;
- contiguous non-KEEP operations form one edit event.

Agreement is defined from frozen event representations, not sentence similarity.

## Runtime safety veto

Before any ACCEPT:
- reject/review events touching digits, Latin letters, citation-like brackets, %, =, <, >, ±, or similarly protected scientific-symbol patterns;
- mark-only/base-letter-unchanged edits are not auto-accepted here;
- no target/gold fields are available at runtime.

These are conservative platform-level protections, not corpus-specific rules.

## Frozen policies

### EXACT_SINGLE_SUB_AGREEMENT — primary

ACCEPT only if both SWEET NoPnx1 and AraBART independently produce:
- a one-source-token substitution event;
- the same source lexical span;
- exactly one output token;
- identical canonical/base-letter output token;
- no protected/scientific-risk veto;
- output base differs from source base.

All other events: REVIEW.

### EXACT_BOUNDED_SUB_EVENT_AGREEMENT — secondary

ACCEPT only if both models independently produce:
- the same source lexical span;
- substitution-only complete events;
- 1 to 3 source tokens;
- equal source/output token counts for each model;
- identical canonical/base-letter output token sequence;
- no protected/scientific-risk veto;
- at least one base-letter change.

This policy includes the primary single-token policy and bounded multiword agreement.

### NORMALIZED_EVENT_AGREEMENT — diagnostic only

A looser normalized comparison may be measured for research diagnostics, but it is not eligible for promotion in this gate.

## Anti-leakage order

1. SWEET job reads raw only and materializes its selected-line hashes + event output.
2. AraBART job reads raw only and independently materializes the same selection + event output.
3. Agreement job asserts identical selected line IDs/hashes.
4. Agreement job materializes frozen ACCEPT/REVIEW decisions without gold.
5. Agreement decision artifact is hashed/frozen.
6. Only then is QALB-2015 L2 TRAIN corrected text opened.
7. Gold comparison is performed.
8. Exact-gold matches count as automatic support.
9. Non-exact accepted events require bounded contextual adjudication; they are not automatically called correct or wrong.
10. No policy threshold or agreement rule is changed on this slice after gold is read.

## Primary success criterion

EXACT_SINGLE_SUB_AGREEMENT may advance only if:
- at least 10 accepted events are observed (preferred minimum for this 50-line slice);
- zero demonstrably wrong accepted events after contextual review;
- zero partial accepted events;
- exact-gold support is non-zero;
- no protected/scientific-risk event is accepted.

If accepted events < 10:
**UNPROVEN_LOW_COVERAGE**, regardless of apparent precision.

Any demonstrably wrong accepted event:
**MODIFY**.

EXACT_BOUNDED_SUB_EVENT_AGREEMENT is secondary:
- any wrong/partial multiword accepted event => do not promote bounded multiword auto-accept.

## Metrics

Report:
- total SWEET edit events;
- total AraBART edit events;
- exact single agreement count;
- bounded exact agreement count;
- exact-gold supported accepted events;
- same-span different-output-vs-gold;
- overlap/non-exact accepted events;
- no-gold-overlap accepted events;
- contextual adjudication of every non-exact accepted event;
- accepted-event passage clustering;
- operation and span-length distribution;
- runtime/model provenance.

## Data handling

QALB license prohibits redistribution.

Do NOT commit:
- QALB raw text;
- QALB corrected text;
- reconstructed passages;
- full model outputs.

Persist to GitHub only:
- upstream commit/file hashes;
- selected original line IDs;
- raw-line hashes;
- event identity hashes and compact event geometry;
- aggregate metrics;
- gold classification labels;
- no QALB excerpts.

Ephemeral GitHub Action artifacts containing internal model event payloads must use short retention and are for internal research only.

No QALB-2015 TEST.
No final sealed benchmark.
No Phase 3.
