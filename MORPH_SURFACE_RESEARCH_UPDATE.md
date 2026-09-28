# Focused research before and after surface adjudication

Date: 2026-09-28. Scope: Arabic morphology, case/mood and source-preserving correction. No market cycle, benchmark, model tuning or new phase.

## Before pass 1

1. Camel Morph MSA provides a broad open morphological analyzer and generator. It enumerates possible forms, not a proof that a proposed upstream edit fits a sentence. This distinction matters for proper-name fallback and inflectional errors. Khairallah et al., LREC-COLING 2024: https://aclanthology.org/2024.lrec-main.240/
2. CAMeL's BERT unfactored disambiguator ranks morphological analyses in context; its documented interface is disambiguation, not correction validation. The MLE and BERT rankings are therefore evaluated separately. https://camel-tools.readthedocs.io/en/latest/api/disambig/bert.html and https://camel-tools.readthedocs.io/en/stable/api/morphology/reinflector.html
3. Arabic core vowels and syntactic case endings are distinguishable modeling problems. A morphologically informed diacritizer can address both, but a surface generator must respect already supplied user marks. Elmallah et al., LREC-COLING 2024: https://aclanthology.org/2024.lrec-main.128/
4. Multi-reference Arabic diacritization research recognizes genuine surface ambiguity, including valid case variants in context. Exact Unicode equality is therefore not equivalent to grammatical correctness. Mohamed & Mubarak, EMNLP 2025: https://aclanthology.org/2025.emnlp-main.846/
5. Nahw's published explanations localize case, mood and agreement errors; a single local correction is not whole-passage gold. Mubarak et al., EACL 2026: https://aclanthology.org/2026.eacl-long.296/

## After pass 2: observed mechanisms and inferences

- On the 13 target-overlapping rows, contextual BERT top-one provides 10 linguistically correct surfaces, MLE top-one seven, and BERT top-two consensus seven. This is development evidence on clustered passages, not a population accuracy claim. CAMeL BERT is useful as a *surface ranker*.
- Consensus accepted `وساعا` as a proper-name-like form although syntax and the Nahw explanation require `وساعيًا`. The analysis proves that morphology rank agreement alone does not validate correction direction. This is an inference from this project, not a claim from CAMeL's paper.
- BERT's top-one `باسْمٍ` conflates the prepositional noun `اسم` with adjectival `باسمٌ`; both BERT and MLE propose a past verb for the source imperative `إستشعِر`. Contextual scoring is fallible for lexical identity and mood.
- The nine label-bounded runtime proposals are linguistically correct in our second review, but only three satisfy strict minimal source-preserving auto-candidate conditions; three are alternate fathatan/alif serialization and three add unnecessary ending marks. Their 0/9 wrong is selection-biased by prior human labels.
- Existing Arabic GEC models AraT5/AraBART are candidates for an independent second generator, not evidence that its suggestions can be trusted. Alhafni et al., EMNLP 2023: https://aclanthology.org/2023.emnlp-main.396/
- Minimal-edit GEC and edit-level combination research motivates local source edits and independent candidate checking. These studies do not establish Arabic performance here. https://aclanthology.org/2025.bea-1.9/ ; https://aclanthology.org/2026.bea-1.60/ ; https://aclanthology.org/2023.emnlp-main.785/
- Selective prediction research describes the coverage versus abstention problem, but cannot supply a safe policy for this Arabic gate without independent evaluation. https://aclanthology.org/2023.acl-long.55/

## Research-backed next bounded questions

A correction-quality verifier must judge edit direction independently of Nahw gold and prior human labels. Test deterministic case/mood constraints plus an independent candidate source and protected-span/semantic checks on development material first. Separately define canonical terminal-alif/tanween serialization and optional marking under an exact DOCX/text source policy. No such new experiment or runtime change was performed in this adjudication.
