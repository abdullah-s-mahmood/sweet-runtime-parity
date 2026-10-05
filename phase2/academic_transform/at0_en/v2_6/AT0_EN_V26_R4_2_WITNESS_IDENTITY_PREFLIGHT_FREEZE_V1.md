# AT0-EN V2.6 R4.2 — Witness Identity Preflight Freeze V1

Date: 2026-10-05
Status: PREFLIGHT PASS / TRAINING NOT YET RUN / TEST SETS UNOPENED BY TRAINER

## Run identity

Workflow:
`AT0 EN V2.6 R4.2 witness identity preflight`

Run:
`37342777050`

Artifact:
`11358568682`

Artifact digest:
`sha256:6b6d93bb00d860f44a93eec786da8bb6317d55edc2ca5e91d5d47f50f7adbabc`

Canonical pre-hash:
`15553f4beb1657cd022f91bd94ecf598bcd322b96c2e0e291e0ff222a6602f80`

## Base model

Repository:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract`

Resolved revision:
`d673b8835373c6fa116d6d8006b33d48734e305d`

License:
`MIT`

Security policy:
- official `pytorch_model.bin` was NOT downloaded or loaded;
- official `flax_model.msgpack` is the sole base weight source;
- conversion to PyTorch token-classification weights must use `from_flax=True`;
- final trained checkpoint must be saved as safetensors.

Safe model file SHA-256:
- `flax_model.msgpack`: `2048c0dca92fe54cf2bec6c36972511ca04e546060307098139b19221dd4e93f`
- `config.json`: `56bab767c02bc792897638feb8addc06d483d9c73769a5f554bbabea1f5507a1`
- `tokenizer_config.json`: `53b6f42b8b8daddbdc6d3532c324187a92b46c1602bd6e8d4ad5a413b4fc90e1`
- `vocab.txt`: `7b36651908a88bc38bda41b728b2a598191e0d3b553cbacf7b1e5f026d5b5b9f`
- `LICENSE.md`: `8542b3a65414366ae3228e8f1658e538ec95f9b8855599c9c6e36751d592be66`

## Frozen data source

Repository:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO`

Commit:
`bc4b878773192f38b2600ec830ca4208b82f7dc0`

Training/calibration SHA-256:
- EBM train: `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`
- EBM dev: `3b12534fedec35660587e6a5084b0b8ff11267c1da4a2f5afe9aa16c4941340a`

Frozen future development-test SHA-256:
- EBM test: `f2e805cd9098c9f52f959e49b5a7b6267c426bbd7d9e26c9e3f25c490a0602af`
- COVID test: `813ca5f596f4d1ac7e96294dfaae4e24b3ef4242a1e1ad82522e942726f2b326`
- AD test: `969c335a8bfc67f08a919dfbaa4fb6e3bb852ce46cff978350251bc53eff927e`

Repository license file:
`NOT OBSERVED`

Current permitted use:
`INTERNAL ACADEMIC RESEARCH DEVELOPMENT PENDING LICENSE CLARIFICATION`

## Leakage guards

- FactPICO used: FALSE
- consumed 60-RCT internal holdout used: FALSE
- opened 30-RCT diagnostic used: FALSE
- training performed in preflight: FALSE
- inference performed in preflight: FALSE

## Authorization after PASS

Authorized:
- create/freeze training script and runtime config;
- train one R4.2 witness on EBM train;
- calibrate threshold on EBM dev only;
- freeze selected checkpoint + threshold;
- STOP before EBM/COVID/AD test inference.

Not authorized:
- test-set inference before checkpoint/threshold freeze;
- consumed holdout reuse;
- FactPICO reuse;
- fusion implementation;
- external validation.
