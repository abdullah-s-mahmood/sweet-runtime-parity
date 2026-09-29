# M1-A — Fresh Research Start: Expert-Grounded Reference Bootstrap

Date: 2026-09-30  
Status: PRE-REGISTERED BEFORE BOOTSTRAP MATERIALIZATION

## Permanent phase rule

Every ACAD_PASS research iteration must:
1. perform fresh research at the start;
2. perform explicit adversarial brainstorming before implementation;
3. preserve prior negative evidence and challenge the proposed direction;
4. perform fresh research/brainstorming again at the end;
5. report IMPROVED / WORSENED / MIXED versus the preceding state;
6. quantify change only with comparable metrics;
7. provide a grounded forecast plus main risks/blockers.

This rule applies to M1-A and future phases.

## Problem

M1 originally required two independent qualified Arabic reviewers. They are not currently available. The project must not:
- relabel agent judgments as human gold;
- stop all research until reviewers become available;
- treat one corpus reference as an infallible oracle;
- consume new sealed/reserved evidence merely to compensate for unavailable reviewers.

M1-A therefore asks a narrower question:

> Can already-published expert human corrections provide a defensible bootstrap for the parts of the M1 contract they directly support, while leaving unsupported dimensions explicitly unresolved?

## Fresh research findings

### QALB expert correction framework
Zaghouani et al. (LREC 2014) describe QALB as a manually annotated Arabic corpus intended both for model development and as a gold standard for error-correction evaluation.

Zaghouani et al. (LAW 2015) provide stronger operational evidence for L2 correction:
- corrections should use a minimum number of edits while producing semantically coherent and grammatically correct Arabic;
- correctness and coherence take priority over minimizing edits;
- unfamiliar but acceptable style should not be rewritten merely to sound more native;
- six annotators with strong Arabic backgrounds participated, with an annotation manager;
- IAA portions were corrected by at least three annotators;
- a second IAA round with another pool of three annotators reached average WER 3.35%;
- documented disagreements show that multiple valid interpretations/corrections can exist.

Implication: QALB is strong evidence for *expert-supported corrections and known reference residuals*, but reference mismatch alone cannot prove that a candidate is wrong.

### Evaluation granularity
SEEDA (TACL 2024) separates edit-level and sentence-level human judgments and shows that granularity matters in GEC meta-evaluation.

Implication: M1-A must not collapse local edit correctness into sentence repair completeness.

### Arabic human-centric evaluation
Ara-HOPE (VarDial 2026) uses an explicit error taxonomy and decision-tree annotation protocol for Arabic post-editing evaluation.

LQM (Findings ACL 2026) uses expert span-level human annotation across sociolinguistic, pragmatic, semantic, morphosyntactic, orthographic, and graphetic levels, with severity-weighted quality scores.

Implication: an explicit multidimensional contract is better supported than a single safe/unsafe label.

### Scientific revision evaluation
Jourdan et al. (ACL 2025) report that LLM-as-judge methods can assess instruction-following but struggle with correctness; hybrid evaluation combining LLM judgment and task-specific metrics is more reliable.

Implication: expert-reference bootstrap can calibrate a future strong judge, but does not justify replacing human confirmation for scientific fidelity.

### Human effort
Vadehra et al. (HCI+NLP 2025) show that post-editing time is a useful human-centered GEC evaluation dimension.

Implication: later ACAD_PASS evaluation should include review burden/time, not precision alone.

## Source policy

Primary executable sources for M1-A:
- QALB14 L1 TRAIN and DEV only, pinned to CAMeL-Lab/arabic-gec revision 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf.
- Existing frozen Nahw Phase-2 development evidence already present in this repository.

Explicitly excluded:
- all QALB14 TEST;
- all QALB15 DEV/TEST;
- any new QALB15 TRAIN slice;
- the 59 reserved Nahw passage IDs;
- sealed/final benchmark material.

QALB14 TRAIN/DEV are already consumed by the preceding CAD work, so M1-A does not spend fresh evaluation evidence.

## References

- Zaghouani et al. 2014. Large Scale Arabic Error Annotation: Guidelines and Framework. https://aclanthology.org/L14-1721/
- Zaghouani et al. 2015. Correction Annotation for Non-Native Arabic Texts: Guidelines and Corpus. https://aclanthology.org/W15-1614/
- Kobayashi et al. 2024. Revisiting Meta-evaluation for Grammatical Error Correction. https://aclanthology.org/2024.tacl-1.47/
- Jourdan et al. 2025. Identifying Reliable Evaluation Metrics for Scientific Text Revision. https://aclanthology.org/2025.acl-long.335/
- Vadehra et al. 2025. Time Is Effort. https://aclanthology.org/2025.hcinlp-1.15/
- Alabdullah et al. 2026. Ara-HOPE. https://aclanthology.org/2026.vardial-1.13/
- Magdy et al. 2026. LQM. https://aclanthology.org/2026.findings-acl.2012/
