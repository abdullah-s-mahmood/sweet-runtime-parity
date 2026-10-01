# MP-SEF P2_V2 STAGE1 GENERATION-CEILING FAILURE TRIAGE V1

Date: 2026-10-01
Stage1 run: `36872617551`
Status: TRIAGED / FAIL-CLOSED / CURRENT V1 UNCHANGED

## Affected row

- UID: `train:12118`
- case_id: `M2H-CAL-03405`
- cluster_id: `cc8601bd66ba1a807a4b9c86e0a30cda0fbf14ad12d898b296cb9f06d5778d89`
- source SHA256: `f3e1d1ebf3b3e1795065558b6f9a0963cbda96c077381e5e9c99c9eda0ff48b5`
- source characters: 343
- source whitespace words: 65
- runtime before fail-closed state: ~6.664 s

Observed terminal state:
`TRUNCATED_OR_LENGTH_UNPROVEN`

Observed reason:
`Stage0Error:GEC_EOS_AT_GENERATION_CEILING_FAIL_CLOSED`

## Root cause

The frozen P2_V2 generation contract uses:
- `max_length = 100`
- explicit terminal-EOS verification
- fail-closed handling when generation reaches the configured ceiling and the first terminal EOS is the final generated token.

For this row, the generated sequence reached the frozen ceiling and terminal EOS occurred at that ceiling boundary.

The implementation therefore refused to treat the output as proven complete.

## Classification

Primary:
`CAPACITY / GENERATION-COMPLETENESS BOUNDARY`

Not:
- GED word-alignment failure;
- morphology identity failure;
- source identity failure;
- tokenizer zero-token failure;
- project gold/reference failure;
- linguistic-quality failure.

## Reproducibility

The row was produced by the frozen Stage1 V1 runner under:
- frozen packet SHA:
  `8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1`
- frozen GED weight:
  `23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f`
- frozen GEC weight:
  `5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f`
- frozen generation ceiling:
  `max_length=100`

The row remains present in the Stage1 artifact and contributes no executable P2_V2 action.

## Scope

Observed frequency in Stage1 V1:
- 1 / 128 = 0.78125% non-executable due to generation completeness ceiling.
- 127 / 128 = 99.21875% terminal state OK.

This frequency is a Stage1 engineering observation only and must not be generalized beyond the frozen packet.

## Confidence

Root-cause confidence:
**HIGH**

The explicit failure reason is emitted directly by the frozen terminal-EOS/ceiling contract.

## Repairability

`FIXABLE_NEXT_VERSION_ONLY`

Potential future repairs include:
- a separately preregistered higher generation ceiling;
- source-length-aware generation budget frozen before execution;
- another explicitly validated long-input generation policy.

Forbidden in Stage1 V1:
- changing max_length after observing this case;
- rerunning this row with a larger ceiling and replacing the V1 failure;
- accepting the ceiling output as complete;
- silently dropping the row.

## Safe next action

Preserve the V1 failure exactly as observed.

Continue source-only architecture work with this P2_V2 row marked non-executable.

If a future P2_V3 or P2_V2.2 long-input policy is investigated, it must:
1. receive a new version;
2. freeze the generation-length policy before project-source execution;
3. include synthetic exact-at-ceiling / over-ceiling / natural-EOS tests;
4. rerun source-only parity/provenance gates;
5. never retroactively rewrite this V1 artifact.

## Scientific interpretation

This event slightly reduces P2_V2 engineering coverage on the Stage1 packet but strengthens fail-closed evidence.

It provides no evidence for or against linguistic correction quality.
