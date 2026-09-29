# Local-Edit Semantic Backstop — Research Start

Date: 2026-09-29

## Fresh checks

1. MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7 remains publicly available with an MIT license and multilingual NLI support. Its config maps entailment=0, neutral=1, contradiction=2; ONNX variants are also published.
2. The 2025 EMNLP Findings paper Reliability Crisis of Reference-free Metrics for Grammatical Error Correction shows that reference-free and LLM-based GEC metrics can be adversarially unreliable. NLI is therefore a backstop signal, not a correctness oracle.
3. Recent GEC work increasingly evaluates edits rather than only sentence-level similarity. This supports testing a local window in parallel with whole-sentence NLI.

## Research implication

The experiment should falsify two competing risks: whole-sentence NLI may be too insensitive to one-token grammar errors, while local-window NLI may be too sensitive and create excessive Arabic REVIEW burden. The contradiction-only policy tests whether a narrower veto captures clear semantic conflicts while preserving more safe edits.