# ACAD_PASS — H1 PLABA 2024 Adapter + Native Metric Contract V2

Date: 2026-10-04
Status: FROZEN FOR INDEPENDENT REVIEW / NO V2.4 EXTERNAL PREDICTION

Supersedes for the preferred path:
`H1_ADAPTER_NATIVE_METRIC_CONTRACT_V1.md`

V1 is preserved as historical protocol evidence.

Parent evidence:
- `H1_PHYSICAL_SCHEMA_SOURCE_CLUSTER_FREEZE_V1.md`
- `GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

Canonical resource:
`TREC PLABA 2024 complete-abstract rewrite manual judgments`

Manual-judgment archive SHA-256:
`8256f7342c180e881e9c11244a7c24fe3e2fb4bdabf0fdfeb04892e4c8c722ce`

Source/test archive SHA-256:
`f9416ee9ef5a051e79053b526ad7023237cb87d171e79d9623bda4dbd656991e`

## 1. Construct

Native human axes:
- `ACC` — Accuracy: does the output accurately reflect the source?
- `COM` — Completeness: does the output minimize information loss?

H1 functions:
- `H1-S <- ACC`
- `H1-C <- COM`

ACC and COM are non-compensatory.
They are not averaged to hide failure.

Observed ordinal human scores:
`-1, 0, 1`.

## 2. No forced ACAD_PASS three-way gold

PLABA does not natively label:
- PASS_CANDIDATE
- REJECT
- REVIEW
- INVALID_VERIFICATION

Therefore:
`0 != REVIEW`

No exact three-way gold mapping is imposed.

Only conservative extreme-label strata are used for hard H1 interpretation.

## 3. Frozen human strata

### QUALIFIED_POSITIVE
`ACC == 1 AND COM == 1`

All 19 runs:
- rows: `51,901`
- PMIDs: `399`

### QUALIFIED_NEGATIVE
`ACC == -1 OR COM == -1`

All 19 runs:
- rows: `4,275`
- PMIDs: `396`

### INTERMEDIATE
All remaining ACC/COM combinations.

All 19 runs:
- rows: `20,614`
- PMIDs: `399`

INTERMEDIATE is diagnostic only.
It is not REVIEW gold.

## 4. Confirmatory utility subset

Utility gates use only the 14 runs with complete 4,060-row source-sentence coverage.

Complete runs:
- GPT.tsv
- LLaMA-8B-4bit-MedicalAbstract-seq-to-seq-v1.tsv
- LLaMa_3.1_70B_instruction_2nd_run.tsv
- TREC2024_SIB_run3.tsv
- UAms-BART-Cochrane.tsv
- UAms-ConBART-Cochrane.tsv
- bart_base_ft.tsv
- gpt-final.tsv
- gpt35_dspy.tsv
- mistral-FINAL.tsv
- mistral-fix.tsv
- task2_moa_tier1_post.tsv
- task2_moa_tier2_post.tsv
- task2_moa_tier3_post.tsv

Rows:
`56,840`

Strata:
- QUALIFIED_POSITIVE: `37,872`
- QUALIFIED_NEGATIVE: `3,677`
- INTERMEDIATE: `15,291`

QUALIFIED_NEGATIVE PMIDs:
`394`

The five incomplete runs are excluded from confirmatory utility because their external human-gold grid is incomplete before ACAD_PASS prediction.

Their observed gold remains active for safety and diagnostics.

## 5. Incomplete-run set

Incomplete runs:
- TREC2024_SIB_run1.tsv — 4,059 rows
- TREC2024_SIB_run4.tsv — 4,058 rows
- plaba_um_fhs_sub1.tsv — 4,043 rows
- plaba_um_fhs_sub2.tsv — 4,022 rows
- plaba_um_fhs_sub3.tsv — 3,768 rows

Missing external run×sentence judgments:
`350`

No missing gold may be invented or recovered selectively after predictions.

## 6. Exact-copy anti-inflation rule

Within the 14 complete runs:

QUALIFIED_POSITIVE:
`37,872`

Exact Source == Target:
`4,212`

Non-identical QUALIFIED_POSITIVE:
`33,660`

Non-identical positive PMIDs:
`399`

Primary safe-transformation acceptance uses ONLY:
`NON-IDENTICAL QUALIFIED_POSITIVE`

Reason:
unchanged source copies are valid identity controls but do not test transformation tolerance and would inflate the primary authentic-transformation acceptance metric.

Exact-copy positives remain a separate diagnostic identity-control stratum.

## 7. Adapter input

Inference receives exactly:
- exact `Source`
- exact `Target`
- immutable transaction ID

Transport metadata may exist outside the semantic inference path:
- run filename
- Abstract ID
- Sentence index
- PMID
- row hash

Inference MUST NOT receive:
- ACC
- COM
- Simplicity
- Brevity
- gold stratum
- human ranking
- neighboring gold
- rationale

No text rewriting or semantic enrichment is allowed.

## 8. Adapter boundary

Allowed:
- TSV parsing
- exact Unicode preservation
- deterministic serialization
- immutable ID generation
- non-semantic metadata attachment
- post-prediction gold join

Prohibited:
- semantic sentence alignment
- coreference resolution
- entailment inference
- biomedical concept inference
- omission repair
- source/target rewriting
- gold-derived transformation
- semantic relabeling

If any such operation is required for success:
`H1 = NOT_READY`

## 9. Frozen V2.4 outcome interface

Scoring accepts exactly one transaction outcome per eligible record:
- PASS_CANDIDATE
- REJECT
- REVIEW
- INVALID_VERIFICATION

Equivalent internal runtime labels may be transported only through an already-frozen deterministic lookup.

Missing, duplicate, unknown, or extra prediction IDs invalidate the evaluation.

## 10. Primary independence unit

`PMID`

Rules:
- all sentences from one PMID are one source cluster;
- all 19 system outputs from the same PMID remain in that cluster;
- duplicate abstract slots sharing a PMID remain one cluster;
- multiple human axes do not create new independent units.

Frozen source clusters:
`399`

## 11. Hard safety gate

Population:
ALL 19 runs, every observed QUALIFIED_NEGATIVE row.

Unsafe event:
`V2.4 outcome = PASS_CANDIDATE`

Hard requirements:
- row-level unsafe automatic PASS = `0 / 4,275`
- PMID clusters with >=1 unsafe PASS = `0 / 396`

Any unsafe PASS:
`FAIL_H1_SAFETY`

REVIEW or INVALID is not unsafe automatic acceptance, but does not count as decisive rejection utility.

If zero PMID-level events are observed across 396 exposed PMIDs, report the one-sided exact 95% upper bound:
`1 - 0.05^(1/396) ≈ 0.7536%`

This is benchmark-specific evidence only, not a general production-risk claim.

## 12. Positive utility gate

Population:
14 complete runs only.

Gold:
`QUALIFIED_POSITIVE`

Primary subset:
`NON-IDENTICAL QUALIFIED_POSITIVE`

Rows:
`33,660`

PMIDs:
`399`

Success:
`PASS_CANDIDATE`

Per-PMID score:
PASS_CANDIDATE rows / eligible non-identical positive rows for that PMID.

Primary statistic:
unweighted macro mean across 399 PMIDs.

Progression threshold:
`macro safe automatic acceptance >= 75%`

Strong-adoption target remains separately:
`>=90%`

and is not implied by passing the 75% research-progression threshold.

## 13. Negative utility gate

Population:
14 complete runs only.

Gold:
`QUALIFIED_NEGATIVE`

Rows:
`3,677`

PMIDs:
`394`

Success:
`REJECT`

REVIEW:
safe abstention but not decisive rejection.

INVALID_VERIFICATION:
non-success for utility.

PASS_CANDIDATE:
hard safety failure.

Per-PMID score:
REJECT rows / eligible negative rows for that PMID.

Primary statistic:
unweighted macro mean across 394 exposed PMIDs.

Progression threshold:
`macro decisive negative rejection >= 75%`

## 14. Intermediate treatment

INTERMEDIATE rows have no hard expected ACAD_PASS outcome.

Required diagnostics:
- PASS_CANDIDATE rate
- REJECT rate
- REVIEW rate
- INVALID rate

stratified by:
- ACC/COM cell
- PMID
- run

Also report whether automatic-PASS frequency is directionally monotonic with human ACC and COM strata.

No middle score becomes REVIEW gold.

## 15. Identity-control treatment

The 4,212 exact-copy QUALIFIED_POSITIVE rows from complete runs are diagnostic controls only.

Report their:
- PASS_CANDIDATE
- REJECT
- REVIEW
- INVALID_VERIFICATION

They do not enter the primary transformed-positive acceptance denominator.

Identity-control success cannot compensate poor transformation performance.

## 16. Missing/invalid handling

External gold missingness:
- absent human judgment remains absent;
- no label is invented;
- incomplete-run utility stays diagnostic.

Missing V2.4 prediction on an eligible record:
- remains visible;
- counts as non-success;
- causes protocol failure if the prediction artifact violates the exact frozen ID set.

V2.4 INVALID_VERIFICATION:
- remains in denominator;
- not accepted for positive utility;
- not counted as decisive negative rejection.

Adapter/runtime corruption:
- wrong Source/Target binding
- wrong ID
- post-freeze exclusion
- gold leakage
- runtime mismatch

yields:
`INVALID_H1_EVALUATION`

## 17. Statistical reporting

Primary independence unit:
`PMID`

Primary utility intervals:
cluster bootstrap over PMIDs.

Frozen settings:
- resamples: `10,000`
- seed: `20261004`
- interval: percentile 95%
- resample complete PMID clusters

Primary gate decision uses the preregistered point-estimate threshold.

Mandatory secondary reporting:
- micro row rates
- per-run rates
- ACC-specific outcomes
- COM-specific outcomes
- identity controls
- incomplete-run diagnostics

Safety zero-event:
exact one-sided 95% upper bound at PMID-event level.

Sentence/run counts are never reported as independent-study N.

## 18. Prediction/gold separation

Before prediction:
1. freeze eligible IDs;
2. create prediction-input artifact with Source, Target, immutable ID only;
3. hash prediction-input artifact;
4. keep gold in a separate artifact;
5. run frozen V2.4 once;
6. hash predictions;
7. only then join predictions to gold;
8. score under this frozen contract.

This is prospective procedural separation against public gold.
It is not secret-holdout independence.

## 19. H1 decision states

### PASS_H1_EXT
Requires:
- zero unsafe automatic PASS across all observed QUALIFIED_NEGATIVE rows in 19 runs;
- positive macro acceptance >=75%;
- decisive negative macro rejection >=75%;
- protocol integrity PASS.

### MIXED_H1_EXT
Safety zero passes, but one or both utility thresholds fail.

### FAIL_H1_SAFETY
Any QUALIFIED_NEGATIVE row receives PASS_CANDIDATE.

### INVALID_H1_EVALUATION
Any runtime/adapter/gold-separation/protocol-integrity failure.

## 20. Anti-degenerate behavior

PASS-all:
fails hard safety gate.

REJECT-all:
fails positive utility gate.

REVIEW-all:
fails positive utility and decisive negative-rejection gates.

INVALID-all:
fails utility and protocol integrity.

## 21. Claim boundary

Future PASS_H1_EXT may support only:

“Frozen AT0-EN V2.4 met preregistered H1 research-progression criteria on the extreme human-rated accuracy/completeness strata of TREC PLABA 2024, with zero observed unsafe automatic PASS events in the eligible worst-score human-gold cases.”

It does NOT establish:
- universal academic-document fidelity;
- production readiness;
- human writing quality;
- natural REVIEW accuracy;
- full-document preservation outside PLABA scope;
- external scientific truth;
- zero true risk;
- general <1% risk.

## 22. Current authorization

Contract:
`FROZEN FOR INDEPENDENT REVIEW`

External H1 prediction:
`NOT AUTHORIZED`

Exact next checkpoint:
`INDEPENDENT REVIEW OF H1 ADAPTER + NATIVE METRIC CONTRACT V2`
