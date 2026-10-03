# MP-SEF Proposer Identity Freeze v1

Date: 2026-09-30
Status: FROZEN BEFORE RUNTIME PARITY
Parent architecture:
phase2/redesign/ARABIC_CORRECTION_ARCHITECTURE_V2_MPSEF.md

## Scope

This file freezes the initial reproducible proposer identities for the
candidate-generation-only feasibility experiment.

No selector is authorized yet.
No reserved dataset is opened.

## P1 — SWEET iterative NoPnx proposer

Role:
candidate proposer only.

Model:
CAMeL-Lab/text-editing-qalb14-nopnx

Frozen weight revision:
21286e56ce98a86362db540863f91c083b8970f9

Frozen model weight SHA256:
9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d

Official text-editing implementation:
CAMeL-Lab/text-editing

Frozen implementation revision:
4d552ca3ae98029550f27fc52aa1b22883e16e61

Inference:
- tokenizer: BertTokenizer from frozen model revision
- model: BertForTokenClassification
- top-1 argmax labels
- official gec.tag.rewrite
- NoPnx only for initial proposal feasibility
- decode_iter = 2
- output of pass 1 becomes input to pass 2
- no confidence threshold
- no top-k expansion
- no punctuation model in the initial union-recall experiment

Important:
P1 is NOT H1-v1.
H1-v1 remains permanently CLOSED FAIL.
This new proposer is separately versioned and uses the documented iterative
SWEET mode that H1-v1 explicitly excluded.

## P2 — AraBART + Morph + GED proposer

Role:
contextual seq2seq candidate proposer plus GED auxiliary evidence.

### GEC model

Model:
CAMeL-Lab/arabart-qalb14-gec-ged-13

Frozen Hugging Face revision:
410588a318d988cdcfdbf64cf5745ed4adea0f6a

Model family:
AraBART+Morph+GEC-13, QALB-2014

### GED model

Model:
CAMeL-Lab/camelbert-msa-qalb14-ged-13

Frozen Hugging Face revision:
447179dc63d186e4bff09a993e90e73ad622d571

Model family:
CAMeLBERT-MSA GED-13, QALB-2014

### Official implementation

Repository:
CAMeL-Lab/arabic-gec

Frozen repository revision:
8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

Repository requirements:
- Python >= 3.9
- torch == 1.11.0
- camel-tools == 1.4.1
- datasets == 2.5.1
- sentencepiece == 0.1.99
- protobuf == 3.20.3

Modified Transformers source dependency:
bc21aaca789f1a366c05e8b5e111632944886393

### Frozen preprocessing / inference

1. Input whitespace tokenization.
2. BERTUnfactoredDisambiguator.pretrained().
3. For each source token, select analyses[0].analysis['diac'].
4. dediac_ar over selected analysis.
5. Join morphologically preprocessed tokens with spaces.
6. Run paired CAMeLBERT GED model.
7. Take argmax GED label per source word.
8. Expand GED label over AraBART subword tokens.
9. Feed GED tag IDs through the modified Transformers GEC model.
10. Generation:
   - num_beams = 5
   - max_length = 100 for initial parity, unless source-length handling
     requires a preregistered deterministic extension before scoring
   - num_return_sequences = 1
   - no_repeat_ngram_size = 0
   - early_stopping = False
11. Decode with:
   - skip_special_tokens = True
   - clean_up_tokenization_spaces = False

No standard unmodified AutoModelForSeq2SeqLM inference may be silently
substituted for the published GED-conditioned path.

## Environment separation

P1 and P2 may use separate frozen environments.

Cross-environment exchange:
JSON / JSONL only.

No Python object serialization across proposer environments.

## Runtime parity requirement

Before any candidate recall is measured:

### P1 parity
On a deterministic source-only sample:
- reproduce the documented two-pass NoPnx output using the frozen official
  text-editing code;
- compare against the MP-SEF P1 runner;
- required normalized output match: 100%.

### P2 parity
On a deterministic source-only sample:
- execute the frozen official arabic-gec preprocessing/inference path;
- compare:
  - morph_preprocessed_text
  - GED labels
  - normalized generated output
against the MP-SEF P2 runner;
- required all-field match: 100%.

Recommended initial sample:
64 CALIBRATION source sentences selected by frozen SHA ranking.

Gold/reference text must not be consulted for parity.

If either proposer fails parity:
- do not compute union recall;
- repair only implementation/environment parity issues;
- do not change model weights or generation semantics.

## Weight/data integrity still to freeze operationally

The acquisition workflow must record:
- downloaded model file SHA256 hashes for P2 GEC and GED;
- exact pip freeze for each environment;
- CAMeL Tools pretrained disambiguator resource identity/hashes;
- any morphology resource files used at runtime;
- source sample UID digest;
- runner source SHA256.

These hashes become part of the proposer lock after parity succeeds.

## Conditional proposers

P3 cross-domain AraBART, MTAGEC, STAGEET, and any LLM proposer are NOT
authorized in the initial union experiment.

They may be considered only after P1+P2 union recall and marginal gain are
measured.

## Integrity

Keep closed:
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST
