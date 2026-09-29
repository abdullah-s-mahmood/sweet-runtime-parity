# M2-R — Fresh Research Start: Residual Span Hunter

Date: 2026-09-30
Status: PRE-REGISTERED BEFORE DATA MATERIALIZATION OR MODEL JUDGMENT

## Trigger

M2 P0/P1 showed that a monolithic sentence-level frontier judge could trade safety for coverage but could not satisfy both. P1 accepted at least three candidates with clear remaining Hamza errors.

The next justified experiment changes the task formulation rather than tuning the same judge prompt.

## Fresh research

### ArabiGEE (2026)
Elhady et al. introduce the first hierarchical Arabic grammatical-error explanation taxonomy grounded in explicit error types. It has:
- 27 error types;
- 140 correction types;
- 324 structured explanations;
- manually annotated portions of existing Arabic GEC corpora.

The public dataset exposes:
- erroneous_word;
- target_word;
- ARETA label;
- lexical / orthographic / morphological / syntactic explanation codes and text;
- erroneous and corrected sentence contexts, with and without punctuation.

This is unusually well matched to an auditable residual-error detector.
Paper: https://arxiv.org/abs/2606.10765
Dataset: https://huggingface.co/datasets/khaled44/arabigee-data

### ARETA
Belkebir & Habash (CoNLL 2021) provide a structured Arabic error taxonomy spanning orthography, morphology, syntax, semantics, punctuation, merge and split; ARETA reports 85.8% micro-F1 on a manually annotated blind ALC portion.
https://aclanthology.org/2021.conll-1.47/

### Nahw
Mubarak et al. (EACL 2026) show substantial remaining Arabic grammar deficiencies even in strong LLMs and emphasize the value of natural high-quality data.
https://aclanthology.org/2026.eacl-long.296/

### LLM judge reliability
Fu & Liu (Findings EMNLP 2025) show multilingual LLM-as-judge consistency is low on average and weaker in low-resource settings. This supports decomposing the task into verifiable claims rather than a single global verdict.
https://aclanthology.org/2025.findings-emnlp.587/

### GEC evaluation
Goto et al. (TACL 2026) show edit-focused representations are more appropriate than whole-sentence similarity for GEC evaluation.
https://aclanthology.org/2026.tacl-1.77/

Rozovskaya & Roth (ACL 2026) demonstrate that fixed references can undercount valid corrections. Therefore M2-R separates:
- error localization;
- correction exact match;
- mandatory-vs-optional interpretation.
https://aclanthology.org/2026.acl-long.2193/

## Key design choice

M2-R uses ArabiGEE **contexts without punctuation** for its primary linguistic test. Punctuation is excluded from the primary gate because:
- Arabic punctuation is partly register/style sensitive;
- punctuation-only reference differences weakened the interpretation of M2;
- the target bottleneck is mandatory residual grammar/spelling, not formatting preference.

Punctuation may be evaluated later as a separate task.

## Research question

Can a strong frontier reasoning model identify **remaining mandatory Arabic error spans** with enough recall and low enough false-positive rate to serve as one auditable component of a future verifier architecture?

M2-R is not an ACCEPT/REJECT judge.
