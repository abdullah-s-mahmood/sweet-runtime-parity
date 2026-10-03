# AT0-EN V2.4 — B2.1 Architecture Decision Closure

Date: 2026-10-03
Status: CLOSED / GO_B2_2_RELATION_AWARE_REPAIR

## Final decision

`HYBRID_RELATION_AWARE_EXTRACTION_REPAIR`

Implementation has NOT started in this checkpoint.

## Why this boundary was selected

Canonical B2 evidence:
- GG: 100%
- GE: 41.67%
- EG: 50%
- EE: 33.33%
- EE safe acceptance: 0%
- EE adversarial acceptance: 0%
- REVIEW preservation: 100%

Interpretation:
- alignment mechanics remain strong on human-correct graphs;
- extraction/representation is the dominant bottleneck;
- safety is conservative but usability is unacceptable.

## Blocking repair capabilities

Required now:
1. predicate/paraphrase normalization;
2. negation/scope ownership;
3. owner/value and owner/meaning split-merge binding;
4. citation-to-claim binding;
5. equation/symbol/coefficient binding.

Deferred unless new evidence makes them blocking:
- generic procedural-order parser;
- generic local-coreference resolver;
- broad semantic-parser replacement;
- general mathematical equivalence.

## Keep vs replace A2

Keep frozen A2 for:
- deterministic anchors;
- exact provenance;
- assertion proposals.

Add a relation-aware structured layer that can use original text, allowed context, evidence, and anchors.

Do not replace A2 with a broad generic semantic parser.

## B2.2 progression gates

EE safety:
- adversarial acceptance 0/6
- dangerous critical false preserve 0
- critical uncertainty promotion 0
- ambiguous pair remains REVIEW

EE usability:
- safe acceptance >=4/5 = 80%
- pair accuracy >=11/12 = 91.67%
- faithful false rejection <=1/5

Regression:
- GG remains 100%
- anchor/provenance behavior does not regress
- critical relation representation is auditable per side

Passing these gates authorizes the next research stage.

## Strong-adoption targets

- adversarial automatic acceptance: 0%
- critical silent scientific errors: 0
- automatic-PASS selective precision: >=99%
- authentic in-domain safe automatic acceptance: >=90%
- extracted-graph pair accuracy: >=95%
- controlled critical relation/ownership correctness: 100%
- deterministic anchor precision/recall: 100% / 100%
- critical evidence/provenance completeness: 100%

## Authentic academic text timing

Immediately after the first B2.2 relation-aware repair prototype exists and before synthetic B2 revalidation:
- small qualitative authentic academic excerpts;
- local context preserved;
- development-only;
- no benchmark claim;
- no numeric adoption claim.

## Consultation provenance

Higher-model response:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_1_HIGHER_MODEL_RESPONSE_V1.md`

Final repair boundary:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_1_FINAL_REPAIR_BOUNDARY_V1.md`

## Completion

B2.1:
**100% COMPLETE**

Gate B2 overall:
**approximately 85% complete**

Whole ACAD_PASS:
**approximately 30% ±5%**

## Exact next authorized stage

`AT0-EN V2.4 B2.2 — HYBRID RELATION-AWARE EXTRACTION REPAIR PROTOTYPE`

Next stage scope:
- implement only the five mandatory blocking capabilities;
- preserve A2 anchors/provenance;
- preserve B1.1 aligner;
- perform small qualitative authentic-text check after prototype;
- then rerun the frozen four-arm B2 revalidation;
- freeze results before any further repair.

Not authorized:
- live generation
- HW1-EN
- untouched holdout
- production claims
