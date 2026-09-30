# M2-H H2 CALIBRATION Result v1

Date: 2026-09-30  
Status: **CALIBRATION RESULT FROZEN**  
Scope: **CALIBRATION only**

## 1. Inputs

H1 CALIBRATION workflow:
- run: `36691616010`
- artifact id: `11088155733`
- artifact SHA256: `907065fd1a3e156456cec7a31f86facff689896b4d8d39b50cbc852ffd7cc8d3`
- cases: **6,888**
- H1 structured candidates: **46,811**
- exact QALB-reference-supported candidates: **32,502**
- reference-unsupported candidates: **14,309**
- overall strict reference support rate: **69.4324%**
- truncated cases: **0**
- non-applicable H1 edits: **18**

H2 predicates were frozen before family metrics were inspected in:
`M2H_H2_ORTHOGRAPHIC_RULES_V1.md`

ARETA enrichment was attached only as diagnostic context.

## 2. H2 family results

### HAMZA_ALIF_SEAT
- candidates: **582**
- exact supported: **498**
- reference unsupported: **84**
- strict reference precision lower bound: **85.57%**
- case coverage: **465**
- automatic promotion: **DISABLED**

### ALIF_MAQSURA_YA
- candidates: **1,646**
- exact supported: **1,487**
- reference unsupported: **159**
- strict reference precision lower bound: **90.34%**
- case coverage: **865**
- automatic promotion: **DISABLED**

### TA_MARBUTA_HA
- candidates: **2,353**
- exact supported: **2,212**
- reference unsupported: **141**
- strict reference precision lower bound: **94.01%**
- case coverage: **1,307**
- automatic promotion: **DISABLED**

### ALIF_VARIANT
- candidates: **19,338**
- exact supported: **18,536**
- reference unsupported: **802**
- strict reference precision lower bound: **95.85%**
- case coverage: **5,467**
- automatic promotion: **DISABLED**

### SINGLE_ARABIC_LETTER_ORTHOGRAPHIC
- candidates: **25,309**
- exact supported: **23,764**
- reference unsupported: **1,545**
- strict reference precision lower bound: **93.90%**
- case coverage: **5,952**
- automatic promotion: **DISABLED**

### DIACRITIC_ONLY
- candidates: **0**
- diagnostic only
- automatic promotion: **DISABLED**

### TATWEEL_ONLY
- candidates: **0**
- diagnostic only
- automatic promotion: **DISABLED**

All measured extraction-invariant violations within matched H2 families: **0**.

## 3. Frozen decision

No H2 family is automatically promoted in v1 under the preregistered conservative rule:

`strict reference precision lower bound >= 98%`

The threshold is **not lowered**.

This is negative calibration evidence for direct family-wide automatic approval.

## 4. Single-reference limitation

`REFERENCE_UNSUPPORTED` is not equivalent to `LINGUISTICALLY_WRONG`.

QALB provides an expert reference correction but does not enumerate every acceptable Arabic alternative.

Therefore:
- the values above are conservative lower bounds;
- they are sufficient to prevent automatic promotion under the current contract;
- they are not sufficient to claim that every unsupported H1 candidate is an actual false positive.

A family may only be reconsidered after a separately frozen, blinded adjudication protocol on CALIBRATION-only reference-unsupported candidates. No INTERNAL_EVALUATION information may influence that protocol.

## 5. Out-of-scope H1 candidates

Primary H2 common-gate exclusions:
- whitespace or multi-token: **16,852**
- empty side: **470**
- no Arabic: **65**

These are not H2 orthographic-family failures.

## 6. Scientific classification

Versus the previous checkpoint:

**MIXED**

- **IMPROVED methodologically:** H1 candidate generation and H2 family calibration are now measured reproducibly with frozen predicates.
- **WORSENED performance outlook for H2 auto-approval:** zero frozen non-diagnostic family currently clears the conservative 98% gate.
- no threshold was weakened and no reserved data was opened.

Measured H2 automatic family count:
- before calibration: unknown
- after calibration: **0 enabled / 5 tested non-diagnostic families**

## 7. Integrity

Still unopened:
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST

## 8. Next authorized decision point

Before moving past H2, choose scientifically between:

1. freeze all H2 automatic families disabled and proceed to H3/H4; or
2. preregister a blinded CALIBRATION-only adjudication protocol for the `REFERENCE_UNSUPPORTED` subset, without inspecting examples before the adjudication protocol is frozen.

No post-hoc family redefinition and no gate weakening are allowed.
