# ACAD_PASS POST-STAGE2 FRESH RESEARCH REBASELINE V1

Date: 2026-10-02
Status: FROZEN RESEARCH / ARCHITECTURE DECISION BEFORE GOLD-AWARE MEASUREMENT
Stage2 source-only closure: `MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2_LOCK.md`

## 1. Trigger

Stage2 full-C_F source-only analysis is complete and protocol-complete.

Frozen source-only evidence:
- C_F: 1,918 UIDs / 764 clusters.
- legal non-KEEP from at least one family: 1,843/1,918 = 96.09%.
- BOTH independent families available: 1,736/1,918 = 90.51%.
- one family only: 107/1,918 = 5.58%.
- no legal non-KEEP family: 75/1,918 = 3.91%.
- cross-family exact legal non-KEEP output agreement: 167 UIDs / 144 clusters.
- P1/P3 remain one SWEET family.
- P2 remains SEQ2SEQ_GED_MORPH.
- P3 Stage-B MIXED_FROM_P1: 1,800/1,918 = 93.85%.
- P2 generation-completeness fail-closed rows: 22/1,918 = 1.15%.

No linguistic correctness claim follows from these source-only counts.

## 2. Fresh 2025-2026 research

### 2.1 Arabic text editing / SWEET remains strong and reproducible

Alhafni & Habash, ACL 2025:
- text-editing GEC for Arabic;
- public code and pretrained models;
- strong Arabic benchmark performance;
- reported >6x inference speed improvement over prior Arabic GEC systems;
- ensemble experiments show system combination can improve results.

Source:
- https://aclanthology.org/2025.acl-long.875/
- DOI 10.18653/v1/2025.acl-long.875
- https://github.com/CAMeL-Lab/text-editing

Consequence:
P1/P3 SWEET lineage remains technically justified, but P1 and P3 are not independent-family votes.

### 2.2 Arabic multi-system combination now has direct evidence

ArbESC+ (Alrehili & Alhothali, 2025 preprint):
- combines AraT5, ByT5, mT5, AraBART, AraBART+Morph+GEC and text-editing systems;
- formulates combination as edit selection with conflict resolution;
- reports F0.5 82.63 on QALB-14, 84.64 on QALB-15 L1 and 65.55 on QALB-15 L2.

Source:
- https://arxiv.org/abs/2511.14230
- DOI 10.48550/arxiv.2511.14230

Consequence:
multi-family proposal combination is scientifically plausible for Arabic.
It does NOT authorize ACAD_PASS learned selection because the exact trained proposer/checkpoint/provenance stack used by ArbESC+ is not frozen inside ACAD_PASS and our anti-leakage rules differ.

### 2.3 Edit-level voting and over-correction

Goto et al., BEA 2026:
- edit-level majority voting over multiple LLM candidates reduces over-correction;
- training-free;
- improves over greedy/MBR in most of nine non-Arabic benchmarks.

Source:
- https://aclanthology.org/2026.bea-1.60/
- DOI 10.18653/v1/2026.bea-1.60

Consequence:
edit-level agreement is a useful future mechanism, but the paper does not establish Arabic validity and does not justify counting same-family P1/P3 as independent votes.

### 2.4 Single-reference evaluation remains incomplete

JELV, AAAI 2026:
- explicitly addresses valid edits missing from single references;
- evaluates grammaticality, faithfulness and fluency;
- reports 90% agreement for its LLM-judge pipeline and 85% precision for a distilled validity classifier on its benchmark.

Source:
- https://ojs.aaai.org/index.php/AAAI/article/view/40761
- DOI 10.1609/aaai.v40i41.40761

Goto et al., TACL 2026:
- proposes evaluation based on optimally transporting edit representations.

Source:
- https://aclanthology.org/2026.tacl-1.77/
- DOI 10.1162/tacl.a.747

Consequence:
QALB single-reference scores must be described as reference-relative development evidence.
JELV/LLM judges are NOT promoted to primary ACAD_PASS gold and may only become supplemental after separate validation.

### 2.5 Arabic LLM grammar remains insufficiently reliable as an oracle

Nahw, EACL 2026:
- broad Arabic grammar benchmark covering understanding, GED, GEC and explanation;
- reports substantial deficiencies across evaluated LLMs;
- synthetic-data fine-tuning did not match natural high-quality data.

Source:
- https://aclanthology.org/2026.eacl-long.296/
- DOI 10.18653/v1/2026.eacl-long.296

Consequence:
a generic Arabic LLM must not become an automatic correctness oracle.

### 2.6 P4 candidates reassessed

#### Gemma-3-1B Arabic GEC

Public checkpoint:
`alnnahwi/gemma-3-1b-arabic-gec-v1`

Evidence:
- ~1B parameters / ~2GB BF16;
- public safetensors;
- deterministic greedy example path;
- MSA GEC intent;
- base family is materially independent of SWEET and AraBART/CAMeLBERT.

But model card states only:
`Dataset: Custom Arabic GEC dataset`

It does not provide enough provenance to exclude QALB overlap and does not provide a quantified QALB benchmark result.

Source:
- https://huggingface.co/alnnahwi/gemma-3-1b-arabic-gec-v1

Decision:
**P4_GEMMA = SOURCE-ONLY PROBE CANDIDATE ONLY / NOT GOLD-ELIGIBLE**

#### MTAGEC

Peer-reviewed 2025/2026 journal work:
- multi-task AraT5-based correction + explanation;
- ExplAGEC 21.8M synthetic pairs;
- code/data public;
- reported QALB-14 F0.5 80.02 and QALB-15 81.73.

Sources:
- DOI 10.1007/s44443-025-00354-2
- https://github.com/Zainabobied/MTAGEC

Repository quick-start requires training a checkpoint; a directly frozen trained correction checkpoint was not established by this audit.

Decision:
**MTAGEC = RESEARCH CANDIDATE / HIGHER INTEGRATION DEBT / NOT IMMEDIATE P4**

#### AraT5 / ByT5 / mT5 candidates from ArbESC+

They provide evidence that an additional seq2seq family can be useful in Arabic combination, but ACAD_PASS does not currently have a provenance-clean, frozen, trained P4 checkpoint from that work.

Decision:
**DEFER AS PRIMARY P4**

## 3. Maximum-effort architecture red-team

### Option A — add P4 before any gold-aware measurement

Potential benefit:
- enables a third materially independent family;
- could support future family-majority logic.

Problems:
- current C_F already has both existing families on 90.51% of UIDs;
- a third family is not needed merely for source-only availability;
- the best immediately runnable independent checkpoint (Gemma) has unresolved training provenance;
- adding P4 now increases architecture surface before measuring whether current actions are correct/useful.

Decision:
**DEFER**

### Option B — activate consensus now

Problems:
- only two independent frozen families exist;
- exact cross-family legal non-KEEP agreement is only 167/1,918 UIDs;
- P1/P3 cannot be counted separately;
- majority logic with two families is not a meaningful majority.

Decision:
**DEFER**

### Option C — train learned selector now

Problems:
- requires gold-aware learning;
- would couple architecture selection to consumed development data;
- violates current frozen boundary;
- literature support (e.g. ArbESC+) is not sufficient to waive ACAD_PASS leakage controls.

Decision:
**DEFER**

### Option D — remove P3 before measurement

Arguments for removal:
- 93.85% of P3 changes relative to P1 are MIXED;
- P3 adds protection burden;
- P3 is not an independent family.

Arguments against removal:
- P3 contributes a unique legal output on 1,598 UIDs;
- removing P3 makes 14 UIDs KEEP-only;
- the Stage2 redundancy rule is not satisfied;
- source-only evidence cannot decide correctness.

Decision:
**KEEP P3 AS SAME-FAMILY ALTERNATE / NOT AN INDEPENDENT VOTE**

### Option E — perform corrected gold-aware development measurement on current frozen V4 actions

Benefit:
- directly answers the unresolved question: whether source-only diversity corresponds to target recovery / complete repair / extra-edit burden;
- avoids architecture churn before evidence;
- preserves P4 as a later response to measured failure modes.

Risk:
- C_F is development evidence only and has historical partial gold exposure;
- QALB is single-reference;
- measurement scorer V3 is not compatible with V4 action capacity/family semantics.

Decision:
**PROCEED TO DESIGN AND SYNTHETIC VALIDATION OF V4 GOLD-AWARE SCORER, BUT DO NOT OPEN GOLD YET**

## 4. Critical scorer incompatibility discovered

Current:
`phase2/redesign/mpsef_rjoint_score_v3.py`

The scorer is not directly valid for Stage2 V4 because:
- it explicitly aggregates `P1`, `P2`, and `PAIR`;
- it assumes action-set size <=3;
- Stage2 V4 can contain KEEP + P1 + P2 + P3 = 4 actions;
- P1 and P3 must aggregate as one SWEET family without double-vote semantics.

Therefore:
**DO NOT RUN R_joint V3 DIRECTLY ON V4**

## 5. Frozen post-Stage2 architecture decision

- P1_CONTROL: **KEEP**
- P2_V2: **KEEP**
- P3_V1: **KEEP AS SAME-FAMILY ALTERNATE**
- P4 primary/gold-eligible: **DEFER**
- P4_GEMMA source-only probe: **RESERVE / DO NOT EXECUTE BEFORE FIRST V4 MEASUREMENT REVIEW**
- family consensus: **DEFER**
- learned selector: **DEFER**
- generic LLM judge: **DEFER FROM PRIMARY EVIDENCE**
- JELV/CLEME/OT-style metrics: **SUPPLEMENTAL CANDIDATES ONLY**
- authoritative protection: **KEEP**
- exact whole-action semantics: **KEEP**
- primary next technical task: **R_joint V4 scorer design + source-free synthetic validation**

## 6. V4 scorer requirements

The new scorer must:
1. preserve V3 M04 all-actions-fail uncertainty semantics;
2. preserve V3 M05 one-whole-action aggregation;
3. support 1+N legal actions, with current frozen N<=3 proposers;
4. support proposer-level P1/P2/P3 diagnostics;
5. support family-level SWEET_QALB14 and SEQ2SEQ_GED_MORPH diagnostics;
6. never count P1/P3 as two independent family votes;
7. score the full legal roster as an oracle action set only through one whole action at a time;
8. freeze target denominator before scoring;
9. preserve scorer failures as intervals;
10. report complete-repair and clean/extra-edit diagnostics;
11. keep punctuation policy explicit and frozen;
12. label all QALB outcomes DEVELOPMENT / REFERENCE-RELATIVE;
13. expose no gold to selector/P4/consensus;
14. pass source-free synthetic regression before any real gold is loaded.

## 7. Current classification

Compared with the pre-Stage2 architecture:

**IMPROVED**

Why:
- the need for P4 is now evidence-driven rather than assumed;
- both current independent families are shown to provide non-redundant legal availability;
- a new third-family public checkpoint was identified but correctly blocked from gold use due provenance uncertainty;
- the incompatible V3 scorer was caught before gold-aware execution.

Linguistic performance:
**STILL UNMEASURED**

## 8. Exact next gate

1. freeze V4 pre-gold measurement contract;
2. implement R_joint V4 source-free synthetic scorer/harness;
3. adversarially review the contract/scorer;
4. only after PASS may C_F gold be loaded for a development-feasibility measurement;
5. P4/selector/consensus remain closed during that measurement.
