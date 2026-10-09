# ACAD_PASS — Federation Training-Loop Checkpoint/Resume Synthetic Freeze V1

Date: 2026-10-09

State:
`FEDERATION_TRAINING_LOOP_CHECKPOINT_RESUME_SYNTHETIC_PASS`

Run:
`37899033856`

Artifact:
`11601174540`

Digest:
`sha256:69338da5e92c2eb9ea4d2ef6694763b7802a4a3a7826969579aa4efc64a37f89`

Scientific data used:
`FALSE`

Scientific encoder loaded:
`FALSE`

Scientific training performed:
`FALSE`

## Frozen mechanics verified

Optimizer:
- AdamW
- encoder LR 2e-5
- head LR 1e-4
- betas (0.9, 0.999)
- eps 1e-8
- weight decay 0.01 except no-decay groups
- gradient clip 1.0

Scheduler:
- 10% linear warmup
- linear decay
- scientific total-update formula:
  `20 * ceil(N_native_train / 8)`

Effective native batch:
`8`

Synthetic resume fixture:
- microbatch 2
- accumulation 4
- 12 optimizer steps
- interruption after optimizer step 5

## Exact resume result

Uninterrupted final model hash:
`efce80dbfb7c28507b55fa722f3e4bddd2814c517f16ffa1b0827bc3a490fdc9`

Resumed final model hash:
same.

Uninterrupted optimizer hash:
`eb108b6d9843754aa4db457657110b7200f89311713dfe48aa1fcc04a50ccdb3`

Resumed optimizer hash:
same.

Also exact:
- scheduler state;
- loss trace;
- LR trace;
- final counters.

Checkpoint files:
- `model.safetensors`
- `training_state.pt`
- `manifest.json`

Tamper/hash guard:
PASS.

## Interpretation

A byte/parameter-equivalent resume path exists for the frozen training mechanics.

GPU-specific microbatch and accumulation remain to be bound during hardware qualification while preserving effective batch 8.

A resumed job is a continuation only when:
- checkpoint manifest hashes verify;
- optimizer/scheduler/RNG state is restored;
- data manifest and runtime manifest are unchanged;
- attempt ID is unchanged.

Otherwise it is a new attempt and is unauthorized beyond the frozen budget.

This PASS consumes no scientific attempt.
