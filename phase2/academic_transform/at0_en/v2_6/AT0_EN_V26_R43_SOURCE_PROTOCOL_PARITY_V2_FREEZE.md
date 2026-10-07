# ACAD_PASS R4.3/R4.4 — Corrected Source Protocol Parity V2 Freeze

Date: 2026-10-07
Status: PASS / CONFIRMS EXISTING R44 SOURCE SEMANTIC CONTRACT

## Identity
- Run: `37580279584`
- Conclusion: SUCCESS
- Artifact: `11464027321`
- Artifact digest: `sha256:86ca5a0efa626df59261884e70b95eea7cee8ee0f196f05b35d222c9bd1bfabe`
- Pinned TRAIN SHA256: `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`
- Source `evaluate.py` SHA256: `b9a527b5169a6f8683644d6bb8b826648fc364ee7d66aa7879c835be551f3c77`
- Source `utils_ner.py` SHA256: `dc79b18559c13be43e35e8b6765d72568fc5e9a9342ea64d8d44e3cac408fcce`
- Source-preprocessed TRAIN SHA256: `ae8e574ce0ad464c389c5a57aeb7e359362d6b3d86f4fb0974f1da9e6ef9b668`

## Correct source pipeline reproduction
This V2 audit uses:
1. the source's own `update_data_to_max_len(256)` preprocessing;
2. the pinned BiomedBERT tokenizer;
3. the actual combined token/GOLD/PRED `-lf` evaluator path used by `PICO_ner.py`.

The earlier run `37570558785` is superseded because it exercised `load_bio()` directly and retained newline characters in label keys.

## Inventory
Raw/current after tokenizer-empty removal:
- documents = 400
- blank-delimited sequences = 1576
- tokens = 41,070

Source-preprocessed:
- documents = 400
- sequences = 1576
- tokens = 41,070
- no additional max-length split inserted
- no empty-surface row remains.

Thus the 17 raw tokenizer-empty rows are removed by the source preprocessing and the current removal is compatible.

## Entity semantics
Official combined-file evaluator:
- P = 426
- I = 1326
- C = 181
- O = 1067
- total = 3000.

Independent manual strict B-start count is IDENTICAL:
- P = 426
- I = 1326
- C = 181
- O = 1067.

Legacy/current local-continuation parser on the same source-preprocessed input:
- P = 434
- I = 1328
- C = 181
- O = 1068
- total = 3011.

Exact delta:
- P +8
- I +2
- C +0
- O +1
- total +11.

The source-preprocessed input has exactly 11 example-initial I-X sequences:
- P = 8
- I = 2
- O = 1.

Therefore all 11 extra legacy entities are exactly continuation fragments, not source-compatible B-start entities.

## Decision
`SOURCE_PROTOCOL_PARITY_V2_PASS`

The existing future semantic contract remains correct:
- only B-X starts a SOURCE_COMPATIBLE entity;
- valid example-initial I-X is continuation metadata and must not add a new entity count;
- invalid initial I-X must be separately diagnosed;
- legacy R4.3 evidence is not retroactively rewritten.

This V2 result strengthens, rather than changes, R44's source semantics.

No DEV, test, other folds or protected data were opened; no model training occurred.
