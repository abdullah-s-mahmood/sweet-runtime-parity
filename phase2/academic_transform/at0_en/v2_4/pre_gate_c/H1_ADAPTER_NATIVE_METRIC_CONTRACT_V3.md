# ACAD_PASS — H1 PLABA 2024 Adapter + Native Metric Contract V3

Date: 2026-10-04
Status: FROZEN FOR INDEPENDENT REVIEW / NO V2.4 EXTERNAL PREDICTION

Supersedes for the preferred path:
- `H1_ADAPTER_NATIVE_METRIC_CONTRACT_V1.md`
- `H1_ADAPTER_NATIVE_METRIC_CONTRACT_V2.md`

Both prior versions remain preserved as historical protocol evidence.

Reason for V3:
V2 still treated repeated human-judgment rows from identical semantic inputs as separate prediction/evaluation units and used run completeness as a utility-selection rule. A direct duplicate/disagreement audit showed that identical `Source+Target` inputs recur across runs, some with conflicting human judgments. V3 removes this evidence inflation and freezes a canonical unique-pair design before any V2.4 prediction.

Parent evidence:
- `H1_PHYSICAL_SCHEMA_SOURCE_CLUSTER_FREEZE_V1.md`
- `GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

Canonical resource:
`TREC PLABA 2024 complete-abstract rewrite manual judgments`

Manual-judgment archive SHA-256:
`8256f7342c180e881e9c11244a7c24fe3e2fb4bdabf0fdfeb04892e4c8c722ce`

Source/test archive SHA-256:
`f9416ee9ef5a051e79053b526ad7023237cb87d171e79d9623bda4dbd656991e`

## 1. Native construct

Human axes:
- `ACC`: accuracy — output accurately reflects the source.
- `COM`: completeness — output minimizes information loss.

Human score alphabet:
`-1, 0, 1`

H1 functions:
- `H1-S <- ACC`
- `H1-C <- COM`

ACC and COM remain separate.

No weighted average can compensate one for the other.

## 2. Context contract

Official PLABA 2024 complete adaptation:
- produces output for each source sentence;
- permits splitting one source sentence into multiple target sentences;
- forbids merging source sentences;
- states output for a source sentence should not contain information from other source sentences.

Therefore the adapter may pass exactly:

`Source -> Target`

to frozen V2.4 without adding semantic context.

No gold rationale, label, neighboring gold, external medical knowledge, or semantic helper is permitted.

## 3. Canonical prediction unit

One V2.4 prediction per unique exact:

`PMID + Source + Target`

Canonical pair ID:

`SHA256("H1PAIRv1\0" + PMID + "\0" + Source + "\0" + Target)`

Text is preserved exactly as decoded from the frozen TSV/source artifacts.

No:
- lowercasing;
- spelling repair;
- whitespace semantic normalization;
- paraphrase merging;
- semantic canonicalization.

Duplicate run outputs and duplicate abstract slots for the same PMID do not create repeated predictions.

Frozen counts:
- human judgment rows: `76,790`
- unique Abstract+Sentence+Source+Target pairs: `62,382`
- unique canonical PMID+Source+Target prediction pairs: `62,315`

Frozen deterministic canonical eligibility-manifest SHA-256:

`f0371da56290999d4786ce86ea319be15f994c8cc8075a8fddaaa81c12cf5dc9`

## 4. Repeated human judgments are gold replication, not prediction replication

For each canonical pair, preserve every available human `(ACC,COM)` rating.

A canonical pair receives one V2.4 prediction.

Repeated human ratings are used only to assess gold consistency/sensitivity.

This prevents:
- repeated identical V2.4 calls;
- run-frequency weighting of identical text;
- treating repeated system outputs as independent evidence.

## 5. Individual rating classes

### SAFE
`ACC == 1 AND COM == 1`

### ERROR
`ACC == -1 OR COM == -1`

### INTERMEDIATE
all remaining combinations:
- `(0,0)`
- `(0,1)`
- `(1,0)`

No mapping:
`0 -> REVIEW`

## 6. Frozen canonical gold classes

### `SAFE_STRICT`

Every available rating for the pair is SAFE.

Pairs:
`40,609`

PMID clusters:
`399`

### `ERROR_STRICT`

Every available rating for the pair is ERROR.

Different raters may identify different failing axes, but every available judgment contains at least one worst-score fidelity defect.

Pairs:
`3,566`

PMID clusters:
`396`

### `INTERMEDIATE`

Every available rating for the pair is INTERMEDIATE.

Pairs:
`16,800`

PMID clusters:
`399`

### `HUMAN_CONFLICT`

Available ratings cross SAFE / ERROR / INTERMEDIATE class boundaries.

Pairs:
`1,340`

PMID clusters:
`320`

Total:
`62,315`

No class may be changed after prediction.

## 7. Multi-rated sensitivity subset

Canonical pairs with >=2 human ratings:
`10,554`

Breakdown:
- SAFE_STRICT: `7,159`
- ERROR_STRICT: `455`
- INTERMEDIATE: `1,600`
- HUMAN_CONFLICT: `1,340`

This is a preregistered sensitivity analysis.

It is not a replacement hard gate.

## 8. Why HUMAN_CONFLICT is not REVIEW gold

Human disagreement may arise from:
- rating variability;
- different views of severity;
- different failing axes.

It does not prove that the scientific relation itself is unresolved for V2.4.

Therefore:
`HUMAN_CONFLICT != REVIEW`

All V2.4 outcomes on HUMAN_CONFLICT are diagnostic only.

## 9. Adapter input

Prediction input contains only:
- `pair_id`
- `pmid`
- exact `source_text`
- exact `candidate_text`
- transport-only audit metadata

Prediction input MUST NOT contain:
- ACC
- COM
- SIM
- BRV
- gold class
- run-level aggregate score
- human rationale
- human disagreement state

## 10. Adapter boundary

Allowed:
- parse frozen ZIP/TSV/JSON;
- validate file hashes;
- exact ID lookup;
- exact text transport;
- deterministic deduplication;
- deterministic pair hashing;
- post-prediction gold join.

Prohibited:
- entailment inference;
- biomedical concept inference;
- coreference resolution;
- omission inference;
- semantic alignment;
- source/target rewriting;
- label repair;
- LLM/embedding use;
- gold-guided evidence selection.

If a semantic operation is needed for comparison:
`H1 = NOT_READY`

## 11. V2.4 outcome interface

Exactly one frozen V2.4 outcome per canonical pair:

- `PASS_CANDIDATE`
- `REJECT`
- `REVIEW`
- `INVALID_VERIFICATION`

No new semantic post-processor may transform this outcome.

## 12. Hard gold mapping

### SAFE_STRICT
Expected usability result:
`PASS_CANDIDATE`

Other outcomes reduce safe acceptance.

### ERROR_STRICT
Expected decisive result:
`REJECT`

`PASS_CANDIDATE`:
hard safety failure.

`REVIEW`:
safe non-acceptance but not successful decisive rejection.

`INVALID_VERIFICATION`:
non-success and remains in denominator.

### INTERMEDIATE
No hard expected outcome.

### HUMAN_CONFLICT
No hard expected outcome.

## 13. H1 hard safety gate

Metric:
`H1-SAFETY-1`

Population:
all `3,566 ERROR_STRICT` canonical pairs.

Eligible source clusters:
`396 PMIDs`

Hard requirement:

`ERROR_STRICT -> PASS_CANDIDATE = 0`

Any unsafe PASS:
`FAIL_H1_SAFETY`

No utility metric compensates.

## 14. Positive utility gate

Metric:
`H1-UTILITY-1`

Population:
all `40,609 SAFE_STRICT` canonical pairs.

Success:
`PASS_CANDIDATE`

Required:
- pair-micro PASS rate >= `75%`;
- PMID-macro PASS rate >= `75%`.

Strong-adoption target:
`>=90%`

remains separate and is not implied by this research-progression threshold.

No Source==Target pair is removed merely for being an identity transform.
Identity controls remain legitimate human-gold pairs and are reported as a prespecified subgroup.
Primary deduplication already prevents repeated identity outputs from inflating prediction count.

## 15. Negative utility gate

Metric:
`H1-UTILITY-2`

Population:
all `3,566 ERROR_STRICT` canonical pairs.

Success:
`REJECT`

Required:
- pair-micro REJECT rate >= `75%`;
- PMID-macro REJECT rate >= `75%`.

`REVIEW`:
safe abstention but not decisive rejection.

`INVALID_VERIFICATION`:
non-success.

`PASS_CANDIDATE`:
hard safety failure.

## 16. PMID macro calculation

Primary independence unit:
`PMID`

For each metric:
1. compute eligible-pair success rate within each PMID;
2. weight each eligible PMID equally;
3. macro-average PMID rates.

Rules:
- all sentences from one PMID are one cluster;
- all repeated system outputs remain within that cluster;
- multiple human ratings do not increase inferential N;
- duplicate source slot PMID `15857353` remains one cluster.

Maximum source clusters:
`399`

## 17. Statistical reporting

Utility metrics:
- cluster bootstrap whole PMIDs;
- `10,000` resamples;
- fixed seed `20261004`;
- percentile 95% CI.

Mandatory:
- pair-micro point estimate;
- PMID-macro point estimate;
- 95% cluster-bootstrap interval.

Safety:
report both:
- unsafe PASS pairs / 3,566;
- PMIDs containing >=1 unsafe PASS / 396.

If zero unsafe-PASS PMIDs are observed among 396:

one-sided exact 95% upper bound under the simple independent-cluster binomial model:

`1 - 0.05^(1/396) ≈ 0.7536%`

This is benchmark-cluster evidence, not a general production-risk guarantee.

## 18. Native ordinal diagnostics

Retain all original human ratings.

Mandatory diagnostics:
- ACC distribution;
- COM distribution;
- V2.4 outcome × canonical gold class;
- V2.4 outcome × ACC;
- V2.4 outcome × COM;
- INTERMEDIATE outcomes;
- HUMAN_CONFLICT outcomes;
- multi-rated sensitivity;
- identity-transform subgroup;
- per-run descriptive reconstruction;
- per-PMID distribution.

Do not numerically rank PASS/REVIEW/REJECT/INVALID solely to manufacture correlation.

## 19. External gold coverage

Possible run×source-sentence slots:
`77,140`

Observed human rows:
`76,790`

Missing external human rows:
`350`

Coverage:
`99.5463%`

Missing external gold:
- remains reported;
- gets no invented label;
- is not a V2.4 failure;
- cannot be selectively recovered after prediction.

The canonical prediction universe is every unique Source/Target pair represented by >=1 existing human judgment.

## 20. INVALID handling

`INVALID_VERIFICATION`:
- is never PASS;
- is never REJECT;
- remains in SAFE_STRICT and ERROR_STRICT utility denominators;
- is reported separately.

No invalid is dropped.

## 21. Criticality boundary

PLABA does not provide frozen ACAD_PASS criticality labels.

Therefore H1 alone cannot establish:
`critical silent scientific errors = 0`

H1 establishes only:
`no automatic PASS on ERROR_STRICT expert-rated fidelity cases`

Criticality-specific safety remains for H4/META and other explicit-criticality tracks.

## 22. Public-gold exposure

The project has inspected:
- schemas;
- labels;
- class frequencies;
- duplicates;
- human disagreement.

Therefore:
`NOT SECRET / NOT UNTOUCHED HOLDOUT`

However:
- V2.4 was frozen before H1 work;
- no V2.4 prediction on these PLABA records has occurred;
- V3 mapping, denominators, thresholds and statistics are frozen before prediction;
- future prediction artifacts must be hashed before gold join/scoring.

Allowed description:

`prospectively executed frozen-procedure evaluation against previously published external biomedical-expert judgments`

## 23. Anti-degenerate behavior

PASS-all:
fails H1-SAFETY-1.

REJECT-all:
fails H1-UTILITY-1.

REVIEW-all:
fails both utility gates.

INVALID-all:
fails both utility gates.

## 24. Gate states

### `PASS_H1_EXT`
Requires:
- zero unsafe automatic PASS on ERROR_STRICT;
- SAFE_STRICT pair-micro PASS >=75%;
- SAFE_STRICT PMID-macro PASS >=75%;
- ERROR_STRICT pair-micro REJECT >=75%;
- ERROR_STRICT PMID-macro REJECT >=75%;
- protocol integrity PASS.

### `MIXED_H1_EXT`
Safety passes but >=1 utility threshold fails.

### `FAIL_H1_SAFETY`
Any ERROR_STRICT pair receives PASS_CANDIDATE.

### `INVALID_H1_EVALUATION`
Any runtime/adapter/gold-separation/protocol-integrity failure.

## 25. Prior-version negative evidence

V1 and V2 are preserved.

Neither was executed.

V3 corrects before prediction:
- repeated identical-input inflation;
- incompatible human-gold expectations on disputed duplicate pairs;
- run-completeness-based utility selection;
- unnecessary exclusion of exact-copy positive transformations from the primary gold universe.

No empirical result is overwritten because no H1 prediction exists yet.

## 26. Exact next checkpoint

`INDEPENDENT REVIEW OF H1 CONTRACT V3`

No H1 adapter implementation or prediction is authorized until the independent review accepts or amends V3.

Still prohibited:
- V2.4 external prediction;
- H1 scoring;
- V2.4 tuning;
- threshold change after prediction;
- original custom Gate C opening;
- new-human recruitment;
- Arabic-track work.
