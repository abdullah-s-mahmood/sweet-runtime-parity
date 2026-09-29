# Phase 2 — Frozen-Encoder CAD Feasibility End Review

Date: 2026-09-29

## Canonical run

- workflow: Phase 2 External Arabic CAD Feasibility
- run: 36533553455
- external training job: SUCCESS
- consumed scoring job: SKIPPED by design because the external criterion failed
- current QALB15 adjudication labels read by this experiment: no
- QALB15 corrected TRAIN read: no
- QALB15 TEST read: no

## External QALB14 result

Frozen CAMeLBERT-MSA encoder + standardized logistic pair classifier:
- train: 8,000 balanced QALB14 examples
- dev: 2,418 balanced QALB14 examples
- feature dimension: 2,304
- dev ROC AUC: 0.5843757975
- max dev-negative probability: 0.9999999658
- frozen zero-false-accept threshold: 0.9999999658+
- dev negative false accepts: 0
- dev positive PASS: 0 / 1,209
- dev positive retention: 0%

Pre-registered external feasibility criterion: FAILED.

## Decision

**WORSENED as a CAD implementation candidate; IMPROVED epistemically.**

The frozen-encoder representation does not provide a useful safety-selective separation for the externally constructed QALB14 local-completeness task. It is not valid to lower the threshold after observing this result because that would violate the pre-registered safety criterion.

The consumed QALB15 scoring stage correctly did not run.

## Interpretation

This result falsifies the hypothesis that a frozen generic CAMeLBERT representation plus a shallow linear discriminator is sufficient.

It does not yet falsify trainable CAD because the published CAD discriminator fine-tunes its BERT representation. A single externally trained, fully fine-tuned Arabic sentence-pair discriminator is therefore the final justified escalation in this model family.

If that external model also fails the unchanged external safety/retention criterion, stop pursuing unattended Arabic auto-accept in Phase 2 and retain REVIEW-first/human verification.
