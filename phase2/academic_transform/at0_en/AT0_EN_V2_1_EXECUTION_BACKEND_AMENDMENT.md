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

## 4. Selected open-weight candidates for resource smoke test

The implementation agent selects the following candidates before results are seen:

### Model A — Qwen family

- model: Qwen3-1.7B
- GGUF repository: `ggml-org/Qwen3-1.7B-GGUF`
- repository revision: `daeb8e2d528a760970442092f6bf1e55c3b659eb`
- artifact: `Qwen3-1.7B-Q4_K_M.gguf`
- artifact SHA-256: `d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5`
- artifact size: 1,282,439,264 bytes
- quantization: Q4_K_M
- license: Apache-2.0
- source: https://huggingface.co/ggml-org/Qwen3-1.7B-GGUF

### Model B — SmolLM family

- model: SmolLM3-3B
- GGUF repository: `ggml-org/SmolLM3-3B-GGUF`
- repository revision: `4965cb60b150737b68a0408c36aeefb65078f894`
- artifact: `SmolLM3-Q4_K_M.gguf`
- artifact SHA-256: `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`
- artifact size: 1,915,305,312 bytes
- quantization: Q4_K_M
- license: Apache-2.0
- source: https://huggingface.co/ggml-org/SmolLM3-3B-GGUF

These are distinct model families, not different quantizations or decoding settings of one model. Both are conversational/instruction-capable GGUF models supported by llama.cpp. Their role in AT0-EN is feasibility diversity, not state-of-the-art English quality.

## 5. Existing-resource execution environment

Target environment:

- repository: `abdullah-s-mahmood/sweet-runtime-parity` (public);
- GitHub-hosted Linux runner: `ubuntu-22.04` or a documented equivalent;
- models run sequentially, one resident at a time;
- one generation request at a time;
- no GPU requirement;
- additional monetary spend ceiling: `USD 0`;
- bounded by workflow timeout, 48 slots and 72 logical requests.

Record the actual runner image, CPU, memory, free disk, llama.cpp revision/version, Python version, model artifact hash, wall-clock duration and any available token counts.

## 6. Required smoke gate before full live matrix

Before executing the 48-slot matrix:

1. rerun the 30 frozen offline fixtures and preserve F07 behavior;
2. download Model A at its pinned revision and verify the expected SHA-256;
3. run exactly one fixed non-evaluation smoke prompt proving instruction-following and structured-output viability;
4. remove/unload Model A;
5. download Model B at its pinned revision and verify the expected SHA-256;
6. run the same non-evaluation smoke prompt;
7. remove/unload Model B;
8. record runtime/resources and decide only whether each backend is mechanically usable.

The smoke prompt must not be one of EN01–EN12 and must not be used to tune generation settings. If either model cannot perform the required structured response reliably enough to start the frozen matrix, stop and return `MODEL_RESOURCE_OR_CAPABILITY_BLOCKER`; do not silently replace it.

## 7. Frozen generation settings

Use deterministic or near-deterministic settings selected before the matrix and shared across both models where llama.cpp semantics permit:

- temperature: 0.0;
- seed: 20261003;
- context window: at least 4096 tokens;
- maximum generated tokens: DIRECT 800, PLAN 400, REALIZE 800;
- concurrency: 1;
- no automatic retry for malformed/refused/poor output;
- at most one transport retry only when an unambiguous infrastructure failure occurred and the same request was not completed.

If a model's chat template requires a specific non-semantic runtime flag, record it. Do not change prompts, sampling or template policy after seeing evaluation outputs.

## 8. Reproducibility classes

Open-weight frozen execution: `REPRODUCIBLE_FROZEN_WEIGHTS` when artifact hash, runtime revision, template and generation settings are all captured.

ChatGPT Plus/Work observation: `OBSERVED_SUBSCRIPTION_LIMITED_REPRODUCIBILITY` unless an exact model snapshot/runtime identity and repeatable programmatic interface are available. Such observation does not substitute for automated harness integration.

## 9. Stop conditions

Stop before or during live generation if:

- artifact hash/revision differs;
- model/runtime identity cannot be recorded;
- model cannot run within available resources;
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
- additional monetary cost (expected `USD 0` for the preferred path);
- any limitation caused by small open models.

Do not start HW1-EN or DR automatically.
