# AT0-EN V2.4 — Frozen Architecture V2

Date: 2026-10-03
Status: FROZEN ARCHITECTURE / LIMITED OFFLINE PROTOTYPE AUTHORIZED / NO GENERATION

## 1. Architecture objective

Prevent scientific meaning drift during academic rewriting by verifying ownership and structure of scientific assertions rather than relying on token presence or case-specific regex templates.

## 2. Core representation

### Scientific Assertion Frame

Each assertion must retain:
- assertion_id
- exact provenance/span
- discourse role
- assertion type
- subject
- normalized predicate
- object
- value
- comparator/direction
- unit
- quantity kind: absolute / relative / ratio / percentage / percentage-point / range / bound
- denominator when material
- uncertainty/precision when material
- raw source expression
- arguments
- conditions
- temporal context
- population/group
- baseline/reference condition
- modality/hedge
- evidential strength
- polarity
- causality class
- scope operators
- exclusions/exceptions
- quantifier structure
- state: proposed / implemented / observed / hypothetical / other
- citation bindings
- equation bindings
- symbol-definition bindings
- extraction confidence/status
- unresolved slots

Critical extraction status:
CERTAIN / UNCERTAIN / AMBIGUOUS.

Critical UNCERTAIN or AMBIGUOUS content cannot support automatic PASS.

### Minimal Assertion Relation Graph

The graph is intentionally small and task-specific.

Nodes:
- assertions
- entities
- metrics
- values
- units
- times
- populations/groups
- conditions
- baselines
- citations
- equations
- symbols
- procedure steps

Edges express ownership and dependency, including:
- ASSERTS_ABOUT
- HAS_VALUE
- HAS_UNIT
- UNDER_CONDITION
- AT_TIME
- IN_POPULATION
- RELATIVE_TO
- APPLIES_ONLY_TO
- CITES
- DEFINES
- MEASURES
- COMPARES_TO
- ASSOCIATED_WITH
- CAUSAL_RELATION
- NEGATES
- EXCLUDES
- PRECEDES
- DEPENDS_ON
- FIXED_BEFORE
- UNCHANGED_DURING

Each edge carries:
- provenance
- polarity
- scope
- modality/evidential strength
- confidence
- normalization trace
- minimal evidence trace supporting the relation decision

Evidence traces must identify the smallest sufficient source/candidate spans used for a critical alignment or rejection. When document context later includes tables, captions, titles, footnotes, or equation blocks, these may be explicit evidence nodes/references rather than being flattened into nearby prose.

No graph database or broad ontology is required.

## 3. Operator and scope representation

The representation must preserve:
- negation scope
- hedge/modality scope
- evidence strength scope
- causal scope
- exceptions
- AND / OR composition
- all / some / none and related quantifiers
- proposed vs implemented vs observed vs hypothetical state
- procedural order and dependencies

A generic free-text scope field is insufficient.

## 4. Deterministic vs semantic verification

### Lane A — deterministic invariants

Authoritative for:
- source/version/hash identity
- authorized transaction scope
- atomicity
- protected-element integrity where directly representable
- exact tokens for numbers, units, IDs, symbols, equations, citations
- deterministic calculations over frozen values

Important:
token presence is deterministic;
ownership of that token is not necessarily deterministic.

A deterministic contradiction cannot be overridden by semantic evidence.

Sentence count is not a scientific invariant.

### Lane B — semantic relation verification

Used for:
- predicate normalization
- paraphrase equivalence
- subject/object ownership
- value/metric/group/time/baseline binding
- condition/scope equivalence
- modality/evidential-strength equivalence
- causal vs associational meaning
- negation scope
- relation rebinding
- split/merge equivalence

Outputs:
MATCH / MISMATCH / UNCERTAIN.

Critical UNCERTAIN -> REVIEW.

No single LLM/NLI/embedding score can be the sole safety oracle.

## 5. Extraction separation

Source extraction:
- once per exact source version;
- frozen before any candidate extraction;
- includes provenance and coverage accounting.

Candidate extraction:
- independent from candidate text plus explicitly permitted context;
- never receives expected source relations as labels.

Alignment:
- begins only after both extractions are frozen;
- may inspect both frozen representations and original evidence jointly;
- may record alternative interpretations;
- may not silently rewrite candidate representation to force agreement.

## 6. Coverage and extraction validity

Extractor self-confidence is not coverage proof.

Required checks:
- unrepresented scientific spans
- unowned numeric/symbol/citation anchors
- unresolved coreference/context
- broken table/title dependencies
- contradictory extracted assertions
- missing critical relations
- empty extraction from claim-bearing text

Critical extraction failure can yield INVALID_VERIFICATION.

## 7. Bidirectional many-to-many alignment

Source -> candidate:
PRESERVED / ALTERED / OMITTED / UNCERTAIN

Candidate -> source:
ALIGNED_EXISTING / NEW_INFORMATION / CONTRADICTORY / UNCERTAIN

Alignment must support:
- one-to-one
- one-to-many
- many-to-one

This is required for legitimate sentence split/merge and redundancy removal.

Similarity/embeddings may propose candidate matches only.
They never confer PASS.
A critical mismatch is non-compensatory.

Critical alignment classes must explicitly support coreference, temporal, causal, comparison/baseline, and hierarchy/subsumption relations where they affect scientific meaning.

## 8. Transaction outcomes

### PASS_CANDIDATE
Meaning preserved relative to the source and verified scope.
Does not claim external scientific truth.
Every critical PASS dependency must have traceable supporting evidence; a correct final label without faithful evidence trace is insufficient for automatic PASS.

### REJECT
Material scientific change supported by traceable evidence.

### REVIEW
Material ambiguity in extraction/alignment or insufficient evidence prevents automatic PASS.

### INVALID_VERIFICATION
Verification transaction itself is invalid/incomplete, e.g.:
- wrong source version
- broken provenance
- corrupt structure
- critical source extraction failure
- invalid identity/scope binding

INVALID_VERIFICATION is not a scientific judgment on the candidate.

Non-material uncertainty may coexist with PASS only if proven outside all decision dependencies.

## 9. Validation gates

### Gate 0 — schema/reference freeze
Freeze:
- relation schema
- criticality rules
- four transaction outcomes
- small fixed human-reference development material

### Gate A — extractor validation
Evaluate source and candidate separately against reference annotations:
- coverage
- false additions
- atomicity
- decontextualization
- ownership
- scope
- negation/hedge handling
- provenance
- abstention quality

No advancement with known critical silent extraction error capable of producing false PASS.

### Gate B1 — alignment validation with human-correct graphs
Test:
- faithful paraphrases
- split/merge
- lexical-preserving relation swaps
- ambiguity

### Gate B2 — alignment with extracted graphs
Measure propagation of extraction errors into alignment outcomes.

### Gate C — frozen end-to-end verifier validation
Only after pipeline freeze:
- create a new holdout
- freeze protocol/denominators
- predictions first
- hash predictions
- labels/evaluation second

Preliminary end-to-end gates:
- observed dangerous adversarial escape: 0
- safe automatic acceptance: >=75%

Do not relax gates after failure.

## 10. Anti-overfitting rules

- V2.3 holdout is consumed development evidence.
- No ID-specific patches from consumed holdout.
- No new untouched holdout until V2.4 pipeline is frozen.
- Synthetic development transformations must be generated from principles, not copied failure IDs.
- Natural faithful controls and adversarial cases are both required.

## 11. Prohibited shortcuts

Do not:
- use extractor self-confidence as truth;
- leak source expected relations into candidate extraction;
- use model agreement as safety proof;
- let semantic judgment override deterministic contradiction;
- build full AMR, general graph DB, or large ontology before need is demonstrated;
- start new generation or HW1-EN before staged validation passes.

## 12. Authorization

Authorized next:
small offline prototype for Gate 0 only.

Not authorized:
- new transformation generation
- HW1-EN
- live expansion
- new untouched benchmark opening
- performance claims

Classification:
ARCHITECTURE IMPROVED / IMPLEMENTATION NOT YET VALIDATED / OFFLINE GATE-0 ONLY
