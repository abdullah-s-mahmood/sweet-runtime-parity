# AT0-EN V2.6-DEV — R4.2 Auxiliary Biomedical Extraction Witness Design V1

Date: 2026-10-05
Status: DESIGN FROZEN BEFORE MODEL ACQUISITION / TRAINING / INFERENCE

## Trigger

R4.1B consumed internal holdout result:
- unresolved predicate rate: 300/715 = 41.9580% > 40% threshold
- non-CERTAIN rate: 304/715 = 42.5175% <= 45% threshold
- documents with non-CERTAIN <=50%: 49/60 = 81.6667% >= 80%
- short evidence <=3 chars: 2 != 0
- overall internal holdout: FAIL
- holdout is permanently CONSUMED and MUST NOT be rerun or tuned against

Per the preregistered R4 design, this triggers R4.2.

## Research-grounded strategy comparison

A. More R4.1B regex/rule expansion
REJECTED as primary path.
Reason: consumed holdout failure cannot be used for further R4.1B tuning; rule expansion also risks brittle coverage and benchmark shaping.

B. LLM-only PICO extraction
REJECTED.
Reason: higher variance, weaker auditability, and literature shows specialized biomedical NER remains stronger for PICO-style extraction. No LLM may become a safety oracle.

C. Weak-supervision-only rule aggregation
RESERVED as fallback.
Reason: literature supports it, but current project already has deterministic rule evidence and the remaining gap is lexical/syntactic coverage. A trainable biomedical NER witness is the narrower complementary signal.

D. Section-aware BiomedBERT PICO token-classification witness
SELECTED.

## Selected R4.2 architecture

Architecture:
1. R4.1B deterministic extractor remains authoritative for explicit deterministic structures.
2. Auxiliary PICO witness identifies span-level P/I/O labels with token probabilities.
3. Witness output is converted to provenance-preserving span proposals only.
4. Fusion may use witness evidence to resolve an otherwise UNRESOLVED assertion only under frozen corroboration rules.
5. A witness prediction can NEVER by itself yield PASS_CANDIDATE.
6. Critical contradictions from deterministic extraction remain non-overridable.
7. Low-confidence or conflicting witness evidence routes to REVIEW.

Base model:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract`
Rationale:
- biomedical abstract pretraining;
- MIT license;
- used as the primary base in the published section-specific PICO extraction pipeline;
- approximately 110M parameters, tractable for reproducible CPU/GPU development.

## Frozen public training/evaluation source

Repository:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO`

Pinned source commit:
`bc4b878773192f38b2600ec830ca4208b82f7dc0`

Dataset roles:
- TRAIN: `data/EBM-NLPmod/fold1/train.txt`
- CALIBRATION/DEV: `data/EBM-NLPmod/fold1/dev.txt`
- IN-DOMAIN DEV TEST: `data/EBM-NLPmod/fold1/test.txt`
- CROSS-DOMAIN DEV TEST 1: `data/COVID-19/fold1/test.txt`
- CROSS-DOMAIN DEV TEST 2: `data/AD/fold1/test.txt`

Frozen Git blob identities:
- EBM train: `9e6ef5b93c9d2b728977c202412cea58fe86fa86`
- EBM dev: `f9e4ec83bde8a564dc3148ef730b0f9801fdbdf7`
- EBM test: `7a22af9caf5a67aa75700a79ad3d47399d53d965`
- COVID test: `659be83d0389b2f2c1e12ee9cf24898346fe55fa`
- AD test: `7b752b3e5f813a8104cf8a1173ecdba89012dbf5`

No FactPICO records are used.
The consumed 60-RCT PICO-Corpus holdout is not used.
The opened 30-RCT diagnostic set is not used for model fitting or threshold selection.

## Label scope

Use the published BIO labels exactly:
- P = Population/Participants
- I = Intervention/Comparator treatment spans
- O = Outcome
- O-tag = outside PICO entity

R4.2 does not invent additional entity labels during this version.

## Training protocol frozen before inference

Runtime target:
- Python 3.11
- PyTorch 2.2.x
- Transformers 4.39.x
- tokenizers from the pinned base model
- safetensors only for final model freeze where supported

Training:
- seed = 20261005
- max sequence length = 256
- optimizer = AdamW
- learning rate = 2e-5
- weight decay = 0.01
- warmup ratio = 0.10
- train batch size = 8
- eval batch size = 16
- gradient accumulation = 2
- maximum epochs = 10
- early stopping patience = 2
- metric for checkpoint selection = entity-level macro F1 on EBM dev
- deterministic algorithms requested where supported
- no hyperparameter search after seeing test results

Subword labeling:
- label first subtoken with gold BIO tag
- remaining subtokens ignored in loss
- prediction spans reconstructed to original word offsets

## Calibration

No arbitrary fixed confidence is selected after external/dev test opening.

Calibration population:
`EBM-NLPmod fold1/dev.txt`

Freeze one witness acceptance threshold chosen from:
`{0.80, 0.85, 0.90, 0.95}`

Selection rule:
choose the LOWEST threshold satisfying BOTH on calibration:
- token/entity precision >= 0.90 for each of P, I, O where estimable
- no class precision below 0.85

If no threshold satisfies this:
`R4_2_WITNESS_NOT_READY`
and no fusion experiment is authorized.

The threshold is then frozen before EBM test/COVID test/AD test evaluation.

## R4.2 witness development gates

On each test corpus report:
- entity-level precision / recall / F1 for P, I, O
- macro F1
- micro F1
- coverage above calibrated threshold
- abstention rate

Minimum witness gate to continue to fusion development:
1. EBM in-domain macro F1 >= 0.75
2. EBM micro F1 >= 0.80
3. COVID micro F1 >= 0.80
4. AD micro F1 >= 0.80
5. no P/I/O class precision < 0.75 on either cross-domain test
6. deterministic/reproducible output hashes under frozen runtime

These are development gates, not external scientific claims.

## Fusion contract

The witness only proposes:
- entity type
- exact character/token span
- probability
- model identity
- source sentence/section
- provenance hash

For an unresolved R4.1B sentence:
- deterministic assertion frame remains primary;
- witness can supply candidate population/intervention/outcome span ownership;
- a critical assertion becomes CERTAIN only if:
  a) witness probability >= frozen threshold, AND
  b) deterministic surface structure supports the relation/predicate or a separately frozen semantic witness corroborates it, AND
  c) no deterministic contradiction exists.

Otherwise:
`UNCERTAIN -> REVIEW`

The witness may NEVER:
- change a frozen numeric value/unit;
- suppress unmatched critical source content;
- override polarity/modality/causality contradiction;
- create PASS solely from model confidence;
- alter FactPICO or consumed holdout results.

## Research basis

This architecture follows evidence that:
- section-aware PICO extraction with biomedical pretrained models achieves strong cross-domain RCT extraction;
- weak/semi-supervision can improve PICO recognition when labels are limited;
- structured PICO representation is preferable to flat holistic judgments;
- LLM-only extraction is not sufficiently reliable to serve as the sole clinical information-extraction oracle.

## Required pre-inference identity freeze

Before training:
- resolve exact Hugging Face base-model revision;
- hash config/tokenizer/model files;
- record base-model license;
- hash all five frozen dataset files;
- freeze training script SHA;
- freeze runtime dependency versions;
- verify no use of FactPICO or consumed 60-RCT holdout.

## STOP boundaries

Preflight identity verification may run now.
Training may begin only after preflight PASS.

After training:
STOP before test evaluation until:
- selected checkpoint SHA is frozen;
- calibrated threshold is frozen using EBM dev only.

After dev-test evaluation:
STOP before any R4.2 fusion implementation.

No external validation.
No FactPICO rerun/rescoring.
No consumed-holdout rerun.
No Arabic work.
