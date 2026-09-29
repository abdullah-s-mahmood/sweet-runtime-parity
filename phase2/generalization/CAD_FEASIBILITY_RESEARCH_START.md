# Phase 2 — Sentence-Level Correction Acceptability Feasibility Research Start

Date: 2026-09-29

## Motivation

All simpler safety gates tested so far leave an unresolved repair-completeness problem:
- tri-model agreement can converge on partial repairs;
- morphology identity and post-edit fixed-point stability are insufficient;
- dependency-change heuristics did not separate the fresh partials;
- CATiB PROP->NOM failed retrospective replication;
- residual target GED improved precision but still admitted one historical partial.

The next question is whether a dedicated source-candidate acceptability discriminator can detect locally plausible but incomplete Arabic corrections.

## Literature basis

Cao et al. (LREC-COLING 2024) introduced Correction Acceptability Discrimination (CAD): a sentence-pair discriminator trained from GEC source/gold pairs and used to reject invalid corrections based on sentence-level correctness rather than edit-local plausibility. Their discriminator uses separate sentence encoding, mean pooling, a symmetrical comparison operator, and ranking-style training. Their English experiments report strong pairwise correctness discrimination and downstream GEC gains.

Qorib & Ng (EMNLP 2023) show that quality estimation can improve GEC system combination, but also document that weak estimators fail to distinguish good from bad corrections reliably. This reinforces the need for a safety-first external-data feasibility test rather than assuming a generic quality score is sufficient.

Arabic-specific GEC work (QALB, ArabicNLP 2023, ACL 2025 SWEET, and later Arabic GEC work) confirms that Arabic morphology and context remain difficult and that strong correction generation does not imply safe unattended acceptance.

## Chosen feasibility direction

Do not adapt an English GRECO checkpoint directly to Arabic.

Instead test an Arabic CAD-inspired local-completeness discriminator:
- external training/calibration data: QALB-2014 only;
- current QALB15 adjudications are never training/calibration input;
- pinned Arabic encoder;
- first feasibility model keeps the encoder frozen and trains only a lightweight classifier;
- target-centered contextual representation is used so distant unrelated errors do not dominate;
- threshold is calibrated only on QALB14 dev under a safety-first zero-false-accept objective.

A positive feasibility result is only evidence to justify a stronger replicated diagnostic. It cannot promote auto-apply.
