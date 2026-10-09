# ACAD_PASS — Federation Compute Backend Readiness V1

Date: 2026-10-09

State:
`GPU_EXECUTION_BACKEND_UNESTABLISHED / HARDWARE_INDEPENDENT_CLOSURE_CONTINUES`

Scientific training:
`NOT_AUTHORIZED`

## Repository ownership

Repository:
`abdullah-s-mahmood/sweet-runtime-parity`

GitHub owner type:
`User`

Visibility:
`public`

## GitHub-hosted GPU finding

Current GitHub documentation states that GPU-powered larger runners are part of GitHub larger runners.

Larger runners are available only to organizations/enterprises using GitHub Team or GitHub Enterprise Cloud.

This repository is currently user-owned rather than organization-owned.

Therefore:
`GITHUB_HOSTED_GPU_AVAILABILITY_NOT_ESTABLISHED_FOR_THIS_REPOSITORY`

Do NOT schedule D0-D5 scientific full-encoder fine-tuning onto ordinary `ubuntu-24.04` CPU runners merely because preflights use them successfully.

## Self-hosted GPU path

GitHub Actions supports self-hosted runners with labels such as:
`[self-hosted, linux, x64, gpu]`.

This is an admissible execution architecture only after a real runner is registered and a hardware qualification workflow proves:
- NVIDIA/CUDA availability;
- sufficient VRAM;
- stable local disk;
- deterministic software stack;
- network/model-cache availability;
- checkpoint persistence;
- resume semantics.

No self-hosted GPU is currently established.

## Scientific runtime requirements not yet frozen

Pending GPU-backend closure:
- PyTorch build;
- CUDA toolkit/runtime;
- cuDNN;
- GPU model/VRAM;
- mixed-precision mode;
- gradient accumulation;
- worker count;
- deterministic algorithm flags;
- TF32 policy;
- CUDA/CUBLAS deterministic environment;
- checkpoint filesystem.

These cannot be selected after scientific result visibility.

## CPU-safe work remains authorized

Allowed on standard GitHub runners:
- source/provenance audits;
- adapter validation;
- tokenizer/config identity;
- model-file metadata hashing;
- strict scorer tests;
- split/family manifest creation;
- synthetic architecture forward/backward closure on tiny randomly initialized fixtures;
- attempt-ledger generation.

Forbidden on standard CPU solely to bypass GPU closure:
- beginning any D0-D5 scientific training attempt;
- beginning PICOX scientific training;
- changing model/training budget because CPU execution is slow.

## Next compute checkpoint

Before the first scientific fit create:

`AT0_EN_V26_FEDERATION_GPU_RUNTIME_QUALIFICATION_PASS_V1.md`

with the exact:
- runner identity/class;
- hardware;
- CUDA/PyTorch/Transformers versions;
- determinism flags;
- mixed precision;
- per-arm batch/accumulation realization;
- storage/cache policy;
- checkpoint/resume contract.

Until then:
`NO_FIRST_FIT`.


## 2026-10-09 qualification gate prepared

A fail-closed GPU qualification package now exists:
- `federation_gpu_qualification.py`
- `.github/workflows/federation_gpu_qualification.yml`
- `AT0_EN_V26_FEDERATION_GPU_QUALIFICATION_GATE_V1.md`

It is intentionally NOT auto-triggered.

Required runner labels:
`self-hosted, linux, x64, gpu, acad-pass-federation`.

A real GPU backend is still NOT established.

The gate verifies:
- canonical software versions;
- CUDA/cuDNN/GPU/VRAM;
- exact model revisions and weight SHA256;
- synthetic full-length forward/backward;
- peak memory;
- deterministic settings;
- microbatch 1;
- effective-batch-preserving accumulation.

No CPU fallback is authorized for scientific fitting.
