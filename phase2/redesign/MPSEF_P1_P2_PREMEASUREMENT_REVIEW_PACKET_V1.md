# MP-SEF P1/P2 PREMEASUREMENT INDEPENDENT REVIEW PACKET V1

Date: 2026-09-30
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `phase2-arabic-eval`

## Review stage

This packet is intentionally **premeasurement**.

The reviewer MUST NOT:
- compute or estimate R_joint from hidden/reference knowledge;
- recommend lowering the frozen >=95% R_joint gate after seeing outcomes;
- train, tune, or authorize a selector;
- open INTERNAL_EVALUATION, STRESS_DIAGNOSTIC, or any reserved set;
- reinterpret candidate activity as correction quality.

The purpose is to decide whether the protocol and frozen proposer artifacts are
scientifically adequate to authorize construction/freeze of the R_joint scorer
and the second pre-measurement preflight.

## Governing documents

Read these first:

1. `phase2/redesign/MPSEF_PRE_UNION_PROTOCOL_V3.md`
2. `phase2/redesign/MPSEF_BUNDLE_CONTRACT_V1.md`
3. `phase2/redesign/MPSEF_TARGET_AND_MATCHING_CONTRACT_V1.md`
4. `phase2/redesign/MPSEF_PROTECTED_INVARIANTS_CONTRACT_V1.md`
5. `phase2/redesign/MPSEF_P1_CF_PROPOSAL_LOCK_V1.md`
6. `phase2/redesign/MPSEF_P2_CF_PROPOSAL_LOCK_V1.md`
7. `RESUME_HERE.md`

## Frozen population

C_F:
- records: **1,918**
- clusters: **764**
- source manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`

Both P1 and P2 consumed this exact source manifest.

Historical independence is NOT restored. The allowed claim remains:
**DEVELOPMENT FEASIBILITY ONLY**.

## P1 frozen evidence

- run: `36765798233`
- artifact: `11123050529`
- ZIP digest:
  `e4020418ca2f2793d4bb79bc766e26838398fb9affba6d0f1c704255cd5aed46`
- cases: **1918/1918**
- batch-vs-single parity: **64/64**
- changed vs source: **1838/1918 = 95.83%**
- protected-touch precheck: **19/1918 = 0.99%**
- empty outputs: **0**
- proposal JSONL SHA256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`

## P2 frozen evidence

- run: `36768378938`
- artifact: `11124303107`
- ZIP digest:
  `5209633d389db02054456a42710a96a1d6e573cefca308254747897969c7d41c`
- cases: **1918/1918**
- batch-vs-single all-field parity: **32/32**
- changed vs source: **1906/1918 = 99.37%**
- protected-touch precheck: **21/1918 = 1.10%**
- empty outputs: **0**
- proposal JSONL SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

## Primary executable action space

For each C_F case, primary candidate availability is intentionally limited to:
- KEEP;
- P1_FINAL whole sentence;
- P2_FINAL whole sentence.

P1 pass-1 is provenance only.
No P2 n-best.
No edit-level hybrid fusion in the primary measurement.

Any protected-invariant violation makes that proposer hypothesis illegal.
The target remains in the denominator even if all non-KEEP proposals are blocked.

## Frozen measurement gate

Primary candidate-availability feasibility gate:

`R_joint(P1,P2) >= 0.95`

Interpretation:
- >=95%: candidate availability may justify continuing to selector research;
- 90% to <95%: borderline; review architecture before selector;
- <90%: revisit/close the high-coverage path.

The gate MUST NOT be changed after measurement.

## Required independent review questions

The reviewer must answer each item explicitly.

### A. Population/provenance
1. Does using the identical source-only C_F manifest for P1 and P2 prevent
   proposer-population drift adequately?
2. Are the historical-exposure limitations and DEVELOPMENT FEASIBILITY ONLY
   claim sufficiently explicit?
3. Is there any remaining reference/gold leakage path in proposal generation?

### B. Proposal semantics
4. Is treating P1 pass-2 and P2 final generation as indivisible whole-sentence
   hypotheses consistent with the anti-cherry-picking objective?
5. Is the KEEP/P1_FINAL/P2_FINAL action space sufficiently frozen before gold
   scoring?
6. Is any source-derived diagnostic field capable of leaking future gold-based
   decisions into candidate construction?

### C. Protected invariants
7. Is the current source-side protected-span detection sufficient as a
   precheck, given that named-entity protection is intentionally inactive
   unless a deterministic high-confidence detector exists?
8. The proposal runners use deterministic `difflib.SequenceMatcher`
   diagnostics and source-overlap checks for protected touches. Is that
   adequate only as a precheck, or must the scorer independently revalidate
   exact protected-span preservation and block ambiguous mappings?
9. Should insertions at protected-span boundaries and number-unit attachment
   changes be conservatively REVIEW/BLOCK even when the protected substring
   itself is textually preserved?
10. What exact frozen protected-invariant validation should be required in the
    scorer before an action is legal?

### D. R_joint definition/scoring
11. Confirm whether R_joint must be computed as an exact oracle over only the
    legal frozen whole-sentence actions for every denominator target.
12. Confirm that failed proposer generation, protected blocking, and no legal
    correction remain denominator failures rather than disappearing.
13. Confirm that R_raw, if reported, must remain diagnostic and cannot replace
    R_joint.
14. Define the minimum matching/alignment evidence needed to decide that a
    candidate realizes the frozen target without allowing gold-driven partial
    bundle selection.
15. Identify any ambiguity where the target-and-matching contract could allow
    optimistic scoring.

### E. Premeasurement authorization
16. Is it scientifically defensible to implement the scorer now without
    computing R_joint, then hash-freeze it and run a second premeasurement
    preflight?
17. What conditions should cause **MODIFY PROTOCOL BEFORE MEASUREMENT**?
18. What conditions should cause **DO NOT MEASURE / ARCHITECTURE INVALID**?
19. If acceptable, state exactly what may be measured once, and what remains
    prohibited afterward.

### F. Operational/reproducibility observations
20. P2 full proposal generation took roughly 35 minutes on the GitHub CPU
    runner. Does this create only an engineering-cost concern, or does it
    threaten methodological reproducibility?
21. Recommend a non-invasive heartbeat/progress mechanism for future long jobs
    that does not alter scientific outputs.

## Required reviewer output

Return a rigorous Arabic review with these sections:

1. **القرار المستقل**
   - ACCEPT PROTOCOL FOR SCORER IMPLEMENTATION
   - MODIFY PROTOCOL BEFORE SCORER FREEZE
   - DO NOT PROCEED

2. **أقوى نقاط البروتوكول**

3. **الثغرات أو مخاطر التحيز/التسرب**

4. **مراجعة protected invariants**

5. **مراجعة تعريف R_joint وطريقة حسابه**

6. **التعديلات الإلزامية قبل القياس**
   - numbered and actionable;
   - distinguish MUST from SHOULD.

7. **هل يسمح ببناء scorer الآن؟**
   - yes/no with rationale.

8. **هل يسمح بقياس R_joint الآن؟**
   - this should normally remain NO until scorer freeze + second preflight.

9. **قائمة تحقق premeasurement نهائية**

10. **التصنيف مقارنة بالمراجعة السابقة**
    - IMPROVED / WORSENED / MIXED;
    - quantify material change where possible;
    - identify remaining blockers.

The reviewer must challenge the design rather than try to justify it.
