# MP-SEF P3_V1 STAGE1 INPUT/MODEL IDENTITY LOCK V1

Date: 2026-10-01
Status: FROZEN BEFORE P3 STAGE1 INFERENCE
Gold/reference use: NONE

## P1 parent artifact

Artifact run:
`36765798233`

Artifact id:
`11123050529`

Artifact ZIP digest:
`sha256:e4020418ca2f2793d4bb79bc766e26838398fb9affba6d0f1c704255cd5aed46`

Proposal file:
`MPSEF_P1_CF_PROPOSALS_V1.jsonl`

Proposal file SHA256:
`2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`

P1 model revision:
`21286e56ce98a86362db540863f91c083b8970f9`

P1 model weight SHA256:
`9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d`

P1 upstream text-editing revision:
`4d552ca3ae98029550f27fc52aa1b22883e16e61`

P3 Stage-A policy:
**reuse exact frozen P1 final output; do not rerun P1.**

For every Stage1 UID:
`P3_input_sha256 == P1_output_sha256`

Any mismatch:
`P3_PARENT_OUTPUT_IDENTITY_MISMATCH`

## Frozen P3 Pnx model identity

Identity workflow:
`Phase 2 MP-SEF P3 Pnx Identity Freeze`

Run:
`36875641902`

Head SHA:
`d94598df939652822709d6bf0928cf41d69c1ee3`

Artifact:
- id: `11169281022`
- digest:
  `sha256:e436e888be5cfa3e443d5472a0c59749f532255dd5abf2c80c8b33549bb30900`

Model repository:
`CAMeL-Lab/text-editing-qalb14-pnx`

Resolved model revision:
`a162d77269ab6ff556d2c58c5dff8b967c1f649e`

Weight SHA256:
`d98d683f9ef1738c27f5031c99483d93e9f73c4116c158a97a678270c84fd262`

Config SHA256:
`2b65052e89f8a44585e3618febf7b65593db109e475f7569ac5d4a96799350f0`

id2label SHA256:
`ae37aed7eb13151a0d016458c1dba78d58359355b030b4a12d607598cf1b5559`

label2id SHA256:
`76e16654e3d567b9d9226f94198dc5786fbd7d569fd2213558912ceb1580ff35`

Tokenizer:
`BertTokenizer`

Model class:
`BertForTokenClassification`

Vocabulary size:
64000

Labels:
35

## Frozen Stage1 packet

Packet SHA256:
`8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1`

UID list SHA256:
`e32b468f27653a1bbabfa5c355483c34ffe9b6e4cb2425c36e6c10b714c104ac`

Cases:
128

Clusters:
128

## P3 Stage1 execution rule

For each frozen packet row:

1. find exact P1 parent row by UID;
2. verify source SHA identity between packet and P1 row;
3. verify P1 output SHA against its stored output;
4. set P3 Stage-B input to exact P1 full_proposer_output;
5. run exactly one Pnx text-editing decode pass;
6. preserve original source separately for final source->P3 protection/legalization;
7. never treat P1/P3 as independent architecture-family votes.

## Scientific boundary

This lock authorizes only source-only P3 Stage1 inference.

It does not authorize:
- correctness measurement;
- R_joint;
- gold/reference access;
- selector training;
- consensus scoring.
