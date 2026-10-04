# ACAD_PASS — H1 Raw Artifact + Schema + Terms Freeze V1

Date: 2026-10-04
Status: PARTIAL FREEZE / EXECUTION NOT AUTHORIZED

Parent:
`H1_ACCESS_ARTIFACT_RESOLUTION_V1.md`

Protocol:
`GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

Purpose:
freeze the strongest currently verifiable H1 artifact identities, schema evidence, source-cluster rules, and legal/usage handling before any V2.4 prediction.

---

## 1. Canonical H1 core candidate

Preferred H1 core:

`TREC PLABA 2024 COMPLETE-ABSTRACT REWRITE MANUAL JUDGMENTS`

Retrospective taxonomy:
`Task 1 = Rewriting abstracts`

Original event-page taxonomy:
`Task 2 = Complete Abstract Adaptation`

Canonical manual-judgment archive for complete rewriting:

`manual-judgments-task1-2024.zip`

Zenodo DOI:

`10.5281/zenodo.18637045`

Zenodo version:

`v2`

Publisher-provided MD5:

`589ad66e0b9324592f0151cc67974015`

Size:

`7.1 MB`

The archive preview exposes 19 TSV files, matching the 19 complete-rewrite submissions reported in the retrospective paper.

---

## 2. Binary artifact freeze status

The exact download URL is publicly exposed by Zenodo:

`https://zenodo.org/records/18637045/files/manual-judgments-task1-2024.zip?download=1`

The current web tool can resolve this URL but refuses to ingest the binary because of file size/content type.

The local execution environment cannot resolve external DNS and therefore cannot independently download the ZIP.

Therefore:

`PUBLISHER ARTIFACT IDENTITY = FROZEN`

`PUBLISHER MD5 = FROZEN`

`LOCAL BYTE COPY = NOT FROZEN`

`LOCAL SHA-256 = NOT FROZEN`

No local SHA-256 may be invented.

---

## 3. Public source/test corpus

Official NIST/TREC 2024 PLABA data page publicly exposes:

`Task 2 test data`

under the original 2024 event naming.

Direct public URL:

`https://trec.nist.gov/data/plaba/PLABA_2024-Task_2.zip`

This is the original complete-abstract-adaptation test corpus corresponding to the retrospective rewrite task.

Current state:

`PUBLIC URL = FROZEN`

`LOCAL BYTE COPY = NOT FROZEN`

`LOCAL SHA-256 = NOT FROZEN`

---

## 4. Physical schema evidence from PLABA 2023 raw manual judgments

Zenodo exposes the 2023 manual judgments as directly readable CSV.

Canonical header:

`,Source,Output,Answer,Simp. sent,Simp. term,Simp. term acc.,Simp. fluency,Acc. comp.,Acc. faith.,Team,Sent,Abst`

Observed fields:

- row/index
- `Source`
- `Output`
- `Answer`
- sentence simplicity
- term simplicity
- term accuracy
- fluency
- accuracy completeness
- accuracy faithfulness
- `Team`
- `Sent`
- `Abst`

Observed source-cluster-style identifier examples:

`Q1_A4`

`Q2_A6`

Observed sentence identifier:

integer `Sent`

Observed team/run identifier examples:

`PLABA_base_3.aln`

`Bee_Man_1`

`PLABA_base_2`

This confirms PLABA manual judgment artifacts carry:
- source text;
- candidate output;
- run identity;
- sentence identity;
- abstract/question identity;
- human semantic scores.

---

## 5. 2024 logical judgment schema

The peer-reviewed retrospective paper freezes the 2024 manual evaluation axes:

- `ACC`: Does the output accurately reflect the source?
- `COM`: Does the output minimize information loss?
- `SIM`: Is the output easy to understand for a non-expert?
- `BRV`: Is the output as concise as possible?
- `FIN`: average of SIM, ACC, COM, BRV.

The paper states:
- 19 complete-rewrite submissions;
- sentence-level outputs;
- all 400 test abstracts included;
- manual evaluation treated as the gold standard.

Logical ACAD_PASS H1 interpretation:

`H1-S <- ACC`

`H1-C <- COM`

Important:
this is a construct-level mapping, NOT yet an outcome-label adapter.

Do not map numeric ACC/COM scores to ACAD_PASS PASS/REJECT until the exact score scale, aggregation record, denominator, and threshold contract are frozen.

---

## 6. 2024 physical TSV schema status

Zenodo archive preview confirms 19 TSV member files.

Examples:
- `GPT.tsv`
- `LLaMA-8B-4bit-MedicalAbstract-seq-to-seq-v1.tsv`
- `LLaMa_3.1_70B_instruction_2nd_run.tsv`
- `TREC2024_SIB_run1.tsv`
- `TREC2024_SIB_run3.tsv`
- `TREC2024_SIB_run4.tsv`
- `UAms-BART-Cochrane.tsv`
- `UAms-ConBART-Cochrane.tsv`
- `plaba_um_fhs_sub1.tsv`
- `plaba_um_fhs_sub2.tsv`
- `plaba_um_fhs_sub3.tsv`

However, exact 2024 TSV column headers cannot currently be extracted through the available binary-preview tooling.

Therefore:

`2024 LOGICAL SCHEMA = FROZEN`

`2024 PHYSICAL COLUMN SCHEMA = NOT YET FROZEN`

This blocks final adapter implementation but does not invalidate the H1 construct choice.

---

## 7. Source-cluster rule

Primary H1 independence unit:

`ORIGINAL BIOMEDICAL ABSTRACT / PMID`

All of the following remain within the same source cluster:
- all sentences from one abstract;
- all system rewrites of that abstract;
- all annotator judgments of those rewrites;
- all derived local relation checks.

The 400 test abstracts are the candidate maximum H1 source-cluster pool.

Do NOT count:
- sentences,
- system runs,
- annotations,
- ACC/COM axes

as independent studies.

Exact PMID mapping remains to be extracted from the source/test corpus before Condition 5 can pass.

---

## 8. Usage / terms freeze

### 8.1 TREC general research-use framework

NIST/TREC states that past track datasets become long-term community research resources, subject to data-sharing terms.

The standard TREC organization agreement permits use for research and development of:
- NLP;
- information retrieval;
- document understanding systems.

It allows publication of summaries, analyses, and interpretations, and small excerpts in scientific/technical contexts, subject to copyright restrictions.

The standard agreement restricts unauthorized redistribution/publication of underlying protected text.

TREC dissemination guidance requires fair, objective scientific reporting and clear description of evaluation limitations.

### 8.2 PLABA-specific status

The current public PLABA 2024 data page exposes the Task 2 test ZIP directly without an authentication barrier.

No separate PLABA-specific data-sharing agreement was found during this checkpoint.

Therefore ACAD_PASS freezes the conservative policy:

`RESEARCH USE ONLY`

`NO RAW TREC/PLABA TEXT REDISTRIBUTION IN THE ACAD_PASS REPOSITORY`

`STORE ONLY IDS / HASHES / DERIVED METRICS / PROTOCOL METADATA IN THE PUBLIC REPOSITORY`

If a specific PLABA agreement is later found, it supersedes this conservative interpretation.

### 8.3 Zenodo manual-judgment archive

Zenodo marks the record:
`Open`

but the rendered record does not display a specific license value.

Therefore:

`PUBLIC ACCESS = VERIFIED`

`EXPLICIT LICENSE = NOT VERIFIED`

The raw judgment ZIP should not be redistributed in the ACAD_PASS repository until explicit reuse terms are documented.

---

## 9. H1 admissible public claim about the artifact

Allowed now:

“ACAD_PASS has identified and preregistered the public Zenodo record and publisher checksums for the PLABA 2024 expert manual judgments, and the public NIST/TREC route for the corresponding complete-adaptation source corpus.”

Not allowed now:
- “local artifact integrity independently verified”;
- “SHA-256 frozen”;
- “license unrestricted”;
- “all 400 PMIDs frozen”;
- “adapter frozen”;
- “H1 ready for execution”.

---

## 10. Current H1 freeze state

Artifact identity:
`PASS`

Publisher checksum:
`PASS`

Public source/test URL:
`PASS`

Construct mapping:
`PASS AT LOGICAL LEVEL`

Physical 2024 TSV schema:
`NOT READY`

Local byte hash:
`NOT READY`

Exact PMID/source-cluster manifest:
`NOT READY`

Exact reuse/license documentation:
`PARTIAL / NOT PASS`

Adapter:
`NOT READY`

Metrics/thresholds:
`NOT READY`

Overall H1 execution readiness:
`NOT_READY`

---

## 11. Blocking issue

The remaining blocker is now narrow:

`PHYSICAL ARTIFACT EXTRACTION + EXACT RECORD SCHEMA`

This is primarily a tooling/access-materialization issue, not a scientific construct problem.

If the user can provide the downloaded ZIPs directly, the next agent can immediately:
- compute SHA-256;
- inspect every TSV header;
- count records;
- extract abstract/question identifiers;
- build PMID/source-cluster manifest;
- freeze exact adapter schema.

Requested external files, if manual upload becomes necessary:

1.
`manual-judgments-task1-2024.zip`

2.
`PLABA_2024-Task_2.zip`

No other file is currently required for the core H1 freeze.

---

## 12. Exact next checkpoint

`H1 PHYSICAL SCHEMA + SOURCE-CLUSTER FREEZE`

Preferred path:
materialize the two public ZIPs and inspect them without running V2.4.

If direct materialization remains impossible:
ask the user to upload those two exact public files.

Still prohibited:
- V2.4 external predictions;
- benchmark scoring;
- tuning;
- original custom Gate C opening;
- new-human recruitment;
- Arabic-track work.
