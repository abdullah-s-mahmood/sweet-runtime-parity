# AT0-EN V2.1 Live Matrix — Closure Lock

Date: 2026-10-03  
Status: **CLOSED / EXECUTION COMPLETE / NO SILENT RERUN**

## Frozen run identity

- Repository: `abdullah-s-mahmood/sweet-runtime-parity`
- Branch: `phase2-arabic-eval`
- Trigger commit: `82e612adf16922e408954119e587c80a420721a0`
- Workflow: `AT0-EN V2.1 Open-Weight Live Matrix`
- Run: `37123963805`
- Run conclusion: **success**
- Job started: `2026-10-03T12:46:35Z`
- Job completed: `2026-10-03T13:49:49Z`
- Artifact id: `11275534001`
- Artifact name: `at0-en-v2-1-live-37123963805-1`
- Artifact SHA-256: `842a9ff304c3ed9c854790ac8f205bfe156289b007b556cd06fa4aa19b609326`
- Additional monetary cost: **USD 0.00**

## Artifact internal hashes

- `MATRIX_EXECUTION_SUMMARY.json`: `22fc2b85903f1e3a92a9e9c3a4d1257b95740b7c6de3c887851f50b01506f9a2`
- `identity.json`: `c7add9f115157cfae46c04066baecc7f20490b3671735e79d180548b64b27012`
- `requests.jsonl`: `2b87e2f4b1c665a091b65d4f3fc21e04f830e602cae15a427ac26a2e4dd09c3f`
- `responses.jsonl`: `1d6249af8175436a9c98ce8e6806b5edb606a63a566f783e1651643d4c3a9469`
- `slots.jsonl`: `1e79aeba528611630a2960080767ddb812d40be53b84cc7b2bc5749bc23a5958`
- offline preflight: `f7b0859a9f70269defaade06919fb70e646bc0ac1b341a2a51335ea813f8e161`
- portability audit: `2045c6bf925c0ac0ea12975740eaf73111cba5cf6e921f3caea4065b9fdf5ba8`

## Runtime input identity recorded by the artifact

- cases SHA-256: `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`
- config SHA-256: `ef82264ae0956c049fea0d6dc5b87e61283edc4d54cd618f563264c9e4b1014f`
- model manifest SHA-256: `9b861c6aac9ae1460ee9c29d1dab648ca3bf66484872dddb4000c9f258519563`
- MODEL_A artifact SHA-256: `2fde00ce69dd4899c70d020845e2638353015bba0fdf161b3eb965f2bca4464e`
- MODEL_B artifact SHA-256: `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`

The older `PROMPT_CASE_POLICY_MANIFEST.json` predates the V2.1 backend authorization and still records blocked model/cost state. It is historical context, not the authoritative identity record for this live run. The live artifact `identity.json`, trigger commit, model manifest, workflow and artifact digest are the run identity anchors.

## Execution accounting

- slots expected: **48**
- slots recorded: **48**
- logical calls: **71 / 72 maximum**
- NOT_RUN: **0**
- `COMPLETE_RAW`: **36**
- `FAILED_PARSE_OUTPUT`: **3**
- `FAILED_PARSE_PLAN`: **1**
- `FAILED_SCHEMA_OUTPUT`: **8**

Model/arm slot completion:
- MODEL_A DIRECT: **11/12**
- MODEL_A PLANNED: **12/12** (one final `REVIEW`, no revised paragraph)
- MODEL_B DIRECT: **3/12**
- MODEL_B PLANNED: **10/12**

The workflow success means the bounded experiment executed and all failures were accounted. It does **not** mean all transformations were structurally valid, scientifically faithful, or human-quality.

## Transport/parser audit

Post-run replay of all 71 raw responses found that strict raw JSON parsing and the current live parser had the same parse-success/failure outcome on this run. No live cell was rescued only by outer-fence removal or first/last-brace extraction.

Nevertheless, the current backend parser is broader than the V2.1 smoke policy because it can extract a JSON object from surrounding text. This is a design debt for the next contract and must not be interpreted as an established acceptance policy.

## Closure boundary

This exact 48-slot matrix is consumed and closed. Do not rerun it silently, do not replace a failed cell, and do not regenerate for quality. Any future inference requires a new versioned authorization after higher-model review.

Scientific/human-writing interpretation is recorded separately in:
`AT0_EN_V2_1_RESULT_ANALYSIS.md`.
