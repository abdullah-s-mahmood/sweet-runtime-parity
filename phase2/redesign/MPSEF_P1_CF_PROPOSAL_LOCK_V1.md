# MP-SEF P1 C_F PREMEASUREMENT PROPOSAL LOCK V1

Date: 2026-09-30
Branch: `phase2-arabic-eval`

## Status

**PASS / PREMEASUREMENT PROPOSALS FROZEN**

No reference-based feasibility metric was computed.

## Workflow

- workflow: `.github/workflows/phase2-mpsef-p1-cf-proposals-v1.yml`
- run: `36765798233`
- job: `110059516744`
- conclusion: **SUCCESS**
- head SHA: `cc163846e87b5c3e55d290b641f3c1058dfd6aa0`

## Artifact

- artifact id: `11123050529`
- artifact name: `mpsef-p1-cf-proposals-v1`
- ZIP digest: `sha256:e4020418ca2f2793d4bb79bc766e26838398fb9affba6d0f1c704255cd5aed46`

## Frozen C_F source manifest

- records: **1,918**
- clusters: **764**
- manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- protected detector: `MPSEF_PROTECTED_DETECTOR_V1`
- reference content used: **false**
- gold edit content used: **false**

## P1 proposal result

- proposal type: `P1_FINAL_WHOLE_HYPOTHESIS`
- cases: **1,918 / 1,918**
- clusters: **764**
- batch size: **32**
- batch-vs-single parity preflight: **64 / 64**
- changed vs source: **1,838 / 1,918 = 95.83%**
- protected-touch proposals: **19 / 1,918 = 0.99%**
- empty outputs: **0**
- proposal JSONL SHA256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`

Changed-vs-source is candidate activity only and is NOT a quality or recall metric.

## Runtime identity

- P1 model revision:
  `21286e56ce98a86362db540863f91c083b8970f9`
- P1 weight SHA256:
  `9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d`
- upstream text-editing revision:
  `4d552ca3ae98029550f27fc52aa1b22883e16e61`

## Frozen implementation hashes

- C_F source manifest builder:
  `0cf1fde15428ad602c883dc0700f10c2ead4502db422b55fe24545fe39369fd2`
- P1 C_F proposal runner:
  `accd5bf9ab46e15905ac07a23d5ee800eb342decf254a9ce15f7a012ed8806e9`
- P1 C_F workflow:
  `4db4809c646c42900ec32e7c84edb0cd1f65e3a76890433438464e9ce0b53e9d`
- source manifest summary:
  `14f29ccfc5fbb54c4153595d144aa0f86c0696f4683eb2c6c7e25b77969075b2`
- proposal summary:
  `48caf5081c0838abd84231c46661882f9d3f8fd3a56f471bd1b60753faf81507`
- pip freeze:
  `aa9c31581f733395b1da19244c9971818499dd1d5bd1d3da0b2057b91fe66df4`

## Integrity

- gold/reference consulted by proposer: **false**
- R_joint computed: **false**
- selector trained: **false**
- INTERNAL_EVALUATION opened: **false**
- STRESS_DIAGNOSTIC opened: **false**
- reserved data opened: **false**

## Interpretation

Relative to the foundational preflight checkpoint:

**IMPROVED IMPLEMENTATION READINESS / PERFORMANCE STILL UNMEASURED**

The P1 source-only proposal layer is now frozen. Protected-touch hypotheses remain recorded but are not automatically executable.

Next authorized step:
build and freeze P2 C_F source-only proposals using the exact same frozen C_F source manifest.
