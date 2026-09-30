# M2-H Component Inventory and Selection

Date: 2026-09-30
Status: FROZEN BEFORE DOWNLOAD OR EXECUTION

## H1 — Structured edit candidate generator

Selected primary candidate:
- CAMeL-Lab text-editing, QALB14 no-punctuation checkpoint.
- Official code/models repository.
- MIT code license.
- Explicit edit representation.
- Reproducible environment documented.

Role:
- over-generating structured edit candidates;
- NOT final verifier;
- NOT sentence-completeness oracle.

## H2 — Orthographic validator

Selected direction:
- deterministic high-precision orthographic rules;
- CAMeL morphology/lexicon evidence where relevant;
- no LLM approval as a safety condition.

Goal:
- maximize precision first;
- report coverage separately.

## H3 — Morphology validator

Selected initial tool family:
- CAMeL Tools / CALIMA-MSA evidence.

Notes:
- CAMeL Tools code is MIT;
- data/model package licensing must be tracked separately;
- research feasibility is allowed;
- packaging/commercial implications remain unresolved.

Fallback:
- CAMeL Morph for open morphology-model construction if required.

## H4 — Structural Split/Merge validator

Targeted literature/tool search did NOT identify an off-the-shelf component that simultaneously satisfies:
- Arabic;
- direct erroneous-word-boundary verification;
- independent of H1;
- open/reproducible implementation;
- acceptable licensing for the longer-term product path;
- explicit Split/Merge precision/recall suitable for the M2-H contract.

Rejected as primary H4:
- Farasa Segmenter: useful Arabic segmentation technology, but not a direct erroneous-space verifier; repository states research-purpose-only licensing for the package.
- ARETA: useful gold/evaluation taxonomy, but requires system output/reference and is not a standalone verifier.
- generic seq2seq spell correctors: not independent structural validators and would reproduce generation-style failure modes.

Historical evidence retained:
- QALB systems treated Split/Merge as case-specific correction problems;
- prior Arabic spelling correction combined lexicon/morphology and language-model evidence for run-on/split candidates;
- deterministic shallow rules have historically been useful for high-frequency Arabic boundary phenomena.

Decision:
**Build H4 locally as a bounded deterministic high-precision validator.**

## Evaluation taxonomy

Use:
- QALB M2 operation labels as primary reproducible operation gold;
- ARETA only when taxonomy annotation is needed and methodologically valid.

## Independence principle

H1 and H4 must not be the same model under two names.

H4 may inspect a candidate proposed by H1, but H4's decision evidence must be independently derived from:
- token boundary structure;
- morphology/analyzability;
- explicit Arabic clitic/orthographic constraints;
- optionally a separately frozen contextual plausibility signal.

## Current feasibility status

H1 availability: PASS.
H2 implementation path: PASS for feasibility.
H3 availability: PASS with licensing caveat.
H4 off-the-shelf availability: FAIL / local implementation selected.
Overall M2-H component availability: **IMPROVED / FEASIBLE TO IMPLEMENT**, with H4 as the principal unresolved engineering risk.
