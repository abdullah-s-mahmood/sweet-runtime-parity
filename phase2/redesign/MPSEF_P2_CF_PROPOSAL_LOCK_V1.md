# MP-SEF P2 C_F PREMEASUREMENT PROPOSAL LOCK V1

Date: 2026-09-30
Branch: `phase2-arabic-eval`

## Status

**PASS / PREMEASUREMENT PROPOSALS FROZEN**

No reference-based feasibility metric was computed.

## Workflow

- workflow: `.github/workflows/phase2-mpsef-p2-cf-proposals-v1.yml`
- run: `36768378938`
- job: `110068215284`
- conclusion: **SUCCESS**
- head SHA: `21ffdb50590bd13a5374abd01424ac5f3cf53cba`

## Artifact

- artifact id: `11124303107`
- artifact name: `mpsef-p2-cf-proposals-v1`
- ZIP digest: `sha256:5209633d389db02054456a42710a96a1d6e573cefca308254747897969c7d41c`

## Frozen C_F source manifest identity

P2 consumed the exact same source-only C_F manifest frozen for P1:

- records: **1,918**
- clusters: **764**
- source manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`

No C_F resampling, reconstruction, or role reassignment occurred between P1 and P2.

## P2 proposal result

- proposal type: `P2_FINAL_WHOLE_HYPOTHESIS`
- cases: **1,918 / 1,918**
- clusters: **764**
- batch size: **8**
- batch-vs-single parity preflight: **32 / 32 all-field exact match**
- field parity:
  - morphology text: 32/32
  - GED labels: 32/32
  - subword tokens: 32/32
  - input IDs: 32/32
  - GED label IDs: 32/32
  - generated text: 32/32
- changed vs source: **1,906 / 1,918 = 99.37%**
- protected-touch proposals: **21 / 1,918 = 1.10%**
- empty outputs: **0**
- proposal JSONL SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

Changed-vs-source is candidate activity only and is NOT a quality, recall, or feasibility metric.

## Runtime identity

- GED revision:
  `447179dc63d186e4bff09a993e90e73ad622d571`
- GEC revision:
  `410588a318d988cdcfdbf64cf5745ed4adea0f6a`
- GED weight SHA256:
  `23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f`
- GEC weight SHA256:
  `5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f`
- upstream arabic-gec revision:
  `8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf`

## Frozen implementation hashes

- P2 C_F proposal runner:
  `e4c983f488f0b5e47695c2092c98e0d639b462db628710d6b361b44c366707b0`
- P2 C_F workflow:
  `86514996041925c979804f1b4be6111adde7e860573c4fd192434d883c4b1e43`
- P2 proposal JSONL:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`
- P2 proposal summary:
  `24ee9eb4114ea619aed24557f7408e23850bf332b94aa90538346f6d8177cebc`
- pip freeze:
  `cbd42c8a3296eb59e933b04f83c70f34d78b98160f09a069fea32fcfc142fe38`

## Integrity

- gold/reference consulted by proposer: **false**
- reference content used: **false**
- feasibility metric computed: **false**
- R_joint computed: **false**
- selector trained: **false**
- INTERNAL_EVALUATION opened: **false**
- STRESS_DIAGNOSTIC opened: **false**
- reserved data opened: **false**

## Runtime observation

Step 10 (`Run frozen P2 source-only proposals`) ran from
`2026-09-30T19:52:23Z` until approximately `2026-09-30T20:27:29Z`,
roughly **35 minutes** including preflight and full source-only proposal generation.

The runner emitted batch progress through `1918/1918`.
The apparent lack of progress visible through the ChatGPT GitHub connector
was caused by active-job log blob unavailability (`BlobNotFound`), not by
a stalled inference process.

## Interpretation

Relative to the P1-frozen checkpoint:

**IMPROVED IMPLEMENTATION COMPLETENESS / PERFORMANCE QUALITY STILL UNMEASURED**

Both primary proposers are now source-only, parity-validated, artifact-frozen,
and anchored to the identical C_F source manifest.

P2 is more active than P1 (99.37% vs 95.83% source changes) and has a slightly
higher protected-touch precheck rate (1.10% vs 0.99%). These are operational
signals only, not evidence that P2 is more accurate.

Next authorized sequence:
1. independent premeasurement review package;
2. implement R_joint scorer against frozen proposal artifacts;
3. freeze scorer/workflow hashes;
4. second pre-measurement preflight;
5. explicit measurement authorization decision;
6. only then compute R_joint once.
