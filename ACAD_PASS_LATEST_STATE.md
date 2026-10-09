# ACAD_PASS — LATEST STATE POINTER

Timestamp: 2026-10-09 13:15:49 Asia/Baghdad (UTC+3)

Current active branch:
`at0-en-v2.6-dev`

Branch HEAD immediately before this pointer update:
`00ef0c61012ca89fc92c171330a585440bf4b25d`

Permanent cross-chat bootstrap contract:
`ACAD_PASS_BOOTSTRAP_CONTRACT.md`

## Latest authoritative checkpoint

`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_FEDERATION_PROGRESS_SNAPSHOT_V6.md`

Checkpoint commit:
`d897973c26cd657b21d1cc93451c7fd407c0544d`

## Governing review/amendment

Final SURUS admission review:
`phase2/academic_transform/at0_en/v2_6/FINAL_SURUS_ADMISSION_REVIEW_V1.md`

Verdict:
`PROCEED_WITH_CHANGES`

Frozen amendment:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_ADMISSION_PROTOCOL_AMENDMENT_V2.md`

Amendment state:
`GO_FOR_BOUNDED_AMENDMENT / NO_SCIENTIFIC_FIT`

## Current scientific state

`SURUS_AMENDMENT_V2_FROZEN / P1_NOT_CLOSED / LIMITED_SOURCE_CONTRACT_REREVIEW_REQUIRED / NO_SUCCESSOR_SCIENTIFIC_FIT`

Current process readiness:
- mandatory F01-F06 closure: **87.83%**
- first-fit readiness: **73.2%**

Current scientific performance:
unchanged; latest real model evidence remains frozen R44C.

## P1 authoritative lineage

Corrected schema/coordinate audit:
- run `37914385700`
- conclusion `FAIL`
- classification `MECHANICAL_PREFLIGHT_FAIL / NO_SCIENTIFIC_ATTEMPT`
- 25 LabelIDs / 7 ClassIDs correctly preserved
- 44,643 / 48,833 exact raw Abstract half-open rows
- 4,190 initial mismatch rows

Diagnostic V1:
- run `37914600126` SUCCESS
- artifact `11609690713`
- digest `sha256:02c42a9e2439f555636c611875c4c7b5a055bdb8f6e93b4d2052d9dc95c1873b`

Diagnostic V2:
- run `37914932110` SUCCESS
- artifact `11608697424`
- digest `sha256:69c688f51996eda49cbb09175f5adcede785efcf99ef0d1fca50f97b46f76d83`
- 437 / 523 articles partially affected
- 0 fully mismatched

Diagnostic V3:
- run `37915291868` SUCCESS
- artifact `11609721783`
- digest `sha256:901c7691556e57f521c589d123312f1a8f078928aa20bfaa37106a67b9872b80`
- 3,060 / 4,190 mismatch rows explained by fixed punctuation/token-spacing mechanics
- 1,130 remain unexplained

Pinned tokenizer diagnostic V4:
- run `37915950311` SUCCESS
- artifact `11608843740`
- digest `sha256:bdd936769d8eaa4abe87d699925a950e4aa2d9aeff2cc1f327a869a57be8a081`
- tokenizer `microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract@d673b8835373c6fa116d6d8006b33d48734e305d`
- tokenizer signature `088f1bdf2509aee48015c38209b07bebec8d4d266232e04c5d9bd82704b76e81`
- 48,640 / 48,833 Start/End spans align exactly to frozen tokenizer boundaries = 99.6048%
- released TokenStart/TokenEnd do NOT globally match this tokenizer under any fixed tested index convention
- best fixed char agreement = 2,209 / 48,833

Latest P1 freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_PINNED_TOKEN_ALIGNMENT_DIAGNOSTIC_FREEZE_V4.md`

## Official reproducibility gap

The SURUS paper links `https://github.com/surus-ai/dataset` as the location of full code/dataset/manual.

Accessible repository history contains dataset/manual/images/license but no training/tokenization/export/offset implementation.

Therefore exact original TokenStart/TokenEnd and Annotation.Text export semantics are not reproducible from the linked official code release.

## Prepared limited re-review

Packet:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_SOURCE_CONTRACT_REREVIEW_PACKET_V1.md`

Packet commit:
`41a8fe976f41f237dd9aa7989e01a2467d2f854e`

Only decision requested:
1. `KEEP_SURUS_WITH_CHAR_COORDINATE_CONTRACT`
2. `KEEP_SURUS_WITH_OTHER_CHANGES`
3. `REJECT_OR_PAUSE_SURUS`

No general protocol reopening.

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
`NOT AUTHORIZED`

R44C:
`FROZEN / CONSUMED / NOT_RERUN`

## Exact next authorized operation

`INDEPENDENT_HIGHER_MODEL_LIMITED_SURUS_SOURCE_CONTRACT_REREVIEW`

No P2 adapter work begins before this verdict is frozen.

No scientific fit is authorized.

## Authority rule

This file is navigation only.

Immutable scientific freezes and completed GitHub Actions evidence override it if conflict exists.

Every new chat must search for newer durable branch evidence before mutation/retry.
