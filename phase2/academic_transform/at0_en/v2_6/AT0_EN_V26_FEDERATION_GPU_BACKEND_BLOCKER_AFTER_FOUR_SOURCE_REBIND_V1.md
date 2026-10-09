# ACAD_PASS — GPU Backend Blocker After Four-Source Rebind V1

Date: 2026-10-10
Timezone: Asia/Baghdad (UTC+3)

State:
`FOUR_SOURCE_PREFIT_REBIND_PASS / REAL_GPU_BACKEND_NOT_YET_QUALIFIED / NO_SCIENTIFIC_FIT`

## Completed immediately before this blocker

Final SURUS source-contract verdict:
`REJECT_OR_PAUSE_SURUS`

Four-source rebind preflight:
- run `37996135012`
- conclusion `SUCCESS`
- artifact `11646239459`
- digest `sha256:d21a392d61be7de48c4591b450d8ade8b18c598f50b885d92cd8f4be3d58ee64`

Binding manifest:
`AT0_EN_V26_FEDERATION_FOUR_SOURCE_PREFIT_BINDING_MANIFEST_V2.json`

Active attempts:
`45 / 45 NOT_STARTED / UNCONSUMED / UNAUTHORIZED`

## Required GPU gate

Workflow:
`.github/workflows/federation_gpu_qualification.yml`

Required runner labels:
`self-hosted, linux, x64, gpu, acad-pass-federation`

Qualification mode:
1. gradient checkpointing OFF first;
2. only if OFF fails specifically from GPU OOM, ON may be tried once before any scientific fit;
3. freeze first passing mode;
4. if neither passes, reject that backend.

No CPU fallback is authorized.

## Current observable evidence

GitHub Actions history on branch `at0-en-v2.6-dev` was queried after the four-source rebind.

Observed completed/queued runs named:
`Federation GPU qualification`

Count:
`0`

Therefore no durable workflow evidence currently establishes a qualified GPU backend.

The available connector does not expose the repository self-hosted-runner inventory endpoint, so absence of a registered runner cannot be asserted categorically from inventory.

The evidence-safe conclusion is:
`NO_QUALIFIED_GPU_BACKEND_IS_DURABLY_ESTABLISHED`

## What must be frozen by a passing qualification

- exact torch build suffix;
- CUDA runtime/toolkit;
- cuDNN;
- GPU model/VRAM;
- precision mode from frozen hardware rule;
- physical microbatch;
- gradient accumulation;
- worker count;
- TF32 policy;
- CUBLAS_WORKSPACE_CONFIG;
- checkpoint filesystem/persistence;
- exact model revision/weight hashes;
- synthetic full-length forward/backward memory results.

## Execution boundary

Do NOT:
- start D0-D4 scientific training;
- start PICOX scientific training;
- run on ordinary GitHub CPU to bypass qualification;
- change model/training protocol to fit inadequate hardware;
- open VERIFY_INTERNAL;
- score AD/COVID.

## Exact next operation

`CONNECT_OR_IDENTIFY_REAL_SELF_HOSTED_GPU_RUNNER -> RUN_GPU_QUALIFICATION_OFF -> FREEZE_PASS_OR_OOM_RESULT`

Only after a PASS:
`BIND_GPU_RUNTIME_HASH_TO_SAME_45_ATTEMPT_IDS -> FINAL_INDEPENDENT_PREFIT_REVIEW`

No scientific job before final independent pre-fit PASS.
