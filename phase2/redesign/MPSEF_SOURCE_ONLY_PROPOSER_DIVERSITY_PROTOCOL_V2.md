# MP-SEF SOURCE-ONLY PROPOSER DIVERSITY PROTOCOL V2

Date: 2026-10-01
Status: FROZEN PRE-STAGE1 SOURCE-ONLY PROTOCOL
Closes: Independent Review MAJOR M02
Supersedes: MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V1 for future execution
Gold/reference use: FORBIDDEN

## 1. Purpose

Measure engineering feasibility and source-only legal candidate diversity for:

- P1_CONTROL;
- P2_V2;
- optional P3_V1.

This protocol does NOT measure correctness, recall, precision, R_joint, complete repair, or safe repair.

## 2. Stage definitions

### Stage 0 — synthetic only

No C_F project sentences.

Purpose:
- interface;
- identity;
- failure injection;
- parity harness;
- protection;
- runtime smoke tests.

### Stage 1 — deterministic source-only packet

Purpose:
- source-only execution/parity/provenance characterization;
- descriptive diversity;
- cost characterization.

Stage 1 is exploratory/descriptive for diversity.
It is NOT an independent scientific test of a threshold learned from itself.

### Stage 2 — full C_F source-only

Allowed only after:
- Stage 0 PASS;
- Stage 1 report frozen;
- proposer roster/retention decision frozen;
- independent review authorizes Stage 2 source-only execution.

Stage 2 still uses no gold/reference.

## 3. Stage 1 packet size

Frozen Stage 1 size:

`128 UIDs`

Rationale:
- large enough to exercise batch/order/repeat and heterogeneous source lengths;
- bounded enough to diagnose P2_V2/P3 implementation before full 1,918-case execution;
- used for engineering characterization, not inferential accuracy.

No claim of statistical representativeness is made.

Changing packet size requires a new protocol version before outputs are inspected.

## 4. Stage 1 deterministic cluster-aware selection

Population input:
C_F source manifest only.

No reference/gold fields allowed.

Selection salt:

`MPSEF-V4-STAGE1-SOURCE-ONLY-20261001-A`

Algorithm:

1. group rows by `cluster_id`;
2. for each cluster compute:
   `cluster_rank = SHA256(salt + "|cluster|" + cluster_id)`;
3. sort clusters ascending by cluster_rank;
4. choose first 128 distinct clusters;
5. inside each chosen cluster rank rows by:
   `row_rank = SHA256(salt + "|uid|" + uid)`;
6. choose the first row in that cluster;
7. sort final packet by UID for execution artifact stability.

Required:
- 128 UIDs;
- 128 distinct clusters;
- zero duplicates;
- all role == C_F.

Before any proposer output is generated, freeze:

- ordered UID list;
- ordered cluster list;
- UID-list SHA256;
- cluster-list SHA256;
- source-manifest SHA256.

## 5. Source-only source strata reported, not selected

After packet freeze, report source-only descriptive strata:

- source character length;
- source whitespace-token count;
- Arabic/Latin mixed-script presence;
- protected citation presence;
- number presence;
- unit presence;
- percent presence;
- URL/email presence;
- equation/technical-token markers where defined by source-only protection extraction.

These strata do not change membership.

No gold error type may be used for packet selection or stratification.

## 6. Engineering gates vs descriptive diagnostics vs retention decisions

### Engineering gates — must PASS

For each proposer:

- exact model/runtime/tokenizer identities frozen;
- all 128 UID records accounted for;
- no silent UID loss;
- no duplicate UID;
- provenance complete for every executable row;
- no unknown truncation among executable rows;
- batch/single parity requirements pass;
- repeat parity requirements pass;
- source identity pass;
- protected/legalizer fail-closed behavior pass;
- failure rows retained;
- gold/reference unavailable.

P2_V2 additionally requires B01 identity contract PASS.

P3 additionally requires M01 role/parent identity rules PASS.

### Descriptive diagnostics — no pass/fail quality meaning

- activity;
- output diversity;
- legal marginal contribution;
- keep-only reduction;
- runtime;
- component overlap;
- protection-disagreement;
- length-change burden.

### Retention decision

Stage 1 does NOT use a numeric diversity threshold.

After Stage 1, a documented architecture review determines:
- RETAIN FOR STAGE2;
- MODIFY AND REPEAT STAGE1;
- DEFER;
- DROP FOR ENGINEERING REASON.

Before Stage 2, the decision rule/roster must be frozen.

## 7. Denominator sets

All summary metrics MUST declare denominator.

### D_all

All 128 Stage 1 UIDs.

Failures remain in D_all.

### D_exec_j

UIDs where proposer j is source-only executable.

### D_joint_exec_jk

UIDs where both proposer j and k are executable.

### D_legal_j

UIDs where proposer j produces a legal whole output after source-only legalizer.

### D_changed_j

UIDs where proposer j final output differs literally from source.

No failure is represented as empty output for agreement calculations.

## 8. Literal output equality

Equality means exact final output string equality.

No normalization for equality/dedup:
- no whitespace normalization;
- no Unicode normalization;
- no punctuation removal;
- no Arabic-letter folding.

Every comparison reports denominator and failure-state handling.

## 9. Legal candidate set

For UID i define:

`L_i = {KEEP} U {all distinct full legal proposer outputs for i}`

after literal whole-output dedup with all provenance retained.

This is a set of legal alternatives, not a set of correct alternatives.

## 10. Legal marginal contribution

For proposer j on UID i:

`MC_ij = |L_i| - |L_i_without_j|`

where removing j removes only j's provenance/output contribution and retains identical output if another proposer supplies it.

Report:

- `sum_i 1[MC_ij > 0]` over D_all;
- number of distinct clusters with MC>0;
- total unique legal outputs contributed:
  `sum_i MC_ij`;
- distribution of MC values.

Name:
`SOURCE_ONLY_LEGAL_MARGINAL_CONTRIBUTION`

Never call this recall or coverage of corrections.

## 11. KEEP-only reduction

For each UID:

`KEEP_ONLY_i = 1 if |L_i| == 1 else 0`

For proposer j:

count UIDs where:
- without j: `|L_i_without_j| == 1`;
- with j: `|L_i| > 1`.

Report:
- UID count;
- distinct cluster count.

Name:
`SOURCE_ONLY_KEEP_ONLY_REDUCTION`

This is not correctness.

## 12. Leave-one-proposer-out source-only diagnostic

For proposer j:

- unique legal output count with all proposers;
- unique legal output count without j;
- UID count with >=1 non-KEEP candidate with all;
- UID count with >=1 non-KEEP candidate without j;
- cluster counts for same.

Report differences as:
`SOURCE_ONLY_LEAVE_ONE_PROPOSER_OUT`

Forbidden names:
- delta recall;
- delta R;
- quality gain.

## 13. Pairwise output diagnostics

For each pair j,k report separately:

Over D_all:
- both executable;
- j-only executable;
- k-only executable;
- neither executable;
- both legal;
- exact final-output equality among jointly executable;
- exact final-output difference among jointly executable.

Over D_joint_exec_jk:
- equality rate;
- difference rate.

Never exclude failures without showing D_all state matrix.

## 14. Component diversity

Use the frozen source-only alignment contract.

For jointly alignable rows report:

- exact component-set equality;
- intersection count;
- union count;
- Jaccard when union>0;
- PUNCTUATION_ONLY overlap;
- MIXED overlap;
- NON_PUNCTUATION overlap;
- WORD_BOUNDARY overlap;
- protected-region-touch overlap.

Alignment states are denominated separately:

- UNIQUE;
- AMBIGUOUS;
- FAILED;
- BUDGET_EXCEEDED.

Do not assign Jaccard=0 to non-computable alignment.

## 15. P3-specific delta diagnostics

Report both:

- P1_final -> P3_final;
- source -> P3_final.

Classify Stage-B changes:
- punctuation-only;
- mixed;
- non-punctuation;
- boundary-affecting;
- protected-touch.

P1/P3 remain one architecture family.

## 16. P2_V2 pipeline diagnostics

For D_all report:

- morphology success/failure;
- GED tokenization success/failure;
- zero-token-word failures;
- single-word-over-budget failures;
- number of GED segments;
- total GED wordpieces;
- exact word-identity coverage;
- unknown/unmapped label failures;
- GEC tokenization success/failure;
- GEC input-too-long failures;
- generation incomplete/ceiling/EOS failures;
- model-interface proof status.

No failed row is dropped.

## 17. Protection diagnostics

For every proposer, derive reason matrix:

- protected entity changed;
- separator/linkage changed;
- local attachment changed;
- global ordinal-only disagreement;
- citation movement;
- unit/number/percent linkage;
- alignment ambiguity;
- proof-budget exceeded;
- other frozen reason codes.

Multiple reasons may occur on one UID.

Report:
- UID count by reason;
- reason-combination count;
- cluster count.

Do not call any blocked row a false positive or lost useful repair.

## 18. Length and change burden

Per proposer report:

- input characters;
- output characters;
- output/input length ratio;
- absolute character delta;
- source token count;
- output token count;
- absolute token delta;
- component count.

Summaries:
- mean;
- median;
- p95;
- max.

These are anomaly diagnostics, not semantic judgments.

## 19. Runtime/resource budget

Stage 1 operational budget is frozen as an engineering safeguard, not a model-quality gate.

For each proposer runner:

- workflow timeout: 180 minutes;
- progress heartbeat <=60 seconds during active long work;
- stale threshold: 600 seconds unless stage-specific evidence justifies a new version;
- record cold-start wall time;
- record model-load time;
- record inference wall time;
- record legalizer wall time;
- record end-to-end wall time;
- record peak resident memory where available;
- if GPU used, record device identity and peak allocated GPU memory where available.

A timeout/OOM is an engineering failure requiring triage.

It is not evidence of linguistic quality.

Any different hardware class must be recorded and comparisons labelled accordingly.

## 20. Cost summaries

For each proposer:
- total end-to-end seconds;
- seconds per D_all UID;
- p50 and p95 per-UID time if measured;
- model load seconds;
- legalizer seconds;
- memory maximum.

For P3:
- separate incremental Pnx Stage-B cost from inherited/reused P1 Stage-A cost.

## 21. Batch/single/repeat parity

Stage 1 requires preregistered parity subset within the frozen 128 packet:

`32 UIDs`

Selection:
lowest SHA256 under:
`MPSEF-V4-STAGE1-PARITY-32-20261001-A|uid`

For those 32:
- single;
- batch;
- reordered batch;
- repeat.

P2_V2 parity covers trace identities defined by B01, not just final output.

P3 parent identity and Stage-B trace must match its contract.

## 22. Failure accounting

Every one of 128 UIDs has exactly one final proposer state per proposer.

Summary:
`sum(state_counts) == 128`

Unknown:
explicit fail-closed state.

No denominator is reduced because a proposer fails.

## 23. Stage 1 output artifacts

Required:

- `MPSEF_V4_STAGE1_PACKET_V1.json`
- `MPSEF_V4_STAGE1_PROPOSER_ROWS_V1.jsonl`
- `MPSEF_V4_STAGE1_LEGAL_ACTION_SETS_V1.jsonl`
- `MPSEF_V4_STAGE1_DIVERSITY_SUMMARY_V1.json`
- `MPSEF_V4_STAGE1_FAILURES_V1.jsonl`
- `MPSEF_V4_STAGE1_RUNTIME_V1.json`
- `MPSEF_V4_STAGE1_SHA256.txt`

## 24. Stage 1 decision rule

No numeric linguistic/diversity threshold is invented.

Automatic engineering DROP is allowed only for:

- unrepaired identity/provenance failure;
- inability to produce complete artifact accounting;
- persistent source identity corruption;
- runtime/resource failure beyond frozen budget that cannot be repaired within the approved architecture;
- zero unique legal whole-output contribution across the FULL authorized population used for the retention decision, when an equal/cheaper proposer supplies identical behavior.

Because Stage 1 is only 128 UIDs, zero marginal contribution on Stage 1 alone does NOT automatically prove zero Stage 2 value.

Stage 1 may justify:
- retain;
- modify;
- defer;
but not a linguistic-quality ranking.

## 25. Stage 2 preconditions

Before full C_F source-only Stage 2:

- Stage 1 report frozen;
- architecture review completed;
- proposer roster frozen;
- resource budget for Stage 2 frozen;
- retention rationale documented;
- no gold/reference used;
- V4 registry/legalizer integration frozen.

If Stage 1 observations motivate new diagnostics or thresholds:
- protocol version increments;
- decisions freeze before Stage 2;
- Stage 2 is not called independent evidence for hypotheses invented from Stage 1.

## 26. Scientific boundary

Forbidden in Stage 0/1/2 source-only diversity:

- R_joint;
- correctness;
- precision/recall/F-score;
- complete repair;
- selector training on correctness;
- gold-aware proposer retention;
- human correctness selection;
- INTERNAL/STRESS/reserved opening.


## 27. Independent-review closure amendment for M02

This section closes the remaining executable-definition gaps identified by the independent architecture review.

### 27.1 Quantile definition

Whenever p95 is reported over a finite list of n values:

- sort ascending;
- use nearest-rank;
- rank = ceil(0.95 * n);
- use 1-based indexing;
- if n=0, report N/A rather than zero.

The same quantile rule applies to runtime, length burden, candidate-set size, and component-count summaries.

### 27.2 Raw-valid versus executable versus legal denominators

Every summary row MUST state one of:

- D_all;
- D_raw_valid_j;
- D_exec_j;
- D_legal_j;
- D_joint_raw_valid_jk;
- D_joint_exec_jk.

No pairwise percentage may be printed without numerator and named denominator.

A failed proposer row never becomes an empty string for similarity/agreement purposes.

### 27.3 Resource-budget decision semantics

The Stage 1 timeout/resource budget is an engineering budget only.

If a proposer exceeds it:
- classify as ENGINEERING_FAIL_PENDING_TRIAGE;
- investigate load time, batching, memory, pathological source length, and alignment-budget causes;
- do not infer poor linguistic quality;
- any increased budget requires a protocol-version change before rerun.

### 27.4 Stage 1 retention semantics

Stage 1 may automatically reject a proposer only for a hard engineering/provenance failure.

Stage 1 descriptive diversity cannot by itself produce:
- BEST;
- WORST;
- HIGH_QUALITY;
- LOW_QUALITY;
- linguistically useful/useless.

A proposer with low or zero marginal contribution on Stage 1 remains DESCRIPTIVE_INCONCLUSIVE unless a hard engineering gate fails.

### 27.5 Full-population redundancy rule

Behavioral redundancy may justify source-only dropping only after an authorized full source-only population shows:

1. zero unique legal whole-output contribution;
2. no distinct legal failure profile needed by the architecture;
3. another proposer supplies the same legal behavior;
4. the retained proposer is equal or cheaper under the frozen resource accounting.

This is redundancy elimination, not a correctness judgment.

### 27.6 Cluster accounting

All marginal-contribution, KEEP-only reduction, and leave-one-proposer-out results MUST report both:
- UID count;
- distinct cluster count.

No UID-level percentage may be described as cluster coverage.

### 27.7 Stage 1 packet freeze artifact

Before any proposer runs, create and freeze:

- ordered 128 UID list;
- ordered 128 cluster list;
- source row hashes for all 128 rows;
- packet JSON SHA256;
- UID-list SHA256;
- cluster-list SHA256;
- source-manifest SHA256;
- registry SHA256.

Changing any of these requires a new Stage 1 packet version.

### 27.8 M02 closure status

M02 DESIGN is considered CLOSED when this protocol version is frozen together with the proposer registry/action-set contract.

Execution closure still requires:
- Stage 0 synthetic PASS;
- packet materialization;
- Stage 1 runtime/provenance execution.

No project gold/reference is required for M02 closure.
