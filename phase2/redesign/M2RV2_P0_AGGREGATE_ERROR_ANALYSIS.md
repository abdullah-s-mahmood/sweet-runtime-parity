# M2-R v2 P0 — Aggregate Error Analysis

Date: 2026-09-30

## Scope

This analysis uses only the already-opened M2-R v2 P0 development gold and the frozen predictions whose SHA-256 is:

`3117a4b553ca5d9b514c76d7f77bbe8b6df2b14a677f3814a2f09e6f97d65eb4`

No Confirmation, Holdout, or A7'ta reserve is opened.

Important labeling constraint:
the v2 QALB key provides exact expert surfaces, replacements, and M2 operation type (Edit/Split/Merge/Delete/Move), but it does not provide a trustworthy linguistic taxonomy label for every gold edit. Therefore gold misses are analyzed by M2 operation type; Orthography/Morphology/Syntax/Lexical counts below refer to the verifier's own predicted dimension labels, not invented gold labels.

## 1. Clean false positives

CLEAN_QALB_REFERENCE:
- cases: 30
- cases with >=1 mandatory-error claim: 18
- CFPR: 18/30 = 60.00%
- false-positive claims: 24
- mean claims per false-positive clean case: 1.33

Verifier-assigned dimensions among the 24 clean false-positive claims:
- ORTHOGRAPHY: 11
- MORPHOLOGY: 8
- SYNTAX: 4
- LEXICAL: 1

Confidence:
- HIGH: 23/24
- MEDIUM: 1/24

This is a calibration failure: false mandatory-error claims are not being expressed as low-confidence uncertainty.

Recurring false-positive rationale categories include:
- Hamza / Hamzat al-Wasl spelling claims;
- Ya / final-letter spelling claims;
- agreement claims;
- definiteness/idafa claims;
- verb mood claims;
- pronoun and attachment claims.

No case-specific examples are used for P1 design.

## 2. Gold operation recall

Across all error-containing families:

- Edit: 129/409 = 31.54%
- Split: 7/31 = 22.58%
- Merge: 3/30 = 10.00%
- Delete: 0/5 = 0%
- Move: 0/1 = 0%
- Other: 0/1 = 0%

Thus the low GELR is not explained only by rare structural operations. Even ordinary Edit operations are mostly missed.

## 3. Natural QALB completeness behavior

NATURAL_QALB_SOURCE cases: 60.

Per-sentence completeness:
- ALL gold edits found: 3/60 = 5.00%
- SOME gold edits found but at least one missed: 52/60 = 86.67%
- ZERO gold edits found: 5/60 = 8.33%

Averages:
- gold edits per sentence: 7.45
- matched gold edits per sentence: 2.00
- missed gold edits per sentence: 5.45
- verifier mandatory-error claims per sentence: 2.65

The main failure is therefore **incomplete enumeration**, not merely inability to notice that a sentence contains an error.

## 4. Strict near-complete residual family

QALB_ALL_BUT_ONE_STRICT:
- hit: 19/30
- recall: 63.33%
- miss: 11/30

This remains far below the preregistered 90% safety target.

## 5. Predicted-dimension diagnostics

Among prediction claims on error-containing contexts that exactly matched a gold error surface:
- ORTHOGRAPHY: 135
- MORPHOLOGY: 3
- LEXICAL: 1
- SYNTAX: 0

Among prediction claims on error-containing contexts that did not match a gold surface:
- ORTHOGRAPHY: 38
- MORPHOLOGY: 11
- SYNTAX: 7

Interpretation:
the current prompt behaves primarily as an orthographic detector. Its own syntax/morphology labels contribute disproportionately to unsupported claims, while exact gold matches are overwhelmingly orthographic.

Because QALB v2 gold does not carry a complete linguistic taxonomy for every edit, this is a diagnostic about the verifier's behavior, not a gold-standard dimension recall table.

## 6. Confidence calibration

Claim precision by verifier confidence:
- HIGH: 136/213 = 63.85%
- MEDIUM: 3/6 = 50.00%

HIGH confidence does not imply high correctness under this task.

## 7. Root-cause synthesis

P0 has two simultaneous and opposing defects:

1. **Under-enumeration**
   - CRR is relatively high because the model often finds at least one error.
   - GELR is low because most additional expert edits are missed.

2. **Over-assertion**
   - CFPR is 60% on fully human-corrected references.
   - 23/24 clean false-positive claims are HIGH confidence.

A simple instruction to “scan harder” risks worsening false positives.
A simple instruction to “be more conservative” risks worsening enumeration.

## 8. Constraint for the single allowed P1

P1 must address both defects structurally, without examples from P0 and without threshold changes.

The aggregate evidence supports a two-stage internal decision structure:
- Stage A: enumerate candidate error spans broadly.
- Stage B: independently classify each proposed span as MANDATORY / OPTIONAL / UNCERTAIN.
- Only MANDATORY spans enter final output.
- Require exact-surface evidence and a concise linguistic rule for each final mandatory claim.
- Add a final second-pass scan specifically for missed independent errors.
- Treat stylistic/register/literary normalization as non-mandatory by default unless a clear correctness rule is violated.

This is a candidate design direction only. P1 is not frozen by this file.

## 9. Current status

- M2-R v2 P0: FAIL.
- Scientific understanding: IMPROVED.
- Deployment readiness: UNCHANGED / REVIEW-first.
- Confirmation: CLOSED.
- Holdout: CLOSED.
- A7'ta reserve: CLOSED.
- One structural P1 remains allowed.
- No P2 is allowed after P1.
