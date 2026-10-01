# MP-SEF V4 PRE-GOLD DEVELOPMENT MEASUREMENT CONTRACT V1

Date: 2026-10-02
Status: FROZEN FOR SOURCE-FREE IMPLEMENTATION AND ADVERSARIAL REVIEW
Gold/reference loading: FORBIDDEN UNTIL REVIEW/PREFLIGHT PASS
Primary population if later authorized: C_F = 1,918 UIDs / 764 clusters
Claim scope: DEVELOPMENT FEASIBILITY / REFERENCE-RELATIVE / NOT INDEPENDENT GENERALIZATION

## 1. Governing evidence

Post-Stage2 research:
`ACAD_PASS_POST_STAGE2_FRESH_RESEARCH_REBASELINE_V1.md`

Stage2 protocol-complete lock:
`MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2_LOCK.md`

Frozen source identities:
- C_F manifest:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- P1:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- P2:
  `87dd3600293b215172f5a75dc7485915013963aa3e661310ea1adac08b9ddba7`
- P3:
  `02f9bd2555b1b9f350665179dcd96dd6accf532355a269b38ef4d099ea25d4ec`
- V4 legal action sets:
  `e38393abb36734d3882e29a78f3b33c80718791957b9b8c0c6e8a8ab77f6e138`

## 2. Purpose

Build and validate a new `R_joint V4` scorer compatible with the frozen V4 action roster before any real reference/gold is opened.

The scorer will later measure reference-relative development feasibility only if a later gate authorizes C_F gold loading.

It will not select models, train a selector, activate consensus, or add P4.

## 3. Why scorer V3 cannot be reused directly

Historical scorer:
`mpsef_rjoint_score_v3.py`

Frozen V3 fixes remain valuable:
- M04 uncertainty interval when all action scorers fail;
- M05 one-whole-action aggregation.

But V3 is incompatible with V4 because:
- V3 groups only P1/P2/PAIR;
- V3 expects action-set size <=3;
- V4 supports KEEP+P1+P2+P3 = up to 4 literal whole actions;
- V4 requires family semantics with P1+P3 = SWEET_QALB14.

Therefore no real V4 measurement may call V3 unchanged.

## 4. Frozen V4 roster

Proposers:
- P1_CONTROL_SWEET_QALB14_NOPNX_ITER2
- P2_V2_ARABART_GED_MORPH_WORDALIGNED
- P3_V1_SWEET_NOPNX2_PNX1

Families:
- SWEET_QALB14 = P1 + P3
- SEQ2SEQ_GED_MORPH = P2

System action:
- KEEP

Rules:
- P1 and P3 never count as two independent family votes.
- exact-source proposer output is KEEP-equivalent.
- P4 is absent.
- no learned selection.

## 5. Action semantics

Primary action is a complete legal whole-sentence output.

Action set:
- KEEP always exists;
- zero to three proposer outputs after authoritative source-only legality and exact-string dedup;
- maximum unique action count = 4.

Gold-aware scorer MUST consume the already frozen legal action set.
It MUST NOT rerun or weaken the protection legalizer.

Every metric that asks "can this group recover target(s)?" must maximize over ONE complete action.
No union/sum of target hits across different actions may manufacture a synthetic hybrid output.

## 6. V4 scorer groups

Required groups:

### Proposer groups
- P1
- P2
- P3

For proposer P:
eligible actions are:
- KEEP;
- legal actions whose provenance contains P.

### Family groups
- SWEET
- SEQ2SEQ

SWEET:
- KEEP;
- legal actions with provenance from P1 and/or P3.

SEQ2SEQ:
- KEEP;
- legal actions with P2 provenance.

Same-family provenance does not increase family vote count.

### ROSTER group
- KEEP;
- every legal whole action in the frozen V4 action set.

ROSTER is an oracle candidate-availability group, not an automated selector.

## 7. Frozen target semantics

Before scoring any action:
1. load the later-authorized gold for the exact frozen UID population;
2. build the complete target population;
3. freeze target identities and denominator;
4. abort if target construction fails;
5. exclude or include punctuation only under the exact preregistered policy below.

Primary target scope:
- non-punctuation primary targets, preserving historical MP-SEF primary semantics.

Punctuation:
- report separately;
- do not silently merge into the primary denominator.

Any future change requires a new contract version before gold execution.

## 8. Required primary reference-relative measures

For each proposer, family and ROSTER group:

- target recovery interval;
- clean target recovery interval;
- complete repair lower/upper bound;
- family-specific target recovery;
- scoring-failure count;
- candidate-availability gate state where applicable.

ROSTER additionally reports:
- best whole-action primary recovery;
- best whole-action clean recovery;
- complete-repair availability;
- action-set size distribution inherited from frozen source-only evidence.

All results are QALB-reference-relative.

## 9. Mandatory V3 safety semantics retained

### M04
If target count is N and every eligible action scoring call fails:
- lower = 0
- upper = N

Never collapse to [0,0].

### M05
For a grouped error family such as BOUNDARY={SPLIT,MERGE}:
- maximize one whole action over the union of relevant target indices;
- never sum maxima from different actions.

Additional-target and cluster evidence uses the same one-whole-action rule.

## 10. Reference incompleteness boundary

QALB may contain only one valid correction path.

Therefore:
- reference-unsupported edit != linguistically wrong;
- extra edit != automatically invalid edit;
- measured precision/extra-edit quantities are reference-relative;
- no source-independent linguistic-validity claim is allowed.

JELV/CLEME/optimal-transport-inspired metrics may be added only as separately labeled supplemental diagnostics after separate validation.
They cannot replace the primary frozen measurement in this cycle.

No LLM judge is authorized.

## 11. Historical gold exposure

Earlier invalidated measurement attempts exposed at least part of C_F to technical gold-aware execution.

Therefore all C_F results must carry:
`ADAPTIVELY_CONSUMED DEVELOPMENT / NOT CLEAN HOLDOUT`

C_F remains useful for architecture development-feasibility measurement.
It is not independent confirmation/generalization evidence.

Confirmation/Holdout/A7'ta reserve/Internal Evaluation/Stress remain governed by their existing locks.

## 12. Source-free implementation gate

Before real gold loading, implement:
`mpsef_rjoint_score_v4.py`

Required source-free synthetic regressions:

1. action set with KEEP only;
2. KEEP+P1;
3. KEEP+P2;
4. KEEP+P3;
5. full 4-action set;
6. exact duplicate P1/P3 output retaining both provenance entries;
7. P1/P3 different outputs but same family;
8. P2 exact agreement with a SWEET output;
9. all action scorers fail with N>0 -> [0,N];
10. one successful + one failed action -> conservative interval;
11. BOUNDARY split/merge whole-action regression preventing sum(max);
12. proposer group cannot consume another proposer's exclusive action;
13. SWEET family can consume either P1 or P3 actions;
14. P1+P3 never produce two independent-family votes;
15. ROSTER uses one action, never synthetic edit fusion;
16. zero-target sentence;
17. clean sentence with unnecessary candidate activity;
18. punctuation-only target separation;
19. scoring error preserves UID and failure evidence;
20. input population/action-set identity mismatch fails closed.

Minimum result:
**20/20 PASS**

## 13. Provenance lock required before gold

Freeze:
- scorer source SHA256;
- core/matcher source SHA256;
- synthetic test source SHA256;
- Python version;
- dependency lock;
- action-set SHA256;
- source manifest SHA256;
- target-builder version;
- error-family map version;
- punctuation policy;
- population UID SHA;
- output schema version.

Any change after preflight invalidates authorization and requires preflight/review again.

## 14. No-current-cycle authorizations

Until a later explicit lock:
- no C_F gold/reference load;
- no R_joint V4 real measurement;
- no selector training;
- no family consensus;
- no P4 execution;
- no generic LLM judge;
- no Confirmation;
- no Holdout;
- no A7'ta reserve;
- no INTERNAL_EVALUATION;
- no STRESS_DIAGNOSTIC.

## 15. Architecture decisions frozen for this contract

- P1: KEEP
- P2: KEEP
- P3: KEEP AS SAME-FAMILY ALTERNATE
- P4: DEFER
- selector: DEFER
- consensus: DEFER
- protection: KEEP
- whole-action semantics: KEEP

## 16. Adversarial review gate

After synthetic scorer PASS and before real gold:
perform an adversarial review focusing on:
- denominator leakage;
- family/provenance semantics;
- same-family double counting;
- scorer failure intervals;
- whole-action aggregation;
- clean/extra-edit interpretation;
- punctuation handling;
- single-reference wording;
- historical exposure wording;
- action-set identity;
- any path by which P4/selector/consensus could see gold.

Allowed verdicts:
- PROCEED
- MODIFY
- BLOCK

Any BLOCKER or semantics-changing MAJOR requires amendment/version change and rerun of synthetic preflight.

## 17. Exact next work

1. implement source-free `mpsef_rjoint_score_v4.py`;
2. implement 20-case synthetic harness;
3. run until genuine PASS;
4. freeze hashes;
5. prepare focused higher-model review packet;
6. do not open gold before review resolution.
