# ACAD_PASS — AT0-EN V2.1 Execution Backend Amendment

Date: 2026-10-03
Status: FROZEN AMENDMENT
Supersedes only the access/backend clauses of AT0-EN V2. All other cases, arms, fixtures, invariants, stop rules and evidence requirements remain unchanged.

## Decision

Commercial API access is NOT required for AT0-EN.

Replace the previous access requirement with:

> Two distinct real model configurations, authorized for use, with auditable execution and bounded resources.

The preferred backend is frozen open-weight inference on an available local or GitHub Actions environment. The two models must be genuinely distinct model families/configurations; a second quantization or decoding setting of the same model is not an independent model.

AT0-EN remains:
- 12 frozen English cases;
- 2 frozen model identities;
- DIRECT and PLANNED arms;
- 48 slots;
- nominal maximum 72 logical generations;
- no best-of-N, regeneration for quality, model judge, detector loop, training or fine-tuning.

## Evidence requirements for open-weight execution

For each frozen model record:
- upstream repository and exact revision;
- license;
- model family and parameter scale;
- exact weight artifact filename;
- weight SHA-256;
- tokenizer/chat-template provenance;
- quantization type and conversion repository/revision;
- runtime and exact runtime version/commit;
- generation settings;
- execution OS, CPU/RAM, precision/quantization;
- start/end timestamps and elapsed time;
- prompt/output token counts where the runtime exposes them;
- additional monetary cost (zero is allowed);
- raw request/prompt and raw output.

Replay of a stored output is not new inference.

## Resource policy

Additional monetary budget may be exactly USD 0.00 when execution uses already-available/free resources.

Bound resources instead by:
- maximum 72 logical generations;
- one model loaded/executed at a time;
- no parallel model jobs;
- fixed context/output limits;
- GitHub Actions job/runtime limits;
- disk/RAM preflight;
- no purchase of GPU/API/credits without explicit user authorization.

## GitHub Actions backend

A standard public-repository `ubuntu-24.04` runner is permitted if current GitHub-hosted runner availability is confirmed. The workflow must execute strictly sequentially:
1. checkout/frozen-input validation;
2. 30/30 affected/offline tests;
3. environment/resource manifest;
4. model A download/hash verification/inference;
5. delete/unload model A artifacts if required for resource bounds;
6. model B download/hash verification/inference;
7. final diagnostics and evidence packaging.

No matrix strategy or concurrent jobs are allowed.

## F07 invariant

`authorized_scope` originates from the frozen pre-generation case/permission record. A model proposal may neither widen nor replace it. The existing F07 repair is accepted and retained.

## Plus/Work fallback

Outputs obtained through a ChatGPT subscription UI may be preserved as observed evidence only when needed, with visible model identity/date/context recorded and reproducibility limits stated. Manual UI outputs do not establish automated backend integration and do not add extra cells to the 48-slot matrix unless a future frozen amendment explicitly defines them.

## Current authorization

The implementation agent is authorized to:
- research model suitability/licensing/resource fit;
- freeze two suitable open-weight model configurations before viewing live results;
- implement/test the backend;
- execute the existing 48-slot matrix on already-available/free compute if all frozen resource and identity checks pass.

The implementation agent is NOT authorized to:
- buy API/GPU/credits;
- change the 12 cases, 2-model count, arms or scientific comparison;
- start HW1-EN or DR;
- resume Arabic research;
- open reserved data.

Return to higher-model review after AT0-EN completion or an early-escalation condition.
