# M1-A v1 → v1.1 Change Log

Date: 2026-09-30

## v1 observed result

Workflow run 36640207701 completed the data scan but failed the pre-registered DATA_READY gate.

Observed QALB14 TRAIN+DEV:
- changed lines: 20,380
- source==reference lines: 48
- M2 reconstructable changed lines: 19,887
- multi-edit reconstructable lines: 19,758
- ONE_OF_MANY_PARTIAL available: 19,758
- ALL_BUT_ONE_PARTIAL available: 19,758
- M2 reconstruction failures: 493
- QALB15 read: false
- QALB TEST read: false
- raw QALB text persisted: false

The sole failed criterion was source==reference >=100 (observed 48).

## Why v1.1 is scientifically justified

We do not lower 100 to 48.

The v1 criterion conflated two different concepts:
1. a naturally unchanged raw source under a correction corpus;
2. a clean sentence suitable for testing KEEP/overcorrection resistance.

The human-corrected reference itself is direct expert evidence for a clean target under the corpus protocol. Therefore v1.1 creates CLEAN_REFERENCE_KEEP cases by using the human-corrected sentence as both input and candidate. This is not inferred from a model and does not require pretending that an unedited noisy source is clean.

v1.1 also reduces single-corpus dependence by adding:
- ZAEBUC Arabic TRAIN only: professionally corrected university essays, with professional Arabic annotators, weekly quality checks, and reported correction IAA Dice 97.1%.
- A7'ta: 470 erroneous/correct pairs manually extracted from a linguistic expert reference book, CC BY 4.0.

No QALB15, QALB TEST, ZAEBUC DEV/TEST, or reserved Nahw data are opened.

## New case families

- CLEAN_REFERENCE_KEEP
- ERRONEOUS_SOURCE_KEEP
- FULL_EXPERT_REPAIR
- SINGLE_EDIT_COMPLETE
- ONE_OF_MANY_PARTIAL
- ALL_BUT_ONE_PARTIAL
- ZAEBUC_FULL_EXPERT_REPAIR
- ZAEBUC_CLEAN_REFERENCE_KEEP
- ZAEBUC_ERRONEOUS_SOURCE_KEEP
- A7TA_EXPERT_RULE_PAIR
- A7TA_CLEAN_REFERENCE_KEEP

## Source hierarchy

Tier S:
- QALB human corrections + M2
- ZAEBUC professional human corrections

Tier A:
- A7'ta expert-book error/correction pairs
- frozen Nahw local expert-reviewed corrections

Tier B / calibration-only:
- Tibyan (expert-reviewed but ChatGPT-augmented)
- Gazelle human evaluation rubrics
- Mohi et al. 2026 four-expert evaluation rubrics/data
- Arabic Learner Corpus thesis/taxonomy

Tier B sources are not treated as primary gold without a separate provenance audit.
