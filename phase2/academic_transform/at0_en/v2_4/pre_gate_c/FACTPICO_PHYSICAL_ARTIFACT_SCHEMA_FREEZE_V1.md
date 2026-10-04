# ACAD_PASS — FactPICO Physical Artifact + Schema Freeze V1

Date: 2026-10-04
Status: PHYSICAL ARTIFACT FROZEN / PRIMARY GOLD COMPLETE / RATIONALE LAYER PARTIALLY DEFECTIVE / NO V2.4 EXECUTION

Parent:
`FACTPICO_ARTIFACT_SCHEMA_LICENSE_AUDIT_V1.md`

Input supplied by user:
`FactPICO.zip`

## 1. Archive integrity

File:
`FactPICO.zip`

Size:
`2,232,398 bytes`

MD5:
`7f14a2b793f0ee5bb03aadb0131768db`

SHA-256:
`ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`

ZIP integrity:
`PASS`

The archive content matches the expected FactPICO release structure and the benchmark counts reported in the ACL 2024 paper.

No publisher checksum was available for direct checksum comparison.

## 2. Exact released files

| File | Rows | Columns | SHA-256 |
|---|---:|---:|---|
| `data/all_evaluations.csv` | 345 | 28 | `1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd` |
| `data/rest_270_annotated_rationales.csv` | 240 | 9 | `fee5954b842b19943cac7bb0c6e995552649407dd6c954a5acf4cee78dee27ea` |
| `data/doubly_annotated_rationales.csv` | 75 | 16 | `adcb12619cc301df1a25f2c0e9b3ce93af4787e8ebda4905ae04d9509bf31a9a` |
| `data/evidence_inference_rationales.csv` | 645 | 9 | `b8ab3c4a3c363277da8aad2006e9aee2058db802ad324b0840479fb8f8d4a0bf` |
| `data/rest_added_information.csv` | 350 | 5 | `825829ac519ed1fa746f843903e37714c68e8a5ec89736c7c0b20dab78976155` |
| `data/doubly_annotated_split_added_information.csv` | 165 | 6 | `4b82da5058c54807981e7ca0ce209e19febb13e8ea9bdc92cbb476191c7c61d4` |
| `data/rest_contradictions.csv` | 38 | 5 | `3a536beeedc28d50f58e09b9b2b25553e65b65a38dc01ac281752abe31589b8d` |
| `data/doubly_annotated_split_contradictions.csv` | 25 | 6 | `eabbca019536c9ff0b43d80c44ced4bf5944547d93fbf60c9a164fcc1413fbf7` |
| `data/pico_rationales.csv` | 345 | 23 | `2fa7d246992111c13578fc51cf69bfbf216e010cb102aa553c08b79bbc3e4321` |
| `data/llm_pico_rationales.csv` | 345 | 23 | `2fa7d246992111c13578fc51cf69bfbf216e010cb102aa553c08b79bbc3e4321` |
| `data/README.md` | — | — | `794507fe5b8b209bf0fbed67272fe4bd9b04700291527c490efc93d33e9de75b` |

Important:
`pico_rationales.csv` and `llm_pico_rationales.csv` are byte-identical duplicates.

## 3. Primary released gold file

Canonical primary numeric human-gold file:

`data/all_evaluations.csv`

Physical columns:

- Abstract
- generation
- model_type
- Population
- Intervention
- Comparator
- Outcome
- Results
- Avg. PICO-R
- holistic score
- QAFactEval
- QuestEval
- AlignScore
- DAE
- GPT-4
- Flipped Llama-2
- Llama-2
- Alpaca
- Mistral
- pico_abs
- pico_sim
- Extract
- RougeL
- gpt_4-score_results
- llama-2-score_results
- alpaca-score_results
- Mistral-score_results
- gpt4_extract_score_results

Primary expert dimensions for future H1 contract:

`Population`
`Intervention`
`Comparator`
`Outcome`
`Results`

The remaining automatic metric columns are NOT human gold.

`Avg. PICO-R` is a derived aggregate and will NOT be used as a hard-gold field.

`holistic score` is not assigned a hard role until its exact provenance/semantics are independently frozen.

## 4. Core benchmark reconciliation

Observed:

- rows/summaries: `345`
- unique source abstracts: `115`
- unique generated summaries: `345`
- unique exact Abstract+generation pairs: `345`
- duplicate Abstract+generation rows: `0`

Model distribution:

- ALPACA: `115`
- GPT-4: `115`
- LLAMA-2: `115`

Every one of the 115 source abstracts has exactly:
`3`
model summaries.

This matches the published FactPICO benchmark design exactly.

## 5. Source-cluster identity

The release does NOT contain an explicit PMID/source-ID column.

Therefore the frozen internal source-cluster identifier is:

`source_cluster_id = SHA256(exact Abstract text)`

Observed unique source clusters:

`115`

All three model summaries for a source abstract remain within one source cluster.

This is sufficient for within-FactPICO clustered evaluation.

Cross-dataset lineage/PMID mapping remains a separate future overlap-audit task.

## 6. Deterministic derived manifests

A source-cluster manifest was generated using exact source-text SHA-256 only.

Fields:
- source_sha256
- record_count
- model_count

Rows:
`115`

SHA-256:
`a5b26ad1bac4a80e6b158c251557383835e7c43772e25b084d4a4a2bf49fc831`

A record/gold manifest was generated without raw text.

Record identity:

`SHA256("FACTPICO_REC_V1\0" + source_sha256 + "\0" + model_type + "\0" + candidate_sha256)`

Fields:
- record_id
- source_sha256
- candidate_sha256
- model_type
- Population
- Intervention
- Comparator
- Outcome
- Results
- holistic score

Rows:
`345`

SHA-256:
`693f15c7eaaa6a4687cff04444a4096a076e71600bf240adcf1e5defafe534a5`

File-inventory manifest SHA-256:

`b5ebb32d68597b0dbe6c5ba9853a92ea4770a36d46b4e405a56b1adccbc0df70`

No protected source text needs to be committed publicly for these identifiers.

## 7. Physical score semantics

Published human PICO scale:

- 4 = mentioned and described accurately
- 3 = somewhat inaccurate or vague
- 2 = severe inaccuracies and/or missing critical descriptors
- 1 = missing
- N/A allowed when no meaningful element exists

Observed released PICO numeric values include:
- integers 1–4
- half-step values in double-annotated records
- `0` in Intervention/Comparator only

Cross-checking released rationales confirms:
`0`
is used for cases described as having no meaningful applicable intervention/comparator.

Therefore for the release:

`0 = N/A encoding`

for the relevant PICO field.

This must be treated as NOT APPLICABLE, not as a worst factuality score.

## 8. Averaging behavior

The 80 source abstracts in:

`rest_270_annotated_rationales.csv`

produce 240 summaries and have integer PICO ratings only.

The 25 source abstracts in:

`doubly_annotated_rationales.csv`

produce 75 summaries and contain half-step PICO scores in `all_evaluations.csv`.

Therefore the released primary PICO scores for double-annotated material contain aggregated/averaged ratings rather than raw independent rater labels.

Important:
- a 3.5 is not a native annotation category;
- it is an aggregate of multiple observed judgments;
- released numeric gold must not be misrepresented as a single annotator's categorical label.

## 9. Results / Evidence Inference structure

`evidence_inference_rationales.csv`:

- rows: `645`
- exact source-summary pairs represented: `345/345`
- all 345 pairs exactly match `all_evaluations.csv`
- result spans per summary range: `1–5`

Distribution:
- 1 span: 147 summaries
- 2 spans: 126
- 3 spans: 51
- 4 spans: 12
- 5 spans: 9

Thus the released `Results` field in `all_evaluations.csv` is a summary-level aggregate over one or more evidence-inference judgments, and can contain non-half fractional values.

It must not be treated as a single native 1–4 categorical judgment.

## 10. PICO rationale release anomaly

Human PICO rationale files:

### Single-annotated rationale file
`rest_270_annotated_rationales.csv`

Despite the filename, actual rows:
`240`

These correspond to:
- 80 source abstracts
- 3 summaries per source
- 240 summaries

### Double-annotated rationale file
`doubly_annotated_rationales.csv`

Rows:
`75`

These correspond to:
- 25 source abstracts
- 3 summaries per source
- 75 summaries

The source-abstract sets are disjoint.

Combined PICO rationale coverage:
- 105 source abstracts
- 315 summaries

Therefore:
- 10 source abstracts
- 30 summaries

have numeric expert ratings in `all_evaluations.csv` but no released human PICO-rationale row.

This is a release-layer rationale omission, not missing primary numeric gold.

## 11. Rationale text corruption/mismatch

After conservative formatting normalization, 15 of the 315 released PICO-rationale candidate strings do not exactly match the corresponding canonical generation text in `all_evaluations.csv`.

Several contain obvious repeated noise/tokens such as:
- MSG
- MS
- MS Windows
- repeated nonsensical token sequences

Therefore:

`PICO RATIONALE TEXT LAYER = PARTIALLY DEFECTIVE`

Policy:
- never replace canonical candidate text using rationale-file candidate text;
- primary Source/Target text comes only from `all_evaluations.csv`;
- rationales are audit/interpretation support only;
- mismatched rationale rows require explicit provenance matching before use;
- rationale corruption cannot alter primary gold denominators.

## 12. Added-information layer

Single-annotated added-information file:
- 350 span rows
- 158 unique source-summary pairs
- labels:
  - yes: 263
  - no: 87

Double-annotated added-information file:
- 165 span rows
- 73 unique source-summary pairs
- labels:
  - yes: 120
  - no: 45

These are span-event files, not one-row-per-summary files.

Absence of a row is not automatically a negative label.

Some candidate strings in these auxiliary files inherit the rationale-layer text mismatch problem.

Therefore added-information fields must be joined using frozen source/candidate identity rules, never by unverified row order.

## 13. Contradiction layer

Contradiction files are sparse.

The paper explicitly states these additional contradiction annotations are scarce and are not included in the core FactPICO benchmark.

Therefore:

`CONTRADICTIONS = DIAGNOSTIC ONLY`

They are not part of hard H1 gold.

## 14. LLM rationale files

`pico_rationales.csv`
and
`llm_pico_rationales.csv`

are byte-identical.

They contain LLM/automatic evaluator rationales, not human hard gold.

Therefore:

`LLM PICO RATIONALES = DIAGNOSTIC ONLY`

They must never enter the H1 inference path or human-gold definition.

## 15. Primary gold hierarchy

Frozen hierarchy:

### PRIMARY HARD-GOLD CANDIDATES
From:
`all_evaluations.csv`

Fields:
- Population
- Intervention
- Comparator
- Outcome
- Results

Subject to H1 Contract V4 mapping.

### HUMAN EXPLANATORY/AUDIT SUPPORT
- doubly_annotated_rationales.csv
- rest_270_annotated_rationales.csv
- evidence_inference_rationales.csv
- added-information annotation files

These support interpretation/provenance but do not define record existence.

### DIAGNOSTIC ONLY
- contradiction files
- LLM rationale files
- automatic metric columns
- Avg. PICO-R aggregate
- holistic score until separately justified

## 16. Artifact completeness verdict

### Primary benchmark/gold completeness
`PASS`

Reason:
- 115/115 sources
- 345/345 summaries
- 3/3 model outputs per source
- primary expert numeric ratings present for every summary
- evidence-inference rationale coverage includes all 345 summaries

### Human PICO rationale completeness
`PARTIAL`

Reason:
- 315/345 rationale rows represented by release structure
- 30 summaries lack PICO rationale rows
- 15 released rationale candidate strings are corrupted/mismatched relative to canonical generation text

This limitation must remain visible.

## 17. License/use boundary

Annotations:
`CC BY 4.0`

Repository code:
`MIT`

Source articles:
from PubMed Open Access subset with reuse-compatible licenses, but underlying article licenses may differ.

Conservative repository policy:
- do not commit raw full abstract/summary text unless required and source-license-compatible;
- commit hashes, IDs, derived metrics, contracts, and non-protected manifests;
- preserve attribution.

## 18. Readiness impact

FactPICO artifact bytes:
`PASS`

ZIP/file integrity:
`PASS`

Primary physical schema:
`PASS`

Primary gold coverage:
`PASS`

Source-cluster identity:
`PASS VIA ABSTRACT HASH`

License/access:
`PASS WITH CONSERVATIVE SOURCE-TEXT REDISTRIBUTION POLICY`

Rationale completeness:
`PARTIAL / NON-BLOCKING FOR PRIMARY NUMERIC GOLD`

Exact hard-gold eligibility/mapping:
`NOT READY`

H1 adapter/metric contract V4:
`NOT READY`

V2.4 external prediction:
`NOT AUTHORIZED`

## 19. Exact next checkpoint

`FACTPICO HARD-GOLD ELIGIBILITY + H1 CONTRACT V4 FREEZE`

Before prediction:
1. define native element-level safe/error/uncertain strata without using Avg. PICO-R;
2. define treatment of 0=N/A;
3. define treatment of half/fractional aggregated ratings;
4. define Results aggregate semantics and thresholds;
5. determine whether Added Information can enter hard H1-S without external fact-checking leakage;
6. freeze source-cluster micro/macro statistics;
7. freeze record IDs and prediction/gold separation;
8. independent review if material mapping choices remain;
9. only then implement adapter/input manifests.

Still prohibited:
- V2.4 FactPICO prediction;
- H1 scoring;
- runtime modification;
- threshold tuning after prediction;
- original custom Gate C opening;
- new-human recruitment;
- Arabic-track work.
