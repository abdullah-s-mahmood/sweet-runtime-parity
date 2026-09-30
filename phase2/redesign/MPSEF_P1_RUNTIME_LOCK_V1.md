# MP-SEF P1 Runtime Lock v1

Date: 2026-09-30
Status: FROZEN PASS
Parent:
phase2/redesign/MPSEF_PROPOSER_IDENTITY_FREEZE_V1.md

## Proposer

P1 — SWEET iterative NoPnx proposer

Model:
CAMeL-Lab/text-editing-qalb14-nopnx

Model revision:
21286e56ce98a86362db540863f91c083b8970f9

Weight SHA256:
9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d

Official implementation:
CAMeL-Lab/text-editing

Implementation revision:
4d552ca3ae98029550f27fc52aa1b22883e16e61

Decode:
- NoPnx
- top-1
- decode_iter=2
- no confidence threshold
- no top-k expansion
- no punctuation model

## Runtime parity

Workflow run:
36749690421

Job:
110004817860

Artifact:
- id: 11113469233
- name: mpsef-p1-iterative-parity-v1
- digest: sha256:994c98dbe965883f9097a1845dc3240105b3fb11de709aeb11f454b6a34dfbb0

Deterministic source-only sample:
- n: 64
- salt: MPSEF-P1-ITERATIVE-PARITY-V1-20260930-A
- UID digest: c8e2ce921476d009992b6b70fadba809c2a0052308b65c7c8e2ccb8c8e8ec50c

Parity:
- pass 1 exact trace match: 64 / 64
- pass 2 exact trace match: 64 / 64
- all-field match: 64 / 64
- mismatches: 0

Integrity:
- gold/reference consulted: false
- INTERNAL_EVALUATION opened: false
- STRESS_DIAGNOSTIC opened: false

Runner SHA256:
31b0d7728b2d74e9848601653fd91017e54d83867861c287479bbe1c847fe1f1

Pip freeze SHA256:
aa9c31581f733395b1da19244c9971818499dd1d5bd1d3da0b2057b91fe66df4

Key runtime pins:
- Python 3.10
- torch 1.12.1+cpu
- transformers 4.30.0
- huggingface-hub 0.16.4
- sentencepiece 0.1.99
- numpy 1.23.5
- pandas 1.5.3
- pyarrow 14.0.2
- datasets 2.14.7
- editdistance 0.8.1

CAMeL compatibility shim:
the same frozen rewrite-only compatibility shim used in the completed H1 official-alignment audit.

## Decision

P1 runtime parity:
**PASS / ACTIVATED AS PROPOSER ONLY**

This does not authorize any automatic correction.
It authorizes P1 only as one source of candidate edits in MP-SEF.

## Next

Proceed sequentially to P2 runtime parity.

Do not compute union recall until P2 parity is also frozen.
