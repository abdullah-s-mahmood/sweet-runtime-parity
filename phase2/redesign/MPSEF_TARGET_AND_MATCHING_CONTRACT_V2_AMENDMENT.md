# MP-SEF TARGET AND MATCHING CONTRACT — V2 EVALUATION-LAYER AMENDMENT

Date: 2026-10-01
Status: **FROZEN FOR CORRECTED V2 CYCLE BEFORE SECOND PREFLIGHT**

Parent:
`MPSEF_TARGET_AND_MATCHING_CONTRACT_V1.md`

This amendment resolves the ambiguity identified in the independent review.
Where this amendment conflicts with V1 wording, this amendment governs the
corrected V2 cycle. It does NOT change population, action space, or the 95% gate.

## 1. Three strictly separated layers

### Layer A — execution/legalization

Inputs:
- frozen source;
- frozen proposer outputs;
- frozen protection policy;
- source-only runtime/provenance evidence.

Gold/reference access:
**FORBIDDEN**

Outputs:
- executable/non-executable hypothesis states;
- A_primary action sets.

This layer is frozen before reference access.

### Layer B — diagnostic decomposition

Inputs:
- frozen source;
- frozen proposer output;
- source-only diagnostic alignment evidence.

Gold/reference access:
**FORBIDDEN**

Outputs:
- diagnostic components for R_raw/family diagnostics only.

These components are never executable.

### Layer C — evaluation matching

Inputs:
- an already frozen legal whole action;
- frozen reference targets.

Gold/reference access:
**ALLOWED ONLY FOR EVALUATION**

The corrected V2 scorer may use the frozen official M2 evaluation algorithm,
including gold-aware M2 path weighting, solely to decide which frozen complete
reference targets are achieved by the already frozen whole action.

Evaluation matching may NOT:
- add or remove an action;
- change executable state;
- split a bundle;
- repair protection;
- change source anchoring;
- change diagnostic components;
- shrink the denominator;
- create R_raw evidence;
- write back into Layer A or Layer B.

Therefore gold-aware M2 path selection is an **evaluation-only exception** to
any broader historical wording that could otherwise be read as prohibiting
reference use in the scoring alignment itself.

## 2. Target scope/family definition

Corrected V2 uses:
`MPSEF_TARGET_FAMILY_MAP_V2.md`

The historical V1 map does not govern corrected V2 punctuation/boundary scope.

## 3. Scoring failures

If a legal whole action cannot be evaluated:
- legality remains unchanged;
- target denominator remains unchanged;
- its exact credit is unknown, not zero;
- scorer reports a proven interval `[L,U]`.

Primary PASS:
- exact/lower bound >=0.95.

Primary FAIL:
- exact/upper bound <0.95.

Otherwise:
- INCONCLUSIVE.

## 4. TP_fixed

Each complete frozen target receives at most one credit from one evaluated
whole action.

No duplicate credit.
No partial credit.
No gold-guided target split.
No target alternative selection.

Corrupt/ambiguous target construction invalidates the measurement rather than
dropping the target.

## 5. R_joint

For each sentence:
- enumerate only frozen legal KEEP/P1_FINAL/P2_FINAL whole actions;
- score each action;
- choose the single action with maximum complete-target credit.

Never union target hits from different actions in one sentence.

## 6. R_raw

R_raw reads only Layer-B frozen diagnostic evidence.

Evaluation-layer M2 edits are not R_raw components.

Diagnostic ambiguity is represented by bounds rather than by selecting the
gold-favorable decomposition.

R_raw can diagnose decomposition/fusion opportunity but cannot alter A_primary.

## 7. Protected actions

Protected blocking occurs only in Layer A.

The evaluation layer cannot rescue a blocked action, and blocked targets remain
visible in population/denominator accounting.

## 8. Family/secondary accounting

Corrected V2 reports:
- R_P1 / R_P2 / R_pair;
- Delta_P1 / Delta_P2 as intervals where necessary;
- R_raw and gap when exact;
- R_clean;
- complete-sentence repair;
- clean-sentence proposer activity;
- family target/sentence/cluster counts;
- family macro interval;
- weak-family routes;
- candidate-set size before/after exact-text dedup;
- final source-only failure states;
- protected-policy accounting;
- per-sentence audit.

Unknown is never silently converted to zero.

## 9. Claim scope

Unchanged:

**DEVELOPMENT FEASIBILITY / ADAPTIVELY CONSUMED QALB-2014 ORIGIN /
NOT INDEPENDENT GENERALIZATION EVIDENCE**

No corrected V2 result alone authorizes selector training, AUTO_SAFE, reserved
sets, or Phase 3.
