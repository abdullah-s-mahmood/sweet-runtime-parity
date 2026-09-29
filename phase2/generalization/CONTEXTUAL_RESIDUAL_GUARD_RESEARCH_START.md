# Contextual Residual-Risk Guard — Research Start

Date: 2026-09-29

## Fresh research

- CamelParser2.0 provides Arabic dependency parsing plus POS and rich morphological features, demonstrating that structured morphosyntactic evidence is available for Arabic rather than relying only on semantic similarity.
- COCOGEC and RobustGEC show that GEC decisions can change under subtle context variation, reinforcing the need to treat context as a first-class correctness variable.
- Edit-level majority voting can reduce over-correction, but the ACAD_PASS tri-model result shows that consensus alone does not guarantee contextual completeness.

## Engineering choice

The first diagnostic intentionally starts with the already operational CAMeL BERT morphological disambiguator rather than introducing CamelParser2.0 immediately.

Reason:
- no new parser dependency is needed;
- the test can falsify whether a very narrow morphology-preserving orthographic lane exists;
- if this fails because syntactic relations remain unresolved, dependency parsing becomes the next justified escalation rather than an assumed solution.

CamelParser2.0 remains the preferred next structured-syntax candidate if V1 is insufficient.
