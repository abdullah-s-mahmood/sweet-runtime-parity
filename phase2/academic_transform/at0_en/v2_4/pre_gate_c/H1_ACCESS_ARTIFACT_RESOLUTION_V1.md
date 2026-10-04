# ACAD_PASS — H1 Access + Artifact Resolution V1

Date: 2026-10-04
Status: SUBSTANTIAL H1 ARTIFACT RESOLUTION / NO VERIFIER EXECUTION

Parent audit:
`H1_DATASET_VERSION_ACCESS_LABEL_AUDIT_V1.md`

Protocol:
`GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

Purpose:
resolve the H1 access/artifact blockers as far as public primary evidence permits, without running frozen V2.4 on any external evaluation record.

---

## 1. Major resolution: PLABA/TREC raw human judgments are publicly archived

A public Zenodo dataset now provides the raw PLABA manual judgments for TREC 2023-2024.

Record:
`Plain Language Adaptation of Biomedical Abstracts (PLABA) at TREC 2023-2024`

Zenodo DOI:
`10.5281/zenodo.18637045`

Resource type:
`Dataset`

Publisher:
`Zenodo`

Related publication:
`10.1016/j.jbi.2026.104983`

Zenodo record version observed:
`v2`

Public files and publisher-provided checksums:

1. `manual-judgments-task1-2023.csv`
   - size: 1.0 MB
   - MD5: `0f320090ce516d799b4e970ebb3194a4`

2. `manual-judgments-task1-2024.zip`
   - size: 7.1 MB
   - MD5: `589ad66e0b9324592f0151cc67974015`

3. `manual-judgments-task2-2024.zip`
   - size: 712.5 kB
   - MD5: `c23fe9c96addedb9c8ad4a8901734996`

Important:
these are publisher-provided MD5 checksums.
Local SHA-256 hashes are still pending because the current execution environment could not directly download the binary ZIP files.

The 2023 CSV is directly web-readable and exposes raw fields including:
- Source
- Output
- Answer
- sentence/term simplicity
- term accuracy
- fluency
- accuracy completeness
- accuracy faithfulness
- Team
- sentence index
- abstract/question identifier

This confirms the archive contains record-level manual gold rather than only aggregate leaderboard scores.

---

## 2. Critical task-numbering normalization

There is a naming mismatch that MUST be preserved.

### Original TREC 2024 task naming

Official 2024 track page:

`Task 1 = Term Replacement`

`Task 2 = Complete Abstract Adaptation`

### Retrospective PLABA paper / Zenodo naming

The later retrospective publication normalizes the historical task taxonomy as:

`Task 1 = Rewriting abstracts`

`Task 2 = Identifying/replacing difficult terms`

It explicitly describes 2024 rewriting results under:
`Task 1 at TREC 2024`

Therefore the Zenodo archive:

`manual-judgments-task1-2024.zip`

is the archive corresponding to COMPLETE ABSTRACT REWRITING / ADAPTATION judgments.

Do NOT select:

`manual-judgments-task2-2024.zip`

for H1 complete-rewrite fidelity merely because the original 2024 event webpage called complete adaptation “Task 2”.

This naming mismatch is now permanent negative/ambiguity evidence and must be checked by any future adapter.

---

## 3. TREC 2024 rewrite judgment structure

The retrospective peer-reviewed paper defines the 2024 complete-rewrite manual axes as:

- `SIM` — simplicity
- `ACC` — accuracy: does the output accurately reflect the source?
- `COM` — completeness: does the output minimize information loss?
- `BRV` — brevity
- `FIN` — average of the four axes

The paper also states:
- manual evaluation is the gold standard;
- 19 complete-rewrite submissions were evaluated in 2024;
- results were based on sentence-level outputs for all 400 test abstracts;
- accuracy and completeness are separate axes in 2024.

This is an unusually direct match to the two ACAD_PASS H1 functions:

`H1-S = output-content support/factuality`
maps conceptually to:
`ACC`

`H1-C = required-content preservation/completeness`
maps conceptually to:
`COM`

This does NOT yet authorize a binary PASS/REJECT mapping.
The native human scores/labels must first be inspected and a preregistered threshold/native-metric contract frozen.

---

## 4. Archive structure evidence

Zenodo preview of:

`manual-judgments-task1-2024.zip`

shows 19 TSV files, matching the 19 complete-rewrite submissions reported in the retrospective paper.

Examples include:
- `GPT.tsv`
- `LLaMA-8B-4bit-MedicalAbstract-seq-to-seq-v1.tsv`
- `LLaMa_3.1_70B_instruction_2nd_run.tsv`
- `TREC2024_SIB_run1.tsv`
- `TREC2024_SIB_run3.tsv`
- `TREC2024_SIB_run4.tsv`
- `UAms-BART-Cochrane.tsv`
- `UAms-ConBART-Cochrane.tsv`
- additional submitted run TSVs

This strongly supports that the archive is the record-level 2024 manual evaluation material.

Exact TSV column schemas remain to be frozen from the actual extracted bytes.

---

## 5. TREC 2024 source/test corpus access

The public NIST/TREC data index now exposes direct links for PLABA 2024 task corpora.

Original 2024 event naming:
- Task 1 ZIP = term replacement
- Task 2 ZIP = complete abstract adaptation

Public complete-adaptation corpus URL:
`https://trec.nist.gov/data/plaba/PLABA_2024-Task_2.zip`

The TREC browser metadata independently confirms this exact public URL.

Thus the source/test corpus access route is no longer considered participant-only in the current public archive state.

Binary bytes still need a local reproducible copy/hash before final execution freeze.

---

## 6. Research-use / rights status

### TREC / NIST

TREC states that its datasets become long-term community research resources, generally subject to a lightweight NIST data-sharing agreement.

The standard TREC research-collection agreement permits use for research/development of NLP, information-retrieval or document-understanding systems, with publication of summaries/analyses under the stated restrictions.

TREC dissemination rules permit scientific/technical publication while restricting advertising/marketing use.

Therefore:
`RESEARCH-USE PATH = IDENTIFIED`

But:
- any applicable TREC organizational/individual agreement must be satisfied before execution if required for these specific files;
- redistribution rights must not be assumed.

### Zenodo PLABA manual judgments

The Zenodo record is publicly marked:
`Open`

However, its current rendered metadata has a `Rights / License` section with no explicit license value.

Therefore:
`PUBLIC DOWNLOAD ACCESS = VERIFIED`

`EXPLICIT ZENODO LICENSE = NOT DECLARED/NOT VERIFIED`

Do not equate “Open” with an unrestricted redistribution license.

This remains a rights-documentation blocker for final artifact freeze, though not an identity/provenance blocker.

---

## 7. FaReBio conditional substitute — access status improved

Resource:
`FaReBio`

Paper:
`Understanding Faithfulness and Reasoning of Large Language Models on Plain Biomedical Summaries`

ACL DOI:
`10.18653/v1/2024.findings-emnlp.578`

Dataset DOI:
`10.25919/6v9c-bw57`

CSIRO Data Access Portal:
`Version 1`
dated:
`2024-11-01`

Published dataset description:
- 25 English biomedical source articles;
- 175 plain summaries;
- 1,445 sentences;
- outputs from 7 LLMs;
- expert annotations for faithfulness and supporting evidence/reasoning.

CSIRO presentation explicitly describes the dataset as:
`open to public for research only`

Construct:
- strong conditional `H1-S` resource;
- NOT a standalone `H1-C` completeness resource.

Exact artifact bytes/hashes were not acquired through the current non-JavaScript path.

Status:
`IDENTITY + RESEARCH-USE TERMS + CONSTRUCT VERIFIED / BYTE HASH PENDING`

---

## 8. FactPICO conditional substitute — access status

Repository:
`lilywchen/FactPICO`

ACL 2024 resource:
`FactPICO`

Repository license:
`MIT`

The repository data README directs users to a UT Austin Box download.

Construct:
- expert fine-grained PICO/finding factuality/preservation;
- conditional domain-specific H1 gap filler;
- not a general full-document completeness certificate.

Important rights boundary:
the GitHub repository MIT license does NOT automatically establish that separately hosted Box dataset files carry the same license.

Status:
`REPO LICENSE VERIFIED / EXTERNAL DATA TERMS + BYTES NOT YET FROZEN`

---

## 9. SimpleText 2025 status

No new public standalone human-annotation artifact or explicit dataset license was found during this resolution pass.

Still verified:
- human annotations of real 2025 system outputs exist;
- 2026 officially reuses manual 2025 annotations as ground truth for information-distortion classification;
- access is available through participant/Codabench workflow.

Current status:
`OPTIONAL / ACCESS-GATED / NOT REQUIRED TO BLOCK H1 IF TREC CONTRACT SUFFICES`

SimpleText remains valuable for broader scientific-transformation evidence, but ACAD_PASS should not stall H1 solely on SimpleText if a valid TREC-based H1 contract is frozen.

---

## 10. Revised H1 core recommendation

The second independent review explicitly allowed a single resource to satisfy H1 if its human evaluation contract genuinely covers BOTH required functions.

Current strongest core candidate:

`TREC PLABA 2024 COMPLETE-REWRITE MANUAL JUDGMENTS`

Why:
- authentic scientific/biomedical source abstracts;
- external system transformations;
- biomedical expert human evaluation;
- `ACC` directly targets source accuracy;
- `COM` directly targets information preservation;
- all 400 test abstracts were represented in sentence-level complete-rewrite evaluation;
- raw manual judgment archive is publicly identified with checksums.

Therefore the preferred H1 freeze strategy becomes:

### H1 CORE
`TREC PLABA 2024 rewrite manual judgments`

for:
- H1-S via `ACC`;
- H1-C via `COM`.

### H1 INDEPENDENT SUPPORT / CONDITIONAL
`FaReBio`

for:
- independent expert faithfulness/evidence diagnostics;
- optional H1-S corroboration if its artifact can be frozen cleanly.

### H1 DOMAIN-SPECIFIC CONDITIONAL
`FactPICO`

only if a PICO/finding-preservation gap is specifically identified.

### OPTIONAL / BROADER TRANSFORMATION
`CLEF SimpleText 2025`

retain as optional until official record-level annotations/terms are accessible.

### DIAGNOSTIC
`LongSciVerify`

unchanged.

This recommendation does NOT yet mean H1 is execution-ready.

---

## 11. Remaining H1 blockers before adapter freeze

### R1 — obtain/freeze actual 2024 manual-judgment ZIP bytes
Publisher MD5 exists, but a local reproducible byte copy and preferably SHA-256 are still pending.

### R2 — inspect exact TSV schema
Need exact per-record:
- source identifier;
- output identifier;
- source text;
- candidate output;
- ACC;
- COM;
- annotator/aggregation fields;
- sentence/abstract mapping.

### R3 — freeze source/test corpus bytes and identifiers
Public TREC URL is identified; local hash still pending.

### R4 — resolve applicable use agreement
Need record of the exact TREC agreement/terms applicable to ACAD_PASS reuse.

### R5 — freeze H1 score semantics
Need decide, before any V2.4 prediction:
- native-score evaluation vs exact preregistered mapping;
- threshold(s), if any;
- denominator;
- treatment of uncertain/missing judgments;
- source-cluster unit.

### R6 — source cluster mapping
Need map all sentence judgments back to 400 original PubMed abstracts and then cluster by original study/PMID.

No verifier execution is needed to resolve R1-R6.

---

## 12. Readiness impact

Condition 1:
`PASS`

Condition 2:
`SUBSTANTIAL PARTIAL / NOT YET PASS`

Improved because:
- exact Zenodo manual-judgment artifacts are identified;
- publisher checksums are available;
- public TREC corpus URL is identified;
- research-use path is documented.

Still not PASS because:
- local bytes/SHA-256 not frozen;
- exact applicable reuse agreement not frozen;
- Zenodo record has no explicit displayed license.

Condition 3:
`SUBSTANTIAL PARTIAL / NOT YET PASS`

Improved because:
- record-level judgment archive is proven;
- H1-S/H1-C human constructs and 400-abstract test scope are identified.

Still not PASS because:
- exact TSV record IDs/schema have not been extracted/frozen.

Condition 4:
`NOT READY`

No adapter is frozen yet.

Overall:
`NOT_READY_GATE_C_EXT_META`

---

## 13. Quality delta

`IMPROVED`

Compared with the previous H1 audit:
- the strongest TREC human-gold artifact is no longer merely hypothetical/inaccessible;
- exact public Zenodo files and checksums are known;
- the task-numbering ambiguity is resolved;
- a single coherent H1 core candidate now covers both required functions conceptually;
- SimpleText access is no longer a mandatory blocker.

No scientific performance metric changed because no verifier prediction was run.

---

## 14. Exact next checkpoint

`H1 RAW ARTIFACT + SCHEMA + TERMS FREEZE`

Authorized:
1. obtain/freeze exact TREC 2024 judgment bytes if tooling permits;
2. inspect TSV schema without running V2.4;
3. freeze public test corpus identifiers/bytes;
4. document applicable TREC reuse agreement;
5. freeze PMID/source-cluster mapping;
6. draft H1 adapter/metric contract only after 1-5.

Not authorized:
- V2.4 prediction;
- external benchmark scoring;
- tuning;
- original custom Gate C opening;
- new human recruitment;
- Arabic-track work.
