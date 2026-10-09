# ACAD_PASS — Federation Adapter Source Preflight Freeze V2

Date: 2026-10-09

State:
`FEDERATION_ADAPTER_SOURCE_PREFLIGHT_PASS`

Canonical run:
`37885471201`

Artifact:
`11596272506`

Digest:
`sha256:a45ad59b89ffcc5e4e3223df5838ddb99191a1733c65a8d91bd90f32c51d8e4a`

Scientific training:
FALSE

Benchmark metrics:
NONE

AD/COVID test labels:
NOT READ

Original EBM expert-test contents:
NOT READ

## Native EBM-NLP_mod

- 400 training documents
- labels restricted to O + B/I for P/I/C/O
- source-compatible B-start semantics preserved
- 104 invalid initial/type-mismatched I observations detected and NOT silently promoted to new entities

## TrialSieve

Canonical modeling corpus:
- 1,609 documents
- 52,638 spans
- 20 native tags

First-campaign admitted auxiliary pool:
- train: 1,148
- validation: 223
- admitted documents: **1,371**
- admitted spans: **44,940**

Reserved and excluded:
- test: **238 documents**

All 20 native tags remain represented in the admitted train+validation pool.

No TrialSieve native type is converted to native ACAD_PASS P/I/C/O.
In particular:
`Non-Study Drug != C`.

## EvidenceOutcomes

Adapter contract:
`OUTCOME_AUXILIARY_ONLY`

No missing P/I/C label is interpreted as a negative native label.

## PICO-Corpus

Adapter contract:
`NATIVE_26_TYPE_AUXILIARY`

No:
- control -> C
- intervention -> I
- outcome -> O
- participant-like label -> P
collapse is performed in the first campaign.

## Original EBM-NLP

Only aggregated training P/I/O annotations are admitted.

Medical-professional expert-test contents are reserved and not read for first-campaign training.

## Synthetic contract

Verified:
- only B-X starts a source-compatible native entity;
- invalid standalone/mismatched I-X does not create a new entity;
- auxiliary source labels never emit native P/I/C/O by automatic mapping.

This supersedes any earlier adapter preflight that did not enforce TrialSieve test exclusion.

Remaining before first fit:
- per-fit family decontamination manifests;
- runtime/GPU closure;
- complete data-manifest binding.

No scientific fit is authorized.
