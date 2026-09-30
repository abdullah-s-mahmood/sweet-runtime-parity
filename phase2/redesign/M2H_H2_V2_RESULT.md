# M2-H H2 Evidence-Constrained Development Iteration v2 — Result

Date: 2026-09-30
Status: **CLOSED / FAIL TO ACTIVATE**
Scope: **CALIBRATION only**

## 1. Workflow

Run:
`36702245858`

Job:
`h2-v2-calibration`

Conclusion:
**SUCCESS**

Started:
`2026-09-30T10:24:42Z`

Completed:
`2026-09-30T10:26:54Z`

Artifact:
- id: `11090183156`
- name: `m2h-h2-v2-calibration-v1`
- SHA256: `769bcd52f897868ebcb5b64b46f217d0b0ee63b047d1815174ca2c7d3ab38d2b`

## 2. Frozen v2 predicate

The preregistered v2 rule accepted an `ALIF_VARIANT` candidate only when:
- the frozen ALIF_VARIANT surface predicate passed;
- source and candidate were single-token clean Arabic surfaces;
- source had zero CALIMA-MSA analyses;
- candidate had one or more analyses;
- candidate analyses exposed one lexical identity;
- no proper-name risk, analyzer failure, or invariant failure existed.

Frozen activation gate:
- n >= 50;
- strict-reference precision lower bound >= 98%;
- zero invariant failures;
- zero analyzer failures among accepted rows.

## 3. Results

ALIF_VARIANT family candidates:
**19,338**

Accepted H2-v2 candidates:
**0**

Exact QALB-supported accepted:
**0**

Reference-unsupported accepted:
**0**

Strict-reference precision lower bound:
**not estimable (n=0)**

Accepted case coverage:
**0**

Invariant failures among accepted:
**0**

Analyzer failures:
**0**

Reason counts:
- `SOURCE_ANALYZABLE`: **18,998**
- `CANDIDATE_UNANALYZABLE`: **339**
- `SURFACE_HYGIENE_FAIL`: **1**

Automatic activation:
**DISABLED**

## 4. Interpretation

The v2 asymmetric morphology-attestation predicate had zero usable coverage.

This is a clean negative result, not a software failure.

The assumption that a wrong ALIF_VARIANT form would often be absent from CALIMA-MSA while the correction would be present was falsified on CALIBRATION.

The result is consistent with the broad coverage of modern Arabic morphological analyzers: analyzability is too permissive to serve as a high-precision spelling-error discriminator by itself.

## 5. Decision

H2-v2 is CLOSED.

Do NOT:
- lower the 98% gate;
- create another narrower ALIF_VARIANT rule from the same observed v2 failures;
- use the blind adjudication packet as a hidden tuning source;
- block progress waiting for unavailable human reviewers.

Current automatic H2 activation:
**none**

The optional blinded adjudication packet remains frozen for future external validation if qualified human reviewers become available, but it is no longer on the critical path.

## 6. Scientific classification

Versus H2-v1:

**WORSENED FOR H2 COVERAGE / IMPROVED SCIENTIFICALLY**

Magnitude:
- H2-v1 best family lower bound: ALIF_VARIANT 95.85%, but not activatable.
- H2-v2 accepted coverage: **0 / 19,338 = 0%**.
- automatic H2 families enabled: remains **0**.

The methodological gain is that the reviewer bottleneck no longer blocks the project, and an explicit falsifiable automatic-evidence hypothesis was tested and rejected without gate weakening.

## 7. Next authorized step

Proceed to:
1. H3 morphology-aware CALIBRATION development proxy;
2. H4 structural boundary calibration;
3. freeze component activation decisions;
4. only then consider opening INTERNAL_EVALUATION.

Reserved/internal data remain closed.
