# Phase 2 — Lexical Continuity Diagnostic: End Review

Date: 2026-09-29

## Decision

**WORSENED / WEAK_OR_UNHELPFUL as a promotion veto.**

The diagnostic completed successfully on the frozen 159-event exact-agreement stream.

## Results

### LEXEME_DISJOINT_VETO
- REVIEW: 2
- KEEP_ACCEPT: 157
- supported retained: 142/144 = 98.61%
- wrong captured: 0/8 = 0%
- unsafe captured: 0/15 = 0%
- residual supported precision: 142/157 = 90.45%

### LEXEME_AND_ROOT_DISJOINT_VETO
- REVIEW: 1
- KEEP_ACCEPT: 158
- supported retained: 143/144 = 99.31%
- wrong captured: 0/8 = 0%
- unsafe captured: 0/15 = 0%
- residual supported precision: 143/158 = 90.51%

### CANDIDATE_UNANALYZABLE_ONLY
- REVIEW: 0
- wrong captured: 0/8
- supported retained: 144/144

## Pre-registered decision

PROMISING_SIGNAL required:
- >=4/8 wrong captured;
- >=90% supported retention.

All three policies are **WEAK_OR_UNHELPFUL**.

## Meaning

The eight wrong cross-model agreements are not primarily caused by obvious out-of-lexicon candidate words or simple lemma discontinuity.

CAMeL's ambiguity means a wrong contextual choice can still have a valid lexical/morphological analysis, and source/candidate lexeme sets can overlap even when the intended sense or grammatical role is wrong.

Therefore:
- dictionary membership is evidence, not correctness;
- lemma/root overlap is evidence, not semantic equivalence;
- analyzer ambiguity prevents this layer from isolating the dangerous minority.

## Combined conclusion from the last two diagnostics

Post-edit GED:
- wrong capture 12.5%;
- supported retention 94.44%.

Lexeme-disjoint:
- wrong capture 0%;
- supported retention 98.61%.

Neither provides the required orthogonality.

Do not tune either on the consumed slice.

## Architecture implication

The next work should not be "one more universal verifier".

We need **selective acceptance by edit-risk family**, and contextual/parser evidence only for families that actually require it.

This is consistent with ACAD_PASS Strict Fidelity:
- safe-looking low-risk corrections may eventually auto-apply after disjoint validation;
- lexical, derivational, complement, agreement, or ambiguous edits remain REVIEW unless stronger context proof exists.

## Next step

**Phase 2 — Cross-Model Agreement Risk-Family Audit**

Exploratory only on the consumed 159 events:
1. assign every frozen edit a target-independent transformation family;
2. report supported/wrong/partial/unnecessary by family;
3. identify candidate low-risk families using pre-registered minimum support and zero/near-zero known unsafe events;
4. do not promote from this audit;
5. freeze candidate families and validate them unchanged on a fresh disjoint external slice.

Parser-assisted evidence is reserved for families where contextual grammar is the blocker, rather than applied indiscriminately to all edits.

No Phase 3.
No QALB TEST.
No final sealed benchmark.
