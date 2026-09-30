# M2-H H4 Structural Boundary CALIBRATION Protocol v1

Date: 2026-09-30
Status: **FROZEN BEFORE H4 METRICS**
Scope: **CALIBRATION only**

## 1. Construct

H4 validates Arabic whitespace-boundary changes only.

A positive H4 transformation must preserve the exact non-whitespace Unicode character sequence:

`remove_whitespace(source_surface) == remove_whitespace(replacement)`

No character insertion, deletion, substitution, or reordering is permitted.

Therefore:
- pure QALB Split/Merge edits are positive calibration targets;
- all non-pure QALB Split/Merge edits are mandatory adversarial negatives.

## 2. Frozen populations

CALIBRATION gold:
- Split total: 3,776
- pure Split: 2,633
- non-pure Split adversarial negatives: 1,143
- Merge total: 6,629
- pure Merge: 5,505
- non-pure Merge adversarial negatives: 1,124

H1 boundary candidate stream is evaluated independently for conservative precision:
- H1 `PURE_SPLIT`: 1,920 candidates
- H1 `PURE_MERGE`: 3,792 candidates

H1 agreement/confidence is diagnostic only and is not evidence.

## 3. Mandatory structural gate

A proposal reaches linguistic evidence only if:
- operation is Split or Merge;
- source/replacement are non-empty;
- exact non-whitespace character preservation passes;
- Split has exactly one source token and >=2 replacement tokens;
- Merge has >=2 source tokens and exactly one replacement token;
- exact original-source span exists;
- extraction invariants pass when the proposal originates from H1.

Failure means `REJECT_STRUCTURAL`.

## 4. Evidence family A — MORPH_SEGMENTATION

Analyze the joined token with frozen CALIMA-MSA:
- database: `calima-msa-r13`
- CAMeL Tools git SHA:
  `be79ca9fc493f0df795375a7255bafef246a802d`
- morphology.db SHA256:
  `195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70`
- backoff: `NONE`

Use retained lexical analyses only (`source == lex`).

Inspect only tokenization fields:
- `d3tok`
- `atbtok`

For comparison only, apply a frozen boundary-normalization function to both proposed segments and analyzer tokenization:
- remove Arabic diacritics;
- remove tatweel;
- map `إ أ آ ٱ → ا`;
- map `ى → ي`;
- map `ة → ه`;
- remove literal `+` markers from tokenizer pieces;
- split analyzer tokenization only on underscore.

This normalization is used only to compare **boundary locations**, never to relax the exact structural gate.

A tokenization observation is comparable only if concatenating its normalized pieces equals concatenating the normalized proposed segments.

`MORPH_SEGMENTATION = SUPPORT` only if:
- at least 2 comparable observations exist; and
- >=80% of comparable observations exactly match the proposed segmentation.

Otherwise this family is `NO_SUPPORT`.

Analyzer exceptions cause abstention, never support.

## 5. Evidence family B — CLITIC_LEGALITY

This is a deliberately narrow deterministic orthographic rule family.

### Merge support

For exactly two source tokens, support attachment when the first token is exactly one of:

`و, ف, ب, ك, ل, س`

These are frozen attachment-required/simple proclitic forms for this v1 test.

### Split support

For exactly two replacement tokens, support separation when the first resulting token is exactly one of:

`يا, ها`

This deliberately omits ambiguous particles such as `ما`.

No suffix/enclitic rule is enabled in v1.

No match means `NO_SUPPORT`, not rejection.

## 6. Evidence family C — DEVELOPMENT_PATTERN_SUPPORT

This is empirical CALIBRATION evidence, independent of H1.

For a two-segment boundary define:
- Split atom = first replacement token;
- Merge atom = first source token.

Pattern key:
`(operation, atom)`

Build counts from all QALB CALIBRATION Split/Merge edits:
- pure-boundary supporting cases;
- non-pure adversarial cases.

For a gold edit being evaluated, use **leave-one-case-out** counts so the case cannot support itself.

For a non-gold/H1 proposal, use all CALIBRATION counts.

`DEVELOPMENT_PATTERN_SUPPORT = SUPPORT` only if:
- atom exists;
- at least **5 other pure-positive cases** support the exact pattern;
- **0 non-pure adversarial cases** contradict that pattern.

Otherwise `NO_SUPPORT`.

No threshold is tuned after metrics.

## 7. H4 automatic support rule

After the mandatory structural gate:

`SUPPORTED_BOUNDARY_PROXY`

requires support from at least **2 of the 3** frozen non-H1 evidence families:
- MORPH_SEGMENTATION
- CLITIC_LEGALITY
- DEVELOPMENT_PATTERN_SUPPORT

One or zero supporting families => `REVIEW_BOUNDARY`.

## 8. Evaluation views

### A. Positive recall view

Apply H4 directly to every pure gold Split and pure gold Merge.

Per operation:

`recall = supported pure gold / all pure gold`

Frozen target if n>=20:
**recall >=70%**

### B. H1 candidate-stream precision view

Apply H4 to every H1 `PURE_SPLIT` / `PURE_MERGE` candidate.

Per operation:

`strict_reference_precision_lower_bound = exact-gold-supported accepted H1 candidates / all accepted H1 candidates`

QALB is single-reference; unsupported is a conservative lower-bound proxy.

Frozen target if accepted n>=20:
**precision >=90%**

Hard stop:
**precision <80%**

If accepted n<20, automatic activation for that operation is not supported.

### C. Mandatory non-pure adversarial negatives

Apply the structural gate to:
- all 1,143 non-pure Split edits;
- all 1,124 non-pure Merge edits.

Required:
**0 may reach SUPPORTED_BOUNDARY_PROXY**.

### D. General no-boundary diagnostic controls

Create deterministic CALIBRATION-only controls.

Salt:
`M2H-H4-GENERAL-NEGATIVE-V1-20260930-A`

Merge controls:
- candidate is concatenation of two adjacent source tokens;
- exclude any span that is an exact QALB Merge edit;
- deterministically select up to **1,000** unique proposals by SHA256 ranking.

Split controls:
- choose a source token of Unicode length 4–12;
- deterministic split position is derived from SHA256(case_id, token_index, salt);
- exclude any proposal that exactly matches a QALB Split edit;
- deterministically select up to **1,000** unique proposals.

These controls are diagnostic because QALB single-reference may omit legitimate alternatives.

Report acceptance rate separately; do not use them to redefine rules.

## 9. Operation activation

Split and Merge are activated independently.

An operation is H4-development-supported only if:
- positive recall >=70%;
- H1 candidate-stream accepted n>=20;
- conservative candidate precision >=90%;
- zero accepted non-pure adversarial negatives;
- zero protected/invariant failure among accepted H1 candidates.

No rule/gate modification after metrics.

## 10. Integrity

Remain unopened:
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST

## 11. Failure handling

If Split or Merge fails:
- freeze the result;
- do not tune the clitic inventory, 80% segmentation ratio, pattern support threshold, or evidence count from observed failures;
- any redesign requires a separately versioned development iteration;
- continue to final component-freeze decision.
