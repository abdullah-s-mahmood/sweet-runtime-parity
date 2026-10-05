# ACAD_PASS — AT0-EN V2.5 Exact Scalable Matcher Specification V1

Date: 2026-10-05
Status: FROZEN IMPLEMENTATION SPECIFICATION / NO FACTPICO EXECUTION

Parent runtime:
`AT0-EN V2.4`

Reason for version bump:
canonical V2.4 B1.1 matcher uses factorial permutation enumeration and failed synthetic scalability preflight before any FactPICO prediction.

Independent reviewer verdict:
`B. VERSION_BUMP_BEFORE_FACTPICO`

## 1. Narrow authorization boundary

V2.5 changes ONLY the one-to-one assertion assignment implementation and the minimum execution/freeze identity needed to support it.

Unchanged from V2.4:
- tokenization;
- normalization/synonym table;
- owner extraction;
- owner incompatibility rule;
- assertion-similarity feature formula;
- criticality;
- outcome rules;
- relation alignment;
- grouping behavior;
- unequal-count slicing/leftover behavior;
- extractors;
- H1 FactPICO V5 gold/thresholds/input/gold artifacts.

No scientific threshold or weight changes are authorized.

## 2. Legacy objective

For an assignment of source assertions to candidate assertions, V2.4 lexicographically maximizes:

1. `- total_hard_owner_mismatches`
2. `total_owner_similarity`
3. `total_semantic_similarity`

Equivalently V2.5 MUST:

1. minimize total hard-owner mismatches;
2. maximize total owner similarity;
3. maximize total semantic similarity;
4. among exact objective ties, select the lexicographically earliest candidate-index tuple in fixed source order.

The fourth rule reproduces V2.4's first-permutation-wins behavior.

## 3. Pairwise formula preservation

### Owner similarity
Exact Jaccard ratio over the unchanged owner-token sets.

### Semantic similarity
Preserve the V2.4 formula exactly as mathematical rational weights:

- predicate exact match: `4`
- owner Jaccard: `3`
- object Jaccard: `5/2`
- binding-token Jaccard: `2`
- each of time/population/baseline/scope Jaccard: `7/10`
- polarity exact match: `1/2`
- causality exact match: `1/2`
- modality exact match: `3/10`

No feature addition, deletion or reweighting.

## 4. Numerical policy

V2.4 accumulated binary floating-point values.

V2.5 declares:

`NUMERIC_POLICY = EXACT_RATIONAL_FORMULA_V1`

All Jaccard values and the declared decimal weights above are represented as exact rational values before assignment optimization.

This is an explicit numeric-policy change under the new V2.5 identity.

It is NOT claimed to be bitwise-equivalent to every possible V2.4 floating-point near-tie.

Required safeguards before runtime freeze:
- exhaustive differential comparison at feasible sizes;
- explicit near-tie cases;
- no unexplained mapping/outcome differences;
- any numeric-policy difference must be reported, not tolerance-hidden.

## 5. Exact scalarization

For an `n x n` assignment matrix:

1. convert all owner-similarity fractions to exact common-denominator integers;
2. convert all semantic-similarity fractions to exact common-denominator integers;
3. encode the candidate-index tuple as a base-`n+1` positional integer:
   `sum(candidate_index_i * (n+1)^(n-1-i))`;
4. compute dominance weights from proven lower-priority score ranges so that:
   - one hard-mismatch unit dominates every possible owner/semantic/tie difference;
   - one owner integer unit dominates every possible semantic/tie difference;
   - one semantic integer unit dominates every possible tie difference.

No arbitrary epsilon or approximate big-M is permitted.

The resulting integer assignment objective is mathematically equivalent to the declared V2.5 lexicographic objective.

## 6. Solver

Use a deterministic exact square linear-assignment solver implemented with arbitrary-precision integer arithmetic.

Chosen implementation:
`Hungarian algorithm, O(n^3)`

The solver returns a globally optimal assignment for the exact integer objective.

No:
- greedy approximation;
- beam search;
- best-so-far acceptance;
- stochastic tie handling;
- floating approximate assignment.

## 7. Tie policy

Because the positional candidate-index code is the final strictly dominated objective level, exact higher-level ties select:

`lexicographically earliest candidate-index tuple`

for the fixed source order.

This matches the observable V2.4 permutation-order tie policy.

A solver's native arbitrary tie choice is not accepted.

## 8. Unequal-count behavior

Preserve V2.4 exactly:

- if counts equal: exact one-to-one assignment;
- if source count == 1: group source with all candidates;
- if candidate count == 1: group all sources with candidate;
- if both counts >1 and unequal:
  - let `n=min(source_count,candidate_count)`;
  - optimize only `source[:n]` against `candidate[:n]`;
  - append source leftovers to the final source group;
  - append candidate leftovers to the final candidate group.

Do NOT replace this with rectangular global matching in V2.5.

Its limitation remains explicit technical debt.

## 9. Empty-input boundary

The matcher itself must handle `n=0` deterministically.

Integration behavior for empty claim-bearing extraction remains governed by the existing pipeline contract; no vacuous PASS may be introduced by the matcher patch.

Any pre-existing empty-input integration defect discovered during regression must be reported separately, not silently repaired under this authorization.

## 10. Required regression evidence

Before V2.5 runtime freeze:

### A. Existing development integration
Rerun canonical B1/B2 development/regression cases and compare:
- assertion groups/mappings;
- relation endpoints/statuses;
- evidence references;
- final outcomes;
- GG/GE/EG/EE behavior where available.

### B. Assignment equivalence
Exhaustive V2.4 permutation oracle at feasible `n=2..6` on a frozen synthetic bank:
- unique optimum;
- priority conflict;
- unavoidable owner mismatch;
- full tie;
- partial tie;
- duplicate-looking assertions with distinct IDs;
- near-tie numeric cases;
- graph-derived score cases.

Compare objective and selected mapping.

### C. Grouping/boundaries
- equal counts;
- 1:N;
- N:1;
- unequal >1 both directions;
- empty/singleton boundaries.

### D. Safety/adversarial
Preserve existing owner/value/group, reversal, scope/time/baseline, polarity/modality/causality, uncertainty and faithful split/merge behavior.
Include a tie case where alternate mapping would change downstream relation behavior.

### E. Scalability
Synthetic-only sizes at minimum:
`n=9,10,12,16,32`
plus a larger supported size selected without FactPICO profiling.

Measure:
- pair-score construction;
- assignment;
- integrated matcher wall time;
- peak memory where available.

### F. Reproducibility/failure path
Fresh-process repeated runs must produce identical mappings/results.
Synthetic timeout/crash must yield exactly one explicit INVALID record and never a provisional PASS.

## 11. Acceptance conditions

All required:
- exact declared optimum;
- declared tie policy reproduced;
- no unexplained per-case differences;
- no new unsafe PASS;
- no lost previously accepted safe controls;
- no hidden conversion to REVIEW/INVALID;
- in-envelope synthetic cases complete inside frozen budget;
- all numerical differences documented;
- runtime/config/dependency identities frozen.

## 12. FactPICO boundary

Forbidden during V2.5 development/freeze:
- passing any FactPICO source/candidate through extraction or matcher;
- profiling FactPICO assertion counts;
- timing FactPICO;
- using FactPICO graphs for matcher tests;
- FactPICO prediction or scoring.

FactPICO V5 scientific artifacts remain unchanged.

## 13. Stop condition

Stop at:

`V2.5 SCALABLE-MATCHER REGRESSION + RUNTIME FREEZE / PRE-PREDICTION REVIEW`

Separate authorization is required before FactPICO execution.
