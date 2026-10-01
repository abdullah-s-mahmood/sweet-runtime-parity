# MP-SEF SCORER V2 SYNTHETIC PREFLIGHT LOCK V1R1

Date: 2026-10-01
Status: **PASS / SUPERSEDES PRIOR SCORER V2 SYNTHETIC PREFLIGHT LOCK**

## Why V1R1 exists

A mandatory pre-authorization legalizer hardening added:
- a frozen all-optimal-alignment work budget;
- explicit ALIGNMENT_FAILED behavior when proof cannot complete;
- additional negative synthetic tests.

This did NOT change the executable action-set SHA or the P1/P2 final state counts.
It DID change the hypothesis-audit artifact SHA because the source-only audit record schema/evidence changed.

No project metric was used in this revision.

## Run

- run: `36808675020`
- conclusion: **SUCCESS**
- head SHA: `3ee8fde3328f65b1364612b73568219f89fb7637`
- artifact id: `11139000492`
- artifact digest:
  `sha256:9a0f5be233ba652f673942ee1dfeb55ade32ea53a908ac239cb2f857b184d8e0`

## Frozen evidence

- executable action sets:
  `6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`
- corrected hypothesis audit:
  `b4736383019d017780a8bfe4b076a0cd742e71bccfbb50350da8fa59b7c9ac75`
- diagnostic components:
  `2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e`

## Implementation

- core v2:
  `2f86146e5485cf79da5a3db44b9f8c86ee2b7ea60bac5859ff9a079fe66d3588`
- scorer v2:
  `5fdcf0653cd0fafd3195444b926c19d8ab0fdef18dea8c728af1ca171821e2da`

## Checks

- legalizer synthetic tests: PASS
- core-v2 synthetic tests: PASS
- scorer-v2 synthetic tests: PASS
- frozen source-only evidence hashes: PASS
- project measurement CLI disabled: PASS

## Integrity

- project gold loaded: false
- project metric computed: false
- R_joint computed: false
- measurement authorized: false

Next:
implement and run Second Premeasurement Preflight v2; a PASS there still must NOT run measurement.
