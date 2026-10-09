# ACAD_PASS — Federation Progress Snapshot V6

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

State:
`SURUS_AMENDMENT_V2_FROZEN / P1_NOT_CLOSED / LIMITED_SOURCE_CONTRACT_REREVIEW_REQUIRED / NO_SUCCESSOR_SCIENTIFIC_FIT`

## Current readiness

Mandatory F01-F06 closure:
`87.83%`

First scientific-fit readiness:
`73.2%`

Change versus V5:
`0.0 percentage points`

Reason:
V4 added decisive source-contract evidence but did not close P1; no readiness credit is granted merely for more diagnostics.

These percentages remain PROCESS READINESS only.

## Latest P1 evidence — V4

Run:
`37915950311`

Conclusion:
`SUCCESS`

Artifact:
`11608843740`

Digest:
`sha256:bdd936769d8eaa4abe87d699925a950e4aa2d9aeff2cc1f327a869a57be8a081`

Pinned tokenizer:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract@d673b8835373c6fa116d6d8006b33d48734e305d`

Tokenizer signature:
`088f1bdf2509aee48015c38209b07bebec8d4d266232e04c5d9bd82704b76e81`

Result:
- 48,640 / 48,833 released Start/End character spans align to pinned tokenizer boundaries = 99.6048%;
- 193 / 48,833 do not = 0.3952%;
- released TokenStart/TokenEnd cannot be globally interpreted as indices of the pinned tokenizer;
- best fixed convention, ZERO_BASED_INCLUSIVE, reproduces released char bounds for only 2,209 / 48,833.

Therefore:
`PINNED_TOKENIZER_DOES_NOT_RECOVER_RELEASED_TOKENSTART_TOKENEND_SEMANTICS`

## Official reproducibility gap

The peer-reviewed SURUS paper states BERT tokenization/BILOU and says full NER code is available at the linked Git repository.

The paper links:
`https://github.com/surus-ai/dataset`.

Accessible repository history contains:
- LICENSE;
- README;
- annotation manual;
- released CSV files;
- images.

It contains no training/tokenization/export/offset implementation.

Therefore the exact original Annotation.Text and TokenStart/TokenEnd export semantics cannot currently be reconstructed from the official linked code source.

## Combined source-contract evidence

Released annotations:
`48,833`

Raw exact Annotation.Text == Abstract[Start:End]:
`44,643 = 91.4197%`

Raw mismatch:
`4,190 = 8.5803%`

Mismatch rows explained by fixed punctuation/token-spacing:
`3,060 / 4,190 = 73.0310%`

Residual Annotation.Text mismatch:
`1,130 / 48,833 = 2.3136%`

Character spans aligned to frozen biomedical tokenizer boundaries:
`48,640 / 48,833 = 99.6048%`

These facts strongly support structural coherence of Start/End while proving incomplete Text serialization reproducibility.

## Scientific boundary

The prior independent review made exact text/offset round-trip and positive representability mandatory.

Changing the rule so Start/End is authoritative while Annotation.Text becomes provenance metadata is a MATERIAL INTERPRETATION CHANGE.

The current assistant does not authorize that change unilaterally.

## Prepared limited re-review

Packet:
`AT0_EN_V26_SURUS_SOURCE_CONTRACT_REREVIEW_PACKET_V1.md`

Commit:
`41a8fe976f41f237dd9aa7989e01a2467d2f854e`

The re-review asks one bounded question only:
- keep SURUS using a prospectively frozen char-coordinate-authoritative contract;
- keep with other changes;
- or reject/pause SURUS.

## Scientific performance

No successor fit.

Latest actual model result remains frozen R44C at t=.95:
- macro precision = 0.8767348592080204
- P = 0.8918918918918919
- I = 0.8171091445427728
- C = 0.9318181818181818
- O = 0.8661202185792349

Performance change:
`NONE`

## Protected / attempt state

45 D0-D4 slots:
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
`FROZEN / CONSUMED`

## Exact next operation

`INDEPENDENT_HIGHER_MODEL_LIMITED_SURUS_SOURCE_CONTRACT_REREVIEW`

No P2 adapter work begins until this verdict is frozen.

No scientific fit is authorized.
