# AT0-EN V2.4 — Gate B2 Protocol and Input Freeze Closure

Date: 2026-10-03
Status: CLOSED CHECKPOINT / PROTOCOL FROZEN / SCORING NOT STARTED

## Integrity execution

Workflow:
`AT0-EN V2.4 B2 Protocol Integrity`

Run:
`37146751607`

Trigger commit:
`c35eda7e29e40eaa424e8b477b43353327da09ad`

Artifact:
- id: `11282226161`
- SHA-256: `035673f9fd02fc28cd516ba23f7594cbbac48c4ed23a276bd6abf99e67370a77`

Integrity:
- status: PASS
- checks: 144
- pair count: 12
- arms: GG / GE / EG / EE
- primary arm: EE
- model inference: none

## Frozen experiment design

GG:
human-correct source -> human-correct candidate
Historical baseline: 100%.

GE:
human-correct source -> extracted candidate
Candidate-extraction degradation.

EG:
extracted source -> human-correct candidate
Source-extraction degradation.

EE:
extracted source -> extracted candidate
Primary combined degradation arm.

All four arms must be reported separately.

## Frozen raw text derivation

B2 raw texts are deterministically derived from B1 graph evidence:
1. assertion evidence in graph order;
2. relation evidence in graph order;
3. exact duplicate evidence removed while preserving first occurrence;
4. no semantic rewriting.

12/12 raw source/candidate pairs were verified against the frozen B1 graphs.

## Frozen bridge rule

The extraction-to-alignment bridge may only mechanically map fields and explicitly owned deterministic anchors.

It may not:
- invent missing relations;
- repair semantic content;
- resolve missing coreference;
- use expected outcomes or gold mappings.

The A2 extractor currently emits no semantic relations.
Therefore absent extracted relations remain absent in B2 and are measured as extraction degradation.

## Pre-registered EE gates

Safety:
- adversarial acceptance: 0/6
- dangerous critical false preserve: 0
- ambiguous pair must remain REVIEW
- critical uncertainty promotion: 0

Usability:
- faithful safe-pair acceptance >= 4/5 = 80%
- pair outcome >= 11/12 = 91.67%
- faithful false rejection <= 1/5

No usability score compensates for a safety failure.

## Frozen identities

- aligner:
  `289d2898c89850f691d52313a1d2a2b12b37cef6b674549215579caedf84cd42`

- extractor:
  `32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`

- B1 pairs:
  `29f3790859c8da6baf65db8b0fb372bc881e25d8e3d1e76b9c67b74d49944dca`

- B2 raw pairs:
  `afa733aa5e0498706df66acb7005fa7fff891ef39afe9e8b086a463fdf107395`

- B2 protocol:
  `a70d70edb4dcf4138c63d5ac46a200ec20d7781c0ac7bc3648232f254bda571d`

- B2 bridge contract:
  `51330f76f2ebca0625e2bb4cb040844dceab59355a13ecde5cd29f24f3ae4a7f`

- integrity checker:
  `0a6b0890ed55bc826648a44582d753d1dc36f47e50f494b4aef43e9a5dbf2c40`

- integrity summary:
  `8641d9b3d41f015cec66670d5f7c538944585a3e6ad45de35c350a4a831b0dd7`

## Research interpretation

Fresh research supports:
- granular evidence alignment is a major bottleneck in decomposition-based verification;
- noisy decomposition/extraction errors can determine downstream robustness;
- conservative abstention reduces error propagation;
- scientific verification should retain source-level accountability and evidence traceability;
- a correct verdict alone does not prove faithful reasoning or attribution.

Therefore B2 explicitly attributes degradation by arm rather than reporting one opaque score.

## Cumulative V2.4 success ledger

- V2.3 end-to-end baseline: 37.5% escape / 25% safe acceptance / BOTH_FAIL
- Gate 0: 326/326 contract checks PASS
- A1: 100% precision / 100% recall / 35/35 provenance
- A2: 100% structural representation; known decimal defects 5 -> 0
- A3: 100% coverage / 100% critical coverage / 0% false additions / 88% atomicity / 92.86% certain precision / 87.5% error-abstention / 0 critical silent errors
- A4: GO alignment development
- B1 reference: 363/363 PASS
- B1 first aligner: 83.33% FAIL
- B1.1 repaired aligner: 100% on all B1 hard gates
- B2: performance NOT YET MEASURED; protocol/input integrity 144/144-equivalent checks PASS

## Quality delta

End-to-end performance:
UNCHANGED.

B2 performance:
NOT YET MEASURED.

Methodological status:
IMPROVED because degradation attribution and leakage controls are now frozen before scoring.

## Completion

B2 protocol/input-freeze checkpoint:
100% COMPLETE

Gate B2 overall:
approximately 35% complete

Whole ACAD_PASS planning estimate:
approximately 29% ±5%

## Exact next authorized checkpoint

`AT0-EN V2.4 GATE B2 — BRIDGE IMPLEMENTATION + FIRST FOUR-ARM SCORE`

Next scope:
- implement the frozen bridge only;
- apply frozen extractor independently to source and candidate raw texts;
- construct GE / EG / EE;
- reuse historical GG=100% baseline;
- score all arms with the frozen B1.1 aligner;
- freeze the first degradation result before any repair.

Not authorized:
- extractor tuning before first B2 result
- aligner tuning before first B2 result
- live generation
- HW1-EN
- untouched holdout
- production claims

Higher-model consultation is not required at this point unless implementation exposes a new construct-validity issue.
