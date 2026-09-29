# Phase 2 — CamelParser Dependency Mapping Smoke Protocol

Date: 2026-09-29
Status: PRE-REGISTERED SMOKE TEST; NO QALB DATA

## Objective

Validate a pinned CamelParser runtime and determine a deterministic mapping strategy before running any dependency diagnostic on consumed QALB evidence.

## Pinned parser

- CAMeL-Lab/camel_parser
- commit: 66f29f7e34e3b5b38780d08bd56cf481635bf1c6
- Python: 3.11.13
- model: CATiB
- morphology/disambiguation: default r13 + BERT where applicable

## Synthetic input only

Use fixed non-QALB Arabic sentences created solely for runtime testing.

Run both:
1. preprocessed_text
2. tokenized

## Required outputs

Persist:
- parser commit/runtime versions;
- number of whitespace input tokens;
- number of produced dependency tokens;
- treeTokens sequence hash;
- CoNLL column count/well-formedness;
- whether tokenized mode preserves exact supplied token sequence;
- whether preprocessed_text mapping to whitespace tokens is uniquely recoverable using parser output metadata.

Synthetic sentence text may be logged, but no QALB text may enter this workflow.

## Decision

- If a deterministic mapping exists: proceed to label-blind dependency feature materialization on consumed evidence.
- If mapping is ambiguous: do not build a dependency policy; first solve mapping or use a safer parser input representation.

No Phase 3. No sealed benchmark. No QALB15 TEST.
