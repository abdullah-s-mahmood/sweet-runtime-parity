# M2-R P0 Status

Date: 2026-09-30

## Result

**P0 FAIL.**

Frozen predictions: 120 cases, 235 mandatory-error claims, 0 invalid surface claims.

Primary metrics:
- CRR: 53/90 = 58.89% (gate >=85%)
- GELR: 64/170 = 37.65% (gate >=80%)
- CFPR: 18/30 = 60.00% (gate <=5%)
- NCWR: 21/30 = 70.00% (gate >=90%)
- Orthography recall: 52/106 = 49.06% (gate >=95%)
- Morphology recall: 16/43 = 37.21%
- Syntax recall: 5/25 = 20.00%
- Lexical recall: 2/23 = 8.70%
- Strict-reference claim precision: 59/235 = 25.11%

Only the invalid-surface requirement passed.

## Integrity

The prediction hash was frozen before the gold key was opened.

Two scorer issues were repaired after gold opening:
1. dimension-specific gating on unavailable values;
2. v1.1 family rename to EXPERT_REINSERTED_RESIDUAL.

Neither repair changed predictions, thresholds, gold labels, or the scientific hypothesis.

## Gate state

- Confirmation: CLOSED
- Holdout: CLOSED
- A7'ta reserve: CLOSED
- One structural P1 prompt revision: ALLOWED
- P2 after P1: NOT ALLOWED

Next legitimate step: aggregate false-positive / false-negative error analysis, then freeze P1 without case-specific examples.
