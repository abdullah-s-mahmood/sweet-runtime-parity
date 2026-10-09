# ACAD_PASS — Federation GPU Qualification Gate V1

State:
`READY_TO_RUN_WHEN_A_REAL_GPU_BACKEND_IS_CONNECTED / NOT_YET_EXECUTED`

This gate consumes no scientific data and no scientific attempt.

It requires a self-hosted GitHub runner with labels:
`self-hosted, linux, x64, gpu, acad-pass-federation`.

Qualification order:
1. run with gradient checkpointing OFF;
2. only if OFF fails from GPU-memory exhaustion, before any scientific fit, run once with checkpointing ON;
3. freeze the first passing mode;
4. if neither passes, reject that GPU backend.

The script:
- verifies canonical software versions;
- requires CUDA;
- downloads every scientific encoder at its exact full revision;
- verifies frozen weight SHA256;
- loads one model at a time;
- runs synthetic full-length forward/backward + AdamW step;
- records GPU, VRAM, CUDA, cuDNN, precision and peak memory;
- fixes physical microbatch=1;
- preserves native effective batch 8 through accumulation=8;
- preserves PICOX boundary effective batch 8 and span effective batch 16.

Hardware precision rule:
- BF16 if the qualified GPU reports native BF16 support;
- otherwise FP16.

No architecture/data/threshold change is allowed to make an inadequate GPU pass.

First scientific fit remains blocked until the resulting artifact is reviewed and frozen into the 45-attempt runtime bindings.
