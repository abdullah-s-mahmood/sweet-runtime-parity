# MP-SEF P2_V2 B01 STAGE0 CLOSURE LOCK V1

Date: 2026-10-01
Status: PASS / SOURCE-FREE STAGE0
Gold/reference use: NONE
Project source use: NONE

## Scope

Closes the implementation-validation portion of independent-review BLOCKER B01 for P2_V2.

This lock combines:
1. synthetic identity/provenance boundary tests;
2. real-model source-free inference using the frozen GED/GEC models.

It does NOT establish linguistic correctness.

## Synthetic identity Stage0

Workflow:
`Phase 2 MP-SEF P2 V2 Identity Stage0`

Run:
`36863549449`

Head SHA:
`87624fd0f1c62176aab79a7c6bfff0e57574e3f0`

Result:
- status: PASS
- tests: 20 / 20 PASS
- project_source_loaded: false
- project_gold_loaded: false
- project_metric_computed: false
- model_inference_run: false

Artifact:
- id: `11162862266`
- digest:
  `sha256:c6a875b7880db119ea660ea84a47c250f49f624d610b4849419e2fd5aa5893e8`

Covered synthetic classes include:
- zero GED/GEC token words;
- exact/over GED segment budget;
- whole-word segmentation;
- duplicate/missing/reordered word identity;
- equal-count wrong assignment;
- label-name remapping;
- GEC conditioning length mismatch;
- GED tags consumed vs ignored;
- decoder prefix==EOS semantics;
- forced EOS at ceiling;
- repeat byte identity;
- missing terminal EOS.

## Initial real-model failure

Historical run:
`36864163724`

Head SHA:
`976d31d5de310a18bbff2a4d15e6d0f32981234b`

Result:
FAIL before model inference.

Root cause:
non-standard assumption that `BertTokenizerFast` exposes `cls_token_type_id`.

Classification:
`IMPLEMENTATION / RUNTIME INTERFACE`

Failure triage:
`MPSEF_P2_V2_REAL_MODEL_STAGE0_FAILURE_TRIAGE_V1.md`

Historical failed artifact:
- id: `11162703948`
- digest:
  `sha256:72ad108428a88822903bafebaacc0300323e8b7404eaf35c074820c82ff0d6d6`

Repair commit:
`fe49ac916d7534b7178a3f0a87092da8b0dccad5`

Repair:
single-sequence BERT token_type_ids are explicit zeroes; segment-field lengths are asserted.

## Real-model Stage0 after repair

Workflow:
`Phase 2 MP-SEF P2 V2 Real Model Stage0`

Run:
`36868057043`

Head SHA:
`fe49ac916d7534b7178a3f0a87092da8b0dccad5`

Result:
PASS

Summary:
- record_id: `MPSEF_P2_V2_REAL_MODEL_STAGE0_V1`
- synthetic/public sources: 3
- repeat_parity_first_source: true
- project_source_loaded: false
- project_gold_loaded: false
- project_metric_computed: false
- real_model_inference_run: true
- quality_claimed: false

Frozen model weight identities:
- GED:
  `23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f`
- GEC:
  `5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f`

Artifact:
- id: `11165486137`
- digest:
  `sha256:9cdb16ad4f3606b2af158e296a7e59e24f3718aec18d8cbc174acfa4a2d50918`

## Interpretation

B01 implementation validation:
**PASS AT SOURCE-FREE STAGE0**

The original universal P2_V1 GED word-alignment provenance defect is no longer present in the tested P2_V2 Stage0 path.

This does NOT prove:
- P2_V2 is linguistically better;
- P2_V2 improves candidate availability;
- P2_V2 should be retained after Stage1/Stage2;
- any project metric.

## Remaining prerequisites before Stage1

- B02 registry/action-set builder synthetic PASS;
- M01 P3 parent/role synthetic PASS;
- M03 shadow protection synthetic PASS;
- canonical Stage0 summary PASS;
- deterministic Stage1 packet frozen;
- no gold/reference access.
