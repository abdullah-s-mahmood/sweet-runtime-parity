# M1-A v1.1 — Result Review

Date: 2026-09-30  
Canonical successful workflow: 36641075882  
Safe result commit: 0bf3c8600404d089d079352deaf589d1bdd5abdd

## Decision

**M1-A expert-grounded bootstrap: DATA_READY.**

This removes the immediate requirement that the project owner must personally recruit two Arabic experts before M1/M2 research can continue.

It does **not** replace publication-grade independent human confirmation of ACAD_PASS on real academic documents.

## Final observed evidence

QALB14 TRAIN+DEV, already-consumed only:
- 20,428 human-corrected reference lines available as CLEAN_REFERENCE_KEEP;
- 20,380 source!=reference lines available as ERRONEOUS_SOURCE_KEEP and FULL_EXPERT_REPAIR;
- 19,887 M2-reconstructable changed lines;
- 19,758 reconstructable multi-edit lines;
- 19,758 ONE_OF_MANY_PARTIAL controlled cases;
- 19,758 ALL_BUT_ONE_PARTIAL controlled cases;
- 129 single-edit complete cases;
- 493 M2 reconstruction failures, excluded from controlled partial synthesis.

ZAEBUC Arabic TRAIN only:
- 150 aligned raw/corrected sentence pairs;
- all 150 differ after normalization;
- 150 clean corrected-reference KEEP cases;
- DEV/TEST unread.

A7'ta pinned expert-book corpus:
- 463 parseable aligned non-empty pairs in the pinned snapshot;
- 375 deterministic bootstrap pairs;
- 88 deterministic reserved M2 pairs;
- published article reports 470 pairs, leaving a 7-pair (1.49%) reproducibility discrepancy to audit.

Safe persisted calibration sample:
- 3,829 hashed/provenance cases;
- 3 independent source families;
- raw Arabic text not persisted;
- all 17 v1.1 DATA_READY criteria satisfied.

Forbidden evidence remained unread:
- QALB14 TEST;
- all QALB15;
- ZAEBUC DEV/TEST;
- reserved Nahw;
- sealed benchmark.

## Comparison with M1-A v1

### Overall methodological state
**IMPROVED.**

v1 was NOT_READY. Its intended evidence gate had only 48 naturally unchanged raw QALB lines versus a requirement of >=100, and the implementation also contained a negative-polarity boolean aggregation bug.

v1.1:
- does not lower the failed threshold;
- changes the evidence definition to clean human-corrected references;
- adds two independent expert/professional evidence families;
- reserves A7'ta evidence for future confirmation;
- passes 17/17 pre-registered v1.1 criteria.

### Magnitude

Comparable/evidence-availability changes:
- independent external corpus families in executable bootstrap: 1 QALB family → 3 families (QALB + ZAEBUC + A7'ta), +2 families;
- immediately usable clean KEEP evidence: the old natural-source strategy yielded 48 cases; the redesigned expert-reference strategy yields 20,428 QALB cases plus 150 ZAEBUC and 375 A7'ta bootstrap correct sides. Because the definition changed, this is an availability expansion, **not a performance gain**;
- controlled QALB incomplete-repair supply remains very large: 19,758 cases for each of ONE_OF_MANY and ALL_BUT_ONE;
- untouched A7'ta reserve created: 88 pairs.

No Arabic correction precision/recall improvement is claimed because no correction model was evaluated in M1-A.

## What improved

- The absence of locally available Arabic experts is no longer a blocking dependency for calibration and verifier feasibility.
- M1 has stronger provenance than agent-only labels.
- Evidence diversity improved substantially.
- The exact “locally correct but incomplete” bottleneck can now be studied using withheld **human** edits rather than weak proxy labels.
- A true external reserved source is now available for M2.

## What worsened / new risks exposed

- A7'ta pinned repository yields 463 parseable pairs rather than the published 470; 7 pairs need provenance/format audit.
- QALB M2 reconstruction fails on 493 changed lines; these must remain excluded from controlled partial synthesis.
- ZAEBUC TRAIN contributes only 150 sentence pairs, so its role is independent-domain evidence, not high-volume training.
- Multi-source references increase heterogeneity; source-stratified reporting becomes mandatory.
- None of these resources directly proves scientific-document fidelity or DOCX preservation.

## Current project status

M1-A: **IMPROVED / DATA_READY.**  
M1 overall: **IMPROVED but not fully human-confirmed.**  
Arabic auto-correction capability: **UNCHANGED / still REVIEW-first.**  
Arabic verification research readiness: **IMPROVED substantially.**  
Scientific/document fidelity: **UNCHANGED / separate validation still required.**

## Forecast

### Realistic case
A strong frontier verifier should now be testable against a much more defensible correction/completeness contract. Expect the greatest gain in detecting:
- incomplete repairs;
- unnecessary editing of already-correct text;
- obvious contextually wrong repairs.

Do not assume equal success on ambiguity or scientific semantics.

### Best case
A single strong verifier, calibrated on QALB/ZAEBUC and confirmed on reserved A7'ta, materially improves selective precision and completeness detection enough to justify a narrow Arabic auto-apply lane later.

### Failure case
The verifier performs well on QALB-style reference completion but degrades on ZAEBUC/A7'ta or project-local Arabic. In that case, Arabic remains Review-first and the expert evidence still provides a publishable, reproducible reason for the stop decision.

## Main blockers

1. Non-reference valid alternatives and ambiguity.
2. Scientific fidelity is not represented by learner-language corpora.
3. No direct independent expert adjudication of the 24 local project cases yet.
4. A7'ta 463 vs published 470 reproducibility discrepancy.
5. Future frontier-verifier reproducibility/cost/calibration.
6. Document preservation remains a separate engineering validation problem.
