# Midphase focused research update

## Before adjudication

- SWEET's primary paper describes token-edit tagging for Arabic and reports speed and benchmark results; these published scores do not establish performance on these 41 Nahw passages or scientific prose. Source: https://aclanthology.org/2025.acl-long.875/
- Nahw is a grammar detection, correction and explanation benchmark. Its explanations support local grammatical decisions here; a one-location corrected reference is not a gold fully corrected passage. Source: https://aclanthology.org/2026.eacl-long.296/ and the project's pinned Nahw-Passage.json.
- Single-reference GEC evaluation can miss valid alternatives; minimal-edit and edit-level judgments should be kept distinct from whole-passage matching. Sources: https://aclanthology.org/2025.bea-1.9/ and https://aclanthology.org/2025.findings-acl.1322.pdf

## After adjudication: findings relevant to interpretation

- The queue shows four target outputs that plausibly fulfill the Nahw rule without optional diacritics (ITEM-075, 201, 434, 508). They should not be scored as wrong solely for differing from the printed reference. Two others show only partial repair (ITEM-098, 332).
- Many other changed targets are lexical loss or bracketed unknown-token fragments; source-to-output text must be separated from the model's non-K edits. The upstream demonstration uses BertTokenizer and gec.tag.rewrite, which explains why the exact input/tokenization/renderer boundary matters; the paper does not validate these corruptions as acceptable. Source: https://github.com/CAMeL-Lab/text-editing
- The Arabic GEC literature includes sequence-to-sequence models and error-detection auxiliary input across genres, so a different generator or routing is a testable fallback if coverage remains low. Source: https://aclanthology.org/2023.emnlp-main.396/
- End-to-end alignment and detokenization can change measured edits; keep literal output corruption and formatting effects visible in the review burden, but do not count whitespace as grammatical improvement. Source: https://aclanthology.org/2025.coling-main.52.pdf
- Current sources do not demonstrate scientific-text invariant preservation for SWEET. The 12 authored scientific stress cases are not human-gold GEC references and are excluded from these accuracy counts.

## Scope

This is a focused method check around the existing outputs; no market research, new benchmark or new inference was performed. Review decisions rest primarily on Nahw's published local explanation and the recorded raw output. Ambiguous collateral edits remain REVIEW_REQUIRED.
