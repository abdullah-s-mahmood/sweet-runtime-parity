# ACAD_PASS — R4.4-A OOF Upstream Bank Authorization V1

Date: 2026-10-07
Authorization: ONE SEQUENTIAL R44-A WORKFLOW ONLY

## Preconditions satisfied

- R4.3 Stage B frozen as scientific FAIL.
- Causal FIT replay proved in-sample B perfection and out-of-document gap.
- Gold/source semantic contract frozen.
- Source preprocessing parity confirmed.
- R4.4 read-only preflight run `37572165532` PASS.
- R4.4 manifest SHA256 `799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`.
- Adversarial review blocks head fitting in R44-A.
- VERIFY_INTERNAL remains sealed.

## Authorized data

Only the 256 DESIGN documents in the frozen R4.4 manifest.

Five OOF folds:
- fold0 held-out: 52 docs
- fold1..4 held-out: 51 docs each.

For each fold k:
- training docs = DESIGN minus held-out fold;
- held-out fold labels may be used only AFTER candidate inference to assign audit targets/taxonomy;
- no VERIFY_INTERNAL;
- no old R4.3 SELECT;
- no historical DEV, test, other folds, FactPICO or consumed 60-RCT.

## Authorized model training per fold

Sequentially, never in parallel:

1. B_CANDIDATE
   - base: pinned BiomedBERT converted identity used in R4.3
   - seed 44
   - lr 5e-5
   - weight decay 0
   - batch 8
   - epochs 10 fixed
   - linear schedule, no warmup, clip 1.0
   - final fixed epoch only

2. C_BOUNDARY
   - same base
   - seed 44
   - lr 5e-5
   - weight decay .01
   - batch 8
   - epochs 3 fixed
   - linear schedule, no warmup, clip 1.0
   - final fixed epoch only
   - source-compatible boundary labels from B-start entities only.

No C_TYPE training.

## Held-out decoding

Source-compatible constrained BIO decoder:
- only B-X starts a candidate;
- same-type I-X extends;
- any initial I-X, O->I-X or cross-type I-X that lacks explicit source-compatible B start is logged as a BIO violation and does not manufacture a candidate;
- document-continuation metadata remains separate and does not increment source-compatible entity count.

## Candidate bank row

For every held-out native B proposal record:
- fold, document, sentence, start, end;
- B proposed type;
- B confidence;
- width;
- section TITLE/METHODS;
- normalized example position;
- normalized start position;
- OOF Boundary start/end probabilities;
- exact coordinate gold target P/I/C/O if present, otherwise NONE;
- B exact-type correctness;
- error taxonomy;
- goldless-example flag.

Gold assignment occurs after model inference and cannot alter candidate generation.

## Required fold diagnostics

- held-out source-compatible gold P/I/C/O;
- candidate count;
- coordinate ceiling;
- typed-B ceiling;
- precision/recall of native B;
- FP taxonomy:
  - WRONG_TYPE_EXACT_COORD
  - SAME_CLASS_WRONG_BOUNDARY
  - DIFFERENT_CLASS_WRONG_BOUNDARY
  - SPURIOUS_NO_OVERLAP
- proposals in goldless examples;
- confidence distribution summaries;
- raw BIO violations;
- model hashes and fixed training losses/steps;
- train/heldout document hashes and overlap guards.

## Storage

Do not upload temporary ~GB fold model weights.
Freeze:
- candidate JSONL;
- fold summary;
- model SHA256 identities;
- code/protocol hashes;
- process status.

The scientific evidence in R44-A is the held-out candidate bank, not re-use of the ephemeral model files.

## Workflow sequencing

Five fold jobs may be implemented as a matrix only with:
`max-parallel: 1`
and `fail-fast: true`.

Therefore only one fold trains at a time.

After all five succeed:
- a read-only aggregation job verifies complete DESIGN coverage and zero document overlap;
- concatenates frozen banks;
- reports total OOF error distribution and class/candidate ceilings;
- does not fit J0/J1 or choose thresholds.

## Stop boundary

After aggregated R44-A bank:
`STOP_BEFORE_ANY_HEAD_TRAINING_OR_VERIFY_INTERNAL_ACCESS`.

Then perform one adversarial audit of the measured OOF bank and freeze R44-B selection protocol.

DECISION:
`AUTHORIZE_R44A_SEQUENTIAL_OOF_B_AND_BOUNDARY_BANK_ONLY`.
