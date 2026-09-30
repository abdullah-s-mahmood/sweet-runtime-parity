# MP-SEF P2 Runtime Lock v1

Date: 2026-09-30
Status: FROZEN PASS
Parent:
phase2/redesign/MPSEF_PROPOSER_IDENTITY_FREEZE_V1.md

## Proposer

P2 — AraBART + Morph + GED proposer

Role:
contextual sequence-to-sequence candidate proposer plus GED auxiliary evidence.

### GEC model

Model:
CAMeL-Lab/arabart-qalb14-gec-ged-13

Frozen revision:
410588a318d988cdcfdbf64cf5745ed4adea0f6a

Observed model file SHA256:
- pytorch_model.bin:
  5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f
- config.json:
  f399d3123101de825a973b15ae3f2c872d750d9a9ec39f72afd99403795ac67e
- sentencepiece.bpe.model:
  cbb59d772bc9bb2da5dc4a73a00c61c0912c6d2596aad970fa2cd3d69898b245
- tokenizer.json:
  4ef36f44cf9d216888654b94bc3bfe75cc3372bd18f4ff13473e71d4d06410fb

### GED model

Model:
CAMeL-Lab/camelbert-msa-qalb14-ged-13

Frozen revision:
447179dc63d186e4bff09a993e90e73ad622d571

Observed model file SHA256:
- pytorch_model.bin:
  23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f
- config.json:
  e00493c39d09e0290358713f01cee90b060cab6e59688bdd2ca53f487396ae11
- vocab.txt:
  1df5f8da6ad6c56153c7a974c0b149bb7a0a6e332bcfa795c99deee6c1136ce2

## Official implementation

Repository:
CAMeL-Lab/arabic-gec

Frozen revision:
8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

Modified Transformers implementation:
the repository-vendored transformers 4.22.2 used by the frozen official path.

## CAMeL morphology/disambiguation resources

CAMeL Tools runtime:
1.4.1

MSA morphology DB SHA256:
195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70

MSA BERT unfactored disambiguator model SHA256:
a1a22431cdc0934151e4039abbd7890f06ba7c1f914ca71a90eba218401ae539

## Frozen inference path

1. whitespace-tokenized source
2. BERTUnfactoredDisambiguator.pretrained(model_name="msa")
3. analyses[0].analysis["diac"] per token
4. dediac_ar
5. paired CAMeLBERT GED inference
6. argmax GED labels
7. GED label expansion to AraBART subword tokens
8. GED-conditioned AraBART generation

Generation:
- num_beams = 5
- max_length = 100
- num_return_sequences = 1
- no_repeat_ngram_size = 0
- early_stopping = false
- skip_special_tokens = true
- clean_up_tokenization_spaces = false

## Runtime parity

Workflow run:
36751445734

Job:
110010823722

Artifact:
- id: 11114738715
- name: mpsef-p2-arabart-ged-parity-v1
- digest:
  sha256:c8d2ea2b378a03b3e6ca5f81b53a0527f0f796d8610a6d615027eedce06cbaf3

Deterministic source-only sample:
- n: 64
- salt: MPSEF-P2-ARABART-GED-PARITY-V1-20260930-A
- UID digest:
  f787df9c7acabbb5b6cb02a04c12e5d505e7590b94b19deca9064d321223c6f6

Parity:
- morphology-preprocessed text: 64 / 64
- GED labels: 64 / 64
- AraBART subword tokens: 64 / 64
- input IDs: 64 / 64
- GED label IDs: 64 / 64
- generated exact output: 64 / 64
- generated normalized output: 64 / 64
- all-field match: 64 / 64

Integrity:
- gold/reference consulted: false
- INTERNAL_EVALUATION opened: false
- STRESS_DIAGNOSTIC opened: false

Runner SHA256:
746274e34cc73f0a6f99994f25d5f7e23dd064f54d1b86a2eddc716da7a15f75

Pip freeze SHA256:
cbd42c8a3296eb59e933b04f83c70f34d78b98160f09a069fea32fcfc142fe38

## Decision

P2 runtime parity:
**PASS / ACTIVATED AS PROPOSER ONLY**

This authorizes P2 only as a candidate proposer/evidence source inside MP-SEF.
It does not authorize direct document rewriting or automatic correction.

## Current architecture state

P1 runtime parity:
PASS

P2 runtime parity:
PASS

Candidate-union evaluation:
NOT YET RUN

Selector:
NOT AUTHORIZED

## Exact next step

Pause before candidate-union evaluation for independent methodological review of:
- MP-SEF construct validity;
- proposer diversity;
- canonical edit decomposition;
- candidate-stage endpoints/gates;
- leakage/double-dipping risk;
- stop rules;
- whether selector training should ever be authorized.

Reserved/internal datasets remain closed.
