# MP-SEF CORRECTED PRE-AUTHORIZATION INDEPENDENT REVIEW PACKAGE V2

Date: 2026-10-01
Status: PREPARED BEFORE SECOND PREFLIGHT; NO MEASUREMENT AUTHORIZATION

## Purpose

This package defines the independent review required AFTER the corrected
Second Premeasurement Preflight V2 succeeds and BEFORE any R_joint measurement
authorization may be created.

The reviewer must inspect the exact code commit reported by the second-preflight
artifact and the exact second-preflight run. The reviewer must not compute,
estimate, infer, or request R_joint.

## Frozen scientific scope

Population:
- C_F = 1,918 records / 764 clusters
- source manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`

Gate:
- R_joint >= 0.95
- PASS only if exact >=0.95 or a proven lower bound >=0.95
- FAIL only if exact <0.95 or proven upper bound <0.95
- otherwise INCONCLUSIVE

Claim scope:
**DEVELOPMENT FEASIBILITY / ADAPTIVELY CONSUMED QALB-2014 ORIGIN / NOT INDEPENDENT GENERALIZATION EVIDENCE**

## Prior independent-review decision

Previous decision:
`MODIFY BEFORE SECOND PREFLIGHT`

The previous review found five BLOCKER and five MAJOR issues.

## Remediation summary to audit

### Exposure/provenance

- A prior V1 technical scorer execution reached 500/1918 before cancellation.
- It produced no valid final scientific result.
- Human recollection of exposure to numerical values is UNKNOWN.
- The corrected cycle must not be described as untouched first execution.

Files:
- `MPSEF_MEASUREMENT_EXPOSURE_AUDIT_V1.md`
- `MPSEF_OPERATOR_EXPOSURE_ATTESTATION_V1.md`

### Population

Current cycle is explicitly:
- C_F = 1918 / 764.
- historical 317-record amendment does not govern this cycle.
- no population member was changed to rescue feasibility.

File:
`MPSEF_POPULATION_PRECEDENCE_DECISION_V1.md`

### Gold-blind executable-action legalizer

Frozen action-set SHA256:
`6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`

Corrected hypothesis-audit SHA256:
`b4736383019d017780a8bfe4b076a0cd742e71bccfbb50350da8fa59b7c9ac75`

Final source-only states:
- P1_OK = 1,806 / 1,918
- P1_PROTECTED_BLOCKED = 112 / 1,918
- P2_EXECUTION_FAILED = 1,918 / 1,918

P2 is non-executable because 1,918/1,918 frozen cases have GED-label count
different from morphology-word count. Frozen P2 text is retained historically
but is not regenerated or rescued in this cycle.

File:
`MPSEF_P2_GED_WORD_ALIGNMENT_PROVENANCE_AUDIT_V1.md`

### Protected invariants / ambiguity / reversibility

Corrected legalizer uses:
- derived protection map with Arabic/Latin units and %/٪;
- closed-boundary insertion blocking;
- exact protected signature preservation;
- all-optimal Levenshtein-path protection proof;
- fail-closed alignment work budget;
- exact apply/inverse source/output SHA proof.

Lock:
`MPSEF_SOURCE_ONLY_LEGALIZER_LOCK_V1R1.md`

### Diagnostic separation / R_raw

Frozen diagnostic artifact:
`2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e`

It is diagnostic-only and executable=false.

Lock:
`MPSEF_DIAGNOSTIC_COMPONENTS_LOCK_V1.md`

### Target/scorer v2

Corrected governing documents:
- `MPSEF_TARGET_FAMILY_MAP_V2.md`
- `MPSEF_TARGET_AND_MATCHING_CONTRACT_V2_AMENDMENT.md`

V2 explicitly preserves mixed punctuation+boundary targets and separates:
source-only execution alignment, source-only diagnostic evidence, and
gold-aware evaluation-only M2 matching.

Corrected core/scorer must be reviewed for:
- punctuation-only vs mixed target classification;
- no a/m/p punctuation bug;
- SPLIT/MERGE preservation when mixed with punctuation;
- no-op / alternative-reference fail-closed behavior;
- duplicate target-credit rejection;
- whole-action oracle only;
- scoring failure -> exact [L,U] uncertainty;
- R_clean;
- complete-sentence repair;
- family/macro accounting;
- weak-family retention;
- per-sentence audit;
- candidate-set statistics;
- source-only diagnostic R_raw isolation.

The scorer library CLI itself must remain unable to execute project measurement.

### One-shot measurement guard

The corrected measurement architecture must enforce:

1. authorization/review metadata read from trigger commit;
2. exact second-preflight code commit checkout;
3. authorization-only + corrected-review-only diff after code commit;
4. exact implementation/contract hashes verified;
5. source-only evidence verified;
6. all non-gold smoke tests rerun;
7. durable `acad-pass/mpsef-rjoint-v2-consumed` status written;
8. only AFTER successful durable claim may project gold be downloaded;
9. cancellation/failure after claim consumes the experiment permanently;
10. no sequential rerun;
11. fixed experiment ID:
   `MPSEF-RJOINT-V2-CF1918-20261001-A`.

Files:
- `MPSEF_RJOINT_EXPERIMENT_ID_V2.json`
- `mpsef_measurement_guard_v2.py`
- `mpsef_cf_gold_projection_v2.py`
- `mpsef_rjoint_measurement_v2.py`
- `.github/workflows/phase2-mpsef-rjoint-measurement-v2.yml`

### Long-process observability

Every long process must publish:
- processed / total / percent;
- last progress time;
- stale duration;
- process liveness;
- final return code.

The measurement progress status must never expose metric values.

## Required second-preflight evidence

The reviewer must inspect the exact:
- second-preflight code commit SHA;
- GitHub run ID;
- artifact digest;
- summary JSON SHA256;
- 22/22 C01-C22 results;
- implementation hash map;
- contract hash map.

Second-preflight success alone does NOT authorize measurement.

## Reviewer decision

Allowed final decisions:

- `GO TO MEASUREMENT AUTHORIZATION`
- `MODIFY BEFORE AUTHORIZATION`
- `STOP / INVALID DESIGN`

A GO must mean only that the frozen one-shot measurement may be authorized.
It must NOT authorize selector training, AUTO_SAFE, reserved sets, or Phase 3.

The final report MUST end with exactly one line:

`DECISION: <GO TO MEASUREMENT AUTHORIZATION | MODIFY BEFORE AUTHORIZATION | STOP / INVALID DESIGN>`

## Forbidden actions

Do not:
- compute R_joint;
- read any measurement result from prior invalid attempts;
- weaken 95%;
- restore P2 by regenerating corrected proposals;
- change C_F;
- open reserved/internal sets;
- train a selector;
- alter executable bundles using gold;
- use R_raw to create an action;
- change timeout/protection/matching after seeing metrics.
