# ACAD_PASS — H1 FactPICO Hard-Gold Contract V5

Date: 2026-10-04
Status: FROZEN PRE-IMPLEMENTATION CONTRACT / NO V2.4 EXECUTION

Supersedes:
`H1_FACTPICO_HARD_GOLD_CONTRACT_V4.md`

Reason:
focused independent review accepted V4 with essential changes. V5 incorporates those changes before adapter implementation or prediction.

Primary resource:
FactPICO, ACL 2024.

Raw archive SHA-256:
`ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`

Primary numeric gold:
`data/all_evaluations.csv`

Primary gold SHA-256:
`1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd`

## 1. Scope

Hard H1 claim remains narrow:

`SOURCE-BOUNDED CRITICAL RCT-ELEMENT FIDELITY / PRESERVATION`

FactPICO does not establish exhaustive preservation of every fact in every academic document.

## 2. Prediction universe

All released FactPICO records remain in the prediction universe:

`345 records / 115 source clusters`

Each record:
- exact full RCT abstract as source;
- exact full plain-language summary as candidate.

Source cluster:
`SHA256(exact Abstract)`

Exactly one V2.4 transaction per frozen record ID.

No gold eligibility may alter the 345-record prediction universe.

## 3. Record identity

Record ID:

`SHA256("FACTPICO_REC_V1\0" + source_sha256 + "\0" + model_type + "\0" + candidate_sha256)`

Prediction artifact integrity requires:
- exactly 345 frozen IDs;
- one prediction per ID;
- no missing ID;
- no duplicate ID;
- no extra/unknown ID.

Any violation:
`INVALID_H1_EVALUATION`

## 4. Human fields

Hard-gold source fields:

- Population
- Intervention
- Comparator
- Outcome

Results:
used for SAFE_STRICT_CONTROL only when exactly 4;
otherwise diagnostic.

Not hard gold:
- Avg. PICO-R
- holistic score
- automatic factuality metrics
- LLM evaluator/rationale fields
- contradiction annotations
- Added Information correctness
- exhaustive-outcome aggregate

## 5. Native score semantics

PICO:
- 4 = accurate
- 3 = vague/somewhat inaccurate
- 2 = severe inaccuracies and/or missing critical descriptors
- 1 = missing
- N/A = not meaningfully applicable

Released:
`0 = N/A`
for relevant PICO fields.

Evidence Inference:
- 4 = accurate
- 3 = vague/slightly inaccurate
- 2 = inaccurate
- 1 = not mentioned

## 6. N/A hard-scope exclusion

If any PICO field is N/A/0 for any summary from a source cluster, that entire source cluster is outside the hard H1 gate.

Frozen:
- 3 source clusters
- 9 summaries

Class:
`N_A_SOURCE_DIAGNOSTIC`

These 9 records remain predicted and reported diagnostically.

Hard source pool:
`112 source clusters / 336 summaries`

## 7. Annotation provenance

Known double-PICO source subset:
- 25 source abstracts
- 75 summaries

Released PICO scores may be half-step arithmetic aggregates.

For these double-PICO records:
- hard safe axis = exactly 4;
- hard error axis = <=1.5;
- all other positive values are non-hard.

Rationale:
<=1.5 guarantees both underlying integer ratings lie in {1,2}, provided no N/A/missing value participates.

A released 2.0 is non-hard because it can represent disagreement such as (1,3).

For non-double PICO records:
- hard safe axis = 4;
- hard error axis = <=2;
- 3 = intermediate.

## 8. Results policy

The released `Results` score is a summary-level average over one or more individual Evidence Inference judgments.

The released data do NOT provide the raw numeric human score per finding.

Therefore:

`Results <=2`

is NOT a hard error trigger.

Results is used as follows:

### Positive control
`Results == 4`

is required for SAFE_STRICT_CONTROL.

Because contributing ratings are bounded by 1–4, an arithmetic mean of 4 implies every contributing rating is 4 under the published averaging contract.

### Other values
diagnostic only.

No negative ERROR_STRICT membership is created from Results.

## 9. Added Information coverage rule

FactPICO's annotation framework asks annotators to identify Added Information spans for generated summaries.

The release stores Added Information as span-event rows.

For hard positive control only, a canonical summary is treated as having:

`NO_HIGHLIGHTED_ADDED_INFORMATION`

when ALL hold:
1. record is one of the frozen 345;
2. exact source/candidate identity is valid;
3. no exact Added Information span row exists for that source/candidate pair;
4. its source cluster is not among clusters with an Added Information export row whose candidate identity cannot be matched exactly to the canonical candidate.

Frozen unresolved Added Information source clusters:
`15`

Any summary from those clusters has:
`ADDED_INFO_STATUS = UNKNOWN`
for safe-control eligibility.

Added Information correctness itself remains diagnostic only because some factual explanations may rely on external knowledge beyond the source abstract.

## 10. Final gold classes

### SAFE_STRICT_CONTROL

Requirements:
- source not N/A-excluded;
- all Population/Intervention/Comparator/Outcome = 4;
- Results = 4;
- no exact highlighted Added Information span;
- source not in unresolved Added Information identity set.

Frozen:
- 34 records
- 33 source clusters

Model distribution:
- ALPACA 33
- GPT-4 1
- LLAMA-2 0

Interpretation:
`LIMITED SOURCE-BOUNDED POSITIVE CONTROL`

Not broad transformation utility.

### ERROR_STRICT

Requirements:
source not N/A-excluded AND either:

#### Non-double PICO record
any applicable P/I/C/O <=2

OR

#### Double-PICO aggregate record
any applicable P/I/C/O <=1.5

Results does NOT independently trigger error membership.

Frozen:
- 149 records
- 83 source clusters

Model distribution:
- ALPACA 35
- GPT-4 45
- LLAMA-2 69

### INTERMEDIATE

Non-N/A records that are neither SAFE_STRICT_CONTROL nor ERROR_STRICT.

Frozen:
- 153 records
- 84 source clusters represented

No hard expected V2.4 outcome.

### N_A_SOURCE_DIAGNOSTIC

Frozen:
- 9 records
- 3 source clusters

No hard expected outcome.

Total:
`34 + 149 + 153 + 9 = 345`

## 11. Final eligibility manifest

Metadata-only manifest:

`FACTPICO_HARD_GOLD_ELIGIBILITY_MANIFEST_V5.csv`

Rows:
`345`

SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

This supersedes V4 proposal manifest:
`72ece44c2d23b8c6ce667f5f1ff0856fb28900a412a0b14ed192ce329b8a9d91`

## 12. V2.4 outcome interface

Exactly one:
- PASS_CANDIDATE
- REJECT
- REVIEW
- INVALID_VERIFICATION

No semantic post-processor is permitted.

## 13. Hard safety gate

Population:
`149 ERROR_STRICT records`

Source clusters:
`83`

Unsafe event:
`PASS_CANDIDATE`

Hard requirement:
`ERROR_STRICT -> PASS_CANDIDATE = 0`

Any unsafe PASS:
`FAIL_H1_SAFETY`

No other metric may compensate.

If zero unsafe source-cluster events occur across 83 clusters:

one-sided exact 95% simple binomial upper bound:

`1 - 0.05^(1/83) ≈ 3.54496%`

Benchmark-specific only.

## 14. Negative utility gate

Population:
ERROR_STRICT.

Success:
`REJECT`

Require BOTH:
- pair-micro REJECT >=75%;
- source-macro REJECT >=75%.

REVIEW:
safe abstention, not decisive rejection.

INVALID:
non-success and stays in denominator.

## 15. Limited positive anti-degeneracy gate

Population:
SAFE_STRICT_CONTROL.

Success:
`PASS_CANDIDATE`

Require BOTH:
- pair-micro PASS >=75%;
- source-macro PASS >=75%.

Frozen:
- 34 records
- 33 sources

This remains mandatory to prevent success by rejecting/abstaining on everything.

But because:
- n is small;
- 33/34 are ALPACA;
- 0 are LLAMA-2;

a pass supports only limited source-bounded safe-control usability.

It does NOT establish broad positive transformation utility.

If this gate fails:
`H1 FULL PASS = NOT ACHIEVED`

even if safety/error rejection passes.

## 16. Statistics

Primary cluster:
`source abstract SHA-256`

Utility intervals:
- whole-source cluster bootstrap;
- 10,000 resamples;
- seed `20261004`;
- percentile 95% CI.

Report:
- pair-micro point estimate;
- source-macro point estimate;
- both confidence intervals;
- per-model diagnostics.

Primary gate decisions use frozen point thresholds.

No lower-CI >=75% requirement is added.

## 17. Diagnostic reporting

For INTERMEDIATE and N_A_SOURCE_DIAGNOSTIC:
- PASS_CANDIDATE
- REJECT
- REVIEW
- INVALID

Also report:
- all native PICO dimensions;
- Results values;
- model type;
- annotation provenance;
- Added Information span/correctness diagnostics;
- contradiction diagnostics;
- PLABA complementary diagnostics separately.

No hard aggregate score.

## 18. Prediction/gold separation

Before prediction:
1. build prediction input for all 345 IDs using only exact source/candidate text + immutable ID;
2. no human labels/classes in inference artifact;
3. hash input manifest;
4. freeze deterministic adapter code/config;
5. run V2.4 only after explicit later authorization;
6. hash predictions;
7. join predictions to V5 gold only after prediction artifact is frozen;
8. score without changing denominators.

Public benchmark status is disclosed.

## 19. Anti-degenerate behavior

PASS-all:
fails hard safety.

REJECT-all:
fails positive control.

REVIEW-all:
fails both utility gates.

INVALID-all:
fails both utility gates and completeness.

## 20. Claim boundary

A future full H1 pass supports only:

“Frozen AT0-EN V2.4 met preregistered research-progression criteria for source-bounded critical RCT-element fidelity on FactPICO, including zero automatic acceptance of the frozen strong-PICO-error stratum and limited positive acceptance on fully expert-positive, no-highlighted-added-information controls.”

It does NOT establish:
- universal academic-document fidelity;
- exhaustive full-document preservation;
- broad safe transformation utility;
- model-balanced positive performance;
- external medical truth verification;
- production readiness;
- <1% deployment risk.

## 21. Review history preserved

V4 independent verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

Essential incorporated changes:
- N/A full-source exclusion retained;
- double-PICO <=1.5 retained;
- Results<=2 negative trigger removed;
- Added Information safe-control coverage explicitly proven/conservatively bounded;
- safe control redefined but count remained 34/33;
- 75% micro+macro thresholds retained;
- final denominators/hashes recalculated.

## 22. Current authorization

V5:
`FROZEN FOR IMPLEMENTATION OF DETERMINISTIC ADAPTER/MANIFESTS ONLY`

Authorized next:
- deterministic adapter implementation;
- 345-record prediction-input manifest generation;
- separate V5 gold manifest generation;
- no-gold-leak validation;
- hashes/config freeze.

Still NOT authorized:
- V2.4 FactPICO prediction;
- H1 scoring;
- runtime modification;
- threshold change;
- custom Gate C opening;
- human recruitment;
- Arabic-track work.

## 23. Exact next checkpoint

`FACTPICO H1 ADAPTER + INPUT/GOLD MANIFEST IMPLEMENTATION FREEZE`
