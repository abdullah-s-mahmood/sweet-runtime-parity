# AT0-EN V2.4 — Final Pre-Scoring Higher-Model Authorization

Date: 2026-10-03
Decision: **AUTHORIZE ONE DEVELOPMENT SEMANTIC CALIBRATION RUN ONLY**

## Preconditions closed

Model/file identity:
- hash-only run 37133900590: PASS
- artifact 11277806000
- digest sha256:789388dfd4305933741895162e708bf9cc6501a2756297eae64a9216cf1381a1
- 16/16 files hashed
- exact HHEM, FLAN dependency and DeBERTa revisions frozen

Load compatibility:
- run 37134546523: PASS
- artifact 11278246583
- digest sha256:815d7c229a634a5a877a184a95da54456ef31d5c12b39d5aa5af6aa5551586ef
- HHEM parameters: 109,630,082
- DeBERTa parameters: 184,424,451
- network blocked after acquisition
- forward pass blocked and not performed
- semantic inference performed: false

Calibration population:
- run 37134401549: PASS
- artifact 11278375914
- digest sha256:a29bb61bfaa9da188028433f9669a2b417f555c7042b0ec3deda147dcb047923
- 58 consumed DEVELOPMENT examples
- 22 safe
- 36 adversarial
- SAFE_EN08 and SAFE_EN09 from V2.2 excluded before scoring because of label defects/scope ambiguity
- population SHA-256: 40f6c7aa6293b374d4d12d837ed96342d0a8e72d08cc014a115b0be3a54e5a65
- source assertion graph SHA-256: ca1ead1c2aa385ffe6aed605f4142eea8c732223efeed620c7108f73c127c210

Semantic pair freeze:
- run 37134914659: PASS
- artifact 11278156411
- digest sha256:4f179106da90086af296cfc29f55ba1f7c6864433fc03139af1135aef80bfddb
- paragraphs: 58
- exact semantic pairs: 462
- SOURCE_TO_CANDIDATE: 275
- CANDIDATE_TO_SOURCE: 187
- pair manifest SHA-256: 27eaeb6bd6ab1a2b9ef3ff477cfa767c6e8c5526a85dcf9c491f32d8f9ac0460
- no scores or thresholds observed

Threshold protocol:
phase2/academic_transform/at0_en/v2_4/SEMANTIC_CALIBRATION_PROTOCOL_V1.md
Frozen before scores.

## Authorized execution

Exactly one DEVELOPMENT semantic calibration execution using:
- the frozen 462-pair manifest only;
- HHEM-2.1-Open pinned identity only;
- DeBERTa NLI pinned identity only;
- pinned runtime only;
- models executed strictly sequentially;
- no generator model;
- no confirmation examples;
- no best-of-N, model substitution, extra judge or threshold policy change.

Record raw witness scores for every pair before threshold selection.

Threshold selection must follow the already frozen grid/tie-break procedure exactly.

## Calibration scientific gate

PASS only if the frozen selection protocol finds a threshold tuple with:
- adversarial auto-pass = 0 / 36
- safe VERIFIED_FOR_REVIEW >= 16 / 22 (>=70%)
- no missing score
- no hash/runtime identity failure

A completed workflow may therefore have scientific status FAIL. Do not confuse execution success with calibration success.

## Still forbidden

- construction/opening of confirmation before thresholds are frozen
- threshold changes after seeing confirmation
- new generator inference
- HW1-EN
- DR
- automatic manuscript application
- Arabic active research or reserved Arabic data
- V2.1/V2.3 reruns for quality

## Return point

Immediately after raw scores and the preregistered threshold result are frozen. If calibration fails, redesign; do not weaken the gate.
