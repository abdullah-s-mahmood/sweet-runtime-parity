# MP-SEF V4 CANDIDATE REGISTRY AND ACTION-SET CONTRACT V2 — CANONICAL

Date: 2026-10-01
Status: FROZEN / CANONICAL PRE-STAGE1 SOURCE-ONLY CONTRACT
Closes: Independent Review BLOCKER B02
Gold/reference use: FORBIDDEN
V3 status: IMMUTABLE HISTORICAL CONTROL

Supersedes for future execution:
- `MPSEF_V4_CANDIDATE_REGISTRY_ACTIONSET_CONTRACT_V1.md`
- `MPSEF_V4_PROPOSER_REGISTRY_ACTION_SET_CONTRACT_V1.md`

The V1 files remain historical evidence and are not deleted.

## 1. Namespace

Registry namespace:
`MPSEF-V4-CANDIDATE-REGISTRY-20261001-A`

Action-set record:
`MPSEF_V4_SOURCE_ONLY_ACTION_SET_V2`

No V3 experiment ID, guard, consumed-status context, action-set hash, authorization, or artifact name may be reused as V4 authorization.

## 2. Canonical proposer roster identities

### P1_CONTROL

- proposer_id: `P1_CONTROL_SWEET_QALB14_NOPNX_ITER2`
- proposer_version: `P1_FROZEN_V1`
- family_id: `SWEET_QALB14`
- ancestry_id: `SWEET_NOPNX_ITER2`
- role: `FROZEN_CONTROL`
- source input: ORIGINAL_SOURCE
- parent: none

### P2_V2

- proposer_id: `P2_V2_ARABART_GED_MORPH_WORDALIGNED`
- proposer_version: `P2_V2_1`
- family_id: `SEQ2SEQ_GED_MORPH`
- ancestry_id: `ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR`
- role: `HETEROGENEOUS_CANDIDATE`
- source input: ORIGINAL_SOURCE
- parent: none

### P3_V1

- proposer_id: `P3_V1_SWEET_NOPNX2_PNX1`
- proposer_version: `P3_V1_1`
- family_id: `SWEET_QALB14`
- ancestry_id: `P1_CONTROL_PLUS_PNX1`
- role: `OPTIONAL_PUNCTUATION_FULLCORRECTION_EXTENSION`
- source input: EXACT_P1_PARENT_OUTPUT
- parent: `P1_CONTROL_SWEET_QALB14_NOPNX_ITER2`

P1 and P3 are one architecture family for any future support-count interpretation.

## 3. Registry schema

Every proposer registry entry MUST contain:

- registry_namespace;
- registry_schema_version;
- proposer_id;
- proposer_version;
- family_id;
- ancestry_id;
- role;
- parent_proposer_id;
- parent_proposer_version;
- source_input;
- implementation_sha256;
- workflow_sha256;
- runtime_lock_sha256;
- model_identities;
- tokenizer_identities;
- source_only=true;
- gold_reference_allowed=false;
- enabled_stage;
- status.

Allowed status:
- DESIGN_FROZEN
- SYNTHETIC_PASS
- STAGE1_AUTHORIZED
- STAGE1_FROZEN
- STAGE2_AUTHORIZED
- STAGE2_FROZEN
- RETIRED

Unknown proposer fields require a schema-version increment if they alter semantics.

## 4. Proposal row schema

Every UID/proposer row MUST contain:

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
- input_text;
- input_sha256;
- parent_proposer_id if applicable;
- parent_proposer_version if applicable;
- parent_output_sha256 if applicable;
- full_proposer_output;
- output_sha256;
- execution_state;
- failure_reasons[];
- protected_touch;
- protection_reasons[];
- provenance_complete;
- trace artifact/hash;
- runtime_identity;
- source_only=true;
- gold_reference_consulted=false;
- quality_scored=false.

No row may be silently dropped.

## 5. Parent identity

P3 MUST prove:

- same UID;
- same source SHA;
- exact parent proposer/version;
- parent_output_sha256 exists;
- `P3_input_sha256 == P1_parent_output_sha256`.

Failure:
`P3_PARENT_OUTPUT_IDENTITY_MISMATCH`

Preferred design:
reuse the exact registered P1 output rather than rerun P1.

If rerun is unavoidable:
- parity must be separately demonstrated;
- packet parity must not be described as proof of full-population identity.

## 6. Terminal execution states

Common states:

- OK
- SOURCE_IDENTITY_MISMATCH
- INPUT_IDENTITY_FAILED
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
- UNKNOWN_FAILURE

UNKNOWN_FAILURE is fail-closed and non-executable.

Proposer-specific subreasons remain mandatory.

## 7. Action-set rule

Every UID starts with KEEP.

Before dedup:
`max_raw_action_count = 1 + N_authorized_proposers`

There is no fixed V3 limit of 3.

Only complete legal whole outputs may enter the action set.

No partial salvage of illegal outputs.

## 8. KEEP invariant

Exactly one KEEP semantic action is always present.

If proposer output equals source exactly:
- exact output may dedup with KEEP-equivalent text;
- KEEP semantics remain explicitly preserved;
- proposer provenance is retained.

KEEP can never disappear because of proposer duplication.

## 9. Literal dedup only

Equality is exact final output string equality.

Forbidden dedup normalization:
- whitespace normalization;
- Unicode normalization not already part of proposer contract;
- punctuation removal;
- Arabic-letter normalization;
- case folding;
- diacritic removal;
- approximate token matching.

On exact duplicate:
- one output action;
- preserve ALL proposer IDs/versions;
- preserve all family/ancestry metadata;
- preserve parent lineage;
- do not create extra support votes from duplicate text.

## 10. Action identity

Canonical action identity binds:

- registry namespace/version;
- UID;
- source SHA;
- exact output SHA;
- sorted proposer/version provenance.

Provenance changes must be detectable even if output text is unchanged.

## 11. Source identity

Every proposal/action binds:
- UID;
- case_id;
- cluster_id;
- source SHA;
- source identity version.

Mismatch is explicit:
`SOURCE_IDENTITY_MISMATCH`

No repair, normalization, or silent rebinding.

## 12. Legalizer boundary

The V4 source-only legalizer adapter MUST:

- consume generic registry proposal records;
- support variable proposer count;
- fail closed;
- preserve failure rows;
- never consult gold/reference;
- never infer proposer identity from filenames;
- never salvage fragments from an illegal whole output;
- never mutate frozen proposal artifacts.

Historical V3 legalizer remains unchanged.

## 13. Stage immutability

Before each stage freeze:
- registry version;
- proposer roster;
- model/tokenizer/runtime identities;
- source manifest/packet identity.

During a stage:
- no proposer addition/removal;
- no version substitution;
- no policy change.

Roster change requires a new registry/stage version.

## 14. Artifact namespace

Minimum canonical names:

- `MPSEF_V4_PROPOSER_REGISTRY_V2.json`
- `MPSEF_V4_STAGE0_*.json`
- `MPSEF_V4_STAGE1_PROPOSER_ROWS_V2.jsonl`
- `MPSEF_V4_STAGE1_SOURCE_ONLY_ACTION_SETS_V2.jsonl`
- `MPSEF_V4_STAGE1_SUMMARY_V2.json`
- analogous STAGE2 names only if later authorized.

Never overwrite V3 artifact names.

## 15. Future scorer boundary

No V3 scorer is automatically compatible with V4.

A future V4 scorer MUST:
- accept variable action count;
- preserve whole-action semantics;
- construct denominator independently of candidate success;
- include M04/M05 fixes or later superseding equivalents;
- consume frozen action sets only;
- never legalize from gold.

A new scorer version is mandatory before gold-aware V4 evaluation.

## 16. Future guard boundary

Any future V4 gold-aware experiment requires:

- new experiment_id;
- new consumed-status context;
- new source-only artifact hashes;
- registry hash;
- proposer hashes;
- action-set hash;
- scorer hash;
- contract hashes;
- new preflight;
- independent review;
- explicit one-shot authorization.

V3 authorization state is irrelevant to V4 authorization.

## 17. B02 mandatory synthetic tests

- B02-S01 all proposers fail => KEEP only.
- B02-S02 KEEP + one legal proposer.
- B02-S03 KEEP + P1 + P2_V2 + P3 => raw max 4.
- B02-S04 P1/P3 exact duplicate => one output, both provenances.
- B02-S05 proposer==source => KEEP semantics preserved with proposer provenance.
- B02-S06 identical output from different ancestry => multi-provenance preserved.
- B02-S07 whitespace-different outputs do not dedup.
- B02-S08 missing P3 parent hash => fail.
- B02-S09 P3 input hash != P1 parent output hash => fail.
- B02-S10 unregistered proposer => fail.
- B02-S11 duplicate proposer ID/version => fail.
- B02-S12 unknown execution state => fail.
- B02-S13 failure row retained but contributes no action.
- B02-S14 action/provenance identity changes when provenance changes.
- B02-S15 V3 experiment/guard identity presented to V4 builder => explicit rejection.
- B02-S16 registry SHA mismatch between packet and action builder => fail.
- B02-S17 proposer roster differs from frozen stage roster => fail.

## 18. Stage 1 prerequisites

Stage 1 forbidden until:

- B01 implementation synthetic PASS;
- B02 builder synthetic PASS;
- M01 P3 role/parent rules synthetic PASS;
- M02 protocol V2 frozen;
- M03 shadow diagnostic design frozen;
- Stage 0 summary PASS;
- deterministic 128-UID/128-cluster packet hashes frozen;
- no gold/reference available to workflow.

## 19. Scientific boundary

This contract establishes:
- identity;
- lineage;
- whole-output action completeness;
- provenance;
- version separation.

It does NOT establish:
- correctness;
- linguistic quality;
- proposer independence;
- recall/precision;
- R_joint;
- consensus validity;
- safe repair.
