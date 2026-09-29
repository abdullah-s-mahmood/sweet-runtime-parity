# M2 P0 — Aggregate Error Analysis Before P1

Date: 2026-09-30
Status: P0 FAILED; ONE P1 REVISION AUTHORIZED BY PRE-REGISTRATION

## Observed aggregate pattern

P0 did not fail because it accepted many unsafe cases. It failed because it was too strict on safe expert-supported text.

- Unsafe Acceptance Rate: 2/48 = 4.17% (passes <=5%).
- Safe Acceptance Coverage: 16/72 = 22.22% (fails >=60%).
- CLEAN_REFERENCE_KEEP accepted: 6/36 = 16.67%.
- FULL_EXPERT_REPAIR accepted: 10/36 = 27.78%.
- ERRONEOUS_SOURCE_KEEP accepted: 0/24 = 0%.
- ONE_OF_MANY_PARTIAL accepted: 1/12 = 8.33%.
- ALL_BUT_ONE_PARTIAL accepted: 1/12 = 8.33% (fails zero-accept criterion).

Source split:
- QALB safe coverage: 14/48 = 29.17%.
- ZAEBUC safe coverage: 2/24 = 8.33%.

## Aggregate diagnosis

The verifier appears to be applying an idealized strict-MSA / textbook-perfection standard rather than the narrower question “is this an acceptable complete correction under the source register and the expert-correction task?”

This matters because:
- QALB may preserve acceptable register/dialect/style variation rather than normalize everything into formal prose.
- ZAEBUC professional correction may target actual correction needs without rewriting every awkward but acceptable learner formulation.
- ACAD_PASS must distinguish mandatory correctness from optional rewriting. Over-rejection is therefore a real product failure, not merely a benchmark inconvenience.

## P1 permitted changes

P1 will only modify rubric wording/order as allowed:
1. distinguish mandatory correctness errors from style/register preferences;
2. explicitly preserve colloquial/register forms when they are coherent and not themselves target errors;
3. count a residual only when it is a clear required correctness repair, not merely a preferred rewrite;
4. perform a final residual-error scan before ACCEPT;
5. keep REPAIR_INCOMPLETE -> non-ACCEPT mandatory.

No examples from P0 are inserted into the prompt.
No P0 case IDs/text are used to choose P1 cases.
No threshold changes.
No second judge.
No A7'ta reserve.
