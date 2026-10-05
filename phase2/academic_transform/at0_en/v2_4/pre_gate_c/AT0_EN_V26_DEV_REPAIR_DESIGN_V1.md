# ACAD_PASS — AT0-EN V2.6-DEV Repair Design V1

Date: 2026-10-05
Status: DESIGN ONLY / NOT AUTHORIZED FOR IMPLEMENTATION

Derived from:
`FACTPICO_V25_FAILURE_ANALYSIS_REPORT_V1.md`

FactPICO V2.5 remains frozen and failed the preregistered utility gates.
This design must not overwrite, correct, or reinterpret those results.

## 1. Design objective

Create the smallest new-version repair that can reduce spurious uncertainty and representation collapse while preserving the existing fail-closed safety behavior.

Proposed development version:
`AT0-EN V2.6-DEV`

Repair package:
`REPRESENTATION_AND_GROUPING_REPAIR_V1`

The design deliberately does NOT start by relaxing the final decision rule.

## 2. Frozen components that remain unchanged initially

During the first development repair:
- V2.5 FactPICO predictions/results remain immutable;
- V5 FactPICO thresholds/gold/population remain immutable historical evidence;
- safety-first ordering remains:
  critical bad -> REJECT;
  unresolved uncertainty -> REVIEW;
  only sufficiently resolved preserved cases -> PASS;
- no result-adaptive conversion of REVIEW to PASS;
- no FactPICO-driven threshold tuning;
- no Arabic work;
- no Gate C reopening.

## 3. Proposed minimal repair package

### R1 — Text boundary / markup normalization

Goal:
prevent representation corruption before assertion extraction.

Design requirements:
- abbreviation-aware sentence segmentation;
- preserve decimal and p-value syntax;
- handle common biomedical abbreviations such as i.e., e.g., etc. without orphan spans;
- normalize HTML/XML escaping and nonsemantic sentence tags before assertion extraction;
- preserve exact normalized-to-original span provenance;
- preserve section headings as metadata, not standalone scientific assertions unless semantically claim-bearing.

Evidence basis:
- 48 frozen records contain <=3-character source evidence fragments;
- recurrent `i` / `e` fragments are present;
- 116 records contain escaped/tag-like candidate evidence fragments;
- current splitter protects decimals but not general abbreviations.

### R2 — Local assertion confidence instead of group-wide contamination

Goal:
one ambiguous local assertion must not automatically contaminate unrelated matched assertions.

Current issue:
`mapping_status()` checks the set of confidence states for the entire alignment group.
If one member is non-CERTAIN, the whole mapping becomes UNCERTAIN before semantic comparison.

Design:
- preserve confidence per assertion;
- align assertions first;
- propagate uncertainty only through explicitly dependent claims/bindings;
- do not promote unknown evidence to CERTAIN;
- unmatched uncertain critical source claims must remain REVIEW or REJECT according to explicit semantics;
- no blanket uncertainty suppression.

Safety invariant:
no uncertain critical proposition may become PASS merely because neighboring assertions match.

### R3 — Exact partial alignment for unequal counts

Goal:
remove the current prefix-match + append-all-leftovers-to-last-group behavior.

Proposed mechanism:
- retain the exact scalable Hungarian machinery for matched assertion pairs;
- extend the assignment matrix with explicit deterministic dummy/unmatched nodes;
- represent unmatched source assertions as explicit omission candidates;
- represent unmatched candidate assertions as explicit new-information candidates;
- avoid giant heterogeneous merge groups by default;
- allow split/merge equivalence only when separately supported by deterministic compositional evidence.

Evidence basis:
- 339/345 frozen records contain non-1:1 groups;
- 331/345 have more source assertions than candidate assertions;
- median source:candidate assertion-count ratio is 4.83;
- maximum observed source group contains 95 assertions;
- current code explicitly appends all leftover assertions to the final group.

Safety invariant:
partial matching must never discard unmatched critical content.

### R4 — Independent predicate/extraction coverage extension, conditional

This is NOT automatically part of the first implementation.

Static inspection indicates the current explicit parser inventory is much narrower than ordinary biomedical RCT prose.

After R1-R3 development tests, if uncertainty remains dominated by unsupported proposition forms, an independent development-only extraction extension may be proposed.

Constraints:
- build from non-FactPICO development material;
- generic RCT/scientific syntax, not memorized FactPICO cases;
- preserve provenance and unresolved states;
- separate population/intervention/comparator/outcome ownership where explicit;
- do not infer absent medical facts.

R4 requires a separate internal design freeze if activated.

## 4. Relation layer

FactPICO V2.5 produced zero relation alignment rows across all 345 cases.

Therefore relation handling is NOT the first repair target.

Do not delete the relation architecture.
Instead:
- leave it unchanged during R1-R3;
- add independent development fixtures that prove whether generic RCT ownership/direction relations require extension;
- only extend relation extraction if independent evidence demonstrates need.

## 5. Independent development test plan

FactPICO is prohibited as a development acceptance set for V2.6.

Proposed independent development suite:
`AT0_EN_V26_REPRESENTATION_DEV_V1`

Material:
- controlled synthetic scientific statements;
- non-FactPICO open-access RCT/scientific text selected before repair implementation;
- no text copied from the frozen FactPICO diagnostic set.

Proposed fixture families:

A. SEGMENTATION / NORMALIZATION — 60 fixtures
- abbreviations;
- decimals and p-values;
- section headings;
- escaped markup/tags;
- parenthetical biomedical terms.

B. SAFE PARAPHRASE PRESERVATION — 60 pairs
- same population/intervention/comparator/outcome;
- surface rewording;
- split/merge propositions;
- explicit modality preserved.

C. CRITICAL ERROR DETECTION — 80 pairs
- population swap;
- intervention/comparator swap;
- outcome omission/change;
- quantity/unit change;
- baseline reversal;
- polarity/causality change;
- modality strengthening.

D. UNEQUAL-COUNT ALIGNMENT — 60 pairs
- one-to-many;
- many-to-one;
- unrelated extra sentence;
- omitted critical sentence;
- mixed critical/noncritical extras.

Total proposed development fixtures:
`260`

## 6. Proposed development acceptance criteria

These are proposals for the next independent review, not yet authorized thresholds.

Hard invariants:
- INVALID = 0 on valid fixtures;
- no critical-error fixture may PASS_CANDIDATE;
- no unmatched critical source assertion may disappear from the audit trail;
- no orphan markup/abbreviation fragment should become a scientific assertion;
- exact deterministic reproducibility across fresh processes.

Utility proposals:
- SAFE PARAPHRASE PASS_CANDIDATE >= 80%;
- CRITICAL ERROR REJECT >= 90%;
- SAFE REVIEW <= 20%;
- every unequal-count fixture must expose explicit matched/unmatched accounting.

The independent reviewer may tighten these before implementation.

## 7. Future external validation boundary

After any V2.6 development repair:
1. pass authorized development tests;
2. freeze runtime/code/config/hashes;
3. do NOT use FactPICO as a prospective independent test again;
4. preregister an untouched external validation protocol on independent material;
5. only then execute external validation.

FactPICO may remain:
- historical benchmark evidence;
- diagnostic material;
- non-prospective regression evidence only if explicitly labeled as exposed.

## 8. Repair success claim boundary

Even if V2.6 passes development:
it does NOT erase the V2.5 FactPICO failure.

Allowed future statement:
`V2.6 addressed evidence-localized representation/alignment weaknesses and passed independent development controls.`

External safety/utility claims require a new untouched validation checkpoint.

## 9. STOP

No implementation is authorized by this document.

Required next checkpoint:
`FAILURE_ANALYSIS_AND_REPAIR_DESIGN_REVIEW`
