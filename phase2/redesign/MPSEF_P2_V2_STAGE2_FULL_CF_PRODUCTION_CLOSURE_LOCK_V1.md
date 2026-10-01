# MP-SEF P2_V2 STAGE2 FULL-C_F PRODUCTION CLOSURE LOCK V1

Date: 2026-10-01
Status: PASS / FULL-C_F PRODUCTION COMPLETE
Scientific scope: SOURCE-ONLY EXECUTION EVIDENCE
Linguistic quality: UNMEASURED

## Production run

- workflow run: `36899056538`
- conclusion: **SUCCESS**
- head SHA: `70d887015d9a625dc401ba77b611622fb28344fa`
- artifact id: `11186450279`
- artifact digest: `sha256:c5c5d32c99ce216a5b93362748cfefa67de4ec1f5b2b1174c8d3caf0fcd914af`

## Population accounting

- expected C_F UIDs: **1,918**
- clusters: **764**
- terminal durable records: **1,918 / 1,918**
- COMPLETED: **1,918**
- ABORTED: **0**
- NOT_ATTEMPTED: **0**
- completion_claim_allowed: **true**

## Terminal execution states

- OK: **1,896 / 1,918 = 98.8530%**
- TRUNCATED_OR_LENGTH_UNPROVEN: **22 / 1,918 = 1.1470%**
- failure stage for all 22: **GENERATION**

These 22 rows remain preserved in the denominator and are non-executable unless a later separately authorized contract changes their semantics. They are not silently dropped or repaired.

## Frozen identities

- input C_F manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- output proposal JSONL SHA256:
  `87dd3600293b215172f5a75dc7485915013963aa3e661310ea1adac08b9ddba7`
- GED weight SHA256:
  `23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f`
- GEC weight SHA256:
  `5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f`

## Watchdog / interruption semantics

- Watchdog V2 child return code: **0**
- final processed: **1,918 / 1,918**
- stale termination: **none**
- durable accounting: **COMPLETE**

## Scientific boundary

- gold/reference consulted: **false**
- project gold loaded: **false**
- quality metric computed: **false**
- R_joint computed: **false**
- selector trained: **false**

## Interpretation

**IMPROVED STRONGLY / P2 FULL-C_F EXECUTION CLOSED**

This proves full-population execution integrity, provenance preservation, fail-closed generation handling, and interruption accounting.

It does **not** prove linguistic correctness or superiority.
