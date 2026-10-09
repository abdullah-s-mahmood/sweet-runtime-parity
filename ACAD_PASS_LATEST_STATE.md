# ACAD_PASS — LATEST STATE POINTER

Timestamp: 2026-10-10 01:02 Asia/Baghdad (UTC+3)

Current active branch:
`at0-en-v2.6-dev`

Branch HEAD immediately before this pointer update:
`8db3dbde89db9328cf9c6b771d90c01f0ac9b1f3`

Permanent cross-chat bootstrap contract:
`ACAD_PASS_BOOTSTRAP_CONTRACT.md`

## Latest authoritative checkpoint

`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_FEDERATION_PROGRESS_SNAPSHOT_V8.md`

Snapshot commit:
`f69dba5be61cdff068973cabba4a910da8556ccd`

## Current scientific state

`SURUS_PAUSED_CURRENT_CAMPAIGN / FOUR_SOURCE_PREFIT_REBIND_PASS / GPU_BACKEND_AND_FINAL_PREFIT_REVIEW_PENDING / NO_SUCCESSOR_SCIENTIFIC_FIT`

Process readiness:
- mandatory F01-F06 closure: **94.5%**
- first-fit readiness: **89.7%**

These are process-readiness values, not model-performance values.

Scientific performance:
unchanged; latest actual model evidence remains frozen R44C.

## Final SURUS source-contract decision

Canonical review:
`phase2/academic_transform/at0_en/v2_6/FINAL_SURUS_SOURCE_CONTRACT_REREVIEW_V2.md`

Verdict:
`REJECT_OR_PAUSE_SURUS`

Current-campaign consequence:
`PAUSE_SURUS / USE_ORIGINAL_FOUR_SOURCE_FALLBACK`

SURUS V1-V7 evidence remains frozen and preserved.

The five-source SURUS Amendment V2 remains historical evidence but is:
`NON_EXECUTING_FOR_CURRENT_CAMPAIGN`

No replacement auxiliary source is authorized.

## Review evidence integrity

Uploaded final-review SHA256:
`3bc60c5c0ef42a13982fd65a346c674c57471c25252f7df4320ac79d3b29ffd5`

Uploaded evidence ZIP SHA256:
`c6f9fe664ab1ad65d7fc6b80d29ccbc4fcd3a61011be16f746e28158677f7e45`

Evidence ZIP internal manifest:
`41 / 41 verified / 0 mismatches`

Verification file:
`phase2/academic_transform/at0_en/v2_6/FINAL_SURUS_SOURCE_CONTRACT_REREVIEW_V2_EVIDENCE_VERIFICATION_V1.json`

## Four-source reversion and rebind

Reversion freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_PAUSE_FOUR_SOURCE_REVERSION_FREEZE_V1.md`

Sampler contract:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_FEDERATION_FOUR_SOURCE_SAMPLER_CONTRACT_V1.json`

Rebind preflight:
- run `37996135012`
- conclusion `SUCCESS`
- artifact `11646239459`
- digest `sha256:d21a392d61be7de48c4591b450d8ade8b18c598f50b885d92cd8f4be3d58ee64`
- state `PASS_FOUR_SOURCE_PREFIT_REBIND`

Rebind freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_FEDERATION_FOUR_SOURCE_PREFIT_REBIND_FREEZE_V1.md`

Comprehensive binding manifest:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_FEDERATION_FOUR_SOURCE_PREFIT_BINDING_MANIFEST_V2.json`

## Active four-source mechanics

Auxiliary sources:
1. EBM
2. TrialSieve
3. EvidenceOutcomes
4. PICO

Auxiliary documents/update:
`8 = 2/2/2/2`

Loss:
`L_aux = (L_EBM + L_TrialSieve + L_EvidenceOutcomes + L_PICO) / 4`

`L = L_native + 0.25 * L_aux`

Effective total-loss coefficient/source:
`0.0625`

## Attempts

Active D0-D4:
`45`

Attempt-ID digest:
`sha256:79128f31a9d712a782be7173b8419be5503d56d13be34e20d595ecf32e6c6673`

All active attempts:
`NOT_STARTED / UNCONSUMED / scientific_training_authorized=false`

D5:
`9 CANCELED_NO_OFFICIAL_SEMANTIC_TYPE_LABELS / 0 CONSUMED / NO REPLACEMENT`

## Data binding

Fold 0:
`7c79f752c38f30a7b4f220c5ab3ff7db3ec559baa1c80797f13b65833203e0b0`

Fold 1:
`1955fa751bb90960af10fcdae40fabe3ae36c06602b4aa00ad74aec9c6466e02`

Fold 2:
`eb28ffdc603f6e0df7a42e216909aa0540b52772008a843fca31cb0f815cb939`

Custody evidence:
- run `37897592120`
- artifact `11601066403`

No data regeneration was performed for the SURUS pause.

## GPU/runtime blocker

Blocker freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_FEDERATION_GPU_BACKEND_BLOCKER_AFTER_FOUR_SOURCE_REBIND_V1.md`

Qualification workflow:
`.github/workflows/federation_gpu_qualification.yml`

Required self-hosted runner labels:
`self-hosted, linux, x64, gpu, acad-pass-federation`

Observed durable GPU qualification runs:
`0`

Safe status:
`NO_QUALIFIED_GPU_BACKEND_IS_DURABLY_ESTABLISHED`

GPU-specific runtime binding:
`PENDING_GPU_QUALIFICATION`

## Protected / historical state

VERIFY_INTERNAL:
`CLOSED`

AD/COVID external scoring:
`CLOSED`

SURUS OOD scoring:
`NOT_AUTHORIZED`

R44C:
`FROZEN / CONSUMED / NOT_RERUN`

## Exact next authorized operation

`CONNECT_OR_IDENTIFY_REAL_SELF_HOSTED_GPU_RUNNER -> RUN_GPU_QUALIFICATION_OFF -> FREEZE_PASS_OR_OOM_RESULT`

If OFF passes:
`BIND_GPU_RUNTIME_HASH_TO_SAME_45_ATTEMPTS -> FINAL_INDEPENDENT_PREFIT_REVIEW`

If OFF OOMs:
one ON qualification may be attempted before any scientific fit, then freeze the first passing mode.

No CPU bypass.

No scientific fit before:
`FINAL_INDEPENDENT_PREFIT_REVIEW = PASS`

## Authority rule

This file is navigation only.

Immutable scientific freezes and completed Actions artifacts override it if conflict exists.

Every new chat must:
`DISCOVER -> VERIFY -> LATEST_STATE -> SEARCH NEWER EVIDENCE -> CONTINUE`
before mutation or retry.
