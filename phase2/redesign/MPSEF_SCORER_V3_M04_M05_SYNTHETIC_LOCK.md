# MP-SEF SCORER V3 M04/M05 SYNTHETIC PREFLIGHT LOCK

Date: 2026-10-01
Status: PASS / SYNTHETIC-ONLY
Gold/reference population use: NONE
Project measurement: NOT RUN

## Purpose

Freeze the synthetic closure of independent-review findings M04 and M05 without modifying historical scorer V2 evidence.

## Implementation

File:
`phase2/redesign/mpsef_rjoint_score_v3.py`

Implementation commit:
`7a01d797e5fd630186910e38f5487364639e8165`

Scorer identity:
`MPSEF_RJOINT_SCORER_V3_M04_M05`

Historical V2 remains unchanged.

## M04 closure

Problem:
when every eligible action failed scoring, V2 could infer target_count=0 from the empty successful-action set and return an exact [0,0] interval even when the frozen sentence target denominator N>0.

V3 rule:
- target_count is supplied from the independently prebuilt frozen target population;
- every successful action score must agree with that target_count;
- if all actions fail and N>0, bounds are [0,N];
- N=0 remains zero/N/A at ratio level.

Synthetic regression:
PASS.

## M05 closure

Problem:
BOUNDARY={SPLIT,MERGE} could sum independent per-family maxima from different whole actions (sum(max)) instead of maximizing one whole action over the union (max(sum)).

V3 rule:
- weak-group bounds are computed sentence-wise over the union of member target indices;
- one whole action determines the group score;
- additional-target and additional-cluster lower/upper evidence follows the same whole-action semantics;
- scoring failures preserve conservative uncertainty.

Synthetic regression:
PASS.

## Workflow evidence

Workflow:
`Phase 2 MP-SEF Scorer V3 Synthetic Preflight`

Run:
`36867448366`

Head SHA:
`7a01d797e5fd630186910e38f5487364639e8165`

Conclusion:
`SUCCESS`

Observed output:
`{"self_test":"PASS","scorer_version":"MPSEF_RJOINT_SCORER_V3_M04_M05"}`

Artifact:
- id: `11164975245`
- name: `mpsef-scorer-v3-synthetic-preflight`
- ZIP digest:
  `sha256:1ed7076c272e66dfe1b4168568113d76c4294db863418352af210ffaae90bb65`

## Scientific interpretation

M04 and M05 are CLOSED at synthetic implementation level.

This does NOT:
- authorize project measurement;
- authorize project gold;
- validate V4 action-set compatibility;
- compute R_joint;
- change any historical V2 result.

A future gold-aware scorer/guard must be separately versioned, bound to the new proposer registry/action artifacts, preflighted, independently reviewed, and explicitly authorized.
