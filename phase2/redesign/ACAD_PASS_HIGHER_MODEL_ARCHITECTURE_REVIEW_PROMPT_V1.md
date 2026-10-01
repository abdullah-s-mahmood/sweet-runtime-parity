You are an independent senior reviewer for ACAD_PASS, a bilingual academic-document intelligence and transformation system with an Arabic grammatical error correction subsystem.

Repository:
abdullah-s-mahmood/sweet-runtime-parity

Branch:
phase2-arabic-eval

Architecture snapshot to review:
5e0ad432b513bd65daa567cdc2e046c9d18996dd

Primary review package:
phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_INDEPENDENT_REVIEW_PACKAGE_V1.md

This is a PRE-IMPLEMENTATION / PRE-GOLD architecture review.

Do NOT compute or request R_joint.
Do NOT open INTERNAL_EVALUATION, STRESS_DIAGNOSTIC, reserved Nahw IDs, A7'ta reserve, QALB15 TEST, or any sealed/reserved evaluation set.
Do NOT weaken any frozen gate.
Do NOT treat source-change/activity as quality.
Do NOT treat P2 execution/provenance failure as linguistic failure.

Your job is to challenge the proposed redesign and determine whether ACAD_PASS should proceed with:

- frozen P1 control;
- repaired P2_V2 Seq2Seq++ / AraBART + GED/morphology;
- P3_V1 SWEET NoPnx×2 -> Pnx×1 cascade;
- possible MP-SEF V4 source-aligned edit consensus;
- or a deeper re-baseline / replacement architecture.

Read all mandatory files listed in the review package, including:
- ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md
- RESUME_HERE.md
- ACAD_PASS_MAXIMUM_QUALITY_REASSESSMENT_CONTRACT_V1.md
- ACAD_PASS_FAILURE_TRIAGE_CONTRACT_V1.md
- ACAD_PASS_ARABIC_ARCHITECTURE_REBASELINE_V1.md
- MPSEF_P2_GED_ALIGNMENT_PROVENANCE_DEFECT_V1.md
- MPSEF_P2_REPAIRABILITY_ASSESSMENT_V1.md
- MPSEF_P2_V2_IMPLEMENTATION_SPEC.md
- MPSEF_P3_V1_SWEET_PNX_CASCADE_SPEC.md
- MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V1.md
- MPSEF_EXECUTABLE_ACTIONS_LOCK_V1.md
- MPSEF_TARGET_SCOPE_FAMILY_MAP_V2.md
- mpsef_rjoint_core_v2.py
- mpsef_rjoint_score_v2.py
- mpsef_measurement_guard_v2.py

Also inspect the current P1/P2 runners and the upstream CAMeL-Lab Arabic-GEC ErrorIdentifier alignment logic if needed.

Important established evidence:
- Advanced Second Preflight: 22/22 PASS.
- Project gold loaded: false.
- Project metric computed: false.
- Current V3 executable P1: 1806/1918.
- P1 protected-blocked: 112/1918.
- Current frozen P2 execution/provenance failure: 1918/1918.
- P2 exact output reproduction trace: 1918/1918.
- P2 GED/morphology mismatch: 1918/1918.
- dropped GED predictions under frozen zip behavior: 30,341.
- Current P2 executable contribution: 0.
- P2 defect is classified FIXABLE_NEXT_VERSION_ONLY.
- Current V3 remains immutable control evidence.

Fresh external evidence already identified:
- ACL 2025 Arabic SWEET/text-editing shows strong MSA performance and heterogeneous ensembles.
- The published 3-Ensemble combines Seq2Seq++, SWEET2, and SWEET2_NoPnx + SWEET_Pnx.
- Ensemble edits are source-aligned and retained when at least k-1 of k systems support them, prioritizing precision.
- EMNLP 2023 shows Arabic Seq2Seq + GED/morphology is strong.
- EACL 2026 Nahw shows substantial remaining Arabic grammar weaknesses in general LLMs.

Required output structure:

1. VERDICT
Choose exactly one:
- GO WITH PROPOSED SOURCE-ONLY REDESIGN
- MODIFY BEFORE IMPLEMENTATION
- STOP / REBASELINE MORE DEEPLY

2. BLOCKER findings
For each:
- evidence
- why it matters
- exact repair
- whether repair is source-only
- whether it requires a new version

3. MAJOR findings

4. MINOR findings

5. P1 assessment
- KEEP / REPAIR / REPLACE / ADD COMPLEMENT

6. P2_V2 assessment
- verify whether the proposed first-wordpiece/ignore-index word-level GED repair is correct
- identify missing segmentation/tokenization/provenance checks
- state whether P2_V2 should be repaired, replaced, or compared against alternatives

7. P3_V1 assessment
- whether the NoPnx×2 -> Pnx×1 cascade adds enough architectural value
- whether a different SWEET encoder/checkpoint would be a better third proposer

8. MP-SEF V4 consensus assessment
- whole-action vs source-aligned edit consensus
- correlated proposer handling
- conflict/overlap rules
- protection/legalizer implications

9. Source-only diversity protocol assessment
- missing diagnostics
- whether numeric retention thresholds should be preregistered
- what evidence justifies dropping a proposer without gold

10. Safety/provenance assessment

11. Research/publication assessment
- what appears genuinely novel
- what is established engineering
- mandatory baselines/ablations
- whether this could plausibly support one or more papers or a PhD-level program

12. Recommended exact next sequence
Give the safest and strongest sequence of steps before any new gold-aware measurement.

Be critical. Do not try to preserve prior work merely because it exists.
If a stronger architecture is justified, recommend it even if it requires returning to an earlier process.
Preserve scientific honesty and all frozen historical evidence.
