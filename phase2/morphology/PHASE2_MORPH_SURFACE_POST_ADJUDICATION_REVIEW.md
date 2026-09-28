# Phase 2 — Morphology Surface Adjudication: Independent Post-Review

Date: 2026-09-28

Status: DEVELOPMENT evidence reviewed after Work adjudication. No sealed benchmark. No Phase 3. No production acceptance policy frozen.

## Verified evidence

Canonical adjudication manifest commit:
- f2600b1a4df1ef934554f92ae6f47dc7cf165d92

Evidence commit recorded by the manifest:
- bc15f8987f25d0ff11637268585f0e14f116d2ba

Adjudication:
- 19/19 morphology rows reviewed
- 9/9 bounded runtime proposals reviewed
- EXACT_SAFE_REALIZATION: 3
- LINGUISTICALLY_CORRECT_ALTERNATIVE_SERIALIZATION: 5
- LINGUISTICALLY_CORRECT_BUT_OVERDIACRITIZED: 4
- NO_SURFACE_PROPOSED: 7
- no partial/wrong/review-required surface among the 12 proposed surfaces after adjudication
- development AUTO_APPLY_CANDIDATE: 3
- seven abstentions: 2 correct rejection, 2 safe surface missed, 3 possibly safe but ambiguous

Gold-independent policy ablation:
- DIRECT_PATCH_ONLY: 2/2 linguistically correct, 2/2 exact source-safe, coverage 2/19
- BERT_TOP2_SURFACE_CONSENSUS: 8/9 linguistically correct, 1 wrong, exact source-safe 1/9
- BERT_TOP1: 13/18 linguistically correct, 3 wrong, 1 unnecessary, 1 review-required
- MLE_TOP1: 9/18 linguistically correct, 3 partial, 5 wrong, 1 unnecessary
- DIRECT_PATCH_OR_BERT_TOP2: 10/11 linguistically correct, 1 wrong, exact source-safe 3/11

Critical counterexample:
- وساعٍ → وساعا survives morphology and BERT top-two consensus, although the required accusative defective-noun form is وساعيًا.
- Therefore morphology analyzability or morphology-model agreement is not a correctness verifier.

## What improved

1. Full Arabic surface realization is no longer the dominant blocker for already-supported normalized candidates.
2. Morphology can enumerate a target-compatible form for 11/13 target-overlapping candidates.
3. Contextual BERT morphology ranks the correct/equivalent target surface more often than the out-of-context MLE prior on this development slice.
4. Three candidates meet strict retrospective source-safe AUTO_APPLY criteria.
5. The architecture preserves the distinction between grammatical correctness and source-fidelity serialization.

## What remains unresolved

1. The 9/9 bounded runtime proposals are selection-biased: the gate used prior human candidate labels.
2. No independent runtime component currently decides whether the upstream correction direction is right.
3. Gold-independent BERT top-two consensus still accepts a known wrong candidate.
4. Review burden remains high: only 3/19 normalized candidates are strict auto-apply candidates.
5. Coverage of the overall 150-target development set remains limited even after normalized recovery.

## Fresh research after adjudication

### Edit verification/reranking is a distinct and validated GEC architecture

Sorokin (EMNLP 2022) explicitly separates GEC into an edit generator and a second model that classifies proposed edits as correct or false. This is directly aligned with the missing component identified here: candidate generation and candidate acceptance should be separate tasks.
- https://aclanthology.org/2022.emnlp-main.785/

### Modern GEC research continues to emphasize edit-level decisions

Edit-wise Preference Optimization (COLING 2025) argues that GEC benefits from optimizing edit tokens separately rather than treating all tokens equally. It is not Arabic evidence, but it supports an edit-level verifier rather than a sentence rewrite judge.
- https://aclanthology.org/2025.coling-main.229/

### Edit-level voting can reduce over-correction

BEA 2026 reports that edit-level majority voting over multiple candidates mitigates over-correction across nine non-Arabic benchmarks. This supports testing agreement as one verifier feature after a second independent Arabic candidate source is available. It is not sufficient evidence to deploy voting in Arabic now.
- https://aclanthology.org/2026.bea-1.60/

### Arabic multi-system edit selection is now directly relevant

ArbESC+ (2025 preprint) combines proposals from AraT5, ByT5, mT5, AraBART, AraBART+Morph+GEC and Text Editing, then uses a classifier to select edits. Reported F0.5 exceeds individual systems on QALB test sets. Because this is a preprint and not independent sealed evidence for this project, it motivates a TEST of multi-source candidate acceptance rather than immediate integration.
- https://arxiv.org/abs/2511.14230

### Public Arabic sequence-to-sequence GEC models exist with reproducible integration

CAMeL-Lab's official Arabic GEC repository provides public GED and GEC models and a documented AraBART+Morph+GED pipeline, including model id:
- CAMeL-Lab/arabart-qalb14-gec-ged-13

The paper reports that GED auxiliary information improves GEC across three Arabic datasets.
- https://github.com/CAMeL-Lab/arabic-gec
- https://aclanthology.org/2023.emnlp-main.396/

### Independent seq2seq evidence also supports AraBART/AraT5 as second sources

A 2025 Neural Computing and Applications study reports strong Arabic GEC results for AraBART/AraT5-family models on QALB-2014/2015. This supports testing them as a second candidate generator, not accepting their outputs automatically.

### Newer Arabic GEC work strengthens the case for multi-task evidence

MTAGEC (2025) combines correction, error-type classification, evidence extraction and explanation using AraT5/AraBART-family models. The architecture is relevant because an acceptance gate can use error-type/evidence signals instead of relying only on model confidence.

### Evaluation should remain edit-centric

UOT-ERRANT (TACL 2026) evaluates GEC by representing and aligning edits rather than relying mainly on whole-sentence similarity. This is consistent with our current edit-level evidence ledger and should inform the later frozen evaluation.
- https://aclanthology.org/2026.tacl-1.77/

### Arabic grammar remains difficult enough to justify abstention

Nahw (EACL 2026) shows substantial remaining deficits in Arabic grammar correction/explanation even among strong models. This supports a precision-first acceptance gate with abstention rather than broad automatic rewriting.
- https://aclanthology.org/2026.eacl-long.296/

## Maximum-effort architecture brainstorming

### A. Independent edit-quality verifier
Decision: **PROTOTYPE NEXT — highest priority**

Input features should be runtime-observable only:
- source passage and local span
- SWEET edit label/confidence
- operation family
- GED error probability/type as soft evidence
- morphology analyses and contextual morphology rank
- source/target base-letter delta
- deterministic grammar validators
- second GEC model agreement/disagreement
- semantic/scientific safety flags

Output:
- ACCEPT
- REVIEW
- REJECT

No Nahw target, no previous human label.

### B. Second Arabic candidate generator
Decision: **TEST NEXT in the same gate**

Prefer the official CAMeL-Lab AraBART+Morph+GED model first because:
- public integration path exists;
- morphology + GED preprocessing is documented;
- it is architecturally independent from SWEET's edit-tagging model.

Do not use its full rewritten sentence directly. Align it back to source-local edits and feed those edits into the same source-preserving verifier.

### C. AraT5 as a third source
Decision: **WATCH / TEST after AraBART**

Useful for independence/ensemble evidence, but adding two new generators at once would make attribution harder.

### D. Deterministic grammar validators
Decision: **PROTOTYPE in parallel**

High-value narrow validators:
- defective noun case/yāʾ restoration
- sound masculine plural case suffix
- five-verbs nūn retention/deletion
- hamzat al-waṣl/qaṭʿ
- case/tanween serialization
- imperative/past mood preservation

These should veto or route to review; they should not broadly rewrite.

### E. Morphology contextual rank
Decision: **INTEGRATE only after candidate acceptance**

Use it to choose surface realization among accepted correction directions. Do not let it accept an upstream correction direction.

### F. GED
Decision: **SOFT FEATURE ONLY**

Previous hard-gate evidence reduced useful coverage without improving the already-zero-wrong operation-aware stream. Use GED probability/error type as evidence, not an acceptance oracle.

### G. Confidence
Decision: **SOFT FEATURE ONLY**

High-confidence wrong edits already exist. Confidence cannot be a sole threshold.

### H. Multi-model agreement
Decision: **PROTOTYPE after AraBART is available**

Agreement between SWEET and an independently trained seq2seq system on the same local edit is a strong candidate feature, but disagreement must not automatically mean wrong.

### I. Reference-free LLM judge
Decision: **WATCH, not primary verifier**

LLM-as-judge can help review explanations, but current evidence does not justify using a general LLM as the sole automatic Arabic correction verifier.

### J. Strict Scientific mode
Decision: **INTEGRATE**

Even ACCEPT from the linguistic verifier must still pass:
- protected spans
- numbers/units/equations
- citations
- technical terminology
- named entities
- semantic equivalence

### K. Review-forward UX
Decision: **INTEGRATE**

For REVIEW cases show:
- original span
- candidate edit
- morphology surface
- error type/evidence
- reason for abstention
- one-click accept/reject

This turns conservative abstention into usable product behavior.

## Recommended next bounded gate

**Phase 2 — Independent Candidate Acceptance Gate**

Do not create sealed data yet.

Sub-gates:
1. reproduce official AraBART+Morph+GED model on the same 41 development passages;
2. align AraBART output into source-local edit candidates without accepting full rewritten text;
3. construct a gold-independent candidate feature table joining SWEET, AraBART, GED, morphology, deterministic grammar features and safety flags;
4. evaluate transparent acceptance strategies first (rules / calibrated classifier if a proper training split exists);
5. explicitly test whether the gate rejects:
   - وساعٍ → وساعا
   - باسمًا → باسْمٍ
   - إستشعِر → past-tense morphology proposal
6. measure supported-edit precision, useful coverage and review burden clustered by passage;
7. freeze the acceptance policy only after development;
8. then create a new independent sealed Arabic evaluation set.

Success condition:
- high candidate acceptance precision with no known HIGH/CRITICAL grammatical-direction failures;
- materially better useful coverage than DIRECT_PATCH_ONLY;
- runtime decisions use no Nahw target or previous adjudication label.

Failure condition:
- if independent acceptance cannot reject the known counterexamples without collapsing coverage, keep normalized/morphology channel REVIEW_ONLY and return to a narrower Arabic product role.
