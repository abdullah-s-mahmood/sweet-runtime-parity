# MP-SEF STAGE1 EXECUTION APPLICABILITY NOTE V1

Date: 2026-10-01
Status: FROZEN BEFORE P2_V2 STAGE1 OUTPUT
Applies to: MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V2

## P2_V2 batching applicability

The frozen P2_V2 implementation validated in Stage0 performs model inference as a single-source model-call path.

No independently implemented true batched P2_V2 model-call path exists in the frozen runner at the time of Stage1 authorization.

Therefore:

- repeat parity: REQUIRED;
- packet-order/reversed-order parity on the fixed parity subset: REQUIRED;
- true batch-vs-single parity for P2_V2: `NOT_APPLICABLE_SINGLE_CASE_MODEL_CALL_IMPLEMENTATION`.

This MUST NOT be reported as PASS.

If a true batched P2_V2 implementation is introduced later:
- increment the runner version;
- freeze its batching semantics;
- perform exact batch-vs-single parity before using batched outputs;
- do not silently substitute the new batched path into Stage1 V1.

For proposers that do implement a true batch model-call path (e.g. existing P1 frozen runner), batch-vs-single parity remains required.

This note was frozen before P2_V2 Stage1 project-source outputs were produced and does not depend on proposer quality or diversity.
