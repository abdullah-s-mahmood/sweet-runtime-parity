# Phase 2 — Selectivity Next Gate: Research + Brainstorming

Date: 2026-09-28

This document is DEVELOPMENT guidance only. It does not freeze thresholds, modify SWEET weights, change the sealed-material exclusion set, or authorize production auto-accept.

## Verified post-adjudication evidence

Primary surgical NoPnx1 evidence:
- 60 applied edits across 41 passage clusters.
- 49/60 supported edits = 81.67% supported precision.
- 7 wrong, 2 partial, 2 unnecessary.
- 100 suppressed hazards audited: 51 harmful, 47 unsafe, 2 possibly useful but unsafe, 0 confirmed useful correction lost.
- 22/41 passages are development AUTO_ACCEPT_CANDIDATE by applied-edit quality only; this does **not** mean the passages are fully corrected.
- Target outcomes remain coverage-limited: 27 exact supported + 10 supported alternatives + 2 partial, while 108/150 published target errors remain unresolved.

## Fresh research findings

### Arabic edit tagging remains technically relevant
SWEET frames Arabic GEC as token edit tagging and reports strong benchmark performance plus >6x speed over compared Arabic GEC systems. The paper also reports ensemble improvements, so a candidate-combination route is research-supported, but its published benchmark success does not validate our Nahw/scientific deployment population.
Source: ACL 2025, https://aclanthology.org/2025.acl-long.875/

### Nahw confirms Arabic grammar remains difficult
Nahw evaluates grammar knowledge, error detection, correction, and explanation; even strong models show substantial deficits, and the paper reports natural high-quality data outperforming synthetic fine-tuning in its experiments. This supports keeping our claims narrow and using real human-corrected material for the next validation.
Source: EACL 2026, https://aclanthology.org/2026.eacl-long.296/

### Edit-disentangled evaluation matches our evidence model
CLEME2.0 separates hit-, wrong-, under-, and over-correction, rather than compressing them into a whole-sentence score. This directly supports our target/edit-level evaluation and continued separation of coverage from precision.
Source: ACL 2025, https://aclanthology.org/2025.acl-long.10/

### Selective prediction supports a coverage-risk gate
Selective prediction explicitly treats abstention as a valid decision on low-confidence inputs and studies risk/coverage trade-offs. However, our own development evidence shows top-1 confidence alone is not enough: a wrong deletion reached ~0.970 confidence while a supported edit appeared around ~0.347.
Source: ACL-IJCNLP 2021, https://aclanthology.org/2021.acl-long.84/

### Edit-level voting is a promising later anti-overcorrection mechanism
BEA 2026 shows training-free edit-level majority voting across multiple generated candidates can reduce over-correction on several non-Arabic GEC benchmarks. This is not Arabic evidence, but it is a credible architecture to TEST after we have at least two independently useful Arabic candidate generators.
Source: BEA 2026, https://aclanthology.org/2026.bea-1.60/

### Arabic GED + Seq2Seq is a strong alternative path
Prior Arabic work reports that explicit grammatical error detection (GED) information used as auxiliary input improves GEC across three datasets, using Arabic pretrained Seq2Seq models including AraBART and AraT5. This is especially relevant because our diagnostic shows edits coinciding with known error locations are much safer than collateral edits. Ground-truth target overlap cannot be used in production, but a separate GED module could approximate that localization without benchmark leakage.
Source: EMNLP 2023, https://aclanthology.org/2023.emnlp-main.396/

### Arabic morphology is suitable for independent validation
Camel Morph MSA is a large open-source MSA analyzer/generator integrated with CAMeL Tools. It is a credible independent morphology validator for inflectional, hamza, weak-verb, case-related and agreement candidates, but should validate rather than overwrite scientific text.
Source: LREC-COLING 2024, https://aclanthology.org/2024.lrec-main.240/

### Reversible normalization is justified, irreversible normalization is not
EACL 2026 reports that Arabic diacritics can increase token fragmentation and degrade model performance. This supports testing a reversible normalized model-view with exact offset mapping back to the original source surface, not delivering normalized text directly.
Source: Findings EACL 2026, https://aclanthology.org/2026.findings-eacl.22/

### Minimal-edit behavior remains the right product objective
BEA 2025 shows that minimal-edit GEC deserves distinct optimization/evaluation from fluency editing. This aligns with our source-preserving surgical approach.
Source: BEA 2025, https://aclanthology.org/2025.bea-1.9/

## New diagnostics from the 60 adjudicated surgical edits

Operation-family quality:
- INSERT: 18/19 supported = 94.74%; the only non-supported case was an unnecessary whitespace split.
- REPLACE: 26/32 supported = 81.25%.
- DELETE: 5/9 supported = 55.56%; this is the riskiest family.

Retrospective confidence diagnostics:
- confidence >= 0.80: 38/42 supported, 1 wrong, 2 partial, 1 unnecessary.
- confidence >= 0.90: 35/38 supported, 1 wrong, 2 partial.
- confidence >= 0.98: 26/28 supported, 0 wrong, 2 partial.
These are development-only and must not be frozen from the same adjudication set.

Runtime-observable conservative candidate policy:
- allow non-space INSERT edits;
- allow REPLACE edits only when top-1 confidence >= 0.80;
- abstain on DELETE edits.

Retrospectively on the same development adjudication:
- 38 edits retained;
- 37 supported;
- 0 wrong;
- 1 partial;
- supported precision 97.37%;
- passage-cluster bootstrap 95% interval approximately 91.18%–100%.

This is promising but **not a valid final estimate**, because the rule was discovered on the same development data.

## Important anti-leakage rule

A diagnostic based on “overlaps a Nahw target” must never become a runtime rule. It uses benchmark truth.

What the diagnostic *does* motivate is a separate deployable error-localization model:
GED/error detector → candidate editor → surgical renderer → morphology/safety validation → accept/review/abstain.

## Brainstorming decisions

### 1. NoPnx1 + surgical renderer
**INTEGRATE as the development reference.**
It solved the renderer corruption mode and reached useful edit precision, but coverage remains low.

### 2. One global confidence threshold
**WATCH / do not freeze.**
Confidence contains signal but is not reliable enough alone; high-confidence wrong/partial edits exist.

### 3. Operation-aware selective gate
**PROTOTYPE next.**
Treat INSERT / REPLACE / DELETE differently. Current evidence strongly argues against auto-applying DELETE edits.

### 4. Separate Arabic GED/error-localization gate
**PROTOTYPE with high priority.**
This is the most important new architecture opportunity. It can approximate “known error location” without benchmark leakage and is directly supported by Arabic GEC literature.

### 5. Morphology-aware validator using Camel Morph MSA
**PROTOTYPE after GED feasibility.**
Use it as an independent validator for inflectional/orthographic candidates, not as an unrestricted correction engine.

### 6. Reversible normalization / diacritic-aware model view
**TEST.**
Normalize only the internal model view, maintain source offsets, round-trip every applied edit to the untouched original surface.

### 7. NoPnx2
**TEST_SELECTIVELY.**
The second pass adds two useful repairs but also a wrong regression, a partial repair and unresolved change. Do not run it globally.

### 8. Pnx
**TEST_SELECTIVELY for explicit punctuation mode only.**
It can add useful punctuation but also unnecessary/wrong/unresolved edits and did not improve target recovery in this development extraction.

### 9. AraBART/AraT5-family Arabic GEC candidate
**TEST after the next selectivity gate.**
Use the same 41 development passages and identical surgical/safety evaluation. Do not replace SWEET merely because coverage is limited.

### 10. Candidate ensemble / edit voting
**WATCH now; PROTOTYPE only after two strong candidate sources exist.**
BEA 2026 supports edit-level voting as an over-correction mitigation strategy, but we currently have one validated Arabic candidate source.

### 11. Strict scientific mode vs general Arabic proofreading
**PROTOTYPE as separate policies.**
Scientific mode should demand protected spans, source fidelity, high precision and abstention. General proofreading can tolerate broader corrections but still needs transparent review.

### 12. Narrow SWEET product role
**TEST.**
Current evidence supports positioning SWEET as a precision-oriented Arabic edit candidate generator, not a complete general proofreader.

## Next bounded gate

Do **not** create a sealed benchmark yet.

The next experiment should be:

**Phase 2 — Selective Surgical Gate**

Primary objectives:
1. prospectively implement an operation-aware policy using only runtime-observable features;
2. explicitly abstain on risky DELETE edits;
3. test reversible source mapping/normalization without changing delivered source text;
4. add a separate Arabic GED/error-localization candidate and measure whether it improves precision/coverage;
5. keep NoPnx2 and Pnx as selective ablations, not defaults;
6. compare against the current NoPnx1+surgical baseline on the same development passages;
7. only after that policy is frozen should a new independent sealed Arabic set be created.

The key success question is no longer “Can SWEET correct Arabic?” It is:

**Can a selective, source-preserving architecture achieve sufficiently high edit precision while retaining enough useful correction coverage to justify integration?**
