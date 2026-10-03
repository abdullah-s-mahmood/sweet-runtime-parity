# AT0-EN V2.4 — B2.2 Hybrid Relation-Aware Prototype Freeze Closure

Date: 2026-10-03
Status: CLOSED CHECKPOINT / PROTOTYPE FROZEN / SYNTHETIC B2 REVALIDATION NOT STARTED

## Prototype decision

Architecture:
`HYBRID_RELATION_AWARE_EXTRACTION_REPAIR`

Frozen A2 extractor:
unchanged.

Frozen B1.1 aligner:
unchanged.

B2.2 adds a versioned relation-aware structured layer around A2.

## Implemented blocking capabilities

1. Predicate/paraphrase normalization
   - explicit reduce/lower normalization
   - explicit scientific predicates: DEFINE, AIM_TO, TREAT, USE_FOR, INTRODUCE
   - explicit modality preserved for purpose statements

2. Negation/scope ownership
   - explicit evaluated/not-evaluated scope
   - explicit negative DEFINE/TREAT/USE_FOR handling
   - non-causality statements kept distinct from positive causal claims

3. Owner/value and owner/meaning binding
   - group/time/value/unit ownership
   - split/merge quantitative normalization
   - run/iteration/seed ownership

4. Citation-to-claim binding
   - explicit CIT_* relations only
   - lexical claim-label resolution requires unique support

5. Equation/symbol/coefficient binding
   - supported explicit equations only
   - coefficient-to-variable ownership preserved
   - no claim of general algebraic equivalence

Additional preservation:
- explicit PRECEDES relation only when stated
- ambiguity remains REVIEW
- no generic coreference parser
- no broad semantic parser

## Principle regression result

Final regression run:
`37149645971`

Result:
**17/17 PASS**

Coverage includes:
- faithful paraphrase
- scope negation
- split/merge ownership
- swapped ownership rejection
- citation preservation and swap rejection
- equation binding and swap rejection
- ambiguity preservation
- five generic scientific predicate patterns
- modality preservation
- three negative-predicate red-team cases

No B1 pair IDs or gold mappings are read by the prototype.

## Authentic academic qualitative check

Final authentic run:
`37149698525`

Artifact:
- id: `11283396807`
- SHA-256: `63a4bfdfd62ca794a81323b45e295e75355dbbc3b04b57e10d32737ed2eebfb5`

Set:
5 short authentic academic excerpts from recent ACL/EMNLP literature.

Before explicit scientific predicate repair:
- CERTAIN: 0
- AMBIGUOUS: 5
- unsupported relations: 0

After repair:
- CERTAIN: 5
- AMBIGUOUS: 0
- UNCERTAIN: 0
- unsupported relations: 0

This is a qualitative development check only.
It is NOT a benchmark and authorizes no adoption percentage.

## Important red-team finding and repair

A final red-team regression found:
`The analysis does not treat ...`

was incorrectly parsed as positive TREAT with "does not" absorbed into the subject.

This was repaired before prototype freeze:
- explicit negative DEFINE/TREAT/USE_FOR patterns now preserve polarity;
- modal AIM_TO preserves MAY/CAN/COULD.

The final 17/17 regression run occurred after this repair.

## Research interpretation

Fresh research reviewed before and during B2.2 supports:
- structured scientific event/argument extraction rather than narrow entity-only representations;
- relation-aware cues for argument-role disambiguation;
- syntactic filtering/high-precision relations for scientific text;
- joint consideration of decomposition and verification;
- conservative handling of mathematical-symbol bindings.

The prototype therefore remains deterministic-first with abstention rather than broad semantic guessing.

## Current official performance

Canonical B2 performance is UNCHANGED until synthetic revalidation:

- GG: 100%
- GE: 41.67%
- EG: 50%
- EE: 33.33%
- EE safe acceptance: 0%
- EE adversarial acceptance: 0%
- REVIEW preservation: 100%
- canonical B2 verdict: MIXED_B2_REPAIR_REQUIRED

Do NOT replace these with prototype-regression or authentic-qualitative results.

## Strong-adoption ledger

- adversarial automatic acceptance:
  current canonical B2 = 0%
  strong target = 0%

- critical silent scientific errors:
  current measured development evidence = 0
  strong target = 0

- human-correct alignment:
  current = 100%
  target = 100%

- extracted-graph pair accuracy:
  current canonical B2 = 33.33%
  strong target = >=95%

- authentic in-domain safe automatic acceptance:
  current = NOT YET MEASURED
  strong target = >=90%

- automatic-PASS selective precision:
  current = NOT YET MEASURED end-to-end
  strong target = >=99%

- ambiguity preservation:
  current B2 = 100%
  target = 100%

## Completion

B2.2 prototype checkpoint:
**100% COMPLETE**

Gate B2 overall:
**approximately 90% complete**

Whole ACAD_PASS planning estimate:
**approximately 31% ±5%**

No whole-system performance improvement is claimed before revalidation.

## Exact next authorized checkpoint

`AT0-EN V2.4 B2.2 — FROZEN FOUR-ARM REVALIDATION WITH RELATION-AWARE PROTOTYPE`

Next scope:
- use the frozen B2.2 prototype on the same frozen raw-text pairs;
- keep GG/GE/EG/EE separate;
- keep the existing frozen B2 development gates unchanged;
- verify A1 anchor/provenance non-regression;
- audit critical relation support independently per side;
- freeze the first repaired B2 result before any further repair.

Not authorized:
- live generation
- HW1-EN
- untouched holdout
- production claims
