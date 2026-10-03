# HIGHER-MODEL REVIEW PACKET — AT0-EN V2.1 SMOKE GATE

## Repository state
- Repository: `abdullah-s-mahmood/sweet-runtime-parity`
- Branch: `phase2-arabic-eval`
- V2.1 backend amendment aligned with frozen models: `1f13ab5668ed0639d6b62b49824eafa2d704670f`
- Frozen model/runtime manifest commit: `04c982dfa52eb6b6f9e91b268574daedd4aecc23`
- Smoke gate blocker report: `fe62dab3af7d044d605c818c405c9bc2d451b3ab`
- Config blocker freeze: `17d3dc57169cab9f198ea3b8c5ab3b95bd633955`

## Stable evidence
- Critical Arabic evidence preservation remains PASS.
- Frozen engineering fixtures: `30/30 PASS`.
- Language portability audit: PASS.
- F07 `authorized_scope` invariant retained.
- Additional monetary cost: USD 0.
- Arabic active research: FROZEN.
- AT0-EN live evaluation matrix: `0/48 NOT_RUN`.

## V2.1 backend
Model A:
- Qwen3-4B-Instruct-2507 Q4_K_M
- SHA-256 `2fde00ce69dd4899c70d020845e2638353015bba0fdf161b3eb965f2bca4464e`

Model B:
- SmolLM3-3B Q4_K_M
- SHA-256 `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`

Runtime:
- pinned llama.cpp `b92761a515ea31e852e7fbc1fad5f874b46f3718`
- public GitHub Actions CPU runner
- models and requests strictly sequential
- no commercial API

## Smoke history

### Attempt 1
Run `37118121815`, artifact `11271932734`.
- Qwen PASS.
- SmolLM exhausted 400 output tokens in default extended-thinking mode and returned empty visible content.
- The model's documented `/no_think` control was then frozen as a runtime/chat-template control.

### Attempt 2
Run `37118533029`, artifact `11272313001`.
- Qwen PASS.
- SmolLM generated concise visible JSON preserving the smoke facts.
- It returned literal status `REVISE|KEEP|REVIEW` because the smoke-only example itself encoded the choices inside one quoted string.
- The smoke fixture was clarified before evaluation; no DIRECT/PLAN/REALIZE prompt changed.

### Attempt 3 — current frozen result
Run `37118961886`, artifact `11272597605`.
- Qwen PASS.
- SmolLM artifact/hash/runtime PASS.
- SmolLM generated in ~11.57 s using 240 prompt + 57 completion tokens.
- Its visible revision preserved 14 observations, two-hour duration, exploratory status, and the negation that improved accuracy was not established.
- Its returned object is valid JSON *inside a Markdown json code fence*.
- The frozen smoke parser applies `json.loads(raw_text)` directly, so the outer fence yields JSONDecodeError.
- Classification: `BLOCKED_STRUCTURED_OUTPUT_CONFORMANCE`.
- No fourth attempt was started.

Full report:
`phase2/academic_transform/at0_en/results/AT0_EN_V2_1_SMOKE_GATE_REPORT.md`

## Independent statuses
```text
ENGINEERING_STATUS: PASS_OFFLINE
OPEN_WEIGHT_BACKEND_STATUS: PARTIAL_SMOKE_PASS
QWEN_SMOKE_STATUS: PASS
SMOLLM3_SMOKE_STATUS: FAIL_STRICT_RAW_JSON_CONFORMANCE
EXPERIMENT_STATUS: NOT_RUN
LIVE_MATRIX: 0/48
HUMAN_WRITING_STATUS: NOT_ASSESSED
SCIENTIFIC_FIDELITY_STATUS: NOT_ESTABLISHED
DETECTOR_ROBUSTNESS_STATUS: NOT_RUN
VOICE_STATUS: NOT_ASSESSED
DOCUMENT_FIDELITY_STATUS: NOT_RUN
COMMERCIAL_USEFULNESS_STATUS: NOT_ASSESSED
```

## Decision required

The remaining issue is no longer model access, compute, licensing, hashes, or apparent English instruction-following on the smoke prompt. It is the exact structured-output boundary.

Please decide one of these approaches, or provide a better one:

1. **KEEP strict raw JSON.** Treat fenced JSON as smoke failure; SmolLM3 is unsuitable for this frozen backend and any model replacement requires an explicit amendment.
2. **Narrow deterministic fence normalization.** Permit the transport/parser layer to remove exactly one outer Markdown JSON code fence, then run the same strict JSON/schema validation. All other malformed JSON remains rejected.
3. **Runtime-constrained JSON.** Apply an identical llama.cpp JSON grammar/schema constraint to both models if you judge this a transport mechanism rather than a material change to model behavior.

Important conflict to resolve: frozen fixture F28 requires malformed JSON/schema responses to be preserved and rejected without a retry. If option 2 is accepted, state explicitly whether a syntactically valid JSON object wrapped in one standard Markdown JSON fence is classified as transport framing rather than malformed model content.

## Implementation-agent recommendation
Do not change models yet. Attempt 3 shows SmolLM3 can perform the smoke transformation and preserve the requested facts; the failure is only outer Markdown framing. A narrowly specified, versioned handling policy may be more scientifically defensible than replacing the model, but this changes the structured-output acceptance boundary and therefore is escalated rather than applied unilaterally.

No fourth smoke attempt, full matrix, HW1-EN, DR, Arabic restart, or model substitution is authorized until this decision is returned.
