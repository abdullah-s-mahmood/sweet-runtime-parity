# MP-SEF P3_V1 ROLE AND INDEPENDENCE AMENDMENT V2

Date: 2026-10-01
Status: FROZEN PRE-STAGE1 SOURCE-ONLY AMENDMENT
Closes: Independent Review MAJOR M01
Supersedes for interpretation: role/independence sections of MPSEF_P3_V1_SWEET_PNX_CASCADE_SPEC.md
Does not modify frozen P1.

## 1. P3 role

P3_V1 is OPTIONAL.

It is NOT a mandatory third proposer and NOT an independent architecture family.

Canonical role:

`OPTIONAL_PUNCTUATION_AND_FULL_CORRECTION_EXTENSION_OF_P1_FAMILY`

P3 may be retained only if source-only evidence justifies one or more of:

- product need for punctuation/full-correction output;
- distinct legal whole output beyond P1;
- mixed punctuation+linguistic differences that are operationally relevant;
- acceptable cost/provenance as an optional candidate.

P3 is not retained merely because published benchmark performance is strong.

## 2. Family identity

P1 and P3 share:

`family_id = SWEET_QALB14`

For any future consensus/support accounting:

- P1 + P3 agreement counts as at most ONE family vote;
- P3 does not create a second independent SWEET witness;
- proposer-level counts may still be reported descriptively.

## 3. Stage A source

Preferred Stage A input for P3 is the exact frozen P1 whole output for the same UID.

Required binding:

- UID equal;
- source_sha256 equal;
- P1 proposer/version identity equal;
- P1 output_sha256 recorded as P3 parent_output_sha256.

If frozen P1 output cannot be reused and Stage A must be rerun:

- the rerun is a new explicit P3 implementation trace;
- parity must be tested;
- packet parity does not imply full-population equality;
- the record must not falsely claim it consumed the historical frozen P1 artifact.

## 4. Stage B delta decomposition

P3 must report two distinct comparisons:

### A. Stage-B-only delta
`P1_final -> P3_final`

### B. Full source delta
`source -> P3_final`

For Stage-B-only delta, classify source-only components into:

- PUNCTUATION_ONLY
- MIXED_PUNCT_LINGUISTIC
- NON_PUNCTUATION
- WORD_BOUNDARY_AFFECTING
- PROTECTED_REGION_TOUCH
- ALIGNMENT_AMBIGUOUS/FAILED

Whitespace that changes token/word boundaries is NOT discarded as punctuation-only.

## 5. P3 protection decision

P3 final legality is evaluated on:

`original source -> P3 final output`

P3 MUST NOT inherit P1 legalizer acceptance.

Even if:
- P1 is legal, and
- the Pnx pass looks punctuation-only,

the final P3 output must pass the full current source-only protection/legalizer contract independently.

## 6. Retention diagnostics

Before Stage 2, report at minimum:

- UIDs where P3 == P1 exactly;
- UIDs where P3 differs only by punctuation;
- UIDs where P3 differs by mixed punctuation+linguistic edits;
- UIDs where P3 introduces non-punctuation changes relative to P1;
- UIDs where P3 is legal and distinct from P1;
- UIDs where P3 is blocked while P1 is legal;
- UIDs where P3 is legal while P1 is blocked;
- unique legal whole outputs added by P3 after literal dedup;
- runtime overhead;
- protected-touch reason distribution.

No correctness inference is permitted.

## 7. Product-scope flag

The registry MUST include a scope field:

`correction_scope = NOPNX_CORE | FULL_WITH_PUNCTUATION`

P1:
`NOPNX_CORE`

P3:
`FULL_WITH_PUNCTUATION`

Future evaluation protocols must not silently mix these scopes.

If the product/evaluation objective for a run excludes punctuation-only changes, P3 may still be retained as a whole candidate, but its role and metric interpretation must explicitly respect the target-scope contract.

## 8. No independence inflation

Forbidden claims:

- "three independent models" for P1/P2/P3;
- "two independent SWEET votes" from P1 and P3;
- using P1/P3 agreement to satisfy a two-family consensus threshold.

Allowed description:

- P1 and P3 are two related proposer variants in one SWEET family;
- P2_V2 is heterogeneous relative to the SWEET family.

## 9. Stage 1 requirement

Stage 1 may test P3 only after:

- parent-output identity rules are implemented;
- P1/P3 family relation is encoded in the registry;
- Stage-B delta classification is implemented;
- final source->P3 protection is enforced.

## 10. Scientific boundary

This amendment changes P3's architectural interpretation, not any historical result.

It does not establish P3's linguistic utility.
