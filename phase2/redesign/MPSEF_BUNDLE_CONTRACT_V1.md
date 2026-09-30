# MP-SEF BUNDLE CONTRACT V1

Date: 2026-09-30
Status: FROZEN BEFORE FEASIBILITY MEASUREMENT

## 1. Purpose

This contract defines how P1 and P2 outputs are converted into source-anchored hypotheses and executable bundles before any reference-based feasibility metric is computed.

No gold/reference may influence decomposition.

## 2. Immutable source

Every record has:
- source_record_id;
- source_uid;
- source_text;
- source_sha256;
- source_tokenization_version.

All offsets are anchored to this original source.

## 3. Hypothesis object

Required fields:
- hypothesis_id;
- proposer_id;
- proposer_runtime_lock;
- source_record_id;
- source_sha256;
- proposer_output_text;
- proposer_output_sha256;
- execution_status;
- truncation_status;
- alignment_status;
- protected_touch_status;
- provenance_trace.

One final hypothesis per proposer in the first cycle:
- P1: final pass-2 output only;
- P2: final generated output only.

KEEP is represented separately and is always legal unless source integrity fails.

## 4. Provenance

### P1

Store:
- x0 source;
- x1 pass-1 output;
- x2 pass-2 output;
- pass-1 edit trace;
- pass-2 edit trace.

Final hypothesis:
x0 -> x2

x1 is never counted as an independent proposer.

If a pass-2 action depends on text created in pass 1, preserve that dependency in provenance.

### P2

Store:
- x0 source;
- morphology-preprocessed text;
- GED labels;
- GED-expanded subword labels;
- final generated output.

Final hypothesis:
x0 -> final output.

Any difference introduced by morphology/preprocessing remains part of the source-to-final provenance.

## 5. Component edit extraction

A deterministic source-to-output aligner may produce component edits for explanation and execution planning.

Each component contains:
- component_id;
- original source span;
- source text;
- replacement text;
- operation family;
- proposer provenance;
- reversible inverse.

Component extraction is not permission to authorize the component independently.

## 6. Bundle definition

A bundle is the smallest unit that may be treated as independently executable under source/proposer-only evidence.

Required fields:
- bundle_id;
- hypothesis_id;
- component_ids;
- source spans;
- replacement effect;
- requires_bundle_ids;
- mutually_exclusive_bundle_ids;
- unresolved_dependency;
- protected_overlap;
- executable;
- reversible;
- failure_reason.

## 7. Dependency rule

Two or more component edits remain in the same bundle when independence cannot be established without gold/reference information.

Examples:
- agreement changes across noun/adjective;
- paired morphology changes;
- a pass-2 SWEET edit depending on a pass-1 edit;
- seq2seq multi-token rewrite whose grammatical validity depends on combined application.

Non-overlapping character spans do not imply independence.

## 8. Gold-blind decomposition

Before reference access:
- create hypothesis;
- align source to output;
- identify candidate components;
- determine bundles;
- determine requires/mutual exclusion;
- freeze bundle graph.

After this freeze, reference may score actions but may not:
- split bundles;
- merge bundles;
- alter offsets;
- remove components;
- repair a failed alignment;
- reclassify a dependency to improve coverage.

## 9. Alignment ambiguity

If deterministic alignment has multiple materially different decompositions and no source/proposer-only rule selects one:
- mark alignment_status=AMBIGUOUS;
- keep the full hypothesis as one bundle when reversible and executable;
- otherwise mark hypothesis non-executable.

Do not choose an alignment using the reference.

## 10. Textual equivalence

Two bundles are textually equivalent if applying either to the same original source yields the same final source string for the affected execution scope.

Textual equivalence:
- deduplicates candidate-count metrics;
- does not erase proposer provenance;
- does not imply statistical independence.

## 11. Conflicts

Conflict types:
- SPAN_OVERLAP;
- REPLACEMENT_INCOMPATIBLE;
- REQUIRES_VIOLATION;
- MUTUAL_EXCLUSION;
- PROTECTED_POLICY;
- SOURCE_VERSION_MISMATCH;
- EXECUTION_ORDER_CONFLICT.

Conflict resolution must use frozen deterministic rules or remain unresolved.

Reference correctness cannot resolve candidate conflict for action-space construction.

## 12. Reversibility

An executable bundle must:
- apply deterministically to the exact source version;
- produce deterministic output;
- store enough information to restore the original source exactly.

Reversibility does not imply correctness or safety.

## 13. Bundle execution

A legal action may include zero or more bundles only when:
- all requires constraints are satisfied;
- no mutual exclusion is violated;
- no source conflict exists;
- protected policy permits execution;
- all selected bundles are executable and reversible.

## 14. Failure accounting

Mandatory statuses:
- OK;
- ALIGNMENT_AMBIGUOUS;
- ALIGNMENT_FAILED;
- TRUNCATED;
- EMPTY_OUTPUT;
- SOURCE_MISMATCH;
- NONREVERSIBLE;
- PROTECTED_BLOCKED;
- EXECUTION_FAILED.

No failed record is removed from later denominators.

## 15. First-cycle constraints

- exactly P1 final pass-2 hypothesis;
- exactly P2 final hypothesis;
- no P1 pass-1 independent candidate;
- no n-best;
- no top-k;
- no third proposer;
- no punctuation proposer.

## 16. Integrity

This contract must be applied before target matching.

Any implementation change that changes bundle construction after feasibility metrics are observed invalidates that protocol version.
