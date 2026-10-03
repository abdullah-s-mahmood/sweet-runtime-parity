# AT0-EN V2.4 B2.1 — Final Repair Boundary Decision V1

Date: 2026-10-03
Status: FINAL / REPAIR BOUNDARY FROZEN / IMPLEMENTATION NOT STARTED

## Final architecture decision

`HYBRID_RELATION_AWARE_EXTRACTION_REPAIR`

Keep:
- frozen A2 anchor/provenance extraction;
- frozen B1.1 aligner;
- frozen B2 four-arm protocol;
- frozen B2 safety/usability gates.

Add:
- a versioned relation-aware structured representation layer that may use original text, allowed local context, exact evidence, and deterministic anchors.

Do NOT:
- replace A2 with a broad semantic parser;
- tune the aligner to compensate for missing extraction semantics;
- weaken B2 gates;
- patch consumed pair IDs individually.

## Mandatory repair capabilities for B2.2

1. Predicate/paraphrase normalization
   - controlled normalization for explicit equivalents;
   - abstaining semantic interpretation when contextual meaning is required.

2. Negation and semantic-operator scope ownership
   - distinguish negated proposition, insufficient evidence, non-causality, and uncertain assertion.

3. Canonical owner-to-value / owner-to-meaning binding
   - must survive 1:1, 1:N and N:1 representation changes.

4. Citation-to-claim binding
   - deterministic high precision for explicit attribution;
   - ambiguous attribution stays unresolved.

5. Equation/symbol/coefficient binding
   - deterministic for supported equation structures;
   - no general algebraic-equivalence claim.

## Deferred capabilities

Not required as independent B2 blockers:
- generic procedural-order parser;
- generic local-coreference resolver;
- broad AMR/SRL replacement;
- general mathematical equivalence prover.

These may be added later only if new evidence makes them blocking.

## Deterministic vs semantic boundary

Deterministic-first:
- citation binding when explicit;
- equation/symbol/coefficient ownership when syntactically explicit;
- anchor/value/unit/symbol identity;
- canonical ownership facts when owner relation is explicit.

Hybrid:
- predicate paraphrase;
- negation/scope;
- owner/value relations requiring local contextual interpretation.

Semantic path rules:
- must abstain when unresolved;
- must preserve evidence trace;
- cannot override deterministic contradictions;
- cannot upgrade shared uncertainty to certainty.

## Shared-error safeguards

1. Independent source and candidate extraction.
2. Independent textual-support and coverage audit.
3. Deterministic anchor checks remain independent of semantic extraction.
4. Shared omission or uncertain agreement cannot become PASS.
5. GG/GE/EG/EE remain separately visible.

## Authentic academic text timing

After the first relation-aware repair prototype exists, but BEFORE synthetic B2 revalidation:

- inspect a small qualitative set of authentic academic excerpts with local context;
- use it only to reveal contract blind spots;
- do not treat it as a benchmark;
- do not create numeric performance claims from it;
- any architecture defect found must be fixed/versioned before B2 rerun.

## Frozen B2.2 progression gates

EE safety:
- adversarial acceptance: 0/6
- dangerous critical false preserve: 0
- critical uncertainty promotion: 0
- ambiguous pair remains REVIEW

EE usability:
- safe acceptance >=4/5 = 80%
- pair accuracy >=11/12 = 91.67%
- faithful false rejection <=1/5

Regression:
- GG remains 100% on all B1.1 hard gates
- deterministic anchor/provenance behavior must not regress
- critical relation representation used in decisions must be auditable against text independently per side

Passing these frozen B2 development gates authorizes progression to the next research stage.

## Strong-adoption targets carried forward

These are later ACAD_PASS project targets, not current B2 gates:

- adversarial automatic acceptance: 0%
- critical silent scientific errors: 0
- automatic-PASS selective precision: >=99%
- authentic in-domain safe automatic acceptance: >=90%
- extracted-graph pair accuracy: >=95%
- controlled critical relation/ownership correctness: 100%
- deterministic anchor precision/recall: 100% / 100%
- critical evidence/provenance completeness: 100%

## Decision on current measured gaps

Current canonical B2 EE:
- pair accuracy: 33.33%
- safe acceptance: 0%
- adversarial acceptance: 0%
- REVIEW preservation: 100%

Current gap to B2 progression:
- pair accuracy: +58.34 pp needed to reach 91.67%
- safe acceptance: +80 pp needed to reach 80%
- safety gap: none on measured adversarial acceptance

Current gap to later strong adoption:
- pair accuracy: +61.67 pp to >=95%
- safe acceptance: +90 pp to >=90%
- selective precision: not yet measured end-to-end

## Final disposition

`GO_B2_2_RELATION_AWARE_REPAIR`

No progression beyond B2 until repaired B2 passes the frozen development gates.
