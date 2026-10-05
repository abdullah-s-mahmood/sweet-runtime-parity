# ACAD_PASS — FactPICO H1 Pre-Prediction Integrity Gate V1

Date: 2026-10-05
Status: BLOCKED_BY_SCALABILITY_PREFLIGHT / NO FACTPICO PREDICTION

## 1. Scope

This gate checks whether the frozen FactPICO H1 V5 evaluation can be executed reproducibly and fairly without:
- gold leakage;
- runtime drift;
- hidden semantic adapter logic;
- incomplete IDs;
- avoidable execution failure.

No FactPICO V2.4 prediction is performed here.

## 2. Claim boundary — PASS

Current authoritative claim map:

`ACAD_PASS_CAPABILITY_CLAIM_MAP_V1.md`

FactPICO role is frozen as:

`HARD SUBGATE FOR SOURCE-BOUNDED CRITICAL RCT/PICO FIDELITY`

FactPICO is NOT complete H1.

This satisfies the strategic-review requirement to lock interpretation before seeing results.

## 3. Added Information completeness — PASS WITH NARROW CLAIM

Decision:

`FACTPICO_ADDED_INFORMATION_COMPLETENESS_DECISION_V1.md`

Allowed V5 statement:

`NO_HIGHLIGHTED_ADDED_INFORMATION_SPAN_IN_THE_RELEASE`

Not:
- no possible addition;
- no externally true elaboration;
- complete source entailment.

No V5 denominator change is required.

## 4. Readiness authority — PASS

Supersession index:

`PRE_GATE_C_READINESS_SUPERSESSION_INDEX_V1.md`

Older readiness/protocol files remain historical evidence but cannot override:
- H1 FactPICO V5;
- current capability map;
- current V2 readiness state.

## 5. FactPICO artifact identity — PASS

Archive SHA-256:

`ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`

Primary numeric gold SHA-256:

`1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd`

Prediction input SHA-256:

`ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`

Separate gold SHA-256:

`6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`

Eligibility manifest SHA-256:

`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

Prediction/gold IDs:
`EXACT MATCH = PASS`

Prediction input gold leakage:
`PASS — NONE`

## 6. FactPICO adapter identity — PASS

Adapter:

`factpico_h1_adapter_v5.py`

Frozen local SHA-256:

`ab128309261eeffdb734464f2a2fef52cef4ce37bdb3b9654317d6b5bba0b7e1`

Adapter was built/run twice sequentially before this gate and reproduced identical:
- prediction hash;
- gold hash;
- eligibility hash;
- build-manifest hash.

No V2.4 execution occurred.

## 7. Frozen V2.4 runtime identity — PASS

Canonical runtime freeze:

Run:
`37150864483`

Trigger commit:
`c0193aa3f578cc32b454a031ead73ff7e56c8918`

Artifact:
`11284520199`

Artifact SHA-256:
`74f765f614b616da2eb101c30d669de0c0931b304a377944be2a4039fe5a844c`

Frozen components include:
- assertion graph schema;
- criticality rules;
- outcome contract;
- A1 extractor;
- A2 extractor;
- B2.2 relation-aware extractor;
- B1.1 aligner/outcome engine.

GitHub compare from the canonical freeze trigger commit to current branch HEAD at this gate found:

`FROZEN_COMPONENT_CHANGES = 0`

Therefore:
`RUNTIME DRIFT = NONE OBSERVED`

## 8. Development evidence boundary — PASS

B2 final closure remains development evidence only.

Canonical B2.2 EE:
- 12/12 pair accuracy;
- 5/5 safe acceptance;
- 0/6 adversarial acceptance.

It used a small mechanics/development set.

It does NOT establish:
- full-document scalability;
- FactPICO performance;
- external generalization.

## 9. New static scalability blocker — FAIL

Frozen aligner:

`gate_b1/b1_aligner.py`

Function:
`best_one_to_one(source, candidate)`

Implementation enumerates:

`itertools.permutations(candidate, len(source))`

When source and candidate assertion counts differ but are both >1, `assertion_groups` takes:

`n = min(len(source), len(candidate))`

then invokes one-to-one permutation search on the first `n` elements.

Therefore the matching stage has factorial worst-case enumeration in:

`n = min(source_assertion_count, candidate_assertion_count)`

Examples:

| n | permutations |
|---:|---:|
| 6 | 720 |
| 8 | 40,320 |
| 10 | 3,628,800 |
| 12 | 479,001,600 |
| 15 | 1,307,674,368,000 |
| 20 | 2,432,902,008,176,640,000 |

This is not a hypothetical code-style concern.

The implementation itself labels one fallback:
`Small B1 mechanics set fallback`.

FactPICO uses:
- full RCT abstracts;
- full generated summaries.

The frozen runtime was never previously shown to scale to arbitrary full-document assertion counts.

## 10. Scientific interpretation of the blocker

This is:

`IMPLEMENTATION SCALABILITY / EXECUTION VALIDITY RISK`

not:
- a FactPICO scientific failure;
- a V2.4 semantic false negative;
- a benchmark failure.

Running FactPICO before resolving execution validity could:
- hang on high-assertion records;
- create incomplete output;
- force arbitrary timeouts after seeing benchmark behavior;
- contaminate the one-shot procedural evaluation;
- conflate scalability failure with semantic verification performance.

Therefore execution is blocked before any FactPICO record is passed to V2.4.

## 11. Why the runtime is not silently repaired

Frozen-runtime rule:

Any modification to:
- B1 aligner;
- B2.2 extractor;
- other frozen verifier components

creates a new pipeline version.

Therefore replacing factorial matching with:
- Hungarian assignment;
- greedy matching;
- beam search;
- semantic retrieval;
- another polynomial matcher

would create a new runtime version.

It cannot be silently called the same V2.4 evaluation.

## 12. Required preflight resolution

Before FactPICO prediction, choose and freeze one scientifically clean path.

### Path A — measure V2.4 as frozen with an execution wrapper
Possible only if a benchmark-independent timeout/resource policy is frozen BEFORE FactPICO execution.

Every frozen record must still produce exactly one transaction result.

Runtime timeout/crash may map only to:
`INVALID_VERIFICATION`

with explicit reason.

No timeout value may be chosen after seeing FactPICO runtime behavior.

### Path B — version-bump scalable matcher before external prediction
Replace factorial assignment with a pre-specified scalable algorithm.

This creates:
`NEW PIPELINE VERSION`

It preserves V2.4 negative evidence but FactPICO would evaluate the new version, not canonical V2.4.

This requires:
- regression checks;
- new runtime freeze;
- updated external-evaluation identity.

### Path C — synthetic scalability preflight first
Use only synthetic/non-FactPICO texts to quantify assertion-count runtime growth and select Path A or B.

This does NOT consume FactPICO prediction data and is the preferred immediate next step.

## 13. Current gate results

| Check | Result |
|---|---|
| FactPICO claim boundary frozen | PASS |
| Added Information interpretation | PASS WITH NARROW CLAIM |
| Readiness supersession | PASS |
| Artifact hashes | PASS |
| Prediction/gold ID separation | PASS |
| No gold leakage | PASS |
| Adapter determinism | PASS |
| Frozen runtime unchanged | PASS |
| Exact prediction runner frozen | NOT READY |
| Failure/retry policy frozen | NOT READY |
| Full-document scalability | FAIL / BLOCKER |
| FactPICO prediction | NOT RUN |

## 14. Gate verdict

`NOT_READY_FOR_FACTPICO_PREDICTION`

Reason:

`BLOCKED_BY_SCALABILITY_PREFLIGHT`

## 15. Exact next checkpoint

`V2.4 SYNTHETIC SCALABILITY PREFLIGHT + EXECUTION-POLICY DECISION`

Authorized:
- static code analysis;
- synthetic/non-FactPICO scalability tests;
- deterministic wrapper design;
- failure/retry-policy design;
- no-gold execution-path audit.

Not authorized:
- any FactPICO V2.4 prediction;
- H1 scoring;
- V2.4 semantic tuning;
- custom Gate C opening;
- Arabic work.
