# MP-SEF Target Scope and Family Map V2

Date: 2026-10-01
Status: FROZEN FOR CORRECTED V2 PREFLIGHT

This document supersedes the V1 family-map rule for the corrected scorer cycle only.
It does not rebuild or alter historical H1 gold/evidence.

## Punctuation set

Punctuation/symbol characters are:
- ASCII punctuation from Python `string.punctuation`;
- Unicode characters whose general category begins with `P` or `S`.

The literal HTML spelling `&amp;` is NOT expanded into a character set.
Therefore letters such as `a`, `m`, and `p` are never punctuation merely because they occur in that string.

## Scope classification

For a frozen target `original -> correction`:

- `PUNCTUATION_ONLY`:
  punctuation/symbol content changes, while lexical content and lexical token boundaries do not.
- `MIXED_PUNCT_LINGUISTIC`:
  punctuation/symbol content changes and lexical content or lexical token boundaries also change.
- `LINGUISTIC`:
  the change is not punctuation-only.

Whitespace is not discarded when deciding whether a word-boundary repair is linguistic.
Thus:
- `m -> a!` is MIXED_PUNCT_LINGUISTIC;
- `ياولد -> يا ولد،` is MIXED_PUNCT_LINGUISTIC;
- `ياولد -> يا ولد` is LINGUISTIC;
- `مرحبا -> مرحبا،` is PUNCTUATION_ONLY.

## Family classification

Families remain:
`INSERT, DELETE, SPLIT, MERGE, SUBSTITUTE, COMPLEX`.

For SPLIT/MERGE detection, punctuation is removed token-wise while token boundaries remain observable:
- one lexical token to multiple lexical tokens with identical concatenation => SPLIT;
- multiple lexical tokens to one lexical token with identical concatenation => MERGE.

## Measurement consequence

Only PUNCTUATION_ONLY targets are excluded from the primary NoPnx denominator.
Mixed punctuation+linguistic targets remain in the denominator.

A target-build defect, multiple reference alternatives, a no-op target, or invalid offsets invalidates the measurement build; none is silently repaired.
