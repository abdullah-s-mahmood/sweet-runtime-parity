# AT0-EN V2.4 — Gate B1 Human-Correct Graph Alignment Contract V1

Date: 2026-10-03
Status: FROZEN PRE-IMPLEMENTATION / DEVELOPMENT-ONLY

## Purpose

B1 evaluates alignment mechanics independently from extraction quality by using human-correct source and candidate assertion graphs.

No source or candidate extractor output is used in the first B1 score.

## Required alignment capabilities

The aligner must support:
- 1:1
- 1:N
- N:1
- mixed mappings
- preserved meaning
- altered relation ownership
- contradiction
- omission
- unsupported new information
- uncertainty propagation

## Non-negotiable semantics

The aligner must preserve/check:
- subject/object ownership
- metric/value/unit ownership
- time
- population/group
- baseline
- scope
- polarity/negation
- modality
- causality
- citation binding
- equation/symbol binding
- procedural order/dependency

A single critical wrong relation is non-compensatory.

Similarity or lexical overlap may only retrieve candidate matches; it cannot by itself produce PRESERVED or PASS_CANDIDATE.

## Uncertainty rule

If any critical input assertion or relation involved in an alignment is UNCERTAIN/AMBIGUOUS:
- the corresponding alignment cannot be promoted to fully certain preservation solely because the two graphs agree;
- unresolved critical uncertainty must remain visible and normally produce REVIEW.

`UNCERTAIN + UNCERTAIN != CERTAIN`.

## Gold-pair set

A fixed development-only set will contain human-correct source/candidate graphs covering:
- faithful 1:1 paraphrase;
- faithful 1:N split;
- faithful N:1 merge;
- relation/value/metric rebinding;
- scope/negation change;
- citation binding change;
- equation/symbol binding change;
- procedural-order change;
- ambiguous alignment.

The set is diagnostic and synthetic.
It is not an untouched holdout and does not establish generalization.

## Pre-registered B1 hard gates

Because graph inputs are human-correct and the set is intentionally small/mechanical:

1. Critical dangerous false-preserve:
   - requirement: **0**

2. Pair-level expected outcome:
   - requirement: **100%**
   - every PASS_CANDIDATE / REJECT / REVIEW pair must be classified correctly.

3. Critical gold alignment coverage:
   - requirement: **100%**

4. Critical alignment-status accuracy:
   - requirement: **100%**

5. Faithful safe-pair rejection:
   - requirement: **0**

6. Material adversarial pair acceptance:
   - requirement: **0**

7. Critical uncertainty preservation:
   - requirement: **100%**

Failure of any hard gate blocks progression from gold-graph mechanics to extracted-graph alignment.

## Secondary diagnostics

Report:
- alignment status counts;
- mapping-shape performance separately for 1:1 / 1:N / N:1 / mixed;
- false preserve;
- false alter/reject;
- missed omission/new-information;
- confidence propagation;
- evidence-trace completeness;
- per-family errors.

Secondary metrics cannot compensate for a hard-gate failure.

## Development stop rule

After the first B1 alignment score:
- freeze all failures;
- any repair is versioned;
- do not rewrite the human-correct graphs merely to match the aligner unless a genuine annotation defect is independently demonstrated;
- do not advance to extracted graphs until B1 hard gates pass.

## Scope exclusions

B1 does NOT authorize:
- candidate extraction;
- extracted-graph alignment;
- live generation;
- HW1-EN;
- untouched holdout creation;
- authentic-document integrated claims;
- end-to-end V2.4 safety claims.
