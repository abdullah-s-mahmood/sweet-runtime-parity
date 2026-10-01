# MP-SEF P3_V1 STAGE1 SOURCE-ONLY RESULT LOCK V1

Date: 2026-10-01
Status: FROZEN / SOURCE-ONLY STAGE1 COMPLETE
Gold/reference use: NONE
Quality claim: NONE

## Workflow evidence

Workflow:
`Phase 2 MP-SEF P3 V1 Stage1 Source-Only`

Successful run:
`36877195995`

Head SHA:
`1822b56de8437d1148e4493274daa7be18d797ed`

Conclusion:
`SUCCESS`

Artifact:
- id: `11169788003`
- digest:
  `sha256:57dc36332f24df3e3bf09367f8ca0a1a99e998dd4c6939fe6bc7bbbb3093ab5e`

## Historical failed attempt

Run:
`36876431628`

Failure:
runtime dependency parity defect before first inference.

Inference progress:
`0/144 = 0%`

Root cause:
missing `datasets` plus NumPy/PyTorch compatibility mismatch relative to the already proven frozen P1 environment.

Triage:
`MPSEF_P3_V1_STAGE1_RUNTIME_FAILURE_TRIAGE_V1.md`

Repair:
restore exact additional P1 runtime dependencies.

Repair commit:
`1822b56de8437d1148e4493274daa7be18d797ed`

## Input/model identity

Stage1 packet SHA:
`8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1`

Frozen P1 parent proposal SHA:
`2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`

Pnx revision:
`a162d77269ab6ff556d2c58c5dff8b967c1f649e`

Pnx weight SHA:
`d98d683f9ef1738c27f5031c99483d93e9f73c4116c158a97a678270c84fd262`

P1 rerun:
false

Exact frozen P1 parent reused:
true

## Execution result

Monitored work:
- 144 / 144
- 100%
- final watchdog status: COMPLETE

Proposal rows:
- execution OK: 128 / 128 = 100%
- execution failures: 0
- identical to P1: 6 / 128 = 4.6875%
- changed from P1: 122 / 128 = 95.3125%

Stage-B source-only change-domain counts relative to P1:
- MIXED_FROM_P1: 118 / 128 = 92.1875%
- PUNCTUATION_ONLY_FROM_P1: 4 / 128 = 3.125%
- NO_CHANGE_FROM_P1: 6 / 128 = 4.6875%

These are change-domain/activity diagnostics, not correctness.

## Determinism

True batch-vs-single parity:
- n = 8
- match = 8 / 8

Batch size:
32

## Runtime/resource

Main 128-case batched Pnx pass:
- total: 22.186 s
- allocated mean: 0.1573 s/case
- allocated median: 0.1570 s/case
- allocated p95 nearest-rank: 0.1665 s/case
- peak RSS: 1,358,032 KiB (~1.30 GiB)

## Data/metric boundary

- project source: frozen Stage1 128 only
- gold_reference_consulted: false
- project_gold_loaded: false
- quality_metric_computed: false
- R_joint_computed: false
- selector_trained: false
- quality_claimed: false

## Interpretation

P3 engineering/provenance outcome:
**STRONGLY SUPPORTED**

P3 linguistic value:
**UNKNOWN / NOT MEASURED**

Important architecture signal:
P3 is not behaving as a punctuation-only micro-extension on this packet. The majority of outputs differ from P1 in a MIXED change domain under the frozen source-only classifier.

This increases the importance of:
- whole-output protection;
- legal candidate filtering;
- exact-output dedup;
- family-aware interpretation;
- P3 marginal legal contribution analysis.

It does not establish over-correction or poor quality.

## Next

Run the frozen source-only V4 action/legal/dedup/diversity analysis over:
- P1 frozen outputs for the same 128 UIDs;
- P2_V2 Stage1 outputs;
- P3_V1 Stage1 outputs.

No gold/reference is permitted.
