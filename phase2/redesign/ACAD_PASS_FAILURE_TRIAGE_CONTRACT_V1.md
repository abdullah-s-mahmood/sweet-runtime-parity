# ACAD_PASS FAILURE TRIAGE AND REPAIRABILITY CONTRACT V1

Date: 2026-10-01
Status: FROZEN PROJECT RULE

## Principle

A FAIL is never accepted as a terminal label without diagnosis.

Every failed gate, hypothesis, workflow, proposer, legalizer, scorer, or preflight check MUST be classified through:

1. observed failure;
2. reproducibility;
3. root-cause evidence;
4. scope of impact;
5. root-cause confidence;
6. repairability class;
7. scientifically safe next action;
8. whether repair is allowed in the current frozen cycle.

The reported FAIL itself is evidence of an outcome, not an explanation of cause.

## Failure classes

Each failure MUST be assigned one primary class:

- INFRASTRUCTURE
- RUNTIME_ENVIRONMENT
- DATA_IDENTITY
- PROVENANCE
- IMPLEMENTATION
- POLICY/LEGALITY
- ALIGNMENT/MATCHING
- METRIC/SCORER
- MODEL/CANDIDATE_QUALITY
- SCIENTIFIC_LIMIT
- UNKNOWN_REQUIRES_DIAGNOSTIC

Secondary causes may also be recorded.

## Repairability classes

- FIXABLE_IN_CURRENT_CYCLE_PRE_GOLD:
  repair is permitted only when it does not mutate a frozen scientific artifact or use forbidden evidence.

- FIXABLE_NEXT_VERSION_ONLY:
  root cause is actionable, but correcting it would mutate or regenerate a frozen artifact. The current artifact remains invalid/blocked and the repair must receive a new explicit version.

- FIXABLE_INFRASTRUCTURE_ONLY:
  retry/fix environment without changing scientific inputs or algorithms.

- NOT_CURRENTLY_FIXABLE:
  no justified repair is known.

- SCIENTIFIC_LIMIT:
  implementation is correct but the method/model does not satisfy the preregistered requirement.

- UNKNOWN:
  diagnosis is insufficient; no repair or scientific interpretation is permitted yet.

## Required evidence

For every nontrivial FAIL record:

- exact failing population/count;
- first reproducible example where applicable;
- frozen hashes/revisions;
- observed vs expected behavior;
- source-only diagnostic whenever legality/provenance is being diagnosed;
- independent implementation/documentation comparison where available;
- whether reserved/gold data were consulted;
- whether the failure changes executability, only diagnostics, or only runtime.

## No metric-only diagnosis

A low metric MUST NOT automatically be labeled a model defect.
A blocked hypothesis MUST NOT automatically be assigned zero linguistic quality.
An execution/provenance failure MUST NOT be interpreted as poor correction accuracy.

Conversely, a high metric MUST NOT excuse a provenance, truncation, protection, or identity defect.

## Repair discipline

Before changing code:

- reproduce the failure;
- identify the narrowest causal mechanism;
- decide whether the artifact is already frozen/exposed;
- if frozen/exposed, preserve it and create a new versioned cycle rather than overwrite it;
- add a regression test that fails on the old defect and passes on the repair;
- rerun only the minimum authorized stage required to validate the repair.

No gate may be weakened merely because a failure is repairable.

## Current-cycle rule

The current MP-SEF V3 legalizer artifacts are immutable.

Any defect requiring regenerated P1/P2 proposals is therefore FIXABLE_NEXT_VERSION_ONLY for this cycle.

## Reporting

Every future checkpoint containing FAIL/BLOCKED/PARTIAL must include:

- WHY it failed;
- HOW confident the causal diagnosis is;
- WHETHER it is repairable;
- WHERE it may be repaired;
- WHAT evidence is still missing;
- WHETHER the failure affects the current scientific conclusion or only future architecture.

