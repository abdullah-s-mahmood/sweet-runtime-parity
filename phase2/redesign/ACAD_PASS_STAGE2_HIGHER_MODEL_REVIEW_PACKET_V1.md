# ACAD_PASS STAGE2 HIGHER-MODEL ARCHITECTURE REVIEW PACKET V1

Date: 2026-10-01
Purpose: adversarial review BEFORE Stage2 full-C_F execution
Gold/reference: MUST REMAIN CLOSED

## Frozen context

Project:
ACAD_PASS Arabic correction safety/evidence stack.

Vision:
Transform -> Protect -> Verify -> Drift -> Repair/Escalate -> Review -> Preserve -> Deliver.

Current milestone:
V4 Stage1 is protocol-complete.

Full C_F:
- 1,918 UIDs
- 764 clusters
- manifest SHA:
  051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193

Stage1 parity:
- P1: 32/32 PASS
- P2_V2: 32/32 PASS
- P3_V1: 32/32 PASS

Stage1 source-only:
- P1 legal 120/128
- P2 legal 122/128
- P3 legal 119/128
- unique legal marginal contribution: P1 101, P2 115, P3 111
- 123/128 have >=1 legal non-KEEP action
- 98/128 have 4 distinct actions including KEEP
- P3 is same SWEET family as P1
- P3 Stage-B relative to P1: 118/128 MIXED, 4 punctuation-only, 6 no-change

Independent architecture families:
1. SWEET_QALB14: P1 + P3
2. SEQ2SEQ_GED_MORPH: P2_V2

P4 fresh-research decision:
DEFER before Stage2 because no third-family candidate simultaneously met:
- released trained GEC checkpoint;
- reproducible inference;
- freezeable provenance;
- architecture independence;
- low integration debt.

Stage2 proposed purpose:
full-population SOURCE-ONLY execution/legal/diversity/family diagnostics.

Absolutely forbidden during this review/Stage2:
- project gold/reference;
- R_joint;
- correctness/F-score;
- selector training;
- LLM judge;
- family-vote activation.

Primary contract to review:
`phase2/redesign/MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_EXECUTION_CONTRACT_V1.md`

Supporting frozen records:
- `MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V2.md`
- `MPSEF_V4_CANDIDATE_REGISTRY_ACTIONSET_CONTRACT_V2.md`
- `MPSEF_V4_STAGE1_PROTOCOL_COMPLETE_CLOSURE_LOCK_V1.md`
- `ACAD_PASS_POST_STAGE1_FRESH_RESEARCH_REBASELINE_V1.md`
- `MPSEF_P1_CF_PROPOSAL_LOCK_V1.md`

## Reviewer mission

Act as an adversarial senior research/ML-systems reviewer.

Do NOT optimize for agreement with the current plan.

Find hidden ways the Stage2 design could create:
- invalid provenance;
- denominator leakage;
- silent UID loss;
- false independence;
- false diversity;
- action duplication artifacts;
- over-edit bias;
- protection leakage;
- parent-output contamination;
- non-reproducible execution;
- post-hoc decision rules;
- accidental quality claims from source-only diagnostics;
- resource-budget confounding.

## Mandatory questions

### A. Identity/provenance
1. Is the exact full-C_F identity sufficiently frozen?
2. Is reuse of frozen P1 preferable to rerunning it?
3. Is P3 exact-parent binding sufficiently proven?
4. Can the Stage2 replay gate detect runner drift?

### B. P2_V2
5. Are B01 word/segment/first-wordpiece semantics still fully protected at 1,918 scale?
6. Are generation ceiling/EOS failures handled without hidden denominator loss?
7. Is there any route by which historical defective P2 evidence could contaminate V2?

### C. Legalization/action sets
8. Can literal whole-output dedup create misleading source-only diversity?
9. Are protection/reversibility failures fail-closed enough?
10. Is KEEP handling correct when a proposer emits an exact source string?
11. Are family/proposer provenance retained after dedup?

### D. Family-aware diagnostics
12. Is P1+P3 correctly treated as one architecture family?
13. Are SOURCE_ONLY_INDEPENDENT_NONKEEP_FAMILY_COUNT and FAMILY_AVAILABILITY_STATE well-defined?
14. Is cross-family exact agreement meaningful as a descriptive metric without implying correctness?
15. What source-only family metric is missing, if any?

### E. Runtime/reproducibility
16. Is the P2 240-minute budget defensible from Stage1 evidence?
17. Should any resource ceiling or progress condition change BEFORE execution?
18. Could hardware/runtime drift invalidate comparison with Stage1?

### F. P4 decision
19. Is P4-DEFER defensible for source-only Stage2?
20. Is there a reproducible third-family Arabic GEC checkpoint we likely missed?
21. What Stage2 source-only pattern should force P4 reopening?

### G. Scientific boundary
22. Does any proposed Stage2 metric accidentally become a quality proxy?
23. Are there post-hoc interpretation risks that should be forbidden now?
24. Is there any reason to open gold before Stage2 source-only closure? Default answer should be no unless a critical methodological contradiction exists.

## Required output format

1. VERDICT: PROCEED / MODIFY / BLOCK

2. BLOCKERS
For each:
- ID
- exact issue
- why it matters
- exact contract change required
- whether rerunning Stage0/Stage1 is necessary

3. MAJOR findings

4. MINOR findings

5. MISSING DIAGNOSTICS
Source-only only.

6. RESOURCE REVIEW
- P2 timeout
- P3 timeout
- watchdog/stale settings
- CPU/GPU comparability

7. P4 REVIEW
- uphold DEFER / reopen now
- evidence
- any concrete checkpoint candidate with exact repository/model identifier if available

8. SCIENTIFIC-BOUNDARY AUDIT
Explicitly identify any phrase/metric that overclaims correctness from source-only data.

9. FINAL RECOMMENDATION
- executable next step
- files/contracts to change
- whether Stage2 can begin after those changes

## Severity semantics

BLOCKER:
execution could invalidate Stage2 evidence or violate frozen scientific boundary.

MAJOR:
important design weakness that should be fixed before full-C_F execution.

MINOR:
clarity/auditability improvement that does not change core semantics.

## Copy-ready review prompt

Continue the ACAD_PASS MP-SEF V4 project as an independent adversarial architecture reviewer.

You are reviewing Stage2 BEFORE any new full-C_F P2/P3 inference.

Read the supplied review packet and all named frozen contracts. Do not assume prior decisions are correct merely because they are frozen.

The full C_F population is 1,918 UIDs / 764 clusters. Stage1 is protocol-complete. No project gold/reference may be opened. Do not compute R_joint, correctness, F-score, or train/select a correctness model.

Your job is to challenge the proposed Stage2 source-only contract for identity/provenance failures, denominator leakage, false family independence, misleading diversity, action-set/dedup errors, protection leakage, P3 parent contamination, P2 word-alignment/generation failure handling, resource-budget issues, and post-hoc decision risks.

P1 and P3 are one SWEET architecture family. P2_V2 is the second independent family. P4 was deferred because fresh research did not find a third-family Arabic GEC checkpoint that was simultaneously trained, public, reproducible, freezeable, independent, and low-debt.

Return exactly the requested VERDICT / BLOCKERS / MAJOR / MINOR / MISSING DIAGNOSTICS / RESOURCE REVIEW / P4 REVIEW / SCIENTIFIC-BOUNDARY AUDIT / FINAL RECOMMENDATION structure.

Be skeptical. Prefer MODIFY or BLOCK if evidence warrants it. Do not invent a PASS.
