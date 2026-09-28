# Phase 2 — Lexical Continuity Diagnostic: Research Start

Date: 2026-09-29

## Rationale

CAMeL Tools provides a finite-state morphological analyzer that can enumerate Arabic lexical and morphological analyses, including lemma/lexeme, POS and root information. Using the analyzer with no backoff allows us to distinguish lexical evidence from noun_prop fallback guesses.

Arabic text-editing GEC research supports interpretable edit-level processing and ensembles, but the previous cross-corpus gate showed agreement is not a correctness guarantee.

COCOGEC 2026 shows that GEC validity can flip under context changes, so lexical continuity is used only as a **negative Strict-Fidelity signal**, not a positive correctness oracle.

## Hypothesis

Many dangerous agreed edits are not pure inflectional/orthographic repairs; they move to a different lexeme or derivational form.

A generic lexeme-disjoint veto may therefore catch semantic-risk edits more orthogonally than post-edit GED.

Expected limitation:
some legitimate misspellings can accidentally form another valid Arabic lexeme. Sending those to REVIEW is acceptable under Strict Fidelity, but excessive supported loss would make the rule commercially impractical.
