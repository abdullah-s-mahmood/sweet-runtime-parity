# AT0-EN V2.3 — Offline Relation-Graph Verifier Contract

Date: 2026-10-03
Status: IMPLEMENTATION GATE / OFFLINE ONLY
Predecessor decision: V2.2 diagnostic-only; no new live inference.

## Objective

Replace case-specific lexical-presence verification with a typed source-relation ledger and a generic verifier.

The verifier checks what the source asserts. It does not determine whether the source claim is externally true.

## Core rule

Case identity selects only a list of frozen relation records. It MUST NOT select case-specific Python logic.

Each relation record contains:
- relation_id
- type
- subject / object / value as applicable
- polarity
- modality / evidential strength where applicable
- scope / time / group / baseline qualifiers
- citation or equation identity where applicable
- generic extraction hints / aliases
- disposition on unresolved extraction

Generic relation types:
- TEXT_ASSERTION
- MODALITY
- SCOPE
- CARDINALITY
- QUANTITY_BINDING
- ASSOCIATION
- CAUSALITY
- POLARITY
- CITATION_EDGE
- EQUATION_IDENTITY
- TERM_DEFINITION
- METHOD_STEP
- ORDER_BEFORE
- EXCLUSION
- METRIC_DEFINITION
- PARAMETER_STABILITY
- DELTA_DIRECTION
- MECHANISM_DISTINCTION

## Decision policy

For every protected relation:
- VERIFIED: relation is positively reconstructed without contradiction.
- VIOLATED: contradictory/rebound/reversed relation is detected.
- UNRESOLVED: required relation cannot be reconstructed with sufficient confidence.

Candidate disposition:
- any VIOLATED => REJECT
- no violations but >=1 UNRESOLVED => REVIEW
- all protected relations VERIFIED => PASS_CANDIDATE

PASS_CANDIDATE is a bounded synthetic engineering outcome, not proof of general scientific fidelity.

## Anti-overfit rule

No `if case_id == ...` or equivalent case-specific branching is permitted in verifier logic.

Case-specific information lives only in the frozen relation ledger.

## Frozen development gates

Before V2.3 can be reviewed for any future live protocol:
1. all 12 V2.2 SAFE controls must remain acceptable;
2. all 24 V2.2 REDTEAM_V1 attacks must be NOT PASS;
3. the known EN01 modality false-negative must be NOT PASS;
4. frozen V2.1 candidates must receive relation-level dispositions;
5. unresolved scientific relations must become REVIEW;
6. after rules are frozen, create a fresh counterfactual suite not used to develop V2.3.

No model generation is authorized in this phase.
