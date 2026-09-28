# Phase 2 — Lexical Continuity Contradiction Diagnostic

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE RESULT INSPECTION

## Purpose

The previous post-edit GED / no-morph diagnostic failed:
- wrong capture: 1/8 = 12.5%
- supported retention: 136/144 = 94.44%
- residual supported precision: 90.67%

The remaining cross-model agreement failures are disproportionately lexical, derivational, complement/preposition, and semantic.

This diagnostic asks whether **lexical continuity** supplies more orthogonal negative evidence under ACAD_PASS Strict Fidelity.

This is a diagnostic on the already consumed 159-event QALB15 TRAIN agreement stream. It cannot authorize production or Phase 3.

## Frozen input

Use the frozen gold-blind agreement artifact from workflow run 36484171517:
- primary population: EXACT_SINGLE_SUB_AGREEMENT == ACCEPT
- 159 events
- artifact digest and feature SHA already recorded by the previous protocol.

No QALB TEST.
No QALB corrected text in runtime.
No human labels in runtime.

## Morphological analyzer

Use CAMeL Tools calima-msa-r13 analysis mode with **no backoff**.

For each one-token source/candidate pair:
- enumerate all source analyses;
- enumerate all candidate analyses;
- extract normalized lemma/lexeme identities using CAMeL `strip_lex` + dediacritization;
- extract root and POS sets;
- never persist the lexical strings, only counts/hashes/boolean relations.

## Frozen diagnostic features

### CANDIDATE_UNANALYZABLE
Candidate has zero lexical analyses.

### SOURCE_AND_CANDIDATE_ANALYZABLE
Both source and candidate have >=1 lexical analysis.

### LEXEME_OVERLAP
At least one normalized source lexeme equals one normalized candidate lexeme.

### ROOT_OVERLAP
At least one non-empty source root equals one candidate root.

### POS_OVERLAP
At least one POS is shared.

## Frozen policies

### LEXEME_DISJOINT_VETO
REVIEW if:
- candidate is unanalyzable; OR
- both source and candidate are analyzable and LEXEME_OVERLAP is false.

Otherwise KEEP_ACCEPT.

Rationale:
when two valid surface forms belong to disjoint lexical entries, automatic proofreading risks changing meaning. Under Strict Fidelity this should be reviewed even if two GEC generators agree.

### LEXEME_AND_ROOT_DISJOINT_VETO
REVIEW if:
- candidate is unanalyzable; OR
- both are analyzable, LEXEME_OVERLAP is false, and ROOT_OVERLAP is false.

This is a weaker comparator that allows same-root derivational changes to remain accepted.

### CANDIDATE_UNANALYZABLE_ONLY
REVIEW only if candidate has no lexical analysis.
Comparator only.

## Evaluation order

1. Download/verify frozen agreement artifact.
2. Materialize morphology-only lexical-continuity features.
3. Hash/freeze runtime features.
4. Only then load prior hash-only manual adjudication.
5. Measure:
   - wrong capture out of 8;
   - total unsafe capture out of 15;
   - supported retention out of 144;
   - residual KEEP_ACCEPT precision.

## Pre-registered interpretation

- STRONG_SIGNAL:
  - wrong capture >= 75% (>=6/8), and
  - supported retention >= 90% (>=130/144).

- PROMISING_SIGNAL:
  - wrong capture >= 50% (>=4/8), and
  - supported retention >= 90%.

- WEAK_OR_UNHELPFUL:
  - wrong capture <50%, or
  - supported retention <90%.

No result from this consumed slice can be promoted directly.
A promising rule must be frozen and tested unchanged on a fresh disjoint population.

## Prohibitions

Do not:
- use word-specific lists;
- use gold/corrected QALB text in runtime;
- tune edit-distance thresholds;
- inspect lexical strings to craft exceptions;
- read QALB TEST;
- start Phase 3;
- create a final sealed benchmark.
