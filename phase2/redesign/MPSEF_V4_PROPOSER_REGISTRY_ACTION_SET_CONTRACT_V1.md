# MP-SEF V4 PROPOSER REGISTRY AND ACTION-SET CONTRACT V1

Date: 2026-10-01
Status: FROZEN PRE-IMPLEMENTATION SOURCE-ONLY CONTRACT
Closes: Independent Review BLOCKER B02
Gold/reference use: FORBIDDEN
Supersedes: no V3 artifact; V3 remains immutable historical control

## 1. Purpose

The redesigned proposer lane introduces P2_V2 and P3_V1 in addition to frozen P1.

Existing V3 legalizer/scorer/guard assumptions are hard-coded around:
- KEEP;
- P1_FINAL;
- P2_FINAL;
- at most three actions.

Those assumptions MUST NOT be reused for the redesigned proposer set.

This contract defines a new source-only proposer registry and action-set interface.

## 2. New architecture identity

Architecture family:
`MPSEF_V4_CANDIDATE_REGISTRY_V1`

This is a NEW versioned design lane.

It MUST NOT:
- overwrite V3 artifacts;
- reuse V3 experiment IDs;
- reuse V3 authorization records;
- reuse V3 action-set hashes as if they represented the new population;
- silently map P2_V2 or P3_V1 into old P1/P2 identifiers.

## 3. Proposer registry

Each authorized proposer receives a unique immutable registry entry.

Required fields:

```json
{
  "proposer_id": "P2_V2_SEQ2SEQ_GED",
  "proposer_version": "1",
  "family_id": "SEQ2SEQ_GED",
  "architecture_class": "AUTOREGRESSIVE_SEQ2SEQ_WITH_GED",
  "ancestry": [],
  "parent_proposer_id": null,
  "parent_output_required": false,
  "source_input": "ORIGINAL_SOURCE",
  "whole_output_only": true,
  "source_only_stage": true,
  "model_revision": "...",
  "tokenizer_revision": "...",
  "runtime_lock_sha256": "...",
  "implementation_sha256": "...",
  "enabled_for_stage": "STAGE0|STAGE1|STAGE2",
  "gold_reference_consulted": false
}
```

## 4. Frozen initial registry roles

### P1_CONTROL

- proposer_id: `P1_CONTROL_SWEET_NOPNX_ITER2`
- family_id: `SWEET_NOPNX`
- ancestry: none
- source input: original source
- role: frozen control
- output identity must match frozen P1 artifact where compared

### P2_V2

- proposer_id: `P2_V2_SEQ2SEQ_GED`
- family_id: `SEQ2SEQ_GED`
- ancestry: none
- source input: original source
- role: heterogeneous repaired candidate generator

### P3_V1

- proposer_id: `P3_V1_SWEET_NOPNX2_PNX1`
- family_id: `SWEET_NOPNX_PNX_CASCADE`
- ancestry: [P1_CONTROL_SWEET_NOPNX_ITER2]
- parent_proposer_id: P1_CONTROL_SWEET_NOPNX_ITER2
- parent_output_required: true
- source input: exact P1 parent output
- role: optional punctuation/full-correction extension

P1 and P3 are RELATED/CASCADE, not independent evidence families.

## 5. Parent-output identity for cascades

For every P3 row record:

- parent_proposer_id;
- parent_proposer_version;
- parent_uid;
- parent_source_sha256;
- parent_output_sha256;
- P3 input_sha256;
- equality proof:
  `P3_input_sha256 == parent_output_sha256`

If not equal:
`EXECUTION_FAILED:P3_PARENT_OUTPUT_IDENTITY_MISMATCH`

No regenerated approximation of the parent output is accepted unless a separately frozen parity contract explicitly authorizes it.

## 6. Proposal record schema

Every proposer row must include:

- registry_schema_version;
- proposer_id;
- proposer_version;
- family_id;
- ancestry;
- uid;
- case_id;
- cluster_id;
- source;
- source_sha256;
- input_text;
- input_sha256;
- parent_output_sha256 if applicable;
- full_proposer_output;
- output_sha256;
- execution_state;
- failure_reasons[];
- protected_touch;
- protection_reasons[];
- provenance_complete;
- runtime_identity;
- source_only=true;
- gold_reference_consulted=false;
- quality_scored=false.

Failure rows MUST remain present.

## 7. Execution-state schema

Common terminal states:

- OK
- SOURCE_IDENTITY_FAILED
- INPUT_IDENTITY_FAILED
- EMPTY_OUTPUT
- EXECUTION_FAILED
- TOKENIZATION_FAILED
- ALIGNMENT_FAILED
- TRUNCATED
- GENERATION_INCOMPLETE
- NONREVERSIBLE
- PROTECTED_BLOCKED
- PROVENANCE_INCOMPLETE
- UNKNOWN

Each state may contain structured subreasons.

UNKNOWN is never executable.

## 8. Action-set construction

For each UID, construct from:

1. KEEP — always present;
2. one whole-output action from every authorized proposer whose terminal state is executable and passes source-only legality/protection;
3. exact textual deduplication.

Before dedup:
`max_raw_action_count = 1 + number_of_authorized_proposers`

No hard-coded limit of 3 actions is permitted.

After dedup:
- retain one canonical output action;
- preserve ALL contributing proposer IDs, versions, families, ancestry, and output hashes in provenance.

## 9. Literal deduplication only

Dedup identity is exact full output bytes/text as executed.

Forbidden for dedup:
- whitespace normalization;
- punctuation stripping;
- Unicode normalization not already part of the proposer output contract;
- case folding;
- diacritic removal;
- token-level approximate matching.

If two proposers emit byte-identical/full-string-identical output, they collapse to one action with multi-provenance.

## 10. KEEP invariance

KEEP is always present even if:
- all proposers fail;
- all proposer outputs duplicate KEEP;
- all non-KEEP actions are protected-blocked.

KEEP provenance is system-generated and separate from proposer provenance.

## 11. Action identity

Each canonical action ID must be derived from:

- registry version;
- UID;
- source SHA256;
- exact output SHA256;
- sorted contributing proposer IDs/versions.

Example logical identity:

`sha256(registry_version || uid || source_sha || output_sha || sorted_provenance)`

Changing provenance while output text is identical MUST change the canonical action identity or preserve a separate provenance hash.

## 12. Source-only legality interface

The new registry/action builder consumes only:
- source;
- protected spans derived from source/document structure;
- proposer outputs;
- proposer traces/provenance;
- frozen source-only policies.

It MUST NOT receive:
- gold/reference correction;
- target family labels derived from gold;
- scorer output;
- correctness score;
- previous gold-aware metric.

No callback from scorer into proposer/action construction is allowed.

## 13. New artifact names

The redesigned lane must use NEW artifact names, for example:

- `MPSEF_V4_PROPOSER_REGISTRY_V1.json`
- `MPSEF_V4_PROPOSER_ROWS_V1.jsonl`
- `MPSEF_V4_ACTION_SETS_V1.jsonl`
- `MPSEF_V4_ACTION_SETS_V1_SUMMARY.json`
- `MPSEF_V4_ACTION_SETS_V1_SHA256.txt`

Do not reuse:
- `MPSEF_EXECUTABLE_ACTIONS_V1_*`
- V3 scorer artifact names;
- V3 experiment IDs.

## 14. New experiment identity later

Any future gold-aware evaluation of this redesigned candidate set MUST receive:

- a new experiment_id;
- new source-only artifact hashes;
- new scorer/guard version hashes;
- new preflight;
- new independent review;
- new one-shot authorization.

The V3 experiment guard is historical evidence only.

## 15. Registry freeze timing

Before Stage 1:

Freeze:
- registry schema;
- proposer IDs;
- versions;
- family/ancestry labels;
- parent-input rule;
- action-set schema;
- dedup rule;
- terminal-state schema.

Model weights and runtime hashes may be populated as implementations are frozen, but field presence and semantics are fixed now.

No proposer may appear in Stage 1 if it was not registered before the packet run.

## 16. Adding or removing proposers

Adding a proposer after Stage 1 requires:
- registry version increment;
- new Stage 1 packet run or explicit source-only compatibility review.

Removing a proposer after observing source-only results is allowed only under the frozen retention procedure and must be recorded.

Any removal based on correctness/gold requires a gold-aware protocol and is outside this contract.

## 17. Stage 1 packet registry snapshot

Every Stage 1 artifact must embed:

- registry_version;
- registry SHA256;
- authorized proposer roster;
- family map;
- ancestry map;
- source manifest SHA256;
- packet UID list SHA256.

This prevents interpreting outputs under a different proposer roster later.

## 18. Scorer compatibility boundary

No existing V3 scorer is automatically compatible with V4 action sets.

Before any future measurement:
- scorer input schema must explicitly accept variable action counts;
- whole-action semantics must remain preserved;
- denominator construction must remain candidate-independent;
- M04/M05 must be fixed;
- scorer gets a new version and preflight.

No gold-aware scorer work is required to begin Stage 0/Stage 1 source-only engineering.

## 19. Guard compatibility boundary

V3 guard and authorization:
NOT VALID for V4.

A future V4 guard must bind:
- new registry hash;
- new proposer artifact hashes;
- new action-set hash;
- new scorer hash;
- new contracts;
- new preflight;
- new review;
- new experiment ID.

## 20. Required B02 synthetic tests

S-B02-01 KEEP only when all proposers fail.
S-B02-02 KEEP + one proposer.
S-B02-03 KEEP + P1 + P2_V2 + P3_V1 gives raw max 4 actions.
S-B02-04 P1 and P3 exact same output dedup to one output with both provenances.
S-B02-05 proposer output equal KEEP dedup preserves proposer provenance without removing KEEP semantics.
S-B02-06 two identical texts with different ancestry preserve multi-provenance.
S-B02-07 whitespace-only different outputs do NOT dedup unless bytes/text are exactly equal.
S-B02-08 missing parent_output_sha for P3 -> FAIL.
S-B02-09 P3 input hash != P1 parent output hash -> FAIL.
S-B02-10 unregistered proposer row -> FAIL.
S-B02-11 duplicate proposer_id/version in registry -> FAIL.
S-B02-12 unknown terminal state -> FAIL.
S-B02-13 failure row remains in proposer artifact but contributes no executable action.
S-B02-14 action identity changes when provenance set changes.
S-B02-15 V3 experiment/guard ID supplied to V4 builder -> explicit rejection.

## 21. B02 closure condition

B02 is CLOSED only when:

- this contract is frozen;
- registry/action builder implementation exists under new versioned paths;
- mandatory synthetic tests PASS;
- no V3 artifact is overwritten;
- Stage 1 packet binds the exact registry snapshot.

Until then:
- synthetic implementation is allowed;
- Stage 1 project-source execution is forbidden.

## 22. Scientific boundary

This registry does not rank proposer quality.

It does not prove:
- correctness;
- complementarity;
- independence;
- recall;
- R_joint;
- safe repair.

It only establishes identity, provenance, action-set completeness, and clean version separation.
