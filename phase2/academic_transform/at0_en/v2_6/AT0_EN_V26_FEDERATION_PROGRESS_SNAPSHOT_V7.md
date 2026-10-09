# ACAD_PASS — Federation Progress Snapshot V7

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

State:
`SURUS_AMENDMENT_V2_FROZEN / HIGHER_MODEL_REREVIEW_INTERRUPTED / P1_SOURCE_CONTRACT_STILL_OPEN / V5_V6_V7_MECHANICS_FROZEN / NO_SUCCESSOR_SCIENTIFIC_FIT`

## 1. Current process readiness

Mandatory F01-F06 closure:
`87.83%`

First scientific-fit readiness:
`73.2%`

Change versus V6:
`0.0 percentage points`

Reason:
V5-V7 substantially reduce uncertainty about SURUS source semantics but do not yet close the mandatory P1 source-coordinate/source-unit contract. No readiness credit is granted until that gate is actually closed.

These percentages are PROCESS READINESS only.

## 2. Scientific performance

No successor scientific fit has occurred.

Latest actual scientific model result remains frozen R44C at t=.95:
- macro precision = 0.8767348592080204
- P = 0.8918918918918919
- I = 0.8171091445427728
- C = 0.9318181818181818
- O = 0.8661202185792349

Performance delta:
`NONE`

## 3. Higher-model rereview interruption

The limited higher-model SURUS source-contract rereview started but was interrupted by the user's usage limit before any final verdict.

Recovered substantive statement:
- high structural coordinate consistency alone does not prove the human annotators intended those exact boundaries;
- the prior 99.6048% diagnostic measured raw-text WordPiece boundaries;
- the reviewer was checking whether that matched the actual segment unit used by the frozen ACAD_PASS implementation.

No final verdict was issued.

No durable GitHub mutation was left by that higher-model session.

Freeze:
`AT0_EN_V26_SURUS_INTERRUPTED_SOURCE_CONTRACT_REVIEW_EVIDENCE_V1.md`

## 4. Frozen ACAD_PASS segment-unit clarification

The existing federation protocol/implementation requires:
- original words/characters;
- source offsets;
- original-to-model offset map;
- window planning by WordPiece budget but rounded to complete source-word boundaries;
- each source word represented by the mean of its subword vectors.

Therefore:
`WORDPIECE_BOUNDARY_ALIGNMENT_ALONE != FULL_SOURCE_UNIT_REPRESENTABILITY_CERTIFICATION`

For SURUS, the public release does not supply a reproducibly documented source-token unit whose absolute TokenStart/TokenEnd semantics can be recovered.

## 5. Source-paper evidence

The peer-reviewed SURUS paper states:
- abstracts were tokenized using a BERT tokenizer;
- the linked model/tokenizer reference is bert-base-uncased;
- BILOU labels were assigned to subword tokens;
- adjacent tokens were aggregated;
- entity evaluation required token-start, token-end and label matches.

The paper/preprint also stated that full model code would be publicly available at publication.

The linked official repository history:
`surus-ai/dataset`

contains dataset/manual/images/license but no released training/tokenization/export/offset implementation.

Thus:
`ORIGINAL_RELEASE_TOKEN_INDEX_EXPORT_IMPLEMENTATION_NOT_PUBLICLY_REPRODUCIBLE`

## 6. V5 — source BERT WordPiece diagnostic

Run:
`37919107413`

Artifact:
`11611123584`

Digest:
`sha256:2d43434d6ecbd33e270a423d4e29300cd75d970353bc5e782f32bdeeaf6da51f`

Pinned reconstruction tokenizer:
`google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`

Findings:
- released Start/End align to BERT WordPiece boundaries: `48,719 / 48,833 = 99.7666%`;
- direct released TokenStart/TokenEnd recovery under 8 fixed index conventions failed;
- best exact token-pair agreement: `279 / 48,833`.

Decision:
`DIRECT_BERT_WORDPIECE_INDEX_SEMANTICS_REJECTED`

## 7. V6 — source-unit diagnostic

Run:
`37919404071`

Artifact:
`11610764435`

Digest:
`sha256:0ec7e0dc73a1096b51d9702f9ffba69613b5d9ab47b91a2ea206e5c2e65fdb2e`

Character Start/End alignment:
- BERT pre-tokenizer: `48,336 / 48,833 = 98.9822%`
- deterministic word+punctuation: `48,483 / 48,833 = 99.2833%`
- whitespace: `27,595 / 48,833 = 56.5089%`

Best absolute token-index agreement:
- word+punctuation: `12,585 / 48,833 = 25.7715%`
- BERT pre-tokenizer: `12,155 / 48,833 = 24.8910%`

Decision:
`TOKENSTART_TOKENEND_NOT_GLOBAL_INDICES_OF_TESTED_SOURCE_UNITS`

## 8. V7 — token width / local shift diagnostic

Run:
`37919734516`

Artifact:
`11611114778`

Digest:
`sha256:fbedf6dbdb16c0d8bffca3a859a2f1db11fd4ae9834eeeb8e8c0c4212aef5970`

Inclusive token-span width agreement:

BERT pre-tokenizer:
- all rows: `42,242 / 48,833 = 86.5030%`
- char-aligned rows: `42,242 / 48,336 = 87.3924%`

Word+punctuation:
- all rows: `42,419 / 48,833 = 86.8654%`
- char-aligned rows: `42,419 / 48,483 = 87.4925%`

Exclusive width agreement is only ~2.3-2.5%.

Thus:
`RELEASED_TOKEN_END_IS_STRONGLY_MORE_COMPATIBLE_WITH_INCLUSIVE_WIDTH_SEMANTICS`

But absolute shift is not stable:

Word+punctuation:
- one observed shift/article = 22
- multiple shifts/article = 501

BERT pre-tokenizer:
- one observed shift/article = 21
- multiple shifts/article = 502

Decision:
`SIMPLE_GLOBAL_OR_DOCUMENT_LOCAL_SHIFT_HYPOTHESIS_REJECTED`

## 9. Combined source-contract conclusion

Strongly supported:
1. released Start/End character coordinates are structurally coherent;
2. they align with BERT-family WordPiece boundaries at >99.6%;
3. they align with deterministic word+punctuation source boundaries at >99.2%;
4. TokenStart/TokenEnd preserve inclusive span-width structure for ~86.9% of all rows.

Not supported:
1. TokenStart/TokenEnd as direct BERT WordPiece indices;
2. TokenStart/TokenEnd as direct BERT-pretoken/regex/whitespace global indices;
3. one fixed article-local token offset;
4. exact public reconstruction of the original annotation/export tokenizer.

Therefore TokenStart/TokenEnd MUST NOT be used to relocate or repair character spans.

The remaining governance question is whether Start/End alone may prospectively serve as authoritative human-gold boundaries with an explicitly frozen SURUS-specific representation contract, or whether SURUS admission must pause/reject.

## 10. Current protected / attempt state

45 D0-D4 scientific attempts:
`NOT_STARTED / UNCONSUMED`

D5:
`CANCELED_WITHOUT_REPLACEMENT`

VERIFY_INTERNAL:
`CLOSED`

AD/COVID external scoring:
`CLOSED`

SURUS OOD scoring:
`NOT_AUTHORIZED`

R44C:
`FROZEN / CONSUMED / NOT_RERUN`

## 11. Exact next operation

`INDEPENDENT_HIGHER_MODEL_LIMITED_SURUS_SOURCE_CONTRACT_REREVIEW_V2`

No P2 adapter implementation and no scientific fit until a final independent verdict is frozen.

If the higher-model account remains unavailable, technical work may continue only where it cannot predetermine or weaken the pending source-contract decision.
