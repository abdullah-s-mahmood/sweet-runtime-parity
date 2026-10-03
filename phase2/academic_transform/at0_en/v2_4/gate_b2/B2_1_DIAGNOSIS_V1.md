# AT0-EN V2.4 — B2.1 Extraction/Relation Representation Diagnosis V1

Date: 2026-10-03
Status: FROZEN DIAGNOSIS / NO REPAIR IMPLEMENTED

## Canonical B2 evidence

Canonical first B2 run:
`37147162271`

Canonical result:
`MIXED_B2_REPAIR_REQUIRED`

Primary EE metrics:
- pair accuracy: 4/12 = 33.33%
- safe automatic acceptance: 0/5 = 0%
- adversarial automatic acceptance: 0/6 = 0%
- REVIEW preservation: 1/1 = 100%
- critical uncertainty promotion: 0

Human-correct GG baseline:
- pair accuracy: 12/12 = 100%
- safe acceptance: 5/5 = 100%
- adversarial acceptance: 0/6

Therefore:
- EE pair-accuracy degradation: -66.67 pp
- EE safe-acceptance degradation: -100 pp
- safety degradation on adversarial acceptance: 0 pp

## Exclusive primary-cause classification of the 8 wrong EE pairs

### 1. Predicate/paraphrase/scope/decomposition coverage
Pairs:
- B1-P01
- B1-P03
- B1-P05
- B1-P12

Count:
4/8 wrong EE pairs = 50%
4/12 total pairs = 33.33%

Observed mechanisms:
- faithful paraphrases not mapped to known predicates;
- wrapper/context wording such as "denotes", "observed", "because", "cannot be claimed" becomes UNRESOLVED;
- explicit negation/scope reversal is routed to uncertainty rather than decisive contradiction;
- embedded non-causality wording is not decomposed into stable semantic roles.

### 2. Split/merge owner-to-value or owner-to-meaning binding
Pairs:
- B1-P02
- B1-P11

Count:
2/8 wrong EE pairs = 25%
2/12 total pairs = 16.67%

Observed mechanisms:
- one source assertion split into iterations + seed is not represented as canonical ownership-equivalent facts;
- merged quantitative candidate keeps values/groups lexically, but owner-to-value bindings are not explicitly preserved.

### 3. Missing explicit semantic relation extraction
Pair:
- B1-P06

Count:
1/8 wrong EE pairs = 12.5%
1/12 total pairs = 8.33%

Observed mechanism:
- citation evidence text is converted into ambiguous assertions rather than CITES edges;
- citation swap therefore becomes REVIEW rather than decisive REJECT.

### 4. Equation/symbol structured relation not represented semantically
Pair:
- B1-P07

Count:
1/8 wrong EE pairs = 12.5%
1/12 total pairs = 8.33%

Observed mechanism:
- equation and symbols survive as deterministic anchors;
- coefficient-to-variable ownership is not extracted as structured relation/binding;
- the equation swap therefore remains AMBIGUOUS and produces REVIEW rather than decisive REJECT.

## Source vs candidate extraction degradation

GE — gold source / extracted candidate:
- 41.67%

EG — extracted source / gold candidate:
- 50%

Candidate-side extraction is descriptively:
- 8.33 pp worse than source-side extraction on this fixed set.

EE:
- 33.33%

Interaction degradation:
- EE vs GE: -8.33 pp
- EE vs EG: -16.67 pp

These are descriptive fixed-set differences, not causal population estimates.

## Bridge diagnosis

Invalid bridge records:
0

The bridge:
- preserved available assertion fields;
- preserved explicit uncertainty;
- did not invent missing relations, as preregistered.

Conclusion:
**Bridge mechanics are not the primary repair target.**

The bridge intentionally exposes upstream representation deficiencies.

## Aligner diagnosis

GG remains:
100%

Therefore:
**B1.1 alignment mechanics are not the primary repair target.**

Do not tune the aligner to compensate for missing extraction semantics.

## Representation gap

The dominant missing capabilities are:

1. normalized scientific predicates across faithful paraphrases;
2. explicit operator scope / negation ownership;
3. canonical split/merge ownership facts;
4. explicit relations for citation, equation-symbol binding, procedure/order, and other material dependencies;
5. context-aware decomposition without forcing uncertain interpretations;
6. source/candidate symmetric extraction behavior.

## Architecture alternatives

### A. Patch current regex patterns case-by-case
Recommendation:
REJECT.

Reason:
would recreate V2.3 over-adaptation and consumed-case brittleness.

### B. Principle-based hybrid structured extraction layer
Candidate recommendation:
PREFERRED.

Concept:
- retain deterministic anchors/provenance;
- add deterministic high-precision relation constructors where syntax is explicit;
- add normalized predicate/operator representations;
- add canonical ownership facts;
- use abstaining semantic extraction only for non-deterministic paraphrase/context relations;
- preserve uncertainty and require evidence trace.

### C. Replace extraction with a broad generic AMR/SRL/LLM semantic parser immediately
Recommendation:
NOT YET.

Reason:
may add broad coverage but introduces a new shared semantic-error surface before the minimal scientific relation contract is validated.

## Strong-adoption targets carried forward

Project-defined targets:

- adversarial automatic acceptance: 0%
- critical silent scientific errors: 0
- critical uncertainty promotion: 0
- ambiguity preservation: 100%
- automatic-PASS selective precision: >=99%
- authentic in-domain safe automatic acceptance: >=90%
- extracted-graph pair decision accuracy before advanced adoption: >=95%
- critical relation/ownership correctness on controlled validation: 100%
- deterministic anchor precision/recall: 100% / 100%
- critical evidence/provenance completeness: 100%

These are ACAD_PASS project acceptance targets, not universal external standards.

## Research grounding

Fresh research is consistent with this diagnosis:

- SciEvent (EMNLP 2025): scientific IE needs structured events, triggers and fine-grained arguments; narrow entity-relation extraction fragments context.
- EventRelBench (EMNLP Findings 2025): coreference, temporal, causal and hierarchy/subsumption relations remain difficult even for modern LLMs.
- SciNLP (EMNLP 2025): full-text scientific entity/relation extraction is a distinct structured-information problem.
- recent claim-verification literature continues to identify decomposition and relation/evidence alignment as central error sources.

## B2.1 pre-consultation recommendation

`HYBRID_RELATION_AWARE_EXTRACTION_REPAIR`

Do not repair aligner.
Do not weaken B2 gates.
Do not patch the 8 pair IDs individually.

Before implementation, obtain one focused higher-model architecture review on the minimum repair boundary:
- which relation families are blocking;
- which can remain deterministic;
- where abstaining semantic extraction is justified;
- whether authentic academic text should be introduced immediately after the repaired B2 prototype.
