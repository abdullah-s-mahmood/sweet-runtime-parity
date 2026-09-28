# Phase 2 — FINAL_ALIF Gate Research Start

Date: 2026-09-28

Fresh evidence considered:
- CamelParser2.0 provides Arabic dependency parsing with tokenization, POS and rich morphological features across multiple Arabic genres. It is a plausible future source of subject/controller evidence for nun-family corrections, but parser error must itself be validated before becoming a safety gate.
- ACL 2025 Arabic text editing supports interpretable local edits but does not imply local surface shape is sufficient for contextual correctness.
- Context-robustness literature reinforces that correction validity can change under contextual perturbation.

Decision:
- test the narrower FINAL_ALIF family now;
- keep nun-family REVIEW-only;
- do not introduce parser complexity until a separately falsifiable NUN_CONTEXTUAL gate is designed.
