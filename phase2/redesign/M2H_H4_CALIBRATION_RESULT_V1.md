# M2-H H4 Structural Boundary CALIBRATION v1 — Result

Date: 2026-09-30
Status: **CLOSED / NOT ACTIVATED**
Scope: **CALIBRATION only**

## 1. Workflow

Run:
`36705698086`

Job:
`h4-calibration`

Conclusion:
**SUCCESS**

Started:
`2026-09-30T10:58:55Z`

Completed:
`2026-09-30T11:00:59Z`

Artifact:
- id: `11092051414`
- name: `m2h-h4-calibration-v1`
- SHA256: `060b5ee437feefae2031108c102ee408ffe61178a813b54396599b199970994e`

## 2. Frozen gates

Per operation:
- positive recall >= **70%**
- accepted H1 candidate-stream precision lower bound >= **90%**
- hard stop if precision < **80%**
- accepted H1 n >= **20**
- **0** accepted non-pure adversarial negatives
- at least 2 of 3 non-H1 evidence families for automatic support

Evidence families:
- MORPH_SEGMENTATION
- CLITIC_LEGALITY
- DEVELOPMENT_PATTERN_SUPPORT

## 3. SPLIT result

Pure gold:
- total: **2,633**
- accepted: **0**
- recall: **0.00%**

H1 stream:
- total PURE_SPLIT candidates: **1,920**
- accepted: **0**
- precision lower bound: **not estimable**

Non-pure adversarial Split:
- total: **1,143**
- accepted: **0**

General no-boundary diagnostic:
- sampled: **1,000**
- accepted: **0**

Evidence-family diagnostic on pure gold:
- CLITIC_LEGALITY support: **413**
- DEVELOPMENT_PATTERN_SUPPORT: **59**
- MORPH_SEGMENTATION: **7**
- no pure Split received 2 supporting families.

Decision:
**SPLIT NOT ACTIVATED**

## 4. MERGE result

Pure gold:
- total: **5,505**
- accepted: **2,612**
- recall: **47.4478%**

Frozen recall target:
**>=70%**

Gap:
**-22.5522 percentage points**

H1 stream:
- total PURE_MERGE candidates: **3,792**
- accepted: **1,853**
- exact-reference-supported accepted: **1,779**
- reference-unsupported accepted: **74**
- strict-reference precision lower bound:
  **96.0065%**

Frozen precision target:
**>=90%**

Precision margin:
**+6.0065 percentage points**

Non-pure adversarial Merge:
- total: **1,124**
- accepted: **0**

General no-boundary diagnostic:
- sampled: **1,000**
- accepted: **0**

Evidence-family diagnostic on pure gold:
- CLITIC_LEGALITY support: **4,738**
- MORPH_SEGMENTATION: **2,631**
- DEVELOPMENT_PATTERN_SUPPORT: **23**

Support-count distribution on pure Merge:
- 0 families: **727**
- 1 family: **2,166**
- 2 families: **2,610**
- 3 families: **2**

Decision:
**MERGE NOT ACTIVATED**

Reason:
precision is strong and adversarial safety is excellent, but recall fails the frozen 70% gate.

## 5. Interpretation

H4-v1 is not a scientific failure of the structural invariance concept.

The strict non-whitespace character-preservation gate is effective:
- zero non-pure adversarial Split accepted;
- zero non-pure adversarial Merge accepted;
- zero general diagnostic controls accepted.

However, the preregistered two-of-three evidence requirement is too sparse to recover enough true boundary corrections, especially Split.

The result demonstrates:
- structural safety is tractable;
- broad automatic boundary correction with the frozen evidence families is not sufficiently complete.

Historical QALB systems often used language-model/context evidence for Split/Merge decisions. Recent Arabic text-editing systems learn edit behavior directly from data. These are materially different evidence sources and were not preregistered for H4-v1; they are therefore not added post hoc.

## 6. Scientific classification

Versus pre-H4 expectation:

**MIXED / WORSENED FOR AUTOMATIC COMPONENT VIABILITY**

SPLIT:
- recall **0.00%** vs target 70%
- automatic activation: disabled

MERGE:
- precision lower bound **96.01%** vs target 90%: PASS
- recall **47.45%** vs target 70%: FAIL
- adversarial accepted: **0**: PASS
- automatic activation: disabled

Overall H4 automatic operations enabled:
**0 / 2**

## 7. Decision

H4-v1 is CLOSED.

Do NOT:
- lower the recall threshold;
- change the 2-of-3 requirement;
- enlarge the clitic inventory from observed failures;
- change morphology support thresholds after seeing these results;
- add a language model/contextual scorer inside H4-v1 post hoc.

Any future contextual boundary verifier must be a separately versioned research iteration.

For the current M2-H calibration cycle:
**H4 automatic activation = none.**

## 8. Next authorized step

Freeze the current M2-H component activation state:

- H1: active as structured candidate generator only
- H2: no automatic family activated
- H3: not activated
- H4: neither Split nor Merge activated

Then inspect the already-preregistered INTERNAL_EVALUATION execution/evaluation contract without reading INTERNAL_EVALUATION text. Only after the final activation manifest is committed and hashed may internal predictions be generated.

Reserved data remain closed until that manifest is frozen.
