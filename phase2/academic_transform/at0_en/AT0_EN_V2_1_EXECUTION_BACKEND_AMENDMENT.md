# ACAD_PASS — AT0-EN V2.1 Execution Backend Amendment

Date: 2026-10-03  
Status: FROZEN EXECUTION AMENDMENT  
Scope: execution backend only; no change to AT0-EN scientific matrix, cases, arms, fixtures, or success claims.

## 1. Superseded access requirement

V2 required two distinct authorized commercial/API model identities plus a positive monetary API ceiling. That requirement is replaced by:

> **Two distinct real model configurations, authorized for use, with auditable execution and bounded resources.**

Commercial APIs are not required. Real inference may run from frozen open weights locally or in GitHub Actions. A paid API may still be used later only if separately authorized; it is not the default path.

## 2. Scientific scope remains unchanged

The frozen matrix remains:
- 12 English synthetic cases;
- 2 distinct model configurations;
- DIRECT and PLANNED arms;
- 48 slots total;
- maximum 72 logical generation requests;
- no best-of-N, judge, automatic repair, detector call, Arabic generation, training, or fine-tuning;
- same cases, prompts, protection constraints, length policy and F07 authorized-scope invariant.

AT0-EN remains an engineering/transformation-feasibility slice. Its completion cannot establish human-writing quality, scientific-fidelity maturity, detector robustness, voice quality, document fidelity, or commercial usefulness.

## 3. Backend preference

Preferred order:
1. frozen public open-weight models executed reproducibly on existing GitHub Actions resources;
2. another already-authorized local/reproducible environment;
3. ChatGPT Plus/Work only as an explicitly documented observation-limited path if reproducible model execution cannot be established.

Do not purchase API access, GPU, credits or additional compute without explicit user authorization.

## 4. Frozen open-weight configurations

The model identities below are frozen before AT0-EN evaluation outputs are seen.

### Model A — Qwen family

- base model: `Qwen/Qwen3-4B-Instruct-2507`
- observed upstream revision: `e7974da369bd887ad4f10a072ec4f933ac5391bf`
- executable GGUF repository: `bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF`
- executable repository revision: `d3037fec123e6fcf1b894f42ff01bd83d4622955`
- artifact: `Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf`
- artifact SHA-256: `2fde00ce69dd4899c70d020845e2638353015bba0fdf161b3eb965f2bca4464e`
- artifact size: approximately 2.5 GB
- quantization: Q4_K_M
- license: Apache-2.0
- intended role: English instruction-following academic rewrite/planning

### Model B — SmolLM family

- base model: `HuggingFaceTB/SmolLM3-3B`
- observed upstream revision: `c8598251715c17cb277a6ff01523b7703925b9c8`
- executable GGUF repository: `ggml-org/SmolLM3-3B-GGUF`
- executable repository revision: `4965cb60b150737b68a0408c36aeefb65078f894`
- artifact: `SmolLM3-Q4_K_M.gguf`
- artifact SHA-256: `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`
- artifact size: 1,915,305,312 bytes
- quantization: Q4_K_M
- license: Apache-2.0
- intended role: English instruction-following academic rewrite/planning

These are distinct model families, not different quantizations or decoding settings of one model. Their AT0-EN role is feasibility diversity, not proof of state-of-the-art English academic writing.

## 5. Frozen runtime and execution environment

Runtime:
- `llama.cpp`
- repository: `ggml-org/llama.cpp`
- frozen commit: `b92761a515ea31e852e7fbc1fad5f874b46f3718`
- CPU backend
- strictly sequential execution, one model resident at a time and one generation request at a time

Target environment:
- repository: `abdullah-s-mahmood/sweet-runtime-parity` (public);
- GitHub-hosted runner: `ubuntu-24.04`;
- expected public-repository runner resources at freeze time: 4 CPU, 16 GB RAM, 14 GB SSD;
- no GPU requirement;
- additional monetary spend ceiling: `USD 0`;
- bounded by workflow timeout, 48 slots and 72 logical requests.

Record the actual runner image, CPU, memory, free disk, Python version, llama.cpp commit/version, artifact hashes, wall-clock duration and available token/resource measurements at execution time.

## 6. Required smoke gate before full live matrix

Before executing the 48-slot matrix:
1. rerun the 30 frozen offline fixtures and preserve F07 behavior;
2. acquire Model A at its pinned revision and verify the expected SHA-256;
3. run exactly one fixed non-evaluation smoke prompt proving inference, instruction-following and mechanically capturable structured output;
4. unload/remove Model A if required for resource isolation;
5. acquire Model B at its pinned revision and verify the expected SHA-256;
6. run the same non-evaluation smoke prompt;
7. unload/remove Model B if required;
8. record runtime/resources and decide only whether each backend is mechanically usable.

The smoke prompt must not be one of EN01–EN12 and must not be used to tune prompts, decoding, model choice or thresholds. If either model cannot perform the required structured response sufficiently to begin the frozen matrix, stop and return `MODEL_RESOURCE_OR_CAPABILITY_BLOCKER`; do not silently replace it.

## 7. Frozen generation settings

Use:
- temperature: 0.0;
- seed: 20261003;
- context window: 4096 tokens;
- maximum generated tokens: DIRECT 800, PLAN 400, REALIZE 800;
- concurrency: 1;
- no automatic retry for malformed/refused/poor output;
- at most one transport retry only when an unambiguous infrastructure failure occurred and the original request did not complete.

If a model's embedded chat template requires a non-semantic runtime flag, record it. Do not change prompts, sampling, quantization, chat-template policy or model identities after seeing evaluation outputs.

## 8. Reproducibility classes

Open-weight frozen execution: `REPRODUCIBLE_FROZEN_WEIGHTS` when artifact hash, runtime revision, embedded template behavior and generation settings are captured.

ChatGPT Plus/Work observation: `OBSERVED_SUBSCRIPTION_LIMITED_REPRODUCIBILITY` unless an exact model snapshot/runtime identity and repeatable programmatic interface are available. Such observation does not substitute for automated harness integration.

## 9. Stop conditions

Stop before or during live generation if:
- artifact hash/revision differs;
- model/runtime identity cannot be recorded;
- a model cannot run within available resources;
- structured output cannot be mechanically captured in the smoke test;
- source/scope/protected-data invariant fails;
- runner resource exhaustion threatens artifact preservation;
- a model silently changes or is substituted;
- a change to cases, arms, sample size, protection gate or scientific meaning would be required.

No reduction of the matrix or silent model replacement is authorized.

## 10. Return gate

After the full matrix closes, return the normal HIGHER-MODEL REVIEW PACKET plus:
- backend identity and reproducibility class;
- exact weight hashes/revisions;
- llama.cpp/runtime identity;
- actual runner resources;
- per-model/arm generation counts and failures;
- wall-clock time and token/resource measurements when available;
- additional monetary cost;
- limitations attributable to small open models.

Do not start HW1-EN or DR automatically.
