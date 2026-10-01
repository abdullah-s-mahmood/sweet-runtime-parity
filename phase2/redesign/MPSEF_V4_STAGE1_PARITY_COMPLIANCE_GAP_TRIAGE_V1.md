# MP-SEF V4 STAGE1 PARITY PROTOCOL-COMPLIANCE GAP TRIAGE V1

Date: 2026-10-01
Status: OPEN / SOURCE-ONLY REMEDIATION REQUIRED BEFORE STAGE2
Gold/reference impact: NONE

## 1. Discovery

During the post-Stage1 review, the frozen diversity protocol was re-read against the executed proposer workflows.

The protocol requires a preregistered Stage1 parity subset of:

`32 UIDs`

selected as the lowest SHA256 ranks under:

`MPSEF-V4-STAGE1-PARITY-32-20261001-A|uid`

For those 32, the protocol requires the applicable combination of:
- single;
- batch;
- reordered batch/order;
- repeat.

## 2. Executed evidence

P2_V2 Stage1:
- parity subset used: 8
- selection: first 8 UIDs of the frozen UID-sorted packet
- repeat: 8/8
- reversed-order single-case execution: 8/8
- true batch model-call: not implemented / N/A under the separately frozen applicability note.

P3_V1 Stage1:
- parity subset used: 8
- batch-vs-single: 8/8
- no protocol-compliant 32-UID reordered-batch + repeat evidence was frozen.

P1 historical C_F:
- batch-vs-single parity: 64/64
- historical selection salt differs from the Stage1 protocol salt
- therefore it does not satisfy the exact Stage1 32-UID parity packet requirement.

## 3. Classification

Primary:
`PROTOCOL-COMPLIANCE / PARITY-SUBSET MISMATCH`

Not:
- model quality failure;
- proposal-output corruption;
- source identity failure;
- legalizer failure;
- gold/reference exposure;
- diversity-analysis correctness failure.

## 4. Scope

The already frozen proposal outputs remain immutable:
- P1 frozen C_F artifact;
- P2_V2 Stage1 proposal artifact;
- P3_V1 Stage1 proposal artifact.

The Stage1 legality/dedup/diversity artifact is preserved as provisional source-only evidence.

Stage1 CANNOT yet be declared fully protocol-complete.

Stage2 is blocked until remediation PASS.

## 5. Root cause

The proposer runners implemented useful parity checks before execution, but used a local `PARITY_N=8` shortcut and did not bind selection to the explicit 32-UID hash rule already frozen in the diversity protocol.

This was an implementation/governance miss.

## 6. Reproducibility

The mismatch is directly reproducible from:
- `MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V2.md`;
- `mpsef_p2_v2_stage1_v1.py`;
- `mpsef_p3_v1_stage1_v1.py`;
- historical `mpsef_p1_cf_proposals_v1.py`.

## 7. Confidence

Root-cause confidence:
**HIGH**

## 8. Repairability

`FIXABLE_SOURCE_ONLY_WITHOUT_REGENERATING_PROPOSALS`

No proposer proposal artifact needs replacement.

Required remediation:
1. materialize the exact deterministic 32-UID parity manifest from the frozen 128-UID Stage1 packet using the already-preregistered salt;
2. P1: on those 32, prove single == batch == reordered batch == repeat == frozen P1 output;
3. P2_V2: on those 32, prove repeat and reordered single-case trace/output identity; true model-call batch remains explicitly N/A under the frozen applicability note;
4. P3: on those 32, prove single == batch == reordered batch == repeat and exact parent identity;
5. freeze parity artifacts/hashes;
6. rerun no proposal generation and change no existing Stage1 proposal artifact.

## 9. Stage2 gate

Stage2 remains forbidden until all three parity remediation tracks PASS.

No gold/reference is required.
