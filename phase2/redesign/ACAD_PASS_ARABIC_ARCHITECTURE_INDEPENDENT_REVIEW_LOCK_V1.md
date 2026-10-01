# ACAD_PASS ARABIC ARCHITECTURE INDEPENDENT REVIEW LOCK V1

Date: 2026-10-01
Status: FROZEN EXTERNAL REVIEW EVIDENCE
Verdict: MODIFY BEFORE IMPLEMENTATION

## Uploaded review identities

- ARABIC_ARCHITECTURE_REVIEW.md
  SHA256: fd66165131b6cd597c1d864f5d7d85f8c17a3dac9b273e37f89909995a635457
  lines: 388

- ACAD_PASS_ARABIC_ARCHITECTURE_REVIEW_2026-10-01.zip
  SHA256: c9393fb260ef7e27d9fa7b2d7edb908240332f44d3e9798c9a742a24d443e9ab

- START_HERE.md
  SHA256: df08fd84747afc028cfe237c502428dea447c15580093905032a60d4f251c980
  lines: 38

## Review scope

Architecture snapshot reviewed:
`5e0ad432b513bd65daa567cdc2e046c9d18996dd`

The review read the later review package from:
`ae6aaa4d9afa709127608adb622ed9ff6089cce8`

No model run, project scorer population run, R_joint computation, reserved-set opening, or new project-gold measurement was performed by the reviewer.

## Findings

- BLOCKER: 2
- MAJOR: 5
- MINOR: 2
- required questions answered: 30
- synthetic findings reproduced: 6
- final verdict: MODIFY BEFORE IMPLEMENTATION

### BLOCKER B01
P2_V2 needs a stricter executable identity/alignment contract:
- explicit UID -> morphology word -> source span -> segment -> first wordpiece mapping;
- one-to-one coverage, no loss/duplication/reordering;
- reject zero-token words;
- reject a word that alone exceeds the actual segment budget;
- freeze label maps, special-token semantics and effective generation configuration;
- prove the loaded model actually consumes GED tags.

### BLOCKER B02
A new proposer/action-set registry contract is required before connecting P2_V2/P3 to V3-era tooling:
- new proposer IDs/versions/families/ancestry;
- parent-output hashes for cascades;
- new artifact names/hashes;
- failure-state schema;
- literal whole-output dedup preserving all provenance;
- KEEP always present;
- action capacity defined as 1 + authorized proposer count before dedup;
- no reuse of V3 measurement guard/experiment authorization.

### MAJOR findings

M01 — P3 must be optional punctuation/full-correction extension from P1 family, never counted as independent support.

M02 — diversity metrics need executable definitions, denominators, packet size/selection, resource budget and retention procedure before Stage 1/2.

M03 — current protection linkage has a global-word-ordinal guard that can block distant edits; investigate source-only with shadow policy, never retroactively rescue V3.

M04 — scorer all-actions-fail case can collapse unknown upper bound to zero; frozen target count must be passed independently and failure must preserve [0,N] or invalidate judgment.

M05 — BOUNDARY aggregation can sum separate SPLIT/MERGE maxima from different whole actions; group-level metric must maximize one whole action over SPLIT∪MERGE when used as a group gate.

## Governing consequence

No Stage 1 project-source packet, Stage 2 full C_F source-only run, V4 consensus generation, new R_joint, or gold-aware measurement may proceed until the required predecessor fixes are completed according to the review sequence.

V3 historical artifacts remain immutable.

## Exact remediation order

1. Close B01 and B02 in new source-only contracts.
2. Close M01 and M02 before Stage 1 packet execution.
3. Add M03 shadow diagnostics before interpreting Stage 2 diversity.
4. Run Stage 0 synthetic implementation only after B01/B02/M01/M02 design freeze.
5. Run Stage 1 only after Stage 0 PASS.
6. Before any future gold-aware measurement, close M04/M05 and version scorer/guard/experiment anew.
