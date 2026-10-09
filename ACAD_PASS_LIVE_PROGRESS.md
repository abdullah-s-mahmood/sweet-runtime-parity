# ACAD_PASS — LIVE PROGRESS

Last updated: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)
Branch: `at0-en-v2.6-dev`

## CURRENT STATE

`SURUS_AMENDMENT_V2_FROZEN / LIMITED_HIGHER_MODEL_REREVIEW_INTERRUPTED_BEFORE_VERDICT / V5_V6_V7_COMPLETE / P1_SOURCE_CONTRACT_OPEN / NO_SUCCESSOR_SCIENTIFIC_FIT`

Execution:
`PAUSED AT GOVERNANCE BOUNDARY AFTER MAXIMAL NON-SCIENTIFIC SOURCE-SEMANTICS CLOSURE`

Scientific training:
`NOT_STARTED`

GO/NO-GO:
`NO-GO FOR SCIENTIFIC FIT`

## 1. PROCESS READINESS

Mandatory F01-F06 closure:
`87.83%`

First-fit readiness:
`73.2%`

Change vs prior checkpoint:
`0.0 percentage points`

Reason:
V5-V7 materially reduced uncertainty but P1 is still not scientifically closed.

These are process-readiness percentages, not model-performance metrics.

## 2. SCIENTIFIC PERFORMANCE

No successor model has been fit.

Latest actual model evidence remains R44C at t=.95:
- macro precision 87.6735%
- P 89.1892%
- I 81.7109%
- C 93.1818%
- O 86.6120%

Scientific-performance change:
`NONE`

## 3. HIGHER-MODEL STATUS

The limited SURUS source-contract rereview started and was interrupted by account usage limits BEFORE verdict.

Recovered concern:
WordPiece-boundary coherence alone does not prove compatibility with the frozen implementation's actual source-word segment unit.

No final verdict:
`NONE`

No durable higher-model repo mutation:
`NONE`

Freeze:
`AT0_EN_V26_SURUS_INTERRUPTED_SOURCE_CONTRACT_REVIEW_EVIDENCE_V1.md`

## 4. SOURCE-CONTRACT EVIDENCE

Released annotations:
`48,833`

Raw Text round-trip:
`44,643 = 91.4197%`

Raw mismatch:
`4,190`

Fixed punctuation/token-spacing explanation:
`3,060 / 4,190 = 73.0310%`

Residual Text mismatch:
`1,130 = 2.3136% of full release`

### V4 — frozen ACAD_PASS BiomedBERT
- run `37915950311`
- Start/End WordPiece-boundary alignment = 99.6048%
- TokenStart/TokenEnd not recoverable as BiomedBERT indices.

### V5 — source-paper bert-base-uncased
- run `37919107413`
- artifact `11611123584`
- digest `sha256:2d43434d6ecbd33e270a423d4e29300cd75d970353bc5e782f32bdeeaf6da51f`
- Start/End WordPiece-boundary alignment = 99.7666%
- best direct TokenStart/TokenEnd recovery = 279 / 48,833

Decision:
`DIRECT_BERT_WORDPIECE_INDEX_SEMANTICS_REJECTED`

### V6 — source units
- run `37919404071`
- artifact `11610764435`
- digest `sha256:0ec7e0dc73a1096b51d9702f9ffba69613b5d9ab47b91a2ea206e5c2e65fdb2e`

Start/End alignment:
- BERT pre-tokenizer = 98.9822%
- deterministic word+punctuation = 99.2833%
- whitespace = 56.5089%

Best absolute token-pair recovery:
- word+punctuation = 25.7715%
- BERT pre-tokenizer = 24.8910%

Decision:
`TOKENSTART_TOKENEND_NOT_GLOBAL_INDICES_OF_TESTED_SOURCE_UNITS`

### V7 — width / local shift
- run `37919734516`
- artifact `11611114778`
- digest `sha256:fbedf6dbdb16c0d8bffca3a859a2f1db11fd4ae9834eeeb8e8c0c4212aef5970`

Inclusive token-span width:
- word+punctuation = 86.8654%
- BERT pre-tokenizer = 86.5030%

Exclusive width:
~2.3-2.5%

Multiple absolute shifts within article:
- word+punctuation = 501 / 523 articles
- BERT pre-tokenizer = 502 / 523 articles

Decision:
`INCLUSIVE_WIDTH_STRUCTURE_SUPPORTED / SIMPLE_GLOBAL_OR_PER_ARTICLE_OFFSET_REJECTED`

## 5. IMPLEMENTATION IMPLICATION

Frozen ACAD_PASS mechanics operate on source-word representations built from subwords and preserve original-to-model offsets.

Therefore high WordPiece-boundary alignment is strong structural evidence but not sufficient to certify the required source-word representation for SURUS.

The public release does not provide reproducibly documented absolute token-index semantics.

TokenStart/TokenEnd MUST NOT be used to relocate or repair Start/End.

## 6. OFFICIAL REPRODUCIBILITY GAP

SURUS publication/preprint states model code would be public and links `surus-ai/dataset`.

Accessible official repository history contains dataset/manual/images/license but no training/tokenization/export/offset implementation.

## 7. UPDATED REREVIEW

Packet:
`AT0_EN_V26_SURUS_SOURCE_CONTRACT_REREVIEW_PACKET_V2.md`

Allowed verdicts:
- KEEP_SURUS_WITH_CHAR_COORDINATE_CONTRACT
- KEEP_SURUS_WITH_OTHER_CHANGES
- REJECT_OR_PAUSE_SURUS

No broad admission review restart is required.

## 8. PROTECTED / ATTEMPT STATE

45 D0-D4:
`NOT_STARTED / UNCONSUMED`

D5:
`CANCELED WITHOUT REPLACEMENT`

VERIFY_INTERNAL:
`CLOSED`

AD/COVID external scoring:
`CLOSED`

SURUS OOD scoring:
`NOT_AUTHORIZED`

R44C:
`FROZEN / CONSUMED`

## 9. EXACT NEXT OPERATION

`INDEPENDENT_HIGHER_MODEL_LIMITED_SURUS_SOURCE_CONTRACT_REREVIEW_V2`

Until higher-model access returns:
only non-decision technical work that cannot predetermine or weaken this verdict is permitted.

No P2 adapter implementation.
No scientific fit.

## 10. CROSS-CHAT CONTINUITY

Permanent contract:
`ACAD_PASS_BOOTSTRAP_CONTRACT.md`

The reusable user bootstrap prompt remains unchanged.

New chats:
`DISCOVER -> VERIFY -> LATEST_STATE -> SEARCH NEWER EVIDENCE -> CONTINUE`.
