# MP-SEF TARGET FAMILY MAP V1

Date: 2026-09-30
Status: **FROZEN BEFORE R_joint MEASUREMENT**

Parent contracts:
- `MPSEF_PRE_UNION_PROTOCOL_V3.md`
- `MPSEF_TARGET_AND_MATCHING_CONTRACT_V1.md`

## 1. Purpose

This file freezes the operation-family mapping used for mandatory family
reporting and proposer-retention diagnostics. It is defined before any
P1+P2 C_F reference-based metric is observed.

The mapping is derived only from the frozen official M2 target tuple:
`(start, end, original, correction)`.

It never uses proposer identity, proposer output, measured recall, or a
post-result rescue rule.

## 2. Punctuation scope

Use the same punctuation/symbol universe frozen by the H1 NoPnx construction:
ASCII punctuation plus Unicode categories P/S.

For a target:
- `PUNCTUATION_ONLY`: the surface change contains punctuation/symbol change,
  but removing punctuation/symbol characters and whitespace leaves the same
  non-punctuation text on source and correction sides.
- `MIXED_PUNCT_LINGUISTIC`: punctuation/symbol content changes AND the
  non-punctuation text also changes.
- `LINGUISTIC`: otherwise.

Primary denominator excludes `PUNCTUATION_ONLY`.
Mixed targets remain complete and in-scope; they are never partially stripped.

The scorer must report all three counts.

## 3. Operation families

The first matching correction alternative is used. The frozen generated
NoPnx M2 is required to contain exactly one correction alternative per target;
otherwise scoring stops as a construction failure.

Given token offsets and whitespace-tokenized surfaces:

### INSERT
- `start == end`
- correction is non-empty.

### DELETE
- `start < end`
- correction is empty.

### SPLIT
- source span contains exactly one source token;
- correction contains more than one whitespace token;
- removing whitespace from source surface and correction gives exactly the
  same character sequence.

### MERGE
- source span contains more than one source token;
- correction contains exactly one whitespace token;
- removing whitespace from source surface and correction gives exactly the
  same character sequence.

### SUBSTITUTE
- non-empty source span and non-empty correction;
- source and correction have the same whitespace-token count;
- not SPLIT or MERGE.

### COMPLEX
All remaining non-noop complete targets, including:
- multi-token replacements with unequal token counts;
- boundary plus lexical/orthographic change;
- composite effects that are not pure SPLIT/MERGE.

No target is dropped because it is COMPLEX.

## 4. Frozen weak-family routes

The preregistered retention routes are evaluated as:
- `INSERT`
- `BOUNDARY = MERGE + SPLIT`

No other family can satisfy the weak-family retention route in this cycle.

## 5. Family R_pair semantics

For family F, use the same whole-hypothesis legal action space as primary
R_joint.

For each sentence, restrict its in-scope gold targets to family F and compute:

`max_y TP_fixed_F(y)`

over legal `KEEP/P1_FINAL/P2_FINAL`.

Then sum over sentences and divide by the number of family-F targets.

This is a family-restricted oracle over the same whole-hypothesis action
space. It is NOT edit-level fusion.

`R_P1(F)` and `R_P2(F)` use KEEP plus the corresponding proposer only.

`R_raw(F)` is target-wise diagnostic union of complete target matches from
raw P1/P2 hypotheses, regardless of protected blocking.

## 6. Family retention gain

For proposer j and weak family F:

`gain_j(F) = R_pair(F) - R_without_j(F)`

The route requires all frozen protocol conditions:
- gain >= 0.05 absolute;
- >=10 additional complete targets;
- additional targets span >=10 distinct document clusters.

The scorer must report all three quantities.

## 7. Additional-target and cluster semantics

For weak-family retention, an `additional complete target` for proposer j is
a family-F target that:

- is completely matched by proposer j's legal whole hypothesis;
- is not completely matched by any legal non-KEEP proposer output in the
  system with proposer j removed;
- remains a complete frozen target; no partial credit or decomposition is
  allowed.

This target-wise diagnostic is used only for the `>=10 additional targets`
and `>=10 document clusters` conditions. It does not replace the
family-restricted whole-hypothesis recall gain.

Distinct-cluster count is computed from the frozen C_F source manifest
`cluster_id` attached to the target's source sentence.

If the proposer hypothesis is protected-blocked or otherwise non-executable,
its target matches do not count as additional legal targets for retention.

## 8. Empty families

Any zero-target family is reported as `N/A` and excluded from macro averages.

## 9. Stop rule

This mapping may not change after any C_F pair metric is observed.
