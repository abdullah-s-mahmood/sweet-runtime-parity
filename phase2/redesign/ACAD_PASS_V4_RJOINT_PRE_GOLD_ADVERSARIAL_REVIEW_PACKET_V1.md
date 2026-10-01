# ACAD_PASS V4 R_JOINT PRE-GOLD ADVERSARIAL REVIEW PACKET V1

Date: 2026-10-02
Status: READY FOR INDEPENDENT/HIGHER-MODEL REVIEW
Requested verdict: PROCEED / MODIFY / BLOCK

## 1. Reviewer mission

Review the proposed ACAD_PASS V4 development-feasibility measurement BEFORE any real C_F gold/reference is loaded.

Do not evaluate linguistic quality.
Do not suggest opening additional reserved datasets.
Do not optimize for attractive metrics.

Primary question:

**Is the frozen V4 scorer/contract methodologically safe enough to permit one reference-relative, development-only gold-aware measurement on the already consumed C_F development population?**

## 2. Required files

Read in this order:

1. `phase2/redesign/MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1.md`
2. `phase2/redesign/MPSEF_RJOINT_V4_SOURCE_FREE_PREFLIGHT_CLOSURE_LOCK_V1.md`
3. `phase2/redesign/mpsef_rjoint_score_v4.py`
4. `phase2/redesign/mpsef_rjoint_v4_synthetic_preflight.py`
5. `phase2/redesign/mpsef_rjoint_core_v2.py`
6. `phase2/redesign/MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2_LOCK.md`
7. `phase2/redesign/ACAD_PASS_POST_STAGE2_FRESH_RESEARCH_REBASELINE_V1.md`

Historical comparison when needed:
- `phase2/redesign/mpsef_rjoint_score_v3.py`
- `phase2/redesign/MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_EXECUTION_CONTRACT_V1.md`
- `phase2/redesign/MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_EXECUTION_CONTRACT_V1_AMENDMENT_A1.md`

## 3. Frozen population and scientific boundary

C_F:
- 1,918 UIDs
- 764 clusters
- source-only manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`

Important:
- C_F is DEVELOPMENT only.
- Historical invalidated attempts technically exposed part of C_F gold.
- Any future result MUST say:
  `ADAPTIVELY_CONSUMED DEVELOPMENT / REFERENCE_RELATIVE / NOT INDEPENDENT GENERALIZATION`

Still forbidden:
- Confirmation
- Holdout
- A7'ta reserve
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC
- P4 execution
- selector training
- family consensus
- generic LLM judge

## 4. Frozen action roster

P1:
`P1_CONTROL_SWEET_QALB14_NOPNX_ITER2`

P2:
`P2_V2_ARABART_GED_MORPH_WORDALIGNED`

P3:
`P3_V1_SWEET_NOPNX2_PNX1`

Families:
- P1 + P3 = `SWEET_QALB14`
- P2 = `SEQ2SEQ_GED_MORPH`

KEEP is a system action, not a model family.

Action semantics:
- whole legal sentence outputs only;
- exact literal dedup;
- maximum current unique action count = 4;
- no edit-level fusion;
- P1/P3 never count as two independent family votes.

## 5. Stage2 source-only evidence motivating measurement

Legal non-KEEP family availability:
- at least one family: 1,843/1,918 = 96.09%
- BOTH families: 1,736/1,918 = 90.51%
- SWEET only: 67
- P2-family only: 40
- NONE: 75

Cross-family exact legal non-KEEP agreement:
- 167 UIDs
- 144 clusters

P3:
- MIXED_FROM_P1: 1,800/1,918 = 93.85%

P2:
- generation-completeness fail-closed: 22/1,918
- upstream identity/morph/GED/GEC-tokenization stages passed on all 1,918 before generation boundary.

These are source-only structural facts, not correctness evidence.

## 6. Why V3 was not reused

Historical scorer V3:
- only P1/P2/PAIR groups;
- assumes <=3 actions;
- no P3 family-aware aggregation.

V4 requires:
- P1/P2/P3 proposer groups;
- SWEET/SEQ2SEQ family groups;
- ROSTER whole-action oracle group;
- <=4 actions.

V4 preserves:
- M04 all-scorers-fail interval semantics;
- M05 one-whole-action aggregation.

## 7. Source-free preflight

GitHub status:
`acad-pass/v4-rjoint-source-free-preflight = success`

20/20 synthetic tests PASS.

Frozen SHA256:
- scorer:
  `b9fdbe205e6e00082b51a7ee16c74d0010c4bbe50406ad58d2f6f9e166db7513`
- synthetic harness:
  `cb07b046fbd36f2afd0c27f46efd3f7561a42f2ac90b9f4ac5f477e8dd56b8b3`
- core:
  `b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`

No project source/gold was loaded by the synthetic preflight.

## 8. Specific adversarial questions

Classify each finding:
- BLOCKER
- MAJOR
- MINOR
- NOTE

### Q1 — target denominator
Does `score_population_v4` freeze the entire target population before evaluating any action, with no candidate-dependent denominator?

### Q2 — historical exposure
Is the claim scope sufficiently conservative for an adaptively consumed C_F development population?

### Q3 — action-set identity
Is consuming the already frozen V4 legal action set, rather than rerunning legalizer under gold, sufficient to prevent gold-dependent action availability?

### Q4 — proposer isolation
Can P1, P2, or P3 receive credit from an action that does not carry that proposer's provenance?

### Q5 — same-family aggregation
Can P1/P3 accidentally create two independent support votes anywhere in scorer semantics?

### Q6 — family aggregation
Does SWEET correctly maximize over KEEP/P1/P3 whole actions without combining edits across P1 and P3?

### Q7 — ROSTER semantics
Does ROSTER maximize one complete legal whole action, or is there any path that could synthesize target hits across separate actions?

### Q8 — M04
If all eligible actions fail scoring for N>0 targets, is uncertainty preserved as [0,N] everywhere relevant?

### Q9 — M05
For grouped error families such as BOUNDARY={SPLIT,MERGE}, is one whole action maximized over the union rather than sum(max) from different actions?

### Q10 — clean recovery
Is `best_clean_bounds` conservative enough when scoring failures occur?

### Q11 — complete repair
Are complete-repair lower/upper bounds correctly defined under failed action scoring?

### Q12 — zero-target sentences
Are clean/no-primary-target sentences handled without inventing successful complete-repair credit?

### Q13 — punctuation
Is excluding PUNCTUATION_ONLY from the primary denominator while freezing it as a separate denominator methodologically clear and non-adaptive?

### Q14 — mixed punctuation/linguistic edits
Does the inherited target scope prevent mixed punctuation+linguistic edits from being silently discarded?

### Q15 — single-reference limitation
Are `extra` and clean-recovery results sufficiently labeled reference-relative so they cannot be interpreted as linguistic invalidity?

### Q16 — scorer-failure identity
Are scoring failures preserved per UID/group/action rather than converted to zero-credit certainty?

### Q17 — family-specific recovery
Does family-specific target recovery use one whole action per group and sentence?

### Q18 — source/hash identity
What additional immutable identity checks, if any, are necessary before gold execution?

### Q19 — hidden leakage
Is there any path by which real gold results could affect P4, selector training, consensus activation, protection legality, or action-set construction during the same measurement?

### Q20 — review verdict
Should the next step be:
- PROCEED to a frozen C_F gold-aware development measurement,
- MODIFY the scorer/contract first,
- or BLOCK the measurement design?

## 9. Reviewer output format

Return:

1. **VERDICT:** PROCEED / MODIFY / BLOCK
2. **BLOCKER findings**
3. **MAJOR findings**
4. **MINOR findings**
5. **Synthetic regressions additionally required**
6. **Exact contract/scorer amendments required**
7. **Whether source-free preflight must be rerun**
8. **Whether real C_F gold loading may be authorized after remediation**
9. **Any wording required to prevent overclaiming**

Do not provide or infer a linguistic performance score.

## 10. Low-token prompt for a higher model

> You are performing an adversarial methodological review of ACAD_PASS before any real gold/reference is opened. Read the files listed in `ACAD_PASS_V4_RJOINT_PRE_GOLD_ADVERSARIAL_REVIEW_PACKET_V1.md` in order. Verify denominator freezing, whole-action semantics, P1/P3 same-family handling, M04/M05 uncertainty, punctuation policy, historical development exposure, single-reference interpretation, action-set/hash identity, and leakage barriers. Return only a structured verdict PROCEED/MODIFY/BLOCK with BLOCKER/MAJOR/MINOR findings, exact required amendments, additional synthetic regressions, and whether source-free preflight must be rerun. Do not score model quality and do not authorize reserved datasets, P4, selector training, consensus, or an LLM judge unless the frozen contract explicitly permits it.
