# ACAD_PASS — SURUS Token/Punctuation Reconstruction Diagnostic Freeze V3

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

Run:
`37915291868`

Workflow:
`Federation SURUS token reconstruction diagnostic`

Conclusion:
`SUCCESS`

Artifact:
`11609721783`

Artifact digest:
`sha256:901c7691556e57f521c589d123312f1a8f078928aa20bfaa37106a67b9872b80`

Classification:
`READ_ONLY_AGGREGATE_MECHANISM_DIAGNOSTIC / NO_SCIENTIFIC_ATTEMPT_CONSUMED`

No raw text, PMID values, article IDs, protected IDs, scientific metrics, protected benchmark opening, or model fit were emitted.

## 1. Input state

Released annotation rows:
`48,833`

Rows already exact at released Abstract half-open offsets:
`44,643`

Rows under mismatch analysis:
`4,190`

## 2. Fixed token/punctuation reconstruction result

Rows explained by at least one fixed, label-independent punctuation/spacing rule:
`3,060 / 4,190 = 73.0310%`

Rows still unexplained:
`1,130 / 4,190 = 26.9690%`

As a fraction of the full released annotations:
- directly exact rows = 91.4197%;
- additional fixed-spacing-explainable rows = 6.2667%;
- still unexplained rows = 2.3136%.

These percentages are source-mechanics diagnostics, NOT model performance.

## 3. Main fixed-rule evidence

Direct transformations of the released source slice:
- Unicode punctuation token split preserving punctuation = 2,691 matches;
- ASCII punctuation spaced around = 2,561 matches;
- hyphen/slash/percent spaced = 2,124 matches;
- parentheses spaced = 106 matches.

Because multiple rules can explain the same row, these counts overlap.

First matching rule under the prospectively fixed diagnostic ordering:
- Unicode punctuation token split = 2,691;
- hyphen/slash/percent spacing = 170;
- parentheses spacing = 3;
- remove space after ASCII punctuation = 181;
- remove space around ASCII punctuation = 6;
- remove space before ASCII punctuation = 9.

Total uniquely classified as explained:
`3,060`.

## 4. Mismatch features

Among the 4,190 mismatch rows:
- punctuation present = 3,468;
- hyphen present = 2,132;
- slash present = 344;
- parentheses present = 321;
- percent present = 270.

This strongly supports the hypothesis that a large majority of the released Annotation.Text mismatches arise from punctuation/token reconstruction conventions rather than invalid entity identity.

However, it does NOT establish a complete source coordinate contract.

## 5. Residual unexplained rows

Still unexplained:
`1,130`

By dataset:
- Indomain = 974;
- indication OOD = 98;
- study-type OOD = 58.

By EvalType:
- Train = 890;
- Test = 240.

Residual unexplained rows occur across multiple labels, including:
- LabelID 8 TRIAL = 208;
- LabelID 17 EFFECT = 180;
- LabelID 11 OUTCOME = 141;
- LabelID 10 INCLUSION_CRITERIA = 122;
- LabelID 21 UNIT = 118;
- LabelID 19 RESULT::DETERMINATION = 77;
and others.

Therefore no label-specific deletion/repair is authorized.

## 6. Scientific interpretation

Evidence now supports:

`LARGE_MAJORITY_PUNCTUATION_TOKEN_RECONSTRUCTION_MECHANISM / RESIDUAL_SOURCE_CONTRACT_UNRESOLVED`

It rejects the simplistic interpretation that all 4,190 rows are corrupt.

It also rejects treating the entire release as coordinate-certified because 1,130 positives remain unexplained under the tested fixed rules.

No source repair is authorized.

Do NOT:
- drop the 1,130 rows;
- repair or snap spans;
- infer source text from labels;
- select a rule using downstream model performance;
- train SURUS;
- relax the Amendment V2 requirement that every admitted positive be representable.

## 7. Next authorized operation

Use the source publication's stated BERT-tokenized/BILOU evaluation semantics and the already-pinned ACAD_PASS biomedical tokenizer identity to perform a READ-ONLY aggregate token-alignment diagnostic.

Exact next operation:
`SURUS_PINNED_BIOMEDBERT_TOKEN_ALIGNMENT_DIAGNOSTIC_V4`

The diagnostic must:
- use a single predeclared pinned tokenizer/revision already frozen in ACAD_PASS;
- test TokenStart/TokenEnd conventions without tuning;
- emit aggregate counts only;
- not expose raw record text/IDs;
- not repair any row;
- not perform scientific fitting.

If no deterministic source-compatible contract explains the residual positives, SURUS admission must remain blocked and may require explicit re-review rather than silent exclusion.
