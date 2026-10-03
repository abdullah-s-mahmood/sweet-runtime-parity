# AT0-EN V2.4 — Higher-Model Consultation Response V1

Date: 2026-10-03
Role: independent Chief Architect / Research Reviewer
Verdict: PROCEED_WITH_CHANGES

## Top risks
1. Benchmark over-adaptation: replacing regex with graph templates derived from the same observed failures.
2. Shared source-extraction error: source and candidate can agree on the same wrong interpretation.
3. Decomposition can change meaning by detaching conditions, exceptions, or complex negation.
4. Context loss across pronouns, symbol definitions, prior sentences, or table headings.
5. Plausible but wrong alignment, especially metric/group/time swaps; excessive abstention can hide this failure by collapsing usability.

## Required architecture changes
1. Keep the graph small and relation-justified; no graph database or broad ontology.
2. Convert flat fields into explicit ownership relations; preserve raw expression; represent absolute/relative quantity, percent vs percentage-point, ranges/bounds, denominator, uncertainty and precision where material.
3. Represent operator scope and procedural structure explicitly: negation, hedging, evidence, causality, exceptions, AND/OR, quantifiers, proposed/implemented/observed/hypothetical status, step order/dependencies, claim-citation binding, equation-symbol-definition binding.
4. Preserve deterministic/semantic separation, but do not treat anchor ownership as deterministic just because token presence is deterministic. Semantic judgment cannot override deterministic failure. Sentence count is not a scientific invariant.
5. Extract source once per source version and freeze it before candidate extraction. Extract candidate independently. Alignment may jointly inspect both original texts/evidence after both extractions are frozen; it must not silently rewrite the candidate graph to match the source.
6. Add coverage checking independent of extractor self-confidence. Every assertion/relation must trace to source spans, and scientifically relevant uncovered spans/anchors must be accounted for.
7. Use bidirectional, many-to-many alignment. Similarity/embeddings retrieve candidates only; they never confer PASS. One critical wrong relation cannot be compensated by many correct ones.
8. Use four outcomes:
   - PASS_CANDIDATE
   - REJECT
   - REVIEW
   - INVALID_VERIFICATION
   INVALID_VERIFICATION is transaction-level failure, not a scientific judgment on the candidate.

## Minimum validation program
A. Freeze schema/critical fields/outcome rules and construct a small fixed human reference set.
B. Validate source/candidate extraction independently: coverage, false additions, atomicity, context, ownership, negation/hedge scope, provenance, and critical undetected extraction errors.
C. Validate relation alignment first with human-correct graphs, including faithful paraphrase, split/merge, lexical-preserving relation swaps and ambiguity.
D. Then evaluate alignment with extracted graphs on development data to measure propagation of extraction errors.
E. Freeze the complete pipeline and only then create a new independent end-to-end holdout with natural controls and adversarial transformations.
F. Keep preliminary gates at zero observed dangerous escapes and >=75% automatic safe-control acceptance; do not relax after failure.

## Do not
- patch by consumed holdout IDs;
- treat self-confidence or self-consistency as proof;
- leak expected source relations into candidate extraction;
- use similarity/NLI/model agreement as substitute for critical evidence;
- build full AMR/graph DB/large ontology before necessity is shown;
- start new generation or HW1-EN before the staged validation review.

## Final disposition
GO for a limited offline prototype and staged validation with these changes.
NO-GO for new generation or HW1-EN.
