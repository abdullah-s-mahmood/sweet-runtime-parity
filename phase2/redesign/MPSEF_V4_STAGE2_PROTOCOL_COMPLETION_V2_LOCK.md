# MP-SEF V4 STAGE2 PROTOCOL COMPLETION V2 LOCK

Date: 2026-10-02
Status: PASS / SOURCE-ONLY PROTOCOL COMPLETION VALIDATED

## Purpose

Close the protocol-output gaps discovered after the successful Stage2 full-C_F source-only legalizer/action-set run without rerunning P1, P2, P3, or the legalizer.

Historical successful analysis is preserved unchanged:
- run: `36923877787`
- artifact: `11192953283`
- artifact digest: `sha256:d773c8b65f607e06ce811d44d7e18deaf49c0da0c17428122d2258b043f82c4b`

Protocol-completion implementation:
- script: `phase2/redesign/mpsef_v4_stage2_protocol_completion_v2.py`
- script commit: `fbf9aa760fb787fbebb835a13b0940f83ba15bc6`
- workflow commit: `7a5715402ba90cdb14636073b037344885d2266a`

The GitHub connector did not expose the push-triggered V2 workflow run through its available run-status interface. Therefore the same deterministic V2 postprocessor was executed directly against the exact frozen artifact bytes after all input SHA256 identities were revalidated. This is an execution-observability limitation only; it is not a model-quality or scientific failure.

## Frozen input identity revalidation

- C_F manifest:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- P1:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- P2:
  `87dd3600293b215172f5a75dc7485915013963aa3e661310ea1adac08b9ddba7`
- P3:
  `02f9bd2555b1b9f350665179dcd96dd6accf532355a269b38ef4d099ea25d4ec`
- V1 diversity summary:
  `00e8d48a42edf129d4fdcf46a02624cec1f893e9c27f23880d156957d0e9bcac`
- V1 proposer rows:
  `6ff90a0b9ee0201d72caba144474b50e34ccb22796bd2f161e4b104c0aaea42d`
- V1 action sets:
  `e38393abb36734d3882e29a78f3b33c80718791957b9b8c0c6e8a8ab77f6e138`
- V1 failures:
  `48cfd2c2574fa56411f1899c15ba1d5a84671eb43e3b875652192384c3081fa9`
- V1 runtime:
  `a2811fff2b8952f9c1714eb913a532592e4d7ccc688305f67ed288019f85f236`

## V2 result

Result:
**PASS**

Protocol gaps closed:
- exact contract artifact naming;
- independent FAMILY_SUMMARY artifact;
- SOURCE_ONLY_INDEPENDENT_NONKEEP_FAMILY_COUNT;
- SOURCE_ONLY_FAMILY_AVAILABILITY_STATE;
- SOURCE_ONLY_CROSS_FAMILY_EXACT_OUTPUT_AGREEMENT;
- family dominance diagnostics;
- per-proposer UID/cluster state accounting;
- per-proposer failure-reason matrices;
- P2 full-population stage diagnostics;
- P1→P3 change burden;
- Stage-B classifier counts over all frozen categories.

## Full-C_F source-only family evidence

Population:
- UIDs: **1,918**
- clusters: **764**

Independent legal non-KEEP family count:
- 0 families: **75 / 1,918 = 3.91%**
- 1 family: **107 / 1,918 = 5.58%**
- 2 families: **1,736 / 1,918 = 90.51%**

Family availability:
- NONE: **75**
- SWEET_ONLY: **67**
- SEQ2SEQ_GED_MORPH_ONLY: **40**
- BOTH_FAMILIES: **1,736**

Legal non-KEEP availability from at least one family:
- **1,843 / 1,918 = 96.09%**

Cross-family exact legal non-KEEP output agreement:
- UIDs: **167**
- clusters: **144**
- shared actions: **167**

This exact agreement is structural/literal evidence only and is not correctness evidence.

Family leave-one-out:
- remove SWEET_QALB14:
  - non-KEEP UIDs: 1,843 → **1,776**
  - delta: **67 UIDs**
  - non-KEEP clusters: 749 → **738**
  - delta: **11 clusters**
  - unique-action-sum delta: **3,268**
- remove SEQ2SEQ_GED_MORPH:
  - non-KEEP UIDs: 1,843 → **1,803**
  - delta: **40 UIDs**
  - non-KEEP clusters: 749 → **740**
  - delta: **9 clusters**
  - unique-action-sum delta: **1,609**

Interpretation:
both independent families provide non-redundant source-only legal availability. P1 and P3 remain one SWEET family and MUST NOT count as two independent votes.

## Per-proposer source-only protocol evidence

P1:
- executable: **1,918 / 1,918**
- legal: **1,806**
- nonlegal: **112**
- protection-blocked: **112**
- changed vs source: **1,838**

P2_V2:
- executable: **1,896 / 1,918**
- failed: **22**
- legal: **1,790**
- nonlegal: **128**
- protection-blocked: **106**
- changed vs source: **1,882**

P3_V1:
- executable: **1,918 / 1,918**
- legal: **1,768**
- nonlegal: **150**
- protection-blocked: **150**
- changed vs source: **1,914**

## P2 full-population diagnostic evidence

All 1,918 rows:
- morphology PASS: **1,918**
- GED tokenization PASS: **1,918**
- zero-token-word failures: **0**
- single-word-over-budget failures: **0**
- unknown/unmapped label failures: **0**
- GEC tokenization failures: **0**
- GEC input-too-long failures: **0**
- model-interface proof rows: **1,918**
- generation incomplete/fail-closed rows: **22**
- generation ceiling rows: **22**
- terminal EOS evidence available: **1,918**

The 22 P2 failures remain fail-closed capacity/generation-completeness evidence, not linguistic-quality failures.

## P3 Stage-B V1 source-only domains

Classifier:
`MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1`

- NO_CHANGE_FROM_P1: **61**
- PUNCTUATION_ONLY_FROM_P1: **57**
- BOUNDARY_ONLY_FROM_P1: **0**
- LEXICAL_ONLY_FROM_P1: **0**
- MIXED_FROM_P1: **1,800**
- UNAVAILABLE_COMPARISON: **0**

This confirms the Stage1 warning at full population: P3 is overwhelmingly a mixed transformation relative to P1, not a punctuation-only cascade.

## V2 deterministic output hashes

- proposer rows V1:
  `6ff90a0b9ee0201d72caba144474b50e34ccb22796bd2f161e4b104c0aaea42d`
- legal action sets V1:
  `e38393abb36734d3882e29a78f3b33c80718791957b9b8c0c6e8a8ab77f6e138`
- diversity summary V1:
  `a18a5ad6c463d98887c1431930411a66accca07a01eb67f7bb9cf8dc5fa16ccc`
- family summary V1:
  `5a351a297c64810a9dc912e5b876e9fb409dfa19e91f9ef49fc6f5a18d677e24`
- failures V1:
  `48cfd2c2574fa56411f1899c15ba1d5a84671eb43e3b875652192384c3081fa9`
- runtime V1:
  `a2811fff2b8952f9c1714eb913a532592e4d7ccc688305f67ed288019f85f236`
- protocol completion V2:
  `94caf9a49a85a78b056ac2674ad421cc0e7d413f40cb0ad1219d10d72331818f`

## Scientific boundary

- source-only: true
- new gold/reference consulted: false
- quality metric computed: false
- R_joint computed: false
- selector trained: false
- family consensus activated: false
- P4 executed: false

## Classification

**IMPROVED STRONGLY IN FULL-POPULATION SOURCE-ONLY ARCHITECTURE EVIDENCE / LINGUISTIC QUALITY STILL UNMEASURED**

## Next mandatory gate

Perform fresh post-Stage2 deep research + maximum-effort architecture brainstorming.

The next decision MUST reconsider:
- P4: KEEP DEFERRED / ADD / REPLACE / REPAIR;
- whether two independent families are sufficient for the next measurement architecture;
- P3 retention despite its overwhelmingly MIXED Stage-B domain;
- whether a third reproducible family is now justified;
- whether any source-only evidence warrants family consensus activation;
- whether gold-aware measurement may be authorized next.

No gold/R_joint/selector/consensus is authorized by this lock.
