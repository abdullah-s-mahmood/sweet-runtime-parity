# MP-SEF P2_V2 STAGE1 SOURCE-ONLY RESULT LOCK V1

Date: 2026-10-01
Status: FROZEN / SOURCE-ONLY STAGE1 COMPLETE
Gold/reference use: NONE
Quality claim: NONE

## Workflow evidence

Workflow:
`Phase 2 MP-SEF P2 V2 Stage1 Source-Only`

Run:
`36872617551`

Head SHA:
`5a25d3396b8d27cbd553b386f6ed64537c2b658a`

Conclusion:
`SUCCESS`

Artifact:
- id: `11168548251`
- name: `mpsef-p2-v2-stage1-v1`
- ZIP digest:
  `sha256:050d376b98ecf0b0be2c9ff49610d1d67834fa4f0839b02ab344f828f6d82ce9`

## Frozen Stage1 input

Packet SHA256:
`8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1`

Cases:
128

Clusters:
128

## Execution result

Watchdog work units:
- completed: 152 / 152
- percent: 100%
- final status: COMPLETE

Proposal rows:
- OK: 127 / 128 = 99.21875%
- TRUNCATED_OR_LENGTH_UNPROVEN: 1 / 128 = 0.78125%
- empty outputs: 0
- generation-ceiling count among successful summary rows: 0
- changed vs source: 126 / 128 = 98.4375%

Important:
`changed_vs_source` is activity, NOT correctness.

## Determinism / provenance

Fixed parity subset:
8 UIDs

- repeat parity: 8 / 8
- reversed-order parity: 8 / 8

True model-call batch path:
not implemented in frozen V1.

Recorded value:
`NOT_APPLICABLE_SINGLE_CASE_MODEL_CALL_IMPLEMENTATION`

No batch PASS is claimed.

## Runtime/resource

Main 128-case proposal pass:
- total: 581.313 s (~9.69 min)
- mean: 4.540 s/case
- median: 4.536 s/case
- p95 nearest-rank: 5.535 s/case
- peak RSS: 2,629,320 KiB (~2.51 GiB)

The full monitored workflow also included model/runtime setup and 24 parity inference operations.

## Single non-executable row

UID:
`train:12118`

Reason:
`GEC_EOS_AT_GENERATION_CEILING_FAIL_CLOSED`

Classification:
`CAPACITY / GENERATION-COMPLETENESS BOUNDARY`

Repairability:
`FIXABLE_NEXT_VERSION_ONLY`

Triage:
`MPSEF_P2_V2_STAGE1_GENERATION_CEILING_FAILURE_TRIAGE_V1.md`

The row remains present and contributes no executable P2_V2 action.

No max_length change is allowed inside V1.

## Data/metric boundary

- source_only: true
- project source: frozen Stage1 128 only
- gold_reference_consulted: false
- project_gold_loaded: false
- quality_metric_computed: false
- R_joint_computed: false
- selector_trained: false
- quality_claimed: false

## Interpretation

P2_V2 Stage1 engineering/provenance outcome:
**STRONGLY SUPPORTED**

Linguistic correction quality:
**UNKNOWN / NOT MEASURED**

What improved:
- the repaired heterogeneous P2 route now executes on real project source;
- 127/128 rows are executable;
- identity/provenance determinism holds on the frozen parity subset;
- one length-boundary row fails closed rather than silently truncating.

What remains risky:
- 98.44% output activity is high and may imply useful correction, over-correction, or both;
- no quality conclusion is possible before authorized evaluation;
- legal/protected availability has not yet been compared against P1/P3;
- one long-input capacity boundary exists.

## Next

Generate P3 source-only outputs on the same exact packet using exact registered P1 parent outputs, then build source-only legal/dedup/diversity diagnostics across P1/P2_V2/P3.
