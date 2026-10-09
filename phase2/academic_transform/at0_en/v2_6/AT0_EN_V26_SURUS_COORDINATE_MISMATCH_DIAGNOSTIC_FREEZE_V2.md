# ACAD_PASS — SURUS Coordinate Mismatch Article/Field Diagnostic Freeze V2

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

Run:
`37914932110`

Workflow:
`Federation SURUS coordinate mismatch diagnostic`

Conclusion:
`SUCCESS`

Artifact:
`11608697424`

Artifact digest:
`sha256:69c688f51996eda49cbb09175f5adcede785efcf99ef0d1fca50f97b46f76d83`

Classification:
`READ_ONLY_AGGREGATE_DIAGNOSTIC / NO_SCIENTIFIC_ATTEMPT_CONSUMED`

## Main result

Released annotations:
`48,833`

Mismatch rows:
`4,190`

Affected articles:
`437 / 523`

Articles with zero mismatches:
`86`

Fully mismatched articles:
`0`

Partially mismatched articles:
`437`

This materially weakens the hypothesis that the dominant problem is a wholly different article version. Every affected article still contains at least some exact source-coordinate annotations.

## Released field search

Among the 4,190 mismatch rows:
- exact annotation Text occurs somewhere in released Abstract: 77;
- exact annotation Text occurs somewhere in released Title: 1;
- no occurrence in released Title/Abstract/Indication/ArticleType: 4,113.

Simple NFKC/HTML/whitespace normalization did not expand the 77/1 occurrence counts.

Whitespace-token coordinate reconstructions explained only 1 row under tested 0/1-based inclusive variants.

## Similarity at released character offset

Most mismatch rows remain highly similar to the current `Abstract[start:end]` slice:

- similarity 0.95–0.99: 1,179
- 0.90–0.95: 1,374
- 0.75–0.90: 1,525
- 0.50–0.75: 79
- <0.50: 23

Annotation-minus-offset-slice length difference is strongly positive:
- +2 characters: 2,154 rows
- +1 character: 1,049 rows
- +3 characters: 322 rows
- +4 characters: 286 rows
- +5 characters: 120 rows
- +6 characters: 96 rows

This supports a row-level text reconstruction/spacing hypothesis more strongly than a whole-document version mismatch.

## Domain distribution

Affected articles:
- Indomain: 395
- indication OOD: 37
- study-type OOD: 5

Mismatch rows:
- Indomain: 3,873
- indication OOD: 256
- study-type OOD: 61

EvalType:
- Train mismatch rows: 3,518
- Test mismatch rows: 672

## Scientific interpretation

Current strongest hypothesis:
`ANNOTATION_TEXT_EXPORT_OR_TOKEN_RECONSTRUCTION_DIFFERS_FROM_RAW_RELEASED_ABSTRACT_FOR_PUNCTUATION/BOUNDARY_CASES`

This is not yet proven.

The peer-reviewed SURUS paper states that entity evaluation is based on token-start/token-end/label complete matches and that adjacent token labels were aggregated after BILOU processing. This makes token-reconstruction effects plausible, but does not authorize inventing a tokenizer or repairing release spans.

## Next authorized operation

`SURUS_COORDINATE_TOKEN_RECONSTRUCTION_DIAGNOSTIC_V3`

Test only prospectively defined, source-plausible text reconstructions such as punctuation-token spacing and, if necessary, paper-compatible BERT tokenization semantics.

Remain aggregate-only.

No row dropping, snapping, training, thresholding, or performance visibility.
