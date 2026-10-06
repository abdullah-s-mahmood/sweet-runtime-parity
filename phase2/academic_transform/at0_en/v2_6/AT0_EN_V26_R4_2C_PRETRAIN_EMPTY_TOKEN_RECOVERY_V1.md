# ACAD_PASS — R4.2C Pre-Training Empty-Token Recovery V1

Date: 2026-10-06
Status: FROZEN EXECUTION-ONLY RECOVERY / NO SCIENTIFIC TRAINING RESULT

## 1. Failed run preserved

R4.2C development training trigger:
- run `37451685278`
- job `112229491860`
- artifact `11406449018`
- artifact digest `sha256:a515ebe81649f456f669b4da32679de4f6ebaa342388bc51978bc2cb33240ad5`

The run failed before the first training unit.

Traceback:
`RuntimeError: boundary truncation: 54 != 55`

Observed durable status:
- completed_units = 0
- no boundary epoch completed
- no span-classifier epoch completed
- no calibration result
- no scientific performance result

Classification:
`PRE_TRAINING_TECHNICAL_IMPLEMENTATION_FAILURE`

## 2. Read-only tokenizer-capacity audit

Audit run:
`37454434658`

Artifact:
`11408961382`

Artifact digest:
`sha256:fd43fccc9b7dc60664af21ac9178a2d59dea557462b2f99dc43a0a0be141da33`

Canonical pre-hash:
`768fb30b1fd0261c0cbf3fddfe83bc407aec083399a56e9c8d8b256ba11c6898`

Result:
- train sentences = 1576
- dev sentences = 205
- train max wordpieces with specials = 141
- dev max wordpieces with specials = 141
- sentences >256 = 0
- sentences >512 = 0

Therefore:
`MAX_LENGTH_256_IS_NOT_THE_CAUSE`

The audit found tokenizer word-id loss in 12 train sentences despite all sequences being far below 256:
- total missing CoNLL surface-token rows = 17
- no dev sentence affected

## 3. Root cause

The pinned fold1 raw train file contains 17 literal zero-length surface-token rows:
- O = 5
- I-I = 5
- I-P = 6
- I-O = 1

These rows have an empty token field and a tag field.

The fast tokenizer emits no wordpiece / word-id for a zero-length surface token. The former R4.2C implementation interpreted the resulting word-count mismatch as truncation.

Thus the prior error label was misleading:
`TOKENIZER_WORD_MAPPING_OMISSION_FROM_ZERO_LENGTH_SOURCE_ROWS`
not sequence-length truncation.

## 4. Pinned-source behavior

Pinned source repository:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO`
commit:
`bc4b878773192f38b2600ec830ca4208b82f7dc0`

In `utils_ner.update_data_to_max_len()`, the source tokenizes each surface word and explicitly executes `continue` when the tokenized length is zero, filtering the complete row before training.

In `PICO_ner.py`, the source configuration uses:
- `max_seq_len_list = [256]`
- `do_update_max_len_list = [True]`

and preprocesses train/dev/test through `update_data_to_max_len()` before training.

Therefore source-aligned handling is to remove tokenized-empty rows, not increase max sequence length and not invent missing symbols.

## 5. Recovery implemented

R4.2C trainer correction commit:
`a74f064b473a5065886afb39926369305532b778`

Correction:
- preserve raw file SHA guards unchanged;
- remove only literal zero-length surface-token rows during CoNLL ingestion;
- assert the exact frozen train empty-row tag distribution:
  `{"O":5,"I-I":5,"I-P":6,"I-O":1}`;
- assert zero such rows in dev;
- preserve max_length = 256;
- preserve all model identities, epochs, learning rates, weight decay, batch sizes, threshold grid, exact scoring, and frozen gates;
- add a full train/dev token-alignment guard to smoke so the prior first-8-sentence blind spot cannot recur.

No:
- threshold change
- hyperparameter change
- test access
- FactPICO access
- consumed holdout access
- scientific training

## 6. Authorization boundary

Next authorized step:
`RERUN R4.2C MECHANICS/SMOKE ONLY ON CORRECTED IMPLEMENTATION`

If smoke passes with full train/dev token alignment:
- freeze recovery smoke evidence;
- then authorize one replacement R4.2C development training + frozen-dev calibration run.

The failed pre-training run does not count as a completed scientific training run because zero training units completed and no scientific result exists.

STOP before any EBM/COVID/AD test inference.
