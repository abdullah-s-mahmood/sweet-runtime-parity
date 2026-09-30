# M2-H H3 Morphology-Aware CALIBRATION v1 — Result

Date: 2026-09-30
Status: **CLOSED / FAIL AS DEVELOPMENT-PROXY COMPONENT**
Scope: **CALIBRATION only**
Role: **DEVELOPMENT PROXY**

## 1. Workflow

Run:
`36703934748`

Job:
`h3-calibration`

Conclusion:
**SUCCESS**

Started:
`2026-09-30T10:41:25Z`

Completed:
`2026-09-30T10:43:20Z`

Artifact:
- id: `11091545756`
- name: `m2h-h3-calibration-v1`
- SHA256: `82372c564d0f05dd16b3f7cc6d141c5eb77647a2c3a4277560ab6c6dc71d7f27`

## 2. Mapping / nomination

MI/MT token annotations:
**2,597**

Mapped to exact source spans:
**2,529**

Mapping failures:
**68**

Mapped MI/MT annotations with no exact-span H1 candidate:
**2,360**

Mapped MI/MT annotations with exact-span H1 candidate:
**169**

Nominated H1 candidates:
**169**

By ARETA diagnostic code:
- MI nominated candidates: **167**
- MT nominated candidates: **2**

## 3. Candidate results

Nominated:
- exact-reference-supported: **85**
- reference-unsupported: **84**

H3 dispositions:
- `REVIEW_AMBIGUOUS`: **79**
- `REVIEW_UNANALYZABLE`: **64**
- `REVIEW_OUTSIDE_INFLECTION`: **12**
- `REVIEW_NO_STABLE_LEMMA_POS`: **11**
- `SUPPORTED_MORPHOLOGY_PROXY`: **3**

Among the 3 H3-supported candidates:
- exact-reference-supported: **1**
- reference-unsupported: **2**

Supported cases:
**3**

False-positive proxy cases:
**2**

## 4. Frozen quality-proxy metrics

Candidate recall:
`1 / 85 = 1.1765%`

Frozen target:
`>= 70%`

Result:
**FAIL**

Supported-candidate precision proxy:
`1 / 3 = 33.33%`

False-positive case rate proxy:
`2 / 3 = 66.67%`

The false-positive case-rate target was preregistered as <=10%, but the metric is formally non-evaluable under the frozen protocol because fewer than 20 cases received H3 support.

## 5. Diagnostic interpretation

The result is not a software failure.

The frozen out-of-context morphology-consensus rule was far too conservative for recall while still allowing spurious support in a tiny number of cases.

Primary abstention causes:
- missing retained lexical analysis: **64**
- disallowed/clitic-changing compatible pairs: **51**
- multiple changed-feature signatures: **25**
- multi-token surfaces: **12**
- no exact shared lex/POS identity: **11**
- empty-vs-changing morphology ambiguity: **3**

This is consistent with the known ambiguity of Arabic surface morphology. Contextual morphological disambiguation is a materially different problem from enumerating all word analyses.

Two of the three supported candidates were reference-unsupported, so the current H3 rule is not merely low-coverage; its tiny accepted set also shows poor conservative precision-proxy behavior.

## 6. Decision

H3-v1 is CLOSED and **not activated**.

Do NOT:
- relax exact lex/POS identity after seeing this result;
- weaken the ambiguity rule;
- select convenient analyses post hoc;
- lower the 70% recall or 10% false-positive gates;
- use ARETA corrected tokens as an approval oracle.

Any future contextual morphology redesign requires a separately versioned development iteration. It is not on the critical path now.

## 7. Scientific classification

Versus the state before H3 measurement:

**WORSENED FOR COMPONENT VIABILITY / IMPROVED SCIENTIFICALLY**

Magnitude:
- recall: **1.18%** vs target **70%** (gap **-68.82 pp**)
- H3-supported candidates: **3 / 169 = 1.78%**
- conservative precision proxy: **33.33%**
- automatic H3 activation: **DISABLED**

The gain is epistemic: a plausible morphology-only verifier hypothesis was directly falsified under preregistered conditions without tuning on failures.

## 8. Next authorized step

Proceed to H4 structural Split/Merge calibration.

H4 retains its previously frozen contract:
- exact character preservation after whitespace removal;
- pure-boundary positives only;
- adversarial non-pure Split/Merge negatives;
- at least two independent non-H1 evidence families for automatic approval;
- H1 agreement diagnostic only.

Reserved/internal data remain closed.
