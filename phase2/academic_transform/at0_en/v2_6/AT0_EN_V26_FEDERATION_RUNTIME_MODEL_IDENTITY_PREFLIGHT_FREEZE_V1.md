# ACAD_PASS — Federation Runtime and Model Identity Preflight Freeze V1

Date: 2026-10-09

State:
`FEDERATION_RUNTIME_MODEL_IDENTITY_PREFLIGHT_PASS`

Run:
`37895636271`

Artifact:
`11600067736`

Digest:
`sha256:3c87cd79c5693137172c50305f4f452ccf2d861e78159e5d51479b9c24e4da73`

Scientific training:
false

Weights loaded:
false

## Frozen software runtime

- Python 3.11.16
- PyTorch 2.5.1 (observed build 2.5.1+cu124)
- Transformers 4.48.0
- Tokenizers 0.21.0
- huggingface_hub 0.28.1
- safetensors 0.5.2
- accelerate 1.3.0
- NumPy 1.26.4

## Frozen model identities

### Reference BiomedBERT base
- id: microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract
- revision: d673b8835373c6fa116d6d8006b33d48734e305d
- model_type: bert
- hidden: 768
- layers: 12
- heads: 12
- positions: 512
- tokenizer signature:
  088f1bdf2509aee48015c38209b07bebec8d4d266232e04c5d9bd82704b76e81

### Adapted PICOX BiomedBERT large
- id: microsoft/BiomedNLP-BiomedBERT-large-uncased-abstract
- revision: 6611fb0be85c82ae6089ab63a0d81edfcd956dae
- model_type: bert
- hidden: 1024
- layers: 24
- heads: 16
- positions: 512
- tokenizer signature:
  088f1bdf2509aee48015c38209b07bebec8d4d266232e04c5d9bd82704b76e81

### BioClinical ModernBERT challenger
- id: thomas-sounack/BioClinical-ModernBERT-base
- revision: c3648aa87af95837c809e6f0c5f85d08160db437
- model_type: modernbert
- hidden: 768
- layers: 22
- heads: 12
- positions: 8192
- tokenizer signature:
  c4bcc77a64bb3a2f71fdde8766f620d2513f9ac96d28ecf11240c2329f1decf3

## Determinism contract

Prospective scientific runtime must:
- set Python/NumPy/Torch/Torch-CUDA seeds;
- enable deterministic algorithms where supported;
- disable cudnn benchmark;
- use final-checkpoint-only selection.

## Remaining runtime blocker

This preflight does NOT qualify:
- future GPU model;
- VRAM capacity;
- batch/mixed-precision feasibility;
- model-weight SHA/download identity;
- wall-clock feasibility.

Therefore runtime state:
`SOFTWARE_AND_CONFIG_IDENTITY_PASS / GPU_WEIGHT_MEMORY_QUALIFICATION_PENDING`

No scientific fit is authorized by this file alone.
