# MP-SEF P2_V2 WORD / WORDPIECE / LABEL IDENTITY CONTRACT V1

Date: 2026-10-01
Status: FROZEN PRE-IMPLEMENTATION SOURCE-ONLY CONTRACT
Closes: Independent Review BLOCKER B01
Applies to: P2_V2 only
Gold/reference use: FORBIDDEN

## 1. Purpose

P2_V2 must prove identity, not merely count equality.

The V1 failure occurred because subword-level GED predictions were consumed as word-level labels. P2_V2 therefore requires an explicit bijective identity map from the source-derived morphology words through GED segmentation and prediction to the GEC-conditioning representation.

No executable P2_V2 proposal may exist unless every required identity invariant passes.

## 2. Frozen identity chain

For every UID the runner MUST persist this chain:

`UID -> source_sha256 -> morphology_sha256 -> morphology_word_index -> source/morph span -> GED segment_id -> GED first_wordpiece_index -> GED word_label -> GEC word_subword_range -> GEC label IDs -> final generation trace`

Each link is explicit and machine-checkable.

## 3. Canonical word identity record

For every morphology word create exactly one record:

```json
{
  "uid": "...",
  "morph_word_index": 0,
  "morph_word_text": "...",
  "morph_char_start": 0,
  "morph_char_end": 4,
  "source_alignment_status": "EXACT|DERIVED|FAIL",
  "source_char_start": 0,
  "source_char_end": 4,
  "ged_segment_id": 0,
  "ged_wordpiece_start": 1,
  "ged_wordpiece_end": 3,
  "ged_first_wordpiece_index": 1,
  "ged_wordpiece_ids": [101,102],
  "ged_prediction_position": 1,
  "ged_label_name": "UC",
  "ged_label_id": 0,
  "gec_subword_start": 1,
  "gec_subword_end": 2,
  "gec_subword_ids": [501],
  "gec_repeated_label_names": ["UC"],
  "gec_repeated_label_ids": [0]
}
```

No field may be silently omitted for an executable row.

## 4. One-to-one morphology-word coverage

Let M be the ordered morphology word list.

For an executable row all conditions MUST hold:

1. every index `0..len(M)-1` appears exactly once;
2. no duplicate `morph_word_index`;
3. no missing index;
4. no reordered reconstruction;
5. every word has at least one GED wordpiece;
6. every word has exactly one GED prediction position;
7. that prediction position is the first wordpiece position for that word;
8. all remaining GED wordpieces are masked by the configured ignore index;
9. reconstructed word-level GED label sequence length equals `len(M)`;
10. the reconstructed sequence order equals morphology-word order.

A pure count match is insufficient.

Any violation:
`EXECUTION_FAILED:P2V2_WORD_IDENTITY_BIJECTION_FAILED`

## 5. Zero-token word rule

If either the GED tokenizer or GEC tokenizer returns zero tokens for a required morphology word:

- retain the UID record;
- mark explicit failure;
- do not drop the word;
- do not merge it with neighbors;
- do not continue using shifted labels.

Failure:
`EXECUTION_FAILED:P2V2_ZERO_TOKEN_WORD`

The runner must distinguish:
- truly empty source;
- non-empty source that morphology made empty;
- non-empty morphology word that a tokenizer maps to zero tokens.

## 6. Segment budget contract

The effective GED segment capacity MUST be derived from the actual loaded tokenizer/model configuration, not assumed from a historical constant.

Record:

- model_max_length;
- configured max_seq_length;
- number of special tokens added;
- effective content-wordpiece budget;
- padding side;
- truncation side;
- tokenizer special-token map.

A word whose wordpiece length alone exceeds the effective content budget MUST fail explicitly.

It MUST NOT:
- be split secretly across segments;
- create an oversized segment;
- be truncated;
- be dropped.

Failure:
`EXECUTION_FAILED:P2V2_SINGLE_WORD_EXCEEDS_GED_BUDGET`

## 7. Whole-word GED segmentation

Segmentation boundaries occur only between complete morphology words.

For every segment record:

- segment_id;
- first morph_word_index;
- last morph_word_index;
- morphology word count;
- content wordpiece count;
- special token count;
- total encoded length;
- max allowed length.

Required:

`total_encoded_length <= configured_max_seq_length`

All words across all segments must form exactly the ordered full morphology-word sequence.

No overlap or omission.

## 8. GED prediction reconstruction

Predictions are reconstructed using the identity map, not batch position assumptions.

For every GED segment:

- logits shape recorded;
- token positions paired with label-mask positions;
- positions with ignore_index excluded;
- retained positions mapped to exact `morph_word_index`.

After collating all segments:

- no duplicate word index;
- no missing word index;
- no out-of-order word index;
- exactly one label name/id per morphology word.

## 9. Label vocabulary identity

Freeze and hash separately:

GED:
- `id2label`;
- `label2id`;
- serialized config;
- checkpoint revision;
- tokenizer revision.

GEC:
- `ged_label2id`;
- serialized config;
- checkpoint revision;
- tokenizer revision.

For every word, conversion MUST be by label NAME with an exact known mapping.

Forbidden:
- assuming numeric label IDs are interchangeable across GED and GEC models;
- silent fallback to `<pad>`;
- silent fallback to `UC`;
- dropping unknown labels.

Unknown or unmapped label:
`EXECUTION_FAILED:P2V2_GED_LABEL_NOT_IN_GEC_VOCAB`

## 10. GEC word-to-subword projection

For every morphology word:

1. tokenize that exact word using the frozen GEC tokenizer;
2. require >=1 GEC subword;
3. repeat the word's GED label NAME across all GEC subwords;
4. map each repeated label name through the frozen GEC `ged_label2id`;
5. persist word->GEC-subword range.

After adding required BOS/EOS:

Required equality:
`len(input_ids) == len(ged_label_ids) == len(attention_mask)`

Any mismatch:
`EXECUTION_FAILED:P2V2_GEC_CONDITIONING_LENGTH_MISMATCH`

## 11. Model-interface proof

P2_V2 MUST prove that the loaded GEC implementation actually consumes GED conditioning.

Before Stage 1:

- freeze exact Transformers/fork revision;
- freeze model class;
- freeze generation code hash;
- inspect/trace the forward/generate path;
- run a synthetic interface test in which only `ged_tags` changes while all other frozen inputs remain the same;
- prove the tags are accepted and reach the intended embedding/conditioning path.

A model accepting an unused keyword or silently ignoring GED conditioning is not acceptable.

Failure:
`EXECUTION_FAILED:P2V2_GED_TAG_INTERFACE_UNPROVEN`

This test proves interface use, not linguistic benefit.

## 12. Morphology identity

Freeze:

- morphology database/model;
- preprocessing code;
- normalization functions;
- input text hash;
- morphology output hash;
- ordered morphology words.

Record source->morphology relation.

Any source/morphology identity mismatch:
`EXECUTION_FAILED:P2V2_MORPHOLOGY_IDENTITY_FAILED`

No gold may repair morphology.

## 13. Effective generation configuration

Persist the FINAL effective generation configuration after merging model defaults and explicit overrides:

- decoder_start_token_id;
- bos_token_id;
- eos_token_id;
- pad_token_id;
- max_length and/or max_new_tokens;
- num_beams;
- num_return_sequences;
- no_repeat_ngram_size;
- early_stopping;
- length_penalty;
- forced_bos_token_id;
- forced_eos_token_id;
- any other non-default generation option.

The artifact must distinguish configured values from inherited defaults.

## 14. Decoder prefix and terminal EOS

If decoder_start_token_id equals EOS, the decoder prefix MUST NOT be treated as terminal natural EOS.

Persist:

- raw generated token IDs including prefix;
- prefix length;
- first terminal EOS searched only after the known prefix;
- whether EOS is natural, forced-at-limit, or absent.

Missing/unknown terminal semantics:
`EXECUTION_FAILED:P2V2_TERMINAL_EOS_UNPROVEN`

## 15. GEC input length / truncation

GEC tokenization must explicitly disable silent truncation unless a separately frozen contract defines it.

Record full pre-special and post-special lengths.

If the input cannot be represented under the frozen GEC model limit:

`EXECUTION_FAILED:P2V2_GEC_INPUT_TOO_LONG`

Do not split and stitch GEC outputs under this contract.

Any such alternative requires a NEW contract/version.

## 16. Batch/order/repeat identity

Stage 0/1 tests MUST compare:

- single inference;
- batch inference;
- reordered batch inference;
- repeated identical inference.

Equality is required not only for final text but for:
- morphology words;
- GED segment mapping;
- GED retained prediction indices;
- word-level labels;
- GEC input IDs;
- GEC GED-label IDs;
- generated token IDs;
- final output bytes.

Any nondeterminism is recorded and triaged before Stage 1 eligibility.

## 17. Required synthetic boundary tests

In addition to the earlier P2_V2 tests, mandatory B01 closure tests are:

S-B01-01 zero GED-token word -> explicit failure, no shift.
S-B01-02 zero GEC-token word -> explicit failure.
S-B01-03 one word exactly fits effective GED content budget -> PASS.
S-B01-04 one word exceeds effective GED content budget by one -> FAIL.
S-B01-05 segment reaches exact total configured length including specials -> PASS.
S-B01-06 next complete word would overflow -> starts new segment without loss.
S-B01-07 duplicate word index on reconstruction -> FAIL.
S-B01-08 missing word index -> FAIL.
S-B01-09 reordered word indices -> FAIL.
S-B01-10 equal total counts but wrong identity assignment -> FAIL.
S-B01-11 GED label known in GED but absent from GEC map -> FAIL.
S-B01-12 modified label numeric IDs with same names -> NAME-based remap remains correct.
S-B01-13 GEC conditioning length mismatch -> FAIL.
S-B01-14 ged_tags accepted but not consumed by model path -> FAIL.
S-B01-15 decoder prefix equals EOS -> not counted as terminal EOS.
S-B01-16 forced EOS at length ceiling -> recorded distinctly and default fail-closed.
S-B01-17 batch reorder preserves UID/word identity.
S-B01-18 repeated run produces byte-identical trace under frozen deterministic runtime.

## 18. Stage eligibility

B01 is considered CLOSED only when:

- this contract is frozen;
- implementation self-tests cover all mandatory cases;
- all tests PASS;
- exact implementation/model/tokenizer/config hashes are frozen;
- independent review of B01 closure finds no BLOCKER.

Until then:
- synthetic implementation work is allowed;
- Stage 1 project-source execution is forbidden.

## 19. Scientific boundary

This contract proves identity/provenance only.

It does not prove:
- GED accuracy;
- morphology usefulness;
- GEC correctness;
- candidate quality;
- R_joint;
- safe repair.

No gold/reference is permitted.
