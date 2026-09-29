# Dependency/Governor Completeness — Research Start

Date: 2026-09-29

## Motivation

Fresh ORTHO_ISOLATED_COMMON_NOUN_V1 validation failed zero-partial safety (12/14 supported, 2 partial). The repaired post-edit/morphology diagnostic also failed its pre-registered promising criterion:
- fixed-point captured 1/16 unsafe and 0/4 wrong;
- morphology identity captured 4/16 unsafe and 2/4 wrong;
- no policy was eligible for fresh validation.

The remaining justified signal is syntactic relation/governor evidence.

## Fresh external research

CamelParser2.0 is an open-source Arabic dependency parser supporting CATiB and UD. Its pipeline can process raw/preprocessed text and produce tokenization, POS, rich morphology, and dependency parses. The current repository recommends Python 3.11.13.

Pinned research implementation:
- repository: CAMeL-Lab/camel_parser
- commit: 66f29f7e34e3b5b38780d08bd56cf481635bf1c6
- date: 2026-09-28
- parser backend: SuPar biaffine dependency parser
- default morphology: CALIMA MSA r13 / CAMeL Tools

Scientific use here is narrow: dependency evidence is a risk/completeness signal, not a correctness oracle.

## Immediate requirement

Before touching consumed QALB events, verify:
1. runtime reproducibility at the pinned commit;
2. CoNLL output shape;
3. tokenization behavior under preprocessed_text;
4. whether tokenized mode preserves whitespace-token alignment;
5. whether target-to-parser-token mapping can be deterministic without labels.

No acceptance rule will be defined until this smoke test is complete.
