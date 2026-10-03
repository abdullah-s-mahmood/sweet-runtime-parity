# ACAD_PASS — External Human-Gold Composite Feasibility Audit V1

Date: 2026-10-04
Status: CLOSED FEASIBILITY AUDIT / NO RUNTIME CHANGE / CUSTOM HOLDOUT UNOPENED

## Executive verdict

`FEASIBLE_WITHOUT_NEW_HUMAN_ADJUDICATORS_FOR_RESEARCH_PROGRESSION`

A scientifically defensible Gate C can be built without recruiting new human adjudicators by combining:

1. independently published human/expert-gold datasets that directly or closely measure source-grounded factual fidelity;
2. scientific/academic rewrite and simplification datasets with expert/human references;
3. fine-grained relation-level human annotations;
4. deterministic ACAD_PASS-specific metamorphic tests for relation mutations whose oracle is known by construction.

This does NOT establish that bespoke fresh human adjudication is unnecessary for every future product/adoption claim.

It DOES support replacing the current custom 80-study/new-human Gate C as the primary research-progression gate, subject to a final construct-validity review before protocol replacement.

## Why the alternative is unusually viable here

The frozen V2.4 verifier:
- uses no external model inference;
- is frozen before the external composite is selected;
- was not trained on these benchmarks;
- is evaluated as fixed code.

Therefore benchmark memorization by the verifier is not the main contamination mechanism.

Primary validity risks are instead:
- prior manual exposure during ACAD_PASS development;
- construct mismatch;
- duplicate source/candidate pairs across benchmark aggregators;
- label-adapter mistakes;
- post-result tuning.

These can be controlled by protocol.

---

## Dataset audit

### Tier A — PRIMARY CORE: closest to ACAD_PASS

### A1. DeFacto — HUMAN CORRECTION / REPAIR

Official source:
`microsoft/DeFacto`

Availability:
PUBLIC.

Repository license:
MIT.

Size:
- Train: 1000
- Val: 486
- Test: 1075
- Total: 2561
- With errors: 1821

Human record contains:
- factual-consistency decision;
- intrinsic/extrinsic error type;
- natural-language explanation;
- selected source evidence sentence;
- corrective instruction;
- human-corrected summary.

Direct ACAD_PASS use:
- source = article
- negative candidate = original system summary when has_error=true
- positive candidate = human-corrected summary
- evidence audit = selected human evidence
- repair-quality diagnostic = instruction/explanation

Construct fit:
VERY HIGH for `DETECT RISK -> REPAIR -> RE-VERIFY`.

Limit:
news summarization rather than academic prose.

Decision:
`PRIMARY CORE / READY`

Do not use downstream derivatives of DeFacto as independent evidence if the same doc_id appears.

---

### A2. PLABA — EXPERT SCIENTIFIC REWRITING / SIMPLIFICATION

Published scientific dataset:
Plain Language Adaptation of Biomedical Abstracts.

Availability:
PUBLIC dataset available separately from code.

Core size:
- 750 PubMed abstracts
- 75 health topics
- 7643 sentence pairs
- each abstract manually adapted by at least one expert annotator

The dataset was deliberately designed as:
- document-level simplification gold;
- sentence-level parallel simplification gold.

TREC PLABA additional evidence:
- task test sets with professionally written references;
- 2023 test used four expert references per sentence;
- 2023/2024 system outputs received biomedical-expert manual judgments;
- faithfulness explicitly asks whether output statements match source statements;
- completeness explicitly evaluates information loss.

Direct ACAD_PASS use:
- source = biomedical abstract/sentence
- candidate = expert plain-language adaptation
- expected = faithful transformation / PASS-equivalent
- use document and sentence alignment to test split/merge and scientific meaning preservation.

Construct fit:
VERY HIGH for authentic scientific transformation.

Limit:
biomedical domain and simplification goal; not all academic-editing styles.

Decision:
`PRIMARY CORE / READY FOR POSITIVE-FIDELITY TRACK`

Raw TREC system-output human judgments should be used only if public/downloadable records are verified before freeze.

---

### A3. CLEF SimpleText 2025 Task 2 — SCIENTIFIC DISTORTION / HALLUCINATION

Official goal:
scientific simplification with strict faithfulness and controlled creativity.

Task 2.1:
- source-aligned hallucination detection;
- train roughly 13.5K source-aligned labeled sentences;
- test roughly 3.3K.

Task 2.2:
- detect/classify information-distortion errors in simplified scientific sentences;
- 14 distortion categories;
- train 42,392 labeled entries / 35,621 unique simplified sentences;
- test 2,659 entries derived from 1,537 source sentences;
- official overview states real CLEF submissions were manually annotated/reused as ground truth for later work.

2026 SimpleText explicitly reuses the human annotations from 2025 Task 1 submissions as ground truth for information-distortion detection.

Direct ACAD_PASS use:
- source = scientific sentence/text
- candidate = simplified output
- error label = information-distortion type
- positive/negative source-grounded fidelity.

Construct fit:
EXTREMELY HIGH.

Access:
official track data requires/required CLEF registration; 2025 Codabench remains operational according to 2026 track information.

Important distinction:
- synthetic Task 2.2 training mutations are NOT independent human-gold negatives;
- manually annotated real-submission material is the preferred external-gold portion.

Decision:
`PRIMARY CORE / CONDITIONAL ON DATA ACCESS AND FINAL LABEL FILE AVAILABILITY`

If accessible, this is the strongest direct replacement for bespoke academic human adjudication.

---

### A4. SciFact — EXPERT SCIENTIFIC CLAIM/EVIDENCE

Availability:
PUBLIC.

Official repository license detail:
- claims and evidence annotations: CC BY 4.0
- S2ORC abstracts: ODC-By 1.0
- code: Apache 2.0

Public labels:
- train/dev labeled;
- official test labels not publicly released.

Dataset:
~1.4K expert-written scientific claims, evidence abstracts, SUPPORT/CONTRADICT rationales.

Direct ACAD_PASS adapter:
- source = evidence abstract/document
- candidate = scientific claim
- SUPPORT -> PASS-like source support
- CONTRADICT -> REJECT-like material scientific contradiction
- human rationale -> evidence fidelity audit

Do not force no-evidence cases to REVIEW without a separate adapter justification.

Construct fit:
HIGH for scientific assertion/evidence verification.

Limit:
claim verification rather than rewrite fidelity.

Decision:
`PRIMARY CORE / READY`

Use only public labeled splits and freeze exact examples before execution.

---

### A5. QASemConsistency — FINE-GRAINED RELATION SUPPORT

Availability:
PUBLIC repository + data.

Repository license:
Apache 2.0.

Scale:
>3000 human-annotated instances across attributable-generation tasks.

Annotation level:
- predicate-argument QA pairs;
- raw multiple annotations;
- supported vs hallucinated relation judgments;
- span localization.

Direct ACAD_PASS use:
- source = grounding document
- candidate = generated text
- relation unit = predicate-argument QA
- critical relation support/unsupported diagnostic
- evidence localization

Construct fit:
EXTREMELY HIGH for SAF/ARG relation correctness.

Important overlap:
underlying source datasets include CLIFF / FactScore / verifiability data.
Do not count overlapping underlying source instances again in aggregate factuality suites.

Decision:
`PRIMARY CORE / READY`

Use relation-level metrics natively; do not coerce all instances into one PASS/REJECT decision unless adapter is preregistered.

---

### A6. USB — HUMAN EVIDENCE + FACTUALITY + ERROR CORRECTION

Availability:
PUBLIC Hugging Face dataset.

License:
Apache 2.0.

Scale:
dataset card: 1K–10K examples.

Human-labeled tasks include:
- evidence for summary sentence;
- factual accuracy;
- unsubstantiated-span identification;
- correcting factual errors.

Domains:
6 Wikipedia-derived domains.

Direct ACAD_PASS use:
- source/candidate factuality
- evidence span
- error localization
- human corrected output

Construct fit:
HIGH for `VERIFY -> RISK -> REPAIR`.

Limit:
Wikipedia summarization, not academic prose.

Decision:
`PRIMARY CORE / READY`

---

### A7. PlainFact — BIOMEDICAL FACTUAL / CONTRASTIVE

Availability:
PUBLIC Hugging Face.

License:
CC BY-SA 3.0.

Scale:
- 200 plain-language summary/abstract pairs
- 2740 sentence-level rows

Fields:
- factual target sentence
- non-factual contrast
- original scientific abstract
- external-information flag

Dataset is described as human-annotated with fine-grained explanation annotations.
Non-factual contrasts are generated by GPT-4o using predefined perturbation criteria.

Direct ACAD_PASS use:
- factual sentence + scientific abstract = positive track
- contrasting sentence = negative stress track

Critical caution:
do not call every generated non-factual contrast independent human-gold unless the released artifact/paper confirms human validation of that exact contrast.

Decision:
`PRIMARY BIOMEDICAL POSITIVE TRACK / NEGATIVE TRACK CONDITIONAL`

---

## Tier B — SECONDARY / DIAGNOSTIC

### B1. QASPER

Availability:
PUBLIC.
License:
CC BY 4.0.

Scale:
- 5049 questions
- 1585 full NLP research papers
- human/practitioner answers
- supporting evidence passages
- unanswerable cases

Strength:
authentic research-paper full-text grounding and evidence localization.

Use:
- evidence completeness
- document-level grounding
- context sufficiency / abstention diagnostics

Do NOT force QA labels into ACAD_PASS PASS/REJECT without a valid semantic adapter.

Decision:
`SECONDARY EVIDENCE-GROUNDING TRACK`

---

### B2. TRUE

Availability:
PUBLIC code + standardized download script.

Composition:
11 manually annotated factual-consistency datasets standardized to:
- grounding
- generated_text
- binary label

Strength:
multi-task cross-domain factual consistency.

Major caution:
TRUE is an aggregator.
Its component datasets overlap with other aggregators and original benchmarks.

Decision:
`SECONDARY TRANSFER TRACK`

Never count TRUE examples plus their original dataset copies as independent evidence.

---

### B3. AggreFact

Availability:
PUBLIC data in repository.

Composition:
factuality annotations aggregated from 9 existing datasets.

Strength:
stratifies by summarizer generation era and error type.

Caution:
aggregator with substantial overlap with TRUE and original factuality datasets.

No root LICENSE file was found during this audit; component/source licensing must be checked before redistribution.

Decision:
`SECONDARY TRANSFER / ERROR-TYPE TRACK`

Use as one canonical view OR use original datasets, not both for aggregate N.

---

### B4. FENICE story-summeval

Availability:
PUBLIC.
License:
CC BY-NC-SA 4.0.

Scale:
319 story-summary pairs with binary human factuality annotations.

Strength:
long-form factuality.

Limit:
stories, not academic text.

Decision:
`SECONDARY LONG-FORM TRACK`

---

## Tier C — OPTIONAL / CONDITIONAL

### C1. SciFact-Open

Availability:
PUBLIC annotations and 500K abstract corpus.

Strength:
open-domain scientific claim verification.

Important annotation caveat:
- citation evidence highlights inherited from SciFact are hand-annotated;
- pooled evidence labels are human-annotated, but pooled evidence sentence highlights are model-predicted and may be wrong.

Use:
- label-level open-domain scientific stress;
- retrieval/evidence generalization.

Do not use pooled predicted highlights as human evidence gold.

Also overlaps SciFact original claims.

Decision:
`OPTIONAL OPEN-DOMAIN STRESS / DEDUP REQUIRED`

---

### C2. Scientific Text Simplification Human-in-the-Loop Corpus (2026)

Availability:
PUBLIC GitHub.
Intended license:
CC BY 4.0.

Content:
- original expert scientific summaries
- GPT simplifications
- 47-passage human study subset
- expert-edited gold simplifications

Strength:
direct scientific simplification and claim-strength preservation.

Limit:
small; based on SciSummNet/CS.

Decision:
`OPTIONAL DIRECT-SCIENTIFIC QUALITATIVE TRACK`

Useful precisely because its expert-edited outputs are closer to ACAD_PASS than generic news factuality.

---

### C3. Cochrane-auto

Availability:
freely available corpus described in TSAR 2024.

Content:
aligned biomedical abstracts and lay summaries at sentence/paragraph/document level.

Strength:
authentic author-produced document-level simplification.

Caution:
lay summaries may intentionally omit/reframe content for audience goals; cannot automatically interpret every aligned output as strict all-claim-preservation under ACAD_PASS.

Decision:
`OPTIONAL TRANSFORMATION GENERALIZATION / NOT HARD FIDELITY GOLD WITHOUT ADAPTER`

---

## Explicitly rejected as primary evidence

### ARXIVEDITS / natural paper revision corpora

Real author revisions are useful for style/revision research but do not guarantee semantic equivalence.

Do not treat author revision pairs automatically as PASS gold.

### Synthetic-only distortion training sets

Useful for metamorphic diagnostics, but not independent human-gold.

Do not count them as external human validation.

### LLM consensus replacing gold

Not accepted as independent human-gold.
May be used only as diagnostic or adjudication-support in a separate provisional setting.

---

# Overlap / deduplication policy

External validation N must be based on unique underlying source-candidate judgments, not dataset wrappers.

Known overlap controls:

1. SciFact-Open contains SciFact original material.
   - mark `scifact_orig`
   - never count same claim/document twice.

2. TRUE aggregates existing benchmarks.
   - if TRUE standardized instance is used, do not also count same original instance from FRANK/QAGS/etc.

3. AggreFact aggregates 9 prior factuality datasets.
   - do not combine raw AggreFact N with raw original dataset N.

4. QASemConsistency uses underlying datasets including CLIFF / FactScore / verifiability.
   - relation-level QASem annotations may be reported separately;
   - if an underlying whole-instance factuality label also appears elsewhere, it is not an independent source.

5. Derived DeFacto localization datasets are not independent of DeFacto.
   - key by DeFacto doc_id/source hash.

6. PLABA/TREC variants:
   - paper/abstract identity is the cluster unit;
   - multiple references/judgments from one source remain one source cluster for inferential counts.

Required canonical dedup keys where available:
- DOI / PMID / PubMed ID
- arXiv ID
- Semantic Scholar/S2ORC ID
- source URL/document ID
- normalized source SHA-256
- dataset-native source id

---

# Proposed no-new-human Gate C architecture

## Gate C-EXT-1 — Direct scientific transformation fidelity

Primary:
- PLABA expert adaptation
- CLEF SimpleText manually annotated real scientific simplifications if accessible
- Scientific Text Simplification 2026 expert-edited subset

Purpose:
authentic scientific rewrite/simplification fidelity.

## Gate C-EXT-2 — Scientific claim/evidence fidelity

Primary:
- SciFact
- optional non-overlapping SciFact-Open evidence

Purpose:
support/contradict, rationales, scientific evidence.

## Gate C-EXT-3 — Fine-grained relation fidelity

Primary:
- QASemConsistency

Purpose:
predicate-argument relation support and localization.

## Gate C-EXT-4 — Human correction / repair

Primary:
- DeFacto
- USB correction/factuality tasks

Purpose:
fault detection + human repair + evidence.

## Gate C-EXT-5 — Biomedical stress

Primary:
- PLABA
- PlainFact
- optional TREC PLABA human judgments where downloadable

Purpose:
high-risk domain scientific fidelity.

## Gate C-EXT-6 — Cross-domain transfer

Secondary:
- USB
- TRUE or AggreFact (choose canonical representation, deduplicated)
- FENICE story-summeval

Purpose:
test transfer outside academic/scientific source style.

## Gate C-META — deterministic ACAD_PASS relation stress

Authentic source text + frozen deterministic mutations.

PASS-preserving:
- sentence split/merge preserving claims
- safe clause reorder
- safe explicit synonym substitution
- format-only transformation
- citation format change preserving ownership

REJECT-guaranteed:
- owner/value swap
- group-label swap
- explicit negation flip
- unsupported modality strengthening
- association -> causation
- citation-owner swap
- coefficient/variable swap
- denominator/baseline change
- temporal-scope change
- deletion of critical qualifier

REVIEW-oracle:
use only transformations with a formal preregistered information-loss condition.
Do not create REVIEW merely from generic truncation.

---

# Adapter principle

Do NOT force all external datasets into PASS/REJECT/REVIEW.

Each track retains native labels.

An ACAD_PASS outcome adapter is allowed only if the semantic mapping is exact and preregistered.

Examples:

- SciFact SUPPORT on a specified evidence document:
  may map to PASS-like supported assertion.

- SciFact CONTRADICT:
  may map to REJECT-like contradiction.

- DeFacto has_error=true original candidate:
  maps naturally to REJECT-like factual inconsistency.

- DeFacto human-corrected summary:
  maps naturally to PASS-like corrected consistency.

- QASemConsistency:
  report relation support/hallucination natively; candidate-level PASS mapping requires all required relations supported under a frozen aggregation rule.

- QASPER:
  retain QA/evidence metrics; do not force into PASS/REJECT.

- human disagreement:
  never maps automatically to REVIEW.

---

# Can new human adjudication be removed entirely?

## Research-progression verdict

**YES, provisionally as a methodology decision pending one final independent construct-validity consultation.**

The evidence base is sufficiently rich to create:
- direct scientific transformation tracks;
- expert scientific claim/evidence tracks;
- predicate-argument relation tracks;
- human factual correction tracks;
- biomedical expert tracks;
- cross-domain factuality tracks;
- deterministic ACAD_PASS-specific relation oracles.

This is stronger than relying only on generic fact-check datasets.

## Strong-adoption boundary

The external composite can establish:
`NON_PROVISIONAL_EXTERNAL_HUMAN_GOLD_VALIDATION`
for the constructs and domains represented.

It cannot by itself establish:
- prevalence of errors in real ACAD_PASS user traffic;
- every academic discipline;
- full-document fidelity if only passages/abstracts are evaluated;
- product UX/review workflow quality;
- true <1% production error without appropriately powered independent deployment-distribution evidence.

Fresh bespoke human adjudication is therefore:
`NOT REQUIRED FOR NEXT RESEARCH PROGRESSION`

and can be:
`DEFERRED / OPTIONAL TARGETED RESIDUAL VALIDATION`

only if a future construct gap or reviewer requirement remains.

---

# Feasibility decision table

| Resource | Public/access | Human/expert gold | Directness to ACAD_PASS | Role |
|---|---|---|---|---|
| DeFacto | Public, MIT | Yes | Very high repair/fidelity | Core |
| PLABA | Public | Expert adaptations | Very high scientific rewrite | Core |
| CLEF SimpleText 2025 | Registration/Codabench | Real submissions manually annotated; synthetic train also exists | Extremely high | Core if accessible |
| SciFact | Public; annotation license clear | Expert | High scientific evidence | Core |
| QASemConsistency | Public, Apache-2.0 | Multi-annotator | Extremely high relation-level | Core |
| USB | Public, Apache-2.0 | Human/crowd | High evidence/factuality/correction | Core |
| PlainFact | Public, CC BY-SA 3.0 | Human annotation; generated contrasts | High biomedical | Core positive / conditional negative |
| QASPER | Public, CC BY 4.0 | Practitioner answers/evidence | Medium for outcome; high evidence | Diagnostic |
| TRUE | Public aggregator | Human labels inherited | Medium transfer | Secondary |
| AggreFact | Public aggregator | Human labels inherited | Medium transfer | Secondary |
| FENICE story-summeval | Public, CC BY-NC-SA 4.0 | Human factuality | Medium long-form | Secondary |
| SciFact-Open | Public | Human labels, mixed evidence-highlight provenance | High open-domain science | Optional |
| 2026 scientific simplification HITL corpus | Public | expert-edited gold + human study | Very high, small | Optional direct |

---

# Remaining blockers before protocol replacement

1. Verify actual downloadable CLEF SimpleText human-annotated real-submission files.
2. Freeze exact external splits/files and SHA-256s.
3. Freeze all dataset-specific adapter contracts before any V2.4 prediction.
4. Build overlap/dedup manifest.
5. Freeze per-track metrics and progression rules.
6. Decide how REVIEW is tested without inventing semantic mappings.
7. Obtain a focused independent higher-model construct-validity review of the protocol replacement.
8. Only after that, version the existing custom Gate C protocol rather than silently editing it.

No runtime change is authorized.

# Exact next checkpoint

`PRE-GATE-C — NO-NEW-HUMAN PROTOCOL REPLACEMENT CONSULTATION`

Purpose:
independent review of whether Gate C-EXT + Gate C-META is scientifically strong enough to replace the custom newly-adjudicated 80-study Gate C for research progression.

Until approved:
- preserve current custom Gate C protocol;
- do not recruit reviewers;
- do not open custom 80-study holdout;
- do not run V2.4 on any candidate external validation split.
