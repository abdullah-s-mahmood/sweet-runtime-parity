# ACAD_PASS — V2.4 Scalability Higher-Model Decision V1

Date: 2026-10-05
Status: ACCEPTED / AUTHORIZE NARROW V2.5 MATCHER REPLACEMENT ONLY

Source:
user-mediated focused higher-model review.

Verdict:
`B. VERSION_BUMP_BEFORE_FACTPICO`

## 1. Core decision

Create:
`AT0-EN V2.5`

Scope:
exact scalable replacement of the frozen B1.1 factorial one-to-one matcher, plus execution/freeze identity controls only.

Canonical V2.4 remains unchanged and preserved as:
`NOT_RUN — PRE-PREDICTION SCALABILITY BLOCKER`

No FactPICO semantic result exists for V2.4.

## 2. Scientific rationale

Running canonical V2.4 with a predeclared timeout would be a valid resource-constrained operational baseline, but an avoidably confounded first semantic/critical-fidelity assessment because known factorial cost could determine which records complete.

A canonical external V2.4 FactPICO baseline is therefore optional, not scientifically mandatory.

## 3. Exact matcher semantics to preserve

Replacement must preserve exactly:

Priority 1:
minimize total hard-owner mismatches.

Priority 2:
maximize total owner similarity.

Priority 3:
maximize total semantic similarity.

Tie policy:
for exactly equal computed objective triples, choose the earliest candidate-index tuple in fixed source order, matching the old strict-improvement enumeration behavior.

Unequal-count behavior:
preserve existing `assertion_groups` semantics:
- take first `min(m,n)` assertions on both sides;
- solve one-to-one assignment only on that square prefix;
- append leftover source/candidate assertions to the final group.

Do NOT silently replace this with rectangular global assignment.

Owner mismatch remains a first-priority finite cost, not a forbidden edge.

## 4. Numeric policy

V2.5 must explicitly freeze:
- score arithmetic;
- comparison semantics;
- tie handling;
- solver implementation/version;
- deterministic ordering.

Any numeric discrepancy from legacy float accumulation must be documented and explained before runtime freeze.

## 5. Minimum regression evidence

Before any FactPICO prediction:

1. Existing B1/B2 integration:
   - rerun canonical development/regression cases;
   - compare individual mappings/groups, relation endpoints/statuses, evidence references and final outcomes;
   - retain B2.2 EE 12/12, safe 5/5, unsafe PASS 0/6, and uncertainty behavior.

2. Assignment equivalence:
   - frozen synthetic bank;
   - brute-force enumeration oracle for manageable n (2–6);
   - unique optima, competing priorities, unavoidable owner mismatches, full/partial ties, duplicate-looking assertions with distinct IDs, near-ties;
   - compare objective triple and selected mapping.

3. Grouping/boundary:
   - equal counts;
   - singleton split/merge;
   - unequal counts both directions;
   - empty/singleton validation boundaries;
   - preserve leftovers/order/occurrence identity.

4. Safety/adversarial:
   - existing owner/value/group swaps;
   - relation reversal;
   - scope/time/baseline;
   - polarity/modality/causality;
   - uncertainty;
   - faithful split/merge;
   - at least one tie where alternate mapping changes downstream behavior.

5. Scalability:
   - synthetic 9/10/12 plus larger predeclared supported n;
   - tie-heavy and unequal-count inputs;
   - measure matching/integration runtime and peak memory;
   - do NOT brute-force infeasible n.

6. Reproducibility/failure:
   - repeated fresh-process deterministic outputs;
   - synthetic timeout/crash path gives exactly one INVALID per affected ID;
   - no provisional/best-so-far PASS.

## 6. Acceptance conditions

- exact optimization demonstrated;
- tie policy demonstrated;
- no unexplained behavior differences;
- no newly unsafe PASS;
- no lost safe-control acceptance;
- no hidden conversion to REVIEW/INVALID;
- all supported in-envelope synthetic cases complete within frozen resource budget;
- every discrepancy documented.

## 7. FactPICO boundary

FactPICO remains prospectively unpredicted.

Do NOT use FactPICO:
- texts;
- source-derived graphs;
- assertion counts;
- timing;
- parameter selection;
- matcher testing.

Static/public artifact knowledge remains distinct from prediction exposure.

## 8. Current authorization

Implementation agent MAY:
- specify exact objective/numeric/tie/resource envelope;
- implement V2.5 scalable matcher;
- run existing development/regression cases;
- run bounded synthetic checks;
- freeze new runtime/config/solver identity;
- create dated FactPICO execution-identity amendment.

Implementation agent MUST STOP at:
`V2.5 SCALABLE-MATCHER REGRESSION + RUNTIME FREEZE / PRE-PREDICTION REVIEW`

Still forbidden:
- FactPICO prediction;
- FactPICO scoring;
- threshold changes;
- H1/H2/H3/H4 redesign;
- custom Gate C opening;
- broad architecture implementation;
- human recruitment;
- Arabic-track work.
