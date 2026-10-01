# ACAD_PASS PRE-STAGE1 FRESH RESEARCH RE-BASELINE V2

Date: 2026-10-01
Status: FROZEN PRE-STAGE1 ARCHITECTURE DECISION
Gold/reference use: NONE
Project-source Stage1: NOT YET RUN

## 1. Purpose

Reassess the Arabic correction candidate architecture after the complete source-free Stage0 PASS, using fresh 2025-2026 research and implementation evidence before materializing or executing the deterministic Stage1 source-only packet.

The decision target is:
KEEP / REPAIR / REPLACE / ADD COMPLEMENT / DEFER

for:
- P1 control;
- P2_V2;
- P3_V1;
- possible P4;
- possible MP-SEF V4 consensus;
- LLM-based proposer roles;
- protection policy;
- evaluation architecture.

## 2. Current internal evidence entering this decision

Source-free Stage0 closure:

- B01 synthetic identity: 20/20 PASS.
- B01 real-model source-free: PASS.
- B02 registry/action-set: 17/17 PASS.
- M01 P3 role: 4/4 PASS.
- M03 shadow protection: 10/10 PASS.
- M04/M05 scorer V3 synthetic preflight: PASS.

No project source, new project gold/reference, R_joint, or Stage1 execution was used to reach this architecture decision.

Current candidate families:

### P1
`P1_CONTROL_SWEET_QALB14_NOPNX_ITER2`

Family:
SWEET / text editing.

### P2_V2
`P2_V2_ARABART_GED_MORPH_WORDALIGNED`

Family:
autoregressive Seq2Seq / AraBART + GED + morphology.

### P3_V1
`P3_V1_SWEET_NOPNX2_PNX1`

Family:
SWEET cascade extension.

Important:
P1 and P3 are RELATED and count as one architecture family for any future support/voting interpretation.

Therefore the current roster contains only TWO materially different architecture families:
1. SWEET
2. Seq2Seq+GED/morphology

## 3. Fresh 2025-2026 external evidence

### 3.1 Arabic SWEET / text editing

Alhafni & Habash, ACL 2025:
`Enhancing Text Editing for Grammatical Error Correction: Arabic as a Case Study`

Relevant findings:
- strong Arabic GEC benchmark performance;
- iterative correction helps up to approximately two iterations for MSA;
- separating non-punctuation and punctuation correction helps;
- the published strong cascade is NoPnx iterations followed by Pnx;
- heterogeneous ensembles outperform individual systems;
- text-editing inference is substantially faster than previous Arabic GEC systems;
- public code/models/data exist.

Implementation freshness:
the public CAMeL-Lab/text-editing repository remains active in 2026.
Latest observed repository commit:
`4d552ca3ae98029550f27fc52aa1b22883e16e61`
dated 2026-02-12.
The repository also contains an ensemble experiment implementation from 2025.

Consequence:
P1 remains a strong current control.
P3 remains justified as a cascade candidate, but not as independent evidence from P1.

### 3.2 Arabic Seq2Seq + GED/morphology

Alhafni et al., EMNLP 2023:
`Advancements in Arabic Grammatical Error Detection and Correction: An Empirical Investigation`

Relevant findings:
- Seq2Seq Arabic GEC is strong;
- GED auxiliary conditioning can improve GEC;
- contextual morphology can help;
- public Arabic-GEC code/models exist.

Implementation freshness:
the public CAMeL-Lab/arabic-gec repository remains available and maintained as a public artifact, although its latest code push is older than text-editing.

Consequence:
P2_V2 is not selected because it is the newest system.
It is selected because it is a technically repaired, reproducible, heterogeneous architecture family.

### 3.3 Arabic grammar/LLM evidence

Nahw, EACL 2026:
current LLMs still show substantial deficiencies in Arabic grammar understanding, detection, correction, and explanation.

A 2026 PeerJ Arabic GEC/explanation study shows that targeted fine-tuning/prompting can improve LLM performance, but output-format, reproducibility, cost, model drift, and evaluation comparability remain concerns.

Earlier Arabic GEC LLM work also found fully fine-tuned task-specific models can outperform much larger instruction-following LLMs.

Consequence:
general LLMs remain diagnostic/adversarial/reviewer candidates, not sole primary proposer or safety verifier.

### 3.4 Edit-level voting / minimal-edit evidence

Recent GEC evidence outside Arabic shows:
- edit-level majority voting can reduce over-correction;
- minimal-edit/conservative objectives matter;
- overcorrection is a real failure mode when generative models are optimized for broader rewriting.

Consequence:
MP-SEF V4 consensus remains scientifically plausible.
However, current ACAD_PASS has only two independent architecture families.
P1 and P3 cannot be counted as independent votes.

Therefore consensus should remain deferred until source-only diversity is measured and a third genuinely independent family is considered if needed.

### 3.5 Newer Arabic ensemble / selector evidence

ArbESC+ (2025 preprint) reports combining multiple Arabic GEC systems, including:
- AraT5;
- ByT5;
- mT5;
- AraBART;
- AraBART+Morph+GEC;
- text editing;

with learned edit selection/conflict resolution.

This supports the architectural idea that heterogeneous candidate families can complement one another.

However:
- it is preprint evidence;
- no official implementation repository was found in the fresh GitHub search performed for this re-baseline;
- a learned selector introduces a new leakage/overfitting/control surface;
- adding selector learning before the candidate space is source-only frozen would contradict current ACAD_PASS governance.

Consequence:
do NOT add a learned selector now.
Treat ArbESC+ as design evidence for a later V4 lane.

### 3.6 Potential third independent family

Fresh Arabic transformer research continues to show strong AraT5/AraBART/mT5 family results.
A recent multitask Arabic GEC/explanation line (MTAGEC) also suggests newer AraT5-derived models may become useful independent candidates.

Potential P4 families:
- AraT5;
- ByT5;
- a reproducible newer Arabic-specific GEC model;
- another architecture materially different from both SWEET and P2_V2.

Consequence:
P4 is a serious future option, but adding it BEFORE Stage1 would expand implementation/provenance/runtime cost without first knowing whether P1/P2_V2/P3 already provide meaningful legal diversity.

## 4. Maximum-effort architecture brainstorm

### Option A — P1 only

Benefit:
lowest complexity.

Risk:
effective single-family candidate architecture; poor diversity ceiling.

Decision:
KEEP as control, NOT sufficient as final redesign by itself.

### Option B — P1 + P2_V2

Benefit:
two genuinely heterogeneous families.

Risk:
P2 may add little legal marginal diversity despite architectural difference.

Decision:
PROCEED to source-only Stage1.

### Option C — P1 + P2_V2 + P3

Benefit:
tests published NoPnx->Pnx cascade behavior and punctuation/full-correction marginal contribution.

Risk:
P3 correlated with P1 and can increase activity/protection burden without independent evidence.

Decision:
PROCEED as OPTIONAL candidate in Stage1.
Never count P1+P3 as two independent votes.

### Option D — add P4 now

Potential benefit:
third independent family; future family-quorum consensus becomes possible.

Risks:
- more runtime/provenance complexity;
- external benchmark strength may not translate to ACAD_PASS legal candidate diversity;
- current Stage1 exists specifically to measure whether more diversity is needed.

Decision:
DEFER before Stage1.
Research P4 immediately after Stage1 if evidence shows insufficient two-family diversity or if consensus is pursued.

### Option E — V4 training-free family-aware consensus now

Potential benefit:
precision-first correction; consistent with recent edit-voting literature.

Critical limitation:
only two independent architecture families currently exist.
A 2-of-2 rule may be too conservative.
A 1-of-2 rule provides no consensus benefit.
Counting P1 and P3 separately would inflate correlated evidence.

Decision:
DEFER until after Stage1.
If later pursued, strongly prefer architecture-family-aware support rather than raw proposer count.

### Option F — learned edit selector now

Potential benefit:
can exploit complementary edits.

Risks:
- selector training leakage;
- target-wise overfitting;
- conflict resolution complexity;
- new calibration and validation burden;
- breaks the clean source-only candidate-space freeze.

Decision:
DEFER / DO NOT IMPLEMENT NOW.

### Option G — general LLM as P4 now

Potential benefit:
potential broad grammatical knowledge.

Risks:
- weaker reproducibility;
- model/API drift;
- expensive inference;
- over-rewriting;
- weaker minimal-edit control;
- Arabic grammar deficiencies remain documented.

Decision:
DEFER from primary Stage1 roster.
Keep diagnostic/reviewer role.

## 5. Frozen pre-Stage1 component decisions

### P1_CONTROL
Decision:
**KEEP**

Reason:
strong current Arabic evidence, fast, mature, frozen, reproducible, required baseline/control.

### P2_V2
Decision:
**KEEP / PROCEED TO STAGE1**

Reason:
- root provenance defect repaired;
- source-free real-model Stage0 PASS;
- architecturally heterogeneous relative to SWEET;
- strongest current opportunity to measure complementary candidate diversity.

No quality claim is made.

### P3_V1
Decision:
**KEEP AS OPTIONAL / PROCEED TO STAGE1**

Reason:
published cascade rationale and low marginal cost when P1 parent output is reused.

Constraints:
- same SWEET family as P1;
- no independent-vote interpretation;
- final protection evaluated original source -> P3 final output.

### P4
Decision:
**DEFER**

Trigger to reopen:
- Stage1 reveals weak P2 marginal legal contribution;
- current roster yields mostly one-family behavior;
- Stage2/consensus design needs a third independent family;
- P3 is largely redundant;
- a clearly reproducible superior Arabic-specific model becomes available.

Preferred research order if reopened:
1. AraT5/ByT5 or another non-SWEET, non-current-P2 family;
2. newer reproducible Arabic-specific GEC such as an MTAGEC-class system;
3. frozen open LLM only if minimal-edit/reproducibility controls are strong.

### MP-SEF V4 consensus
Decision:
**DEFER**

Reopen only after Stage1 source-only diversity report.

If reopened:
- count architecture families, not raw proposers;
- P1/P3 together <= one SWEET-family support;
- training-free consensus should be investigated before learned selection;
- conflicting/overlapping edits require an independent contract.

### Learned selector
Decision:
**DEFER**

No selector training before candidate-space freeze and independent review.

### General LLM proposer
Decision:
**DEFER FROM PRIMARY ROSTER**

Allowed:
diagnostic/adversarial/reviewer work under separate controls.

### Protection
Decision:
**KEEP CURRENT AUTHORITATIVE POLICY + SHADOW DIAGNOSTICS**

Do not relax protection based on synthetic shadow findings.
Stage1/Stage2 may quantify ordinal-only blocking source-only.

### Evaluation
Decision:
**KEEP R_joint/whole-action primary architecture for the next authorized evaluation version**

Possible supplemental future diagnostics:
- newer edit-level metrics;
- external robustness benchmarks;
- family diversity measures.

Do not replace the frozen primary construct based solely on newer metrics.

## 6. Why Stage1 is now justified

Stage1 is source-only and descriptive.

It can answer the missing architecture questions without consuming gold:

1. Does P2_V2 produce distinct legal candidates relative to P1?
2. Is P3 mostly duplicate of P1 or does the Pnx stage add legal marginal outputs?
3. How much candidate-set size increases after exact dedup?
4. How much protection blocks each family?
5. How often is V3 blocking attributable only to global ordinal logic under the shadow diagnostic?
6. What are runtime/provenance costs?
7. Does the roster justify P4 research before Stage2?

These are exactly the unknowns that external literature cannot answer for ACAD_PASS.

## 7. Stage1 authorization boundary

This re-baseline authorizes only the NEXT ENGINEERING STEP:
materialize and freeze the deterministic source-only Stage1 packet and implement/freeze Stage1 proposer runners.

It does NOT yet authorize gold-aware measurement.

Before Stage1 execution:
- deterministic packet manifest must be frozen;
- P2_V2 Stage1 runner must bind B01 identities;
- P3 runner must bind exact P1 parent output;
- registry/action builder must bind Canonical V2;
- shadow protection diagnostics must be source-only;
- progress monitoring/resource accounting must be active;
- no gold/reference available to workflow.

## 8. Current classification

Compared with the pre-review architecture:

**IMPROVED**

Improvement is methodological/architectural, not linguistic.

Concrete evidence:
- complete source-free Stage0 gates now PASS;
- P2_V2 real-model path executes reproducibly after a documented repair;
- registry/action semantics are version-separated;
- P3 correlation is explicitly controlled;
- protection overblocking can now be measured without relaxing safety;
- scorer M04/M05 defects are corrected in V3.

New/remaining risks:
- P2_V2 may add little legal diversity;
- P3 may be mostly redundant;
- current roster has only two independent architecture families;
- protection may materially constrain useful candidate availability;
- a P4 may become necessary before meaningful family consensus;
- Stage1 runtime/provenance may expose further implementation defects.

## 9. Engineering forecast

Engineering estimate, not a statistical probability:

- confidence in reaching a scientifically defensible architecture: approximately 90%;
- residual architecture/implementation risk: approximately 10%.

Do NOT interpret this as:
- probability R_joint will pass;
- probability of linguistic success;
- measured model accuracy.

Primary next-risk concentration:
candidate diversity and protected-candidate availability, not the already-repaired P2 word-alignment defect.

## 10. Exact next sequence

1. freeze deterministic Stage1 packet manifest (128 UIDs / 128 clusters), source-only;
2. inspect/implement P2_V2 Stage1 runner;
3. inspect/implement P3 Stage1 runner using exact P1 parent output;
4. implement/freeze generic V4 action builder against Canonical B02 V2;
5. integrate M03 shadow diagnostics;
6. add progress/resource monitoring;
7. run Stage1 source-only only;
8. freeze Stage1 report;
9. perform another architecture re-baseline:
   - retain/drop/modify P2_V2;
   - retain/defer P3;
   - decide whether P4 research is required;
   - decide whether V4 consensus remains deferred;
10. still do not open new gold until that decision and independent authorization are frozen.

## 11. References considered

- Alhafni, B. & Habash, N. (2025). Enhancing Text Editing for Grammatical Error Correction: Arabic as a Case Study. ACL 2025.
- Alhafni, B. et al. (2023). Advancements in Arabic Grammatical Error Detection and Correction: An Empirical Investigation. EMNLP 2023.
- Mubarak, H. et al. (2026). Nahw: A Comprehensive Benchmark of Arabic Grammar Understanding, Error Detection, Correction, and Explanation. EACL 2026.
- Recent 2026 edit-level majority-voting work on GEC over-correction.
- Recent minimal-edit / preference-optimization GEC work.
- Recent Arabic LLM GEC/explanation evaluation work.
- Recent Arabic transformer and multitask GEC work including AraT5/AraBART family evidence.
- ArbESC+ (2025 preprint) as design evidence for heterogeneous edit selection; not used as authoritative implementation evidence.
