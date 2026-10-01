# MP-SEF V4 CANDIDATE REGISTRY AND ACTION-SET CONTRACT V1

Date: 2026-10-01
Status: FROZEN PRE-IMPLEMENTATION SOURCE-ONLY CONTRACT
Closes: Independent Review BLOCKER B02
Scope: New redesign lane only
V3 status: IMMUTABLE HISTORICAL CONTROL
Gold/reference use: FORBIDDEN

## 1. Purpose

P2_V2 and P3_V1 MUST NOT be connected to V3-era action-set/scorer/guard identities.

This contract defines a new versioned proposer registry and whole-output action-set interface for the redesign lane.

It does not authorize measurement.

## 2. Architecture namespace

New architecture namespace:

`MPSEF-V4-CANDIDATE-REGISTRY-20261001-A`

This is a source-only registry namespace, NOT a measurement experiment ID.

No V3 experiment/guard/authorization ID may be reused.

## 3. Registered proposers

### P1_CONTROL

- proposer_id: `P1_CONTROL_SWEET_QALB14_NOPNX_ITER2`
- proposer_version: `P1_FROZEN_V1`
- family_id: `SWEET_QALB14`
- ancestry_id: `SWEET_NOPNX_ITER2`
- role: `FROZEN_CONTROL`
- upstream behavior: frozen current P1
- may be regenerated: NO for historical control evidence
- source-only current frozen artifact may be referenced by hash

### P2_V2

- proposer_id: `P2_V2_ARABART_GED_MORPH_WORDALIGNED`
- proposer_version: `P2_V2_1`
- family_id: `SEQ2SEQ_GED_MORPH`
- ancestry_id: `ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR`
- role: `HETEROGENEOUS_CANDIDATE`
- parent proposer: NONE
- source-only only until later independent authorization

### P3_V1

- proposer_id: `P3_V1_SWEET_NOPNX2_PNX1`
- proposer_version: `P3_V1_1`
- family_id: `SWEET_QALB14`
- ancestry_id: `P1_CONTROL_PLUS_PNX1`
- role: `OPTIONAL_PUNCTUATION_FULLCORRECTION_EXTENSION`
- parent proposer: `P1_CONTROL_SWEET_QALB14_NOPNX_ITER2`
- parent output identity REQUIRED

P1 and P3 share one architecture family for any later support-count interpretation.

## 4. Registry record schema

Every authorized proposer version must have a frozen registry record:

```json
{
  "registry_namespace": "MPSEF-V4-CANDIDATE-REGISTRY-20261001-A",
  "proposer_id": "...",
  "proposer_version": "...",
  "family_id": "...",
  "ancestry_id": "...",
  "role": "...",
  "parent_proposer_id": null,
  "parent_version": null,
  "implementation_sha256": "...",
  "workflow_sha256": "...",
  "runtime_lock_sha256": "...",
  "model_identities": {},
  "tokenizer_identities": {},
  "source_only": true,
  "gold_reference_allowed": false,
  "status": "DESIGN_FROZEN|SYNTHETIC_PASS|STAGE1_AUTHORIZED|STAGE1_FROZEN|STAGE2_AUTHORIZED|STAGE2_FROZEN|RETIRED"
}
```

Unknown fields may be added only by a new schema version.
Required fields may not be omitted.

## 5. Per-UID proposal record

Every proposer output row MUST contain:

- registry_namespace;
- proposer_id;
- proposer_version;
- family_id;
- ancestry_id;
- uid;
- case_id;
- cluster_id;
- source;
- source_sha256;
- source_identity_version;
- parent_proposer_id if any;
- parent_proposer_version if any;
- parent_output_sha256 if any;
- full_proposer_output;
- output_sha256;
- execution_state;
- failure_reasons[];
- source_only=true;
- gold_reference_consulted=false;
- provenance_complete boolean;
- trace artifact reference/hash.

No proposal row is silently dropped.

## 6. Cascaded proposer parent identity

For P3_V1, Stage A must consume a specific P1 output identity.

Required:
- parent proposer ID/version;
- parent output SHA256;
- UID;
- parent source SHA256.

P3 may not claim ancestry from P1 if Stage A was independently rerun and produced a different output unless a new proposer version explicitly records that fact.

Preferred Stage 1 design:
reuse the frozen/reference P1 source-only output artifact when technically valid, rather than unnecessarily regenerate Stage A.

If regeneration is required:
- parity is tested;
- output identity is recorded;
- the record does not imply full-population equality from a packet-only check.

## 7. New action-set namespace

New source-only action-set record:

`MPSEF_V4_SOURCE_ONLY_ACTION_SET_V1`

This is distinct from V3 `MPSEF_EXECUTABLE_ACTIONS_V1_ACTION_SETS`.

V3 action-set files remain immutable.

## 8. Whole-output-only action policy

Each action set begins with KEEP.

Pre-dedup authorized raw actions are:

- KEEP;
- one full legal output from each proposer version explicitly authorized in the registry for the current stage.

If N proposer versions are authorized:

maximum raw action count before dedup:
`1 + N`

No fixed V3 maximum of 3 applies.

No partial salvage from an illegal whole proposer output is permitted in this contract.

## 9. KEEP invariant

Every UID MUST contain exactly one KEEP action before and after dedup.

KEEP output:
the exact original source bytes/string used by the execution layer.

KEEP provenance:
`["KEEP"]`

KEEP may never be removed because it duplicates a proposer.
If a proposer equals source exactly, its provenance is merged into the KEEP-equivalent output record while KEEP remains explicitly represented.

## 10. Literal output deduplication

Dedup equality is EXACT final output string equality as executed.

Forbidden for dedup:
- whitespace normalization;
- Unicode normalization not already part of the proposer output contract;
- punctuation stripping;
- token normalization;
- case folding;
- Arabic letter normalization.

If two proposers emit byte/string-identical final outputs:

- retain one action output;
- retain ALL proposer provenance;
- retain all family/ancestry metadata;
- do not count duplicates as multiple distinct candidate outputs.

Example:

```json
{
  "action_id": "...",
  "output": "...",
  "output_sha256": "...",
  "types": ["P1_CONTROL","P3_V1"],
  "provenance": [
    {"proposer_id":"...","version":"...","family_id":"..."},
    {"proposer_id":"...","version":"...","family_id":"..."}
  ]
}
```

## 11. Source identity

Every action set is bound to:

- uid;
- case_id;
- cluster_id;
- source_sha256;
- source_identity_version.

A proposal whose source identity differs from the action-set source is not deduplicated or repaired.

It is rejected with explicit state:
`SOURCE_IDENTITY_MISMATCH`

## 12. Failure-state schema V1

Common required states:

- OK
- SOURCE_IDENTITY_MISMATCH
- EMPTY_OUTPUT
- EXECUTION_FAILED
- TOKENIZATION_FAILED
- WORD_IDENTITY_FAILED
- TRUNCATED_OR_LENGTH_UNPROVEN
- GENERATION_INCOMPLETE
- ALIGNMENT_FAILED
- ALIGNMENT_AMBIGUOUS
- NONREVERSIBLE
- PROTECTED_BLOCKED
- PROVENANCE_INCOMPLETE
- RUNTIME_IDENTITY_MISMATCH
- MODEL_INTERFACE_UNPROVEN

Proposer-specific subreasons are mandatory where applicable.

Unknown state:
`UNKNOWN_FAILURE`
is fail-closed and non-executable.

## 13. Legalizer interface boundary

A new V4-compatible source-only legalizer adapter/interface must consume generic proposer records via registry metadata.

It MUST NOT:
- hard-code only P1/P2;
- assume max action count 3;
- infer proposer identity from filename;
- consult gold/reference;
- rescue illegal proposer fragments;
- mutate source-only proposer artifacts.

The V3 legalizer remains historical and unchanged.

## 14. Future scorer interface boundary

No V4 scorer is implemented or authorized by this contract.

The future scorer interface must consume:
- frozen source membership;
- frozen registry;
- frozen legal action sets;
- later authorized target/reference data.

It must not construct or legalize candidates from gold.

The existing V3 scorer may not be silently pointed at V4 artifacts.

A new scorer version and experiment ID are required before any gold-aware V4 measurement.

## 15. Guard / experiment isolation

The following V3 elements are NOT authorizations for V4:

- V3 measurement guard;
- V3 experiment ID;
- V3 consumed-status context;
- V3 authorization file;
- V3 source-only action-set hash;
- V3 preflight PASS.

Future V4 measurement requires:
- new experiment ID;
- new frozen implementation hashes;
- new contract hashes;
- new guard version;
- new consumed-status context;
- new independent review;
- new explicit authorization.

## 16. Artifact naming

All redesign artifacts must use new names containing `V4` or explicit proposer versions.

Forbidden:
overwriting any frozen V3 artifact path/name.

Minimum future names:

- `MPSEF_V4_PROPOSER_REGISTRY_V1.json`
- `MPSEF_V4_P2_V2_PROPOSALS_*.jsonl`
- `MPSEF_V4_P3_V1_PROPOSALS_*.jsonl`
- `MPSEF_V4_SOURCE_ONLY_ACTION_SETS_V1.jsonl`
- `MPSEF_V4_SOURCE_ONLY_HYPOTHESES_V1.jsonl`
- `MPSEF_V4_SOURCE_ONLY_SUMMARY_V1.json`

Stage suffixes must distinguish SYNTHETIC / STAGE1 / STAGE2.

## 17. Registry immutability per stage

Before each stage:
- registry version frozen;
- authorized proposer roster frozen;
- model/runtime identities frozen.

During a stage:
- no proposer added/removed;
- no version substituted;
- no action policy changed.

If roster changes:
new stage/version required.

## 18. Stage 1 eligibility

Before Stage 1:

- B01 contract frozen and synthetic closure tests PASS;
- this B02 contract frozen;
- M01 P3 role amendment frozen;
- M02 diversity/packet/budget contract frozen;
- registry file generated from these contracts;
- no project gold/reference available to the workflow.

## 19. Stage 2 eligibility

Before Stage 2:

- Stage 1 artifacts frozen;
- Stage 1 review complete;
- proposer retention/roster decision frozen;
- V4 source-only legalizer integration validated;
- resource budget accepted;
- no gold/reference involved.

## 20. Scientific boundary

This registry/action-set contract governs identity and provenance.

It does not establish:
- linguistic correctness;
- independence of errors;
- model quality;
- consensus validity;
- R_joint;
- safe repair.

No gold/reference is permitted under this contract.
