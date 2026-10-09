# ACAD_PASS — Federation Real Tokenizer/Windowing Preflight Freeze V1

Date: 2026-10-09

State:
`FEDERATION_REAL_TOKENIZER_OFFSET_WINDOWING_PREFLIGHT_PASS`

Run:
`37890868248`

Artifact:
`11597948931`

Digest:
`sha256:55e3bef05c3246660c187e9c190807d075203f77cef21543500073ad5c1a6397`

Scientific training:
`FALSE`

Benchmark test used:
`FALSE`

Gold labels consumed:
`FALSE`

Source:
`EBM-NLP_mod fold1/train.txt`

Source documents:
`400`

## BASE — BiomedBERT-base

Revision:
`d673b8835373c6fa116d6d8006b33d48734e305d`

Tokenizer:
`BertTokenizerFast`

Documents:
400

Source words:
41,087

Wordpieces:
43,342

Windows:
400

Documents requiring >1 window:
0

Maximum source words/document:
339

Maximum wordpieces/document:
350

Tokenizer-empty source words:
17

Policy:
all 17 are retained through explicit UNK representation; none are dropped.

Oversized single-word failures:
0

Full source-word coverage:
true

Deterministic rerun:
true

Fixture digest:
`bc8e9c9259345491f1c206cc7e6e24c7b2e1fea1d63606b87698a673301d8091`

## MODERN — BioClinical ModernBERT-base

Revision:
`c3648aa87af95837c809e6f0c5f85d08160db437`

Tokenizer:
`PreTrainedTokenizerFast`

Documents:
400

Source words:
41,087

Wordpieces:
54,485

Windows:
400

Documents requiring >1 window:
0

Maximum wordpieces/document:
443

Tokenizer-empty source words:
17

Oversized single-word failures:
0

Full source-word coverage:
true

Deterministic rerun:
true

Fixture digest:
`91b1687b3a0348c24204f7825cfa242e53ab6da28f5d85041d3da3eb012ad337`

## PICOX — BiomedBERT-large

Revision:
`f18ff5ec008285849e7c467b2618262b0def6238`

Tokenizer:
`BertTokenizerFast`

The tokenizer/windowing identity equals BASE for this exposed source:
fixture digest
`bc8e9c9259345491f1c206cc7e6e24c7b2e1fea1d63606b87698a673301d8091`.

## Interpretation

The frozen text-only preprocessing contract is executable with the real pinned tokenizers and does not require gold-dependent chunk boundaries.

For this EBM-NLP_mod development source, every document fits inside one allowed content window for all three encoders. Therefore the historical gold-dependent chunking defect does not need to be reproduced for this development source.

This closes F03 for source-word/tokenizer/window coverage.

Remaining runtime work is GPU/model execution, not tokenizer identity.

No scientific model fit is authorized by this PASS.
