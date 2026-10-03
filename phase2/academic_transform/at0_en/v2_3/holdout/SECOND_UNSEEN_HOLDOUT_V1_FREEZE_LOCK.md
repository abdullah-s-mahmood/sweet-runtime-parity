# AT0-EN V2.3 — Second Unseen Holdout V1 Freeze Lock

Date: 2026-10-03
Status: **FROZEN PRE-SCORE / INTEGRITY PASS / SCORING NOT RUN**

## Scope

This checkpoint freezes the second unseen-to-scoring adversarial holdout for the already-frozen V2.3 assertion-graph verifier.

No V2.3 scoring was performed in this stage.
No model inference was performed.
No holdout-driven verifier modification was performed.

## Frozen identities

Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `phase2-arabic-eval`

Protocol commit:
`251704410db9e9bc6921910bf775b0a8ea1bc53c`

Inputs commit:
`b8fd69277e27d61ad779508604f486db310da5d9`

Labels commit:
`d560b47d485afb82fd7e32e37b272242e276885d`

Manifest commit:
`d549ca5862384903bbdc7ab13b93205a95f6afc0`

Integrity-script commit:
`be35211aac30c6cd909e7eed1dcb72adcef57919`

Freeze-trigger commit:
`bda935f597ad716f1c492c4ed380c434c1016f65`

## Verified SHA-256 identities

- inputs:
  `b1633df5e0418082a990945dfc92a267f6cdc8c943b385d7edc2d8b9181f551c`
- labels:
  `9936377336708dbeaf88b7ee83a8ae5fb4272013129041332094dfa625345a9b`
- frozen V2.3 verifier:
  `d82af97d276131477ab2f8c452f24e3302703f54b856a8ad46547af59d7ec0da`
- source cases:
  `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`

All four observed SHA-256 values exactly match the manifest.

## Structural integrity

- total inputs: **36**
- total labels: **36**
- unique holdout IDs: **36**
- ID/order alignment: **PASS**
- SAFE_CONTROL: **12**
- ADVERSARIAL: **24**
- source cases represented: **EN01–EN12**
- adversarial cases per source case: **2 each**
- safe controls per source case: **1 each**

Integrity result: **PASS**

## Holdout composition

The holdout contains:
- 12 faithful contrastive paraphrase controls;
- 24 adversarial cases spanning relation rebinding, qualifier/scope changes, unit/baseline changes, citation/outcome changes, manipulation-status changes, equation/variable binding changes, metric-label swaps, partial retuning, and related scientific-preservation failures.

The source paragraph is authoritative. Older frozen `content_units` are supporting indices only.

## Independence statement

This holdout is **temporally held out from V2.3 scoring** and its labels were frozen before scoring.

It is **not claimed to be fully designer-blind independent evidence**, because the same project context was aware of the V2.3 architecture and prior V2.2 failure classes during construction.

Therefore a future one-shot score is valid as a second temporally separated adversarial check, but not as a universal unbiased benchmark.

## End-of-stage research check

Fresh research reviewed at closure supports the current safeguards:

- Jourdan et al., ACL 2025: scientific text revision evaluation needs correctness-sensitive, task-specific and hybrid evaluation; similarity or instruction-following alone is insufficient.
- Chen et al., EMNLP 2025: contamination risk motivates movement from static toward dynamic benchmarking and explicit benchmark-design criteria.
- FactBench, ACL 2025: dynamic factuality evaluation addresses staleness/contamination concerns.
- ACL 2026 factual-consistency stress testing: factuality metrics can behave inconsistently under meaning-preserving paraphrases, supporting the inclusion of safe paraphrase controls rather than adversarial cases alone.

This research supports the holdout design but does not establish the correctness of V2.3.

## GitHub Actions integrity workflow note

A dedicated workflow file was added:
`.github/workflows/at0_en_v2_3_holdout_freeze_integrity.yml`

A non-semantic trigger commit was created, but GitHub exposed **no workflow run** for that integrity workflow. No scientific state was changed in response.

Instead, the exact frozen repository contents at commit
`bda935f597ad716f1c492c4ed380c434c1016f65`
were independently read and checked for:
- SHA-256 equality,
- counts,
- unique IDs,
- label/input ordering,
- class balance,
- two adversarial cases per source case,
- verifier/source identity.

That repository-level integrity check passed.

The absent Actions run is therefore an **operational tooling issue**, not a scientific failure. It must not be represented as an Actions PASS.

## Quality delta versus prior checkpoint

### Methodological status

**IMPROVED**

Compared with the previous known-failure regression checkpoint:
- V2.3 previously had only a regression test against attack families already known during redesign;
- this stage adds a separately frozen 36-case holdout before scoring;
- labels and inputs now have pre-score hashes and commits;
- safe paraphrase controls are included to measure false positives, not only attack detection.

### Scientific performance delta

**NOT YET MEASURED**

No new V2.3 score exists yet, so no scientific improvement percentage may be claimed from this stage.

The last comparable measured robustness evidence remains:
- V2.2 independent attack escape: **21/24 = 87.5%**
- V2.3 known-failure regression: **0/24 escape on the same known attacks**
- this is a **-87.5 percentage-point escape-rate change on known attacks only**, not unseen generalization evidence.

## Completion status

Current stage:
**100% COMPLETE**

Whole ACAD_PASS program:
**approximately 20% ±5% complete** as a planning estimate, not a scientific metric.

Major unfinished blocks include:
- one-shot scoring of the frozen second holdout;
- higher-model interpretation of that unseen result;
- any further verifier redesign if failures appear;
- HW1-EN human-writing evaluation;
- broader/cross-domain scientific fidelity;
- document/DOCX fidelity;
- voice/profile validation;
- detector robustness;
- long-document behavior;
- product/commercial usefulness and release engineering.

## Exact next authorized stage

**SECOND_UNSEEN_HOLDOUT_V1 ONE-SHOT SCORE**

Only after explicit user continuation:

1. bind to the frozen verifier SHA;
2. bind to frozen inputs/labels hashes;
3. produce predictions before evaluation;
4. score once;
5. freeze all errors;
6. do not tune V2.3 and reuse this holdout as untouched evidence.

No model inference is required for this score.

HW1-EN remains blocked.
Arabic active research remains frozen.
Arabic V4.2 remains closed.
Reserved Arabic populations remain closed.
