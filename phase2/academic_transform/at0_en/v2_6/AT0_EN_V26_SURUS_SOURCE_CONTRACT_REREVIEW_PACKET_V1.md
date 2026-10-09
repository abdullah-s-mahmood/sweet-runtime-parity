# ACAD_PASS — Limited SURUS Source-Contract Re-Review Packet V1

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `at0-en-v2.6-dev`

State:
`LIMITED_HIGHER_MODEL_RE_REVIEW_REQUIRED / NO_SCIENTIFIC_FIT`

## 1. Scope

This is NOT a general reopening of the SURUS admission review.

The prior independent review:
`FINAL_SURUS_ADMISSION_REVIEW_V1.md`

already decided:
`PROCEED_SURUS_ADMISSION_WITH_CHANGES`

and Amendment V2 has been prospectively frozen.

Only ONE unresolved scientific question is referred back:

> Can the pinned public release's Start/End character coordinates be prospectively treated as the authoritative SURUS human-gold span boundary representation even when released Annotation.Text is not an exact raw substring of the current released Abstract, under a fixed fail-closed contract? Or does the remaining source-serialization ambiguity require rejection/pause of SURUS admission?

No scientific fitting is authorized by this re-review.

---

## 2. Governing prior requirement

The original independent review required:
- exact text/offset round-trip validation;
- every positive to be representable;
- unrepresentable positives halt closure;
- no silent dropping or repair.

It also stated admission failure includes:
`unrecoverable positive spans`.

This re-review exists because new read-only evidence shows the source release has a systematic annotation-text serialization issue, while the released character coordinates are far more coherent.

The current assistant is NOT authorized to weaken the prior requirement without independent review.

---

## 3. Frozen source

Repository:
`surus-ai/dataset`

Commit:
`3a61790d5c304dea95fb278f76cc3b1a0ca07564`

Release:
- 523 article rows
- 48,833 annotation rows
- 25 released LabelIDs
- 7 LabelClasses
- Start / End
- TokenStart / TokenEnd
- Text
- ArticleID / LabelID

License:
`CC-BY-NC-4.0`

---

## 4. Corrected ontology evidence

The higher-model review found that the original project audit incorrectly keyed ontology/counts by label name and collapsed 25 IDs into 22 names.

This was repaired.

Corrected audit now preserves:
`(source_commit, released_LabelID)`

and all 25 channels independently.

The corrected schema component is not the remaining blocker.

---

## 5. Corrected schema/coordinate audit attempt

Run:
`37914385700`

Result:
`FAIL — MECHANICAL PREFLIGHT / NO SCIENTIFIC ATTEMPT`

Released rows:
`48,833`

Exact:
`Abstract[Start:End] == Annotation.Text`

for:
`44,643`

Initial mismatch:
`4,190 = 8.5803%`

All Start/End values were numerically in bounds.

No protected data/model fit/scientific metric was involved.

---

## 6. Aggregate mismatch diagnostic V1

Run:
`37914600126`

Artifact:
`11609690713`

Digest:
`sha256:02c42a9e2439f555636c611875c4c7b5a055bdb8f6e93b4d2052d9dc95c1873b`

Among 4,190 mismatches:
- 4,113 Annotation.Text values have no exact occurrence anywhere in released Abstract;
- 45 have one exact occurrence at another offset;
- 32 have multiple exact occurrences;
- simple Title/Abstract coordinate models do not explain the release;
- simple NFKC/HTML/whitespace normalization does not rescue them.

---

## 7. Article/field diagnostic V2

Run:
`37914932110`

Artifact:
`11608697424`

Digest:
`sha256:69c688f51996eda49cbb09175f5adcede785efcf99ef0d1fca50f97b46f76d83`

Findings:
- affected articles = 437 / 523;
- exact-only articles = 86;
- fully mismatched articles = 0;
- every affected article contains both exact and mismatch annotations.

This argues against a simple whole-document-version mismatch.

At released offsets, mismatch Text is usually highly similar to the raw slice.

Dominant length differences:
- Annotation.Text longer by 2 chars: 2,154 rows;
- +1: 1,049;
- +3: 322;
- +4: 286;
- +5: 120;
- +6: 96.

---

## 8. Fixed punctuation/token-spacing diagnostic V3

Run:
`37915291868`

Artifact:
`11609721783`

Digest:
`sha256:901c7691556e57f521c589d123312f1a8f078928aa20bfaa37106a67b9872b80`

Of 4,190 mismatches:

Explained by at least one fixed label-independent punctuation/spacing rule:
`3,060 = 73.0310%`

Still unexplained:
`1,130 = 26.9690% of mismatch rows`

Relative to all released annotations:
`1,130 / 48,833 = 2.3136%`

Main mechanistic evidence:
- 2,691 match Unicode punctuation-token splitting;
- punctuation is present in 3,468 mismatch rows;
- hyphen in 2,132;
- inverse punctuation-spacing transforms explain large overlapping subsets.

Therefore a large majority of mismatches are consistent with tokenized/exported display text rather than different semantic spans.

No repair was authorized.

---

## 9. Pinned BiomedBERT alignment V4

Run:
`37915950311`

Artifact:
`11608843740`

Digest:
`sha256:bdd936769d8eaa4abe87d699925a950e4aa2d9aeff2cc1f327a869a57be8a081`

Frozen tokenizer:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract@d673b8835373c6fa116d6d8006b33d48734e305d`

Frozen tokenizer signature:
`088f1bdf2509aee48015c38209b07bebec8d4d266232e04c5d9bd82704b76e81`

Runtime:
- Python 3.11.16
- transformers 4.48.0
- tokenizers 0.21.0
- huggingface_hub 0.28.1

Key result:

Released Start/End character spans align exactly to frozen tokenizer boundaries for:
`48,640 / 48,833 = 99.6048%`

Only:
`193 = 0.3952%`
do not align exactly to those tokenizer boundaries.

However, released TokenStart/TokenEnd DO NOT correspond globally to this tokenizer.

Four fixed conventions were tested:
- zero-based inclusive;
- zero-based exclusive;
- one-based inclusive;
- one-based exclusive.

Best released-character agreement:
`ZERO_BASED_INCLUSIVE = 2,209 / 48,833`

Therefore the project must NOT reinterpret released TokenStart/TokenEnd as ACAD_PASS BiomedBERT indices.

---

## 10. Official source-code reproducibility search

Peer-reviewed SURUS paper states:
- abstracts were tokenized using a BERT tokenizer;
- BILOU was used;
- adjacent tokens were aggregated into annotations;
- full NER training code, dataset and annotation guide are available at the linked Git repository.

The paper's footnote 8 links:
`https://github.com/surus-ai/dataset`

The complete accessible repository history was checked.

Commits:
- `56c97229dd8a731f618103b0c0610cc4c9dedec0` — LICENSE only;
- `ea172bd779a8b969dbacf01c3ab88055228a23ef` — LICENSE update;
- `67241b4d2ef246e1a41d297487768dc5094c6cd8` — dataset/manual/images/README publication;
- `3a61790d5c304dea95fb278f76cc3b1a0ca07564` — LICENSE merge.

No training code, tokenization code, export code, offset code or annotation-system code is present in the linked official repository history.

Public searches found no separate verified official SURUS implementation repository.

Therefore:
`ORIGINAL_TOKENSTART_TOKENEND_AND_TEXT_EXPORT_SEMANTICS_NOT_REPRODUCIBLE_FROM_RELEASED_CODE`

---

## 11. Important distinction

There are now three separate facts:

A. Label identity:
`CLOSED / 25-ID ontology recoverable`

B. Character coordinates:
`VERY HIGH STRUCTURAL COHERENCE`
- all numerically in bounds;
- 99.6048% align to frozen biomedical tokenizer boundaries.

C. Annotation.Text serialization:
`PARTIALLY NON-ROUNDTRIPPING`
- 91.4197% raw exact;
- most mismatch rows have punctuation/token-spacing explanation;
- 2.3136% of all rows remain unexplained.

The question is whether B can be the authoritative boundary gold while C is retained as non-authoritative release metadata with explicit source-defect accounting.

---

## 12. Candidate rule for adversarial review ONLY

NOT AUTHORIZED unless approved:

1. Authoritative boundary identity:
   `(ArticleID, LabelID, Start, End)`

2. `Annotation.Text` is a consistency/provenance field, not the boundary source of truth.

3. Admission requires:
   - Start/End numeric and inside the released Abstract;
   - non-empty span;
   - full released LabelID/ClassID validity;
   - no protected/family contamination;
   - deterministic tokenizer/window representability.

4. If Start/End is not representable in the frozen ACAD_PASS window/token mapping:
   `FAIL / EXCLUDE DOCUMENT OR STOP`
   only under a prospectively approved rule.

5. Never alter Start/End from Annotation.Text.

6. Never search for Annotation.Text elsewhere to relocate a span.

7. Never snap boundaries.

8. Preserve an audit flag:
   - RAW_TEXT_EXACT
   - FIXED_PUNCT_SERIALIZATION_EXPLAINED
   - TEXT_SERIALIZATION_UNRESOLVED

9. The unresolved flag is source-quality metadata and cannot be used for data/model selection based on performance.

10. No claim that Annotation.Text exactly reproduces the current released Abstract for all rows.

The independent reviewer must accept, reject or modify this rule.

---

## 13. Strongest argument FOR the candidate rule

The human annotation database explicitly releases Start/End coordinates together with LabelID and Text.

The release's character coordinates are:
- in bounds;
- highly tokenizer-boundary coherent;
- spread across partially affected documents rather than corrupted whole documents;
- associated with systematic punctuation-spacing Text differences for most mismatches.

This makes it plausible that Start/End are the intended machine-readable anchors and Text was exported/reconstructed through a different token-display convention.

Rejecting all SURUS supervision because a display/provenance Text field does not always raw-roundtrip may discard otherwise usable expert-reviewed span coordinates.

---

## 14. Strongest argument AGAINST the candidate rule

The original independent review explicitly required exact text/offset round-trips.

No official released implementation proves that Start/End rather than Text is canonical.

1,130 Annotation.Text mismatches remain unexplained.

193 character spans do not align exactly with the already-frozen BiomedBERT token boundaries.

If Start/End itself came from another text serialization, treating it as authoritative against the current Abstract could train small systematic boundary errors.

Changing the rule after examining source diagnostics increases degrees of freedom unless independently authorized now, before any scientific model fit.

---

## 15. Exact questions

Answer explicitly:

1. Does the new evidence justify changing the P1 contract so Start/End character coordinates become authoritative SURUS span boundaries?
2. Or does the prior exact text/offset round-trip requirement remain mandatory, implying SURUS admission must STOP?
3. If Start/End may be authoritative, what exact invariants must every admitted positive satisfy?
4. May Annotation.Text mismatch be retained as a provenance-quality flag without excluding the positive?
5. What exact policy applies to the 193 spans not aligned to frozen BiomedBERT token boundaries?
6. May window/token alignment expand a gold char span to covering subwords, or must exact token-boundary alignment be mandatory?
7. Is document-level exclusion allowed if any positive in that document is unrepresentable, or must the entire SURUS source fail?
8. Does the 1,130 unresolved Text mismatch group require exclusion, quarantine, or merely reporting?
9. Does the 705-row paper/release discrepancy alter the decision?
10. Does absence of the promised official training/export code require rejection, or is transparent release-specific use sufficient?
11. What exact claim wording is allowed if SURUS is admitted under a char-coordinate-authoritative contract?
12. What additional preflight, if any, is required before P2 adapter implementation?
13. Final verdict:
    - `KEEP_SURUS_WITH_CHAR_COORDINATE_CONTRACT`
    - `KEEP_SURUS_WITH_OTHER_CHANGES`
    - `REJECT_OR_PAUSE_SURUS`
14. Exact next operation after the verdict.

---

## 16. Required review behavior

Perform:
- Deep Research;
- Adversarial Review;
- Alternative Hypotheses;
- Failure Analysis;
- Disconfirming Evidence Search;
- source/release-semantics review;
- degrees-of-freedom audit;
- reproducibility audit.

Do NOT optimize for retaining SURUS.

Do NOT authorize model training.

Do NOT open VERIFY_INTERNAL or AD/COVID scoring.

Do NOT change the frozen 45-fit budget.

---

## 17. Copy-ready higher-model prompt

Continue ACAD_PASS as an independent scientific review board for ONE bounded unresolved question. Do NOT train anything and do NOT open protected benchmarks.

Repository:
`abdullah-s-mahmood/sweet-runtime-parity`

Branch:
`at0-en-v2.6-dev`

Read first:
1. `ACAD_PASS_LATEST_STATE.md`
2. `ACAD_PASS_BOOTSTRAP_CONTRACT.md`
3. `phase2/academic_transform/at0_en/v2_6/FINAL_SURUS_ADMISSION_REVIEW_V1.md`
4. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_ADMISSION_PROTOCOL_AMENDMENT_V2.md`
5. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_SCHEMA_COORDINATE_AUDIT_ATTEMPT1_FREEZE_V1.md`
6. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_COORDINATE_MISMATCH_DIAGNOSTIC_FREEZE_V1.md`
7. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_COORDINATE_MISMATCH_DIAGNOSTIC_FREEZE_V2.md`
8. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_TOKEN_RECONSTRUCTION_DIAGNOSTIC_FREEZE_V3.md`
9. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_PINNED_TOKEN_ALIGNMENT_DIAGNOSTIC_FREEZE_V4.md`
10. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_SOURCE_CONTRACT_REREVIEW_PACKET_V1.md`

The prior review approved SURUS only subject to exact source/coordinate closure. New read-only diagnostics show:
- 48,833 released annotations;
- 44,643 raw exact Annotation.Text == Abstract[Start:End];
- 4,190 Text mismatches;
- 3,060/4,190 mismatch rows explained by fixed punctuation/token-spacing transformations;
- 1,130 remain Text-unexplained;
- every affected article is only partially affected; zero articles are wholly mismatched;
- all released Start/End are numerically in bounds;
- 48,640/48,833 (99.6048%) Start/End spans align exactly to the already-frozen BiomedBERT tokenizer boundaries;
- released TokenStart/TokenEnd do not correspond globally to that frozen tokenizer under any fixed 0/1-based inclusive/exclusive convention;
- the SURUS paper states BERT tokenization/BILOU and promises code at its linked GitHub repository, but the complete accessible repository history contains dataset/manual/images/license only and no training/tokenization/export implementation.

The single decision is whether released Start/End character coordinates may now be frozen prospectively as authoritative SURUS span gold, treating Annotation.Text as a non-authoritative provenance/consistency field with explicit mismatch flags; OR whether the original exact text/offset round-trip requirement must remain, forcing SURUS admission to pause/reject.

Perform Deep Research, Adversarial Review, Alternative Hypotheses, Failure Analysis, Disconfirming Evidence Search, source-semantics/reproducibility review and a degrees-of-freedom audit.

Answer all 14 questions in Section 15 of the packet.

Do NOT:
- train a model;
- authorize scientific fitting;
- open VERIFY_INTERNAL;
- score AD/COVID;
- change the 45-fit ceiling;
- invent missing source semantics;
- silently drop/repair spans.

End with exactly one verdict:
`KEEP_SURUS_WITH_CHAR_COORDINATE_CONTRACT`
or
`KEEP_SURUS_WITH_OTHER_CHANGES`
or
`REJECT_OR_PAUSE_SURUS`

and give the exact next non-scientific operation.
