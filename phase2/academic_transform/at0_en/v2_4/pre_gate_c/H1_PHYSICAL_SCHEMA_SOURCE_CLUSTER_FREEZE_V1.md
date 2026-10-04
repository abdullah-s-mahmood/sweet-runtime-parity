# ACAD_PASS — H1 Physical Schema + Source-Cluster Freeze V1

Date: 2026-10-04
Status: PHYSICAL SCHEMA FROZEN / SOURCE-CLUSTER RULE FROZEN / NO V2.4 EXECUTION

Inputs supplied by user:
1. `manual-judgments-task1-2024.zip`
2. `PLABA_2024-Task_2.zip`

No external benchmark prediction was run.

## 1. Raw archive integrity

### Manual judgments

File:
`manual-judgments-task1-2024.zip`

Size:
`7,054,073 bytes`

Local MD5:
`589ad66e0b9324592f0151cc67974015`

Publisher MD5 expected:
`589ad66e0b9324592f0151cc67974015`

Match:
`YES`

Local SHA-256:
`8256f7342c180e881e9c11244a7c24fe3e2fb4bdabf0fdfeb04892e4c8c722ce`

ZIP integrity:
`PASS`

### Source/test corpus

File:
`PLABA_2024-Task_2.zip`

Size:
`231,126 bytes`

Local MD5:
`daa454a5234161489fef52eab1ebec26`

Local SHA-256:
`f9416ee9ef5a051e79053b526ad7023237cb87d171e79d9623bda4dbd656991e`

ZIP integrity:
`PASS`

Inner source files:

`PLABA_2024-Task_2/test.json`
- size: 820,481 bytes
- SHA-256:
  `2d53f485082ea16571ac54d9f3bcbd56c1c199130d4b8542e93b678ed561e9a7`

`PLABA_2024-Task_2/README.md`
- size: 708 bytes
- SHA-256:
  `1ae6b192c43c07f2e0ccdbd1af617462904ff2302e39c286718c89986221ae83`

## 2. Source corpus physical schema

The README specifies:

- 40 consumer-question IDs:
  `Q1 ... Q40`
- each question has 10 abstract slots:
  `A1 ... A10`
- each abstract has:
  - PMID
  - title
  - ordered sentence list

Observed source totals:

- questions: `40`
- abstract slots: `400`
- source sentences: `4,060`
- unique PMIDs: `399`

Sentence count per abstract:
- minimum: `3`
- maximum: `38`

Primary source-cluster ID:
`PMID`

## 3. Duplicate source-cluster finding

Exactly one PMID occurs in two abstract slots:

PMID:
`15857353`

Slots:
- `Q14_A3`
- `Q37_A5`

Each contains 7 source sentences.

The source sentence sequences are exactly identical.

Therefore:

`Q14_A3` and `Q37_A5` are ONE statistical source cluster.

Maximum independent H1 source clusters from this corpus:

`399`

not 400.

This is a permanent de-duplication rule.

## 4. Manual-judgment archive structure

ZIP contains:
- 1 directory entry
- 19 TSV files

All 19 TSV files have the exact same physical schema:

`Abstract`
`Sentence`
`Source`
`Target`
`Accuracy`
`Completeness`
`Simplicity`
`Brevity`

Observed score alphabet on all four manual axes:

`-1, 0, 1`

The peer-reviewed PLABA paper confirms that sentence-level judgments use a three-point Likert scale:

`-1, 0, 1`

and are later linearly mapped to `0–100` for aggregate reporting.

No blank Accuracy or Completeness cell was observed in any retained judgment row.

## 5. Exact source-row reconciliation

Every judgment row was joined to `test.json` by:

`Abstract + Sentence`

For every retained judgment row:

- ID pair exists in source corpus: `100%`
- judgment `Source` text exactly equals source `test.json` sentence: `100%`
- extra source-sentence pairs: `0`
- empty target fields: `0`

This strongly establishes exact record provenance.

## 6. Run-level physical manifest

| Run file | Rows | Abstract slots | PMID clusters | Missing source-sentence rows | SHA-256 |
|---|---:|---:|---:|---:|---|
| GPT.tsv | 4060 | 400 | 399 | 0 | dc8a6b29345435ef078f6ac5b498591fc362ca48c3750462c1bdfbbe27918bb7 |
| mistral-FINAL.tsv | 4060 | 400 | 399 | 0 | a349ec0991785d752c4d95145f19633998c67a359daa79308aa58fe3e98a2996 |
| gpt-final.tsv | 4060 | 400 | 399 | 0 | d28c4e7c7f3bf8cdadfb837f8f44a9fcb0c627550375fa28974fd5023872aa86 |
| bart_base_ft.tsv | 4060 | 400 | 399 | 0 | 0c4353c4c6bb6ba1f095fc00ff7f18ea11f982c573c355fc5e23b11734c96b70 |
| LLaMa_3.1_70B_instruction_2nd_run.tsv | 4060 | 400 | 399 | 0 | a70e3027068675cd3dc22724f5a44be67840774800df7661537af25147c6a545 |
| task2_moa_tier1_post.tsv | 4060 | 400 | 399 | 0 | 55bc7ef72ecb66e6c11eb743e5dd301ab5c7b6a93eeb2fe630b9e9e5d488dcc8 |
| plaba_um_fhs_sub1.tsv | 4043 | 400 | 399 | 17 | f5b5961c13132c57de1853037cda43c3ea9cf954fb2943ae43848ec2662fcfd3 |
| UAms-BART-Cochrane.tsv | 4060 | 400 | 399 | 0 | 49f5d2d9a0e2ed4da26a8ac4db0d2bc85496c846b1a6bae2c286722fa853567c |
| plaba_um_fhs_sub2.tsv | 4022 | 400 | 399 | 38 | b1c26b36166e34460500c43d7ad8660203a627a0afb3b23e4d71da975e87336c |
| gpt35_dspy.tsv | 4060 | 400 | 399 | 0 | 05eabb2f3f717e3c360335d4699a532aab0135275a0a6d78d2d74c3af35d5c04 |
| plaba_um_fhs_sub3.tsv | 3768 | 400 | 399 | 292 | 35e001b9e4190606801491c93592cb5d2b5526f2cc5b6afbcb66f94ff5786908 |
| mistral-fix.tsv | 4060 | 400 | 399 | 0 | 885ad973b09c44de34b83d72bbb491221fad70199dc75ab99cd7f99a0504d74b |
| UAms-ConBART-Cochrane.tsv | 4060 | 400 | 399 | 0 | 86872abfc198655f48f5b1a113a9d899b3515511d7370e17a8288a3987e57fbd |
| TREC2024_SIB_run4.tsv | 4058 | 400 | 399 | 2 | c43c49c0791ee0685081a1907b042e7cefff0e8cbf357579a83b3abfc09f533d |
| TREC2024_SIB_run3.tsv | 4060 | 400 | 399 | 0 | 98a42c9a9ef2f7c896ad6f1b6b9e5be01275c96ff089f446e3256f007e1ef766 |
| task2_moa_tier2_post.tsv | 4060 | 400 | 399 | 0 | f73f4b133053f77d493aaf01575cfbd2b48bb9b0da4a6d0c6c41e2407976e509 |
| task2_moa_tier3_post.tsv | 4060 | 400 | 399 | 0 | 9f443230e84d10ccc246a1bff488b80ab3616e8f96cbddf4ccdc115fedf19fb1 |
| TREC2024_SIB_run1.tsv | 4059 | 400 | 399 | 1 | abdf741da5faddfa43111d6eed3215d6d96643d37941616fc9eae7cfb9641c33 |
| LLaMA-8B-4bit-MedicalAbstract-seq-to-seq-v1.tsv | 4060 | 400 | 399 | 0 | c3eb7b4d49306cf201eea8f2a7355772a597fd4672b3c3d4b643a7442140127e |

Totals:
- judgment rows: `76,790`
- runs with all 4,060 source sentences: `14/19`
- runs with missing source-sentence rows: `5/19`
- missing run×sentence rows: `350`
- unique source-sentence pairs missing in at least one run: `315`

No missing row may later be silently removed from a frozen denominator.

## 7. Manual-axis distributions

Across all 76,790 retained judgment rows:

### Accuracy
- `-1`: 2,084
- `0`: 10,296
- `1`: 64,410

### Completeness
- `-1`: 3,151
- `0`: 16,992
- `1`: 56,647

### Simplicity
- `-1`: 7,875
- `0`: 21,490
- `1`: 47,425

### Brevity
- `-1`: 11,647
- `0`: 34,829
- `1`: 30,314

These are descriptive properties of the gold archive only.
They are NOT ACAD_PASS performance results.

## 8. Reproducible derived-manifest hashes

A deterministic compact source-cluster CSV was generated from:
`test.json`

Fields:
`abstract_id, pmid, sentence_count, source_cluster_id, duplicate_pmid`

SHA-256:
`1128c1188f94fd4ff58e8694bbd9b42a2596d7db548a3faae8f0b0021a0a7c70`

A deterministic compact judgment-run CSV was generated with:
- run filename
- member SHA-256
- row count
- abstract count
- PMID cluster count
- missing-pair count
- empty-target count
- ACC counts
- COM counts

SHA-256:
`52a9fce0ed5b5332f3c720327b3510a2ac300ecf510e75059421d27e5df7f306`

A deterministic missing-pair manifest was generated.

SHA-256:
`9ba1b24ff7bcaf5595044c015f7b9058be70ba1c88b89b23d3ce04a8daa21854`

These manifests contain IDs/metadata only, not protected source text.

## 9. Statistical independence freeze

Primary H1 independence unit:
`PMID`

Rules:
- all sentences from one PMID are clustered;
- all 19 system runs for one PMID are clustered;
- duplicate appearances of the same PMID across question slots are clustered;
- multiple manual axes do not create new independent units;
- sentence-level observations may be used for within-cluster metrics but not counted as independent studies.

Maximum H1 source clusters:
`399`

## 10. Missing-output rule

Five gold run files omit some source-sentence rows.

This omission is part of the external gold archive and must remain visible.

For any future ACAD_PASS use:
- denominators must be frozen before predictions;
- gold rows that do not exist cannot be invented;
- missing run×sentence rows cannot be retrospectively treated as favorable;
- if a chosen metric requires full gold coverage, incomplete run records must be handled by a preregistered rule.

No exclusion may be chosen after seeing ACAD_PASS predictions.

## 11. H1 construct conclusion

The physical archive now verifies that the selected external resource provides real sentence-level human judgments for:

`Accuracy`
and
`Completeness`

over authentic biomedical abstract transformations.

The H1 core construct choice is therefore materially strengthened.

However:

`H1 ADAPTER / METRIC CONTRACT = NOT YET FROZEN`

because we still must preregister:
- native-score treatment;
- any mapping of -1/0/1 to ACAD_PASS outcomes;
- denominator choice;
- aggregate level;
- threshold(s);
- handling of incomplete external runs;
- use of ACC and COM jointly vs separately;
- confidence/statistical reporting.

## 12. Readiness impact

Condition 2 — dataset artifacts/versions/access/licenses:
`PARTIAL PASS ON ARTIFACT IDENTITY + LOCAL INTEGRITY`

Remaining:
explicit reuse/license documentation.

Condition 3 — eligible splits/IDs/human-label provenance/context:
`PASS FOR PHYSICAL SOURCE/JUDGMENT SCHEMA; FINAL ELIGIBLE SUBSET NOT YET FROZEN`

Condition 5 — overlap/source-cluster manifest:
`H1 INTERNAL CLUSTER RULE PASS`

Cross-dataset overlap remains future work.

Condition 4:
`NOT READY`

Condition 6:
`NOT READY`

Overall:
`NOT_READY_GATE_C_EXT_META`

## 13. Exact next checkpoint

`H1 ADAPTER + NATIVE METRIC CONTRACT FREEZE`

Before any V2.4 prediction, freeze:
1. which external records/runs are eligible;
2. whether ACC and COM remain native ordinal metrics or support an exact outcome mapping;
3. denominator and aggregation unit;
4. missing-gold treatment;
5. per-PMID clustering/statistics;
6. threshold/sample-size rationale;
7. measurable V2.4 output mapping with zero semantic helper inference.

Still prohibited:
- V2.4 external predictions;
- benchmark scoring;
- tuning;
- custom 80-study Gate C opening;
- new-human recruitment;
- Arabic-track work.
