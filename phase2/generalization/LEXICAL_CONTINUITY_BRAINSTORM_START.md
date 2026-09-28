# Phase 2 — Lexical Continuity Diagnostic: Brainstorm Start

Date: 2026-09-29

## Competing hypotheses

1. **Lexeme-disjoint is high-value**
   - catches semantic drift and wrong lexical substitutions;
   - preserves same-lemma spelling/inflection fixes.

2. **Lexeme-disjoint is too conservative**
   - Arabic spelling errors may map between two valid lexemes;
   - analyzer ambiguity may create false overlap or false disjointness.

3. **Root overlap is too permissive**
   - wrong derivational forms often share a root;
   - same-root does not imply same meaning or grammatical role.

Therefore both lexeme-only and lexeme+root policies are measured.

## If this fails

Do not tune analyzer thresholds.
Proceed to parser-assisted contextual contradiction:
- controller/subject agreement;
- dependency role changes;
- preposition/complement compatibility;
- parse stability.

Parser output remains a veto/evidence source, never an acceptance oracle.
