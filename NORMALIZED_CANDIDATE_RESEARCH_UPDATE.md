# Focused research before and after normalized candidate adjudication

Date: 2026-09-28. This is a development gate, not a new benchmark or model run.

## Before adjudication: relevant evidence

- Inoue et al., *Do Diacritics Matter?* (Findings of EACL 2026), report that Arabic diacritics can increase subword fragmentation. This is consistent with the observed 98/98 tokenizable normalized views, but does not establish correction quality. https://aclanthology.org/2026.findings-eacl.22/
- Mohamed & Mubarak, *Advancing Arabic Diacritization* (EMNLP 2025), introduce multi-reference evaluation because valid diacritization can differ with linguistic context. Therefore stripping marks cannot serve as a case/mood correctness oracle. https://aclanthology.org/2025.emnlp-main.846/
- Khairallah et al., *Camel Morph MSA* (LREC-COLING 2024), provide an open analyzer and generator suitable for testing candidate morphological constraints. An out-of-context analysis is not a syntactic decision for a full passage. https://aclanthology.org/2024.lrec-main.240/
- CAMeL Tools morphology documentation describes analysis, generation and reinflection, including diacritized output and feature requirements. Its default normalization can be broader than the source-fidelity view; use it as a validator, not as a writer of source text. https://camel-tools.readthedocs.io/en/stable/api/morphology/reinflector.html and https://camel-tools.readthedocs.io/en/stable/api/morphology/analyzer.html
- Nahw published local correction explanations are the primary grammatical evidence for 13 overlapping targets, not whole-passage gold. Source: project-pinned `phase1/iteration4/source/Nahw-Passage.json`, SHA-256 `97d4f5e0b75ff5848ffdff113a74676c0de607d0bb877e1f26c1bde1585a2208`; paper https://aclanthology.org/2026.eacl-long.296/

## After adjudication: interpretation and challenge

- Nine of 12 automated normalized target matches have a supported **base-word direction**; three delete the wrong accusative ending without restoring nominative marking. The nine still need source-surface realization; the two simple hamzat-al-wasl replacements are the only currently low-ambiguity local patches. These are our own development judgments, not a paper's result.
- Case and mood cannot be inferred by dediacritized equality. `مالٌ`→`مالا` needs `مالًا`, while `المصريِّين`→`المصريون` needs a new stem vowel. A morphology generator can enumerate valid forms; context and source marks must select among them. The multi-reference diacritization work reinforces this limitation. https://aclanthology.org/2025.emnlp-main.846/
- Alhafni et al., *Advancements in Arabic GEC* (EMNLP 2023), investigate Arabic detection/correction models including AraT5 and AraBART. Their existence supports testing an independent generator if coverage remains limited, without assuming its outputs are safe. https://aclanthology.org/2023.emnlp-main.396/
- SWEET's token edit formulation supplies interpretable candidate provenance, but the observed identity label and malformed defective noun show that a tag is not grammatical proof. https://aclanthology.org/2025.acl-long.875/
- Staruch et al. (BEA 2025) and Goto et al. (BEA 2026) investigate minimal edits and edit-level combination to address over-correction. The latter's English-focused result is a design analogy, not measured Arabic performance here. https://aclanthology.org/2025.bea-1.9/ and https://aclanthology.org/2026.bea-1.60/

## Inference for next bounded engineering experiment

Keep the normalized channel after surgical abstention and under review. Test a surface realization layer on these existing adjudicated candidates, with character-level source offsets, morphology/case features, preservation of unaffected marks, exact round-trip checks, and an abstain state. Separately compare a second Arabic generator only if its edits can be projected and reviewed with the same source-preserving interface. Neither experiment was run here. No confidence threshold, normalization broadening, or production rule is justified by 19 clustered candidates.
