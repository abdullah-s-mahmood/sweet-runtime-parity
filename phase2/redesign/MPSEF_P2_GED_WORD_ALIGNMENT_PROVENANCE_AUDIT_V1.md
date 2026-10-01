# MP-SEF P2 GED WORD-ALIGNMENT PROVENANCE AUDIT V1

Date: 2026-10-01
Status: FROZEN SOURCE-ONLY PROVENANCE FINDING

## Scope

This audit inspects only the already frozen P2 C_F proposal artifact:

- cases: 1,918
- proposal SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

No gold/reference data was read.
No R_joint value was computed.
No proposal text was regenerated or modified.

## Finding

For every frozen P2 proposal, compare:

`len(morph_preprocessed_text.split())`

against:

`len(ged_labels)`

Observed:

- total cases: **1,918**
- mismatched cases: **1,918 / 1,918 = 100%**
- matched cases: **0**
- total excess GED labels: **30,341**
- mean excess labels/case: **15.8191**
- median excess labels/case: **15**
- p95 excess labels/case: **27**
- minimum excess: **2**
- maximum excess: **87**

Example first failing UID:

`dev:1003`

- morphology words: **50**
- GED labels: **58**

## Frozen implementation cause

The current frozen P2 runner obtains GED predictions from tokenized BERT output after removing special tokens, then passes the resulting label list into:

`zip(morph.split(), ged_labels)`

inside `make_gec_inputs`.

Therefore the zip length is limited by the shorter morphology-word list.

When the GED tokenizer emits more than one subword for a whitespace-delimited morphology word, later GED predictions are shifted relative to morphology words and tail labels are silently unused.

## Upstream evidence

The frozen official `CAMeL-Lab/arabic-gec` revision
`8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf` contains two relevant facts:

1. The public root README inference example uses the same pattern:
   - obtain GED predictions from tokenized model output;
   - then `zip(morph_pp_text.split(), pred_ged_labels)`.

2. The same repository's data construction explicitly requires:
   `len(tags.split()) == len(source.split())`,
   meaning GEC GED tags are defined at source-word level.

3. The GED utilities use tokenizer `word_ids` to align subword tokens to source words during token-classification preprocessing.

Thus the frozen public inference example does not by itself prove correct word-level projection of predicted GED labels.

## Scientific interpretation

This is not merely missing truncation metadata.

It is a source-only provenance defect in the frozen P2 construction:
the exact mapping from predicted GED subword labels to morphology words is not validly established.

The frozen P2 outputs remain immutable historical proposals and must NOT be rewritten or replaced inside this cycle.

However, under the independent-review requirement L09, the current P2 hypotheses cannot be certified executable because GED coverage/alignment is not proven and silent zip loss is present in every C_F record.

## Legalizer consequence

For this cycle, every P2 hypothesis with:

`len(ged_labels) != len(morph_preprocessed_text.split())`

must receive:

`EXECUTION_FAILED:GED_WORD_ALIGNMENT_MISMATCH`

before any gold/reference is available.

These records remain in the source-only legalizer audit.
They are not deleted from the C_F population.
KEEP remains available for a source-valid case.
P2 is not silently replaced by a corrected regeneration.

## Measurement consequence

The frozen P1/P2 whole-hypothesis protocol remains structurally defined as:
KEEP / P1_FINAL if executable / P2_FINAL if executable.

This finding means the frozen P2 candidate is non-executable under the corrected source-only legality contract for all 1,918 observed C_F cases.

No R_joint measurement is authorized by this audit.

The next scientific step is a source-only legalizer run to determine the resulting executable action sets and remaining P1 legality, followed by a protocol decision before any reference-based measurement.
