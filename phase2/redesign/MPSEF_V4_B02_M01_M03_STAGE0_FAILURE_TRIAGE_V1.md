# MP-SEF V4 B02/M01/M03 STAGE0 FAILURE TRIAGE V1

Date: 2026-10-01
Run: `36869315004`
Head SHA: `7ed7edd51d0e89fa335353ce7a7c2fe17d6ec9f1`
Conclusion: FAILURE

## Observed failure

The source-free Stage0 harness reached:
- all B02 tests before M03;
- all M01 tests before M03;
- M03-S01, S02, S03;

then failed at:

`M03-S04_ENTITY_TEXT_CHANGE`

Synthetic case:
`الجرعة 5 mg يوميا -> الجرعة 6 mg يوميا`

Observed diagnostic:
- V3 status: FAIL
- reasons include:
  - PROTECTED_SIGNATURE_CHANGED
  - OPTIMAL_PATH_CAN_SUBSTITUTE_PROTECTED_CHAR
  - NO_OPTIMAL_EXACT_MATCH_FOR_PROTECTED_CHAR
- shadow status: SHADOW_INCONCLUSIVE
- cause: ALIGNMENT_AMBIGUOUS

Expected higher-level diagnostic:
protected entity/signature changed, therefore this cannot be a global-ordinal-only case and must remain shadow-blocked.

## Root cause A — diagnostic precedence

The shadow classifier checked alignment ambiguity before material protected-signature change.

That precedence is incorrect for this diagnostic purpose.

If the protected signature differs, a material protected-entity change is already established directly from source/output protected extraction.

Alignment ambiguity may be retained as a secondary diagnostic, but it must not erase the stronger known fact:
`ENTITY_TEXT_CHANGED`.

## Root cause B — workflow error propagation

The workflow used:

`python ... | tee result.json`

without `set -o pipefail`.

Therefore the Python traceback did not make the execution step fail because `tee` exited successfully.

The following JSON validation step then failed on an empty result file.

This is a workflow fail-open observability defect.

## Classification

A:
`IMPLEMENTATION / POLICY-DIAGNOSTIC PRECEDENCE`

B:
`WORKFLOW / ERROR-PROPAGATION`

Neither is:
- model quality failure;
- candidate quality failure;
- scientific limit;
- gold/reference failure.

## Scope

Affected:
- Stage0 shadow diagnostic classification;
- workflow failure signaling.

Not affected:
- V3 legalizer decision;
- frozen V3 artifacts;
- B01 closure;
- scorer V3 M04/M05;
- project source/gold;
- any linguistic metric.

## Reproducibility

Run:
`36869315004`

The traceback is deterministic for M03-S04 under the current shadow-classifier precedence.

## Confidence

Root-cause confidence:
HIGH.

## Repairability

`CURRENT_CYCLE_PRE_GOLD`

Allowed repairs:
1. classify protected-signature change before alignment-only uncertainty;
2. preserve alignment ambiguity as secondary evidence if desired;
3. never label such case global-ordinal-only;
4. add `set -o pipefail` in workflow execution step.

## Safe next action

Patch only the Stage0 diagnostic harness and workflow error propagation, rerun Stage0, and triage any next failure before further changes.

No Stage1 authorization is implied.
