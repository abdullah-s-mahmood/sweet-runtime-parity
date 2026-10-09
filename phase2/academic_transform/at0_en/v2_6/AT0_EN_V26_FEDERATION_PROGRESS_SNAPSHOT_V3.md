# ACAD_PASS — Federation Progress Snapshot V3

Date: 2026-10-09

State:
`PREFIT_CLOSURE_NEAR_COMPLETE / GPU_BACKEND_AND_FINAL_REVIEW_PENDING / NO_SUCCESSOR_SCIENTIFIC_FIT`

## 1. Mandatory independent-review findings F01-F06

Conservative rubric:

- F01 exposure lineage + protected identity/family custody: 90%
  - R43/R44 lineage corrected to EBM-NLP_mod;
  - exact-text, registry, PMID and DOI custody layers completed;
  - protected identities remain undisclosed;
  - unresolved same-trial-family identity cannot be proven absent for every record.

- F02 weak-role semantics: 100%
  - DISTANT-CTO cannot supervise native I/C roles;
  - D5 prospectively canceled when the official release failed the proposed semantic-type contract;
  - no replacement arm.

- F03 gold-independent preprocessing: 95%
  - historical gold-aware chunking defect verified;
  - text-only window planner PASS;
  - real pinned-tokenizer/windowing PASS on all 400 EBM-NLP_mod docs;
  - source offsets/UNK retention deterministic.

- F04 benchmark eligibility/provenance: 82%
  - AD/COVID official split identity and text disjointness PASS;
  - partial exact-title PMID resolution PASS;
  - DOI/registry collision audit PASS;
  - no observed collisions with checked protected/exposed sources;
  - residual unknown publication/trial-family aliases remain an interpretation limitation.

- F05 incompatible-comparator handling: 100%
  - FinePICO/AlpaPICO/PICOX/GPT-4o task/metric incompatibilities explicitly bounded;
  - adapted PICOX strict four-class comparator recipe/mechanics frozen.

- F06 finite first campaign: 100%
  - D0-D4 only;
  - 45 active fits;
  - three folds;
  - seeds 44/45/46;
  - losses/training constants/stopping rules frozen;
  - D5 canceled without replacement;
  - no extra adaptive arm.

Arithmetic mean:
`94.5%`

## 2. End-to-end first scientific development-fit readiness

Ten-domain conservative rubric:

1. Source identity / ontology / research-use / split closure: 90%
2. Alias / trial-family graph: 80%
3. Protected custody: 85%
4. External benchmark eligibility: 82%
5. Gold-independent preprocessing: 95%
6. Dataset adapters and architecture mechanics: 95%
7. Strict scorer / aggregation mechanics: 95%
8. Comparator recipe/mechanics: 95%
9. Scientific software/runtime/checkpoint mechanics: 85%
10. Attempt/data/runtime-contract binding: 95%

Arithmetic mean:
`89.7%`

Interpretation:
- this is PROCESS READINESS;
- it is NOT model accuracy;
- it is NOT a probability of scientific success.

The main missing runtime fraction is a REAL qualified GPU, not unspecified model logic.

## 3. Improvement versus earlier snapshots

Earlier:
- F01-F06 closure = 80.83%
- first-fit readiness = 44.0%

Intermediate:
- F01-F06 = 90.0%
- first-fit readiness = 73.5%

Current:
- F01-F06 = 94.5%
- first-fit readiness = 89.7%

Change from initial snapshot:
- F01-F06: +13.67 percentage points
- first-fit readiness: +45.7 percentage points

Change from immediate prior snapshot:
- F01-F06: +4.5 percentage points
- first-fit readiness: +16.2 percentage points

## 4. Performance status

No new scientific successor model has been fit.

Therefore there is:
`NO NEW PERFORMANCE IMPROVEMENT OR DEGRADATION TO CLAIM`

Latest actual model evidence remains frozen R44C:
- macro precision .8767348592080204 at t=.95
- P .8918918918918919
- I .8171091445427728
- C .9318181818181818
- O .8661202185792349

## 5. What improved scientifically

- provenance risk reduced;
- invalid direct I/C weak-supervision assumption removed;
- data leakage controls strengthened;
- all 45 active fits bound to immutable per-fold data hashes;
- canonical scientific runtime software contract frozen;
- PICOX revision conflict removed;
- exact checkpoint/resume equivalence PASS;
- GPU qualification gate prepared fail-closed.

## 6. What worsened / was removed

D5 was canceled:
`D5_CANCELED_WITHOUT_REPLACEMENT`

This removes one speculative weak-supervision arm, but it is NOT an observed performance degradation because D5 was never scientifically fit.

Scientific validity improved because the official DISTANT-CTO release did not contain the proposed semantic subtype labels needed for that arm.

Residual risks:
- unresolved trial-family identity for a minority of public benchmark records;
- GPU backend not yet qualified;
- final independent pre-fit review not yet returned.

## 7. Target

Before first scientific fit:
`100% OF BLOCKING PREFIT CHECKS MUST PASS`

This does not require proving every historical/public trial-family identity in existence; unresolved external-benchmark identity may remain an explicit limitation if independent review judges it nonblocking for DEVELOPMENT.

Model target after fitting is NOT a generic "90% overall":
- standard mode primary target = best reproducible strict exact-span P/I/C/O performance versus comparable systems;
- selective high-precision mode = per-class precision >=.90, recall >=.33, accepted >=30/class, >=20 trial families/class under one frozen global threshold;
- SOTA claim requires same benchmark/schema/matching/metric.

## 8. Current blocker stack

1. real GPU execution backend;
2. GPU qualification artifact and exact runtime hash;
3. bind that runtime hash into all 45 active attempt slots;
4. final independent higher-model pre-fit review/adjudication;
5. only then authorize first D0-D4 scientific fit.

External AD/COVID benchmark scoring remains later and stays sealed during development.

## 9. Current checkpoint

`HARDWARE_INDEPENDENT_CLOSURE_NEAR_COMPLETE`
->
`QUALIFY_GPU`
->
`FINAL_HIGHER_MODEL_PREFIT_REVIEW`
->
`BIND_GPU_RUNTIME_HASH_TO_45_SLOTS`
->
`FIRST_SCIENTIFIC_FIT`
