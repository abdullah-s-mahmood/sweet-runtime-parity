# MP-SEF P3_V1 STAGE2 PRODUCTION-BOUND REPLAY CLOSURE LOCK V1

Date: 2026-10-01
Status: PASS / P3 PRODUCTION-BOUND REPLAY CLOSED
Gold/reference use: NONE
Full-C_F execution: NOT STARTED

## Unit preflight

Run: `36897040255`
Result: SUCCESS / 5/5 PASS

Artifact:
- id: `11179319008`
- digest: `sha256:5e374f7558c074df731ee0ba3b10d5cab6a94728eb74448de623556e172197ff`

Validated:
- exact P1 parent identity;
- P3 input bound to frozen P1 output;
- bad parent output hash fails closed;
- missing parent fails closed;
- durable append order.

## Production-bound Parity32

Run: `36897419883`
Result: SUCCESS

All production executions used:
`mpsef_p3_v1_stage2_production_adapter_v1.py`
under:
`run_with_progress_watchdog_v2.py`

Comparisons:
- single_vs_batch = 32/32
- batch_vs_reversed = 32/32
- batch_vs_repeat = 32/32
- batch_vs_frozen_trace = 32/32
- batch_output_vs_frozen_output = 32/32
- parent_identity = 32/32

Production adapter CLI used: true
P1 rerun: false
Exact frozen P1 parent reused: true

Artifact:
- id: `11180560530`
- digest: `sha256:67a271032ccd7bef0614634dd01b1b1292eb98799d81f2c57fea9b6aeb331c8c`

Frozen identities:
- Parity32 manifest SHA:
  `384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e`
- P1 proposal SHA:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- P3 Stage1 frozen proposal SHA:
  `69720287154071611a0e0d0af2a6689ef6ed5242acf374fb945de70013a16083`
- Pnx weight SHA:
  `d98d683f9ef1738c27f5031c99483d93e9f73c4116c158a97a678270c84fd262`
- Pnx config SHA:
  `2b65052e89f8a44585e3618febf7b65593db109e475f7569ac5d4a96799350f0`
- Pnx revision:
  `a162d77269ab6ff556d2c58c5dff8b967c1f649e`

## Interpretation

P3 production-path replay requirement:
**PASS / CLOSED**

This proves production-path determinism/parent binding for the frozen 32, not linguistic quality.

Any semantic change to P3 adapter/runtime/model/classifier/parent identity invalidates this lock and requires replay before full-C_F execution.
