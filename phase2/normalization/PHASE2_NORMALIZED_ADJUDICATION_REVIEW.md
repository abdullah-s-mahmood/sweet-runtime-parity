# Phase 2 — Normalized Candidate Adjudication Review and Next Gate

Date: 2026-09-28

Status: DEVELOPMENT REVIEW COMPLETE. Not sealed. No production threshold frozen. Phase 3 not started.

## Verified adjudication evidence

Canonical manifest commit:
- 12b0c5cc44a1f827314959b9f438652492194718

Evidence commit recorded in manifest:
- 4fe6f976e60b2fc03750749842e6824df6846c67

Population:
- 19 normalized candidates
- 14 passages
- 13 published Nahw targets touched
- 12 automated normalized target matches rechecked
- 9 automated matches confirmed
- 9 new supported target recoveries previously ERROR_PRESERVED

Candidate classes:
- SUPPORTED_CORRECTION: 12
- SUPPORTED_ALTERNATIVE: 1
- PARTIAL_CORRECTION: 4
- UNNECESSARY_EDIT: 1
- WRONG_CORRECTION: 1
- REVIEW_REQUIRED: 0

Candidate-level supported-or-alternative precision:
- 13/19 = 68.42%

Directionally useful candidates including partial:
- 17/19 = 89.47%

The population is small and clustered. These are development proportions, not independent production precision estimates.

## Surface realization is now the principal blocker

Only 2/19 candidates are currently classified as safe local source realizations:
- NORM-45-17-0: إشتدادًا → اشتدادًا (patch initial hamza while preserving final tanween/punctuation)
- NORM-63-11-0: إستشعِر → استشعِر (patch initial hamza while preserving internal kasra)

15 candidates require nontrivial source-surface reconstruction:
- CASE_ENDING_OR_TANWEEN_REQUIRED: 10
- BASE_LETTER_PLUS_DIACRITIC_CHANGE_REQUIRED: 4
- INFLECTIONAL_RECONSTRUCTION_REQUIRED: 1

The remaining two candidates are wrong/no-op and should not be realized.

This means source-span identification succeeded geometrically, but correct Arabic surface realization requires morphology, case/mood, agreement, and diacritic handling.

## Operation-family interpretation

INSERT:
- 7 candidates
- 6 supported
- 1 wrong
- 0 partial

REPLACE:
- 8 candidates
- 7 supported
- 1 unnecessary
- 0 wrong

DELETE:
- 4 candidates
- 0 fully supported
- 4 partial

This strongly reinforces keeping normalized DELETE candidates out of any automatic path. In this population they remove part of a bad ending but fail to restore the required nominative/case diacritic.

## Confidence is not a safe decision rule

Confidence distributions overlap:
- supported corrections include confidence as low as ~0.427
- the wrong candidate NORM-38-24-0 has confidence ~0.974
- partial candidates include confidence up to ~0.9999

Therefore no global confidence threshold should be tuned or frozen from this population.

## Target-level impact

The normalized channel confirmed 9 new supported target recoveries among targets that the surgical path previously left as ERROR_PRESERVED.

Three of the 12 automated normalized target matches were only partial because dediacritized equality masked missing nominative/case realization:
- كريمًا → كريم (needs كريمٌ)
- باسمًا → باسم (needs باسمٌ)
- واقعًا → واقع (needs واقعٌ)

This is the key lesson: normalized base-word equality is useful candidate evidence but is not sufficient proof of a correct Arabic correction.

## Scientific safety

The normalized scientific stress diagnostic generated two harmful candidates:
- SCI-DEV-03: corrupts the technical phrase فاصل الثقة
- SCI-DEV-12: deletes punctuation from “al.” before citation [12]

Neither was applied. Therefore Strict Scientific mode should keep normalized candidates behind review/safety validation and retain citation/technical-term firewalls.

## Fresh external research — 2026 update

1. **Diacritics and tokenization.**
   Inoue et al. (Findings EACL 2026) show that increasing Arabic diacritization increases subword fragmentation across tokenizers and can degrade downstream performance. This supports a reversible internal normalized view, but not automatic surface rewriting.
   https://aclanthology.org/2026.findings-eacl.22/

2. **Diacritics-aware Arabic representation is becoming an explicit model-design concern.**
   NeoAraBERT (Findings ACL 2026) includes diacritics-aware tokenization as a design variable, which supports treating diacritics as first-class model evidence rather than incidental characters.
   https://aclanthology.org/2026.findings-acl.1293/

3. **Case endings remain a difficult subproblem.**
   Recent Arabic diacritization work continues to separate core-word diacritics from case endings. The 2024 morphologically informed character model explicitly models both, and OSACT 2026 system reports again identify case endings/vowel ambiguity as major error sources.
   https://aclanthology.org/2024.lrec-main.128/
   https://aclanthology.org/2026.osact-1.28/

4. **Modern Arabic diacritization can preserve user-specified marks.**
   Mohamed & Mubarak (EMNLP 2025) report a model variant that preserves user-specified diacritics. This is directly aligned with our requirement to keep authoritative source marks whenever they do not need correction.
   https://aclanthology.org/2025.emnlp-main.846/

5. **CAMeL Morph MSA is suitable as an independent morphology engine.**
   Camel Morph MSA exposes case, mood, state, gender, number, person, voice and diacritized-form features and can analyze/generate/reinflect forms. It is a strong candidate validator/generator for the 15 ambiguous surface cases.
   https://aclanthology.org/2024.lrec-main.240/
   https://camel-tools.readthedocs.io/en/master/reference/camel_morphology_features.html
   https://camel-tools.readthedocs.io/en/latest/cli/camel_morphology.html

6. **Contextual morphosyntactic disambiguation exists in CAMeL Tools.**
   The BERTUnfactoredDisambiguator predicts contextual features including case (cas) and mood (mod), which are exactly the missing dimensions in several normalized candidates.
   https://camel-tools.readthedocs.io/en/v1.5.5/api/disambig/bert.html

7. **Arabic GEC remains a multi-component problem.**
   SWEET provides an efficient edit-tagging candidate source, but the paper also reports ensemble gains. This supports preserving SWEET as one candidate generator while adding independent validation rather than expanding raw rewrite behavior.
   https://aclanthology.org/2025.acl-long.875/

## Maximum-effort architecture brainstorming

### A. Morphology-aware surface realization
Decision: **PROTOTYPE NEXT**

Pipeline:
source token
→ normalized candidate
→ CAMeL Morph analyses/generation
→ contextual morphosyntactic features (case/mood/state/number/gender/person)
→ candidate surface forms
→ exact source-mark preservation where compatible
→ explicit diacritic delta
→ safety checks
→ apply/review/abstain

This directly targets the observed blocker rather than adding another correction model prematurely.

### B. Contextual BERT morphological disambiguator
Decision: **TEST WITH CAMeL Morph, not alone**

Use case/mood/state predictions as one source of evidence. Do not let one contextual tagger auto-write the correction.

### C. Controlled diacritic realization
Decision: **PROTOTYPE**

Rules:
- untouched characters remain byte-for-byte original;
- marks outside edited morpheme are preserved;
- any changed case/mood mark must be explicit in the candidate trace;
- case-ending/tanween changes require contextual morphological support;
- if candidate has multiple valid surface forms, abstain.

### D. Preserve user/source diacritics
Decision: **INTEGRATE AS INVARIANT**

The EMNLP 2025 result that user-specified marks can be preserved aligns with our strict-fidelity requirement. Existing correct source marks should not be globally rediacritized.

### E. Normalized DELETE candidates
Decision: **REVIEW/ABSTAIN**

All four were partial in this population. A DELETE may remove the wrong ending but cannot by itself prove the required replacement case mark.

### F. Normalized INSERT/REPLACE
Decision: **TEST AFTER MORPHOLOGY VALIDATION**

They are more promising than DELETE, but one INSERT was wrong and one REPLACE was a no-op. Operation family alone is not enough.

### G. Broader orthographic normalization
Decision: **DROP FOR NOW**

Do not normalize Alef variants, Alef Maksura/Yeh, or Teh Marbuta/Heh in the candidate view because those distinctions are themselves correction targets.

### H. Second Arabic GEC candidate source
Decision: **WATCH / TEST AFTER SURFACE REALIZATION GATE**

AraBART/AraT5 remains the next alternative if morphology-aware realization cannot unlock enough of the 15 ambiguous supported/partial candidates. Adding a second model before solving source realization would create more candidates that we still cannot safely apply.

### I. Diacritization model as a surface validator
Decision: **TEST LATER, not primary next step**

A model that preserves user marks could help rank alternative vocalized realizations, but it should not replace deterministic source alignment + morphology constraints.

### J. Strict Scientific mode
Decision: **INTEGRATE ARCHITECTURALLY**

Normalized candidates remain REVIEW_ONLY or blocked near:
- citations
- numbers/units
- formulas
- p-values/confidence intervals
- technical terms
- protected entities

## What improved

- 9 previously missed targets now have linguistically supported normalized correction directions.
- normalized candidate generation is useful: 13/19 are supported or supported alternatives.
- 17/19 are at least directionally useful if partial corrections are included.
- exact source provenance is preserved; no normalized output was written into source.
- only two candidates are clearly bad/no-op.

## What worsened / became clearer

- the optimistic “12 automated matches” fell to 9 confirmed.
- only 2/19 can currently be realized safely on the fully diacritized source without deeper morphology/syntax.
- the main bottleneck has moved from tokenization to **surface realization and morphosyntactic disambiguation**.
- normalized confidence is not a reliable safety signal.

## Current forecast

The normalized channel is worth keeping, but only as a secondary recovery channel after base surgical abstention.

The highest-value next experiment is not another broad GEC model yet. It is a bounded **Morphology-Aware Surface Realization Gate** on the existing 19 adjudicated candidates.

Success criterion:
- safely realize a substantial fraction of the 13 supported/alternative + 4 partial candidates;
- exact Unicode preservation outside the corrected morpheme;
- zero wrong surface applications;
- explicit abstention whenever case/mood/agreement remains ambiguous.

If this gate cannot safely realize enough candidates, then test AraBART/AraT5 as a second Arabic correction source.
