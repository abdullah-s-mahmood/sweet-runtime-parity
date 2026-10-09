# ACAD_PASS — LATEST STATE POINTER

Timestamp: 2026-10-09 13:51:19 Asia/Baghdad (UTC+3)

Current active branch:
`at0-en-v2.6-dev`

Branch HEAD immediately before this pointer update:
`c10746398a590294716d9e3a65f00064873babaa`

Permanent cross-chat bootstrap contract:
`ACAD_PASS_BOOTSTRAP_CONTRACT.md`

## Latest authoritative checkpoint

`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_FEDERATION_PROGRESS_SNAPSHOT_V7.md`

Checkpoint commit:
`87b3d33f2c3264ea91cea0596db12fb32e356fe0`

## Current scientific state

`SURUS_AMENDMENT_V2_FROZEN / HIGHER_MODEL_REREVIEW_INTERRUPTED_BEFORE_VERDICT / P1_SOURCE_CONTRACT_OPEN / V5_V6_V7_FROZEN / NO_SUCCESSOR_SCIENTIFIC_FIT`

Process readiness:
- mandatory F01-F06 closure: **87.83%**
- first-fit readiness: **73.2%**

Readiness change versus V6:
`0.0 percentage points`

Reason:
V5-V7 reduced source-semantics uncertainty but did not close P1.

Scientific performance:
unchanged; latest actual result remains frozen R44C.

## Governing review / amendment

Original final SURUS admission review:
`phase2/academic_transform/at0_en/v2_6/FINAL_SURUS_ADMISSION_REVIEW_V1.md`

Verdict:
`PROCEED_WITH_CHANGES`

Frozen amendment:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_ADMISSION_PROTOCOL_AMENDMENT_V2.md`

Still:
`GO_FOR_BOUNDED_AMENDMENT / NO_GO_FOR_SCIENTIFIC_EXECUTION`

## Interrupted higher-model rereview

Freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_INTERRUPTED_SOURCE_CONTRACT_REVIEW_EVIDENCE_V1.md`

Status:
`INTERRUPTED_BEFORE_VERDICT`

No final governance verdict was produced.

Recovered concern:
WordPiece-boundary coherence does not itself prove compatibility with the frozen ACAD_PASS source-word segment unit.

## Frozen implementation clarification

ACAD_PASS preserves:
- original words/characters;
- source offsets;
- original-to-model offset map;
- complete source-word window boundaries;
- source-word representations formed from subword means.

Therefore:
`WORDPIECE_ALIGNMENT != FULL_SOURCE_UNIT_CERTIFICATION`

## P1 evidence V1-V4

Raw release:
- annotations = 48,833
- raw Text == Abstract[Start:End] = 44,643 = 91.4197%
- mismatch = 4,190 = 8.5803%
- fixed punctuation/token-spacing explanation = 3,060 / 4,190
- residual Text mismatch = 1,130

V4 frozen ACAD_PASS BiomedBERT:
- run `37915950311`
- artifact `11608843740`
- digest `sha256:bdd936769d8eaa4abe87d699925a950e4aa2d9aeff2cc1f327a869a57be8a081`
- Start/End on WordPiece boundaries = 48,640 / 48,833 = 99.6048%
- released TokenStart/TokenEnd not recoverable as BiomedBERT indices.

## V5 — source-paper BERT WordPieces

Freeze:
`AT0_EN_V26_SURUS_SOURCE_BERT_ALIGNMENT_DIAGNOSTIC_FREEZE_V5.md`

Run:
`37919107413`

Artifact:
`11611123584`

Digest:
`sha256:2d43434d6ecbd33e270a423d4e29300cd75d970353bc5e782f32bdeeaf6da51f`

Pinned reconstruction tokenizer:
`google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`

Findings:
- Start/End align to WordPiece boundaries = 48,719 / 48,833 = 99.7666%
- best direct TokenStart/TokenEnd recovery = 279 / 48,833

Decision:
`DIRECT_BERT_WORDPIECE_INDEX_SEMANTICS_REJECTED`

## V6 — source-unit reconstruction

Freeze:
`AT0_EN_V26_SURUS_SOURCE_UNIT_DIAGNOSTIC_FREEZE_V6.md`

Run:
`37919404071`

Artifact:
`11610764435`

Digest:
`sha256:0ec7e0dc73a1096b51d9702f9ffba69613b5d9ab47b91a2ea206e5c2e65fdb2e`

Start/End alignment:
- BERT pre-tokenizer = 48,336 / 48,833 = 98.9822%
- deterministic word+punctuation = 48,483 / 48,833 = 99.2833%
- whitespace = 27,595 / 48,833 = 56.5089%

Best absolute released token-pair recovery:
- word+punctuation = 12,585 / 48,833 = 25.7715%
- BERT pre-tokenizer = 12,155 / 48,833 = 24.8910%

Decision:
`TOKENSTART_TOKENEND_NOT_GLOBAL_INDICES_OF_TESTED_SOURCE_UNITS`

## V7 — token width / local shift

Freeze:
`AT0_EN_V26_SURUS_TOKEN_WIDTH_SHIFT_DIAGNOSTIC_FREEZE_V7.md`

Run:
`37919734516`

Artifact:
`11611114778`

Digest:
`sha256:fbedf6dbdb16c0d8bffca3a859a2f1db11fd4ae9834eeeb8e8c0c4212aef5970`

Inclusive released token-span width matches:
- word+punctuation = 42,419 / 48,833 = 86.8654%
- BERT pre-tokenizer = 42,242 / 48,833 = 86.5030%

Exclusive width matches only ~2.3-2.5%.

Absolute shifts vary inside:
- 501 / 523 articles for word+punctuation
- 502 / 523 articles for BERT pre-tokenizer

Decision:
`INCLUSIVE_WIDTH_STRUCTURE_SUPPORTED / SIMPLE_GLOBAL_OR_PER_ARTICLE_SHIFT_REJECTED`

## Official reproducibility gap

The SURUS publication/preprint says model code would be public and links:
`https://github.com/surus-ai/dataset`

Accessible official history contains dataset/manual/images/license but no training/tokenization/export/offset implementation.

Therefore:
`ORIGINAL_TOKEN_INDEX_EXPORT_IMPLEMENTATION_NOT_PUBLICLY_REPRODUCIBLE`

## Updated limited re-review packet

`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_SOURCE_CONTRACT_REREVIEW_PACKET_V2.md`

Packet commit:
`c10746398a590294716d9e3a65f00064873babaa`

Supersedes V1.

Allowed final verdicts remain:
1. `KEEP_SURUS_WITH_CHAR_COORDINATE_CONTRACT`
2. `KEEP_SURUS_WITH_OTHER_CHANGES`
3. `REJECT_OR_PAUSE_SURUS`

## Attempt / protected state

45 D0-D4 fits:
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

## Exact next authorized operation

`INDEPENDENT_HIGHER_MODEL_LIMITED_SURUS_SOURCE_CONTRACT_REREVIEW_V2`

No P2 adapter implementation before verdict freeze.

No scientific fit is authorized.

If higher-model access is temporarily unavailable, only non-decision technical work that cannot predetermine or weaken the source-contract verdict is allowed.

## Authority rule

This file is navigation only.

Immutable scientific freezes and completed GitHub Actions evidence override it if conflict exists.

Every new chat must search for newer durable branch evidence before mutation/retry.
