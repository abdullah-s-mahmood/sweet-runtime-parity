# MP-SEF SOURCE-ONLY EXECUTABLE ACTION LEGALIZER LOCK V1R1

Date: 2026-10-01
Status: **PASS / SUPERSEDES V1 LOCK**

## Revision reason

V1R1 adds a frozen all-optimal-alignment work budget and explicit fail-closed
`ALIGNMENT_FAILED` behavior plus additional negative synthetic tests.

No project metric was used.
The executable action space did not change.

## Run

- run: `36808497947`
- conclusion: SUCCESS
- head SHA: `ad482b4688cd3bb8f3986ca74e9dcc4a55d04394`
- artifact id: `11138269108`
- artifact digest:
  `sha256:97f60f7d8147dd8cc5378df94a2b506d790086146395720e631c771d0db4fee1`

## Final states

- P1_OK: 1,806
- P1_PROTECTED_BLOCKED: 112
- P2_EXECUTION_FAILED: 1,918

## Frozen hashes

- legalizer code:
  `f17af03343490f6edba59693babed9ec65c992309eec5a3b32dd68d9b9969686`
- progress helper:
  `01a8dfc044b5ef6ecab000e0d4518b8819d1ad0f1ee76f37062761fe0c72cbb6`
- watchdog:
  `2d808ebf587d8f62e34e24bea63df77450578f14771c76b1e853575482eeaa40`
- hypotheses:
  `b4736383019d017780a8bfe4b076a0cd742e71bccfbb50350da8fa59b7c9ac75`
- executable action sets:
  `6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`
- summary:
  `39c2ba054df0d413166d0dd4bd67563f64012d3b25c0a59d52ce37b1d7ca073e`

## Invariant versus V1

Executable action-set SHA is identical to V1:
`6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`

Thus the hardening changed audit evidence, not action membership.

Gold/reference consulted: false.
R_joint computed: false.
