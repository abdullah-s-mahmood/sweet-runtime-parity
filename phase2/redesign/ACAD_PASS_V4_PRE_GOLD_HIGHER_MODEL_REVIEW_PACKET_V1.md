# ACAD_PASS V4 PRE-GOLD HIGHER-MODEL ADVERSARIAL REVIEW PACKET V1

Date: 2026-10-02
Status: FROZEN REVIEW PACKET / NO GOLD
Requested verdict: PROCEED / MODIFY / BLOCK

## 1. Review objective

Adversarially review the frozen ACAD_PASS V4 pre-gold development-measurement design and its source-free scorer implementation BEFORE any project gold/reference is loaded.

Do not evaluate linguistic correction quality.
Do not request or inspect QALB gold.
Do not redesign the whole ACAD_PASS product.
Focus only on whether the measurement design is safe, internally coherent, and ready for a development-feasibility gold-aware run.

## 2. Authoritative evidence

Read in this order:

1. `phase2/redesign/MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1.md`
2. `phase2/redesign/ACAD_PASS_POST_STAGE2_FRESH_RESEARCH_REBASELINE_V1.md`
3. `phase2/redesign/MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2_LOCK.md`
4. `phase2/redesign/MPSEF_RJOINT_V4_SOURCE_FREE_PREFLIGHT_CLOSURE_LOCK_V1.md`
5. `phase2/redesign/mpsef_rjoint_score_v4.py`
6. `phase2/redesign/mpsef_rjoint_v4_synthetic_preflight.py`
7. historical comparison only: `phase2/redesign/mpsef_rjoint_score_v3.py`
8. inherited target/matcher core: `phase2/redesign/mpsef_rjoint_core_v2.py`

Frozen scorer SHA256:
`b9fdbe205e6e00082b51a7ee16c74d0010c4bbe50406ad58d2f6f9e166db7513`

Frozen synthetic harness SHA256:
`cb07b046fbd36f2afd0c27f46efd3f7561a42f2ac90b9f4ac5f477e8dd56b8b3`

Frozen synthetic result SHA256:
`4eb8c2510fd62b50ff3a557018bc58d52853e53e4625389572308e62b39585d2`

Inherited core SHA256:
`b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`

Synthetic preflight:
**20/20 PASS**

## 3. Frozen architecture facts

Population if later authorized:
- C_F = 1,918 UIDs / 764 clusters
- development-feasibility only
- historical partial technical gold exposure exists
- NOT a clean independent holdout

Frozen V4 proposer roster:
- P1 = SWEET no-punctuation path
- P2 = AraBART + GED/morph word-aligned path
- P3 = SWEET punctuation-enabled extension

Architecture families:
- SWEET_QALB14 = P1 + P3
- SEQ2SEQ_GED_MORPH = P2

P1 and P3 MUST NOT count as two independent family votes.

Action set:
- KEEP always present
- up to 3 legal proposer outputs
- max 4 literal whole actions after exact-string dedup
- source-only legalizer already frozen
- gold-aware scorer consumes legal actions only
- scorer MUST NOT repair, regenerate, normalize, merge, or synthesize actions

Frozen current decisions:
- P1 KEEP
- P2 KEEP
- P3 KEEP as same-family alternate
- P4 DEFER
- learned selector DEFER
- family consensus DEFER
- generic LLM judge DEFER
- protection KEEP
- whole-action semantics KEEP

## 4. Why V4 scorer exists

Historical V3 is incompatible with V4:
- V3 groups only P1/P2/PAIR
- V3 expects <=3 actions
- V4 supports KEEP+P1+P2+P3 = 4 actions
- V4 requires same-family P1/P3 aggregation without double counting

V4 groups:
- P1
- P2
- P3
- SWEET
- SEQ2SEQ
- ROSTER

ROSTER means:
best available WHOLE legal action among the frozen action set.
It is an oracle candidate-availability diagnostic, NOT an executable selector.

## 5. Mandatory semantics

### M04 uncertainty
If N frozen primary targets exist and all eligible action-scoring calls fail:
- lower = 0
- upper = N

Never collapse to [0,0].

### M05 whole-action rule
For grouped error families such as BOUNDARY={SPLIT,MERGE}:
- maximize one whole action over the union of relevant target indices
- never sum maxima from different actions

The same rule must govern proposer/family/ROSTER interpretation.

### Target population
- target identities and denominator are frozen before scoring any action
- target-build failure aborts measurement
- punctuation-only targets are separated from the primary denominator
- no post-result gate weakening

### Reference boundary
QALB is single-reference.
Therefore:
- unsupported != linguistically wrong
- extra edit != automatically invalid
- all quantities are reference-relative
- no general correctness claim

## 6. Source-free preflight coverage

The 20 synthetic tests cover:
- KEEP-only
- P1/P2/P3 individual groups
- full 4-action set
- P1/P3 exact dedup with dual provenance
- P1/P3 different actions but one family
- cross-family exact agreement
- M04 all-fail and mixed-failure intervals
- M05 grouped whole-action regression
- proposer isolation
- SWEET access to P1/P3
- no same-family double vote
- ROSTER no synthetic fusion
- zero-target
- clean-sentence candidate activity
- punctuation separation
- scorer-failure evidence
- source/action identity fail-closed

GitHub status:
`acad-pass/v4-rjoint-source-free-preflight = success`

## 7. Review questions

Classify each finding as:
- BLOCKER
- MAJOR
- MINOR
- NOTE

Answer every question.

### A. Denominator / leakage
1. Is the target denominator truly frozen before action scoring?
2. Can any action-scoring failure alter the target denominator?
3. Can action availability or provenance affect which gold targets are constructed?
4. Is historical partial C_F gold exposure described strongly enough to prevent clean-holdout claims?

### B. Action/provenance semantics
5. Can P1 consume a P2-only action, or vice versa?
6. Can P3 accidentally create an independent-family vote separate from P1?
7. Does exact-string dedup retain multi-proposer/multi-family provenance correctly?
8. Can KEEP-equivalent proposer output be treated as non-KEEP evidence?
9. Is ROSTER clearly an oracle candidate-availability group rather than a selector?

### C. M04 failure intervals
10. Does all-actions-fail preserve [0,N]?
11. Can one failed action improperly make the lower bound optimistic?
12. Can failures in one group contaminate another group's interval?

### D. M05 whole-action semantics
13. Can the scorer ever combine target hits from different actions into one score?
14. Do error-family/group diagnostics use max(sum for one action), not sum(max across actions)?
15. Is any future family comparison vulnerable to synthetic fusion?

### E. Clean/extra-edit interpretation
16. Are complete-repair and clean-recovery quantities well defined?
17. Is clean-sentence extra-edit activity sufficiently separated from target recovery?
18. Is there any place where single-reference "extra" could be misreported as linguistic error?

### F. Punctuation
19. Is punctuation-only separation deterministic and frozen?
20. Could MIXED_PUNCT_LINGUISTIC targets be accidentally excluded?
21. Is any punctuation treatment inconsistent between target construction and scoring?

### G. Architecture boundaries
22. Can P4 access gold in this cycle?
23. Can selector training access gold in this cycle?
24. Can family consensus be activated from this scorer run?
25. Can a generic LLM judge become hidden primary gold?

### H. Identity / reproducibility
26. Are source/action population identity checks adequate before scoring?
27. Are scorer/core/test hashes sufficient to freeze semantics?
28. What additional runtime/dependency identity must be frozen before real measurement?
29. Should the exact legal-action-set SHA be asserted inside the measurement runner?
30. Is any required failure/progress artifact missing?

## 8. Required verdict format

Return:

### VERDICT
Exactly one:
- PROCEED
- MODIFY
- BLOCK

### FINDINGS
For every finding:
- ID
- severity
- exact file/function/semantic location
- why it matters scientifically
- repair required before gold? yes/no
- minimal repair

### QUESTIONS
Answer questions 1-30 explicitly.

### GOLD AUTHORIZATION
Exactly one:
- SAFE TO AUTHORIZE DEVELOPMENT GOLD AFTER SPECIFIED PRECONDITIONS
- NOT SAFE TO AUTHORIZE GOLD

### REQUIRED PRECONDITIONS
Short exact list.

Do not propose opening Confirmation/Holdout/Internal Evaluation/Stress.
Do not compute or infer a real performance number.
Do not suggest weakening frozen gates because the current architecture looks promising.
