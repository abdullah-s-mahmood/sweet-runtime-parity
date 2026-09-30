# MP-SEF PROTECTED INVARIANTS CONTRACT V1

Date: 2026-09-30
Status: FROZEN BEFORE FEASIBILITY MEASUREMENT

## 1. Purpose

This contract defines hard protected-span rules for MP-SEF candidate construction and feasibility accounting.

Protection is applied before candidate actions enter the legal action space.

## 2. Principle

A proposal may touch protected content and be logged.

A legal executable action may not silently alter protected content unless a separately frozen rule explicitly authorizes that exact transformation class.

For the first feasibility cycle there are no such automatic protected-span exceptions.

## 3. Protected categories

At minimum:

### NUMBERS
- Arabic digits;
- Arabic-Indic digits;
- decimal values;
- percentages;
- ranges;
- signed numbers;
- scientific notation where detectable.

### UNITS
- explicit measurement units attached to numeric or scientific values;
- common SI symbols;
- recognized unit tokens.

### CITATIONS
- bracketed numeric citations;
- author-year citation structures where deterministically recognizable;
- DOI strings;
- citation anchors.

### EQUATIONS / FORMULAS
- math spans;
- equation-like symbolic sequences;
- LaTeX-like math fragments;
- OMML placeholders where present in later document pipelines.

### URL / EMAIL
- URLs;
- email addresses;
- URI-like identifiers.

### CODE / LATIN TECHNICAL FRAGMENTS
- code-like tokens;
- identifiers;
- variable names;
- version strings;
- paths;
- mixed Latin technical spans where deterministic protection applies.

### DOCUMENT STRUCTURE MARKERS
- placeholders representing figures;
- tables;
- equations;
- comments;
- bookmarks;
- fields;
- document-control tokens.

### HIGH-CONFIDENCE NAMED ENTITIES
Only where a deterministic high-confidence protection detector has been frozen before measurement.

If no such detector is frozen for the first cycle, this category is reported as NOT ACTIVE rather than approximated post hoc.

## 4. Span map

For each source record create a protected-span map before proposer output is scored.

Each protected span records:
- protected_id;
- category;
- source_start;
- source_end;
- exact source text;
- detector/version;
- confidence if detector exposes one;
- hard_protected=true/false.

Only hard_protected=true spans block legal actions in the first cycle.

## 5. Raw proposal touch

A raw proposer hypothesis/bundle receives:
- protected_touch=false; or
- protected_touch=true plus protected IDs/categories.

A touch is not automatically counted as an execution failure because proposers are allowed to generate unsafe suggestions for diagnostic accounting.

## 6. Legal action veto

Any bundle that would alter a hard-protected span is:
- executable=false;
- failure_reason=PROTECTED_BLOCKED;
- excluded from legal action space A_s(P).

If one component of an inseparable bundle violates protection, the entire bundle is blocked.

Gold/reference may not be used to retain only the non-protected part.

## 7. Character preservation

For any legal action:
every hard-protected span must remain byte/text equivalent under the source-preserving normalization contract used by the pipeline.

Whitespace movement around a protected span is permitted only if:
- it does not alter the protected span itself;
- document/source offset remapping remains reversible;
- no semantic attachment to number/unit/citation is broken.

For the first sentence-level feasibility cycle, uncertain cases are blocked rather than normalized permissively.

## 8. Number-unit coupling

A number and an immediately associated protected unit may be treated as a coupled protected structure.

Actions that:
- change number;
- change unit;
- move unit to a different number;
- delete separator required for interpretation;
are blocked.

## 9. Citation integrity

A legal action may not:
- change citation index;
- change DOI;
- delete citation anchor;
- merge citation text into neighboring lexical text;
- create a new citation.

## 10. Mixed-script risk

Arabic correction around Latin/code spans is allowed only if the protected Latin/code characters are preserved exactly.

If alignment cannot prove preservation, block the bundle.

## 11. Metrics

Mandatory:

### protected_touch_proposal_rate
raw unique proposals touching >=1 hard protected span
/
all raw unique proposals

### protected_touch_sentence_rate
sentences with >=1 protected-touch proposal
/
all feasibility sentences

### blocked_bundle_count

### reference_target_blocked_by_protection_count
Reference targets that become unreachable because all achieving legal actions would violate protection.

These targets remain visible in product-level accounting.

They are not silently removed to improve R_joint.

## 12. Structural gate

Unauthorized protected alteration in a legal executable action:
0

Any non-zero event is a construction failure and invalidates the feasibility run.

This gate is separate from candidate recall.

## 13. Proposal vs authorization

A model proposing an unsafe edit does not by itself fail the proposer feasibility experiment.

The architecture fails only if:
- unsafe protected changes enter legal action space;
- accounting hides them;
- or protected policy silently changes after metrics.

Proposal risk is still reported because high rates may make the architecture operationally unattractive.

## 14. Named entities

No generic named-entity protection is assumed unless an exact detector/version and decision rule are frozen.

Until then:
- numbers/units/citations/etc. remain active hard protections;
- named-entity semantic risk is reported later during selector/human-review design;
- no post-result NER rule may be introduced to rescue feasibility metrics.

## 15. Future document pipeline

This contract is sentence/text-level for the current Arabic correction experiment.

The long-term ACAD_PASS DOCX pipeline must additionally preserve:
- OOXML structure;
- fields;
- comments;
- references;
- OMML;
- bookmarks;
- style/run boundaries where required.

Those requirements are not evaluated by the current QALB feasibility run and cannot be inferred from success here.

## 16. Freeze rule

Protected categories, detectors, and blocking semantics must be hashed/frozen before feasibility metrics.

No protection rule may be weakened after seeing R_joint.
