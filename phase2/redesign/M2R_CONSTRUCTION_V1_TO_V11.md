# M2-R Construction v1 → v1.1

Date: 2026-09-30

## v1 observed result

Data feasibility: PASS.
Packet construction: FAIL with 0 reconstructable ALL_BUT_ONE contexts.

The failure was caused by an invalid assumption: ArabiGEE annotation rows are manually selected error/explanation units linked to sentence contexts, but they are not guaranteed to constitute an exhaustive edit script whose simultaneous replacements reconstruct `target_context`.

The v1 scientific thresholds are not lowered.

## v1.1 redesign

Replace `ALL_BUT_ONE_RESIDUAL` with `EXPERT_REINSERTED_RESIDUAL`.

Construction:
1. start from the expert-corrected `target_context`;
2. select one ArabiGEE human-annotated pair `erroneous_word → target_word`;
3. require `target_word` to occur exactly once in the clean target context;
4. replace that unique `target_word` with the documented `erroneous_word`;
5. verify the erroneous surface occurs in the resulting candidate;
6. record that one pair as the only construction gold residual.

This is a controlled counterfactual, not a naturally produced model error.

Why this is stronger:
- the clean baseline is the expert-corrected target;
- the inserted error is a real documented Arabic error from ArabiGEE, not random corruption;
- there is exactly one known injected residual by construction;
- no assumption is made that ArabiGEE annotations exhaust all source→target differences.

The packet size remains 120 and the 70/15/15 context partition remains unchanged.
