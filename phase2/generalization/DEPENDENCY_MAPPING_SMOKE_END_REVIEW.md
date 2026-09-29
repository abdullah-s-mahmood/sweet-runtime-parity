# Phase 2 — CamelParser Dependency Mapping Smoke End Review

Date: 2026-09-29

## Canonical successful run

- Workflow: Phase 2 CamelParser Dependency Mapping Smoke
- Successful run: 36522675709
- Parser: CAMeL-Lab/camel_parser
- Pinned commit: 66f29f7e34e3b5b38780d08bd56cf481635bf1c6
- Python: 3.11.13
- torch: 2.0.1
- camel-tools: 1.5.6
- transformers: 4.29.2
- QALB data read: no
- QALB15 TEST read: no

The first smoke run 36522571985 failed before parsing because camel-kenlm required system Boost development libraries. The repair added only cmake/libboost-all-dev; parser/data/protocol were unchanged.

## Mapping result

Two fixed synthetic Arabic sentences were tested.

### tokenized mode

Input token counts:
- sentence 1: 7 -> 7 parser tokens
- sentence 2: 8 -> 8 parser tokens

Exact supplied token sequence preservation:
- sentence 1: true
- sentence 2: true
- all sentences: **true**

### preprocessed_text mode

Input token counts:
- sentence 1: 7 -> 8 parser tokens
- sentence 2: 8 -> 9 parser tokens

The extra tokens are consistent with clitic-aware CAMeL preprocessing. Therefore raw whitespace index cannot be treated as a parser-token index.

## Code-level interpretation

CamelParser's preprocessed_text path performs contextual disambiguation and feature extraction before parsing. It supplies token FORM, LEMMA, CATiB POS and rich morphology to the dependency parser.

The tokenized path preserves supplied tokens but constructs parser tuples with lemma "_" and POS "UNK".

## Decision

**Use preprocessed_text for dependency diagnostics, but never by direct positional indexing.**

The accepted mapping method is:
1. contextual-disambiguate the whitespace-tokenized sentence using the same parser disambiguator;
2. run the same CamelParser per-word feature extraction;
3. accumulate each whitespace word's emitted parser-token span;
4. assert the reconstructed emitted token sequence equals the parser input sequence after the same normalization;
5. fail closed if the equality assertion fails.

This preserves rich CATiB/morphology evidence while maintaining deterministic target alignment.

The mapping smoke is therefore **PASS** for dependency feature research.

No correctness or auto-accept claim follows from this smoke test.
