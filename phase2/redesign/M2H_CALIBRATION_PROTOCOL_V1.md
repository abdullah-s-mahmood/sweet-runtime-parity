# M2-H Calibration Protocol v1

Date: 2026-09-30
Status: FROZEN BEFORE COMPONENT EXECUTION
Scope: CALIBRATION only

## 1. Purpose

This protocol operationalizes H2/H3/H4 calibration without opening INTERNAL_EVALUATION or STRESS_DIAGNOSTIC text and without changing any preregistered M2-H success gate.

No component output has been inspected before this protocol was frozen.

## 2. Fixed CALIBRATION evidence

CALIBRATION:
- 6,888 cases
- 6,867 changed source/reference cases
- 21 unchanged cases
- UID SHA256:
  3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9

Operation inventory:
- Edit: 59,875
- Add_before: 34,816
- Split: 3,776
- Merge: 6,629
- Delete: 2,427
- Move: 132
- Add_after: 12
- Other: 599

## 3. H4 boundary-validation gold definition

The M2 operation name alone is NOT the H4 gold definition.

H4 is restricted to word-boundary changes where the normalized Arabic character sequence is unchanged and only whitespace boundaries differ.

### 3.1 Pure-space positive

A Split or Merge edit is H4-eligible only when:

1. removing whitespace from source surface and reference replacement produces the exact same character sequence;
2. no character is inserted, deleted, substituted, reordered, or normalized away;
3. the edit is not in a protected context excluded by the frozen H4 rules;
4. the exact source span and reference replacement are recoverable.

Observed CALIBRATION inventory before component execution:

- Split total: 3,776
- pure-space Split: 2,633
- non-pure Split: 1,143

- Merge total: 6,629
- pure-space Merge: 5,505
- non-pure Merge: 1,124

Sentence-level availability:

- sentences with at least one pure-space Split: 1,732
- sentences with at least one pure-space Merge: 1,936
- sentences with at least one pure-space Split or Merge: 3,347
- sentences with both: 321
- sentences with neither: 3,049

### 3.2 Mandatory adversarial negatives

The 1,143 non-pure Split edits and 1,124 non-pure Merge edits are NOT counted as H4 positives.

They are mandatory adversarial negatives for unsupported "boundary-only" approval because they require at least one non-whitespace change.

### 3.3 General negatives

Sentences with no pure-space Split/Merge are available as general false-positive controls.

### 3.4 H4 calibration use

Because H4 is deterministic and the CALIBRATION set is already development-only, the full eligible CALIBRATION pool may be used to freeze:
- rule activation;
- evidence-family requirements;
- abstention conditions;
- contradiction handling.

No INTERNAL_EVALUATION text or result may be used for any of those choices.

The preregistered H4 evaluation gates remain unchanged:
- recall >= 70% if n >= 20 per operation;
- precision >= 90%;
- hard stop if precision < 80%.

## 4. H2 orthographic calibration

H2 targets high-precision deterministic orthographic validation.

ARETA enrichment may nominate orthographic strata, but ARETA labels are not independent gold.

Primary orthographic nomination codes:
- OA, OC, OD, OG, OH, OM, ON, OR, OS, OT, OW.

Promotion of an H2 rule requires:
1. exact source/reference edit evidence;
2. membership in a frozen deterministic surface rule family;
3. no protected-invariant violation;
4. no reliance on an ARETA label alone.

The preregistered H2 objective remains:
- safe precision >= 98%;
- zero protected-invariant violations;
- coverage reported separately.

## 5. H3 morphology-aware calibration

H3 uses CAMeL morphology as evidence, not as sentence-level truth.

ARETA may nominate morphology strata:
- MI: word inflection
- MT: verb tense

Other syntax classes that can correlate with morphology, such as gender, number, definiteness, or case, must be reported separately and must not silently expand the primary H3 subset.

A source/reference pair may enter the primary H3 development-proxy subset only if:
1. ARETA nominates MI or MT;
2. the source/reference edit is recoverable;
3. the reference is the QALB expert correction;
4. CAMeL analyses can be recorded for both sides.

Important limitation:
- ARETA is an automatic classifier;
- CAMeL is also used by H3;
- therefore this subset is a DEVELOPMENT PROXY, not independent human morphology gold.

The preregistered H3 target is retained, but results on this proxy subset must be labeled accordingly:
- recall >= 70% if n >= 20;
- false-positive case rate <= 10%.

Publication-grade morphology claims still require independent confirmation.

## 6. ARETA role

ARETA is permitted only for:
- stratification;
- candidate selection;
- diagnostic taxonomy;
- coverage/error analysis.

ARETA is prohibited from being treated as:
- independent human gold;
- a sole approval condition;
- a sole rejection condition;
- a substitute for QALB source/reference evidence.

## 7. Frozen ARETA source

Use the enhanced ARETA implementation inside:

Repository:
CAMeL-Lab/arabic-gec

Revision:
8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

This is the same frozen upstream revision already used for the QALB14 source in this project.

Run ARETA in an isolated environment if dependency compatibility requires it.

## 8. Calibration output contract

Each calibration decision must preserve:
- case_id
- UID
- exact source span
- reference replacement
- operation
- component
- component version/hash
- evidence families
- ARETA diagnostic labels if available
- CAMeL analyses if applicable
- disposition
- abstention/rejection reason

No hidden state may cross component boundaries.

## 9. Forbidden actions before freeze

Before component parameters/rules are frozen:
- do not materialize INTERNAL_EVALUATION text;
- do not materialize STRESS_DIAGNOSTIC text;
- do not inspect their gold;
- do not weaken preregistered gates;
- do not add rules inspired by INTERNAL_EVALUATION;
- do not use A7'ta reserve, QALB15 TEST, Confirmation, Holdout, or reserved Nahw evidence.

## 10. Next authorized execution

1. run ARETA enrichment on CALIBRATION only;
2. derive H2/H3 diagnostic strata;
3. run H4 deterministic calibration on the full CALIBRATION boundary pool;
4. freeze component rules/thresholds;
5. only then create predictions for INTERNAL_EVALUATION while its gold remains hidden.
