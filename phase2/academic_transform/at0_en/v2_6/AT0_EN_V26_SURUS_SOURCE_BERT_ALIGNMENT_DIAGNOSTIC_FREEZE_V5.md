# ACAD_PASS — SURUS Source BERT Alignment Diagnostic Freeze V5

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

Run:
`37919107413`

Workflow:
`Federation SURUS source BERT tokenizer alignment diagnostic`

Conclusion:
`SUCCESS`

Artifact:
`11611123584`

Artifact digest:
`sha256:2d43434d6ecbd33e270a423d4e29300cd75d970353bc5e782f32bdeeaf6da51f`

Classification:
`READ_ONLY_SOURCE_TOKENIZER_DIAGNOSTIC / NO_SCIENTIFIC_ATTEMPT_CONSUMED`

## Source-tokenizer basis

The SURUS publication explicitly states that abstracts were tokenized using the BERT tokenizer and links `bert-base-uncased`.

For source reconstruction only, V5 pinned:
`google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`

This immutable revision predates the first public SURUS preprint.

The publication itself did NOT pin an exact tokenizer revision, so this is a reproducible source-reconstruction diagnostic, not proof of historical binary identity.

Tokenizer signature:
`80f508e1bf2096e323a95d5cf6f4105cdbb380b7d0df52b62118cb988897a130`

## Character boundary result

Released annotations:
`48,833`

Start/End spans aligning exactly to bert-base-uncased WordPiece boundaries:
`48,719 / 48,833 = 99.7666%`

Not aligned:
`114 / 48,833 = 0.2334%`

This is slightly stronger structural alignment than the future ACAD_PASS BiomedBERT tokenizer V4 result:
`48,640 / 48,833 = 99.6048%`.

## Released TokenStart/TokenEnd result

Eight fixed conventions were tested:
- 0/1 based;
- inclusive/exclusive end;
- with/without one special-token shift.

No convention recovered the released token pairs.

Best exact token-pair/char-span agreement:
`BASE0_INCLUSIVE_SPECIALSHIFT0 = 279 / 48,833`

The same convention reconstructed Annotation.Text exactly in only:
`403 / 48,833`

Thus:
`TOKENSTART_TOKENEND_ARE_NOT_DIRECT_BERT_BASE_UNCASED_WORDPIECE_INDICES`

## Index-delta structure

Under the best WordPiece convention, start/end deltas are not random one-off differences; recurrent negative deltas such as approximately -17 through -62 occur across hundreds of rows.

This pattern is consistent with released token indices using a coarser token unit than WordPiece, but does not prove which one.

## Interpretation

V5 closes one hypothesis:
`DIRECT_BERT_WORDPIECE_INDEX_SEMANTICS = REJECTED`

It does NOT reject:
- BERT pre-token / basic-token indexing;
- annotation-platform token indexing;
- another deterministic word/punctuation tokenization preceding WordPiece.

The published paper's wording about a BERT tokenizer does not distinguish these released CSV field semantics.

## Exact next operation

`SURUS_BERT_PRETOKEN_SOURCE_UNIT_DIAGNOSTIC_V6`

Test:
1. bert-base-uncased backend pre-tokenizer offsets;
2. deterministic regex word/punctuation tokens;
3. whitespace tokenization;

against released TokenStart/TokenEnd and Start/End.

No raw text/IDs emitted.
No repair.
No training.
No protocol change.
