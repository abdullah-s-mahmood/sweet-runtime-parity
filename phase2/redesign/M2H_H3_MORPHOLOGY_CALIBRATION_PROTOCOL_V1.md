# M2-H H3 Morphology-Aware CALIBRATION Protocol v1

Date: 2026-09-30
Status: **FROZEN BEFORE H3 MORPHOLOGY METRICS**
Scope: **CALIBRATION only**
Role: **DEVELOPMENT PROXY**

## 1. Purpose

H3 evaluates whether a candidate edit has conservative, independent morphology support.

H3 is not a generic grammar checker and does not use H1 confidence as evidence.

ARETA `MI` / `MT` is used only to nominate a morphology-relevant development stratum. ARETA's corrected token is not used to approve an H1 candidate.

## 2. Research basis and caveats

ARETA defines:
- `MI`: word inflection
- `MT`: verb tense

ARETA is an automatic diagnostic tagger, not human gold.

CAMeL morphology analysis is out-of-context and may return many analyses for the same undiacritized surface form. Therefore:
- analyzability alone is insufficient;
- existence of one compatible pair alone is insufficient;
- contradictory compatible analyses force abstention.

The analyzer's documented default normalization is retained because H3 targets morphology rather than orthographic seat/form distinctions.

## 3. Frozen resources

CAMeL Tools git revision:
`be79ca9fc493f0df795375a7255bafef246a802d`

Morphology database:
`calima-msa-r13`

Frozen morphology.db SHA256:
`195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70`

ARETA CALIBRATION enrichment artifact:
- artifact id: `11074295904`
- SHA256: `e29cd674e8606eff4d685ef59fa3e11b51b6a769425a29dcb4042884100dde1c`

H1 candidate artifact:
- artifact id: `11088155733`
- SHA256: `907065fd1a3e156456cec7a31f86facff689896b4d8d39b50cbc852ffd7cc8d3`

## 4. Candidate nomination without circularity

A candidate is H3-nominated only when:

1. an ARETA token annotation contains `MI` or `MT` in its codes;
2. that annotation's **raw/source side** can be deterministically mapped to the original source sentence;
3. the H1 candidate's original-source token span exactly equals the mapped ARETA raw span;
4. the candidate replacement is taken from H1, not from ARETA `correct`;
5. candidate extraction invariants pass.

ARETA `correct` is never used to decide whether the H1 candidate is morphologically supported.

## 5. Frozen ARETA-raw → source span mapping

For every sentence, process ARETA token annotations in order.

For each annotation:
- begin searching at the end cursor of the previous mapped annotation;
- first attempt exact substring matching of `raw`;
- if exact matching fails, allow only whitespace-flexible matching in which every non-whitespace character remains identical and one-or-more whitespace characters may replace a raw whitespace run;
- choose the earliest match after the cursor;
- map the matched character interval to the exact overlapping original whitespace-token interval;
- advance the cursor to the match end;
- if no valid mapping exists, mark the annotation `UNMAPPED`.

Skipped source material is allowed because ARETA alignment can omit source tokens deleted by the reference.

No fuzzy character substitution, normalization, or semantic matching is permitted in this mapping.

An H1 candidate must match the mapped source token interval exactly; overlap alone is insufficient.

## 6. Morphological analysis filter

Analyze source surface and H1 candidate replacement with:
- `Analyzer(calima-msa-r13)`
- backoff: `NONE`
- documented default normalization.

Retain only analyses whose:
- `source == "lex"`;
- `lex` is non-empty;
- `pos` is non-empty.

Both source surface and H1 candidate replacement must each contain exactly one whitespace-delimited token. Multi-token surfaces are `REVIEW_OUTSIDE_INFLECTION` and are not passed to the word-level analyzer.\n\nBoth sides must retain at least one analysis.

## 7. Stable lexical identity

A compatible pair requires:
- exact `lex` equality;
- exact `pos` equality.

No broad POS-class relaxation is permitted in v1.

Lemma-changing / derivational replacements are not H3 positives.

## 8. Frozen inflectional feature sets

Features examined when present:

`asp, cas, form_gen, form_num, gen, mod, num, per, rat, stt, vox`

Clitic features are held fixed:

`prc3, prc2, prc1, prc0, enc0`

If any clitic feature differs in a same-lemma/same-POS pair, that pair is not an allowed H3 inflectional support path.

### MI

For an `MI`-only nomination:
- at least one examined inflectional feature must differ;
- `asp` must not be the sole distinguishing feature;
- all grammatical differences must lie within the examined inflectional feature set;
- clitic features must remain unchanged.

### MT

For any nomination containing `MT`:
- `asp` must differ explicitly;
- all other grammatical differences must lie within the examined inflectional feature set;
- clitic features must remain unchanged.

## 9. Ambiguity / contradiction rule

Enumerate all source/candidate analysis pairs with exact same `lex` and `pos`.

For each such pair compute:
- changed inflectional feature names and values;
- changed clitic features;
- whether the path satisfies the applicable MI/MT rule.

H3 gives positive support only if:

1. at least one same-lemma/same-POS pair exists;
2. every same-lemma/same-POS pair that differs morphologically is compatible with the applicable rule;
3. no same-lemma/same-POS pair has an empty grammatical difference while another pair claims a morphology-changing correction;
4. all compatible pairs agree on one **changed-feature-name signature**.

Otherwise disposition is `REVIEW_AMBIGUOUS`.

This deliberately prefers abstention over selecting a convenient analysis.

## 10. H3 disposition

- `SUPPORTED_MORPHOLOGY_PROXY`: all positive-support conditions pass.
- `REVIEW_UNANALYZABLE`: either side lacks retained lexical analyses.
- `REVIEW_NO_STABLE_LEMMA_POS`: no exact shared lex/POS identity.
- `REVIEW_AMBIGUOUS`: contradictory compatible analysis paths.
- `REVIEW_OUTSIDE_INFLECTION`: only derivational, clitic-changing, or otherwise disallowed morphology paths exist.
- `REVIEW_MAPPING`: ARETA raw span cannot be mapped exactly.
- `REVIEW_NO_H1_CANDIDATE`: MI/MT token has no exact-span H1 candidate.

H3 support is evidence for later hybrid fusion; it is not by itself final clean-document approval.

## 11. Development-proxy metrics

Report:

### Stratum/mapping
- MI token annotations;
- MT token annotations;
- MI/MT annotations successfully mapped;
- mapping failures;
- mapped MI/MT annotations with exact-span H1 candidates.

### Candidate-level
- nominated H1 candidates;
- exact-reference-supported nominated candidates;
- reference-unsupported nominated candidates;
- both-sides analyzable;
- shared lex/POS;
- supported morphology proxy;
- abstentions by reason.

### Quality proxy
- **candidate recall** =
  exact-reference-supported nominated candidates receiving H3 support /
  all exact-reference-supported nominated candidates.

- **supported candidate precision proxy** =
  exact-reference-supported H3-supported candidates /
  all H3-supported candidates.

- **false-positive case rate proxy** =
  cases containing at least one H3-supported reference-unsupported candidate /
  all cases containing at least one H3-supported candidate.

Because QALB is single-reference, reference-unsupported is a conservative development false-positive proxy, not proof of linguistic incorrectness.

## 12. Frozen H3 development targets

If the exact-reference-supported nominated denominator is >=20:
- candidate recall >= **70%**

If at least 20 cases receive H3 support:
- false-positive case rate proxy <= **10%**

Both must pass for H3-v1 to be considered a supported morphology-development component.

No threshold weakening after metrics are observed.

## 13. Integrity

Remain unopened:
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST

## 14. Failure handling

If H3-v1 fails either frozen target:
- record the negative result;
- do not tune feature sets or ambiguity rules from the observed failures in this iteration;
- proceed to H4;
- any H3 redesign requires a separately versioned development iteration before internal evaluation.
