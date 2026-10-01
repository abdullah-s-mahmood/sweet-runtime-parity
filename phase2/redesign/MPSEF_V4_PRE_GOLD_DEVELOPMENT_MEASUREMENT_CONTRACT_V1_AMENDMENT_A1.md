# MP-SEF V4 PRE-GOLD DEVELOPMENT MEASUREMENT CONTRACT V1 — AMENDMENT A1

Date: 2026-10-02
Status: FROZEN / MANDATORY BEFORE ANY REAL C_F GOLD LOAD
Governing review:
`ACAD_PASS_V4_RJOINT_INTERNAL_ADVERSARIAL_REVIEW_V1.md`

This amendment supersedes conflicting V1 measurement semantics. Historical V4 source-free preflight remains preserved as evidence and is not rewritten.

## A1.1 — Full-reference scoring with primary/punctuation projection

The measurement MUST freeze all reference targets before any action score.

For each UID:
- `ALL_TARGETS`: every frozen reference target;
- `PRIMARY_TARGETS`: all targets with scope != PUNCTUATION_ONLY;
- `PUNCTUATION_TARGETS`: targets with scope == PUNCTUATION_ONLY.

Every whole action MUST be evaluated against the **full reference edit set**.

Matched target indices are then projected onto:
- primary indices;
- punctuation-only indices.

Reason:
a reference-supported punctuation correction must not be counted as an `extra` merely because punctuation is excluded from the primary target denominator.

Primary target recovery:
best one whole action's matched count over PRIMARY_TARGETS.

Punctuation recovery:
best one whole action's matched count over PUNCTUATION_TARGETS.

Reference-unsupported extra edits:
use the scorer's `extra` computed against ALL_TARGETS.

No action may be evaluated against a candidate-dependent target subset.

## A1.2 — Clean/complete terminology

Required measures:

### PRIMARY_RECOVERY
Recovery of non-punctuation primary targets.

### PRIMARY_CLEAN_RECOVERY
Primary targets recovered by one whole action with `extra == 0` against the full reference.

This allows a correct reference-supported punctuation edit without treating it as extra.

### PRIMARY_COMPLETE_REPAIR
Sentence-level availability of one whole action that:
- matches every primary target;
- has `extra == 0` against the full reference.

It may leave punctuation targets unrepaired.

### ALL_REFERENCE_COMPLETE_REPAIR
Sentence-level availability of one whole action that:
- matches every frozen reference target;
- has `extra == 0`.

These constructs MUST be reported separately.

## A1.3 — Sentence reference-state categories

Every UID is exactly one of:
- `ALL_REFERENCE_CLEAN`: zero frozen targets;
- `PUNCTUATION_ONLY_REFERENCE`: zero primary targets and >=1 punctuation target;
- `PRIMARY_ERROR_PRESENT`: >=1 primary target.

These categories are mutually exclusive at UID level.

Candidate activity on ALL_REFERENCE_CLEAN is the only metric that may be called clean-sentence candidate activity.

PUNCTUATION_ONLY_REFERENCE activity MUST be reported separately.

## A1.4 — M05 composite routes

Freeze:
- `INSERT_ROUTE = {INSERT}`
- `BOUNDARY_ROUTE = {SPLIT, MERGE}`

For each route and sentence:
- union all target indices belonging to the route;
- maximize one complete whole action over that union.

Forbidden:
`sum(max per member family)`.

Family comparison is between:
- `SWEET_QALB14`
- `SEQ2SEQ_GED_MORPH`

For each route report:
- SWEET recovery interval;
- SEQ2SEQ recovery interval;
- ROSTER recovery interval;
- SWEET additional-target lower/upper vs SEQ2SEQ;
- SEQ2SEQ additional-target lower/upper vs SWEET;
- corresponding distinct-cluster lower/upper counts.

Additional target and cluster evidence MUST use the same one-whole-action semantics.

No weak-route quality claim follows from these diagnostics.

## A1.5 — Overall 95% development candidate-availability gate

Historical V3 95% rule is retained.

Apply it ONLY to:
`ROSTER PRIMARY_RECOVERY`

Using integer arithmetic:
- PASS if `20 * lower_numerator >= 19 * denominator`;
- FAIL if `20 * upper_numerator < 19 * denominator`;
- otherwise INCONCLUSIVE;
- denominator zero -> INCONCLUSIVE_NO_TARGETS.

Name:
`ROSTER_PRIMARY_CANDIDATE_AVAILABILITY_GATE_95`

This is a reference-relative development candidate-availability gate, not correctness, safety, or generalization.

No proposer-level or family-level 95% pass/fail ranking is authorized.

## A1.6 — Production measurement input lock

Before any gold execution, a separate wrapper/input lock MUST freeze and verify:

- C_F source manifest SHA256;
- V4 legal action-set SHA256;
- scorer SHA256;
- scorer-core SHA256;
- target-builder/matching version;
- target-family-map version;
- punctuation-policy version;
- population UID-list SHA256;
- exact gold/reference input identity and SHA256;
- Python version;
- dependency lock;
- result schema version.

The wrapper MUST fail closed before scoring on any mismatch.

The scorer library itself MUST NOT locate or download project gold.

## A1.7 — Result identity fields

Every real measurement result MUST embed:
- claim scope;
- population identity;
- action-set identity;
- gold/reference identity;
- scorer/core identities;
- matching/family-map/punctuation-policy versions;
- primary and punctuation denominators;
- scoring-failure count;
- all scientific-boundary flags.

## A1.8 — Single-reference wording

Required wording:
- `REFERENCE_SUPPORTED`
- `REFERENCE_UNSUPPORTED_EXTRA`

Forbidden interpretation:
`REFERENCE_UNSUPPORTED_EXTRA == LINGUISTICALLY_WRONG`

All metrics remain:
`DEVELOPMENT / ADAPTIVELY_CONSUMED / REFERENCE_RELATIVE / NOT INDEPENDENT GENERALIZATION`

## A1.9 — Expanded source-free preflight

Create a new scorer version; do not overwrite frozen V4.

Minimum:
**27/27 PASS**

Tests 1-20:
preserve previous V4 regressions.

Additional:
21. reference-supported punctuation edit does not become an extra under primary projection;
22. punctuation target recovery is separate;
23. sentence category distinguishes ALL_REFERENCE_CLEAN vs PUNCTUATION_ONLY_REFERENCE;
24. population BOUNDARY={SPLIT,MERGE} uses one whole action;
25. family additional-target/additional-cluster route evidence obeys one whole action;
26. ROSTER 95% gate exact integer PASS/FAIL/INCONCLUSIVE semantics;
27. production identity-contract mismatch fails closed.

## A1.10 — Authorization boundary

Still forbidden:
- real C_F gold/reference load;
- real R_joint;
- P4 execution;
- selector training;
- family consensus;
- LLM judge;
- reserved/internal populations.

After 27/27 PASS:
perform remediation closure review and freeze production input-lock/wrapper.

Only a later explicit authorization lock may permit real C_F gold loading.
