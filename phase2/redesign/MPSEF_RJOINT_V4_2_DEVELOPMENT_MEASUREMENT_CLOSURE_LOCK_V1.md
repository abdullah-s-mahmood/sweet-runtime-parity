# MP-SEF R_JOINT V4.2 DEVELOPMENT MEASUREMENT CLOSURE LOCK V1

Date: 2026-10-02

Status:
**CLOSED SUCCESSFULLY**

Architecture disposition:
**MODIFY BEFORE SELECTOR TRAINING**

## Frozen execution evidence

Workflow run:
`36940844664`

Run conclusion:
`success`

Consumed status:
`acad-pass/v4-2-rjoint-consumed = success`

Artifact id:
`11200024879`

Artifact digest:
`sha256:10ecdb75b5d80540d2c9ddf5e94672e8d64bbe3eb685ca3f53d63789c3d308af`

Summary SHA256:
`5a649c5e050b34679e27958814201d49a948e039c38961032ced263bdacddc91`

Per-sentence SHA256:
`0e6c51435e978c1c917b9a37a361fad1a5fe4f65da6e18b17759ad2ecb67cc50`

Evidence lock:
`phase2/redesign/MPSEF_RJOINT_V4_2_DEVELOPMENT_MEASUREMENT_EVIDENCE_LOCK_V1.md`

Result analysis:
`phase2/redesign/MPSEF_RJOINT_V4_2_DEVELOPMENT_RESULT_ANALYSIS_V1.md`

## Frozen denominators

- UIDs: 1,918
- clusters: 764
- primary targets: 9,679
- punctuation targets: 129
- all reference targets: 9,808
- primary-error sentences: 1,864
- all-reference-clean sentences: 48
- punctuation-only-reference sentences: 6

## Primary conclusions

ROSTER primary recovery:
- lower: 72.2285%
- upper: 72.2699%

SWEET family primary recovery:
- lower: 66.9284%
- upper: 66.9697%

SEQ2SEQ family primary recovery:
- exact: 58.6941%

ROSTER gain over SWEET:
- approximately +5.26 to +5.34 percentage points
- at least 509 and at most 517 additional reference-supported primary targets

ROSTER 95% candidate-availability gate:
`FAIL_CANDIDATE_AVAILABILITY`

95% target requirement:
9,196

ROSTER upper numerator:
6,995

Deficit:
2,201 targets

Deficit:
22.7301 percentage points

ROSTER clean whole-action recovery:
- lower: 23.6491%
- upper: 23.6905%

ROSTER primary complete repair:
- lower: 21.8884%
- upper: 21.9421%

## Architecture disposition

P1:
`KEEP`

P2:
`KEEP`

P3:
`KEEP AS DIAGNOSTIC SAME-FAMILY ALTERNATE / DEFER AS PRIMARY PRODUCT ROUTE`

Current whole-sentence ROSTER:
`DO NOT TRAIN SELECTOR YET`

Selector:
`DEFER`

Family consensus:
`DEFER`

Generic LLM judge:
`DEFER AS PRIMARY`

Specific previously discussed P4:
`DEFER PENDING PROVENANCE / OVERLAP AUDIT`

Candidate representation:
`REPAIR / REDESIGN GATE`

## Why selector is deferred

The current candidate union fails the frozen 95% availability gate by 2,201 primary targets.

A selector cannot select a correction that is absent from all candidate actions.

The next bottleneck is therefore candidate generation / candidate representation, not selector optimization.

## Fresh-research implications

Relevant external directions reviewed after the result:
- ArbESC+ (2025): Arabic multi-system edit selection and conflict-aware combination.
- STAGEET (2026): staged typed edit tagging for Arabic GEC.
- JELV (AAAI 2026): limited-reference validity and automated reference expansion.
- CLEME2.0 (ACL 2025): edit-disentangled GEC evaluation.

These motivate edit-level/provenance-aware research but do not themselves authorize a new proposer, judge, or selector.

## Evaluation boundary

C_F is now permanently:
`ADAPTIVELY_CONSUMED DEVELOPMENT / NOT CLEAN HOLDOUT`

No future architecture selected or tuned using this result may report C_F as independent confirmation.

No silent rerun of V4.2 is authorized.

## Next formal gate

`POST-V4.2 CANDIDATE ARCHITECTURE REDESIGN GATE`

Required sequence:
1. source-only architecture brainstorming and red-team;
2. provenance audit for proposed new proposer families;
3. edit-level representation/conflict contract;
4. freeze an untouched future evaluation population before any gold-aware tuning;
5. source-free synthetic preflight;
6. independent review before any new reference set is opened.
