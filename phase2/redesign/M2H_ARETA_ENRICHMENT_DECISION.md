# M2-H ARETA Enrichment Decision

Date: 2026-09-30
Status: FROZEN

## Decision

Use enhanced ARETA as a DEVELOPMENT-ONLY enrichment and stratification layer.

Do not use ARETA as independent gold.

## Basis

The original ARETA paper reports automatic Arabic error-type annotation across orthography, morphology, syntax, semantics, punctuation, merge, and split classes, with 85.8% micro-average F1 on its manually annotated blind ALC test.

The later CAMeL-Lab Arabic GEC work uses an enhanced ARETA implementation to construct multi-class Arabic GED labels.

The project already pins the relevant CAMeL-Lab arabic-gec repository at:
8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

The enhanced ARETA implementation is present under:
areta/

## Scientific constraint

Automatic error-type labels are useful for:
- stratification;
- diagnosis;
- candidate sampling.

They are not sufficiently independent to become the truth source for evaluating H2/H3.

QALB expert source/reference correction remains the primary correction evidence.

## Consequence

H2:
ARETA orthographic labels may nominate cases, but deterministic surface-family checks must independently support approval.

H3:
ARETA MI/MT labels may nominate a morphology proxy subset, but all reported H3 metrics on that subset must explicitly say DEVELOPMENT PROXY unless later confirmed independently.

H4:
ARETA SP/MG labels are not the operative gold. H4 gold is defined by exact character preservation with whitespace-only boundary change.

## Classification

Scientific methodology versus the immediately previous state:
IMPROVED.

Magnitude:
- removes 1,143 Split and 1,124 Merge edits from false H4-positive eligibility;
- retains 2,633 pure-space Split and 5,505 pure-space Merge edits for legitimate H4 calibration;
- prevents ARETA's automatic labels from being promoted to independent gold.

Measured verifier performance:
UNCHANGED.

Deployment:
REVIEW-first.
