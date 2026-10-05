# ACAD_PASS — FactPICO V2.5 Failure-Analysis Taxonomy V1

Date: 2026-10-05
Status: FROZEN BEFORE CASE CODING / DIAGNOSTIC ONLY / NO REPAIR IMPLEMENTATION

Purpose:
Classify the already-frozen 345 FactPICO cases without changing predictions, gold, labels, thresholds, denominators, runtime, scorer, or results.

Each case may receive multiple evidence-backed mechanism codes. A primary code is assigned only when the frozen trace directly supports it. Otherwise the case is marked UNRESOLVED.

## Evidence levels

- ESTABLISHED_MECHANISM: directly demonstrated by frozen trace + executed code path.
- SUPPORTED_HYPOTHESIS: consistent with frozen trace and static code, but causal attribution is not uniquely established.
- UNRESOLVED: required trace is absent or competing explanations remain.

## Diagnostic codes

### D1 — EXTRACTION_UNCERTAINTY_PROPAGATED
Trigger:
at least one assertion alignment is UNCERTAIN with reason indicating preserved source/candidate extraction uncertainty.

Interpretation:
the aligner receives at least one non-CERTAIN extracted assertion group; pair_outcome maps any surviving UNCERTAIN to REVIEW unless a critical reject condition dominates.

Evidence class:
ESTABLISHED_MECHANISM for the REVIEW trigger.
Root cause inside extraction remains a SUPPORTED_HYPOTHESIS unless the underlying extraction trace identifies the unresolved slot.

### D2 — RELATION_UNCERTAINTY_PROPAGATED
Trigger:
relation alignment status UNCERTAIN.

Interpretation:
relation confidence is non-CERTAIN and therefore contributes directly to REVIEW.

### D3 — CRITICAL_BINDING_OR_SEMANTIC_MISMATCH
Trigger:
CRITICAL assertion alignment has status ALTERED or CONTRADICTORY.

Subcodes from frozen reason:
- D3_TIME_BINDING
- D3_POPULATION_BINDING
- D3_BASELINE_BINDING
- D3_SCOPE_BINDING
- D3_OWNER_VALUE_BINDING
- D3_PREDICATE_CHANGE
- D3_CONCEPT_COVERAGE
- D3_MODALITY
- D3_POLARITY_CAUSALITY
- D3_RELATION_PROPAGATION

Interpretation:
direct mechanistic cause of REJECT under pair_outcome.

### D4 — CRITICAL_RELATION_FAILURE
Trigger:
CRITICAL relation alignment is ALTERED, CONTRADICTORY, OMITTED, or NEW_INFORMATION.

Interpretation:
direct cause of REJECT and may propagate ALTERED to endpoint assertions.

### D5 — NONCRITICAL_MISMATCH_WITHOUT_DECISIVE_REJECTION
Trigger:
non-CRITICAL ALTERED/CONTRADICTORY/OMITTED/NEW_INFORMATION exists but no CRITICAL reject condition.

Interpretation:
does not itself force REJECT under the frozen decision rule; pair may still REVIEW due to uncertainty or PASS if no uncertainty remains.

### D6 — DECISION_RULE_UNCERTAINTY_GATE
Trigger:
final outcome REVIEW and at least one UNCERTAIN alignment.

Interpretation:
the frozen decision map is explicitly:
critical bad -> REJECT;
else any UNCERTAIN -> REVIEW;
else PASS_CANDIDATE.
This code describes the final gating mechanism, not the upstream cause.

### D7 — REPRESENTATION_GRANULARITY_OR_COUNT_IMBALANCE
Trigger:
frozen alignment groups exhibit one-to-many or many-to-one source/candidate ID grouping, or evidence suggests substantial clause/assertion fragmentation.

Interpretation:
SUPPORTED_HYPOTHESIS for an upstream representation mismatch; never sufficient alone to claim root cause.

### D8 — FACTPICO_CONSTRUCT_RUNTIME_SCOPE_MISMATCH
Trigger:
no trace-local defect uniquely explains the failure and static inspection shows the runtime's assertion vocabulary/extraction rules are narrower than general biomedical RCT prose.

Interpretation:
SUPPORTED_HYPOTHESIS only. Must not be used as a catch-all or performance excuse.

### D9 — TRACE_INSUFFICIENT
Trigger:
a causal attribution would require extractor-internal artifacts not preserved in the frozen prediction output.

Interpretation:
UNRESOLVED. No rerun is permitted to manufacture missing evidence.

## Primary-cause assignment priority

For REJECT:
D4 > D3 > D9.

For REVIEW:
D1/D2 upstream evidence first; D6 records the final gating mechanism.
D7/D8 may be secondary supported hypotheses only.
If no direct upstream trace exists: D9.

For PASS_CANDIDATE:
no failure code.

## Required reporting

Report counts by:
- all 345 records;
- SAFE_STRICT_CONTROL, prioritizing its 6 REJECT + 28 REVIEW;
- ERROR_STRICT, prioritizing its 16 REJECT + 133 REVIEW;
- INTERMEDIATE and N_A_SOURCE_DIAGNOSTIC diagnostically only;
- model type where useful.

For every sampled/manual example used in the report, preserve:
- record_id;
- source_cluster_id;
- gold class;
- frozen prediction;
- trace status/reason;
- evidence excerpt;
- mechanism code;
- evidence level;
- plausible alternative explanation.

No code/runtime modification is authorized by this taxonomy.
