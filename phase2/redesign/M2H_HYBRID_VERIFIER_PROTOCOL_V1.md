# M2-H — Specialized/Hybrid Verifier Feasibility Protocol v1

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION

## 1. Research question

Can a heterogeneous verifier architecture outperform the closed M2-R LLM residual hunter on:
1. edit discovery;
2. mandatory-error precision;
3. structural edit coverage;
4. clean-text false positives;
5. sentence-level residual/completeness decisions;

without using reserved/confirmation/test evidence?

## 2. Atomic unit

The atomic object is an **evidence-bearing edit candidate**:

{
  sentence_id,
  exact_surface,
  proposed_replacement_or_operation,
  operation_type,
  candidate_sources[],
  evidence_features{},
  component_votes{},
  calibrated_risk,
  disposition
}

Possible dispositions:
- SUPPORTED_MANDATORY
- SUPPORTED_OPTIONAL_OR_ALTERNATIVE
- UNCERTAIN
- REJECTED
- REVIEW

A sentence-level verdict is derived only after edit-level evidence is evaluated.

## 3. Component hypotheses

### H1 — Structured Candidate Generator
A specialized explicit-edit detector/tagger should recover substantially more expert residual edits than the P1 LLM residual hunter.

Target feasibility gate:
- candidate edit-instance recall >= 80%;
- context residual recall >= 90%.

This layer may intentionally over-generate and is NOT a final accept/reject oracle.

### H2 — Orthographic High-Precision Validator
A deterministic or tightly constrained orthographic validator should achieve:
- precision >= 98% on claims it marks SAFE;
- zero known invariant violations;
- report coverage separately.

No promotion if precision is traded for coverage.

### H3 — Morphology-Aware Validator
A morphology-aware component should add evidence beyond surface spelling.

Feasibility target:
- >= 70% recall on morphology-tagged validation subset when n>=20;
- <= 10% false-positive case rate on morphology-clean controls.

If reliable linguistic gold taxonomy is unavailable, this hypothesis remains unresolved rather than relabeled post hoc.

### H4 — Structural Edit Validator
Word-boundary and structural operations must be tested explicitly.

For Split and Merge, when each has n>=20:
- recall >= 70%;
- precision >= 90%.

Delete/Move are reported if n is sufficient; otherwise no broad claim is allowed.

### H5 — Risk Fusion
Combining heterogeneous evidence should outperform every individual component on the same held development packet.

Required:
- false-positive sentence rate <= 10%;
- context residual recall >= 90%;
- strict residual recall >= 90%.

The fusion score must be calibrated from a calibration subset that is disjoint from evaluation.

### H6 — Sentence Completeness
This is a separate hypothesis from edit correctness.

A sentence may be marked CLEAN/COMPLETE only when:
- no component identifies an unresolved mandatory candidate above the preregistered risk threshold;
- no protected invariant fails;
- no structural uncertainty remains;
- the system is not in abstention.

Primary sentence-level safety targets:
- unsafe-clean rate <= 5%;
- clean-text false alarm rate <= 10%;
- abstention/review burden reported, not hidden.

## 4. Development data design

Use QALB14 TRAIN+DEV DEVELOPMENT partition only.

Create three mutually disjoint subsets:
- CALIBRATION
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC

All must exclude every UID already used in M2-R v2 P0 and P1.

No Confirmation/Holdout/reserved/test data may be opened.

Suggested deterministic split of eligible remaining DEVELOPMENT UIDs:
- 50% calibration
- 40% internal evaluation
- 10% stress diagnostic

The exact hash salt must be frozen before materialization.

## 5. Gold and alternative-correction handling

Exact expert edit matches remain the primary reproducible signal.

However:
- exact-reference mismatch != automatically wrong;
- unmatched claims that could be valid alternatives are flagged for later bounded adjudication;
- no claim may be promoted to SAFE solely because a language model prefers it.

Report:
1. strict-reference metrics;
2. alternative-aware metrics only if independently adjudicated;
3. unresolved ambiguity count.

## 6. Calibration

Do not use textual LLM confidence as probability.

If probabilistic fusion is used:
- fit only on CALIBRATION;
- freeze model/weights/thresholds before INTERNAL_EVALUATION;
- report Brier score or log loss if probabilistic labels are meaningful;
- report calibration curve / ECE when sample size permits;
- report selective-risk vs coverage.

No threshold may be tuned on INTERNAL_EVALUATION.

## 7. Required baselines

At minimum compare:
1. M2-R P1 structured LLM residual hunter;
2. best single specialized component;
3. hybrid without LLM reasoning;
4. hybrid with LLM reasoning as ambiguity-only signal.

No baseline may consume different gold for the headline comparison.

## 8. Primary metrics

Edit level:
- candidate recall;
- mandatory-claim precision;
- edit localization recall;
- operation-specific recall/precision;
- alternative/unresolved rate.

Sentence level:
- context residual recall;
- strict residual recall;
- clean false-positive rate;
- unsafe-clean rate;
- complete-sentence coverage;
- review/abstention burden.

Calibration:
- selective risk vs coverage;
- ECE/Brier/log-loss where valid.

## 9. Feasibility success contract

M2-H is considered technically promising only if INTERNAL_EVALUATION achieves all:

1. unsafe-clean rate <= 5%;
2. clean false-positive rate <= 10%;
3. context residual recall >= 90%;
4. strict residual recall >= 90%;
5. mandatory-claim precision >= 90%;
6. edit localization recall >= 70%;
7. no protected-invariant safety failure;
8. hybrid beats M2-R P1 on at least:
   - CFPR by >=10 pp; and
   - GELR by >=10 pp;
   on comparable definitions.

These are development feasibility thresholds, not production claims.

## 10. Stop rules

STOP M2-H without confirmation if any of the following occurs:

- INTERNAL_EVALUATION unsafe-clean rate >10%;
- INTERNAL_EVALUATION CFPR >20%;
- edit localization recall <60%;
- mandatory-claim precision <80%;
- structural component fails to improve Split/Merge coverage materially;
- calibration requires changing thresholds after INTERNAL_EVALUATION is seen;
- hybrid gains come only from increased review burden with negligible safety gain;
- a component duplicates another component's errors without independent value.

No P2-style iterative prompt tuning is allowed.

One implementation revision is allowed only for a demonstrated software/protocol bug, not for scientific underperformance.

## 11. What is not authorized

This protocol does not authorize:
- Confirmation;
- Holdout;
- A7'ta reserve;
- QALB15 TEST;
- reserved Nahw;
- M3 factorial;
- Phase 3;
- production auto-apply.

## 12. First implementation checkpoint

Before any model run:
1. inventory candidate specialized components and licenses;
2. verify whether an Arabic explicit-edit model/checkpoint is practically obtainable;
3. verify CAMeL/morphology tooling compatibility;
4. define the deterministic remaining-development split;
5. freeze component versions and hashes;
6. only then materialize CALIBRATION/INTERNAL_EVALUATION packets.

If the necessary components are not reproducibly obtainable, stop and redesign rather than substitute an unplanned model.
