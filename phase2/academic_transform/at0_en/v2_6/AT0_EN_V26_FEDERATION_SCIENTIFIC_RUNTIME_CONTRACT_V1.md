# ACAD_PASS — Federation Scientific Runtime Contract V1

Date: 2026-10-09

State:
`SCIENTIFIC_SOFTWARE_RUNTIME_FROZEN / GPU_SPECIFIC_BINDING_PENDING`

Scientific training:
`NOT_AUTHORIZED`

## Canonical scientific software runtime

- Python 3.11.16
- NumPy 1.26.4
- PyTorch base 2.5.1
- Transformers 4.48.0
- Tokenizers 0.21.0
- huggingface_hub 0.28.1
- safetensors 0.5.2
- accelerate 1.3.0

Canonical preflight:
- run `37898560516`
- artifact `11601622017`
- digest `sha256:854bef337e95e56fdaaccebc77ffb93bdf98a9dd489fe5c4122b0b259a8f6368`

The prior Transformers 4.57.3 environment from run 37882354519 is explicitly classified as:
`IDENTITY_AUDIT_ONLY`.

It was used to hash/inspect model/tokenizer files and is NOT authorized for scientific training.

## Canonical model revisions

D0-D3:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract@d673b8835373c6fa116d6d8006b33d48734e305d`

D4:
`thomas-sounack/BioClinical-ModernBERT-base@c3648aa87af95837c809e6f0c5f85d08160db437`

Adapted PICOX:
`microsoft/BiomedNLP-BiomedBERT-large-uncased-abstract@f18ff5ec008285849e7c467b2618262b0def6238`

PICOX weight:
- file `pytorch_model.bin`
- SHA256 `2d7a3e00619bab3b5c9a9d04dc173c6197becd5a53a253999ded7ed742ba2419`

The later `6611fb0...` revision is RETIRED from the ACAD_PASS scientific contract.
It introduced a safetensors conversion; it is not needed because the f18ff5e PyTorch weight identity was already audited and frozen.

## Remaining GPU-specific binding

Before first fit, freeze:
- actual GPU model / VRAM;
- exact PyTorch CUDA build;
- CUDA runtime/toolkit;
- cuDNN;
- mixed precision;
- gradient accumulation;
- worker count;
- TF32;
- deterministic CUDA/CUBLAS settings;
- checkpoint filesystem/resume contract.

Until that document is PASS:
`NO_FIRST_FIT`.
