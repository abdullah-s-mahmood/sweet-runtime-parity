# M2-H H2 ALIF_VARIANT Blind Adjudication Protocol v1

Date: 2026-09-30  
Status: **FROZEN BEFORE ANY REFERENCE_UNSUPPORTED EXAMPLE IS INSPECTED**  
Scope: **CALIBRATION only**

## 1. Purpose

The strict-reference lower bound for `ALIF_VARIANT` is 95.85% (18,536 / 19,338), below the frozen 98% automatic-promotion gate.

Because QALB is single-reference and valid corrections are not exhaustively enumerated, `REFERENCE_UNSUPPORTED` is not automatically equivalent to an incorrect correction.

This protocol tests whether enough reference-unsupported `ALIF_VARIANT` candidates are genuinely mandatory, correct corrections to satisfy the existing 98% gate without lowering it.

## 2. Frozen population

Family:
`ALIF_VARIANT`

Total H1 candidates in family:
**19,338**

Exact QALB-reference-supported:
**18,536**

Reference-unsupported:
**802**

Minimum total safe candidates required for 98%:
`ceil(0.98 * 19,338) = 18,952`

Therefore at least:
`18,952 - 18,536 = 416`

of the 802 reference-unsupported candidates must be genuinely safe under the H2 automatic disposition.

Required finite-population proportion:
`416 / 802 = 51.87%`

## 3. Primary sample

Deterministic simple random sample without replacement:

- unsupported population sample: **n = 200 of 802**
- hidden exact-supported controls: **n = 50**
- packet total: **250**

Frozen sampling salt:
`M2H-H2-ALIF-VARIANT-BLIND-V1-20260930-A`

Selection ranking:
`SHA256(salt + "|" + candidate_id)`, ascending.

The 200 unsupported and 50 exact-supported controls are sampled independently using the same salt plus population tag, then pooled and deterministically shuffled with:
`SHA256(salt + "|PACKET|" + candidate_id)`.

No sampled example may be inspected before the packet is built from this frozen rule.

## 4. Blinding

Reviewers receive only:

- blinded packet ID;
- original source sentence;
- source span highlighted by token indices;
- source surface;
- proposed candidate replacement;
- candidate-only rewritten sentence;
- minimal context already present in the same sentence.

Reviewers must NOT receive:

- QALB reference;
- gold-support status;
- H1 identity;
- H1 confidence;
- ARETA codes;
- H2 family metric;
- whether the row is unsupported or a control;
- historical decision;
- model rationale.

## 5. Reviewer judgment

Two independent qualified Arabic reviewers are the promotion-standard evidence.

For each row, Stage A judgments are:

### Necessity
- `REQUIRED_CORRECTION`
- `OPTIONAL_OR_STYLISTIC`
- `NO_CORRECTION_NEEDED`
- `UNCERTAIN`

### Candidate correctness
- `CORRECT_IN_CONTEXT`
- `ACCEPTABLE_ALTERNATIVE`
- `INCORRECT`
- `UNCERTAIN`

### Meaning/fidelity
- `PRESERVED`
- `CHANGED`
- `UNCERTAIN`

### Final blinded disposition
- `SUPPORTED_MANDATORY`
- `SUPPORTED_OPTIONAL_OR_ALTERNATIVE`
- `UNNECESSARY_EDIT`
- `WRONG_CORRECTION`
- `UNCERTAIN_REVIEW`

A row counts as H2-v1 safe for automatic `SUPPORTED_MANDATORY` only if the final adjudicated disposition is exactly:
`SUPPORTED_MANDATORY`.

Anything else is non-safe for this promotion test.

## 6. Independence and disagreement

Primary reviewers work independently.

Before resolving disagreements, report:
- raw agreement;
- Cohen's kappa where category support permits;
- disposition confusion matrix.

Disagreements are resolved by:
- a third qualified Arabic adjudicator, or
- a documented consensus adjudication session.

AI may prepare packets, validate structure, and provide a clearly labeled developmental diagnostic pass, but **AI-only judgments do not satisfy the promotion-standard human evidence requirement**.

A higher-capability model may be consulted only for a focused ambiguous-case packet and remains advisory unless a later explicitly versioned protocol changes this rule.

## 7. Statistical decision rule

The unsupported population is finite:
- `N = 802`
- sample `n = 200`

Use an exact **one-sided 95% hypergeometric lower confidence bound** for the number `K` of genuinely `SUPPORTED_MANDATORY` candidates in the full unsupported population.

Let:
- `x` = number of adjudicated `SUPPORTED_MANDATORY` rows among the 200 unsupported sampled rows.

The lower bound is the smallest feasible `K` such that:

`P[X >= x | N=802, K, n=200] >= 0.05`.

Automatic promotion requires:

`(18,536 + K_lower_95) / 19,338 >= 0.98`.

For this frozen design, this requires at least:

**x >= 115 / 200**

which yields:
- `K_lower_95 >= 419`
- combined lower-bound precision >= **98.019%**

Observed `x <= 114` fails to establish the 98% gate in this v1 sample.

The gate is not lowered.

## 8. Control rule

The 50 exact-supported controls test construct validity and reviewer calibration.

A control is a critical contradiction if final adjudication is:
- `UNNECESSARY_EDIT`, or
- `WRONG_CORRECTION`.

If any critical contradiction is confirmed by final adjudication:
- do not automatically promote the family under this v1 protocol;
- investigate whether exact QALB support is sufficient for the intended `SUPPORTED_MANDATORY` disposition.

Controls are not included in the primary 200-row hypergeometric estimate.

## 9. No peek / no tuning

Before both primary reviewer passes are frozen:
- do not reveal support status;
- do not inspect QALB reference for sampled rows;
- do not change sample size;
- do not change the sampling salt;
- do not redefine `ALIF_VARIANT`;
- do not change the 98% gate;
- do not exclude difficult rows post hoc.

## 10. Reserved data

Remain unopened:
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST

## 11. Interpretation

This is a CALIBRATION-only development adjudication.

Passing this protocol allows `ALIF_VARIANT` to clear the H2-v1 precision gate conservatively on CALIBRATION.

It does not replace later independent evaluation on INTERNAL_EVALUATION after all component rules and thresholds are frozen.
