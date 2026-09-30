# M2-H Component Calibration Freeze v1

Date: 2026-09-30  
Status: **FROZEN BEFORE H2/H3/H4 CALIBRATION EXECUTION**  
Scope: **CALIBRATION only**

## 1. Purpose

This file freezes the component search space, evidence contracts, abstention rules, and reporting requirements before executing H2/H3/H4 calibration.

No `INTERNAL_EVALUATION` or `STRESS_DIAGNOSTIC` text may be opened while selecting or modifying these rules.

The previously preregistered component gates remain unchanged.

## 2. Evidence hierarchy

Evidence priority:

1. exact QALB source/reference edit evidence;
2. deterministic surface/structure predicates;
3. component-specific independent evidence;
4. ARETA diagnostic stratum only.

ARETA is never an approval oracle.

A rule family not listed in this file cannot be activated after calibration merely because it improves metrics. Adding a new family requires a new explicitly versioned development iteration before any internal evaluation.

## 3. H2 — deterministic orthographic validator

### 3.1 Frozen candidate-family search space

H2 calibration may examine only these conservative surface families:

- `HAMZA_ALIF_SEAT`: substitutions among Arabic hamza/alif seat forms where string length and all non-target characters are unchanged.
- `ALIF_MAQSURA_YA`: local `ى ↔ ي` substitution only.
- `TA_MARBUTA_HA`: local `ة ↔ ه` substitution only.
- `ALIF_VARIANT`: local alif-form normalization not involving word-boundary change.
- `SINGLE_ARABIC_LETTER_ORTHOGRAPHIC`: exactly one Arabic-letter substitution with no insertion/deletion/reordering; this family is diagnostic by default and may activate only if the >=98% precision gate is met independently.
- `DIACRITIC_ONLY`: combining-mark-only difference; **REVIEW/ABSTAIN by default**, not auto-accept, because case/mood/meaning may change.
- `TATWEEL_ONLY`: tatweel-only difference; diagnostic only until invariant checks prove safe.

Explicitly excluded from H2:
- whitespace Split/Merge;
- multi-character lexical replacement;
- inflectional suffix/prefix changes;
- punctuation-only changes;
- edits crossing protected spans;
- any edit requiring semantic or syntactic interpretation.

### 3.2 Promotion rule

A family is eligible for automatic `SUPPORTED_MANDATORY` only if, on CALIBRATION:

- exact family predicate is satisfied;
- QALB edit is recoverable;
- safe precision >= 98%;
- zero protected-invariant violations;
- no contradictory deterministic veto;
- coverage is reported separately.

Anything below the precision gate remains `REVIEW` or `REJECTED`; the threshold may not be lowered.

## 4. H3 — morphology-aware validator

Primary development-proxy stratum remains ARETA `MI` or `MT`.

### 4.1 Frozen morphology evidence contract

A candidate may receive positive H3 support only if:

1. source and reference surfaces are both recoverable;
2. both sides have at least one CAMeL morphological analysis;
3. there exists at least one compatible source/reference analysis pairing with stable lexical identity:
   - same lemma where available;
   - compatible POS class;
4. the difference is explainable through an allowed inflectional feature change rather than lexical replacement;
5. no protected invariant is touched;
6. contradictory analyses cause abstention rather than forced acceptance.

For `MT`, tense/aspect-related feature change must be explicitly represented in the analysis pair.

For `MI`, the analysis difference must remain within inflectional morphology; lemma-changing or derivational changes are not promoted by H3.

### 4.2 Ambiguity rule

CAMeL analyzability or existence of a compatible analysis is **not sufficient** by itself.

If multiple plausible analyses support incompatible grammatical conclusions, disposition is `REVIEW`.

### 4.3 Reporting

Report as **DEVELOPMENT PROXY**:
- eligible cases;
- analyzable both sides;
- compatible-pair cases;
- supported cases;
- abstentions;
- false-positive case rate;
- recall against the proxy subset.

Frozen target:
- recall >=70% if n>=20;
- false-positive case rate <=10%.

## 5. H4 — structural Split/Merge validator

Gold remains the previously frozen pure-whitespace contract.

### 5.1 Mandatory structural gate

Before any evidence fusion:

- removing whitespace from source surface and reference replacement must yield the exact same character sequence;
- no Unicode character insertion/deletion/substitution/reordering is permitted;
- protected contexts are excluded;
- exact span mapping must succeed.

Failure of this gate means the case is not an H4 positive.

### 5.2 Frozen evidence families

After structural legality, H4 may use only these evidence families:

- `MORPH_SEGMENTATION`: CAMeL segmentation/morphology supports the proposed token boundary.
- `CLITIC_LEGALITY`: deterministic closed Arabic proclitic/enclitic legality rules support the boundary.
- `DEVELOPMENT_PATTERN_SUPPORT`: the exact boundary pattern has non-trivial support in CALIBRATION and is not contradicted by adversarial non-pure Split/Merge cases.

At least **two distinct evidence families** must support automatic approval.

H1 agreement may be recorded diagnostically but is not counted toward the two-family minimum.

### 5.3 Negative controls

Mandatory:
- all 1,143 non-pure Split edits;
- all 1,124 non-pure Merge edits;
- general no-boundary cases sampled deterministically from CALIBRATION.

No non-pure Split/Merge may be counted as a positive.

### 5.4 Frozen targets

Per operation, if n>=20:
- recall >=70%;
- precision >=90%;
- hard stop if precision <80%.

## 6. Common abstention and invariant rules

All H2/H3/H4 components must abstain on:
- failed exact span mapping;
- protected-span overlap;
- conflicting component evidence;
- unresolved `UNK` dependence;
- transformations outside the frozen family/search space;
- evidence requiring use of `INTERNAL_EVALUATION` or any reserved dataset.

`UNK` is not interpreted as clean and not interpreted as automatic error. It is an explicit uncertainty state.

## 7. Frozen calibration outputs

Each component output must contain:
- `case_id`
- `uid`
- exact source span
- reference replacement
- component
- rule/evidence family IDs
- ARETA diagnostic codes
- CAMeL evidence if applicable
- structural predicates
- disposition
- abstention/rejection reason
- invariant-check result

Summaries must report numerator and denominator, not only percentages.

## 8. Post-calibration freeze rule

After H2/H3/H4 calibration metrics are observed:

- eligible families may be enabled only under the gates above;
- no new rule family may be invented from errors observed in the same calibration execution without versioning a new development iteration;
- after final component activation/thresholds are committed and hashed, only then may `INTERNAL_EVALUATION` predictions be generated.

## 9. Current data-integrity basis

ARETA artifact validation passed:
- rows: 6,888
- unique UIDs: 6,888
- unique case IDs: 6,888
- UID SHA256 matches frozen CALIBRATION:
  `3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9`
- structural errors: 0
- pip-freeze SHA256 matches:
  `56b9a3964f149eeab9db64ff118287b23a63bf05eb52c6599e9b4af859a12704`

## 10. Exact next execution

Implement and run CALIBRATION-only component calibration in this order:

1. H2 family classification and precision/coverage table;
2. H3 MI/MT morphology proxy evaluation;
3. H4 pure-boundary calibration with mandatory adversarial negatives;
4. freeze enabled/disabled families and thresholds;
5. update `RESUME_HERE.md`;
6. only then consider opening `INTERNAL_EVALUATION`.
