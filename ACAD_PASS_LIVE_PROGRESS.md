# ACAD_PASS — LIVE PROGRESS

Last updated: 2026-10-10
Timezone: Asia/Baghdad (UTC+3)
Branch: `at0-en-v2.6-dev`

## CURRENT STATE

`SURUS_PAUSED_CURRENT_CAMPAIGN / FOUR_SOURCE_PREFIT_REBIND_PASS / GPU_BACKEND_AND_FINAL_PREFIT_REVIEW_PENDING / NO_SUCCESSOR_SCIENTIFIC_FIT`

Scientific training:
`NOT_STARTED`

GO/NO-GO:
`NO-GO FOR SCIENTIFIC FIT UNTIL GPU QUALIFICATION + FINAL INDEPENDENT PREFIT PASS`

## 1. PROCESS READINESS

Mandatory F01-F06 closure:
`94.5%`

First-fit readiness:
`89.7%`

Change vs V7:
- F01-F06: `+6.67 pp`
- first-fit readiness: `+16.5 pp`

Reason:
SURUS was independently paused and the already-qualified original four-source campaign was rebound successfully.

This is process readiness, NOT model accuracy.

## 2. SCIENTIFIC PERFORMANCE

Latest actual model evidence remains frozen R44C at t=.95:
- macro precision 87.6735%
- P 89.1892%
- I 81.7109%
- C 93.1818%
- O 86.6120%

No successor fit.
No performance change.

## 3. FINAL SURUS DECISION

Review:
`FINAL_SURUS_SOURCE_CONTRACT_REREVIEW_V2.md`

Verdict:
`REJECT_OR_PAUSE_SURUS`

Current-campaign action:
`PAUSE_SURUS_AND_USE_FOUR_SOURCE_FALLBACK`

SURUS V1-V7 evidence remains frozen.
Five-source Amendment V2 remains historical/non-executing.

No replacement source is authorized.

## 4. FOUR-SOURCE REBIND

Preflight:
- run `37996135012`
- conclusion `SUCCESS`
- artifact `11646239459`
- digest `sha256:d21a392d61be7de48c4591b450d8ade8b18c598f50b885d92cd8f4be3d58ee64`

Binding:
`PASS_FOUR_SOURCE_PREFIT_REBIND`

Active auxiliary sources:
- EBM
- TrialSieve
- EvidenceOutcomes
- PICO

Auxiliary batch:
`8 total = 2/2/2/2`

Loss:
`L_aux = mean(four source losses)`
`L = L_native + 0.25 * L_aux`

Effective source coefficient:
`0.0625 each`

Binding manifest:
`AT0_EN_V26_FEDERATION_FOUR_SOURCE_PREFIT_BINDING_MANIFEST_V2.json`

## 5. ATTEMPT / DATA STATE

Active D0-D4 attempts:
`45`

Attempt-ID digest:
`sha256:79128f31a9d712a782be7173b8419be5503d56d13be34e20d595ecf32e6c6673`

All:
`NOT_STARTED / UNCONSUMED / UNAUTHORIZED`

D5:
`9 CANCELED / 0 CONSUMED / NO REPLACEMENT`

Per-fold data manifest hashes remain:
- F0 `7c79f752c38f30a7b4f220c5ab3ff7db3ec559baa1c80797f13b65833203e0b0`
- F1 `1955fa751bb90960af10fcdae40fabe3ae36c06602b4aa00ad74aec9c6466e02`
- F2 `eb28ffdc603f6e0df7a42e216909aa0540b52772008a843fca31cb0f815cb939`

No data regeneration was performed.

## 6. GPU BLOCKER

GPU gate:
`AT0_EN_V26_FEDERATION_GPU_QUALIFICATION_GATE_V1.md`

Required self-hosted runner labels:
`self-hosted, linux, x64, gpu, acad-pass-federation`

Durable GPU-qualification runs observed:
`0`

Current evidence-safe status:
`NO_QUALIFIED_GPU_BACKEND_IS_DURABLY_ESTABLISHED`

GPU runtime hash:
`PENDING_GPU_QUALIFICATION`

No CPU fallback is authorized.

## 7. PROTECTED STATE

VERIFY_INTERNAL:
`CLOSED`

AD/COVID external scoring:
`CLOSED`

SURUS OOD scoring:
`NOT AUTHORIZED`

R44C:
`FROZEN / CONSUMED`

## 8. EXACT NEXT OPERATION

`CONNECT_OR_IDENTIFY_REAL_SELF_HOSTED_GPU_RUNNER -> RUN_GPU_QUALIFICATION_OFF -> FREEZE_PASS_OR_OOM_RESULT`

Then, only after GPU PASS:
`BIND_GPU_RUNTIME_HASH_TO_SAME_45_ATTEMPTS -> FINAL_INDEPENDENT_PREFIT_REVIEW`

STOP before the first scientific job until final independent pre-fit PASS.

## 9. CROSS-CHAT CONTINUITY

Permanent contract:
`ACAD_PASS_BOOTSTRAP_CONTRACT.md`

Reusable user bootstrap prompt remains unchanged.

New chats:
`DISCOVER -> VERIFY -> LATEST_STATE -> SEARCH NEWER EVIDENCE -> CONTINUE`.
