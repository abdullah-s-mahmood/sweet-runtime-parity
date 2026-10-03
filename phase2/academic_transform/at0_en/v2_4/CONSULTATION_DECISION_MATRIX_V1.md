# AT0-EN V2.4 — Consultation Decision Matrix

Date: 2026-10-03
Status: ARCHITECTURE REVIEW INTEGRATED / NO IMPLEMENTATION YET

## Decision summary

Higher-model verdict: PROCEED_WITH_CHANGES

Project decision:
- required architecture changes accepted: 8/8
- top risks accepted as active risks: 5/5
- validation stages accepted: all
- do-not-do items accepted: all
- implementation authorization: LIMITED OFFLINE PROTOTYPE ONLY
- new generation authorization: NO
- HW1-EN authorization: NO

## Recommendation decisions

### R1 — Keep graph small and relation-justified
Decision: ACCEPT.

Reason:
The observed failure is relation ownership/rebinding, not a need for a general-purpose knowledge graph. A minimal typed assertion graph reduces unnecessary ontology complexity and makes provenance auditable.

### R2 — Convert flat fields into owned relations
Decision: ACCEPT.

Required additions:
- anchor ownership must be explicit;
- quantity type: absolute / relative;
- percent vs percentage-point distinction;
- range/bound representation;
- denominator where material;
- uncertainty/precision where material;
- raw source expression preserved alongside normalization.

### R3 — Explicit operator scope and procedural structure
Decision: ACCEPT.

Required additions:
- scoped negation;
- scoped hedge/modality;
- evidence/causality scope;
- exception scope;
- AND/OR;
- all/some and related quantifiers;
- proposed / implemented / observed / hypothetical status;
- procedure order and dependencies;
- citation-to-claim binding;
- equation-to-symbol-definition binding.

### R4 — Correct deterministic vs semantic boundary
Decision: ACCEPT WITH CLARIFICATION.

Deterministic:
- identity/version/hash;
- authorized scope;
- transaction atomicity;
- protected-element byte/token integrity where directly representable;
- exact numeric/symbol/citation/equation token presence;
- exact deterministic calculations derived from frozen values.

Semantic:
- which assertion owns a number;
- which claim a citation supports;
- which group/time/baseline a value belongs to;
- whether two paraphrases preserve the same relation.

Rule:
semantic evidence can never override a deterministic contradiction.
Sentence count is explicitly NOT a scientific invariant.

### R5 — Freeze source extraction, independently extract candidate, then jointly align
Decision: ACCEPT.

Source graph:
- extracted once per source version;
- frozen before candidate extraction.

Candidate graph:
- extracted independently from candidate + allowed context;
- no expected source relation labels supplied.

Alignment:
- may inspect both frozen graphs and original evidence jointly;
- may propose alternative interpretations with provenance;
- may not silently rewrite a candidate graph to force agreement.

### R6 — Independent coverage checking
Decision: ACCEPT.

Coverage cannot depend on extractor self-confidence.
Need explicit accounting for:
- unrepresented scientific spans;
- unowned deterministic anchors;
- relation fragments;
- table/title/context dependencies;
- unresolved references.

A missing graph node does not imply missing source information.

### R7 — Bidirectional many-to-many alignment
Decision: ACCEPT.

Required:
- source -> candidate preservation/alteration/omission;
- candidate -> source aligned/new/contradictory;
- one-to-many and many-to-one allowed for valid split/merge;
- critical relation mismatch is non-compensatory;
- lexical/embedding similarity is retrieval support only, never PASS evidence.

### R8 — Four outcomes
Decision: ACCEPT WITH TRANSACTION-LEVEL CLARIFICATION.

PASS_CANDIDATE:
meaning preserved relative to source and verified scope only; not external scientific truth.

REJECT:
material change supported by traceable evidence.

REVIEW:
material ambiguity in extraction/alignment or insufficient evidence prevents automatic PASS.

INVALID_VERIFICATION:
the verification transaction itself is invalid or incomplete, e.g. wrong source version, broken provenance, critical source extraction failure, corrupt structure, or invalid identity binding.
This is NOT a statement that the candidate is scientifically wrong.

Optional non-material uncertainty may coexist with PASS only when it is provably outside any decision dependency.

## Validation-plan decision

Accepted staged program:

Gate 0 — freeze schema, criticality rules and four outcomes.

Gate A — extractor validation on fixed human-reference development material.

Gate B1 — alignment validation on human-correct graphs.

Gate B2 — alignment validation on extracted graphs to measure error propagation.

Gate C — new end-to-end verifier validation on a newly frozen set after the pipeline is frozen.

Preliminary end-to-end gates remain:
- observed dangerous adversarial escape: 0
- safe automatic acceptance: >=75%

These are not to be relaxed post hoc.

## Architecture consequence

V2.4 is authorized to proceed only to a small offline architecture/prototype phase.

Not authorized:
- new transformation generation;
- HW1-EN;
- live experiment expansion;
- new untouched benchmark opening before V2.4 pipeline freeze.

## Quality status

Experimental performance is unchanged from V2.3:
- adversarial escape 37.5%
- safe acceptance 25%
- BOTH_FAIL

Methodological status:
IMPROVED — consultation identified and closed several architecture-definition gaps before implementation.

No quantitative performance improvement is claimed.
