# ACAD_PASS — SURUS Coordinate Mismatch Diagnostic Freeze V1

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

Run:
`37914600126`

Workflow:
`Federation SURUS coordinate mismatch diagnostic`

Conclusion:
`SUCCESS`

Artifact:
`11609690713`

Artifact digest:
`sha256:02c42a9e2439f555636c611875c4c7b5a055bdb8f6e93b4d2052d9dc95c1873b`

Classification:
`READ_ONLY_AGGREGATE_DIAGNOSTIC / NO_SCIENTIFIC_ATTEMPT_CONSUMED`

No raw text, PMID values, protected IDs, scientific metrics, protected evaluation, or model fit were emitted.

## Exact result

Total released annotations:
`48,833`

Exact `Abstract[start:end]` half-open matches:
`44,643`

Mismatch rows:
`4,190`

Mismatch rate:
`8.5802633465%`

Mismatch mechanism:
- annotation text has no exact occurrence anywhere in released Abstract: 4,113;
- one exact occurrence elsewhere in Abstract: 45;
- multiple exact occurrences in Abstract: 32;
- exact Title half-open at released coordinates among mismatch rows: 0;
- simple Unicode/HTML/whitespace normalization of the released offset slice rescued: 0;
- tested simple Title+separator+Abstract coordinate models rescued: 0.

Among the 45 unique-occurrence rows, offset differences are usually small but they explain only a tiny minority of the 4,190 mismatch rows.

Mismatch distribution:
- Indomain: 3,873
- indication OOD: 256
- study-type OOD: 61

EvalType:
- Train: 3,518
- Test: 672

Mismatch occurs across many LabelIDs and is not isolated to one entity class.

## Interpretation

The dominant mismatch mechanism is NOT:
- a universal inclusive-vs-exclusive end convention;
- a simple Title coordinate origin;
- a simple Title+Abstract concatenation;
- a simple whitespace/Unicode/HTML normalization;
- a universal one- or two-character offset.

The strongest current hypothesis is:
`ANNOTATION_TEXT_SOURCE_VERSION_OR_SERIALIZATION_MISMATCH_FOR_A_SUBSET_OF_RELEASED_RECORDS`

This is not yet proven.

Do NOT:
- drop 4,190 rows;
- snap boundaries;
- replace annotation Text with current article slices;
- train on rows lacking exact source-text recoverability;
- silently classify the full release as coordinate-certified.

## Next authorized operation

`SURUS_COORDINATE_MISMATCH_ARTICLE_LEVEL_AND_FIELD_DIAGNOSTIC_V2`

It must remain aggregate-only and determine:
- number of affected articles;
- per-article mismatch concentration;
- whether affected articles are fully or partially mismatched;
- exact/normalized occurrence in any other released textual field;
- whether mismatch correlates with Dataset/EvalType;
- whether TokenStart/TokenEnd provide a reproducible released-text reconstruction signal;
- whether a deterministic, source-documented subset can be certified without performance visibility.

No P2 adapter closure until P1 source-coordinate policy is frozen.
