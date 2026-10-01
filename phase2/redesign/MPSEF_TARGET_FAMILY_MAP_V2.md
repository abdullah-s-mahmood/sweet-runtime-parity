# MP-SEF TARGET FAMILY MAP V2

Date: 2026-10-01
Status: **FROZEN FOR CORRECTED V2 CYCLE BEFORE SECOND PREFLIGHT**

Supersedes for the corrected V2 cycle:
`MPSEF_TARGET_FAMILY_MAP_V1.md`

V1 remains historical and is not deleted.

Parent:
- `MPSEF_TARGET_AND_MATCHING_CONTRACT_V1.md`
- `MPSEF_TARGET_AND_MATCHING_CONTRACT_V2_AMENDMENT.md`

## 1. Punctuation universe

Punctuation/symbol characters are exactly:

- ASCII punctuation characters; UNION
- Unicode characters whose general category begins with `P` or `S`.

Literal letters in an HTML-like sequence such as `&amp;` are NOT punctuation
merely because they occur inside the sequence:
- `&` and `;` may be punctuation;
- `a`, `m`, and `p` remain lexical characters.

No proposer output or gold result may change this universe after measurement.

## 2. Target scope

For frozen target original O and correction C compute:

1. `punctuation_sequence`: characters in the frozen punctuation universe;
2. `lexical_character_sequence`: remove punctuation/symbol and whitespace;
3. `lexical_token_sequence`: whitespace-tokenize, remove punctuation/symbol
   characters inside each token, and drop empty tokens.

Then:

- `punctuation_changed` iff punctuation sequences differ.
- `lexical_changed` iff lexical character sequences differ.
- `boundary_changed` iff lexical token sequences differ.
- `linguistic_changed = lexical_changed OR boundary_changed`.

Classification:

- `PUNCTUATION_ONLY` iff punctuation_changed AND NOT linguistic_changed.
- `MIXED_PUNCT_LINGUISTIC` iff punctuation_changed AND linguistic_changed.
- `LINGUISTIC` otherwise.

Consequences:

- `m -> a!` is mixed/linguistic, never punctuation-only.
- `ياولد -> يا ولد،` is mixed and remains in the primary denominator.
- pure addition/removal/change of punctuation with identical lexical characters
  and identical lexical token boundaries is punctuation-only.

Primary denominator excludes only `PUNCTUATION_ONLY`.

Mixed targets remain complete and are never stripped into a more favorable
sub-target.

## 3. Target construction integrity

Each target must have exactly one frozen correction alternative.

If:
- multiple alternatives exist;
- the target is an exact no-op;
- offsets cannot be reconciled to the frozen source;

construction fails closed.

No target is silently dropped for construction convenience.

## 4. Families

Family mapping uses lexical token sequences from Section 2.

### INSERT
- `start == end`;
- correction non-empty.

### DELETE
- `start < end`;
- correction empty.

### SPLIT
- non-empty source span;
- one lexical source token;
- more than one lexical correction token;
- concatenated lexical source and correction characters are identical.

Punctuation may also change; such a target is then
`MIXED_PUNCT_LINGUISTIC`, but family remains SPLIT.

### MERGE
- non-empty source span;
- more than one lexical source token;
- one lexical correction token;
- concatenated lexical source and correction characters are identical.

Punctuation may also change; such a target remains complete and family MERGE.

### SUBSTITUTE
- source/correction non-empty;
- equal lexical token count;
- not SPLIT/MERGE.

### COMPLEX
All remaining complete in-scope targets.

## 5. Whole-hypothesis family semantics

For family F:
- use the same frozen legal A_primary as R_joint;
- evaluate each whole legal action;
- for each sentence choose the single whole action with greatest complete
  family-F target credit;
- never union P1 and P2 target hits.

If any otherwise legal action cannot be scored:
- family value is reported as a proven `[L,U]` interval;
- no scoring failure becomes known zero;
- exact is reported only when `L==U`.

## 6. Diagnostic R_raw(F)

R_raw(F) reads only the frozen source-only diagnostic-component artifact.

Gold-aware M2 evaluation alignment is NOT a source for R_raw components.

If diagnostic attribution is ambiguous:
- lower bound gets no credit from the ambiguous evidence;
- upper bound may include the complete target if reachability is possible;
- ambiguity never creates an executable action.

## 7. Weak-family routes

Frozen routes:
- INSERT
- BOUNDARY = SPLIT + MERGE

For proposer j, all three preregistered conditions remain required:

1. family gain >= 0.05;
2. >=10 additional complete targets;
3. those additional targets span >=10 document clusters.

Under uncertainty report lower/upper values.

Route status:
- PASS only if all three lower bounds satisfy the requirements;
- FAIL if at least one requirement cannot be met even at its upper bound;
- otherwise INCONCLUSIVE.

No weak route authorizes selector training automatically.

## 8. Empty families and macro

A zero-target family is `N/A`.

Macro R_pair averages only non-empty frozen families.

Under uncertainty report macro lower/upper and exact only if equal.

## 9. Freeze

This V2 map governs only the corrected V2 cycle.

It may not be changed after the Second Premeasurement Preflight code commit is
frozen unless that preflight is invalidated and rerun from a new code commit.
It may never be changed after observing corrected-cycle metrics to rescue a
result.
