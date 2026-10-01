# ACAD_PASS ARABIC ARCHITECTURE INDEPENDENT REVIEW PACKAGE V1

Date: 2026-10-01
Review type: PRE-IMPLEMENTATION / PRE-GOLD ARCHITECTURE REVIEW
Architecture snapshot commit:
`5e0ad432b513bd65daa567cdc2e046c9d18996dd`

Repository:
`abdullah-s-mahmood/sweet-runtime-parity`

Branch:
`phase2-arabic-eval`

## 1. Review objective

Independently determine whether the proposed ACAD_PASS Arabic correction redesign is the strongest scientifically defensible next step before any new gold-aware measurement.

The review must challenge the architecture rather than justify prior work.

## 2. Current frozen evidence

### Current V3 source-only control

Population:
- C_F = 1,918 cases
- clusters = 764

Frozen executable actions:
- P1_OK = 1,806 / 1,918 = 94.16%
- P1_PROTECTED_BLOCKED = 112 / 1,918 = 5.84%
- P2_EXECUTION_FAILED = 1,918 / 1,918 = 100%

P2 current-cycle executable contribution:
- 0 / 1,918

Current action-set SHA256:
`6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`

### P2 provenance defect

Observed on frozen P2:
- GED/morphology count mismatch = 1,918 / 1,918
- exact matches = 0 / 1,918
- total dropped GED predictions under zip semantics = 30,341
- minimum excess = 2
- maximum excess = 87
- median excess = 15
- mean excess = 15.8191
- frozen output reproduction = 1,918 / 1,918 exact
- generation ceiling = 24
- missing terminal EOS = 0

Root cause:
subword GED predictions were consumed as word-level labels and silently truncated by zip.

Repairability classification:
`FIXABLE_NEXT_VERSION_ONLY`

### Second Preflight

Current hardened source-only preflight:
- run = 36825797396
- code commit = 7c31da92a75495f11e1faac10ecc4e84685845c3
- C01-C22 = 22 / 22 PASS
- gold loaded = false
- metric computed = false
- measurement authorized = false
- artifact digest:
  `sha256:fcd653251e4e6870adfdcfb26d71e2bfa8f11f14e6f15b040f054077cb008896`

Historical simplified baseline:
- strict PASS = 36.36%
- weighted remediation = 65.91%
- later superseded by advanced 22/22 PASS.

## 3. Why no R_joint is being run now

Although V3 passed source-only preauthorization checks, current executable candidate space is effectively P1-only.

The project adopted:
`ACAD_PASS_MAXIMUM_QUALITY_REASSESSMENT_CONTRACT_V1.md`

Therefore the project chose to re-baseline architecture before spending additional gold-aware evaluation exposure.

No gate was weakened.

## 4. Fresh external evidence

### ACL 2025 — Arabic SWEET text editing

Alhafni & Habash (ACL 2025):
- Arabic text editing achieved SOTA on two GEC benchmarks and competitive results on two others.
- iterative correction improves MSA up to two iterations;
- separate NoPnx then Pnx correction improves MSA;
- heterogeneous ensembles further improve results;
- ensemble method aligns model outputs to source, extracts edits, then retains an edit if at least k-1 of k systems support it;
- the method intentionally prioritizes precision over recall.

For QALB-2014 and ZAEBUC, the published 3-Ensemble combines:
1. Seq2Seq++;
2. SWEET2;
3. SWEET2_NoPnx + SWEET_Pnx.

Published test F0.5:
- QALB-2014: 3-Ensemble 81.3; 4-Ensemble 81.7
- QALB-2015: 3-Ensemble 81.3; 4-Ensemble 82.9
- ZAEBUC: 3-Ensemble 85.9; 4-Ensemble 87.2

### EMNLP 2023 — Seq2Seq + GED/morphology

Alhafni et al.:
- GED auxiliary information improves Arabic GEC across three datasets;
- contextual morphology is useful;
- public GED and AraBART GEC models exist.

### EACL 2026 — Nahw

Mubarak et al.:
- current LLMs still show substantial Arabic grammar deficiencies;
- synthetic fine-tuning helps but does not match high-quality natural training.

The project therefore does not plan to make a general LLM the sole primary corrector or verifier.

## 5. Proposed redesign

### Frozen control lane

Keep V3 immutable.

Do not repair current P2 in place.

### New redesign lane

#### P1_CONTROL

Current:
`P1_SWEET_QALB14_NOPNX_ITER2`

Role:
frozen control.

#### P2_V2

Repair heterogeneous Seq2Seq++ / AraBART + GED/morphology proposer.

Key repair:
- first-wordpiece word-level GED alignment;
- ignore-index for remaining wordpieces;
- segment at whole-word boundaries;
- exact word-level coverage assertion;
- no zip truncation;
- exact GEC input/GED-label length equality;
- source-only truncation/EOS/provenance traces.

Specification:
`phase2/redesign/MPSEF_P2_V2_IMPLEMENTATION_SPEC.md`

#### P3_V1

Published SWEET cascade:

`SWEET_QALB14_NOPNX_ITER2 -> SWEET_QALB14_PNX_ITER1`

P1 already equals the NoPnx ×2 component; P3 adds only the frozen Pnx stage.

Specification:
`phase2/redesign/MPSEF_P3_V1_SWEET_PNX_CASCADE_SPEC.md`

### Diversity protocol

Before any new gold measurement:

- synthetic tests;
- deterministic small C_F source-only parity packet;
- only after review, possible full C_F source-only diversity run;
- report execution, provenance, output duplication, pairwise diversity, legalizer states, protected-touch, runtime;
- no correctness metrics.

Protocol:
`phase2/redesign/MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V1.md`

## 6. Possible MP-SEF V4

A future V4 may explore source-aligned edit consensus.

Important:
- V3 whole-action rules remain immutable;
- V4 would be a NEW architecture;
- correlated variants cannot be counted as independent evidence families;
- no consensus primary action is authorized yet.

## 7. Files the reviewer should inspect

Mandatory:

1. `ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md`
2. `RESUME_HERE.md`
3. `phase2/redesign/ACAD_PASS_MAXIMUM_QUALITY_REASSESSMENT_CONTRACT_V1.md`
4. `phase2/redesign/ACAD_PASS_FAILURE_TRIAGE_CONTRACT_V1.md`
5. `phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_REBASELINE_V1.md`
6. `phase2/redesign/MPSEF_P2_GED_ALIGNMENT_PROVENANCE_DEFECT_V1.md`
7. `phase2/redesign/MPSEF_P2_REPAIRABILITY_ASSESSMENT_V1.md`
8. `phase2/redesign/MPSEF_P2_V2_IMPLEMENTATION_SPEC.md`
9. `phase2/redesign/MPSEF_P3_V1_SWEET_PNX_CASCADE_SPEC.md`
10. `phase2/redesign/MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V1.md`
11. `phase2/redesign/MPSEF_EXECUTABLE_ACTIONS_LOCK_V1.md`
12. `phase2/redesign/MPSEF_TARGET_SCOPE_FAMILY_MAP_V2.md`
13. `phase2/redesign/mpsef_rjoint_core_v2.py`
14. `phase2/redesign/mpsef_rjoint_score_v2.py`
15. `phase2/redesign/mpsef_measurement_guard_v2.py`

Review historical upstream interaction:
- current P1 runner;
- current frozen P2 runner;
- official CAMeL-Lab Arabic-GEC ErrorIdentifier alignment behavior.

## 8. Required review questions

The reviewer MUST answer:

### A. Re-baseline decision
1. Was it correct to stop before R_joint and re-baseline after P2 became non-executable?
2. Is there any stronger reason to run the frozen P1-only V3 measurement before redesign?

### B. P2_V2
3. Is the proposed GED alignment repair technically correct?
4. Are there unaddressed segmentation/tokenization/provenance failure modes?
5. Should P2_V2 be repaired, replaced, or both compared?

### C. P3_V1
6. Is P3_V1 sufficiently distinct to justify a candidate slot?
7. Is adding Pnx likely to add useful diversity under a NoPnx-centric primary endpoint, or mostly correlated activity?
8. Should an alternate SWEET encoder/checkpoint be considered instead/in addition?

### D. Candidate diversity
9. Are the source-only diversity metrics sufficient?
10. Should numeric retention thresholds be preregistered before Stage 1 or only before full Stage 2?
11. What source-only evidence would justify dropping a proposer without gold?

### E. V4 consensus
12. Is source-aligned edit consensus scientifically preferable to whole-action candidate pools for ACAD_PASS?
13. How should correlated proposer families be weighted/count as evidence?
14. What overlap/conflict rules are required to prevent invalid hybrid outputs?

### F. Safety
15. Does the current protected-invariant/legalizer design create hidden overblocking risk?
16. Are there source-only diagnostics that should be added before any gold-aware run?

### G. Research value
17. Does this architecture create a defensible academic research contribution beyond application engineering?
18. What ablations/baselines would be mandatory for publication or a PhD-level study?
19. Which parts appear novel vs established practice?

### H. Final decision
20. Choose exactly one:
   - GO WITH PROPOSED SOURCE-ONLY REDESIGN
   - MODIFY BEFORE IMPLEMENTATION
   - STOP / REBASELINE MORE DEEPLY

If MODIFY, list all BLOCKER and MAJOR findings separately.

## 9. Non-negotiable review constraints

The reviewer must NOT:

- weaken frozen scientific gates;
- recommend using gold to choose proposer implementation;
- treat source-change/activity as quality;
- treat P2 execution failure as linguistic error;
- overwrite historical frozen artifacts;
- open INTERNAL/STRESS/reserved data;
- recommend selector tuning before architecture freeze.

## 10. Expected deliverable

A structured independent report containing:

- verdict;
- BLOCKER findings;
- MAJOR findings;
- MINOR findings;
- assessment of each P1/P2_V2/P3/V4 option;
- missing tests;
- recommended architecture;
- publication/PhD research significance;
- exact next safe sequence.

No project metric should be computed during this review.
