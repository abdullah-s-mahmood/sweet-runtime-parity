# ACAD_PASS — H1 FactPICO Hard-Gold Contract V4

Date: 2026-10-04
Status: FROZEN FOR INDEPENDENT REVIEW / NO V2.4 EXECUTION

Supersedes H1 hard-gold role from PLABA.
PLABA remains diagnostic/authentic-transformation evidence.

Primary resource:
FactPICO, ACL 2024.

Raw archive SHA-256:
`ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`

Primary numeric gold:
`data/all_evaluations.csv`

Primary gold SHA-256:
`1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd`

## 1. H1 construct

Hard H1 scope is deliberately narrow:

`CRITICAL RCT-ELEMENT FIDELITY / PRESERVATION`

H1-S:
critical scientific support/factuality.

H1-C:
preservation of critical RCT descriptors/findings.

FactPICO does not establish exhaustive preservation of every sentence or detail.

## 2. Prediction context

Frozen V2.4 receives:

`source_text = full FactPICO RCT abstract`

`candidate_text = full generated plain-language summary`

This matches the human annotation context and requires no hidden semantic context channel.

## 3. Prediction universe

All 345 released FactPICO summary records are predicted exactly once.

Each source has 3 candidates:
- GPT-4
- LLAMA-2
- ALPACA

Unique source clusters:
`115`

Source cluster key:
`SHA256(exact Abstract)`

Record ID:
`SHA256("FACTPICO_REC_V1\0" + source_sha256 + "\0" + model_type + "\0" + candidate_sha256)`

No raw text normalization beyond file decoding.

Prediction artifact integrity:
- exactly 345 frozen record IDs;
- one output per ID;
- missing ID = INVALID_H1_EVALUATION;
- duplicate ID = INVALID_H1_EVALUATION;
- unknown/extra ID = INVALID_H1_EVALUATION.

## 4. Human-gold fields

Hard-gold candidate fields:

- Population
- Intervention
- Comparator
- Outcome
- Results

Human PICO semantics:
- 4 = mentioned and accurate
- 3 = somewhat inaccurate/vague
- 2 = severe inaccuracies and/or missing critical descriptors
- 1 = missing
- N/A = not meaningfully applicable

Released `0` is treated as the N/A encoding for Intervention/Comparator where observed.

Evidence Inference semantics:
- 4 = accurate
- 3 = vague/slightly inaccurate
- 2 = inaccurate
- 1 = not mentioned

`Results` in the release is an aggregate over 1–5 evidence-inference spans and, for double-annotated cases, may also aggregate multiple human observations.

## 5. Fields NOT used as hard gold

Not hard gold:
- Avg. PICO-R
- holistic score
- automatic factuality metrics
- LLM rationales/evaluations
- contradiction files
- Added Information correctness
- exhaustive-outcome field

Reasons:
- Avg. PICO-R is derived;
- holistic score semantics are not frozen for H1;
- automatic metrics are not human gold;
- contradiction annotations are sparse by publication design;
- factual added explanations may be externally true but unsupported by the source, which conflicts with source-bounded V2.4 semantics;
- exhaustive outcomes explicitly include non-critical omission policy.

Added Information remains diagnostic/audit evidence only.

## 6. N/A source-cluster rule

The paper states N/A may occur for examples that are not meaningfully standard RCTs.

Observed:
- 3 source clusters
- 9 summaries

contain at least one PICO N/A/0.

For construct purity, all 3 source clusters are:

`N_A_SOURCE_DIAGNOSTIC`

and excluded from hard H1 gate denominators.

Hard-gate source pool:
`112 source clusters / 336 summaries`

No record is removed from the prediction universe.

## 7. Annotation-provenance treatment

PICO double-annotated subset:
- 25 source abstracts
- 75 summaries
- released PICO scores may contain half-step averages.

Other records:
- integer PICO scores.

For double-annotated PICO averages:
- 4.0 is safe-strict because both integer ratings must be 4;
- <=1.5 is error-strict because both integer ratings must fall in {1,2};
- 2.0 is NOT made hard error because it may represent either (2,2) or disagreement such as (1,3);
- 2.5, 3.0, 3.5 remain non-hard.

For non-double PICO records:
- 4 = safe on that axis;
- <=2 = strong human error on that axis;
- 3 = intermediate.

This avoids inventing raw rater labels from an average.

## 8. Source-bounded safe-control compatibility

FactPICO permits explanatory added information and separately assesses whether it is factual.

Frozen V2.4 is source-bounded and cannot automatically certify external explanations merely because they are true outside the abstract.

Therefore a record can enter the primary positive safe-control stratum only when:

1. all four PICO fields = 4;
2. Results = 4;
3. no Added Information span is identified for that exact source/candidate pair;
4. its source cluster is not among the 15 source clusters containing an auxiliary Added Information candidate whose identity is corrupted/unresolved;
5. its source is not N/A-excluded.

This is intentionally conservative.

## 9. Proposed hard classes

### SAFE_STRICT_CONTROL

Definition:
criteria in Section 8.

Frozen proposal count:
- records: `34`
- source clusters: `33`

Model distribution:
- ALPACA: `33`
- GPT-4: `1`
- LLAMA-2: `0`

Important:
this is a LIMITED SAFE CONTROL, not representative evidence of broad transformation diversity.

FactPICO itself reports Alpaca as more extractive and more factual.

### ERROR_STRICT

Eligible non-N/A source plus either:

A. PICO error trigger:
- non-double record: any applicable PICO <=2;
- double-annotated PICO record: any applicable PICO <=1.5;

OR

B. Results error trigger:
`Results <= 2`

Frozen proposal count:
- records: `172`
- source clusters: `91`

Model distribution:
- ALPACA: 42
- GPT-4: 53
- LLAMA-2: 77

### INTERMEDIATE

Hard-eligible non-N/A records not assigned SAFE_STRICT_CONTROL or ERROR_STRICT.

Count:
- records: `130`
- source clusters represented: `79`

No hard expected ACAD_PASS outcome.

### N_A_SOURCE_DIAGNOSTIC

- records: `9`
- source clusters: `3`

No hard expected outcome.

Counts sum:
`34 + 172 + 130 + 9 = 345`

## 10. Frozen eligibility-manifest proposal

A deterministic metadata-only eligibility manifest was generated.

Rows:
`345`

SHA-256:
`72ece44c2d23b8c6ce667f5f1ff0856fb28900a412a0b14ed192ce329b8a9d91`

It contains no raw source/candidate text.

It records:
- record ID
- source hash
- candidate hash
- model type
- annotation-provenance class
- N/A-source flag
- exact added-information-span flag
- unresolved-added-information-source flag
- proposed V4 gold class
- PICO-error trigger
- Results-error trigger

This manifest is PROVISIONAL until independent review accepts V4.

## 11. Hard safety gate

Population:
all `172 ERROR_STRICT` records.

Eligible source clusters:
`91`

Unsafe event:
`PASS_CANDIDATE`

Hard requirement:
`ERROR_STRICT -> PASS_CANDIDATE = 0`

Any event:
`FAIL_H1_SAFETY`

REVIEW:
safe non-acceptance, not decisive rejection.

INVALID_VERIFICATION:
non-success and remains visible.

If zero unsafe-PASS source clusters occur across 91 eligible clusters, the simple one-sided 95% exact upper bound is approximately:

`3.2384%`

This is benchmark-specific, not a production-risk guarantee.

## 12. Negative utility gate

Population:
ERROR_STRICT.

Success:
`REJECT`

Require both:
- pair-micro REJECT >=75%;
- source-cluster macro REJECT >=75%.

REVIEW and INVALID do not count as decisive rejection.

## 13. Limited positive safe-control gate

Population:
SAFE_STRICT_CONTROL.

Success:
`PASS_CANDIDATE`

Require both:
- pair-micro PASS >=75%;
- source-cluster macro PASS >=75%.

Because only 34 records / 33 clusters qualify and 33/34 are ALPACA, this gate supports only:

`LIMITED SOURCE-BOUNDED SAFE-CONTROL USABILITY`

It must NOT be cited as broad authentic-transformation acceptance.

Strong-adoption target >=90% remains separate and cannot be established from this stratum alone.

## 14. Statistical contract

Primary cluster:
`exact Abstract source cluster`

Utility:
- whole-source cluster bootstrap
- 10,000 resamples
- seed `20261004`
- percentile 95% CI
- report pair-micro and source-macro

Safety:
- unsafe pair count
- unsafe source-cluster event count
- exact one-sided 95% upper bound when zero events

No summary, element, result span, model, or human judgment is treated as an independent study.

## 15. Intermediate diagnostics

For INTERMEDIATE and N_A_SOURCE_DIAGNOSTIC report:
- PASS_CANDIDATE
- REJECT
- REVIEW
- INVALID_VERIFICATION

Stratify by:
- model_type
- source cluster
- PICO field
- Results value
- annotation provenance

No hard gate.

## 16. Added Information policy

Added Information is NOT hard mapped in V4.

Reason:
FactPICO asks whether additions are factually correct, including explanatory material not necessarily supported by the source abstract.

V2.4 is source-bounded.

Therefore:
- external factuality cannot be granted by the adapter;
- using Added Information correctness as hard PASS would add external-world semantics unavailable to V2.4;
- using all additions as hard REJECT would contradict FactPICO's valid plain-language elaboration construct.

Allowed:
diagnostic cross-tab only.

## 17. Prediction/gold separation

Before prediction:
1. freeze 345 record IDs;
2. create input manifest with record ID + exact full abstract + exact full summary only;
3. exclude all human labels and class flags from inference artifact;
4. hash input manifest;
5. run frozen V2.4 once;
6. hash predictions;
7. only then join to gold/eligibility manifest;
8. score under accepted V4.

Public gold remains known/public.
This is procedural separation, not secret holdout independence.

## 18. Anti-degeneracy

PASS-all:
fails hard safety.

REJECT-all:
fails limited safe-control utility.

REVIEW-all:
fails both utility gates.

INVALID-all:
fails both utility gates and completeness.

## 19. Claim boundary

A future V4 H1 pass may support only:

“Frozen AT0-EN V2.4 met preregistered research-progression criteria for source-bounded critical RCT-element fidelity on FactPICO, including zero automatic acceptance of the frozen strong-error stratum and limited safe-control acceptance on fully expert-positive, no-added-information controls.”

It does NOT establish:
- broad transformation utility;
- universal academic fidelity;
- exhaustive preservation of every fact;
- production readiness;
- external medical truth verification;
- <1% deployment risk.

PLABA remains complementary authentic-transformation diagnostic evidence.

## 20. Material issues requiring independent review

Independent review is required before implementation on exactly these points:

1. Is excluding all 3 N/A source clusters methodologically preferable to field-wise N/A omission?
2. Is the double-annotated PICO strict-error cutoff <=1.5 appropriately conservative?
3. Is `Results <=2` a defensible hard error despite Results being an aggregate over multiple findings/annotations?
4. Is the source-bounded SAFE_STRICT_CONTROL rule valid, especially exclusion of all Added Information spans?
5. Is a 34-record/33-source safe-control gate useful enough to remain a hard progression criterion despite severe ALPACA skew?
6. Are 75% pair-micro + source-macro thresholds still defensible for these narrowed strata?

## 21. Current authorization

Contract:
`FROZEN FOR INDEPENDENT REVIEW`

AUTHORIZED:
- independent methodological review only.

NOT AUTHORIZED:
- adapter implementation;
- FactPICO V2.4 prediction;
- H1 scoring;
- V2.4 modification;
- threshold changes after prediction;
- original custom Gate C opening;
- new-human recruitment;
- Arabic-track work.

## 22. Exact next checkpoint

`INDEPENDENT REVIEW OF FACTPICO H1 CONTRACT V4`
