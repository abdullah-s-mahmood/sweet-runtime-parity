# ACAD_PASS — FactPICO V2.5 Stage Progress Scorecard V1

Date: 2026-10-05
Status: POST-PREDICTION / PRE-GOLD

## 1. Completion rubric

This scorecard is an engineering progress indicator, NOT a benchmark performance metric.

Weighted FactPICO V2.5 validation checklist:
- frozen scientific/gold contract: 10% — COMPLETE
- deterministic adapter + frozen input/gold/eligibility identities: 10% — COMPLETE
- V2.5 scalability/runtime closure: 15% — COMPLETE
- one-shot execution controls + independent authorization: 15% — COMPLETE
- one prospective prediction run + immutable freeze: 20% — COMPLETE
- independent post-prediction/pre-gold authorization: 5% — PENDING
- deterministic gold join + preregistered scoring: 15% — PENDING
- result freeze + interpretation / next-decision checkpoint: 10% — PENDING

Current FactPICO V2.5 validation completion:
`70%`

Current authorized prediction-execution checkpoint completion:
`100%`

## 2. Quality / maturity assessment

These are engineering assessments, not scientific outcome claims.

Execution-integrity maturity:
`96/100`

Reason:
- immutable checkout verified;
- exact input identity verified;
- durable one-shot claim enforced;
- zero retries;
- 345/345 predictions frozen;
- exact ID order preserved;
- zero INVALID outcomes;
- immutable artifact and hashes preserved;
- stop-before-gold boundary respected.

Scientific-validation completeness:
`70/100`

Reason:
prediction evidence is complete, but gold-based H1 performance has not yet been measured.

Current FactPICO-stage quality satisfaction:
`90/100`

Overall ACAD_PASS English-track system maturity:
`78/100`

Target for describing the current research system as `EXCELLENT / REVIEW-READY`:
`>=90/100`

Main remaining gap to that target:
not runtime stability, but external validation evidence and frozen scoring/interpretation.

## 3. Improvement since the previous major checkpoint

Previous state:
`AUTHORIZED / PREDICTION NOT RUN`

Current state:
`RUN ONCE / COMPLETE / IMMUTABLY FROZEN`

Completion delta:
approximately `+20 percentage points` within the FactPICO V2.5 validation subphase.

Execution-integrity maturity delta:
approximately `+8 points` because the one-shot control is now proven on the real authorized run rather than only synthetic/pre-execution evidence.

Scientific-performance delta:
`NOT YET COMPARABLE`
because gold join/scoring is still forbidden and has not been performed.

## 4. Interpretation guardrail

The unscored prediction distribution:
- PASS_CANDIDATE = 0
- REJECT = 37
- REVIEW = 308
- INVALID_VERIFICATION = 0

MUST NOT change the progress or scientific-quality score through post-hoc interpretation before the frozen gold/scoring checkpoint.

## 5. Exact next step

`INDEPENDENT POST-PREDICTION / PRE-GOLD AUTHORIZATION REVIEW`

If authorized:
`ONE DETERMINISTIC GOLD JOIN + FROZEN SCORING RUN -> RESULT FREEZE -> STOP FOR INTERPRETATION REVIEW`
