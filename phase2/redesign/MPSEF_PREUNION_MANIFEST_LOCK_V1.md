# MP-SEF PRE-UNION MANIFEST LOCK V1

Date: 2026-09-30
Status: FROZEN PASS
No candidate feasibility metric computed.

## Workflow

Run:
36761718922

Job:
110045678462

Conclusion:
SUCCESS

Artifact:
- id: 11119695370
- name: mpsef-preunion-manifests-v1
- digest: sha256:1163b37d2c0b50f8a1f6f804e3c012928f1bc3a894c7cb0d87cbffd66196b712

## Frozen CALIBRATION input

Artifact:
m2h-calibration-v1

Source run:
36654588477

Source artifact:
11070819539

Artifact digest:
sha256:ab5f303b4405162684d9a8ece23c0ed378b25e7863129a284f3e65ca0844058a

Observed extracted JSONL SHA256:
2442c84d0b7683f12ae9c82f2ab8d7d2fd118cac3a3fc29e26cfc94657066c00

## Preflight result

Status:
PASS

Counts:
- total records: 6,888
- original train: 6,571
- original dev: 317
- total clusters: 6,871
- non-singleton clusters: 15
- maximum cluster size: 4
- near-duplicate edges: 20
- dev clusters: 317
- train/dev crossing clusters: 0

Primary feasibility population:
D_DEV_FEAS_V1

- records: 317
- clusters: 317
- original split: dev
- training-origin records: 0
- independence status: DEVELOPMENTAL_NOT_INDEPENDENT

Train-origin internal population:
D_TRAIN_INTERNAL_V1

- records: 6,571
- clusters: 6,554
- primary feasibility use allowed: false

## Exposure result

All 6,888 records:
- gold_exposed: true
- aggregate_result_exposed: true
- independence_claim_allowed: false

Training-overlap status:
- KNOWN_OR_HIGHLY_EXPECTED_DIRECT_TRAIN_OVERLAP: 6,571
- MODEL_DEVELOPMENT_EVALUATION_EXPOSURE: 317

Unknown fine-grained historical exposure:
- 6,888 records conservatively marked unknown_exposure=true.

## Integrity

- candidate_metric_computed: false
- reference_content_used_for_manifest_generation: false
- gold_edit_content_used_for_manifest_generation: false
- INTERNAL_EVALUATION opened: false
- STRESS_DIAGNOSTIC opened: false
- reserved data opened: false
- D_DEV_FEAS_V1 / D_TRAIN_INTERNAL_V1 cluster overlap: 0

## Frozen file hashes

MPSEF_CLUSTER_MAP_SUMMARY_V1.json
4072ca5d3f296b81cdf53031c0f09cf66856b2e8e06601026734933ab19b0b94

MPSEF_CLUSTER_MAP_V1.jsonl
eca4509ab5c2714530c1f12333f9ddcfb08f372a681b07bc0e8574edaa22b2ba

MPSEF_EXPOSURE_LEDGER_SUMMARY_V1.json
d1dd5fc63c446f22b75595acef0de531ca4165c67aedf8dd5aceaf10a092b6c0

MPSEF_EXPOSURE_LEDGER_V1.jsonl
ab88fae0a83aa02cf7b54cf7a3bcaa9c656fb2efb8ada27d43fd4c767385058c

MPSEF_FEASIBILITY_POPULATION_SUMMARY_V1.json
d73021cb1a83bf1e7a4e4ec722f092461aec4c86364513b9bc6ecf31c865364a

MPSEF_FEASIBILITY_POPULATION_V1.jsonl
f9ee85a110f36db6c47da33902b6af9c0ec8db597c11ee0d5cb7da28d2f091a1

MPSEF_NEAR_DUPLICATE_EDGES_V1.jsonl
c1a77ce747ee45866c691e8efab3cec51f655e7e4e89f45c3800b790bf024d64

MPSEF_PRE_UNION_MANIFEST_PREFLIGHT_V1.json
c06b7500dfe5bc8fa6c16d487be6b726e98bd4d556bcafebc99cbb15a2bfef6c

MPSEF_TRAIN_INTERNAL_POPULATION_SUMMARY_V1.json
68bec66caaa8ffd3a2fc680bd960379a3a769bc4c4ac98fdb616fb9108b33378

MPSEF_TRAIN_INTERNAL_POPULATION_V1.jsonl
9778246367eb12801ceefe19256741032b3ae81c486b6bf39f2a67bed5378d90

Generator SHA256:
a79e0bfc0c73a9cf92ea342103cc4d4b357363ba61da049e212ba576be1f0d5d

## Decision

Pre-union manifests:
**PASS / FROZEN**

This does not authorize candidate feasibility measurement by itself.

The active protocol is:
- MPSEF_PRE_UNION_PROTOCOL_V3.md
- plus MPSEF_PRE_UNION_PROTOCOL_V3_TRAINING_OVERLAP_AMENDMENT_V1.md

Primary future feasibility population:
D_DEV_FEAS_V1 only.

The result, if later authorized, must be labeled:
DEVELOPMENTAL / DEV-ORIGIN / NOT INDEPENDENT.
