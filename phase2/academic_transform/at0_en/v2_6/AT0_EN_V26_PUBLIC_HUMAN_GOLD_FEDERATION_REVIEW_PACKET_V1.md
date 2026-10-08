# ACAD_PASS — Public Human-Gold Federation / SOTA Rebuild Review Packet V1

Date: 2026-10-08

State:
`REVIEW_REQUIRED_BEFORE_ANY_SUCCESSOR_TRAINING`

Objective:
replace the unavailable local-expert annotation dependency with a rigorously audited federation of already-human-annotated public corpora, weak/distant supervision and fixed public benchmarks, while preserving scientific validity.

Target:
build an ACAD_PASS English P/I/C/O extraction system that is demonstrably at least competitive with, and preferably better than, the strongest published comparable systems under the SAME datasets, task definitions and metrics.

This packet does NOT authorize training.

## 1. Why the previous acquisition path is blocked

The independently reviewed fresh-2026 acquisition protocol required:
- two qualified independent human annotators;
- a third senior adjudicator;
- independent EVAL custodian;
- resources for 80 qualification + 400 DEV + 5,000 sealed EVAL.

The user has confirmed those local human resources are unavailable.

Therefore the question is no longer:
"Can we pretend AI labels are expert gold?"

The question is:
"Can we replace locally created gold with already-existing public human gold and still build/evaluate a stronger system rigorously?"

## 2. Evidence that public human gold is substantial

### A. Section-specific P/I/C/O federation — Hu et al., Bioinformatics 2023

Public resource:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO`

Human-reannotated corpora:
- EBM-NLP_mod: 500 RCT abstracts
- COVID-19: 150 RCT abstracts
- Alzheimer disease: 150 RCT abstracts

Total:
- 800 abstracts
- 6,821 P/I/C/O entities

Published entity counts:
- P = 1,006
- I = 2,726
- C = 523
- O = 2,566

Published exact entity-level standalone PubMedBERT results:
- EBM-NLP_mod overall F1 = .683
- COVID overall F1 = .838
- AD overall F1 = .795

Published end-to-end section-specific entity-level F1:
- EBM-NLP_mod = .712
- COVID = .850
- AD = .805

Important:
C is explicitly separate, unlike original EBM-NLP simplifications.

Scientific role candidate:
`NATIVE_PICO_HUMAN_GOLD`

### B. PICO-Corpus — Mutinda et al., 2022

- 1,011 PubMed breast-cancer RCT abstracts
- human annotated Participants, Intervention, Control, Outcomes
- public BRAT files

Project status:
definite prior ACAD_PASS exposure.

Scientific role candidate:
`TRAIN_DEVELOPMENT_ONLY`

It must not become new independent evidence.

### C. Original EBM-NLP

- 4,993 abstracts
- training annotations from crowdsourcing/aggregation
- official test labels collected from medical professionals
- original schema focuses P/I/O and does not natively match the target separate-C construct.

Scientific role candidate:
- auxiliary representation/span supervision;
- official benchmark only where schema mapping is native and prespecified;
- NOT direct separate-C gold.

### D. DISTANT-CTO — BioNLP 2022

Public distant-supervision resource:
- >300,000 clinical trials
- approximately one million sentences
- 977,682+ Intervention/Comparator annotations across semantic types

Published result:
- +2% macro-F1 for Intervention over the manually annotated benchmark;
- >5% improvement when distant + manual labels were combined.

Scientific role candidate:
`WEAK_I_C_SUPERVISION`

This directly targets ACAD_PASS's weakest precision class/role problem.

It is NOT human gold.

### E. TrialSieve — 2025

Public repository:
`pathology-dynamics/trialsieve_final`

Pinned currently observed repo head:
`62dd931124e36a8c1d9dc4a2469893553d90d2e4`

License:
CC0-1.0

Public data include:
- 1,609 PubMed abstracts
- 170,557 raw annotations
- 52,638 final nonoverlapping spans
- 20 entity categories
- >=3 annotators per abstract
- QC/senior review for inconsistent cases

Useful classes include:
- Disease/Condition
- Group Characteristic
- Group Name
- Group Population/Sample Size
- Drug Intervention
- Non-Pharmaceutical Intervention
- Non-Study Drug
- Outcome
- Dosage/frequency/duration/administration
- quantitative measurements

Important limitation:
native schema is richer than flat P/I/C/O and does not directly encode our exact I-vs-C target for every span.

Scientific role candidate:
`AUXILIARY_MULTI_TASK_HUMAN_GOLD`
and potentially a prospectively frozen role-mapping experiment.

Do NOT silently convert all TrialSieve labels to native P/I/C/O gold.

### F. C-TrO corpus — Journal of Biomedical Semantics 2022

- 211 human-annotated randomized phase 3/4 clinical-trial abstracts
- 107 glaucoma + 104 T2DM
- entity-level + schema/template relations
- relations connect intervention to arm and outcome to intervention
- reported entity agreement substantial; mean kappa about .74 and .68 in the two corpora

Scientific role candidate:
`ROLE_RELATION_AUXILIARY_HUMAN_GOLD`

This may be especially useful for intervention/comparator arm reasoning.

Do NOT treat its ontology labels as direct flat P/I/C/O without a frozen mapping.

### G. EvidenceOutcomes

Public corpus:
- 500 randomly selected PubMed RCT abstracts
- plus 140 EBM-NLP abstracts
- three independent annotators
- clinically meaningful Outcome annotations
- reported IAA .76

Scientific role candidate:
`OUTCOME_AUXILIARY_HUMAN_GOLD`

### H. FinePICO — JAMIA 2025

Used:
- 2,511 abstracts
- four public datasets
- small labeled + larger unlabeled/semi-supervised training

Published:
precision/recall/F1 .567/.636/.600 in its fine-grained setup,
with >16 F1 point improvement over the small-data baseline.

Scientific role:
methodological evidence supporting semi-supervision / corpus federation.

### I. PICOX — JAMIA 2024

Architecture:
- explicitly predicts whether words mark entity starts/ends;
- constructs span candidates;
- multi-label span classification;
- handles overlapping PICO.

Evaluated on:
- EBM-NLP
- PICO-Corpus
- AD
- COVID

Published:
- micro F1 improved 45.05 -> 50.87 overall comparison;
- PICO-Corpus recall 56.66 -> 67.33;
- COVID micro F1 77.10 -> 80.32;
- AD comparable F1 with higher precision.

Scientific role candidate:
`PRIMARY_BOUNDARY_SPAN_BASELINE_AND_ARCHITECTURAL_COMPARATOR`

This is mechanistically relevant because R44C's residual false positives were dominated by invalid/boundary spans.

### J. AlpaPICO — Methods 2024

Uses:
- LLM in-context learning;
- instruction tuning/LoRA;
- EBM-NLP/EBM-COMET and fine-grained variants.

Authors report state-of-the-art results on their evaluated EBM datasets.

Scientific role candidate:
`LLM_COMPARATOR / TEACHER_CANDIDATE`

Metrics/task definitions must be reconciled before any claim of superiority.

### K. GPT-4o mass PICO extraction — Pharmaceutical Medicine 2024

Processed:
682,667 PubMed abstracts.

Random human-validation sample:
350 abstracts.

Reported:
342/350 (98%) had accurate and comprehensive PICO extraction, with missed elements mainly outcomes.

Important:
this is a semantic abstract-level human verification measure, NOT strict exact-span per-class precision/recall.

Scientific role candidate:
`PRACTICAL_SEMANTIC_LLM_COMPARATOR`

Do not compare its 98% directly with exact-span ACAD_PASS precision.

## 3. Key conclusion from evidence

The absence of local annotators does NOT imply lack of human supervision.

There already exist:
- thousands of human/crowd/expert annotated abstracts;
- corpora with separate P/I/C/O;
- comparator-rich weak supervision at very large scale;
- human-annotated rich relation/arm datasets;
- official public test sets.

Therefore a public-human-gold federation is technically plausible.

The scientific question is how to use it without:
- schema leakage;
- overlap contamination;
- test-set tuning;
- invalid cross-dataset label mapping.

## 4. Proposed evidence split philosophy

### EXPOSED_POOL
Every corpus or record previously used by ACAD_PASS:
training/development only.

Includes at minimum:
- PICO-Corpus project records;
- R44 DESIGN;
- FactPICO;
- consumed holdouts;
- old SELECT;
- any other proven exposure.

### NATIVE_PICO_FEDERATION
Human P/I/C/O corpora with compatible explicit C:
candidate sources:
- EBM-NLP_mod
- COVID
- AD
- any additional audited compatible corpus.

Exact exposure audit required before assigning benchmark role.

### AUXILIARY_HUMAN_GOLD
Schema-rich corpora:
- TrialSieve
- C-TrO
- EvidenceOutcomes
- original EBM-NLP test where target semantics are compatible.

Used only with a frozen task adapter.

### WEAK/SILVER
- DISTANT-CTO
- weak supervision
- semi-supervised pseudo-labels
- LLM teacher outputs

Never called gold.

## 5. Proposed development paradigm

Candidate high-performance procedure for review:

### Stage A — corpus normalization
Build an immutable common interchange schema:
- raw text;
- native gold;
- native ontology;
- source corpus;
- document/trial identifiers;
- offsets;
- section;
- native relationships;
- mapping provenance.

Keep native annotations intact.
Generate P/I/C/O views only through versioned adapters.

### Stage B — multi-source representation training
Candidate supervision:
- native P/I/C/O human gold;
- TrialSieve auxiliary types;
- C-TrO arm/intervention/outcome relations;
- EvidenceOutcomes O;
- original EBM-NLP P/I/O;
- DISTANT-CTO weak I/C.

No benchmark-test labels used in training.

### Stage C — boundary-first exact span model
At least reproduce/compare:
- PICOX-style start/end boundary proposal;
- exact span classification;
- overlapping spans where native gold permits.

Candidate stronger implementation:
modern biomedical encoder + span scorer / global span model.

Do not decide exact architecture until independent review.

### Stage D — role-aware I/C module
Use:
- native separate-C human gold;
- DISTANT-CTO weak comparator supervision;
- C-TrO/TrialSieve group/arm evidence where construct-compatible.

Purpose:
attack ACAD_PASS's historically weakest I precision / role distinction.

### Stage E — selective high-precision verifier
Retain evidence-backed lessons from R44C:
- low-capacity regularization baseline;
- explicit invalid/NONE modeling;
- calibrated/selective diagnostics;
- no assumption that bigger head is better.

Candidate:
ensemble/stacking only if training predictions are generated with leakage-safe cross-fitting.

### Stage F — LLM teacher / adjudication ensemble
Candidate teacher sources:
- strong current LLM extraction;
- AlpaPICO-style instruction/ICL setup.

Use:
- silver label generation;
- disagreement mining;
- semantic consistency features.

Do not use LLM-generated labels as final gold.

## 6. Proposed benchmark program

No single published "best system" is comparable on every metric.

Therefore define three axes.

### AXIS 1 — strict exact-span native P/I/C/O
Primary:
human P/I/C/O public benchmarks with exact entity scoring.

Compare against:
- section-specific PubMedBERT pipeline;
- PICOX;
- FinePICO where task-compatible;
- other reproducible exact-span systems.

Target:
beat strongest reproducible comparator on each benchmark under its official split/metric.

### AXIS 2 — cross-corpus generalization
Freeze ONE global procedure.

For each compatible corpus:
- train on all other training corpora;
- evaluate once on held-out corpus;
- no corpus-specific threshold tuning.

Report:
- per-corpus P/R/F1;
- macro across corpora;
- class-wise P/I/C/O;
- strict exact-span.

Purpose:
prevent "winning" only through dataset-specific tuning.

### AXIS 3 — practical semantic extraction
Compare with LLM baselines under a separate semantic correctness protocol using an already-human-labeled public evaluation source where possible.

Do NOT merge this metric with exact-span claims.

## 7. What "better than all existing systems" can validly mean

A scientifically defensible claim requires:
- same public benchmark;
- same split;
- same annotation schema;
- same matching rule;
- same metric;
- reproducible comparator.

Possible claim:
"ACAD_PASS achieves the best reported/reproduced exact-span F1/precision under benchmark X among the compared systems."

Invalid claim:
"ACAD_PASS is globally more accurate than GPT-4o because its exact-span precision exceeds a semantic 98% human-verification number."

## 8. Proposed from-scratch rebuild rule

After protocol freeze:
- discard all current learned ACAD_PASS weights;
- do not initialize from R44B/R44C learned heads;
- retain only approved method knowledge;
- rebuild training data from immutable source corpora/adapters;
- retrain the final pipeline from pretrained public base models;
- use only authorized training/development splits;
- external benchmark outputs immutable before gold scoring.

This is a true computational rebuild.

It does NOT erase historical exposure classifications.

## 9. Critical review questions

Return exactly one:

`PROCEED_PUBLIC_HUMAN_GOLD_FEDERATION`

`PROCEED_FEDERATION_WITH_CHANGES`

`RETAIN_NEW_HUMAN_ACQUISITION_REQUIREMENT`

`BLOCK_FOR_OTHER_REASON`

Review:

1. Can public already-human-annotated corpora replace new local experts for system DEVELOPMENT?
2. Can they also support credible SOTA benchmark claims?
3. Which corpora are native enough for P/I/C/O exact-span training?
4. Which should be auxiliary only?
5. Is EBM-NLP_mod+COVID+AD sufficient as the native separate-C core?
6. Should PICO-Corpus, because of prior ACAD_PASS exposure, be train-only?
7. Can TrialSieve be used safely as auxiliary supervision without inventing P/I/C/O gold?
8. Can C-TrO relations improve I/C role learning without construct leakage?
9. How should EvidenceOutcomes be incorporated?
10. How should DISTANT-CTO weak labels be weighted/filtering?
11. Is FinePICO-style semi-supervision justified?
12. Should an LLM teacher be used, and how should silver confidence/disagreement be handled?
13. Should the primary architecture be boundary-first/span-based similar to PICOX?
14. What modern 2025–2026 biomedical encoder/span architecture is the strongest justified candidate?
15. Should a generative extractor be included in the final ensemble?
16. How should overlapping spans be handled?
17. How should exact P/I/C/O mapping adapters be validated without new local annotators?
18. Can native public test sets provide sufficient final benchmark evidence?
19. Which public test sets should be frozen now as untouched-by-ACAD_PASS one-shot tests after exposure audit?
20. What cross-corpus protocol best tests generalization?
21. How do we prevent published benchmark knowledge from becoming test-set tuning?
22. What constitutes a fair head-to-head comparison with PICOX/FinePICO/AlpaPICO/section-specific models?
23. Should GPT-4o-style semantic extraction be a secondary comparator only?
24. What exact primary metric should define SOTA?
25. Should high-precision selective extraction remain a separate operating mode from standard F1 benchmark evaluation?
26. What exact architecture/loss/optimizer should be prospectively frozen for the first federation experiment?
27. How many scientific attempts are defensible?
28. What ablations are necessary to establish novelty versus data-scale effects?
29. What evidence would falsify the proposed federation hypothesis?
30. Is new human annotation actually required before publication, or only for a future strongest prospective validation claim?

## 10. Desired scientific target

Primary:
`BEST_REPRODUCIBLE_STRICT_EXACT_SPAN_PICO_SYSTEM_ON_COMPARABLE_PUBLIC_HUMAN_GOLD_BENCHMARKS`

Secondary:
`ROBUST_CROSS_CORPUS_GENERALIZATION`

Tertiary:
`HIGH_PRECISION_SELECTIVE_MODE_WITH_STRONG_PRACTICAL_SEMANTIC_EXTRACTION`

No claim of superiority is allowed until verified under comparable metrics.

## 11. Current authorization boundary

Allowed:
- provenance audit;
- public dataset metadata/schema audit;
- comparator literature/code audit;
- synthetic adapter tests;
- independent higher-model review of this packet.

Not allowed yet:
- successor model training;
- changing R44C scientific history;
- calling old exposed data fresh;
- opening VERIFY_INTERNAL;
- public test-set score-driven tuning.

Checkpoint:
`PUBLIC_HUMAN_GOLD_FEDERATION_REVIEW_REQUIRED_BEFORE_TRAINING`.
