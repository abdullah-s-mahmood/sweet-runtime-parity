# ACAD_PASS — SURUS Source-Unit Diagnostic Freeze V6

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

Run:
`37919404071`

Conclusion:
`SUCCESS`

Artifact:
`11610764435`

Artifact digest:
`sha256:0ec7e0dc73a1096b51d9702f9ffba69613b5d9ab47b91a2ea206e5c2e65fdb2e`

Classification:
`READ_ONLY_SOURCE_UNIT_DIAGNOSTIC / NO_SCIENTIFIC_ATTEMPT_CONSUMED`

## Purpose

Test whether released SURUS TokenStart/TokenEnd refer to a coarser source-token unit rather than BERT WordPieces.

Fixed segmenters:
1. `BERT_PRETOKENIZER`
2. `REGEX_WORD_PUNCT`
3. `WHITESPACE`

No scientific model fitting, scoring, protected access, source repair, or row exclusion occurred.

## Character-span boundary alignment

Released annotations:
`48,833`

Start/End align exactly to source-unit boundaries:

- BERT pre-tokenizer: `48,336 / 48,833 = 98.9822%`
- deterministic word+punctuation regex: `48,483 / 48,833 = 99.2833%`
- whitespace tokens: `27,595 / 48,833 = 56.5089%`

Thus the released character coordinates are highly compatible with word/punctuation source units and poorly characterized by whitespace-only words.

## Released token-index recovery

Best fixed convention:
`BASE0_INCLUSIVE_SPECIALSHIFT0`

Exact released TokenStart/TokenEnd pair equals char-derived source-token span:

- REGEX_WORD_PUNCT: `12,585 / 48,833 = 25.7715%`
- BERT_PRETOKENIZER: `12,155 / 48,833 = 24.8910%`

Whitespace is far worse.

Therefore:
`TOKENSTART_TOKENEND_ARE_NOT_GLOBAL_INDICES_OF_THE_TESTED_SOURCE_UNITS`

## Important structure

For the two strongest source-unit segmenters, the start- and end-index delta distributions are strikingly similar.

This raises a narrower remaining hypothesis:

`RELEASED_TOKEN_INDICES_MAY_PRESERVE_SPAN_WIDTH_BUT_USE_LOCAL_OR_SHIFTED_INDEX_ORIGIN`

This can be tested without introducing another tokenizer or changing the protocol.

## Exact next operation

`SURUS_TOKEN_WIDTH_AND_LOCAL_SHIFT_DIAGNOSTIC_V7`

It must test:
- inclusive vs exclusive released token-span width;
- derived token-span width under BERT pre-tokenizer and deterministic word+punctuation segmentation;
- equality of start/end shifts;
- whether shifts are constant per article or vary within article;
- aggregate-only outputs.

No source repair.
No row dropping.
No scientific fit.
