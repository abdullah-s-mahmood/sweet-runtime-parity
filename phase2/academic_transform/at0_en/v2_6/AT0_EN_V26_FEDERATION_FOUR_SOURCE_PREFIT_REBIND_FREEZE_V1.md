# ACAD_PASS — Four-Source Prefit Rebind Freeze V1

Date: 2026-10-10
Timezone: Asia/Baghdad (UTC+3)

State:
`PASS_FOUR_SOURCE_PREFIT_REBIND / GPU_QUALIFICATION_PENDING / NO_SCIENTIFIC_FIT`

## Authority

Final SURUS source-contract verdict:
`REJECT_OR_PAUSE_SURUS`

Canonical review:
`FINAL_SURUS_SOURCE_CONTRACT_REREVIEW_V2.md`

Four-source reversion:
`AT0_EN_V26_SURUS_PAUSE_FOUR_SOURCE_REVERSION_FREEZE_V1.md`

Sampler contract:
`AT0_EN_V26_FEDERATION_FOUR_SOURCE_SAMPLER_CONTRACT_V1.json`

## Preflight evidence

Workflow:
`Federation four-source prefit rebind preflight`

Run:
`37996135012`

Head:
`68a78c9ab30ee6800d14a08e18a64b634d4c3de1`

Conclusion:
`SUCCESS`

Artifact:
`11646239459`

Artifact digest:
`sha256:d21a392d61be7de48c4591b450d8ade8b18c598f50b885d92cd8f4be3d58ee64`

Classification:
`NON_SCIENTIFIC_PREFIT_BINDING / NO_ATTEMPT_CONSUMED`

## Frozen four-source execution binding

Active auxiliary sources:
1. EBM
2. TrialSieve
3. EvidenceOutcomes
4. PICO

SURUS:
`PAUSED_NOT_ADMITTED_CURRENT_CAMPAIGN`

Auxiliary documents/update:
`8`

Documents/source/update:
`2`

Allocation:
`2/2/2/2`

Total auxiliary coefficient:
`0.25`

Effective coefficient/source:
`0.0625`

Loss:
`L_aux = mean(L_EBM, L_TrialSieve, L_EvidenceOutcomes, L_PICO)`

`L = L_native + 0.25 * L_aux`

## Attempt identity

Active D0-D4 attempts:
`45`

All active attempts:
`NOT_STARTED / UNCONSUMED / scientific_training_authorized=false`

Active attempt-ID digest:
`sha256:79128f31a9d712a782be7173b8419be5503d56d13be34e20d595ecf32e6c6673`

D5:
- canceled slots = 9
- consumed = 0
- no replacement

## Data binding

Fold 0:
`7c79f752c38f30a7b4f220c5ab3ff7db3ec559baa1c80797f13b65833203e0b0`

Fold 1:
`1955fa751bb90960af10fcdae40fabe3ae36c06602b4aa00ad74aec9c6466e02`

Fold 2:
`eb28ffdc603f6e0df7a42e216909aa0540b52772008a843fca31cb0f815cb939`

Evidence:
- run `37897592120`
- artifact `11601066403`

These were rebound, not regenerated.

## File SHA256 binding from preflight

- adapter contract: `12b16ed2fcfc6ca3a902c40cd7d638340055f48bde55b51d95b72c2fa63240dc`
- architecture preflight: `5f668fcc54efbb4f03b6a2553a8ebb7c1c85ce26e90184ede0fa5b024175fe1b`
- attempt manifest V1: `247be4eb17ea2fee09eb6d62b8559e5656b6c72e4d5c58490d5924b9929fcb7b`
- data custody freeze: `92c84a3542fa4dd758609eea3caddf313611d07a8eed0545b734810b8a4a5ca8`
- protocol V1: `11da22d5e254eeedc865315ca2eb78374c4b19208082172493ca6024630eb459`
- runtime contract V1: `1ffc2647fd36ca26744db0fe3fe002b40b5ab41569284a5354f64ee08906b08f`
- sampler contract V1: `2ca963700c09d593cb8285284a12e86c76af9e4880ad1ae5d30a535af5253bd2`
- source admission V1: `821cc3f1d2ca713b341cd2e255a7a1094ef65aacab48ef765289beaed973b587`
- source pin V1: `d6198e0bce428532bab91ccee16aa397703d38ebf79be5d4fd02387aca59a726`
- reversion freeze: `9f0e0c1e35f9b31eb1bd0356596695c4db02113444eadf3cf6e5a81a067ac211`

## Runtime state

Scientific software runtime:
frozen.

GPU-specific runtime:
`PENDING_GPU_QUALIFICATION`

Pending:
- exact torch build suffix;
- CUDA runtime/toolkit;
- cuDNN;
- GPU model and VRAM;
- mixed precision mode;
- gradient accumulation realization;
- worker count;
- TF32 policy;
- CUBLAS_WORKSPACE_CONFIG;
- checkpoint filesystem.

## Safety boundary

No:
- scientific training;
- protected data opening;
- VERIFY_INTERNAL;
- AD/COVID scoring;
- SURUS diagnostics;
- attempt consumption.

## Exact next operation

`CREATE_VERSIONED_ATTEMPT_REBIND_V2 -> RESUME_GPU_QUALIFICATION`

Final independent pre-fit review remains mandatory before the first scientific job.
