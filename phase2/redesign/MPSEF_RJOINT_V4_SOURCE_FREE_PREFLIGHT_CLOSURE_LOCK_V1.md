# MP-SEF R_JOINT V4 SOURCE-FREE PREFLIGHT CLOSURE LOCK V1

Date: 2026-10-02
Status: PASS / SOURCE-FREE / PRE-GOLD
Real project gold loaded: false
Real R_joint computed: false

## 1. Governing contract

`phase2/redesign/MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1.md`

Contract commit:
`2a749a5a41d5f8e8fd57b596d5c6d25a23c7f986`

## 2. Implementation

Scorer:
`phase2/redesign/mpsef_rjoint_score_v4.py`

Scorer commit:
`3edee5e48c96c2930246c35783312686cf894e8b`

Synthetic harness:
`phase2/redesign/mpsef_rjoint_v4_synthetic_preflight.py`

Harness commit:
`cf55653873c561018b5e0102c582d74510cc008c`

Workflow:
`.github/workflows/phase2-mpsef-v4-rjoint-source-free-preflight.yml`

Observable workflow commit:
`df097dffee26b155cb013206e71d6594b3734df4`

## 3. GitHub execution result

Commit status:
`acad-pass/v4-rjoint-source-free-preflight = success`

Additional successful identity status contexts:
- `acad-pass/v4-rjoint-scorer-sha256`
- `acad-pass/v4-rjoint-test-sha256`
- `acad-pass/v4-rjoint-result-sha256`

The GitHub connector confirms these contexts as SUCCESS.

## 4. Frozen source SHA256 identities

Scorer:
`b9fdbe205e6e00082b51a7ee16c74d0010c4bbe50406ad58d2f6f9e166db7513`

Synthetic preflight:
`cb07b046fbd36f2afd0c27f46efd3f7561a42f2ac90b9f4ac5f477e8dd56b8b3`

Historical core/matcher helper:
`phase2/redesign/mpsef_rjoint_core_v2.py`

Core SHA256:
`b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`

Git blob identities:
- scorer: `dbe1261d658163a4d66a27bd71311e625bf45d72`
- synthetic preflight: `f0a8e81964a67043d5f98199abbfc7fbbb7c2d5d`
- core: `2c83eab97c9ad47f0d5a044d3cd6650525eb02ef`

Runtime:
- Python 3.10
- source-free preflight uses only Python standard-library code on the V4 path
- no model inference
- no project source load
- no project gold load

## 5. Frozen target/matching semantics inherited from core V2

Matching version:
`MPSEF_RJOINT_M2_EVALUATION_MATCH_V2`

Target-family map:
`MPSEF_TARGET_FAMILY_MAP_V2`

Error families:
- INSERT
- DELETE
- SPLIT
- MERGE
- SUBSTITUTE
- COMPLEX

Primary punctuation rule:
targets with `scope == PUNCTUATION_ONLY` are separated from the primary non-punctuation denominator.

## 6. V4 group semantics validated

Required groups:
- P1
- P2
- P3
- SWEET
- SEQ2SEQ
- ROSTER

Family mapping:
- P1 + P3 = `SWEET_QALB14`
- P2 = `SEQ2SEQ_GED_MORPH`

ROSTER:
oracle candidate-availability group only; not a selector.

Maximum frozen action capacity:
KEEP + P1 + P2 + P3 = 4 literal whole actions after source-only legality/dedup.

## 7. Synthetic preflight result

Required:
20/20 PASS

Observed:
**20/20 PASS**

Validated regressions:
1. KEEP only.
2. KEEP+P1.
3. KEEP+P2.
4. KEEP+P3.
5. full four-action set.
6. P1/P3 literal dedup with retained dual provenance.
7. P1/P3 different outputs but one SWEET family.
8. cross-family exact output agreement.
9. M04 all-action scorer failure preserves [0,N].
10. M04 success+failure preserves conservative interval.
11. M05 BOUNDARY whole-action rule prevents sum(max).
12. proposer action isolation.
13. SWEET can use P1 or P3 actions.
14. P1/P3 never create two independent-family votes.
15. ROSTER never synthesizes target fusion across different actions.
16. zero-target sentence.
17. clean-sentence candidate activity.
18. punctuation target separation.
19. scorer failure evidence preservation.
20. population/action identity mismatch fails closed.

## 8. Scorer architecture

The V4 scorer:
- freezes the full target population before scoring;
- has no embedded project-gold loader;
- requires gold to be explicitly supplied by a caller only after later authorization;
- preserves M04 and M05 semantics;
- supports up to four actions;
- supports proposer and family groups;
- reports reference-relative intervals;
- keeps punctuation separate;
- records complete-repair availability;
- records scoring failures;
- does not train a selector;
- does not activate consensus;
- does not use P4.

## 9. Scientific boundary

This closure proves:
- implementation semantics are synthetically consistent with the frozen V4 contract;
- same-family double counting is blocked;
- action fusion across whole outputs is blocked;
- failure uncertainty remains fail-closed.

It does NOT prove:
- linguistic correction quality;
- QALB target recovery;
- complete repair on C_F;
- precision/recall;
- R_joint;
- generalization;
- selector quality;
- consensus quality.

## 10. Classification

**IMPROVED STRONGLY IN PRE-GOLD MEASUREMENT READINESS / PERFORMANCE UNMEASURED**

## 11. Next mandatory gate

Before any C_F gold/reference load:

1. adversarially review the V4 measurement contract and scorer;
2. focus on denominator leakage, provenance/family semantics, M04/M05, punctuation, reference incompleteness, historical exposure, and any hidden path to selector/P4/consensus;
3. allowed verdict: PROCEED / MODIFY / BLOCK;
4. any semantics-changing MAJOR or any BLOCKER requires amendment and synthetic rerun.

No real gold/R_joint is authorized by this lock.
