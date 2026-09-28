# Phase 2 — Morphology-Aware Surface Realization Gate: Research Start

Date: 2026-09-28

Status: DEVELOPMENT ONLY. This gate does not change SWEET, does not create a sealed benchmark, does not start Phase 3, and does not authorize production auto-application.

## Established input evidence

Normalized candidate adjudication:
- 19 candidates across 14 passages
- 12 SUPPORTED_CORRECTION
- 1 SUPPORTED_ALTERNATIVE
- 4 PARTIAL_CORRECTION
- 1 WRONG_CORRECTION
- 1 UNNECESSARY_EDIT
- 9 new supported target recoveries
- 2 currently low-ambiguity local surface patches
- 15 candidates require morphology/case/mood/diacritic reconstruction

The immediate bottleneck is no longer tokenization. It is source-preserving Arabic surface realization.

## Fresh research before implementation

### CAMeL Morph directly supports the required morphological dimensions

CAMeL Tools morphology provides analysis, generation, and reinflection over the CALIMA MSA database. Its feature inventory explicitly includes:
- cas: nominative / accusative / genitive
- mod: indicative / jussive / subjunctive
- stt: construct / definite / indefinite
- gender, number, person, aspect, voice

References:
- https://camel-tools.readthedocs.io/en/latest/cli/camel_morphology.html
- https://camel-tools.readthedocs.io/en/stable/api/morphology/reinflector.html
- https://camel-tools.readthedocs.io/en/master/reference/camel_morphology_features.html

### CAMeL morphology must not be allowed to silently normalize the delivered source

The default Analyzer normalization collapses distinctions including Alef variants, Alef Maksura/Yeh, and Teh Marbuta/Heh. Several of these distinctions are themselves Arabic GEC targets, so this gate will use morphology as a candidate validator/ranker and will always filter generated forms back through our own exact base-letter/source-preservation constraints.

Reference:
- https://camel-tools.readthedocs.io/en/stable/api/morphology/analyzer.html

### Case endings are a separate hard subproblem

Arabic diacritization research explicitly distinguishes core-word diacritics from case endings. This matches our observed failure mode where normalized equality hid incomplete nominative/accusative realization.

Reference:
- https://aclanthology.org/2024.lrec-main.128/

### Preserving user-provided diacritics is technically justified

Recent Arabic diacritization work reports a model variant that preserves user-specified diacritics. This supports the gate invariant that correct source marks should remain untouched unless the corrected morpheme explicitly requires a change.

Reference:
- https://aclanthology.org/2025.emnlp-main.846/

### Morphological structure cannot be reduced to tokenizer behavior

LREC 2026 reports that tokenizer morphological alignment is neither necessary nor sufficient for Arabic morphological generation. This reinforces the need for an explicit morphology/surface layer after SWEET rather than assuming better tokenization solves inflection.

Reference:
- https://aclanthology.org/2026.lrec-1.923/

### Contextual morphological disambiguation is desirable, but reproducibility must be verified

CAMeL Tools exposes a BERTUnfactoredDisambiguator whose feature set includes case and mood. The public API supports contextual sentence disambiguation, but model/data availability must be verified in the pinned runtime before it can become a required dependency.

Reference:
- https://camel-tools.readthedocs.io/en/v1.5.5/api/disambig/bert.html

## Gate design fixed before execution

This bounded gate will use two evidence layers:

1. **Morphology lattice**
   - CAMeL Morph MSA analyses for each normalized candidate word.
   - retain only analyses whose dediacritized/base-letter form matches the candidate exactly under our narrow Mn/tatweel view.
   - record diacritized surface, POS, case, mood, state, gender, number, person, aspect and voice.

2. **Morphological prior / disambiguation**
   - CAMeL MLE MSA disambiguator as a reproducible ranking prior.
   - it is out-of-context and MUST NOT be described as contextual syntactic proof.
   - contextual BERT morphology is tested only as an optional feasibility probe if its pretrained resources are available reproducibly.

## Source-preserving realization invariant

For every proposed surface:
- original source remains authoritative;
- punctuation outside the edited token remains byte-for-byte identical;
- unchanged source letters remain unchanged;
- source diacritics outside the edited morphological neighborhood remain unchanged;
- no broad Alef/Ya/Teh-Marbuta normalization is allowed;
- any new or deleted case/mood mark is explicitly logged;
- ambiguity causes abstention.

## Evaluation-only use of Nahw references

Published Nahw corrections/explanations may be used only AFTER morphology inference to evaluate whether a proposed realization is compatible with the known local correction.

They must not select the runtime morphology candidate.

## Pre-registered questions

Q1. For how many of the 15 ambiguous candidates does CAMeL Morph contain a compatible grammatical surface form?

Q2. For how many cases does a target-independent morphology ranking produce one unique minimally source-preserving surface?

Q3. How often does MLE top-1 morphology agree with the adjudicated correction direction?

Q4. Can the two previously safe local patches remain exact under morphology verification?

Q5. Do DELETE-derived partial candidates remain ambiguous after morphology analysis?

Q6. Does morphology reject the known wrong defective-noun candidate وساعا?

## Success criteria

Primary development success:
- zero wrong **automatic** surface applications;
- exact source preservation outside the corrected token/morpheme;
- explicit abstention for unresolved case/mood/agreement;
- safely realize more than the existing 2 low-ambiguity candidates.

Secondary:
- demonstrate that correct surface forms exist in the CAMeL morphology lattice for a substantial fraction of the 15 ambiguous useful candidates.

If morphology can generate but cannot reliably select the correct contextual form, the next gate should focus on contextual morphosyntactic ranking rather than adding a second GEC generator.
