# ACAD_PASS — FactPICO H1 Adapter + Input/Gold Manifest Implementation Freeze V1

Date: 2026-10-04
Status: IMPLEMENTATION FREEZE COMPLETE / NO V2.4 PREDICTION

Parent contract:
`H1_FACTPICO_HARD_GOLD_CONTRACT_V5.md`

Landscape strategy:
`SCIENTIFIC_VERIFICATION_LANDSCAPE_RESET_V1.md`

## 1. Deterministic adapter

Repository file:

`phase2/academic_transform/at0_en/v2_4/pre_gate_c/factpico_h1_adapter_v5.py`

Commit:

`c36aef499fe28c83b80f1d7a9f296deefa309d2d`

Frozen adapter SHA-256:

`ab128309261eeffdb734464f2a2fef52cef4ce37bdb3b9654317d6b5bba0b7e1`

The adapter performs only:
- raw ZIP integrity verification;
- exact CSV parsing;
- exact text hashing;
- deterministic source/record identity;
- deterministic V5 gold-class reconstruction;
- exact Added Information identity checks;
- input/gold separation;
- count/hash/integrity assertions.

It does NOT:
- call V2.4;
- perform semantic inference;
- repair or normalize source/candidate meaning;
- use embeddings/LLMs/NLI;
- expose human gold fields to inference input;
- score predictions.

## 2. Frozen source artifact

User-supplied FactPICO archive:

`FactPICO.zip`

SHA-256:

`ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`

Primary numeric gold member:

`data/all_evaluations.csv`

SHA-256:

`1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd`

## 3. Prediction input artifact

Private local artifact:

`FACTPICO_H1_V5_PREDICTION_INPUT_PRIVATE.jsonl`

Records:

`345`

Allowed keys only:

- `record_id`
- `source_text`
- `candidate_text`

SHA-256:

`ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`

Gold-field leakage assertion:

`PASS`

Prediction input contains no:
- PICO score;
- Results score;
- gold class;
- N/A flag;
- annotation provenance;
- Added Information flags;
- model-generated gold rationale.

## 4. Separate gold artifact

Private local artifact:

`FACTPICO_H1_V5_GOLD_PRIVATE.jsonl`

Records:

`345`

SHA-256:

`6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`

Prediction/gold record-ID sets:

`EXACT MATCH = PASS`

Gold join is prohibited until a future V2.4 prediction artifact has itself been frozen and hashed.

## 5. Public metadata-only eligibility manifest

Reconstructed deterministic artifact:

`FACTPICO_HARD_GOLD_ELIGIBILITY_MANIFEST_V5.csv`

Rows:

`345`

SHA-256:

`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

This exactly reproduces the previously frozen V5 eligibility hash.

The adapter fails closed if this hash changes.

## 6. Public build manifest

Repository file:

`FACTPICO_H1_V5_BUILD_MANIFEST.json`

Commit:

`8450003be24db1b101cb7a8be663431a934dbd76`

Expected build-manifest byte SHA-256:

`67bfbd4302f66d2248009c8a6fe9cef658a6f202d278450b73e942c68cb6f16b`

The build manifest records:
- adapter hash;
- source/gold hashes;
- output hashes;
- class counts;
- source-cluster counts;
- per-model class counts;
- no-gold-leak status;
- no V2.4 execution status.

## 7. Reproducibility check

The adapter was executed twice sequentially in separate output directories.

Both runs returned:

`return code = 0`

Both runs produced identical:

- adapter SHA-256;
- prediction input SHA-256;
- gold file SHA-256;
- eligibility manifest SHA-256;
- build manifest SHA-256.

Therefore:

`DETERMINISTIC REBUILD = PASS`

## 8. Environmental warning

During the first local Python invocation, the environment emitted an unrelated:

`artifact_tool spreadsheet runtime warmup`

warning/error during Python startup.

The FactPICO adapter itself completed with:

`return code = 0`

and all expected hashes/counts passed.

A second independent sequential build produced the same hashes.

Classification:

`TOOLING/ENVIRONMENT WARNING — NOT SCIENTIFIC OR ADAPTER FAILURE`

Preserve this negative evidence.

## 9. Frozen V5 gold counts reproduced by code

- SAFE_STRICT_CONTROL:
  `34 records / 33 sources`

- ERROR_STRICT:
  `149 records / 83 sources`

- INTERMEDIATE:
  `153 records / 84 sources represented`

- N_A_SOURCE_DIAGNOSTIC:
  `9 records / 3 sources`

Per-model counts also reproduce the frozen V5 contract exactly.

## 10. Identity / integrity controls

Adapter verifies:

- exactly 345 primary records;
- exactly 115 source abstracts;
- exactly 115 records per generating model;
- exactly 3 candidates per source;
- exactly 25 double-PICO sources;
- exactly 3 N/A source clusters;
- exactly 216 canonical source/candidate pairs with Added Information span rows;
- exactly 15 source clusters with unresolved auxiliary Added Information candidate identity;
- no duplicate record ID;
- exact frozen eligibility hash.

Any mismatch causes hard build failure.

## 11. Privacy / redistribution policy

Raw source abstracts and generated summaries are NOT committed to the public ACAD_PASS repository in the prediction or gold private artifacts.

Repository stores:
- deterministic adapter;
- contracts;
- hashes;
- metadata;
- counts;
- eligibility rules/build manifest.

This preserves the conservative source-text redistribution policy.

## 12. Current readiness

FactPICO physical artifact:
`PASS`

H1 V5 gold contract:
`PASS / FROZEN`

Deterministic adapter:
`PASS / FROZEN`

Prediction input:
`PASS / FROZEN HASH`

Separate gold:
`PASS / FROZEN HASH`

No-gold-leak validation:
`PASS`

Deterministic rebuild:
`PASS`

V2.4 prediction:
`NOT YET RUN`

H1 performance:
`NOT YET MEASURED`

## 13. Landscape strategy correction

A fresh 2024–2026 research audit confirms that many strong benchmarks and systems exist.

The correct strategy is:

`CONSTRUCT-MODULAR EXTERNAL VALIDATION`

not one-resource-per-whole-system validation.

Current future candidate upgrades include:

H1 broader revision/factuality:
- scientific text revision evaluation;
- ParaRev;
- XtraGPT;
- LongSciVerify;
- long-document factuality stress testing.

H2:
- SciVer;
- CLAIM-BENCH;
- SciCiteVal/CiteAudit where citation support is the construct;
- SciFact retained as established baseline.

H3:
- SciClaimEval;
- SciTab/Table-Text Alignment;
- CLAIM-BENCH;
- QASemConsistency where relation contract fits.

H4/META:
- ACAD_PASS independent oracle;
- current long-document meaning-preserving perturbation literature for family coverage.

Applications/products such as Scite, Elicit, Paperpal, SciSpace, IPPOLIS Write and research systems such as SciTrue cover important parts of the workflow but not the full audited ACAD_PASS loop.

## 14. Exact next checkpoint

`H1 FACTPICO PRE-PREDICTION INTEGRITY GATE`

Before any V2.4 run:
1. verify repository adapter bytes/hash;
2. verify frozen runtime hash;
3. verify input/gold/build hashes;
4. freeze exact one-shot prediction command/config;
5. verify no gold is readable by inference path;
6. freeze failure/retry policy;
7. decide whether independent review is needed for execution mechanics only;
8. STOP before execution unless explicitly authorized.

No prediction was performed in this checkpoint.
