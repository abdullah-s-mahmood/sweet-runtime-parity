# M2-H H2 Deterministic Orthographic Rules v1

Date: 2026-09-30  
Status: **FROZEN BEFORE H2 FAMILY METRICS ARE INSPECTED**  
Scope: **CALIBRATION only**

## 1. Purpose

This file operationalizes the already frozen H2 family search space without adding any new family.

H2 validates only local orthographic candidates. It does not infer sentence semantics and it does not use H1 confidence as safety evidence.

## 2. Common candidate gate

A candidate is H2-eligible only when all of the following hold:

- source span is recoverable and anchored to the original source;
- source surface and candidate replacement are non-empty;
- candidate is not a whitespace Split/Merge;
- candidate does not insert/delete/reorder whitespace;
- candidate does not cross multiple whitespace tokens;
- candidate contains Arabic script;
- candidate is not punctuation-only;
- no designated protected-span overlap is present;
- no unresolved extraction invariant is present.

Anything outside this gate is `OUT_OF_SCOPE`.

## 3. Unicode handling

Predicates operate on NFC-normalized strings.

Arabic combining marks are code points whose Unicode general category is `Mn` or `Mc` and whose character name begins with `ARABIC`.

Tatweel is U+0640.

## 4. Frozen family predicates

Families may overlap. The narrow family IDs are preserved independently; the broad single-letter family does not erase a narrower match.

### 4.1 `HAMZA_ALIF_SEAT`

Exactly one code point differs, all other code points are identical, and both differing characters are members of:

`{ء, أ, إ, ؤ, ئ}`

This family intentionally excludes plain alef `ا`; plain-alef variation is handled by `ALIF_VARIANT`.

### 4.2 `ALIF_MAQSURA_YA`

Exactly one code point differs, all other code points are identical, and the differing pair is exactly:

`ى ↔ ي`

### 4.3 `TA_MARBUTA_HA`

Exactly one code point differs, all other code points are identical, and the differing pair is exactly:

`ة ↔ ه`

### 4.4 `ALIF_VARIANT`

Exactly one code point differs, all other code points are identical, and both differing characters are in:

`{ا, أ, إ, آ, ٱ}`

At least one side must be `ا`, `آ`, or `ٱ`.

This prevents `أ ↔ إ` from being double-counted as the narrow hamza-seat family.

### 4.5 `SINGLE_ARABIC_LETTER_ORTHOGRAPHIC`

Source and replacement have identical code-point length.

Exactly one position differs.

Both differing characters are Arabic letters (`Unicode category L*`, Arabic-script code point), with no insertion, deletion, whitespace change, combining-mark-only change, or reordering.

This is a broad diagnostic family and may activate only under the already frozen >=98% precision gate.

### 4.6 `DIACRITIC_ONLY`

After removing Arabic combining marks from both source and replacement, the remaining strings are exactly identical, while the original strings differ.

Disposition is always `REVIEW` / `ABSTAIN` in v1; this family cannot auto-promote.

### 4.7 `TATWEEL_ONLY`

After removing U+0640 tatweel from both source and replacement, the remaining strings are exactly identical, while the original strings differ.

This family is diagnostic only in v1 and cannot auto-promote.

## 5. Family metric

For each family report:

- total H1 candidates matching the deterministic predicate;
- exact QALB-reference-supported candidates;
- reference-unsupported candidates;
- strict reference precision lower bound:
  `exact_supported / family_candidates`;
- case coverage;
- candidate coverage relative to all H1 candidates.

Because QALB is single-reference, `REFERENCE_UNSUPPORTED` is not automatically a linguistic false positive.

## 6. Promotion rule

A family may be enabled for automatic `SUPPORTED_MANDATORY` only if:

- it is not diagnostic-only;
- strict reference precision lower bound >= 98%;
- zero extraction/invariant violations;
- no deterministic contradiction is present.

If the lower bound is below 98%, the family is not promoted from this calibration result. It is not automatically declared linguistically wrong.

No threshold may be lowered.

## 7. ARETA role

ARETA codes are attached only as diagnostic context.

ARETA never changes the deterministic family predicate and never converts a reference-unsupported candidate into an accepted candidate.

## 8. Reserved data

No `INTERNAL_EVALUATION`, `STRESS_DIAGNOSTIC`, Confirmation, Holdout, A7'ta reserve, reserved Nahw IDs, or QALB15 TEST may be read during H2 calibration.
