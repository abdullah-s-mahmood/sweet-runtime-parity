# AT0-EN V2.1 Open-Weight Smoke Gate Report

Date: 2026-10-03  
Final smoke state: **BLOCKED — STRUCTURED_OUTPUT_CONFORMANCE**

## Frozen backend

- Model A: `Qwen/Qwen3-4B-Instruct-2507`, executable GGUF `Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf`
- Model A SHA-256: `2fde00ce69dd4899c70d020845e2638353015bba0fdf161b3eb965f2bca4464e`
- Model B: `HuggingFaceTB/SmolLM3-3B`, executable GGUF `SmolLM3-Q4_K_M.gguf`
- Model B SHA-256: `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`
- Runtime: pinned `llama.cpp` commit `b92761a515ea31e852e7fbc1fad5f874b46f3718`
- Execution: GitHub Actions public runner, CPU, one model at a time, one request at a time
- Additional monetary cost: USD 0

## Repeated preflight evidence

All three smoke attempts reran the frozen engineering preflight and language-portability checks before model inference:
- engineering fixtures: `30/30 PASS`
- language portability audit: `PASS`
- F07 independent `authorized_scope` invariant retained

No AT0-EN evaluation case EN01–EN12 was opened to model inference. The 48-slot matrix remains `0/48 NOT_RUN`.

## Attempt 1

Run: `37118121815`  
Trigger commit: `7127aaf4d15e1c7a84b7724d9edce3d3349ef77b`  
Artifact: `11271932734`

- Qwen smoke: PASS
- SmolLM smoke: FAIL
- SmolLM consumed the 400-token output ceiling with empty visible content.
- Diagnosis: SmolLM3 extended-thinking mode was active by default.
- Repair: record and apply the model-documented `/no_think` system control. This is a model-specific runtime/chat-template control; no evaluation prompt, model, sample or output ceiling changed.

## Attempt 2

Run: `37118533029`  
Trigger commit: `665bf47f7b06ed601faff9bcda5adc1a2ff3b9e1`  
Artifact: `11272313001`

- Qwen smoke: PASS
- SmolLM produced concise visible JSON and preserved the smoke facts.
- SmolLM returned literal `"status":"REVISE|KEEP|REVIEW"` because the smoke-only schema example itself encoded the enum choices in one quoted string.
- Diagnosis: ambiguity in the smoke fixture, not an evaluation prompt or model-capability result.
- Repair: clarify the smoke-only fixture to require exactly one enum value. No DIRECT/PLAN/REALIZE evaluation prompt changed.

## Attempt 3 — frozen current result

Run: `37118961886`  
Trigger commit: `e91f00f9212ac956443f540ec5d9f9aed9b35e62`  
Artifact: `11272597605`

- Qwen smoke: PASS.
- SmolLM weights/hash/runtime: PASS.
- SmolLM inference: completed normally.
- SmolLM prompt tokens: 240.
- SmolLM completion tokens: 57.
- SmolLM latency: ~11.57 s.
- SmolLM semantic smoke constraints: visibly preserved.
- SmolLM raw visible result:

```text
```json
{
  "status": "REVISE",
  "revised_paragraph": "A pilot sensor recorded 14 observations during a two-hour calibration window. The calibration was exploratory, and the observations do not establish improved accuracy.",
  "uncertainty": []
}
```
```

The frozen smoke parser calls `json.loads(raw_text)` directly. Therefore the Markdown code fence causes:
`JSONDecodeError: Expecting value: line 1 column 1`.

Current classification:
- inference capability: observed;
- English instruction following: observed on smoke only;
- protected smoke facts: visibly preserved;
- strict raw-JSON conformance: FAIL;
- full AT0-EN matrix: NOT_RUN.

## Why execution stops here

A fourth automatic attempt is not authorized. The remaining issue is no longer model access or compute. Resolving it requires an explicit policy decision on structured-output handling.

Potential decisions for the architect, without implementation-agent preference being treated as authorization:

1. **KEEP strict raw JSON:** SmolLM3 fails the current smoke gate; select a different predeclared model only through an explicit amendment.
2. **Allow deterministic fence normalization:** define a narrowly versioned parser that removes exactly one outer Markdown JSON fence before JSON parsing, while keeping malformed JSON rejection unchanged.
3. **Use runtime constrained JSON/grammar:** require llama.cpp JSON-schema/grammar output for both models, if the architect judges this part of the transport layer rather than a material generation-policy change.

Options 2 or 3 may affect the meaning of structured-output conformance and therefore require explicit higher-model approval before another inference run.

No HW1-EN, DR, Arabic work, model substitution, evaluation-matrix reduction, or live matrix execution is authorized from this report.
