# AT0-EN V2.3 — Known-External Assertion-Graph Gate Closure

Date: 2026-10-03
Status: CLOSED CHECKPOINT / OFFLINE ONLY / NO NEW MODEL INFERENCE

## Frozen execution

- Workflow: `AT0-EN V2.3 Assertion-Graph Offline Gate`
- Run: `37134559401`
- Run number: `5`
- Trigger commit: `e7671e833a2177beaf56f21a74907d3613bc346c`
- Conclusion: **SUCCESS**
- Artifact id: `11278485956`
- Artifact name: `at0-en-v2-3-assertion-graph-37134559401`
- Artifact ZIP SHA-256: `f9a5858791ebeacf918b990a7eccf52d9690b5955c3cb65da00001a8279f4c9f`

Artifact-internal hashes:
- assertion-graph verifier: `d82af97d276131477ab2f8c452f24e3302703f54b856a8ad46547af59d7ec0da`
- known-external test harness: `62e904874a0120bca5dcc69bf4ae099024c0c88e0bf7d9a6051edd742987235a`
- result JSON: `e1eddea894f504094520d2ac9d738ffb9444a357b0f7ef6b940fd144b620be6c`

## Gate result

Total checks: **36/36 PASS**

Controls:
- 11 valid safe controls -> `PASS_CANDIDATE`
- `SAFE_EN09` -> intentionally NOT PASS because the control itself omits a scientific relation present in the source: larger priority occurs only when the weighted combination becomes larger.
- The frozen EN09 `content_units` also omit that source relation. This is a benchmark-label defect, not verifier failure.

Adversarial set:
- **24/24 constructed attacks were NOT PASS**
- detected classes include scope expansion, modality strengthening, relation-decoy values, count contradictions, direction reversal, mechanism conflation, citation swapping, same-mechanism contradiction, causal contradiction, group/value swapping, ordered-step reversal, exclusion negation, equation-operator change, priority-direction reversal, measurement-rate decoys, imputation contradiction, duplicate-policy negation, timestamp negation, parameter retuning, and metric negation.

## Critical interpretation

This is **not an untouched independent validation result**.

The 24 attacks originated from the V2.2 independent red-team that exposed a severe weakness in the earlier rule validator. V2.3 was redesigned in response to those attacks. Therefore this 36/36 result is a **known-external regression gate** proving that the assertion-graph redesign closes the already-observed failure classes.

It must not be reported as evidence of generalization to unseen adversarial scientific drift.

The earlier V2.2 independent red-team remains negative evidence:
- 24 adversarial tests
- only 3 caught by the V2.2 rule validator
- 21/24 escaped as `PASS_CANDIDATE`
- escape rate: **87.5%**

That failure motivated the V2.3 assertion-oriented redesign.

## Architecture consequence

V2.3 changes the verification principle from positive lexical witness checking toward explicit scientific assertions with:
- subject / predicate / object binding;
- qualifiers and modality;
- polarity;
- scope;
- direction;
- contradiction/decoy checks;
- ordered relations where required.

The source paragraph remains authoritative. Frozen `content_units` are supporting indices only and cannot be treated as complete gold, because EN09 demonstrated an omitted source relation.

## Current scientific classification

**IMPROVED METHODOLOGICALLY / KNOWN-FAILURE REGRESSION PASS / GENERALIZATION NOT ESTABLISHED**

What improved:
- all 24 previously escaping adversarial patterns are now blocked;
- safe controls remain accepted except a demonstrably defective control;
- contradiction and decoy detection is explicit rather than inferred from token presence;
- source-text authority over incomplete content-unit lists is now explicit.

What is not established:
- unseen adversarial robustness;
- general scientific fidelity;
- human academic writing quality;
- cross-domain behavior;
- production safety.

## Exact next checkpoint

No new model inference is authorized.

The next stage must create and freeze a **second, unseen adversarial holdout** that is not used to modify V2.3 before scoring. Its construction and labels must be separated from the V2.3 implementation, then the frozen V2.3 verifier is run once against that holdout.

If the unseen holdout exposes failures, preserve them and return for redesign; do not tune on the holdout and re-score it as if still untouched.

HW1-EN remains blocked.
Arabic active research remains frozen.
Arabic V4.2 remains closed.
Reserved Arabic populations remain closed.
