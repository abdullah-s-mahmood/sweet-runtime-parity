# ACAD_PASS — DISTANT-CTO Official File Audit and D5 Cancellation Freeze V1

Date: 2026-10-09

State:
`DISTANT_CTO_OFFICIAL_FILE_AUDIT_PASS / D5_CANCELED_BEFORE_FIT`

Canonical run:
`37885235969`

Artifact:
`11596332070`

Artifact digest:
`sha256:5373e7ee64977b2dcd157d2a181ca35024e5c07f5ccb77e63b98d2da5d09373e`

Official Zenodo record:
`10.5281/zenodo.6497284`

Official file:
`extraction1_pos_posnegtrail_conf09.txt`

Published MD5 verified:
`e95e3984a9b46e340b90aeed262e12cc`

Computed file SHA256:
`256150be8ac46bcf88ae016a37c3d5013e443b79bddc4f96eb6c960a5f59e764`

Bytes:
`360187585`

## Official-file findings

- JSON records: 106,889
- unique NCT IDs: 106,889
- malformed JSON lines: 0
- aggregate annotation token total: 17,953,786
- aggregate positive token total: 864,683
- `extraction1` entries: 0
- `intervention_type` count: 0
- semantic intervention-type supervision available: FALSE

Aggregate annotation fields observed:
- brief_summary_annot: 76,944
- brief_title_annot: 57,090
- detailed_description_annot: 48,120
- intervention_description_annot: 59,594
- official_title_annot: 64,043

The official confidence>=0.9 Zenodo file is a large weak binary Intervention resource, but it does NOT expose the eleven semantic `intervention_type` labels required by the prospectively frozen D5 design.

## Protocol consequence

The frozen federation protocol explicitly required:
- exactly 11 released weak semantic intervention types for D5;
- cancellation of D5 before fitting if that inventory cannot be resolved;
- no replacement arm.

Therefore:

`D5_11_WAY_WEAK_SEMANTIC_HEAD_CANCELED_WITHOUT_REPLACEMENT`

No D5 scientific fit has started.
No D5 slot is consumed.

Development campaign becomes:
- D0
- D1
- D2
- D3
- D4

Seeds:
44,45,46

Folds:
0,1,2

Maximum development fits:
`5 * 3 * 3 = 45`

The nine former D5 slots are permanently:
`CANCELED_NO_OFFICIAL_SEMANTIC_TYPE_LABELS`

They MUST NOT be repurposed to:
- binary DISTANT-CTO weak supervision;
- another weak dataset;
- another architecture;
- another hyperparameter;
- extra seed;
- extra fold.

DISTANT-CTO may remain literature/method evidence, but it is not used in the first federation campaign after this cancellation unless a separately reviewed future campaign authorizes a new hypothesis.

No successor training is authorized by this freeze.
