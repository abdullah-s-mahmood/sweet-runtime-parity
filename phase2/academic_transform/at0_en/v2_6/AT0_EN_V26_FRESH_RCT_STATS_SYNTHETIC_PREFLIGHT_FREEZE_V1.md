# ACAD_PASS — Fresh RCT Trial-Balanced Statistics Synthetic Preflight Freeze V1

Date: 2026-10-08

State:
`FRESH_RCT_TRIAL_BALANCED_STATS_SYNTHETIC_PREFLIGHT_PASS`

Scientific/new-data status:
- new RCT data used = false
- SEALED_FRESH_EVAL used = false
- model used = false
- annotation used = false
- acquisition authorized = false

## Official run

Workflow:
`Fresh RCT trial-balanced statistics synthetic preflight`

Run:
`37828307955`

Head SHA:
`8737ed38dd85139cf0497adcd5978e4f75323ce8`

Conclusion:
`SUCCESS`

Artifact:
- ID `11572557395`
- name `fresh-rct-trial-balanced-stats-synthetic-preflight`
- digest `sha256:f9f8f5cd80b0936f8183aacfe008525949428a1f5b310f401c6b233838668926`

## Frozen implementation

Script:
`phase2/academic_transform/at0_en/v2_6/fresh_rct_trial_balanced_precision.py`

Runtime:
`requirements/fresh_rct_stats.txt`

Pinned SciPy:
`1.17.0`

## Verified numerical fixtures

One-sided Clopper-Pearson with per-class alpha=.0125:

- 95/100 -> `0.8772335911610268`
- 190/200 -> `0.9037442005509154`
- 475/500 -> `0.9235837897122915`

These reproduce the independent review's stated planning values.

## Verified selection mechanics

HMAC domain:
`ACAD_PASS_FRESH2026_V1|precision-audit`

The synthetic closure verified:
- exactly one accepted prediction selected per class/family;
- selection uses a 256-bit secret;
- selection is independent of gold correctness;
- selection is independent of model confidence;
- changing the secret changes the synthetic selection;
- duplicate accepted prediction identities fail closed;
- malformed coordinates/classes fail closed.

The HMAC selection happens before gold correctness join.

## Verified support/bound rules

Frozen:
- minimum contributing families/class = 200;
- lower bound threshold/class = .90;
- alpha/class = .0125.

Synthetic:
- 190/200 for every class -> PASS;
- 95/100 for every class -> FAIL.

## Estimand boundary

This implementation evaluates:
`TRIAL_BALANCED_PRECISION_ONE_ACCEPTED_SPAN_PER_CLASS_PER_FAMILY`

It MUST NOT be described as an exact confidence bound for pooled entity-weighted population precision.

Pooled entity exact-span precision remains a separate point-estimate gate.

## Current effect on readiness

This closes only the synthetic statistical-implementation item.

It does NOT close:
- human annotator readiness;
- adjudicator readiness;
- independent custodian;
- funding/resource feasibility;
- prior-exposure inventory completeness;
- protected-corpus fingerprint custody;
- EVAL access control;
- complete annotation-manual packaging;
- retrieval archive tooling;
- trial-family provenance tooling;
- acquisition sign-off.

Therefore:
`ACQUISITION_REMAINS_BLOCKED`
