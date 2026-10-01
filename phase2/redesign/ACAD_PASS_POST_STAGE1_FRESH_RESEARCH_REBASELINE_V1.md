# ACAD_PASS POST-STAGE1 FRESH RESEARCH REBASELINE V1

Date: 2026-10-01
Scope: Post-Stage1 architecture rebaseline before Stage2/P4/V4-consensus decisions
Status: FROZEN DECISION RECORD

## 1. Starting point

V4 Stage1 is protocol-complete.

Frozen Stage1 facts:
- P1 parity32: 32/32 PASS
- P2_V2 parity32: 32/32 PASS
- P3_V1 parity32: 32/32 PASS
- P1 legal: 120/128
- P2_V2 legal: 122/128
- P3_V1 legal: 119/128
- unique legal marginal contribution P1/P2/P3: 101/115/111 UIDs
- 123/128 UIDs have at least one legal non-KEEP candidate
- 98/128 UIDs have four unique legal actions including KEEP
- P3 is same SWEET family as P1 and is mostly MIXED_FROM_P1 (118/128)

No gold/reference has been used.
R_joint has not been computed.

## 2. Research question

Before Stage2, determine whether a materially independent P4 should be added now or whether the current roster is sufficient for full-population source-only scaling.

P4 acceptance criteria:
1. public trained checkpoint, not only a base model;
2. reproducible inference path;
3. frozen provenance/weights possible;
4. materially independent architecture family;
5. no requirement for large retraining merely to enter the roster;
6. no unresolved licensing/provenance ambiguity;
7. source-only execution possible without project gold.

## 3. MTAGEC audit

Source:
- paper: Multi-task Arabic GEC / MTAGEC (2025/2026 publication cycle)
- repository: https://github.com/Zainabobied/MTAGEC

Findings:
- repository contains training/evaluation code, config, data tooling, and model implementation;
- models/ contains implementation code, not released trained MTAGEC weights;
- README workflow is training-oriented and depends on the large ExplAGEC resource;
- no official frozen pretrained MTAGEC GEC checkpoint was found in the repository during this audit;
- no directly usable official Hugging Face MTAGEC GEC checkpoint was found during fresh search.

Architecture independence:
HIGH.

Immediate reproducibility:
INSUFFICIENT for ACAD_PASS P4 admission.

Decision:
DEFER.

## 4. AraT5/AraT5v2 audit

Sources:
- UBC-NLP/AraT5 and AraT5v2 public base checkpoints;
- 2025 Neural Computing and Applications Arabic GEC transfer-learning study;
- recent Arabic GEC work using AraT5v2 with synthetic/distilled data.

Findings:
- AraT5/AraT5v2 base checkpoints are public and reproducible;
- recent Arabic GEC studies fine-tune them for GEC;
- fresh search did not identify an official released GEC-finetuned AraT5/AraT5v2 checkpoint matching the reported experiments that can be directly frozen as P4;
- using the base checkpoint would require our own GEC training and would create a new training study rather than a source-only proposer integration.

Architecture independence:
HIGH.

Immediate P4 readiness:
INSUFFICIENT.

Decision:
DEFER unless a frozen GEC checkpoint is later published or a separate training phase is explicitly authorized.

## 5. ByT5 audit

Findings:
- ByT5 appears in recent Arabic GEC system-combination literature as an evaluated component;
- fresh search did not identify a released Arabic-GEC-finetuned ByT5 checkpoint with sufficient provenance for immediate ACAD_PASS freezing;
- generic ByT5/base or unrelated Arabic correction checkpoints do not satisfy the P4 criterion.

Architecture independence:
HIGH if GEC-finetuned checkpoint exists.

Immediate P4 readiness:
INSUFFICIENT.

Decision:
DEFER.

## 6. mT5/mBART audit

Findings:
- public base and Arabic-adapted mT5 checkpoints exist;
- published Arabic GEC studies fine-tune mT5/mBART;
- fresh search did not identify a suitable official Arabic-GEC-finetuned mT5 checkpoint that can be directly frozen for this project;
- unrelated translation/summarization checkpoints are not admissible as GEC proposers.

Architecture independence:
HIGH for mT5 if independently fine-tuned.

Immediate P4 readiness:
INSUFFICIENT.

Decision:
DEFER.

## 7. Older independent Transformer/capsule GEC audit

Repository:
https://github.com/aimanmutasem/Arabic-GEC

Findings:
- repository README describes a Transformer + capsule/EM-routing Arabic GEC system;
- "trained models" directory contains a README with Google Drive links rather than in-repository weights;
- listed L2R and R2L entries reuse the same Google Drive IDs in the README;
- README states that the whole code files would be released later;
- environment is old (PyTorch 1.6 / torchtext 0.6 era).

Architecture independence:
HIGH.

Provenance/runtime confidence:
TOO LOW for immediate P4 admission.

Decision:
REJECT FOR CURRENT P4 ROSTER; retain only as historical fallback candidate.

## 8. 2026 ZAEBUC reproducibility release audit

Repository:
https://github.com/CAMeL-Lab/zaebuc

The Arabic GEC runner explicitly uses:
- GED: CAMeL-Lab/camelbert-msa-zaebuc-ged-13
- GEC: CAMeL-Lab/arabart-zaebuc-gec-ged-13

Therefore the 2026 release does not add a materially independent third GEC family for ACAD_PASS; it remains the same CAMeLBERT GED + AraBART seq2seq family lineage as P2.

Decision:
NOT P4-INDEPENDENT.

## 9. ArbESC+ relevance

ArbESC+ reports combination of AraT5, ByT5, mT5, AraBART, AraBART+Morph+GEC, and text-editing systems.

Interpretation for ACAD_PASS:
- supports the design principle that heterogeneous architecture families can add value;
- does not by itself provide the frozen checkpoints required for immediate P4 admission;
- its learned edit-selection approach is design evidence only at this stage;
- it does not authorize a learned selector before source-only/full-population evidence and later gold-aware authorization.

## 10. Architecture decision

### P4 before Stage2

Decision:
**DEFER**

Reason:
No freshly identified third-family Arabic GEC system simultaneously satisfies independence, trained-checkpoint availability, provenance freezing, and low integration debt.

Adding a weakly reproducible or self-trained P4 now would reduce evidence quality and confound the next stage.

### Stage2

Decision:
**AUTHORIZE SOURCE-ONLY FULL-C_F STAGE2 WITH CURRENT ROSTER**

Roster:
- P1_CONTROL_SWEET_QALB14_NOPNX_ITER2
- P2_V2_ARABART_GED_MORPH_WORDALIGNED
- P3_V1_SWEET_NOPNX2_PNX1
- KEEP

Purpose:
scale legality, execution, protected-touch, deduplication, redundancy, candidate-set size, and family/action diversity from Stage1 128 to the frozen full C_F population.

Stage2 MUST NOT:
- open project gold/reference;
- compute R_joint;
- score linguistic correctness;
- train a selector;
- treat P1 and P3 as independent family votes;
- weaken protection or execution gates;
- replace frozen Stage1 artifacts.

### V4 consensus

Decision:
**DEFER FAMILY-CONSENSUS ACTIVATION**

Reason:
the current roster contains only two independent architecture families:
1. SWEET family: P1 + P3
2. AraBART+GED/morph family: P2_V2

P1 and P3 may contribute distinct actions, but they count as one architecture family for any future family-support logic.

### P4 reopening trigger

Reopen P4 after Stage2 if any of the following occurs:
1. full-C_F candidate diversity collapses materially versus Stage1;
2. one family dominates legal coverage or marginal contribution;
3. too many UIDs have only one independent-family non-KEEP action;
4. family-level consensus is required for the next quality gate;
5. a reproducible trained AraT5/ByT5/mT5/MTAGEC checkpoint becomes available;
6. an explicit P4 training phase is authorized with separate data/provenance controls.

## 11. Comparison versus pre-research state

Architecture decision quality:
**IMPROVED**

P4 readiness:
**WORSENED RELATIVE TO OPTIMISTIC ASSUMPTION** because fresh audit did not find an admissible ready checkpoint.

Current roster evidence quality:
**IMPROVED / SUFFICIENT FOR SOURCE-ONLY STAGE2**

Linguistic quality:
**UNCHANGED / UNMEASURED**

## 12. Engineering forecast

For source-only Stage2 with the current frozen roster:
- engineering optimism estimate: 94%
- engineering risk estimate: 6%

These are engineering judgment estimates, not scientific probabilities.

Primary Stage2 risks:
- P2 generation-capacity edge cases at full C_F scale;
- protection-block rates may change outside the 128-case packet;
- P3 may show higher redundancy or protected-touch burden at full scale;
- two-family architecture may be insufficient for later consensus even if Stage2 execution is successful.

## 13. Next action

Build and freeze the Stage2 source-only full-C_F execution contract before running any proposer.

No gold/reference or quality scoring is authorized by this record.
