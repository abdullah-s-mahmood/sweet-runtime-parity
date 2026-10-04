# ACAD_PASS — H1 PLABA 2024 Adapter + Native Metric Contract V1

Date: 2026-10-04
Status: FROZEN PRE-PREDICTION CONTRACT / NO V2.4 EXECUTION

Parent evidence:
- `H1_PHYSICAL_SCHEMA_SOURCE_CLUSTER_FREEZE_V1.md`
- `GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

Canonical external resource:
`TREC PLABA 2024 complete-abstract rewrite manual judgments`

Manual-judgment archive SHA-256:
`8256f7342c180e881e9c11244a7c24fe3e2fb4bdabf0fdfeb04892e4c8c722ce`

Source/test archive SHA-256:
`f9416ee9ef5a051e79053b526ad7023237cb87d171e79d9623bda4dbd656991e`

## 1. Native human construct

The 2024 PLABA human axes are retained natively:

- `ACC` — Accuracy: whether the output accurately reflects the source.
- `COM` — Completeness: whether the output minimizes information loss.
- `SIM` — Simplicity.
- `BRV` — Brevity.

Observed human score alphabet:
`-1, 0, 1`

H1 uses only ACC and COM as fidelity constructs.

SIM and BRV are retained as diagnostic metadata and do not determine scientific-fidelity PASS/FAIL.

## 2. No forced three-way gold mapping

PLABA does NOT provide ACAD_PASS-native labels:
- PASS_CANDIDATE
- REJECT
- REVIEW
- INVALID_VERIFICATION

Therefore ACAD_PASS will NOT map:
`0 -> REVIEW`

A middle Likert score is a quality judgment, not evidence that the relation is genuinely unresolved.

Likewise, PLABA does not directly encode ACAD_PASS criticality/materiality.

## 3. Frozen gold strata

### EXTREME_POSITIVE

Definition:
`ACC == 1 AND COM == 1`

Interpretation:
the human judgment gives the highest available score on both source accuracy and information preservation.

Observed:
- rows: `51,901`
- PMID source clusters: `399`

For the exact sentence-level fidelity scope of PLABA, this is the only gold stratum considered eligible for PASS-compatible hard-gate evaluation.

### EXTREME_NEGATIVE

Definition:
`ACC == -1 OR COM == -1`

Interpretation:
at least one core fidelity axis receives the worst available human score.

Observed:
- rows: `4,275`
- PMID source clusters: `396`

This stratum is eligible for hard containment testing:
V2.4 must not automatically PASS these worst-score fidelity cases.

Because PLABA does not label materiality/ambiguity, REJECT and REVIEW are both acceptable conservative dispositions.

INVALID_VERIFICATION is NOT counted as a successful scientific disposition.

### MIDDLE

Definition:
all other ACC/COM combinations.

Observed:
- rows: `20,614`
- PMID source clusters: `399`

Status:
`DIAGNOSTIC ONLY`

No exact ACAD_PASS outcome is assigned.

## 4. Eligible external records

Use ALL human-gold rows present in the frozen 19-run archive.

Gold-available rows:
`76,790`

Expected 19 x 4,060 run-sentence grid:
`77,140`

External-gold coverage:
`76,790 / 77,140 = 99.5462794918%`

The 350 absent run×sentence gold rows:
- remain explicitly reported;
- are not invented;
- are not scored;
- cannot be selectively recovered after predictions.

No run is excluded merely because it is incomplete.

## 5. Adapter input construction

For every eligible human-gold row:

`source_text = Source`

`candidate_text = Target`

Transport metadata only:
- record_id
- run filename
- Abstract ID
- Sentence index
- PMID / source_cluster_id

Do NOT include in prediction input:
- Accuracy
- Completeness
- Simplicity
- Brevity
- gold stratum
- any gold-derived explanation
- any human rationale

No lowercasing.
No paraphrase normalization.
No spelling correction.
No entailment inference.
No coreference resolution.
No semantic label repair.

The adapter performs transport/identity validation only.

## 6. Context policy

Primary verification scope:
`one PLABA source sentence -> its submitted target adaptation`

No full-abstract context is injected by the adapter.

Reason:
PLABA 2024 requires output for a given source sentence not to contain information from other source sentences.

If the frozen V2.4 verifier cannot resolve a critical relation from the permitted sentence-local evidence, conservative REVIEW/INVALID behavior remains visible.

The adapter must not resolve that ambiguity itself.

## 7. V2.4 output contract

The scorer accepts exactly one frozen V2.4 transaction outcome per eligible record:

- `PASS_CANDIDATE`
- `REJECT`
- `REVIEW`
- `INVALID_VERIFICATION`

Prediction IDs must equal the frozen eligible record IDs exactly.

Missing, duplicate, unknown, or extra prediction IDs invalidate the H1 evaluation.

## 8. Primary independence unit

`PMID`

Rules:
- all sentences from one PMID are one source cluster;
- all 19 system outputs from the same PMID remain in that cluster;
- duplicate abstract slots sharing a PMID remain one cluster;
- human axes do not create new independent units.

Frozen source clusters:
`399`

Extreme-negative clusters:
`396`

## 9. Hard H1 progression metrics

### H1-POS — positive safe automatic acceptance

For every PMID with >=1 EXTREME_POSITIVE record:
1. compute within-PMID proportion of positive records predicted `PASS_CANDIDATE`;
2. macro-average equally across PMIDs.

Hard threshold:
`>= 0.75`

Rationale:
this is semantically close to the original Gate C faithful-safe-acceptance progression threshold, but applied only to the strongest human positive stratum.

Strong-adoption target remains:
`>= 0.90`

and is NOT silently substituted for this research-progression threshold.

### H1-NEG-CONTAIN — valid conservative handling of worst-score gold

For every PMID with >=1 EXTREME_NEGATIVE record:
1. record success when outcome is `REJECT` or `REVIEW`;
2. record failure when outcome is `PASS_CANDIDATE` or `INVALID_VERIFICATION`;
3. compute within-PMID success proportion;
4. macro-average equally across PMIDs.

Hard threshold:
`>= 0.75`

This prevents a verifier from passing H1 by returning INVALID on the negative stratum.

### H1-NEG-AUTOPASS — unsafe automatic acceptance

A negative-cluster event occurs if ANY EXTREME_NEGATIVE record inside one PMID is predicted `PASS_CANDIDATE`.

Hard threshold:
`0 clusters with an event`

Observed gold denominator before prediction:
`396 PMID clusters`

If zero events are observed, the simple one-sided 95% exact upper bound under the independent-cluster binomial model is approximately:

`0.7536%`

This bound describes the frozen benchmark-cluster model only.
It does NOT establish <1% general production risk.

## 10. Diagnostic metrics

Report, but do not use as compensating hard gates:

- micro positive PASS rate;
- micro negative REJECT/REVIEW rate;
- INVALID_VERIFICATION rate by stratum;
- REJECT vs REVIEW composition in negative stratum;
- outcome distribution for MIDDLE;
- full 3x3 ACC×COM outcome tables;
- PASS_CANDIDATE extreme-stratum selective precision, when defined;
- per-run results;
- per-PMID distribution;
- ACC and COM distributions within each V2.4 outcome.

No weighted global accuracy across H1/H2/H3/H4 is permitted.

## 11. Statistical reporting

Use:
`PMID-cluster bootstrap`

Frozen settings:
- bootstrap replicates: `10,000`
- RNG seed: `20261004`
- interval: `95% percentile`
- resampling unit: complete PMID source cluster

Report cluster-macro point estimates plus bootstrap intervals.

For H1-NEG-AUTOPASS:
- report event clusters / 396;
- if zero, report one-sided exact 95% upper bound.

Multiple sentences/runs within a PMID never increase the inferential N.

## 12. Missing/invalid treatment

### Missing external gold
The frozen 350 absent run×sentence gold cells:
`EXTERNAL_GOLD_MISSING`

They are reported in coverage and excluded from scored gold because no human label exists.

### Missing V2.4 prediction
Any missing prediction for one of the 76,790 eligible gold records:
`INVALID_H1_EVALUATION`

Do not shrink the denominator.

### V2.4 INVALID_VERIFICATION
Retain in the denominator.

For EXTREME_POSITIVE:
not accepted.

For EXTREME_NEGATIVE:
not counted as valid containment.

For MIDDLE:
reported diagnostically.

## 13. Safety / utility precedence

If any EXTREME_NEGATIVE PMID has >=1 automatic PASS:

`FAIL_H1_UNSAFE_AUTO_PASS_ON_WORST_HUMAN_GOLD`

No utility metric compensates.

If unsafe auto-PASS is zero but H1-POS or H1-NEG-CONTAIN fails:

`MIXED_H1_UTILITY_OR_COVERAGE_FAIL`

If all three hard rules pass:

`PASS_H1_PLABA_RESEARCH_PROGRESSION`

Protocol-integrity failure yields:

`INVALID_H1_EVALUATION`

## 14. Anti-degenerate behavior

This contract prevents:

- PASS-all:
  fails negative auto-PASS gate.

- REVIEW-all:
  fails positive safe-acceptance gate.

- REJECT-all:
  fails positive safe-acceptance gate.

- INVALID-all:
  fails positive acceptance and negative valid-containment gates.

## 15. Prediction/gold separation

Prediction file contains source/candidate text and transport metadata only.

Gold file is separate.

Predictions must be:
1. generated with frozen V2.4;
2. written and hashed;
3. frozen;
4. only then joined to gold for scoring.

Public-gold status is acknowledged.
This is procedural anti-leakage separation, not a claim of secret holdout independence.

## 16. Claim boundary

A future H1 pass may support:

“Frozen V2.4 met preregistered fidelity progression criteria on the extreme human-rated accuracy/completeness strata of the PLABA 2024 biomedical adaptation benchmark.”

It does NOT establish:
- universal academic-document preservation;
- production safety;
- full-document fidelity outside this task;
- natural REVIEW accuracy;
- external scientific truth;
- <1% general population error.

## 17. Execution state

Adapter/metric semantics:
`FROZEN`

V2.4 external predictions:
`NOT AUTHORIZED YET`

Remaining before H1 execution:
- freeze adapter implementation hash;
- freeze scorer implementation hash;
- freeze generated eligible-ID/input/gold manifest hashes;
- close applicable rights documentation;
- satisfy remaining global EXT/META readiness conditions.
