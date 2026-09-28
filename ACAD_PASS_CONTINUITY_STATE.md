# ACAD_PASS — Canonical Continuity State

Date: 2026-09-28

## Project identity

ACAD_PASS is the unified project context for the bilingual Academic Document Intelligence & Transformation Platform.

The historical work came from:
1. **"كتابة برومبت النظام الاحترافي"** — primary source for platform architecture, product scope, processing modes, semantic/safety constraints, document-preservation requirements, and phase boundaries.
2. **"توصية بحثية أولية"** — major source for Phase 2 Arabic evaluation execution, adjudication, research iterations, and gate decisions.
3. **ChatGPT Work / project work artifacts** — supporting implementation/research context.
4. **GitHub repository `abdullah-s-mahmood/sweet-runtime-parity`, branch `phase2-arabic-eval`** — canonical execution/evidence ledger for the current Arabic correction work.

GitHub evidence does not supersede the broader platform architecture. The Arabic GEC stack is one bounded proofreading subsystem.

## Permanent architecture context

Platform flow remains:

UNDERSTAND
→ PROTECT
→ TRANSFORM / PROOFREAD
→ INDEPENDENTLY VERIFY
→ DETECT RISK
→ REPAIR
→ RE-VERIFY
→ ESCALATE / REVIEW
→ PRESERVE DOCUMENT
→ DELIVER

Arabic correction acceptance must remain subordinate to:
- strict-fidelity mode;
- semantic fidelity verification;
- scientific integrity / protected facts;
- numbers, units, dates, statistics and citation protection;
- DOCX/OOXML/OMML preservation;
- mixed-language / wrong-language guards;
- review-state enforcement.

Arabic author-aware remains disabled unless separately validated.

## Current Phase

**Phase 2 only.**

Do NOT:
- restart Phase 0 / 0B / earlier closed Phase 1 iterations;
- regenerate the frozen 150 Nahw development targets;
- change the 41 Nahw development passages;
- consume the 59 reserved Nahw passage IDs;
- create the final sealed benchmark yet;
- start Phase 3;
- tune SWEET or modify the frozen safety stack merely to improve current metrics.

## Closed / completed evidence

### Independent Candidate Acceptance
Clean canonical rerun:
- existing local candidate policy `EXACT_LOCAL_AGREEMENT`
- 23 accepted
- 23 supported
- 0 wrong
- 0 partial
- development-only

### AraBART-only substitution audit
67 new one-to-one substitutions:
- 29 supported/alternative
- 33 wrong
- 2 partial
- 2 unnecessary
- 1 alignment uncertain

Conclusion:
AraBART is a useful recall-expanding generator, not an acceptance oracle.

### Full AraBART event audit
106 complete events:
- 62 supported/alternative
- 35 wrong
- 7 partial
- 2 unnecessary

Conclusion:
complete edit-event representation is necessary; wordwise decomposition can misclassify multiword edits.

### Reverse Acceptance Gate
Narrow structural local policy:
- 6 accepted
- 6 supported
- 0 wrong
- development-only

### Full Edit-Event Acceptance Prototype
On repeatedly inspected development evidence:
- EVENT_STRUCTURAL_TYPED: 24/24 supported
- EVENT_STRUCTURAL_STRICT: 23/23 supported
- 0 accepted wrong/partial

This result was explicitly NOT sufficient for freeze because of repeated-data risk.

## Generalization evidence

### ZAEBUC-v1.0 Arabic DEV
Frozen policy before gold.

EVENT_STRUCTURAL_TYPED:
- accepted 6
- 5 supported
- 1 wrong after contextual review
- observed precision 83.33%

EVENT_STRUCTURAL_STRICT:
- accepted 3
- 2 supported
- 1 wrong
- observed precision 66.67%

Critical counterexample:
`ينشرون → ينشروا` looked locally like a valid five-verbs nun change but was wrong because context required singular `ينشر`.

**Falsified:** context-free nun insertion/deletion as auto-accept proof.

Post-gate:
- NUN family = REVIEW_ONLY unless additional independent syntactic/controller evidence exists.

### FINAL_ALIF disjoint validation on separate ZAEBUC TRAIN hash slice
Generic final-alif family showed substantial exact support but also non-exact/unmatched cases.

Conclusion:
surface pattern `source + ا` conflates:
1. context-sensitive accusative/tanwin alif;
2. orthographic differentiating alif after plural waw.

Generic final-alif is not promotable as a single family.

### QALB-2015 L2 DEV context gate
Deterministic raw-only 100-line slice; runtime decisions before gold; QALB test unread; no QALB text persisted.

- WAW_ALIF_VERB_ONLY: 0 candidates → **UNPROVEN**, not failed.
- ACCUSATIVE_ALIF_SINGLE: 28 diagnostic candidates; 14 exact-gold, 14 require contextual review.
- FINAL_ALIF_GENERIC: 36 diagnostic candidates; 18 exact-gold, 18 require contextual review.

Conclusion:
accusative/final-alif family remains context-sensitive.
WAW-alif needs a better morphosyntactic detector and a fresh untouched slice.

## Current active task

**QALB15 WAW-ALIF raw-only diagnostic**

Purpose:
determine why the source-POS-based WAW-alif rule produced zero candidates, without reading gold and without changing any policy on the consumed QALB15 DEV slice.

Parallel research conclusion:
the Arabic differentiating alif is valid only after terminal **واو الجماعة attached to a verb**; it must not be inferred from final waw alone.

Candidate future hypothesis, to be tested only on a fresh disjoint population:
- source ends in و;
- candidate == source + ا;
- candidate contextual morphology POS=verb;
- candidate number=plural;
- preferably explicit evidence that terminal waw is the group pronoun rather than root waw / nominal plural;
- dependency/controller evidence if ambiguity remains.

## Scientific posture

The project is currently **epistemically improved but the generic structural auto-accept policy is MIXED/WORSENED under disjoint generalization**.

Do not hide negative evidence.
Do not retune on consumed slices.
Every next gate must report:
- IMPROVED / WORSENED / MIXED;
- magnitude with comparable metrics;
- likely next progress;
- blockers and failure risks.

## Immediate next decision

Wait for the raw-only WAW diagnostic.

Then:
1. define a new morphosyntactically justified WAW-alif hypothesis without consulting gold;
2. pre-register it;
3. test it on an untouched external slice;
4. keep NUN auto-accept disabled;
5. keep accusative-alif review-only unless an independently validated syntactic governor/case signal is added.

No Phase 3.
No final sealed benchmark yet.
