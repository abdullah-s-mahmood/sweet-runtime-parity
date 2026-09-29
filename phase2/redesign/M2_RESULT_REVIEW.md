# M2 — Frontier Reasoning Verifier Result Review

Date: 2026-09-30

## Executive decision

**M2 verifier gate: FAIL.**  
**Scientific understanding: IMPROVED.**  
**Arabic auto-apply: unchanged — REVIEW-first.**  
**A7'ta reserve: untouched.**

A single strong frontier reasoning verifier did not achieve the preregistered safety/coverage operating point.

## P0 result

- UAR: 2/48 = 4.17%.
- SAC: 16/72 = 22.22%.
- Review burden: 37.50%.
- Safe rejection error: 44.44%.
- CLEAN_REFERENCE_KEEP acceptance: 16.67%.
- FULL_EXPERT_REPAIR acceptance: 27.78%.
- ALL_BUT_ONE_PARTIAL acceptance: 8.33%.

Interpretation: relatively safe but too conservative to be useful.

## P1 result

- UAR: 9/48 = 18.75%.
- SAC: 41/72 = 56.94%.
- Review burden: 20.83%.
- Safe rejection error: 27.78%.
- CLEAN_REFERENCE_KEEP acceptance: 44.44%.
- FULL_EXPERT_REPAIR acceptance: 69.44%.
- ONE_OF_MANY_PARTIAL acceptance: 8.33%.
- ALL_BUT_ONE_PARTIAL acceptance: 66.67%.

Interpretation: useful coverage improved, but safety failed badly on near-complete repairs.

## Comparable magnitude P0 → P1

- UAR: **+14.58 percentage points — WORSENED**.
- SAC: **+34.72 pp — IMPROVED**.
- Review burden: **−16.67 pp — IMPROVED operationally**.
- Safe rejection error: **−16.67 pp — IMPROVED**.
- CLEAN KEEP acceptance: **+27.78 pp — IMPROVED but still below gate**.
- FULL repair acceptance: **+41.67 pp — IMPROVED and passed its family gate**.
- ALL_BUT_ONE unsafe acceptance: **+58.33 pp — severely WORSENED**.

Overall P0→P1: **MIXED, with the safety dimension worsening enough to dominate the deployment decision.**

## Forensic correction to interpretation

The strict 18.75% UAR treats every withheld reference edit as mandatory. That is intentionally conservative but can overstate error because punctuation/register choices may be optional.

Post-result audit found:
- three accepted cases with clearly mandatory Hamza errors;
- three punctuation-only omitted edits;
- two dialect/register corrections;
- one ONE_OF_MANY case dominated by punctuation/reference formatting.

Even if all six disputed cases are forgiven, at least 3/48 = **6.25%** of the original unsafe denominator are clear mandatory-error accepts, still above the 5% ceiling. Therefore the safety failure survives the reference-ambiguity audit.

## Status versus M1-A

M1-A improved evidence readiness but did not claim model quality. M2 provides the first strong-model feasibility evidence under the redesigned contract.

- **Project scientific understanding: IMPROVED materially.**
- **Frontier verifier as sole auto-accept gate: WORSENED versus the hypothesis/expectation; not supported.**
- **Arabic verification architecture: MIXED — strong signal for obvious errors/full repairs, weak for near-complete residual detection.**
- **Arabic auto-correction capability: UNCHANGED — REVIEW-first.**

## Forecast

### Most realistic
A decomposed verifier can improve over the monolithic judge because the observed misses are heterogeneous and some are simple, auditable residual errors. The highest-value next test is explicit residual-span detection.

### Best case
A residual hunter achieves high recall on mandatory withheld edits with low false-positive rate on clean references. Combined later with edit validation and deterministic protections, this could create a narrow high-precision auto-apply lane.

### Failure case
Residual detection still shows the same safety–coverage tradeoff or over-flags acceptable Arabic variation. Then unattended Arabic auto-apply should be abandoned for this phase and Arabic should remain a review assistant, while ACAD_PASS invests more heavily in English/document-preservation capabilities.

## Main blockers

1. Mandatory-error vs optional-reference distinction.
2. Arabic orthographic/morphosyntactic residual detection.
3. Judge inconsistency and multilingual reliability.
4. Ambiguity and valid alternatives.
5. Scientific fidelity remains untested.
6. Document preservation remains untested.
