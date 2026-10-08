# ACAD_PASS — Fresh Independent RCT/PICO Data Acquisition Review Packet V1

Date: 2026-10-08

Status:
`REVIEW_REQUIRED_BEFORE_ANY_NEW_DATA_ACQUISITION_OR_ANNOTATION`

## 1. Why this packet exists

The prospectively frozen R44C experiment has completed and failed its scientific gate.

Frozen result:
`AT0_EN_V26_R44C_LINEAR5_DEVELOPMENT_RESULT_FREEZE_V1.md`

Official R44C run:
`37726111765`

Decision:
`NO_ARCHITECTURE_NOMINATED`

The predeclared sole fallback is now active:

`STOP_FURTHER_MODEL_THRESHOLD_LOSS_ADAPTATION_ON_DESIGN_AND_ACQUIRE_GENUINELY_FRESH_INDEPENDENTLY_ANNOTATED_DATA_UNDER_A_SEPARATELY_FROZEN_PLAN`.

Therefore this packet does NOT propose another model on the existing 256 DESIGN documents.

It asks for independent review of the data-acquisition design before:
- sampling records;
- annotating spans;
- creating a new development split;
- creating a new sealed evaluation split;
- opening VERIFY_INTERNAL;
- training any successor model.

## 2. Evidence motivating genuinely fresh data

R44-B and R44C both fail the current strict precision gate despite:
- leakage-controlled nested upstream generation;
- complete frozen candidate populations;
- large nonlinear verifier heads;
- a much smaller regularized linear verifier.

R44C materially improved generalization diagnostics versus J0:
- best frozen macro precision: 0.8453 -> 0.8767;
- high-confidence FP: 189 -> 130;
- outer NLL: 1.2102 -> 0.9456;
- ECE: 0.2079 -> 0.1769.

But P/I/O and macro precision remain below .90.

Continuing to choose new losses/architectures/thresholds on the same 256 DESIGN documents is no longer authorized.

## 3. Candidate temporal source

A strong candidate source is PubMed RCT abstracts published in a strictly post-project/public-corpus temporal window.

Candidate primary window for review:
`2026-01-01 through 2026-09-30`

Why this window is attractive:
- it is temporally far later than the public AD/COVID RCT corpora used in related PICO literature, which were retrieved in 2021;
- PICO-Corpus and EBM-NLP-derived resources are also substantially older;
- current PubMed contains many 2026 RCT publications across pharmacologic, behavioral, surgical, rehabilitation, nutrition and other intervention types;
- ending at 2026-09-30 avoids a moving partially indexed October 2026 boundary at the time this protocol is being designed.

Candidate PubMed eligibility query concept:
- publication type Randomized Controlled Trial;
- publication/index date inside the frozen window;
- English;
- human study;
- abstract available.

The exact query syntax, date field (publication date versus electronic/index date) and retrieval timestamp must be frozen before acquisition.

## 4. Why existing public PICO corpora should not simply become the new benchmark

Known public PICO resources are valuable for annotation guidance and methodological comparison, but they are not automatically fresh for ACAD_PASS.

Examples:
- EBM-NLP-derived data;
- EBM-NLP_mod;
- COVID-19 150-RCT corpus;
- Alzheimer disease 150-RCT corpus;
- PICO-Corpus;
- FinePICO's combined public corpora;
- any previously protected EBM/COVID/AD material in this project.

They may have:
- prior direct project exposure;
- overlap with earlier training/evaluation corpora;
- different annotation semantics;
- older temporal coverage;
- merged Intervention/Comparison categories in some benchmark usage.

They must remain excluded unless a future protocol explicitly proves non-exposure and schema compatibility.

## 5. Annotation evidence from prior work

The section-specific PICO annotation work of Hu et al. used separate P/I/C/O annotations and reported:
- P kappa ~0.714;
- I kappa ~0.808;
- C kappa ~0.701;
- O kappa ~0.790;
- overall kappa ~0.746
after revised annotation guidelines and two medical-background annotators.

Its published corpus statistics show C is rarer than I/O:
- EBM-NLP_mod: 240 C entities / 500 documents;
- COVID-19: 180 / 150;
- AD: 103 / 150.

This supports:
- explicit boundary rules;
- separate C;
- independent annotation;
- enough document volume to avoid an extremely small C evaluation population.

However, those old counts MUST NOT be treated as guaranteed prevalence in a 2026 sample.

## 6. Candidate acquisition architecture for review — not yet frozen

A defensible candidate is to create TWO prospectively separated corpora from one temporally fresh candidate pool:

### FRESH_DEV
Purpose:
- future model development/training after the current DESIGN set is retired from adaptive tuning.

### SEALED_FRESH_EVAL
Purpose:
- one-time prospective evaluation after a complete future procedure is frozen.

Candidate scale for review:
- 400 FRESH_DEV abstracts;
- 400 SEALED_FRESH_EVAL abstracts;
- total 800 independently annotated RCT abstracts.

This is deliberately larger than the previous disease-specific 150-document corpora and is intended to provide substantially better support for the rarer C class.

The number 400+400 is a candidate design commitment requiring independent review. It has NOT been optimized against model outcomes.

The reviewer should determine whether:
- this is sufficient;
- it is unnecessarily large;
- a different fixed size is more defensible;
- a fixed random sample plus a separately reported C-enriched challenge stratum is preferable.

Do not adopt label-dependent optional stopping after model evaluation.

## 7. Sampling must precede model access

Before any PICO annotation or successor-model training:

1. Retrieve the complete eligible 2026 candidate pool.
2. Freeze raw PubMed identifiers and raw source text/metadata hashes.
3. Perform all predeclared exclusion/deduplication.
4. Freeze a deterministic randomization seed.
5. Allocate documents to FRESH_DEV and SEALED_FRESH_EVAL.
6. Persist the complete membership manifest and SHA256.
7. Prevent any future model-development process from reading SEALED_FRESH_EVAL text or labels until separately authorized.

No model score may influence:
- inclusion;
- exclusion;
- allocation;
- sample size;
- annotation priority.

## 8. Freshness and duplicate/trial-family audit

The protocol must exclude direct and near overlap against ALL prior ACAD_PASS sources.

At minimum check:
- PMID;
- DOI;
- normalized exact title;
- normalized abstract hash;
- fuzzy title similarity;
- trial registration identifiers such as NCT/ISRCTN where available;
- duplicate publications;
- corrections/editorials/comments;
- secondary analyses of a trial already represented in prior corpora;
- conference abstract/full-paper pairs where identifiable;
- same trial family reported in multiple publications.

The exclusion ledger must include:
- candidate ID;
- exclusion reason;
- matched prior source/identifier;
- algorithm/version used;
- manual adjudication flag if needed.

A simple exact-PMID deduplication is insufficient for a genuinely fresh benchmark.

## 9. Primary-result eligibility

The review must decide exact inclusion rules for:
- pilot randomized trials;
- cluster randomized trials;
- crossover RCTs;
- factorial trials;
- multi-arm trials;
- pragmatic RCTs;
- noninferiority/equivalence trials;
- secondary/subgroup analyses;
- protocols without results;
- feasibility studies;
- randomized studies where the abstract is not a primary clinical trial report.

The intended construct is primary RCT evidence with identifiable P/I/C/O elements, not every publication containing the phrase "randomized trial."

## 10. Annotation schema must be frozen before annotation

The new annotations must preserve the target construct ACAD_PASS actually intends to verify.

At minimum:
- P = Population/Participants
- I = Intervention
- C = Comparison/Control
- O = Outcome

Separate C is mandatory.

Before annotation starts, freeze exact rules for:
- minimal versus maximal span boundaries;
- articles/prepositions/modifiers;
- conjunctions and coordinated interventions;
- drug dose/frequency/duration;
- placebo/usual-care/control wording;
- multi-arm trials;
- repeated mentions;
- abbreviations and parenthetical expansions;
- nested/overlapping spans;
- composite outcomes;
- outcome measurement names versus numeric results;
- population condition versus eligibility qualifiers;
- whether title repetitions are annotated;
- whether Methods-only, Title+Methods, or the full abstract is in scope.

The last point MUST be reconciled against the exact source-compatible construct used by the frozen ACAD_PASS candidate generator. Do not silently change annotation scope.

## 11. Annotation independence

For a genuinely independent gold set, candidate requirement:

- at least two annotators independently annotate each selected document;
- annotators are blinded to:
  - ACAD_PASS predictions;
  - B/Boundary outputs;
  - J0/J1/R44C outputs;
  - candidate coordinates;
  - model confidence;
- adjudication occurs only after independent annotation is complete;
- adjudicator does not use model output to resolve disagreement.

Preferred:
- medical/clinical or evidence-synthesis background;
- formal annotation guideline training;
- pilot qualification set that is NOT part of the final FRESH_DEV or SEALED_FRESH_EVAL populations.

The reviewer must state whether two annotators plus one adjudicator is sufficient or whether another design is needed.

If qualified independent human annotation cannot be obtained:
- explicitly state whether AI-only labels can satisfy the term "independently annotated";
- if not, define the weaker scientific status of any AI-assisted corpus.
Do not silently call AI-generated labels gold standard.

## 12. Annotation quality metrics

Prespecify:
- span-level exact agreement;
- per-class agreement;
- boundary disagreement counts;
- type disagreement counts;
- Cohen's kappa only where mathematically appropriate;
- entity-level agreement metrics robust to span boundaries;
- adjudication rate;
- disagreement taxonomy.

Do not use IAA to remove difficult documents after seeing model outputs.

## 13. Raw-text and annotation immutability

For every record freeze:
- PMID;
- DOI;
- title;
- abstract;
- PubMed retrieval timestamp;
- publication metadata;
- trial registry identifiers if found;
- normalized text hash;
- raw response/source hash;
- annotation version;
- annotator IDs represented by non-identifying codes;
- adjudicated gold hash.

Once SEALED_FRESH_EVAL is adjudicated and sealed:
- corrections require a versioned erratum process;
- old labels remain archived;
- model outputs may never overwrite gold.

## 14. Candidate leakage controls

Before any future training:
- test exact and near duplicates between FRESH_DEV and SEALED_FRESH_EVAL;
- test trial-family overlap;
- test duplicates with every prior ACAD_PASS corpus;
- test previous public corpus membership;
- document uncertain matches.

The future base/context model may have broad historical biomedical pretraining.
Temporal 2026 sampling materially reduces direct text-pretraining exposure for older biomedical encoders, but this must be verified against the exact base-model provenance rather than assumed.

## 15. Evaluation role

Do NOT immediately score current R44C on SEALED_FRESH_EVAL.

First:
1. acquire/annotate/freeze FRESH_DEV and SEALED_FRESH_EVAL;
2. use only FRESH_DEV for any successor scientific development allowed by a later protocol;
3. freeze the complete future procedure, including upstream refit and acceptance rule;
4. then separately authorize exactly one SEALED_FRESH_EVAL access.

Otherwise the new evaluation set would immediately become another development set.

## 16. Statistical precision question requiring review

The original ACAD_PASS gate uses:
- per-class precision >= .90;
- recall >= .20;
- accepted >= 10;
- macro precision >= .90.

For a genuinely fresh external evaluation, accepted>=10 is too weak to support a strong population precision claim.

The reviewer must decide prospectively whether the fresh sealed evaluation should add:
- exact/binomial or Wilson confidence bounds;
- a minimum accepted count substantially above 10;
- both point-estimate and lower-confidence-bound requirements.

Illustrative planning only:
with observed precision around .95, roughly O(100) accepted predictions per class are needed for a 95% lower confidence bound near .90.
This is NOT yet a frozen gate or sample-size calculation.

## 17. No model adaptation while acquisition design is unresolved

Until a fresh-data protocol is independently reviewed and frozen:

NOT ALLOWED:
- R44D model fit;
- factorized verifier;
- calibration fit;
- boundary repair;
- hard-negative loss;
- alternate linear/nonlinear head;
- more threshold experiments;
- VERIFY_INTERNAL;
- sampling records based on current model scores;
- starting annotation on convenience examples.

Allowed:
- literature review;
- source/query feasibility analysis;
- annotation-guideline design;
- duplicate-detection tooling on synthetic/public test fixtures;
- higher-model/adversarial review of this packet.

## 18. Questions for independent/higher-model review

Return one acquisition verdict:
- `PROCEED_TEMPORAL_FRESH_2026_DUAL_CORPUS`
- `PROCEED_WITH_ACQUISITION_PROTOCOL_CHANGES`
- `USE_EXISTING_INDEPENDENT_PUBLIC_CORPUS_AFTER_PROVENANCE_AUDIT`
- `BLOCK_UNTIL_HUMAN_ANNOTATION_RESOURCES_EXIST`
- `BLOCK_FOR_OTHER_REASON`

Answer:

1. Is 2026-01-01 through 2026-09-30 an appropriate temporal freshness window?
2. Which PubMed date field and query must be frozen?
3. Should sampling be pure random, domain-stratified, trial-design-stratified, or another prespecified scheme?
4. Is 400 FRESH_DEV + 400 SEALED_FRESH_EVAL justified?
5. What fixed sample sizes best balance C support and annotation burden?
6. Should a separate C-enriched challenge set exist, and if so must it be excluded from headline pooled performance?
7. What exact document-level inclusion/exclusion rules should be frozen?
8. What exact duplicate/trial-family checks are mandatory?
9. How should trial registration IDs be used?
10. What exact P/I/C/O span annotation schema should be frozen?
11. What abstract sections are in scope so construct validity matches the current system?
12. Are two independent medical-background annotators + one adjudicator sufficient?
13. If human annotation resources are unavailable, can any AI-assisted design satisfy independent-gold requirements?
14. What annotation IAA/adjudication diagnostics must be reported?
15. Should FRESH_DEV and SEALED_FRESH_EVAL membership be allocated before annotation?
16. Should SEALED_FRESH_EVAL text itself remain inaccessible to model developers, or only its labels?
17. What minimum accepted count and confidence-bound criterion should replace/supplement accepted>=10 in final fresh evaluation?
18. Should the current .90 precision/.20 recall gates remain?
19. Is 2026 temporal sampling sufficiently protected from the frozen biomedical base encoder's pretraining, or must exact model pretraining provenance be audited first?
20. When, if ever, should VERIFY_INTERNAL be used now?
21. What exact conditions would make the new corpus no longer independent?
22. Define the one-way transition from data acquisition to future model development without contaminating SEALED_FRESH_EVAL.

Objective:
`CREATE_A_GENUINELY_FRESH_REPRODUCIBLE_INDEPENDENT_PICO_CORPUS_WITH_A_SEALED_EVALUATION_SET_BEFORE_ANY_FURTHER_MODEL_ADAPTATION`.
