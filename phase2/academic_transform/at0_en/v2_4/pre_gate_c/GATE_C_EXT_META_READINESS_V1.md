# ACAD_PASS — Gate C EXT/META Pre-Execution Readiness V1

Date: 2026-10-04
Status: PRE-EXECUTION / NOT READY FOR BENCHMARK EXECUTION

This file operationalizes the ten mandatory preconditions in:
`GATE_C_EXT_META_PROTOCOL_AMENDMENT_V1.md`

No verifier execution on external evaluation cases is authorized by this file.

## Readiness ledger

| # | Condition | Current status | Evidence required before PASS |
|---|---|---|---|
| 1 | Independent review of amendment | PENDING | external/higher-model review of amendment + this readiness contract |
| 2 | Dataset artifacts, versions, access, licenses | NOT READY | exact artifact/version/access/license records for every hard-track dataset |
| 3 | Eligible splits/IDs + human-label provenance | NOT READY | frozen IDs, labels used, excluded IDs and provenance |
| 4 | Dataset-specific adapter contracts | NOT READY | one frozen adapter contract per hard dataset |
| 5 | Overlap/source-cluster manifest | NOT READY | DOI/PMID/arXiv/native IDs/hashes/lineage and de-dup report |
| 6 | Metrics, thresholds, sample sizes, statistics | NOT READY | frozen native metrics and justified thresholds per hard track |
| 7 | META oracle contract and case freeze | NOT READY | applicability rules, operators, expected outcomes, controls, seeds, exclusions |
| 8 | Runtime + adapter identity freeze | PARTIAL | runtime already frozen; adapter hashes not yet available |
| 9 | Prior exposure + prediction/gold separation | NOT READY | exposure register and prediction-input/gold-join separation plan |
| 10 | One-shot failure/exclusion/retest/full-report policy | PARTIAL | original Gate C principles exist; EXT/META-specific policy must be frozen |

Current overall readiness:
`NOT_READY_GATE_C_EXT_META`

## A. Hard-track candidate inventory

### H1 — Scientific transformation fidelity

Candidate pool:
- CLEF SimpleText 2025 manually annotated real-system submissions
- PLABA/TREC eligible human-faithfulness/completeness units
- FactPICO
- FaReBio
- LongSciVerify

Required final composition:
- >=1 direct scientific-transformation human-judgment source
- >=1 independent expert scientific-factuality source with different construction/granularity

Selection is not frozen yet.

### H2 — Claim/evidence

Primary:
- SciFact

Need:
- exact public labeled split/version
- exact eligible label semantics
- no full-rewrite overclaim

### H3 — Relation fidelity

Primary:
- QASemConsistency

Need:
- exact release/version
- underlying dataset lineage
- relation-level eligible records
- overlap manifest

### H4 — META

Need:
- frozen authentic source pool or source-construction rule
- exact applicability predicates
- PASS/REJECT/REVIEW oracle conditions
- matched controls
- source clustering
- seed policy
- case-count/sample-size plan

## B. Diagnostic inventory

Initial diagnostic-only:
- DeFacto
- USB
- PlainFact
- QASPER
- FENICE
- TRUE or AggreFact
- expert-edited 2026 scientific simplification corpus
- optional additional long-document benchmark

No diagnostic track may be promoted after verifier outputs are inspected.

## C. Mandatory dataset adapter contract template

Each hard dataset must have a versioned contract containing:

1. Dataset name + citation
2. Release/version/date
3. License and access route
4. Raw artifact file names
5. Raw artifact hashes
6. Native task and label definitions
7. Human/expert annotation provenance
8. Source/candidate/context fields
9. Eligible split(s)
10. Eligible record IDs
11. Exclusion rules
12. Exact ACAD_PASS input construction
13. Exact native-label preservation or mapping
14. ACAD_PASS decision semantics, if mapped
15. Native metric(s)
16. Progression threshold(s)
17. INVALID/missing-output handling
18. Source-cluster definition
19. Overlap/lineage fields
20. Prior-exposure note
21. Adapter code/config hash
22. Prediction/gold separation method

No implicit label mapping is allowed.

## D. Hard safety invariants

For every eligible mapped critical case:

- unsafe automatic PASS = 0
- critical silent scientific error = 0
- critical uncertainty -> automatic PASS = 0
- unsupported critical evidence used for automatic critical decision = 0

A single confirmed hard-gate violation yields:
`FAIL_GATE_C_EXT_META_SAFETY`

No averaging.

## E. META validity checklist

Every META family must answer YES:

1. Is the source relation explicit enough to establish the oracle?
2. Is the transformation deterministic or fully seeded?
3. Is the expected semantic consequence guaranteed by the transformation?
4. Are edge cases that break the oracle excluded before prediction?
5. Is there a matched control against trivial reject/review-all behavior?
6. Is source identity/cluster tracked?
7. Is class leakage prevented where feasible?
8. Is the case immutable before prediction?
9. Are invalid transformations retained in audit history but excluded by a preregistered rule?
10. Is the operator independent of verifier output?

Any NO:
family is not ready for hard-gate use.

## F. Prediction/gold separation for public benchmarks

Public benchmark labels may already be available to researchers and therefore cannot be represented as secret untouched holdout labels.

Required procedural separation:
1. freeze eligible IDs before predictions;
2. construct prediction inputs without gold/rationale/correction fields;
3. freeze adapter;
4. freeze runtime identity;
5. run predictions once;
6. hash predictions;
7. then join predictions to frozen gold for scoring;
8. preserve all failures/invalid outputs.

Report benchmark exposure honestly.

## G. Statistical contract requirements

Before execution, freeze per hard track:
- denominator
- source-cluster unit
- metric
- threshold
- confidence interval method
- zero-event treatment
- missing/invalid output treatment
- subgroup reporting
- any bootstrap/randomization seeds

Heterogeneous track Ns must not be summed into one fake independent N.

## H. Full-report policy

Every hard-track report must include:
- total raw records
- selected eligible records
- exclusions by reason
- unique source clusters
- overlap removals
- invalid outputs
- native metric results
- mapped safety results where applicable
- uncertainty intervals
- all hard failures
- adapter/runtime/prediction artifact hashes

Negative evidence must remain visible.

## I. Current blockers

1. No independent review yet of the new amendment/readiness contract.
2. Exact external dataset releases/files have not yet been frozen.
3. Exact hard-track dataset membership has not yet been selected.
4. Adapter semantics and thresholds have not yet been frozen.
5. Overlap manifest does not yet exist.
6. META case-generation/oracle contract is not yet frozen.

These are methodological readiness blockers, not verifier failures.

## J. Next authorized action

`USER-MEDIATED HIGHER-MODEL PRE-EXECUTION REVIEW`

The review must decide whether:
- the amendment preserves construct validity;
- the hard/diagnostic split is defensible;
- FactPICO/FaReBio/LongSciVerify should be mandatory or conditional H1 components;
- the readiness conditions are sufficient;
- any residual human requirement remains before execution.

Until that review returns:

`NO EXTERNAL BENCHMARK EXECUTION`
`NO CUSTOM 80-STUDY HOLDOUT OPENING`
`NO NEW HUMAN RECRUITMENT`
`NO V2.4 RUNTIME CHANGE`
