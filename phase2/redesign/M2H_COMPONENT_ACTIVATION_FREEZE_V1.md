# M2-H Component Activation Freeze v1

Date: 2026-09-30
Status: **FROZEN AFTER CALIBRATION / BEFORE H5 FUSION AND INTERNAL_EVALUATION**
Scope: M2-H development

## 1. Purpose

This file freezes the activation state of H1–H4 after their preregistered CALIBRATION evaluations.

No H2/H3/H4 threshold, rule inventory, ambiguity rule, or evidence requirement may be changed after this freeze within the current M2-H iteration.

## 2. H1 — Structured Candidate Generator

Status:
**ACTIVE AS CANDIDATE GENERATOR ONLY**

Frozen model:
`CAMeL-Lab/text-editing-qalb14-nopnx`

Frozen model revision:
`21286e56ce98a86362db540863f91c083b8970f9`

Frozen weight SHA256:
`9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d`

CALIBRATION:
- cases: 6,888
- H1 candidates: 46,811
- exact-reference-supported: 32,502
- reference-unsupported: 14,309
- truncation: 0
- non-applicable edits: 18

H1 output is never a safety verdict by itself.

H1 confidence remains diagnostic and may only be used by a separately preregistered H5 calibration model as a predictive feature; it is not interpreted as calibrated safety probability.

## 3. H2 — Orthographic Validator

Status:
**NO AUTOMATIC FAMILY ACTIVATED**

H2-v1:
- HAMZA_ALIF_SEAT: 85.57%
- ALIF_MAQSURA_YA: 90.34%
- TA_MARBUTA_HA: 94.01%
- ALIF_VARIANT: 95.85%
- SINGLE_ARABIC_LETTER_ORTHOGRAPHIC: 93.90%

Frozen automatic gate:
>=98%

Enabled:
**0 / 5 non-diagnostic families**

H2-v2 evidence-constrained ALIF_VARIANT:
- accepted: 0 / 19,338
- activation: disabled

H2 raw family identities/evidence may be retained as H5 input features only if preregistered before H5 metrics. H2 may not directly emit `SUPPORTED_MANDATORY` in the current freeze.

## 4. H3 — Morphology-Aware Validator

Status:
**NOT ACTIVATED**

CALIBRATION DEVELOPMENT PROXY:
- nominated candidates: 169
- exact-reference-supported nominated: 85
- H3-supported: 3
- exact-reference-supported H3-supported: 1
- candidate recall: 1.18%
- supported-candidate precision proxy: 33.33%
- false-positive case proxy: 66.67% on 3 supported cases

Frozen recall target:
>=70%

H3 may not directly emit `SUPPORTED_MANDATORY` or clean-document evidence.

Frozen H3 raw diagnostic fields may be retained as H5 input features only if preregistered before H5 metrics.

## 5. H4 — Structural Boundary Validator

Status:
**NO OPERATION ACTIVATED**

SPLIT:
- recall: 0.00%
- accepted H1 candidates: 0
- activation: disabled

MERGE:
- recall: 47.45%
- strict-reference precision lower bound: 96.01%
- accepted H1 candidates: 1,853
- non-pure adversarial accepted: 0
- general diagnostic accepted: 0 / 1,000
- activation: disabled because recall <70%

Enabled:
**0 / 2 operations**

H4's exact structural-invariance gate remains a valid hard safety feature.

Frozen H4 evidence-family outputs may be retained as H5 input features only if preregistered before H5 metrics.

No H4 operation may directly emit `SUPPORTED_MANDATORY` in the current freeze.

## 6. Current standalone automatic validation state

Standalone automatic validators activated after CALIBRATION:

**NONE**

This is a negative but valid calibration result.

It does not authorize lowering gates.

## 7. H5/H6 authorization under the original frozen protocol

The original `M2H_HYBRID_VERIFIER_PROTOCOL_V1.md` preregistered:

- H5 Risk Fusion
- H6 Sentence Completeness

Therefore one H5/H6 implementation is still authorized.

H5 may use only evidence already frozen before H5 outcome inspection, including:
- H1 candidate metadata/probability as an uncalibrated predictive feature;
- H2 frozen family identities/predicate outcomes;
- H3 frozen diagnostic morphology outcomes;
- H4 exact structural-gate and frozen evidence-family outcomes;
- operation type;
- candidate span/shape features;
- protected-invariant flags.

H5 may NOT:
- reinterpret a failed H2/H3/H4 component as standalone safe;
- invent a new H2/H3/H4 rule from calibration failures;
- use INTERNAL_EVALUATION for feature selection, fitting, thresholding, or calibration;
- use ARETA corrected text as an approval oracle;
- use reserved/confirmation/test data.

## 8. One-attempt rule for H5/H6

Because multiple component hypotheses failed and reviewer burden is high, the current M2-H cycle permits:

**one preregistered H5/H6 calibration implementation only**

After its CALIBRATION metrics:
- freeze model/features/thresholds;
- if feasibility criteria cannot be met without changing frozen feature definitions or gates, record failure;
- do not run iterative H5 tuning loops;
- do not open INTERNAL_EVALUATION until the H5/H6 freeze is complete.

## 9. INTERNAL_EVALUATION remains closed

Still unopened:
- INTERNAL_EVALUATION text
- STRESS_DIAGNOSTIC text
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST

## 10. Exact next step

Start H5/H6 as a new substantive iteration:
1. fresh research and adversarial brainstorming;
2. freeze H5 feature set, calibration model, target labels, thresholds, and H6 sentence-level derivation;
3. calibrate only on CALIBRATION;
4. freeze the resulting H5/H6 artifact and activation decision;
5. only then open INTERNAL_EVALUATION once.
