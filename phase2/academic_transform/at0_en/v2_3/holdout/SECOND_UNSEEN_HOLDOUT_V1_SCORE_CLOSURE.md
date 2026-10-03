# AT0-EN V2.3 — SECOND_UNSEEN_HOLDOUT_V1 One-Shot Score Closure

Date: 2026-10-03  
Status: **CLOSED / BOTH_FAIL / HOLDOUT CONSUMED DEVELOPMENT EVIDENCE**

## 1. Frozen run identity

- workflow: `AT0-EN V2.3 Second Unseen Holdout One-Shot Score`
- run id: `37136722184`
- trigger commit: `44728dfb5fcf3e1bf211ba330b618741c2d382de`
- run attempt: 1
- conclusion: **SUCCESS** (execution only)
- artifact id: `11278888488`
- artifact name: `at0-en-v2-3-second-unseen-one-shot-37136722184`
- artifact SHA-256: `8b66dbf18b0b7f0939f66754c803b3753f1bc9a1cc912051129ecbeca77f5ae9`

No model inference occurred.

The execution order was preserved:
1. label-blind predictions;
2. prediction hash freeze;
3. label evaluation;
4. final evidence hash freeze;
5. artifact upload.

## 2. Frozen evidence hashes

Bound inputs:
- verifier SHA-256: `d82af97d276131477ab2f8c452f24e3302703f54b856a8ad46547af59d7ec0da`
- inputs SHA-256: `b1633df5e0418082a990945dfc92a267f6cdc8c943b385d7edc2d8b9181f551c`
- labels SHA-256: `9936377336708dbeaf88b7ee83a8ae5fb4272013129041332094dfa625345a9b`
- source cases SHA-256: `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`

Generated evidence:
- predictions SHA-256: `e36a99873e7f7d87a63cc77c928109bf844a718ca20f5b09d5287378be081c25`
- predictions metadata SHA-256: `914d5ad414380a900ef1086edaef00eafb2fc1b285b2f539be3dee2cc8149fa8`
- prediction-hash record SHA-256: `139bd2c20893af8d924a7dee35c3b247a83f9abed319c704271a517ba1ccd5b6`
- score detail SHA-256: `2eea29e5f6e3e738484c2a3d723d649e2777c1aeff5f956902700092b2d23e4c`
- score summary SHA-256: `854b6ebbe9c3491d0d8957bde9b4f1d13d4327c5ca82e36616dc9b92114c7955`

Repository mirror of the frozen score summary:
`phase2/academic_transform/at0_en/v2_3/holdout/results/SECOND_UNSEEN_HOLDOUT_V1_SCORE_SUMMARY_FROZEN.json`

## 3. Pre-registered gates and result

Pre-registered safety gate:
- required adversarial escape: **0/24 = 0%**
- observed: **9/24 = 37.5%**
- result: **FAIL**

Pre-registered safe-control usability gate:
- required safe automatic acceptance: **>=9/12 = >=75%**
- observed: **3/12 = 25%**
- result: **FAIL**

Combined checkpoint:
**BOTH_FAIL**

Additional metrics:
- adversarial caught: **15/24 = 62.5%**
- adversarial escape: **9/24 = 37.5%**
- safe accepted: **3/12 = 25%**
- safe rejected/non-pass: **9/12 = 75%**
- exact binary correct: **18/36 = 50%**
- balanced accuracy: **43.75%**

Prediction counts:
- adversarial: 15 REJECT, 9 PASS_CANDIDATE
- safe controls: 3 PASS_CANDIDATE, 9 REJECT
- no REVIEW predictions were produced in this holdout score.

## 4. Escaped adversarial cases

Nine materially invalid cases passed as `PASS_CANDIDATE`:

1. `H2-EN01-A1` — scope binding shift
2. `H2-EN02-A2` — deployment-status invention
3. `H2-EN03-A1` — percentage/metric rebinding
4. `H2-EN04-A2` — density-direction shift
5. `H2-EN10-A1` — grouping-interval rebinding
6. `H2-EN10-A2` — metadata-scope reduction
7. `H2-EN11-A1` — forwarding-scope expansion
8. `H2-EN11-A2` — timestamp substitution
9. `H2-EN12-A1` — metric-label swap

All nine produced no finding under the frozen V2.3 verifier.

The dominant failure class is **relation rebinding under lexical preservation**: the correct words, values, symbols, or entities remain present, but they are attached to the wrong predicate, scope, agent, condition, unit, or output relation.

## 5. Safe-control false positives

Nine faithful controls were rejected:

- `H2-EN01-S1`
- `H2-EN02-S1`
- `H2-EN03-S1`
- `H2-EN05-S1`
- `H2-EN06-S1`
- `H2-EN08-S1`
- `H2-EN09-S1`
- `H2-EN11-S1`
- `H2-EN12-S1`

Observed causes include:
- word-order dependence;
- narrow lexical patterns;
- insufficient paraphrase equivalence handling;
- regex windows crossing neighboring relations;
- negation-scope confusion;
- failure to recognize equivalent verbs/phrases;
- overly literal relation templates.

This is not merely a threshold problem. The same representation produces both unsafe false negatives and excessive safe false positives.

## 6. Comparison with prior checkpoints

### Versus V2.3 known-failure regression

Known attacks:
- escape: **0/24 = 0%**

New temporally held-out attacks:
- escape: **9/24 = 37.5%**

Descriptive change:
- **+37.5 percentage points worse escape rate**

Safe acceptance:
- previous valid known controls: **11/11 = 100%**
- new safe controls: **3/12 = 25%**
- descriptive change: **-75 percentage points**

These are **not same-population comparisons**. They quantify the generalization gap exposed by the new holdout; they must not be interpreted as a within-population regression.

### Versus V2.2 independent red-team

V2.2 independent attacks:
- escape: **21/24 = 87.5%**

V2.3 second holdout:
- escape: **9/24 = 37.5%**

Descriptive difference:
- **-50 percentage points escape**

However, the attack sets differ, so this is not a valid causal or same-population improvement estimate. It is evidence that V2.3 is directionally stronger than the earlier rule-only verifier while still failing the current safety gate.

## 7. Scientific interpretation

The main conclusion is not that V2.3 needs more regex patterns.

The holdout demonstrates a structural limitation:

1. positive lexical evidence can coexist with a contradictory or rebound scientific relation;
2. local regex windows do not reliably identify which subject/predicate/object/qualifier belongs together;
3. handcrafted assertion patterns remain brittle under faithful paraphrase;
4. adding case-specific exceptions after each failure would overfit the consumed holdout and destroy the value of future validation.

Therefore V2.3 must **not** be patched against these 36 cases and then rescored as untouched evidence.

The holdout is now:
`CONSUMED DEVELOPMENT EVIDENCE / NOT UNTOUCHED HOLDOUT`

## 8. Fresh end-of-stage research

Relevant current research supports this interpretation:

- Jourdan et al., ACL 2025: scientific revision metrics that focus on similarity or instruction following do not reliably establish correctness; hybrid task-specific evidence is needed.
  https://aclanthology.org/2025.acl-long.335/

- Lu et al., ACL 2025, *Optimizing Decomposition for Optimal Claim Verification*: decomposition and verification must be aligned at appropriate atomicity; decomposition quality materially affects verification performance.
  https://aclanthology.org/2025.acl-long.254/

- Hu et al., NAACL 2025, *Decomposition Dilemmas*: decompose-then-verify can improve or degrade fact checking; decomposition introduces its own error/noise trade-off.
  https://aclanthology.org/2025.naacl-long.320/

- Pham et al., NAACL 2025, *Verify-in-the-Graph*: complex claim verification benefits from graph-style triplet representation and explicit entity/relation disambiguation.
  https://aclanthology.org/2025.naacl-long.268/

- Mujahid et al., ACL 2026: factuality metrics are unstable under meaning-preserving paraphrases and dense claims; multi-span reasoning and context-aware calibration are needed.
  https://aclanthology.org/2026.acl-long.1472/

The project result is consistent with these findings but remains project-specific evidence.

## 9. Higher-model consultation status

This is a high-stakes frozen-result interpretation point.

A separate stronger-model consultation tool is not exposed in the current chat environment. No external higher-model consultation is claimed. The current reasoning model performed the strategic review. If a separate higher-model review becomes available, this frozen packet is an appropriate escalation point.

## 10. Architecture decision

**DO NOT START HW1-EN.**

**DO NOT rerun this holdout.**

**DO NOT patch V2.3 case-by-case against the consumed holdout.**

Authorize the next stage as an offline architecture redesign:

`AT0-EN V2.4 — GENERALIZED SCIENTIFIC ASSERTION REPRESENTATION`

Design target:
- source-derived atomic assertions independent of case-specific regex templates;
- explicit relation schema: subject, predicate, object/value, unit, qualifiers, modality, polarity, scope, temporal condition, population, citation/equation binding;
- extraction uncertainty explicitly represented;
- contradiction and addition detection over normalized relations;
- paraphrase-tolerant matching separated from scientific relation identity;
- deterministic checks retained for exact quantities, equations, citations and structural invariants;
- any learned/NLI/LLM semantic component used only as separately calibrated evidence, never as sole safety oracle;
- new future holdout must be frozen after V2.4 is frozen and must not reuse this consumed set as untouched evidence.

No new model inference is authorized in this closure.

## 11. Completion reporting

Current one-shot scoring stage:
**100% COMPLETE**

Result classification:
**WORSENED ON UNSEEN GENERALIZATION / BOTH_FAIL**

Whole ACAD_PASS program:
**approximately 20% ±5% complete** as a planning estimate.

The negative result does not reduce completed research work, but it prevents advancement to the next product-validation blocks.

Major remaining blocks:
- V2.4 generalized verification redesign;
- a future new untouched validation set;
- higher-level review of verifier readiness;
- HW1-EN human-writing evaluation;
- cross-domain scientific fidelity;
- DOCX/document fidelity;
- voice;
- detector robustness;
- long-document evaluation;
- product/commercial usefulness and release engineering.

No reliable wall-clock completion promise is possible because the V2.4 gate can expose further redesign needs.
