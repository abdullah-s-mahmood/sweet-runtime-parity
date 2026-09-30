# MP-SEF PRE-UNION PROTOCOL V3
## ACAD_PASS Arabic Correction — Frozen Methodology Before Candidate-Union Measurement

Date: 2026-09-30
Status: FROZEN PRE-UNION PROTOCOL
Measurement status: BLOCKED UNTIL THIS DOCUMENT'S PRE-MEASUREMENT CHECKLIST IS SATISFIED
Parent architecture:
- phase2/redesign/ARABIC_CORRECTION_ARCHITECTURE_V2_MPSEF.md

Independent methodological review:
- MPSEF_INDEPENDENT_REVIEW_AR.md
- decision: MODIFY PROTOCOL BEFORE UNION MEASUREMENT

## 1. Purpose

This protocol replaces the earlier raw candidate-union formulation for the first MP-SEF feasibility measurement.

It does not authorize:
- selector training;
- AUTO_SAFE Arabic correction;
- opening INTERNAL_EVALUATION;
- opening STRESS_DIAGNOSTIC;
- QALB15 TEST;
- Confirmation;
- Holdout;
- A7'ta reserve;
- reserved Nahw IDs;
- adding a third proposer;
- changing P1 or P2 after observing feasibility metrics.

The only future measurement authorized by this protocol, after its checklist is satisfied, is one preregistered P1+P2 candidate-feasibility measurement on the designated feasibility role partition.

## 2. Historical facts that remain fixed

### H1-v1

H1-v1 remains formally CLOSED FAIL.

Frozen historical result:
- model role: one-pass SWEET NoPnx candidate generator;
- official-alignment one-pass NoPnx M2 recall: 69.39%;
- frozen feasibility gate: >=80%;
- deficit: -10.61 percentage points;
- inference parity: 256/256;
- CALIBRATION gold construction: 6,888/6,888;
- gold-construction failures: 0;
- char-alignment cross mismatches: 0;
- word/subword cross mismatches: 0.

H1-v1 must not be reinterpreted as P1 and must not be rewritten after later results.

### Closed components

H2:
- closed;
- no deterministic orthographic family activated.

H3:
- closed fail as standalone morphology validator.

H4:
- not activated;
- MERGE showed useful precision but insufficient recall.

M2-R:
- useful residual-risk signal;
- failed as standalone safety verifier.

## 3. Current proposer identities

### P1 — iterative SWEET proposer

Role:
candidate proposer only.

Model:
CAMeL-Lab/text-editing-qalb14-nopnx

Frozen model revision:
21286e56ce98a86362db540863f91c083b8970f9

Frozen weight SHA256:
9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d

Official implementation:
CAMeL-Lab/text-editing

Frozen implementation revision:
4d552ca3ae98029550f27fc52aa1b22883e16e61

Inference contract:
- NoPnx;
- top-1 labels;
- decode_iter=2;
- final pass-2 output is the single P1 proposal for the first feasibility cycle;
- pass-1 output is retained only as provenance/dependency trace;
- no confidence threshold;
- no top-k expansion;
- no punctuation model;
- no third pass.

Runtime parity:
- deterministic source-only sample n=64;
- pass 1 exact trace: 64/64;
- pass 2 exact trace: 64/64;
- all-field: 64/64;
- mismatches: 0.

Runtime artifact:
- run 36749690421;
- artifact 11113469233;
- digest sha256:994c98dbe965883f9097a1845dc3240105b3fb11de709aeb11f454b6a34dfbb0.

### P2 — AraBART + Morph + GED proposer

Role:
contextual seq2seq candidate proposer plus GED auxiliary evidence.

GEC model:
CAMeL-Lab/arabart-qalb14-gec-ged-13

GEC revision:
410588a318d988cdcfdbf64cf5745ed4adea0f6a

GEC pytorch_model.bin SHA256:
5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f

GED model:
CAMeL-Lab/camelbert-msa-qalb14-ged-13

GED revision:
447179dc63d186e4bff09a993e90e73ad622d571

GED pytorch_model.bin SHA256:
23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f

Official implementation:
CAMeL-Lab/arabic-gec

Frozen implementation revision:
8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

CAMeL morphology DB SHA256:
195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70

CAMeL MSA BERT unfactored disambiguator weight SHA256:
a1a22431cdc0934151e4039abbd7890f06ba7c1f914ca71a90eba218401ae539

Frozen inference path:
1. source whitespace tokenization;
2. MSA BERT unfactored disambiguation;
3. analyses[0].analysis["diac"];
4. dediac_ar;
5. CAMeLBERT GED;
6. argmax GED labels;
7. GED label expansion over AraBART subwords;
8. GED-conditioned AraBART generation.

Generation:
- num_beams=5;
- max_length=100;
- num_return_sequences=1;
- no_repeat_ngram_size=0;
- early_stopping=false;
- skip_special_tokens=true;
- clean_up_tokenization_spaces=false.

Runtime parity:
- deterministic source-only sample n=64;
- morphology text: 64/64;
- GED labels: 64/64;
- tokens: 64/64;
- input IDs: 64/64;
- GED label IDs: 64/64;
- generated exact output: 64/64;
- generated normalized output: 64/64;
- all-field: 64/64;
- mismatches: 0.

Runtime artifact:
- run 36751445734;
- artifact 11114738715;
- digest sha256:c8d2ea2b378a03b3e6ca5f81b53a0527f0f796d8610a6d615027eedce06cbaf3.

## 4. Scope of the first feasibility cycle

The first cycle contains exactly:
- P1 final pass-2 proposal;
- P2 final generated proposal;
- KEEP.

It does not contain:
- P1 pass-1 as an additional independent proposal;
- P1 pass-3;
- P1 top-k;
- P2 n-best;
- punctuation proposer;
- MTAGEC;
- STAGEET;
- cross-domain AraBART;
- generic LLM proposer;
- any proposal added after metrics are observed.

The first cycle is therefore a fixed two-proposer feasibility experiment.

## 5. Source-anchored hypothesis and bundle representation

Atomic reversibility alone is insufficient.

Each proposer output must first be represented as an immutable hypothesis rooted in the original source version.

Each hypothesis records:
- hypothesis_id;
- proposer_id;
- proposer runtime lock id;
- source_record_id;
- source_version_hash;
- full proposer output;
- source-to-output alignment status;
- truncation status;
- execution status;
- protected-span contacts;
- proposer-internal trace where available.

Each hypothesis is decomposed into one or more BUNDLES.

Each bundle records:
- bundle_id;
- hypothesis_id;
- original-source character/token spans;
- source text;
- replacement text;
- component edits;
- reversible inverse;
- operation-family labels;
- requires relationships;
- mutually-exclusive relationships;
- unresolved-dependency flag;
- protected-span overlap;
- provenance to proposer stage:
  - P1 pass 1;
  - P1 pass 2;
  - P2 morphology;
  - P2 GED;
  - P2 generation.

Rule:
if independence between component edits cannot be established without consulting the gold reference, the components remain one bundle.

Gold/reference data may never be used to split a bundle into easier independent candidates.

## 6. Original-source anchoring

All proposal effects are measured from the original source x0.

P1:
x0 -> x1 -> x2

The final P1 hypothesis is x0 -> x2.
x1 is provenance only.
Any pass-2 dependency on pass-1 changes is recorded.

P2:
x0 -> morphology_preprocessed -> GED-conditioned generation -> y

The final P2 hypothesis is x0 -> y.
Changes introduced by morphology/preprocessing are not allowed to disappear from the transaction history.

No feasibility metric may compare only morphology_preprocessed -> y.

## 7. Candidate equivalence and deduplication

Two bundles may share the same textual effect on x0 but still retain distinct provenance.

Deduplication therefore has two layers:
1. textual-effect equivalence;
2. execution-contract identity.

For coverage counting, identical textual effects are not counted twice.

For provenance/diversity analysis, proposer identity is retained.

Identical final strings do not imply independent corroboration.

## 8. Action space A_s(P)

For source sentence s and proposer pool P, define A_s(P) as the set of outputs that are legally constructible from:
- KEEP;
- P1 bundles;
- P2 bundles;

subject to all frozen:
- requires constraints;
- mutually-exclusive constraints;
- source-span conflicts;
- bundle integrity;
- protected-span policy;
- execution validity.

A_s(P) must be constructed using source text and proposer outputs only.

Gold/reference data may not:
- create actions;
- split bundles;
- repair alignments;
- remove difficult candidates;
- choose a more favorable decomposition.

Adding a proposer must not remove KEEP or any previously legal action.

## 9. Punctuation scope

The first feasibility cycle is NoPnx.

Primary feasibility denominator:
reference corrections inside the frozen NoPnx scope.

Punctuation-only reference corrections are reported separately as out-of-scope-for-this-cycle targets.

Mixed bundles that combine punctuation and linguistic change may not be partially stripped using the gold reference.

If a mixed bundle cannot be separated by source/proposer-only rules, it remains a bundle and is reported as such.

No punctuation target may silently disappear from product-level accounting.

## 10. Protected invariants

Protected spans include, at minimum:
- numbers;
- units;
- equations;
- citations;
- URLs;
- emails;
- code/Latin fragments;
- document structural markers;
- high-confidence named entities where the protection rule is deterministically applicable.

Distinguish:
A. proposal touches protected content;
B. executable action silently changes protected content.

A is a risk metric.
B is a structural failure.

The first feasibility cycle may log raw protected-touch proposals, but no action violating the frozen protected-span policy enters A_s(P).

Structural gate:
unauthorized executable protected-span changes = 0.

## 11. Exposure ledger

The protocol distinguishes:
- source-only exposure;
- gold/reference exposure;
- aggregate-result exposure;
- error-analysis exposure;
- fitting;
- threshold selection.

Established current exposure state:

### CALIBRATION as a whole

The full 6,888-case CALIBRATION population has already been used in prior H1 official-alignment gold construction and aggregate feasibility measurement.

Therefore:
- CALIBRATION is development evidence;
- no later partition of it may be described as historically untouched;
- repartitioning separates future roles only;
- repartitioning does not erase adaptive reuse.

P1 parity:
- source-only 64-case deterministic sample;
- no gold/reference consulted.

P2 parity:
- source-only 64-case deterministic sample;
- no gold/reference consulted.

Before feasibility measurement, the repository must contain a machine-readable exposure ledger assigning, for every allowed CALIBRATION cluster/record, at least:
- source_only_exposed;
- gold_exposed;
- aggregate_result_exposed;
- error_analysis_exposed;
- fit_exposed;
- threshold_selection_exposed;
- unknown_exposure.

Any unknown exposure is treated conservatively as exposed for independence claims.

## 12. Future role partition of CALIBRATION

Because CALIBRATION is already development-consumed, the split below is a future role split, not an independent-confirmation split.

Roles:
- C_F: 30% feasibility;
- C_T: 40% future selector development, if later authorized;
- C_R: 30% future risk calibration, if later authorized.

C_R is NOT permitted to certify independent 98% AUTO_SAFE precision merely because it is held out from this point forward.

### Cluster unit

Clusters connect records sharing, where available:
- same document;
- same author;
- exact duplicate;
- near duplicate.

Near-duplicate key:
- NFC;
- whitespace normalization for duplicate detection only;
- whitespace tokenization;
- Jaccard token-set similarity >=0.90;
- shorter/longer token-length ratio >=0.90;
- no normalization collapsing distinct Arabic letters.

Missing document/author metadata is recorded as a limitation.

### Allowed source-only stratification

- corpus/domain;
- L1/L2 if already available without opening hidden labels;
- source length bins:
  - <=20 words;
  - 21-40;
  - 41-80;
  - >80;
- unknown;
- mixed.

### Deterministic assignment

Cluster identifier:
- sort unique record IDs by Unicode code-point order;
- join with LF and no trailing LF;
- SHA256 UTF-8.

Within each source-only stratum, sort clusters by:
SHA256("ACAD_PASS|MPSEF|V3|SPLIT1" + LF + cluster_id)

For strata with m >= 10 clusters:
- first floor(0.30*m) -> C_F;
- next floor(0.40*m) -> C_T;
- remainder -> C_R.

For strata with m < 10:
integer SHA256 value modulo 10:
- 0-2 -> C_F;
- 3-6 -> C_T;
- 7-9 -> C_R.

Do not choose a new salt for better balance.

Report actual cluster and record proportions.

## 13. Primary endpoint

Primary endpoint:

R_joint(P)

Definition:

For each source sentence s, let G_s be the frozen set of complete NoPnx reference correction targets under the frozen official alignment/matching definition.

Let A_s(P) be the legal action space defined before consulting G_s.

For any y in A_s(P), TP_fixed(y,G_s) is the number of complete reference targets correctly achieved under the frozen matching rule, with:
- no half-credit;
- no duplicate credit;
- no gold-guided bundle splitting.

Then:

R_joint(P) =
sum_s max_{y in A_s(P)} TP_fixed(y,G_s)
/
sum_s |G_s|

Interpretation:
R_joint is an oracle feasibility ceiling for a selector restricted to the same action space.

It is not:
- expected selector performance;
- AUTO_SAFE precision;
- semantic safety;
- proof of complete sentence correctness.

If exact optimization is not computationally feasible, report a proven interval:
L <= R_joint <= U

Decision rules use the interval, not a greedy point estimate.

## 14. Strict residual recall

The phrase strict residual recall is frozen here as follows for this candidate-feasibility phase:

Primary coverage target:
all in-scope NoPnx reference correction targets in C_F.

Historical residual target:
targets not achieved by the frozen H1-v1 one-pass output under a representation-compatible mapping, reported as a separate secondary endpoint only.

No claim is permitted that overall R_joint directly equals residual recall.

If later product requirements define residual recall as errors routed to REVIEW rather than correction candidates, that is a separate detection endpoint and requires a separate protocol.

## 15. Mandatory secondary endpoints

Report all of the following:

1. R_P1:
R_joint({P1})

2. R_P2:
R_joint({P2})

3. R_raw:
per-reference-target reachability without requiring joint realization of all reached targets in one legal output.

Required relationship:
R_raw >= R_joint

4. R_raw - R_joint gap.

5. R_clean:
maximum reference recall achievable by a legal output containing no extra reference-incompatible edit under the frozen reference comparison.

6. Complete-sentence repair coverage:
fraction of erroneous sentences for which one legal output achieves all frozen reference corrections with no extra reference-incompatible edits.

7. Four-way target coverage:
- both P1 and P2;
- P1 only;
- P2 only;
- neither.

8. Leave-one-proposer-out marginal gains:
Delta_P1 = R_joint(P1,P2) - R_joint(P2)
Delta_P2 = R_joint(P1,P2) - R_joint(P1)

9. Micro recall.

10. Macro recall across frozen operation/error families.

11. Family-level recall with exact target/sentence/document denominators.

12. Clean-sentence proposal rate:
reference-clean sentences with >=1 non-KEEP proposal / clean sentences.

13. Conflict burden:
- fraction of unique candidates in >=1 conflict;
- fraction of sentences with conflict;
- spatial conflicts;
- dependency conflicts.

14. Candidate volume per sentence:
- median;
- p95;
- max;
- total;
before and after protected-span filtering.

15. Protected-touch proposal rate.

16. Reference-target loss induced by protected-span policy, reported without removing targets from the original product denominator.

17. Source-attribution failures.

18. Ambiguous alignments.

19. truncation events.

20. execution failures.

21. empty outputs.

22. case accounting:
every C_F record must terminate in exactly one accountable state.

Failures remain in denominators.
They are not silently excluded.

## 16. Candidate-stage feasibility gate

Primary gate:

R_joint(P1,P2) >= 0.95

Interpretation:
passing means only that the frozen P1+P2 action space provides sufficient candidate availability for later research.

It does not authorize:
- selector training automatically;
- AUTO_SAFE;
- opening INTERNAL_EVALUATION;
- adding hidden thresholds.

If exact R_joint is unavailable and only [L,U] is proven:
- PASS if L >= 0.95;
- FAIL if U < 0.95;
- INCONCLUSIVE otherwise.

Diagnostic bands:
- >=0.95: candidate availability PASS;
- >=0.90 and <0.95: feasibility FAIL, one diagnostic memo allowed;
- <0.90: current P1+P2 high-coverage path FAIL for this cycle.

No threshold change is allowed after measurement.

## 17. Historical-residual reporting

Because H1-v1 achieved 69.39% on its frozen historical metric, do not infer residual coverage from overall R_joint unless denominators and mappings are demonstrated compatible.

Where a valid mapped residual target set exists, report:
R_joint,residual

It is secondary in V3.

If a future protocol makes residual correction recall the primary endpoint, it must set its own denominator and gate before measurement.

## 18. Proposer retention

A proposer may be retained in a later architecture only if, in the preregistered comparison, at least one route passes.

### General route

Leave-one-out gain:
Delta_j >= 0.010 absolute R_joint.

### Frozen weak-family route

Only these families are eligible in this cycle:
- INSERT;
- MERGE/SPLIT.

A proposer passes the family route if:
- family recall gain >=5 percentage points;
- >=10 additional complete reference targets;
- those targets occur across >=10 distinct document clusters.

If cluster identity is unavailable, the family route cannot pass by substituting sentences for document clusters.

### Not accepted

"unique corroborating evidence" alone is not a successful retention route in this candidate-stage protocol.

Agreement provenance is retained for later research but does not justify keeping a proposer by itself.

## 19. Simplest-system preference

If one proposer alone passes the candidate-stage gate and the other passes no retention route, prefer the simpler retained system for the next stage.

If both single proposers pass and neither provides >=1 pp gain when paired:
- prefer lower measured operational cost;
- if operational cost is tied/unavailable, use P1 as fixed tie-break baseline.

This tie-break is a resource policy, not a scientific claim of superiority.

## 20. Stop rules

All are frozen before measurement.

1. First cycle is exactly P1+P2.
2. One final output per proposer.
3. No third proposer after observing results.
4. No third SWEET pass.
5. No top-k expansion.
6. No P2 n-best expansion.
7. No punctuation addition.
8. No post-result change to:
   - target definition;
   - families;
   - denominator;
   - matching;
   - protection policy;
   - bundle splitting;
   - proposer identity;
   - decode settings.
9. R_joint <0.95 blocks selector training in this cycle.
10. 0.90-<0.95 permits exactly one diagnostic memo, not an automatic rescue experiment.
11. <0.90 closes the P1+P2 high-coverage cycle.
12. INCONCLUSIVE closes the cycle without adding a proposer.
13. One technical rerun is permitted only for a failure occurring before any feasibility metric is observed and with identical scientific configuration.
14. A construction bug discovered after metrics invalidates that protocol version; rerunning the same consumed sample is not called an independent new test.
15. Passing does not authorize AUTO_SAFE.
16. Passing does not automatically authorize selector fitting.

## 21. Selector authorization — not part of this run

Selector training is not currently authorized.

If the candidate stage later passes, a separate frozen selector protocol is required.

At minimum it must specify:
- bundle-level labels;
- human adjudication rubric;
- source-cluster separation;
- model family;
- features;
- threshold-selection rule;
- risk-calibration method;
- REVIEW / REJECT / AUTO_SAFE policy;
- protected-span hard vetoes;
- composed-output recheck.

No proposer score or GED score is independent verification merely because it is numeric.

A simple inspectable selector such as logistic regression or bundle ranking is preferred as the first research baseline if later authorized.

## 22. AUTO_SAFE future constraint

No AUTO_SAFE claim is authorized in V3.

Future minimum constraint remains:
- one-sided 95% lower confidence bound for necessary-edit precision >=98%;
- zero protected-invariant failures;
- zero unauthorized number/unit/citation changes.

The 98% target is not evaluated in the candidate-feasibility run.

C_R cannot be called historically independent merely because it is reserved from now on.

If valid independent calibration evidence cannot be established later, Arabic may remain REVIEW-only.

## 23. Training-overlap audit

Before interpreting feasibility as evidence of generalization, record what is known about overlap between proposer training corpora and C_F.

Required fields:
- P1 known training corpus identity;
- P2 known training corpus identity;
- record/document overlap known yes/no/unknown;
- method used to establish overlap;
- unresolved overlap.

Unknown overlap does not invalidate a development feasibility study, but it blocks stronger generalization claims.

No hidden/reserved dataset may be opened to perform this audit.

## 24. Required pre-measurement artifacts

The feasibility measurement may not start until all exist and are frozen:

1. MPSEF_PRE_UNION_PROTOCOL_V3.md
2. MPSEF_EXPOSURE_LEDGER_V1.jsonl
3. MPSEF_EXPOSURE_LEDGER_SUMMARY_V1.json
4. MPSEF_ROLE_SPLIT_V1.jsonl
5. MPSEF_ROLE_SPLIT_SUMMARY_V1.json
6. MPSEF_BUNDLE_CONTRACT_V1.md
7. MPSEF_TARGET_AND_MATCHING_CONTRACT_V1.md
8. MPSEF_PROTECTED_INVARIANTS_CONTRACT_V1.md
9. P1 runtime lock
10. P2 runtime lock
11. exact runner/workflow hashes
12. a preflight showing:
   - C_F/C_T/C_R disjoint at cluster level;
   - every CALIBRATION record assigned exactly once;
   - no reserved/internal split opened;
   - no feasibility metric computed.

## 25. Pre-measurement blocker fields

Current known state:

- P1 exact identity: RESOLVED
- P2 exact identity: RESOLVED
- P1 runtime parity: RESOLVED PASS
- P2 runtime parity: RESOLVED PASS
- CALIBRATION historical independence: RESOLVED NEGATIVE
  - it is development-consumed;
- exact exposure ledger per record/cluster: NOT YET MATERIALIZED
- deterministic role split manifests: NOT YET MATERIALIZED
- bundle contract: NOT YET MATERIALIZED
- target/matching contract: NOT YET MATERIALIZED
- protected-invariant contract: NOT YET MATERIALIZED
- training-overlap audit: NOT YET RESOLVED
- candidate-union metric: NOT OBSERVED
- selector: NOT AUTHORIZED

Measurement remains blocked while any required artifact in Section 24 is missing.

## 26. Scientific interpretation

Relative to the original MP-SEF v2 proposal:

**IMPROVED METHODOLOGICALLY / PERFORMANCE STILL NOT MEASURED**

Main improvements:
- raw union recall replaced by jointly realizable R_joint;
- atomic-edit independence replaced by bundle/dependency semantics;
- original-source anchoring required for both P1 and P2;
- CALIBRATION reuse explicitly treated as adaptive development evidence;
- future role split no longer misrepresented as restored independence;
- retention and stop rules frozen;
- selector and AUTO_SAFE remain separate later decisions.

## 27. Exact next authorized step

Do not run P1+P2 feasibility yet.

Materialize, sequentially:
1. exposure ledger;
2. role split manifests;
3. bundle contract;
4. target/matching contract;
5. protected-invariants contract;
6. preflight.

Only after these artifacts are frozen may a separate explicit decision authorize the single P1+P2 feasibility measurement on C_F.

Reserved/internal datasets remain closed.
