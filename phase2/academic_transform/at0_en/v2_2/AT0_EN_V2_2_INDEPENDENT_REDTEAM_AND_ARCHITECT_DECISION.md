# AT0-EN V2.2 — Independent Red-Team Closure and Higher-Model Architecture Decision

Date: 2026-10-03  
Decision: **MODIFY / NO NEW LIVE INFERENCE / V2.3 OFFLINE REQUIRED**

## 1. Scope and provenance

This review used **no new model inference**.

Frozen predecessor:
- AT0-EN V2.1 live run: `37123963805`
- V2.1 artifact: `11275534001`
- V2.1 artifact SHA-256: `842a9ff304c3ed9c854790ac8f205bfe156289b007b556cd06fa4aa19b609326`

Initial V2.2 canonical checkpoint:
- `d51ac2547ad05344a17a5ab828bc5ba05e772519`

A concurrent repository update appeared after that checkpoint:
- commit: `eeb6b2eec68a33e2b91a2d9e5380010ccc4705d0`
- message: `Harden V2.2 validator after independent false-negative red-team`
- changes:
  - added EN03 mechanism-conflation detection;
  - added EN04 assertion-weakening detection.

This concurrent change was preserved. The independent red-team described below tested the **hardened** validator, not the earlier weaker copy.

Hardened validator SHA-256 used by both subsequent workflows:
`749aa234e223faaecbb5e434ed4d165f856c6362fb9931ed560f657d77a80c2c`

## 2. Current frozen-output replay after hardening

Workflow:
- run: `37130414885`
- trigger commit: `1a2efe73556ea0958b4ab5df9d856fae2c635144`
- conclusion: SUCCESS
- artifact: `11276398612`
- artifact digest: `sha256:1e520e9b479854689c662dd2eef09eab0312716416b8df1958afde202a41b200`

Replay hashes:
- detail JSONL: `af0b54f3994628256258dc6093edfd411e703fabb95d41cce7a1a8a4a9e8af7e`
- summary JSON: `f183469580d26cf75c9a188853284320688c2c52c24e0abd348d95678b79cca8`

Current automatic dispositions across the 48 frozen V2.1 cells:
- PASS_CANDIDATE: **30**
- REJECT: **5**
- REVIEW: **8**
- REVIEW_ESCALATED: **1**
- UNAVAILABLE: **4**

Compared with the pre-hardening V2.2 replay:
- PASS_CANDIDATE: 32 → 30
- REJECT: 3 → 5
- two real false negatives were removed:
  1. MODEL_A EN04 DIRECT: asserted reduction weakened to association;
  2. MODEL_B EN03 PLANNED: edge aggregation incorrectly generalized over batching studies.

This is a methodological improvement, not a new model-performance result.

## 3. Independent counterfactual red-team

Workflow:
- run: `37130259582`
- trigger commit: `4ab44badeced0b0f8a847a9c65aef110ccc9bd1f`
- conclusion: SUCCESS
- artifact: `11276616582`
- artifact digest: `sha256:cee42205419c467dbecdeb0111dcc2109b996cb7855b2987693de5e169a2d960`

Red-team identities:
- script SHA-256: `577f182d2d3f56bad3446017cf5fde020aa7a2f510b9e3881e92132faed81972`
- detail JSONL SHA-256: `d29feba41d092774662a86af15e86f8a3fccf560a8f79c5e91ad797875c05421`
- summary SHA-256: `c00f763652e937a21f9b5662a4156e941765277b36a77a39d3fdcd4bdb2b5ad2`

Test design:
- 12 benign paraphrase controls;
- 24 counterfactual attacks, two per frozen case;
- attacks deliberately preserve lexical anchors while corrupting a protected relation;
- no attack was used to modify the validator before this run.

Results:
- benign controls: **12/12 PASS_CANDIDATE**
- benign false positives: **0/12**
- adversarial attacks correctly caught: **3/24**
- adversarial attacks escaping as PASS_CANDIDATE: **21/24**
- constructed-attack escape rate: **87.5%**

The 87.5% value is a diagnostic on a deliberately adversarial constructed set. It is not an estimate of real-world failure probability.

Caught attacks:
- EN02 interval decoy;
- EN03 mechanism conflation;
- EN10 measurement-rate decoy.

Escaped attack families included:
- negated/reversed scope while retaining the word `only`;
- modality strengthening;
- wrong cardinality with a decoy mention of the correct count;
- energy-direction reversal;
- citation swap inside one sentence;
- explicit contradiction after a correct-looking clause;
- association-direction reversal;
- delta reversal with negated correct wording;
- group/value swap with lexical decoys;
- method-order reversal;
- exclusion negation;
- causal contradiction;
- equation operator change;
- priority-direction reversal;
- imputation contradiction;
- duplicate-rejection negation;
- original-timestamp negation;
- parameter-freeze negation;
- metric-negation.

Conclusion: lexical presence plus local regex windows cannot serve as an automatic scientific-fidelity verifier.

## 4. Independent review of actual frozen outputs

The current hardened validator labels 30 real frozen cells PASS_CANDIDATE.

Higher-model manual semantic red-team identified one concrete live-output false negative:

### MODEL_A-EN01-DIRECT

Source:
`Continuous traffic observations can support faster identification of congestion.`

Candidate:
`...continuous data collection from roadside devices, facilitating faster identification of congestion...`

Issue:
the source expresses capability/possibility (`can support`), while the candidate asserts actual facilitation. This is a modality/claim-strength change. It must not be auto-accepted.

Higher-model overlay on the current 30 automatic PASS_CANDIDATE cells:
- confirmed bounded PASS candidates: **29**
- false-negative requiring REVIEW: **1**
- observed false-negative fraction within this tiny, post-hoc reviewed pass set: **1/30 = 3.33%**

This 3.33% is descriptive only and must not be generalized beyond these 30 cells.

The five automatic REJECT cells were all confirmed as defensible hard failures.

The eight automatic REVIEW cells were all defensible escalation cases. REVIEW is not an assertion that the text is wrong; several are borderline and may be accepted by a qualified reviewer. Therefore a conventional false-positive error rate is not assigned to REVIEW.

## 5. Why V2.2 cannot authorize auto-accept

V2.2 improved failure localization and caught multiple real V2.1 drifts, but it remains fundamentally lexical.

A protected scientific proposition is not a bag of keywords. It is a typed relation containing, as applicable:
- subject / entity;
- predicate / event;
- object / value;
- quantity and unit;
- comparison direction;
- time / baseline;
- population and scope;
- polarity / negation;
- modality / hedge;
- evidential strength;
- causal status;
- condition;
- citation edge;
- equation/operator identity;
- method ordering.

The counterfactual suite demonstrates that the present validator can see the right words while accepting the wrong relation.

Therefore:
- `PASS_CANDIDATE` from V2.2 is diagnostic only;
- no V2.2 result may trigger automatic manuscript acceptance;
- no new live generation experiment is authorized from this checkpoint.

## 6. Research alignment

### Scientific revision evaluation

Jourdan et al., ACL 2025, *Identifying Reliable Evaluation Metrics for Scientific Text Revision*:
https://aclanthology.org/2025.acl-long.335/

They report that common similarity metrics do not capture revision quality adequately, and that LLM judges are stronger on instruction following than correctness. Their hybrid-evaluation conclusion supports keeping task-specific scientific checks separate from writing-quality assessment.

### Counterfactual scientific reasoning

Dycke & Gurevych, TACL 2026, *Automatic Reviewers Fail to Detect Faulty Reasoning in Research Papers*:
https://aclanthology.org/2026.tacl-1.22/

Their controlled counterfactual framework directly supports the methodological choice made here: test whether a verifier reacts when the scientific relation is deliberately corrupted while surface form remains plausible.

### Evidence-aligned claim strength

James et al., Findings of ACL 2026, *RIGOURATE: Quantifying Scientific Exaggeration with Evidence-Aligned Claim Evaluation*:
https://aclanthology.org/2026.findings-acl.1699/

Their evidence-aligned treatment of scientific overstatement reinforces the need to model claim strength and evidential proportionality explicitly rather than through isolated trigger words.

### Scientific-writing evaluators

Şahinuç et al., ACL 2026, *Reward Modeling for Scientific Writing Evaluation*:
https://aclanthology.org/2026.acl-long.567/

Their multi-aspect evaluation framing supports separating scientific correctness, task criteria and writing quality instead of collapsing them into one score.

These papers motivate architecture choices. They do not prove the correctness of ACAD_PASS V2.3.

## 7. Higher-model decision

Decision:
**MODIFY / V2.2 DIAGNOSTIC-ONLY / NO NEW LIVE / NO HW1-EN**

Keep:
- English-first product architecture;
- reversible transactions;
- source immutability;
- minimal generation envelope;
- late deterministic packaging;
- separate DIRECT and PLANNED research arms;
- review-first disposition;
- no silent regeneration.

Reject as an auto-accept architecture:
- lexical-presence verification;
- sentence co-occurrence as citation binding;
- keyword windows as relation proof;
- any generic LLM judge as the sole verifier.

## 8. Exact next authorized phase — AT0-EN V2.3 OFFLINE RELATION-GRAPH VERIFIER

No model generation is authorized in V2.3.

### V2.3 source contract

Create a frozen `SOURCE_RELATION_LEDGER` for the 12 synthetic cases. Each protected assertion must be represented as typed records, for example:

- `ASSOCIATION(subject, object, direction, population, scope)`
- `QUANTITY(entity, value, unit, time, group, baseline)`
- `CLAIM_STRENGTH(predicate, modality, evidence_status)`
- `CAUSALITY(cause, effect, status)`
- `CITATION_SUPPORT(citation_id, claim_id)`
- `EQUATION(identity, operator_tree, variable_bindings)`
- `METHOD_STEP(step_id, order, precondition, exclusion)`
- `SCOPE(assertion_id, population, setting, time_window)`
- `POLARITY(assertion_id, positive|negative)`

Do not infer external scientific truth. The ledger represents what the source asserts.

### Candidate verification

1. deterministic exact invariants first: numbers, units, symbols, equations, citation IDs;
2. relation/argument binding;
3. polarity and contradiction;
4. direction/comparator;
5. modality and claim-strength compatibility in both directions;
6. scope/population/time restrictions;
7. citation-to-claim edges;
8. method order and exclusions;
9. new-proposition detection;
10. unresolved extraction → REVIEW, never PASS.

### Counterfactual generator

Generate tests from relation operators rather than hand-written keyword perturbations:
- negate;
- swap arguments;
- reverse comparator;
- change quantity/cardinality;
- rebind time/group/baseline;
- change equation operator;
- relax/reassign scope;
- strengthen or weaken modality;
- convert association↔causation;
- swap citation edge;
- reorder method steps;
- remove or invert exclusion;
- inject contradiction while preserving original wording as a decoy.

### Required pre-live gates

Before any new live inference is considered:
1. current 12 benign controls: 12/12 acceptable;
2. V2.2 REDTEAM_V1: **24/24 attacks must be caught**;
3. all 30 current automatic PASS_CANDIDATE V2.1 cells must receive a frozen relation-level adjudication, with the known EN01 modality drift no longer auto-passing;
4. a second fresh counterfactual suite must be created **after** V2.3 rules are frozen and used as a post-freeze red-team;
5. any unresolved scientific relation returns REVIEW;
6. no release/human-quality claim is inferred from these synthetic gates.

A new live protocol may be designed only after higher-model review of those results.

## 9. Status comparison

Versus the original V2.2 freeze:

**SCIENTIFIC UNDERSTANDING: IMPROVED**  
**VALIDATOR ROBUSTNESS ASSESSMENT: WORSENED**  
**OVERALL: MIXED, WITH A CLEARER REDESIGN PATH**

Improved:
- two real false negatives were already repaired by the concurrent hardening;
- current frozen replay is now traceable;
- independent counterfactual testing exposes systematic relation-blind failure modes;
- benign paraphrase controls show the problem is not simply universal over-rejection.

Worsened/new risk:
- 21/24 constructed relation corruptions escaped the hardened validator;
- one real live output still falsely auto-passes;
- case-specific regex additions risk an endless patch cycle and overfitting.

The next step is therefore structural, not another round of regex patches.
