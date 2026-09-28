# Phase 2 — Contextual Contradiction Veto: Research Start

Date: 2026-09-29

## Evidence motivating the gate

Cross-corpus exact agreement between SWEET NoPnx and AraBART substantially enriched useful edits but still accepted demonstrably wrong corrections.

Current primary cross-corpus result after contextual review:
- 159 exact single-token agreements
- 144 supported/alternative
- 8 wrong
- 6 partial
- 1 unnecessary
- supported precision 90.57%

Therefore a third positive vote is not the immediate priority. The higher-value question is whether orthogonal negative evidence can detect contradictions.

## Fresh research

- Alhafni & Habash, ACL 2025, Arabic text editing GEC: edit-tagging is efficient and interpretable; ensemble combinations improve performance. This supports preserving edit-level evidence instead of returning to full-sentence rewriting.
  https://aclanthology.org/2025.acl-long.875/

- Goto et al., BEA 2026: edit-level majority voting mitigates over-correction across multiple benchmarks, but voting remains an empirical quality mechanism rather than a correctness proof.
  https://aclanthology.org/2026.bea-1.60/

- Wang et al., Findings ACL 2026, COCOGEC: subtle context perturbations can flip GEC predictions, directly motivating context-sensitive contradiction checks.
  https://aclanthology.org/2026.findings-acl.195/

- Goto et al., Findings EMNLP 2025: reference-free and LLM-based GEC metrics can be adversarially unreliable; a single neural judge should not replace multi-evidence safety.
  https://aclanthology.org/2025.findings-emnlp.1356/

- CamelParser2.0 provides Arabic dependency parsing with tokenization, POS and rich morphology across diverse genres. It is a candidate for a later syntactic veto, but parser output must itself be validated before becoming safety evidence.
  https://aclanthology.org/2023.arabicnlp-1.15/

## Diagnostic order

Start with evidence already available in the frozen stack:
1. post-edit QALB14 GED contradiction;
2. contextual CAMeL morphology availability;
3. only if separation is inadequate, prototype parser/lexical-context evidence.

No threshold sweep.
No lexical blacklists.
No production promotion from the consumed slice.
