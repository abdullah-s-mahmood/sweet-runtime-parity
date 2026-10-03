# AT0-EN V2.4 Gate A4 — Readiness Decision Matrix

Date: 2026-10-03
Status: FINAL READINESS DECISION / NO ALIGNMENT IMPLEMENTATION YET

## Decision

Final verdict:
`ACCEPT_AND_PROCEED_TO_ALIGNMENT`

Scope:
development alignment research only.

Not authorized:
- production acceptance
- extractor generalization claims
- end-to-end safety claims
- live generation
- HW1-EN
- untouched holdout opening

## Change from implementation-agent preliminary decision

Pre-consultation recommendation:
`REPAIR_TARGETED_FIRST`

Final decision after independent review:
`ACCEPT_AND_PROCEED_TO_ALIGNMENT`

Reason for change:
The preliminary analysis treated the observed 12% overmerge and narrow certain-precision margin as reasons to repair before alignment.

The consultation correctly distinguishes:
- atomicity imperfection as a diagnostic property,
from
- semantic loss as the actual safety problem.

Because the frozen architecture already supports one-to-many and many-to-one alignment, overmerge is not blocking unless it demonstrably loses or corrupts:
- ownership;
- scope;
- negation;
- relation identity;
- or other material scientific semantics.

The current A3 evidence did not demonstrate such a CERTAIN silent failure.

## Accepted consultation recommendations

### 1. Start alignment research now
Decision: ACCEPT.

Alignment must begin on development data only.

### 2. Use human-correct graphs first
Decision: ACCEPT.

Reason:
This isolates alignment error from extraction error.

Required order:
1. human-reviewed/correct source and candidate representations;
2. alignment validation;
3. extracted representations on the same development material;
4. compare degradation caused by extraction.

### 3. Keep uncertainty visible
Decision: ACCEPT.

Two UNCERTAIN representations agreeing with each other cannot create automatic semantic confidence.

### 4. Keep overmerge/abstention in denominators
Decision: ACCEPT.

No filtering of difficult examples to improve alignment metrics.

### 5. Do not force zero overmerge
Decision: ACCEPT.

Repair only when a merge is proven to lose or rebind material semantics.

### 6. Defer assertion-type optimization
Decision: ACCEPT.

Assertion type remains diagnostic unless it changes semantic routing or causes omission/bypass of checks.

### 7. Defer unnecessary-abstention optimization
Decision: ACCEPT.

23.53% unnecessary abstention is a usability/efficiency weakness, not a blocker for alignment research.

### 8. Authentic academic text after alignment prototype
Decision: ACCEPT.

Authentic text must enter:
after a diagnosable alignment prototype exists,
but before system freeze or integrated-validity claims.

## Active risks carried forward

1. Small synthetic development reference.
2. Certain precision based on only 14 CERTAIN predictions.
3. Overmerge may become harmful under alignment even if non-blocking now.
4. Candidate-side extraction behavior remains unknown.
5. Source/candidate shared extraction bias can still produce false agreement.
6. Alignment may amplify rather than isolate extraction uncertainty if confidence propagation is poorly designed.

## Alignment safety constraints

Alignment research must enforce:
- source and candidate extraction frozen before alignment;
- correct/human-reviewed graphs used first;
- uncertainty cannot be erased by graph agreement;
- one critical wrong relation is non-compensatory;
- one-to-many / many-to-one supported;
- every alignment decision has traceable evidence;
- PASS-like alignment states cannot be inferred from similarity alone;
- extracted-graph results reported separately from gold-graph results.

## Revalidation trigger

Extractor revalidation is required only if extractor logic changes.

If changed:
- rerun six-case development evaluation;
- preserve original A3 result;
- use frozen A3 thresholds;
- add only small contrastive repair examples;
- critical silent semantic errors must remain zero.

## Research interpretation

Current literature supports this decision:
- claim decomposition should be optimized/evaluated jointly with downstream verification rather than by atomicity alone;
- alignment between decomposition quality and verifier behavior is a distinct bottleneck;
- ambiguity-aware extraction and coverage remain independently important.

## Final disposition

`GO_ALIGNMENT_RESEARCH_DEVELOPMENT_ONLY`

No repair is required before starting alignment mechanics.

The source extractor remains:
`DEVELOPMENT-VIABLE / NOT GENERALLY VALIDATED`
