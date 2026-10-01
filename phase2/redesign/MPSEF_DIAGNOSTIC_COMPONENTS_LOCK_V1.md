# MP-SEF DIAGNOSTIC COMPONENTS LOCK V1

Date: 2026-10-01
Status: **PASS / SOURCE-ONLY DIAGNOSTIC EVIDENCE FROZEN**

## Run

- workflow: `.github/workflows/phase2-mpsef-diagnostic-components-v1.yml`
- run: `36807629220`
- conclusion: **SUCCESS**
- head SHA: `c21f38f27897f8501f48a58b55caa863210c9c66`

## Artifact

- artifact id: `11138426729`
- name: `mpsef-diagnostic-components-v1`
- ZIP digest:
  `sha256:e27bee3c9690fb1794b413d8a9ab5d5134f4f3d0cd8da5bc3350e525a9c6e33b`

## Inputs

- P1 proposal SHA256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- P2 proposal SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

## Result

- cases: **1,918**
- diagnostic records: **3,836**
- total frozen diagnostic components: **43,207**
- diagnostic JSONL SHA256:
  `2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e`

Each record contains:
- uid/case/cluster;
- proposer identity;
- source/output hashes;
- frozen source and output strings;
- frozen source-to-output diagnostic components;
- alignment-version identity;
- `diagnostic_only=true`;
- `executable=false`.

## Integrity

- gold/reference consulted: **false**
- executable actions created by this artifact: **false**
- R_raw computed: **false**
- R_joint computed: **false**

## Purpose

This artifact is the only frozen diagnostic component evidence intended for future R_raw accounting.

It must never:
- add an action to A_primary;
- override the source-only legalizer;
- repair a blocked hypothesis;
- change a target denominator;
- feed gold information back into action construction.

R_raw implementation remains pending and must be validated before measurement.
