# Phase 2 — Cross-Corpus Independent Edit Agreement: End Review

Date: 2026-09-29

## Decision

**WORSENED / MODIFY for auto-accept, while the overall project is epistemically IMPROVED.**

Canonical workflow:
- Phase 2 Cross-Corpus Independent Edit Agreement
- GitHub Actions run: 36484171517
- conclusion: SUCCESS

The gate did what it was designed to do: test whether exact agreement between two different Arabic GEC systems is strong enough to justify automatic correction on a fresh cross-corpus population.

It is **not strong enough by itself**.

## Population and frozen runtime evidence

External development-generalization population:
- QALB-2015 L2 TRAIN
- deterministic raw-only 50-line slice
- QALB TEST unread
- runtime decisions frozen before corrected/gold text
- no QALB text persisted to this repository

Generators:
- SWEET NoPnx iteration 1
- AraBART QALB14 independent generator

Generated edit events:
- SWEET: 532
- AraBART: 469
- exact event agreements before policy filtering: 229

## Primary policy — EXACT_SINGLE_SUB_AGREEMENT

Accepted: 159

After gold comparison + contextual review:
- supported correction: 138
- supported alternative: 6
- wrong: 8
- partial: 6
- unnecessary: 1
- HIGH/CRITICAL wrong: 1

Supported precision after contextual review:
**90.57% (144/159)**

The pre-registered contract required zero demonstrably wrong accepted events.
Observed wrong accepted events = 8.

**Decision: MODIFY — do not promote exact single-model agreement to an automatic acceptance oracle.**

## Secondary policy — EXACT_BOUNDED_SUB_EVENT_AGREEMENT

Accepted: 170

After contextual review:
- supported correction: 147
- supported alternative: 7
- wrong: 8
- partial: 7
- unnecessary: 1
- HIGH/CRITICAL wrong: 1

Supported precision:
**90.59% (154/170)**

Multiword expansion added useful corrections, but it did not eliminate the wrong/partial events already present in the shared single-token population.

**Decision: MODIFY — do not promote bounded agreement to auto-accept.**

## Magnitude of change

Compared with the earlier repeatedly inspected Nahw development result:
- EXACT_LOCAL_AGREEMENT: 23/23 supported = 100% development precision.
- Cross-corpus EXACT_SINGLE_SUB_AGREEMENT: 144/159 supported = 90.57%.

Observed precision therefore fell by **9.43 percentage points** under cross-corpus generalization.

This is not evidence that independent agreement is useless. It is evidence that the earlier apparent 100% was optimistic because the development population was small and repeatedly inspected.

Compared descriptively with raw AraBART full-event development quality (58.49% supported/alternative), ~90.6% cross-model agreement is a major enrichment. The populations differ, so this is not a controlled head-to-head.

## Failure families exposed

Exact agreement can still converge on the same wrong edit. The observed failures include:
- semantic wrong-lexeme selection;
- gender/agreement error;
- incomplete malformed-word repair;
- hamza choice that changes the intended lexeme;
- incorrect prepositional/lexical choice;
- semantic verb drift;
- wrong derivational form;
- unnecessary case-marking over-correction.

One accepted wrong event was classified HIGH under Strict Fidelity because both models agreed on a different verb meaning from the intended context.

## What survives

Keep exact cross-model agreement as **strong positive evidence**.

Do not use it alone as proof.

The architecture should become:

candidate generators
→ complete edit events
→ exact independent agreement
→ **contextual contradiction / source-validity veto**
→ error-type / lexical-morphosyntactic evidence
→ ACCEPT / REVIEW / REJECT
→ scientific-integrity lock
→ semantic-fidelity verification
→ exact source-local patch.

## Fresh research interpretation

- Alhafni & Habash (ACL 2025) show Arabic edit tagging is efficient/interpretable and that ensembles can improve performance, supporting edit-level multi-model evidence rather than full-sentence rewriting.
- Goto et al. (BEA 2026) show edit-level majority voting can mitigate over-correction, but voting is a quality-improvement mechanism, not a mathematical correctness guarantee.
- Wang et al. (Findings ACL 2026, COCOGEC) show GEC predictions can flip under subtle context changes, directly matching the contextual failures exposed here.
- Goto et al. (Findings EMNLP 2025) show reference-free/LLM-based metrics can be unreliable as sole judges, so replacing the failed agreement oracle with a single LLM judge would not solve the safety problem.

## Next technical gate

**Phase 2 — Contextual Contradiction Veto Gate**

Do not search for another positive auto-accept heuristic first.

Instead ask:
> Can a separate context-sensitive verifier reliably detect the small minority of wrong/partial edits inside the high-precision exact-agreement stream?

Priority evidence:
1. source-token validity and alternative morphology;
2. local controller/subject/complement compatibility;
3. lexical/derivational consistency;
4. candidate-vs-source contextual likelihood as a veto, not a positive oracle;
5. counterfactual context perturbations around the known eight wrong families.

Success criterion:
- preserve most of the 144 supported single agreements;
- reject/review all 8 known wrong agreements in development;
- reject/review all partial/unnecessary events;
- then test the frozen veto on a new disjoint slice before any promotion.

Do not:
- tune another confidence threshold on the same 50 lines;
- add lexical exception lists for the observed words;
- use an LLM judge as sole verifier;
- read QALB15 TEST;
- start Phase 3;
- create the final sealed benchmark.
