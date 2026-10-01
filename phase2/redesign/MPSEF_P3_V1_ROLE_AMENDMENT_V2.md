# MP-SEF P3_V1 ROLE AMENDMENT V2

Date: 2026-10-01
Status: FROZEN PRE-STAGE1 SOURCE-ONLY AMENDMENT
Closes: Independent Review MAJOR M01
Amends: MPSEF_P3_V1_SWEET_PNX_CASCADE_SPEC.md

## 1. Role

P3_V1 is an OPTIONAL punctuation/full-correction cascade extension of P1.

It is NOT:
- an independent architecture family;
- a second independent vote beside P1;
- mandatory for the primary candidate set;
- evidence that punctuation changes improve the NoPnx primary target.

Family relationship:
- P1 family: SWEET
- P3 family: SWEET
- P3 subtype: CASCADE_EXTENSION
- ancestry: P1 -> Pnx

For conservative support counting:
P1 + P3 count as at most ONE SWEET-family source of support.

## 2. Stage-A source

Preferred Stage-A input for P3:
the exact frozen/registered P1 output for the same UID.

Required:
`P3_stageA_input_sha256 == P1_output_sha256`

Do not rerun P1 merely to generate Stage A if the exact registered P1 output is available.

If a rerun is technically unavoidable:
- use the exact frozen P1 model/runtime path;
- run preregistered parity;
- record that packet parity does not prove full-population equality;
- do not replace historical P1 evidence.

## 3. P3 final protection

Protection is evaluated on:

`ORIGINAL_SOURCE -> FINAL_P3_OUTPUT`

Passing P1 protection does NOT confer protection acceptance to P3.

The Pnx stage can introduce punctuation or mixed changes that alter:
- citations;
- units;
- percentages;
- decimal notation;
- technical tokens;
- boundary/linkage.

Therefore P3 receives a fresh whole-output protection proof.

## 4. P3 change-domain diagnostics

For each UID classify Stage-B contribution relative to P1 parent output and relative to original source.

Required categories:

- NO_CHANGE_FROM_P1
- PUNCTUATION_ONLY_FROM_P1
- BOUNDARY_ONLY_FROM_P1
- LEXICAL_ONLY_FROM_P1
- MIXED_FROM_P1
- PROTECTED_REGION_TOUCH_FROM_P1
- ALIGNMENT_AMBIGUOUS
- ALIGNMENT_FAILED

Separately classify original-source -> final-P3 output using the same source-only component taxonomy.

Whitespace changes that alter token boundaries MUST NOT be discarded as punctuation.

## 5. Retention rationale

P3 may be retained after source-only stages only for one or more explicit reasons:

- unique legal full outputs not produced by the non-cascade candidates;
- product need for punctuation/full correction;
- a distinct legal failure profile useful to the candidate pool;
- acceptable cost for a reproducible optional path.

P3 must NOT be retained merely because:
- its output differs from P1;
- ACL 2025 reports strong benchmark performance;
- it changes punctuation frequently.

## 6. Independence interpretation

For any future consensus/diagnostic support:

- P1 and P3 share one SWEET family vote ceiling;
- P1/P3 agreement is intra-family agreement;
- P2_V2 vs SWEET is cross-family support;
- identical P1/P3 outputs dedup to one action with both provenances.

No numeric independence weight is introduced in this version.

## 7. Product-target boundary

If the active product mode is NoPnx-only and P3's legal marginal contribution is entirely punctuation-only, P3 may be deferred without being declared linguistically poor.

If the product mode requires full correction including punctuation, P3 remains a justified optional candidate subject to source-only gates.

## 8. Required source-only diagnostics

Report:

- number and percentage of P3 outputs identical to P1;
- P3 unique legal outputs;
- P3-only legal outputs after dedup;
- cases where P3 turns a legal P1 output into protected-blocked;
- cases where P3 is legal and P1 is blocked;
- Stage-B domain distribution;
- original->P3 domain distribution;
- runtime overhead of Pnx stage;
- family-level dedup effect.

These are NOT correctness metrics.

## 9. Stage 1 eligibility

Before Stage 1:

- this amendment frozen;
- parent-output identity rule implemented;
- P3 Stage-A/P1 parity or direct parent reuse proven;
- whole-output protection on original->P3 implemented;
- change-domain classifier self-tests pass.

## 10. Scientific boundary

No P3 correctness, usefulness, recall, precision, or R_joint claim is allowed from source-only diagnostics.
