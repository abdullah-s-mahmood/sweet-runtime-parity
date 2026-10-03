# AT0-EN V2.4 — Gate B1 Human-Correct Reference Freeze Closure

Date: 2026-10-03
Status: CLOSED CHECKPOINT / REFERENCE FROZEN / ALIGNER NOT YET IMPLEMENTED

## Purpose

This checkpoint freezes the human-correct graph reference and scoring contract for B1 before any alignment-engine implementation.

No model inference occurred.
No source/candidate extractor output was used.
No aligner has been implemented or scored yet.

## Frozen run identity

Workflow:
`AT0-EN V2.4 B1 Reference Integrity`

Run:
`37145151369`

Trigger commit:
`ff4173729d94bf90217ac05d986846cd58eeaacd`

Artifact:
- id: `11281568714`
- SHA-256: `ba404b99186582a259f683736f0018832bf09f34a71f6dc247cd8ef2a4bfcaaf`

## Integrity result

Status:
**PASS**

Checks:
**363**

Pairs:
**12**

Expected outcomes:
- PASS_CANDIDATE: 5
- REJECT: 6
- REVIEW: 1

Mapping shapes:
- ONE_TO_ONE: 7
- ONE_TO_MANY: 2
- MANY_TO_ONE: 2
- MIXED: 1

Human-correct graph counts:
- source assertions: 19
- candidate assertions: 19
- source relations: 6
- candidate relations: 6

Assertion-alignment gold statuses:
- PRESERVED: 7
- ALTERED: 8
- CONTRADICTORY: 1
- UNCERTAIN: 1

Relation-alignment gold statuses:
- PRESERVED: 3
- ALTERED: 2
- CONTRADICTORY: 1

Uncertain REVIEW pair:
`B1-P10`

## Frozen identities

- alignment schema SHA-256:
  `49935f5ea0de2e972c7bb7b557f4b477dbd72caed6cd7dd066117da6761f5a3a`

- scoring contract SHA-256:
  `385581867da42c6e0a13f1031ccf96787740bc2233cd25ec7b98c484fcbc42e1`

- human-correct pair set SHA-256:
  `29f3790859c8da6baf65db8b0fb372bc881e25d8e3d1e76b9c67b74d49944dca`

- integrity checker SHA-256:
  `1d4b9e68760cc07790283ae7dcf148c424baa5438d58f63e79e1a55acee0e539`

- integrity summary SHA-256:
  `6e91b9f98ea549994929e6988d1b3f2bc75daa3fcdc3987c784f702eccb9568d`

## Important design repair before freeze

The first B1 alignment schema represented assertion-level gold mappings but did not independently represent relation-level gold mappings.

This was repaired before the pair set was frozen by adding:
`gold_relation_alignment`

Reason:
citation, procedural-order, and other graph-edge failures must be independently measurable even when assertion text remains preserved.

Final schema therefore tests both:
- assertion alignment;
- relation alignment.

## Scenario coverage

The 12-pair set covers:
- faithful paraphrase;
- faithful 1:N split;
- faithful N:1 merge;
- value/group relation rebinding;
- scope/negation reversal;
- citation-binding swap;
- equation/symbol rebinding;
- procedural-order reversal;
- metric-definition change;
- ambiguity/uncertainty propagation.

This is a development mechanics set, not an untouched benchmark.

## Pre-registered hard gates for the future aligner score

Before progression to extracted graphs:

- critical dangerous false-preserve: **0**
- pair-level outcome accuracy: **100%**
- critical gold alignment coverage: **100%**
- critical alignment-status accuracy: **100%**
- safe faithful pair rejection: **0**
- material adversarial pair acceptance: **0**
- critical uncertainty preservation: **100%**

These thresholds are intentionally strict because B1 inputs are human-correct graphs.

## End-stage research / red-team

Fresh literature review reinforces the B1 design:

- decomposition quality and verifier performance can be misaligned; alignment must be evaluated directly;
- event relations such as coreference, temporal, causal, and hierarchy/subsumption remain difficult even for modern models;
- uncertainty should remain tied to evidence conflicts/agreements rather than be silently erased;
- graph-inspired factuality methods can be useful, but graph structure alone does not guarantee correct semantic alignment.

Therefore:
- do not collapse relation errors into a single aggregate similarity score;
- do not let many correct alignments compensate for one critical wrong relation;
- preserve uncertainty explicitly;
- keep relation-level gold separate from assertion-level gold.

## Quality delta

End-to-end scientific-fidelity performance:
**UNCHANGED**

Last full verifier result remains:
- adversarial escape: 37.5%
- safe automatic acceptance: 25%
- BOTH_FAIL

B1 performance:
**NOT YET MEASURED**

Methodological status:
**IMPROVED**

The improvement is in test validity and isolation of alignment mechanics, not in system performance.

## Completion

B1 reference-freeze checkpoint:
**100% COMPLETE**

Gate B1 overall:
**approximately 45% complete**

Whole ACAD_PASS:
**approximately 27% ±5% complete** as a planning estimate.

## Exact next authorized checkpoint

`AT0-EN V2.4 GATE B1 — ALIGNER IMPLEMENTATION + FIRST HUMAN-CORRECT GRAPH SCORE`

Next checkpoint scope:
- implement alignment mechanics only;
- use the frozen human-correct graphs;
- no model inference initially;
- support 1:1 / 1:N / N:1 / mixed;
- score assertion and relation alignment separately;
- preserve uncertainty;
- produce traceable evidence for every critical alignment;
- run one first score against the frozen B1 contract;
- freeze all failures before repair.

Not authorized:
- extracted-graph alignment;
- candidate extraction;
- live generation;
- HW1-EN;
- untouched holdout;
- production claims.

Higher-model consultation is not required at aligner implementation start unless a new construct-validity issue appears.
