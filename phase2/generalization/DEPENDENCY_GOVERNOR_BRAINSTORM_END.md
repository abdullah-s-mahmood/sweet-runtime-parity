# Dependency/Governor Diagnostic — Brainstorm End

Date: 2026-09-29

| Candidate signal | Observed on 14 | Decision |
|---|---:|---|
| Any dependency structural change | 10/12 supported, 0/2 partial | DROP as risk signal |
| Unchanged + OBJ | 0/12 supported, 2/2 partial | OVERFIT-RISK; do not promote |
| NOM + OBJ | 0/12 supported, 2/2 partial | OVERFIT-RISK; do not promote |
| OBJ headed by root VRB | separates partials with extra conjunctions | OVERFIT-RISK; semantically too broad |
| source CATiB PROP to candidate NOM | 10/12 supported, 0/2 partial | TEST RETROSPECTIVELY |
| candidate NOM alone | 14/14 | non-discriminative |

## Why PROP to NOM is preferable for the next test

The frozen V1 morphology gate already requires noun-to-noun identity under CAMeL contextual morphology. CATiB PROP to NOM therefore supplies a differently encoded lexical-category normalization signal: the candidate becomes recognizable as an ordinary noun in the parser representation while the source looked proper/unknown-like.

This may be a useful positive proof component for orthographic normalization, but it may also simply reflect parser sensitivity to spelling. It must be replicated.

## Next test

Pre-register CATIB_PROP_TO_NOM_EVIDENCE_V1 and apply it label-blind to the earlier consumed 36-event ORTHO_MORPH_COMMON_NOUN_V1 population:
- 34 supported;
- 2 partial;
- V1 isolated subset: 19 supported.

No rule tuning after features are materialized.
