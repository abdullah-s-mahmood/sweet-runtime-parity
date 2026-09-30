# MP-SEF TARGET AND MATCHING CONTRACT V1

Date: 2026-09-30
Status: FROZEN BEFORE FEASIBILITY MEASUREMENT

## 1. Scope

This contract defines the reference target set and scoring semantics for the first MP-SEF candidate-feasibility cycle.

Population:
D_DEV_FEAS_V1 only.

Cycle scope:
NoPnx linguistic correction.

## 2. Source of truth

Targets derive only from the frozen CALIBRATION record/reference and the already frozen official-alignment NoPnx construction rules.

No new annotation or reference repair is introduced for the first feasibility cycle.

## 3. Target unit

A reference target is a complete frozen NoPnx correction unit under the official alignment/matching representation.

A target is not:
- an arbitrary character difference;
- a partial component of a coupled correction;
- a gold-guided fragment extracted from a proposer bundle.

Each target has:
- target_id;
- source_record_id;
- source span/effect identity;
- complete reference replacement/effect;
- operation family;
- punctuation scope;
- matching identity/version.

## 4. Punctuation scope

Primary target denominator excludes punctuation-only corrections for this first cycle.

Mandatory reporting:
- number of punctuation-only targets;
- number of mixed punctuation+linguistic targets;
- how mixed targets are represented.

Mixed reference targets are not silently split merely to improve NoPnx recall unless the frozen official target construction already defines a separable linguistic target independently of proposer output.

## 5. Matching principle

A legal candidate output y is scored against the frozen target set G_s using a single frozen representation-invariant matching function.

Matching is based on achieved source-to-output correction effect under the official-alignment definition.

No proposer-specific tag identity is required.

## 6. TP_fixed

For a legal output y and target set G_s:

TP_fixed(y,G_s)

counts complete frozen reference targets achieved by y.

Rules:
- one target can receive at most one credit;
- no half-credit;
- no duplicate credit;
- no credit for a component that does not achieve the full frozen target;
- no reference-driven split of candidate bundles;
- no reference-driven repair of candidate alignment.

## 7. Primary metric

R_joint(P) =
sum_s max_{y in A_s(P)} TP_fixed(y,G_s)
/
sum_s |G_s|

The action space A_s(P) must be frozen before G_s is consulted for scoring.

## 8. Exact optimization

Preferred:
exact maximization over the legal action space.

If exact optimization is not feasible:
- compute a mathematically valid lower bound L;
- compute a mathematically valid upper bound U;
- report [L,U].

Decision:
- PASS only if L >=0.95;
- FAIL only if U <0.95;
- otherwise INCONCLUSIVE.

A greedy result alone is not called R_joint.

## 9. R_raw

For each reference target, ask whether at least one legal action in A_s(P) achieves that complete target.

R_raw =
reachable complete targets / all in-scope targets.

R_raw ignores whether all individually reachable targets can be realized jointly in one output.

Expected:
R_raw >= R_joint.

## 10. R_clean

R_clean is the maximum target recall achievable by a legal action that contains no extra reference-incompatible edit under the same frozen reference comparison.

R_clean is a reference-based diagnostic, not a full semantic safety proof.

## 11. Complete-sentence repair

For erroneous source sentences only:

complete_sentence_repair =
sentences for which one legal action achieves all frozen in-scope reference targets with no extra reference-incompatible edits
/
erroneous sentences

Reference-clean sentences are reported separately.

## 12. Clean-sentence proposal rate

For reference-clean sentences:

clean_proposal_rate =
clean sentences with >=1 raw non-KEEP proposal
/
reference-clean sentences

Also report total raw proposals on clean sentences.

## 13. Per-proposer metrics

Using identical target/matching semantics:
- R_P1 = R_joint({P1});
- R_P2 = R_joint({P2});
- R_pair = R_joint({P1,P2}).

Leave-one-out:
- Delta_P1 = R_pair - R_P2;
- Delta_P2 = R_pair - R_P1.

## 14. Coverage quadrants

Each complete target belongs to exactly one reachability quadrant:
- BOTH;
- P1_ONLY;
- P2_ONLY;
- NEITHER.

This is raw target reachability, not proof that all targets in a quadrant can be jointly realized.

## 15. Family reporting

Report:
- target count;
- sentence count;
- document/cluster count where available;
- micro recall;
- per-family recall;
- macro average across non-empty frozen families.

Empty family:
N/A.

No family denominator may be created or removed after metrics are observed.

## 16. Historical comparison

H1-v1 historical recall 69.39% remains a separate frozen historical metric.

Do not subtract it from R_joint unless a validated mapping establishes:
- same population;
- same target unit;
- same punctuation scope;
- same matching semantics.

Otherwise comparison is:
NOT COMPARABLE.

## 17. Residual target set

A historical-H1 residual set may be reported secondarily only if constructed with a frozen compatibility mapping before pair metrics are inspected.

It does not replace the primary all-target D_DEV_FEAS_V1 denominator in this V1 cycle.

## 18. Failures

Records with:
- proposer execution failure;
- truncation;
- unalignable output;
- non-executable bundles;
remain in the source population.

Their unreachable reference targets remain in denominators.

No complete-case-only scoring is permitted.

## 19. Alternative references

The first cycle uses the frozen reference representation already established in CALIBRATION.

Do not:
- choose among alternatives after seeing proposer output;
- synthesize a hybrid gold;
- adjudicate alternatives to rescue the gate.

Human adjudication of valid alternatives may be a later diagnostic only and cannot retroactively convert this first-cycle decision.

## 20. Gate

Primary candidate availability gate:
R_joint(P1,P2) >=0.95

Developmental population label:
DEV-ORIGIN / DEVELOPMENTAL / NOT INDEPENDENT

Passing this gate means candidate availability only.

It does not imply:
- independent generalization;
- selector success;
- precision;
- semantic fidelity;
- AUTO_SAFE authorization.
