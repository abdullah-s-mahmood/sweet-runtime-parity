# ACAD_PASS — Federation Progress Snapshot V8

Date: 2026-10-10
Timezone: Asia/Baghdad (UTC+3)

State:
`SURUS_PAUSED_CURRENT_CAMPAIGN / FOUR_SOURCE_PREFIT_REBIND_PASS / GPU_BACKEND_AND_FINAL_PREFIT_REVIEW_PENDING / NO_SUCCESSOR_SCIENTIFIC_FIT`

## 1. Independent SURUS verdict

Final review:
`FINAL_SURUS_SOURCE_CONTRACT_REREVIEW_V2.md`

Verdict:
`REJECT_OR_PAUSE_SURUS`

Current-campaign action:
`PAUSE_SURUS_AND_USE_ORIGINAL_FOUR_SOURCE_FALLBACK`

No completed scientific evidence was invalidated or consumed.

SURUS V1-V7 evidence remains frozen.

Five-source Amendment V2 remains historical/non-executing and is not deleted.

## 2. Four-source rebind status

Reversion freeze:
`AT0_EN_V26_SURUS_PAUSE_FOUR_SOURCE_REVERSION_FREEZE_V1.md`

Sampler contract:
`AT0_EN_V26_FEDERATION_FOUR_SOURCE_SAMPLER_CONTRACT_V1.json`

Rebind preflight:
- run `37996135012`
- SUCCESS
- artifact `11646239459`
- digest `sha256:d21a392d61be7de48c4591b450d8ade8b18c598f50b885d92cd8f4be3d58ee64`

Rebind freeze:
`AT0_EN_V26_FEDERATION_FOUR_SOURCE_PREFIT_REBIND_FREEZE_V1.md`

Binding manifest:
`AT0_EN_V26_FEDERATION_FOUR_SOURCE_PREFIT_BINDING_MANIFEST_V2.json`

Result:
`PASS_FOUR_SOURCE_PREFIT_REBIND`

## 3. Restored four-source mechanics

Auxiliary sources:
1. EBM
2. TrialSieve
3. EvidenceOutcomes
4. PICO

Auxiliary documents/optimizer update:
`8`

Allocation:
`2/2/2/2`

Auxiliary loss:
`L_aux = (L_EBM + L_TrialSieve + L_EvidenceOutcomes + L_PICO) / 4`

Total:
`L = L_native + 0.25 * L_aux`

Effective coefficient/source:
`0.0625`

No SURUS term.
No replacement source.
No coefficient sweep.

## 4. Attempt continuity

Active D0-D4 attempts:
`45`

Active attempt-ID digest:
`sha256:79128f31a9d712a782be7173b8419be5503d56d13be34e20d595ecf32e6c6673`

All 45:
`NOT_STARTED / UNCONSUMED / scientific_training_authorized=false`

D5:
`9 CANCELED / 0 CONSUMED / NO REPLACEMENT`

## 5. Data binding

Fold 0:
`7c79f752c38f30a7b4f220c5ab3ff7db3ec559baa1c80797f13b65833203e0b0`

Fold 1:
`1955fa751bb90960af10fcdae40fabe3ae36c06602b4aa00ad74aec9c6466e02`

Fold 2:
`eb28ffdc603f6e0df7a42e216909aa0540b52772008a843fca31cb0f815cb939`

Existing custody evidence retained:
- run `37897592120`
- artifact `11601066403`

No data regeneration was performed merely because SURUS was paused.

## 6. Process readiness restored to original four-source track

Mandatory F01-F06 closure:
`94.5%`

Components:
- F01 exposure/protected custody = 90
- F02 weak-role semantics = 100
- F03 gold-independent preprocessing = 95
- F04 benchmark eligibility/provenance = 82
- F05 incompatible-comparator handling = 100
- F06 finite first campaign = 100

Arithmetic:
`94.5%`

First scientific development-fit readiness:
`89.7%`

Components:
1. source identity/ontology/research-use/split = 90
2. alias/trial-family graph = 80
3. protected custody = 85
4. external benchmark eligibility = 82
5. gold-independent preprocessing = 95
6. adapters/architecture mechanics = 95
7. strict scorer/aggregation = 95
8. comparator recipe/mechanics = 95
9. software/runtime/checkpoint mechanics = 85
10. attempt/data/runtime binding = 95

Arithmetic:
`89.7%`

Change from V7 five-source-amendment blocked state:
- F01-F06: `+6.67 percentage points`
- first-fit readiness: `+16.5 percentage points`

Interpretation:
This is NOT model improvement.
It is restoration of the already-qualified simpler four-source campaign after the optional SURUS amendment was independently paused.

## 7. Scientific performance

No successor fit has started.

Latest actual model evidence remains frozen R44C at t=.95:
- macro precision = 0.8767348592080204
- P = 0.8918918918918919
- I = 0.8171091445427728
- C = 0.9318181818181818
- O = 0.8661202185792349

Scientific performance delta:
`NONE`

## 8. GPU/runtime blocker

GPU blocker:
`AT0_EN_V26_FEDERATION_GPU_BACKEND_BLOCKER_AFTER_FOUR_SOURCE_REBIND_V1.md`

Required workflow:
`Federation GPU qualification`

Required runner labels:
`self-hosted, linux, x64, gpu, acad-pass-federation`

Current durable qualification runs observed:
`0`

Safe conclusion:
`NO_QUALIFIED_GPU_BACKEND_IS_DURABLY_ESTABLISHED`

GPU-specific runtime hash remains:
`PENDING_GPU_QUALIFICATION`

## 9. Protected / attempt state

VERIFY_INTERNAL:
`CLOSED`

AD/COVID external scoring:
`CLOSED`

SURUS OOD scoring:
`NOT_AUTHORIZED`

R44C:
`FROZEN / CONSUMED / NOT_RERUN`

45 D0-D4:
`NOT_STARTED / UNCONSUMED`

## 10. Exact next operation

`CONNECT_OR_IDENTIFY_REAL_SELF_HOSTED_GPU_RUNNER -> RUN_GPU_QUALIFICATION_OFF -> FREEZE_PASS_OR_OOM_RESULT`

If OFF passes:
`BIND_GPU_RUNTIME_HASH_TO_SAME_45_ATTEMPTS -> FINAL_INDEPENDENT_PREFIT_REVIEW`

If OFF fails specifically by GPU OOM:
one ON qualification may be run before any scientific fit, then first passing mode is frozen.

If no qualified GPU backend:
`NO_FIRST_FIT`

Even after GPU PASS:
STOP before scientific training until the final independent pre-fit review returns PASS.
