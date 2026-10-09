# ACAD_PASS — Federation Model/Tokenizer Identity Preflight Freeze V1

Date: 2026-10-09

State:
`FEDERATION_MODEL_TOKENIZER_IDENTITY_PREFLIGHT_PASS`

Run:
`37882354519`

Artifact:
`11594613594`

Digest:
`sha256:48cdb8bc6b82567f2e1ec38fe5a3fb13c449c32419053ef5d8ac6dfb07a40e50`

Runtime used for identity preflight:
- Python 3.11.16
- transformers 4.57.3
- huggingface-hub 0.36.0
- tokenizers 0.22.1
- no PyTorch/model forward pass was used.

## D0-D3 reference encoder

Repository:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract`

Revision:
`d673b8835373c6fa116d6d8006b33d48734e305d`

Resolved revision:
exact match.

Weight:
`pytorch_model.bin`

SHA256:
`d513412d396cecec5f67936ac871b4aaf1178dfb5193776e790fd2b28bba240c`

Tokenizer:
`BertTokenizerFast`

Vocab:
28,895

Vocab digest:
`319443b55546c116fd03df09721addc1731b7d9abb2ad687b19ee55339d0bbd1`

Synthetic tokenization fixture digest:
`8c44cdda4f6b718ff111654c625b8e7cd6ca480ecfa90b07de5cdc55bbf45f45`

Model:
- type bert
- hidden size 768
- max positions 512.

## D4 modern challenger

Repository:
`thomas-sounack/BioClinical-ModernBERT-base`

Revision:
`c3648aa87af95837c809e6f0c5f85d08160db437`

Resolved revision:
exact match.

Weight:
`model.safetensors`

SHA256:
`ea7388682b12cb833491ca8a697e84e3e67122c65c9c658f4ad3355fdd891546`

Tokenizer:
`PreTrainedTokenizerFast`

Vocab:
50,368

Vocab digest:
`de3e1f69578434aad68361023e6bd0f5927dbe154e85017b9ca016f2cf5bff88`

Synthetic tokenization fixture digest:
`7ab897455dad2316d0205fdc06de3a694f813dc9d99b99670afc6395c40363e9`

Model:
- type modernbert
- hidden size 768
- max positions 8192.

## Adapted PICOX encoder

Repository:
`microsoft/BiomedNLP-BiomedBERT-large-uncased-abstract`

Revision:
`f18ff5ec008285849e7c467b2618262b0def6238`

Resolved revision:
exact match.

Weight:
`pytorch_model.bin`

SHA256:
`2d7a3e00619bab3b5c9a9d04dc173c6197becd5a53a253999ded7ed742ba2419`

Tokenizer:
`BertTokenizerFast`

Vocab:
28,895

Vocab digest:
same as BiomedBERT base:
`319443b55546c116fd03df09721addc1731b7d9abb2ad687b19ee55339d0bbd1`

Synthetic tokenization fixture digest:
same as BiomedBERT base:
`8c44cdda4f6b718ff111654c625b8e7cd6ca480ecfa90b07de5cdc55bbf45f45`

Model:
- type bert
- hidden size 1024
- max positions 512.

## Interpretation

Model and tokenizer identities are now frozen and reproducible.

This closes:
- floating model revision risk;
- tokenizer drift risk;
- weight identity ambiguity for the three primary encoders.

It does NOT close:
- full PyTorch/CUDA training runtime;
- GPU hardware;
- mixed precision;
- deterministic CUDA settings.

Therefore:
`MODEL_TOKENIZER_IDENTITY_CLOSED / GPU_TRAINING_RUNTIME_PENDING`.
