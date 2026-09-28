# Phase 2 — Independent Candidate Acceptance Gate: Research Start

Date: 2026-09-28

Status: DEVELOPMENT ONLY. No sealed benchmark, no production auto-accept policy, no Phase 3.

## Starting evidence

The Arabic development track has already isolated four distinct problems:
1. raw rewrite/detokenization corruption — addressed by source-preserving surgical rendering;
2. over-broad edit application — reduced by operation-aware selectivity;
3. tokenizer [UNK] failures — partially recovered with a reversible normalized model view;
4. fully vocalized Arabic surface realization — substantially improved with CAMeL morphology + contextual morphology ranking.

The remaining blocking question is different:

**Can a runtime-only verifier decide whether a proposed correction direction is actually justified, without Nahw gold or previous human adjudication labels?**

Current counterexamples demonstrate why this is necessary:
- `وساعٍ → وساعا` is morphologically analyzable and receives contextual morphology consensus, but is grammatically wrong; the accusative defective-noun form requires `وساعيًا`.
- morphology can read `باسم` as `باسْمٍ` even where the sentence requires predicate `باسمٌ`.
- contextual morphology can rank a past-tense realization where the source speech act is imperative.

## Fresh research before implementation

### 1. Edit generation and edit verification should be separate tasks

Sorokin (EMNLP 2022) uses a first GEC model to generate edits and a second model to classify proposed edits as correct/false, improving GEC. This is the closest general-GEC architecture to the missing component in this project.

Reference:
https://aclanthology.org/2022.emnlp-main.785/

### 2. Arabic already has a public, architecturally independent second correction source

CAMeL-Lab's official Arabic GEC repository provides public AraBART/AraT5-family GEC models, GED models, contextual morphology preprocessing, code and pretrained Hugging Face models. Their documented example uses:
- CAMeL contextual morphology
- CAMeLBERT GED-13
- AraBART+GED generation

Initial second generator selected for this gate:
`CAMeL-Lab/arabart-qalb14-gec-ged-13`

Official repository pinned for reproducibility:
`CAMeL-Lab/arabic-gec@8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf`

References:
https://github.com/CAMeL-Lab/arabic-gec
https://aclanthology.org/2023.emnlp-main.396/

### 3. Arabic multi-system edit selection is a plausible architecture, not merely a project-specific idea

ArbESC+ (2025 preprint) combines AraT5, ByT5, mT5, AraBART, AraBART+Morph+GEC and Text Editing candidates, then selects edits with a classifier. It reports higher QALB F0.5 than individual systems. Because it is preprint evidence, it motivates testing multi-source features rather than immediate deployment.

Reference:
https://arxiv.org/abs/2511.14230

### 4. Recent Arabic seq2seq evidence supports AraBART/AraT5 as independent generators

A 2025 Neural Computing and Applications study reports strong QALB results for AraBART/AraT5-family GEC systems. This does not validate the exact model chosen here, but it strengthens the case for using seq2seq as an independent family relative to SWEET edit tagging.

Reference:
https://consensus.app/papers/transformers-to-the-rescue-alleviating-data-scarcity-in-ismail-abdou/4ffb28a9d70a5f439a45f692e6e0ec73/

### 5. Multi-task Arabic GEC can expose evidence/error-type signals

MTAGEC (2025) combines correction, error-type classification, evidence extraction and explanation using AraT5/AraBART-family models. This supports the broader verifier design: error type and evidence should become explicit features rather than trusting one scalar confidence.

Reference:
https://consensus.app/papers/mtagec-multitask-arabic-grammatical-error-correction-as-a-mahmoud-zappatore/72d7ca40e5395b6eb3b03da7437a205b/

### 6. Evaluation should remain edit-centric

UOT-ERRANT (TACL 2026) evaluates GEC through edit representations/alignment rather than sentence-level similarity. The acceptance gate therefore evaluates local aligned edits, not whether AraBART's whole rewritten sentence looks similar to the source.

Reference:
https://aclanthology.org/2026.tacl-1.77/

### 7. SWEET remains useful as a fast interpretable generator

The SWEET paper reports strong Arabic benchmark performance, >6x speed relative to compared Arabic GEC systems, and ensemble gains. Therefore the new model is added as independent evidence, not as a wholesale replacement.

Reference:
https://aclanthology.org/2025.acl-long.875/

## Permanent anti-leakage rule for this gate

Runtime features may include:
- original source/context;
- SWEET label, operation family and confidence;
- GED output/probability;
- CAMeL morphology analyses/ranks;
- AraBART output and source-aligned edit agreement/disagreement;
- deterministic grammar features computed only from source/candidate;
- scientific/source-fidelity flags.

Runtime decisions MUST NOT use:
- Nahw target location or correction;
- published Nahw explanation;
- previous human candidate classification;
- prior AUTO_ACCEPT/REVIEW/REJECT adjudication label.

Those labels are loaded only after the runtime decision table has been materialized, for development evaluation.

## Candidate population

This gate should unify two disjoint streams:
- 60 source-preserving NoPnx1 applied edits from the surgical path;
- 19 normalized recovery candidates from prior tokenizer-UNK locations.

Total candidate evidence population before deduplication: 79 candidate edits.

The primary unit remains candidate edit nested within source passage; passage clustering must be preserved in evaluation.

## Pre-registered hypotheses

H1. AraBART local agreement is positively associated with supported SWEET candidates but is not sufficient alone.

H2. AraBART disagreement can help reject known bad directions such as `وساعٍ → وساعا`, but disagreement may also occur for valid alternative corrections and must route to REVIEW rather than automatic rejection.

H3. Direct source-local patches remain the safest surface mechanism but have very low coverage.

H4. GED is useful as a soft error-location/type feature, not a hard gate.

H5. Morphology rank is useful after candidate direction is accepted, but morphology analyzability/consensus is not a correctness feature strong enough to accept edits alone.

H6. Transparent rule-based acceptance should be tested before fitting a learned classifier on this small development population.

H7. If no transparent runtime-only policy can reject known high-severity counterexamples while retaining materially better coverage than direct-patch-only, normalized/morphology corrections remain REVIEW_ONLY and the Arabic development architecture should stop expanding before sealed evaluation.

## Initial acceptance strategies to test

All strategies are runtime-observable:

1. DIRECT_PATCH_ONLY
2. ARABART_EXACT_LOCAL_AGREEMENT
3. ARABART_NORMALIZED_LOCAL_AGREEMENT
4. SWEET_OPERATION_AWARE + ARABART_SUPPORT
5. SWEET_OPERATION_AWARE + (ARABART_SUPPORT OR high-confidence local evidence) — diagnostic only
6. GED + ARABART + morphology evidence score — transparent scoring, no learned weights unless a proper training split is created
7. STRICT_CONSENSUS: independent generator agreement + no deterministic grammar veto + source-safe realization
8. REVIEW_FIRST: accept only narrow exact rules; route all other supported evidence to REVIEW

## Brainstorming before execution

- Full AraBART rewritten sentence as product output: **DROP**
- AraBART as independent candidate generator: **PROTOTYPE**
- Source-local AraBART edit alignment: **INTEGRATE as evidence representation**
- GED hard gate: **DROP**
- GED soft feature: **TEST**
- Morphology consensus as sole verifier: **DROP**
- Direct local patch: **INTEGRATE narrow**
- Deterministic Arabic grammar vetoes: **PROTOTYPE**
- Multi-model agreement: **PROTOTYPE**
- Small learned classifier on 79 same-development edits: **WATCH; do not treat as independent validation**
- Strict scientific locks after linguistic ACCEPT: **INTEGRATE**
- Abstention/review: **INTEGRATE**

## Success criterion

A development policy is worth freezing for later sealed evaluation only if it:
- uses no gold/adjudication labels at runtime;
- rejects all known HIGH/CRITICAL wrong-direction counterexamples in this development set;
- achieves materially better useful supported coverage than DIRECT_PATCH_ONLY;
- preserves source bytes outside accepted local spans;
- does not let scientific/protected spans bypass the existing safety stack;
- reports REVIEW/ABSTAIN rather than guessing under unresolved evidence.
