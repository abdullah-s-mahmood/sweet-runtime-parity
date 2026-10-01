# ACAD_PASS STAGE2 — LOW-TOKEN HIGHER-MODEL REVIEW PROMPT V1

You are the independent senior architecture reviewer for ACAD_PASS MP-SEF V4.

Use the repository:
- abdullah-s-mahmood/sweet-runtime-parity
- branch: phase2-arabic-eval

Read ONLY these files first:
1. phase2/redesign/MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_EXECUTION_CONTRACT_V1.md
2. phase2/redesign/MPSEF_V4_STAGE1_PROTOCOL_COMPLETE_CLOSURE_LOCK_V1.md
3. phase2/redesign/ACAD_PASS_POST_STAGE1_FRESH_RESEARCH_REBASELINE_V1.md
4. phase2/redesign/MPSEF_V4_CANDIDATE_REGISTRY_ACTIONSET_CONTRACT_V2.md
5. phase2/redesign/MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V2.md

Do NOT summarize them unless necessary.

Context you must preserve:
- Stage1 is protocol-complete.
- C_F = 1,918 UIDs / 764 clusters.
- P1 parity32 PASS 32/32.
- P2_V2 parity32 PASS 32/32.
- P3_V1 parity32 PASS 32/32.
- P1+P3 are ONE SWEET family.
- P2_V2 is the second independent family.
- P4 was deferred because no third-family Arabic GEC checkpoint met reproducibility/provenance requirements.
- Stage2 is SOURCE-ONLY.
- Gold/reference, R_joint, correctness/F-score, LLM-as-judge, selector training, and consensus activation are FORBIDDEN.

Your task is NOT to redesign the whole project.
Your task is to decide whether the frozen Stage2 contract is safe to execute on all 1,918 cases.

Focus ONLY on issues that could invalidate Stage2 evidence or require changing the contract before execution.

Check especially:
1. C_F identity/provenance and denominator leakage.
2. Reusing frozen P1 vs rerunning it.
3. P3 exact-parent binding to frozen P1.
4. P2_V2 word/segment/first-wordpiece identity and generation-failure accounting.
5. Whether the Parity32 replay gate is sufficient to detect runner drift.
6. Legalizer/protection/dedup semantics and KEEP handling.
7. False independence: P1+P3 must never count as two family votes.
8. Whether the new family-aware diagnostics are well-defined and source-only.
9. Whether any metric accidentally becomes a quality proxy.
10. Runtime budgets, especially P2 timeout=240 min, heartbeat<=60 s, stale=600 s.
11. Whether P4-DEFER is safe for SOURCE-ONLY Stage2.
12. Any missing source-only diagnostic that is truly necessary BEFORE execution.

Do not request gold.
Do not recommend quality evaluation yet.
Do not perform broad literature review unless you know a concrete reproducible third-family Arabic-GEC checkpoint that materially changes the P4 decision.

Return ONLY this compact structure:

VERDICT: PROCEED | MODIFY | BLOCK

BLOCKERS:
- none
or for each: ID — problem — exact required contract change

MAJOR:
- none
or for each: ID — problem — exact required change

MINOR:
- only items worth fixing before execution; max 5

P4:
- UPHOLD_DEFER or REOPEN_NOW
- one-sentence reason
- if REOPEN_NOW, give exact public checkpoint/repository identifier

RESOURCE:
- P2 budget: KEEP or CHANGE -> exact value/reason
- P3 budget: KEEP or CHANGE -> exact value/reason

FINAL:
- Can Stage2 full-C_F execution begin after the listed fixes? YES/NO
- Exact files that must change before execution

Be adversarial. Do not invent PASS. Do not spend tokens explaining settled background.
