# MP-SEF SCORER V2 SYNTHETIC PREFLIGHT LOCK

Date: 2026-10-01
Status: **PASS / SYNTHETIC-ONLY SCORER PREFLIGHT FROZEN**

## Run

- workflow: `.github/workflows/phase2-mpsef-scorer-v2-synthetic-preflight.yml`
- run: `36808060412`
- conclusion: **SUCCESS**
- head SHA: `d2f29d0735452e31bd4f039141d61e05500d5709`

## Artifact

- artifact id: `11138334064`
- name: `mpsef-scorer-v2-synthetic-preflight`
- ZIP digest:
  `sha256:75cf7c16140b97be7fba8720a789e91d60cfbfcef4be80d77c7069b00f83828b`

## Frozen implementation identities

- `mpsef_rjoint_core_v2.py` SHA256:
  `2f86146e5485cf79da5a3db44b9f8c86ee2b7ea60bac5859ff9a079fe66d3588`
- `mpsef_rjoint_score_v2.py` SHA256:
  `5fdcf0653cd0fafd3195444b926c19d8ab0fdef18dea8c728af1ca171821e2da`

## Frozen source-only evidence identities

- executable action sets:
  `6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`
- hypothesis states:
  `c91195a66a687ba8acf12d1b1e51741183b28992f89681c8510cdac8fddf9e14`
- diagnostic components:
  `2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e`

## Synthetic checks passed

- corrected punctuation/linguistic target-scope tests;
- mixed punctuation + SPLIT preservation;
- whole-action oracle does not union P1/P2 target hits;
- scorer exception produces a bounded unknown interval rather than known zero;
- source-only legalizer synthetic checks;
- frozen action/diagnostic hashes match;
- project-gold measurement CLI remains deliberately disabled.

Explicit guard result:
`SCORER_V2_PROJECT_MEASUREMENT_DISABLED_OK`

## Integrity

- project gold loaded: **false**
- project metric computed: **false**
- R_joint computed: **false**
- project measurement CLI enabled: **false**

## Interpretation

**IMPROVED SCORER CONTRACT COMPLIANCE / PERFORMANCE STILL UNMEASURED**

This lock does NOT authorize measurement.

Remaining mandatory work includes:
- F08/C21 immutable execution guard;
- exact code/contract/preflight hashes before any reference access;
- consumed-experiment lock;
- second premeasurement checklist implementation;
- independent review of the corrected package before authorization.
