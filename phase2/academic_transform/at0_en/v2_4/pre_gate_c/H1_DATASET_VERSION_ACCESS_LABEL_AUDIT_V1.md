# ACAD_PASS — H1 Dataset / Version / Access / Label Audit V1

Date: 2026-10-04
Status: H1 PARTIAL FREEZE / NO VERIFIER EXECUTION

Protocol:
`GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

Purpose:
freeze what is currently defensible about the two primary H1 candidates before any V2.4 prediction is run.

This audit does NOT execute any benchmark and does NOT authorize predictions.

---

## 1. CLEF SimpleText 2025

### 1.1 Identity

Official track:
`CLEF 2025 SimpleText`

Official Task 2 paper:
`Overview of the CLEF 2025 SimpleText Task 2: Identify and Avoid Hallucination`
Vendeville, Bakker, Azarbonyad, Ermakova, Kamps.
CLEF 2025 Working Notes, CEUR-WS Vol. 4038, pp. 4186-4204.

Official 2025 track website repository:
`simpletext-madics/2025`

Observed current main HEAD at audit time:
`14cb2f19a5eb7e8d7d3382b241578c5affc5bbac`

Repository license metadata:
`NONE DECLARED AT REPOSITORY LEVEL`

Important:
repository/site license status is NOT sufficient to infer dataset-license status.

### 1.2 Official access facts

Official 2025 task page states:
- track data are made available to registered participants;
- Task 1 evaluates scientific text simplification;
- human assessment is performed on samples of submissions;
- Task 2 focuses on creative generation / information distortion.

Official 2026 SimpleText page states:
- CLEF 2025 submissions were annotated for overgeneration/information distortion;
- manual annotations from CLEF 2025 Task 1 submissions are reused as ground-truth data for CLEF 2026 Task 2 information-distortion classification;
- the CLEF 2025 Task 2 Codabench remains operational.

Current access finding:
- Codabench competition page is public;
- actual data/annotation artifact retrieval is not available through the unauthenticated inspection path used in this audit;
- participant registration/login may be required.

Therefore:
`SIMPLETEXT_ARTIFACT_BYTES_NOT_YET_FROZEN`

### 1.3 Label/schema evidence

Official sources establish that the track contains human-evaluated real system outputs relevant to:
- overgeneration / significant new content;
- information distortion;
- factuality-related evaluation.

A published CLEF 2025 participant paper reports, for planning only:
- Task 2.2 train: 42,392 annotated entries / 35,621 unique simplified sentences;
- Task 2.2 test: 2,659 entries / 1,537 unique source sentences;
- a multi-label error taxonomy including contradiction, factuality hallucination, faithfulness hallucination, topic shift, overgeneralization, overspecification, loss of informative content, and out-of-scope generation.

These counts/taxonomy details are useful provisional evidence but are NOT a substitute for freezing the actual official artifact.

### 1.4 H1 construct fit

Potential H1-S:
`STRONG CANDIDATE`

Reason:
human annotations of real simplification outputs directly address unsupported/distorted generated content.

Potential H1-C:
`POSSIBLE BUT NOT YET PROVEN AS SUFFICIENT`

Reason:
loss-of-informative-content/distortion labels may contribute to preservation/completeness, but exact human-label scope, denominator and coverage must be inspected in the official artifact before ACAD_PASS may claim that H1-C is covered.

### 1.5 Current SimpleText freeze state

Dataset/version identity:
`PARTIAL PASS`

Exact artifact files:
`NOT READY`

Artifact hashes:
`NOT READY`

Dataset-specific license:
`NOT VERIFIED`

Eligible IDs/splits:
`NOT READY`

Exact human-label provenance per selected record:
`NOT READY`

Adapter contract:
`NOT READY`

H1-S candidacy:
`SUPPORTED FOR FURTHER FREEZE`

H1-C candidacy:
`UNRESOLVED UNTIL LABEL ARTIFACT INSPECTION`

---

## 2. PLABA original dataset

### 2.1 Identity

Dataset:
`Plain Language Adaptation of Biomedical Abstracts (PLABA)`

Version-of-record paper:
Attal, Ondov, Demner-Fushman.
Scientific Data 10, 8 (2023).

DOI:
`10.1038/s41597-022-01920-3`

Public archive:
OSF project:
`rnpmf`

Official PLABA repository:
`attal-kush/PLABA`

Canonical public data file named by official sources:
`data.json`

Official data size description:
- 750 biomedical abstracts;
- 7,643 aligned sentence pairs;
- each abstract manually adapted to plain language by at least one annotator.

The Scientific Data paper states that data are organized by question ID and PubMed ID (PMID).

### 2.2 License/access

The Scientific Data article is CC BY 4.0 and describes the dataset as publicly archived on OSF.

However:
- a separate machine-verifiable dataset-license record was NOT obtained in this audit;
- direct OSF artifact retrieval failed through the current tool path;
- therefore the dataset bytes and SHA-256 cannot yet be frozen.

Status:
`PLABA_PUBLIC_IDENTITY_VERIFIED / DATASET_LICENSE_SEPARATELY_UNVERIFIED / ARTIFACT_HASH_PENDING`

Do NOT infer that the dataset itself is CC BY 4.0 solely because the article is CC BY 4.0.

### 2.3 Construct limitation

The original PLABA adaptation task explicitly permits:
- splitting source sentences;
- omitting source sentences.

Therefore:
`HUMAN-WRITTEN PLABA REFERENCE != AUTOMATIC FULL-CONTENT PASS GOLD`

PLABA raw references can support authentic scientific transformation research, but H1-C must not be inferred from reference existence alone.

---

## 3. TREC PLABA 2023

Official NLM/NIST task page:
`PLABA at TAC/TREC 2023`

Test design:
- 40 consumer questions;
- 10 retrieved abstracts per question.

Manual evaluation:
experts rank outputs.

For every sentence:
- sentence simplicity;
- term simplicity;
- term accuracy;
- fluency.

For up to 3 sentences judged most relevant to the consumer question:
- completeness;
- faithfulness.

Important construct boundary:
2023 completeness/faithfulness is QUESTION-RELEVANT SENTENCE-SAMPLED evaluation, not proof that every source assertion in the entire abstract is preserved.

Therefore:
`TREC-2023 H1-C = PARTIAL / SAMPLED-SCOPE ONLY`

---

## 4. TREC PLABA 2024

Official NLM/NIST page:
`PLABA at TREC 2024`

Task 2:
complete end-to-end adaptation of biomedical abstracts.

Official expert manual evaluation dimensions:
- simplicity;
- accuracy;
- completeness;
- brevity.

Official definition:
completeness asks systems to minimize information lost from the original text.

This is currently the strongest identified PLABA-family candidate for H1-C.

Published retrospective evidence:
`Lessons from the TREC Plain Language Adaptation of Biomedical Abstracts (PLABA) track`
reports:
- 2023 and 2024 PLABA tracks;
- four professionally written references for automatic evaluation of Task 1;
- extensive manual evaluation by biomedical experts;
- manual judgments of factual accuracy and completeness.

### 4.1 Access limitation

Official TREC 2024 site states that:
- Task 2 test data are available in the TREC active-participants area;
- judgments were returned after submission.

The actual reusable test/judgment artifact and reuse/license terms have NOT yet been frozen.

Therefore:
`TREC-2024 HUMAN-JUDGMENT ARTIFACT = ACCESS/REUSE NOT YET FROZEN`

### 4.2 H1 construct fit

H1-S:
`STRONG CANDIDATE`
via expert accuracy/faithfulness judgments.

H1-C:
`STRONGEST CURRENT PLABA-FAMILY CANDIDATE`
via expert completeness judgments on complete abstract adaptation.

But no ACAD_PASS hard-gate use is authorized until:
- exact judgment records are accessible;
- their record-level source/candidate mapping is frozen;
- reuse terms are established;
- denominators and source clusters are frozen.

---

## 5. Current H1 decision

### 5.1 What is now frozen conceptually

H1 must remain function-based:

`H1-S = output content support/factuality`

`H1-C = preservation/completeness of required source content`

### 5.2 Preferred evidence order

For H1-S:
1. CLEF SimpleText 2025 real human-annotated outputs;
2. TREC PLABA expert accuracy/faithfulness judgments;
3. FaReBio only if a support/factuality gap remains.

For H1-C:
1. TREC PLABA 2024 expert completeness judgments, if reusable at record level;
2. CLEF SimpleText human distortion/content-loss labels only if official artifact inspection proves sufficient coverage;
3. FactPICO only as a conditional domain-specific gap filler.

### 5.3 LongSciVerify

Remains:
`DIAGNOSTIC ONLY`

It is not promoted to a hard H1 requirement.

---

## 6. Readiness impact

Condition 1 — independent protocol review:
`PASS`

Condition 2 — exact dataset artifacts/versions/access/licenses:
`H1 PARTIAL / NOT PASS`

Condition 3 — eligible splits/IDs/human-label provenance/context:
`H1 PARTIAL / NOT PASS`

Condition 4 — dataset-specific adapter contracts:
`NOT READY`

No later readiness condition is upgraded by this audit.

Overall:
`NOT_READY_GATE_C_EXT_META`

---

## 7. Blockers discovered

### B1 — SimpleText official annotation artifact
Need exact downloadable/registered artifact containing the 2025 human annotations used/reused as ground truth.

### B2 — SimpleText dataset license/reuse terms
No explicit dataset license was verified from the public website repository metadata.

### B3 — PLABA OSF artifact bytes
Public identity is established, but direct download/hashing is still pending.

### B4 — PLABA dataset license
Article license is verified; dataset-specific license still requires explicit confirmation.

### B5 — TREC 2024 judgment artifact
Need access to record-level expert accuracy/completeness judgments or an official reusable equivalent.

### B6 — TREC reuse terms
Need explicit confirmation that the judgments/test records may be reused in ACAD_PASS evaluation.

These are DATA ACCESS/PROVENANCE blockers, not V2.4 failures.

---

## 8. Negative-evidence preservation

Do not erase these limitations:
- SimpleText public task descriptions do not by themselves freeze the annotation bytes.
- Human evaluation of samples is not equivalent to complete record-level gold.
- PLABA human references allow omission and are not automatic full-preservation PASS labels.
- TREC 2023 completeness/faithfulness applies only to selected question-relevant sentences.
- TREC 2024 is stronger for H1-C, but actual judgment artifact reuse/access is not yet established.
- article licensing must not be silently substituted for dataset licensing.

---

## 9. Exact next checkpoint

`H1 ACCESS + ARTIFACT RESOLUTION`

Authorized work:
1. identify an official downloadable SimpleText 2025 human-annotation artifact or registration route;
2. establish SimpleText data reuse/license terms;
3. obtain or independently verify PLABA OSF artifact/license metadata;
4. identify TREC 2024 expert-judgment artifact availability/reuse path;
5. only then freeze exact IDs/hashes and draft H1 adapters.

Still prohibited:
- V2.4 predictions;
- benchmark scoring;
- tuning;
- original custom Gate C opening;
- new-human recruitment.
