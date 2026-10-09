# ACAD_PASS — SURUS Token Width / Local Shift Diagnostic Freeze V7

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

Run:
`37919734516`

Conclusion:
`SUCCESS`

Artifact:
`11611114778`

Artifact digest:
`sha256:fbedf6dbdb16c0d8bffca3a859a2f1db11fd4ae9834eeeb8e8c0c4212aef5970`

Classification:
`READ_ONLY_SOURCE_INDEX_SEMANTICS_DIAGNOSTIC / NO_SCIENTIFIC_ATTEMPT_CONSUMED`

## Purpose

Test whether SURUS TokenStart/TokenEnd preserve source-token span WIDTH even though their absolute indices do not globally match candidate source segmentations.

No new tokenizer family was introduced.

Fixed source-unit candidates:
- BERT_PRETOKENIZER
- deterministic REGEX_WORD_PUNCT

## Character span alignment

BERT_PRETOKENIZER:
- aligned = 48,336
- unaligned = 497

REGEX_WORD_PUNCT:
- aligned = 48,483
- unaligned = 350

## Token-span width semantics

### BERT pre-tokenizer

Released inclusive width:
`TokenEnd - TokenStart + 1`

matches the char-derived source-unit span width for:
`42,242 / 48,833 = 86.5030%`

Among char-aligned rows:
`42,242 / 48,336 = 87.3924%`

Released exclusive width:
`TokenEnd - TokenStart`

matches only:
`1,205 / 48,833 = 2.4676%`

### REGEX word+punctuation

Inclusive width matches:
`42,419 / 48,833 = 86.8654%`

Among char-aligned rows:
`42,419 / 48,483 = 87.4925%`

Exclusive width matches:
`1,118 / 48,833 = 2.2894%`

Therefore:
`TOKEN_WIDTH_STRONGLY_SUPPORTS_INCLUSIVE_END_SEMANTICS`

but not a recoverable absolute token origin.

## Absolute shift structure

For inclusive-width-matching rows, define:
`shift = released TokenStart - char-derived source-unit start index`.

REGEX_WORD_PUNCT:
- shift 0 = 12,585 rows
- shift +1 = 3,714
- shift +2 = 2,774
- shift -2 = 2,665
- many additional positive and negative shifts occur.

BERT_PRETOKENIZER:
- shift 0 = 12,155
- shift +1 = 3,528
- shift +2 = 3,133
- shift -2 = 2,449
- many additional shifts occur.

Article-level structure:

REGEX_WORD_PUNCT:
- articles with one observed shift = 22
- articles with multiple observed shifts = 501
- articles with zero inclusive-width match = 0

BERT_PRETOKENIZER:
- articles with one observed shift = 21
- articles with multiple observed shifts = 502
- articles with zero inclusive-width match = 0

Thus:
`SIMPLE_DOCUMENT_LOCAL_OFFSET_HYPOTHESIS = REJECTED`

The released token fields are not explained by one global or per-document index shift.

## Interpretation

The strongest source-index interpretation now supported is:

1. TokenStart/TokenEnd likely encode inclusive token-span width information for a tokenization related to word/punctuation units.
2. Their absolute origin/segmentation cannot be reconstructed from the public release, linked code, BERT WordPieces, BERT pre-tokenization, regex word/punctuation segmentation, or whitespace segmentation.
3. They therefore MUST NOT be used to relocate or repair released character spans.
4. Start/End remain the strongest machine-readable released boundary representation.
5. The interrupted higher-model concern remains valid: wordpiece-boundary coherence is not identical to certification of the frozen ACAD_PASS source-word span unit.

## Current scientific boundary

No local authority exists to change the prior review requirement.

P1 remains:
`NOT_CLOSED`

SURUS scientific fitting remains:
`NO-GO`

Exact next governance operation:
`UPDATED_LIMITED_HIGHER_MODEL_SOURCE_CONTRACT_REREVIEW`

The updated packet must include V5-V7 and explicitly distinguish:
- released char-coordinate authority;
- unrecoverable released token-index absolute semantics;
- frozen ACAD_PASS source-word representation requirements;
- whether a prospectively fixed SURUS-specific source-unit adapter is scientifically permissible.
