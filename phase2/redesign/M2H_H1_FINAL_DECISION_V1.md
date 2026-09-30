# M2-H H1 Final Decision v1

Date: 2026-09-30
Status: FROZEN FINAL DECISION
Scope: Phase 2 / M2-H / H1-v1

## Decision

H1-v1 is formally:

**CLOSED FAIL**

The current M2-H path must not proceed to H5/H6.

## Basis

The frozen M2-H protocol requires:

- H1 candidate edit-instance recall >= 80%.

The frozen H1 official-alignment audit defines the key operational realization of this gate as:

**official-alignment one-pass NoPnx M2 recall**

The completed CALIBRATION result is:

- Precision: 71.53%
- Recall: 69.39%
- F1: 70.44%
- F0.5: 71.09%

Frozen recall gate:

- >=80.00%

Deficit:

-10.61 percentage points

This is substantially below the gate and is not borderline.

## Reproducibility status

Inference parity:
- 256 / 256 all-field match
- mismatches: 0

Gold construction:
- 6,888 / 6,888 cases processed
- failures: 0
- char-alignment cross mismatches: 0
- word/subword cross-path mismatches: 0

Therefore the failure cannot reasonably be attributed to:
- an H1 runner parity bug;
- exact-transaction decomposition alone;
- punctuation contamination;
- tatweel construction loss;
- silent exclusion of difficult CALIBRATION cases.

## Downstream consequence

Do NOT start:
- H5 Risk Fusion
- H6 Sentence Completeness
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC

H2, H3, and H4 remain closed/not activated as previously frozen.

M1, M2, and M2-R remain closed.

## Iterative decoding

The public SWEET model card/repository usage example applies NoPnx with decode_iter=2 before one Pnx pass.

This does not change the H1-v1 decision.

The H1 candidate contract explicitly froze one-pass decoding and stated that multi-pass behavior could only be studied later as a separately versioned diagnostic.

Therefore:

- H1-v1 remains permanently FAIL.
- A future iterative SWEET diagnostic, if ever authorized, must be a new version and cannot rewrite this result.
- Such a diagnostic should be performed only if it can materially inform a new architecture, because iterative corrections complicate exact reversible source-span attribution required by ACAD_PASS.
- No iterative tuning loop is authorized in the current M2-H path.

## Scientific classification

**WORSENED FOR CURRENT M2-H VIABILITY / IMPROVED SCIENTIFIC CERTAINTY**

The important improvement is epistemic:
a misleading provisional 30.02% exact-transaction figure has been replaced by a reproducible representation-invariant result of 69.39% recall, with validated inference parity and complete gold construction.

The resulting decision is still negative:
the frozen H1-v1 prerequisite fails by 10.61 pp.

## Next authorized direction

Close the current M2-H implementation path before H5/H6.

Any further Arabic correction work must begin as a separately versioned architectural decision, not as tuning of H1-v1 or H5/H6.

A future redesign may compare:
- iterative SWEET as a diagnostic candidate generator;
- sequence-to-sequence Arabic GEC candidates such as AraBART-derived systems;
- REVIEW-first ensemble/candidate union architectures;
- conservative error detection plus human/LLM review instead of automatic correction.

Such work requires a fresh protocol and frozen gates before evaluation.

Reserved datasets remain closed.
