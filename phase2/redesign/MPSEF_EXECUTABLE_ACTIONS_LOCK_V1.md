# MP-SEF EXECUTABLE ACTIONS LEGALIZER LOCK V1

Date: 2026-10-01
Status: FROZEN SOURCE-ONLY LEGALITY EVIDENCE

## Governing population

- C_F cases: 1,918
- C_F clusters: 764
- hypothesis records: 3,836
- primary action sets: 1,918

## Frozen upstream identities

- source manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- P1 proposal SHA256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- P2 proposal SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

## Legalizer execution

Workflow run:
`36818173661`

Result:
- P1_OK = 1,806
- P1_PROTECTED_BLOCKED = 112
- P2_EXECUTION_FAILED = 1,918

No gold/reference content was consulted.
No R_joint was computed.
No selector was trained.
INTERNAL/STRESS/reserved data remained closed.

## Frozen output identities

- hypotheses SHA256:
  `a54c1bcd38c9d34d389054cb125878be92bc9e603f062621e6d44a627037dc4f`
- action sets SHA256:
  `6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`

## Interpretation

P2 is excluded from executable primary actions in this cycle because the frozen proposer provenance contains a GED word-label alignment defect in 1,918/1,918 cases.

This is a source-only legality determination, not a linguistic-quality result.

P1 retains 1,806 executable whole-hypothesis actions and 112 protected-blocked hypotheses.

## Freeze rule

These legalizer artifacts are immutable inputs for the corrected scorer/preflight cycle.

They MUST NOT be regenerated, edited, or relaxed after any gold-aware result is observed.

Any future methodological revision must create a new explicitly versioned cycle rather than overwrite this lock.
