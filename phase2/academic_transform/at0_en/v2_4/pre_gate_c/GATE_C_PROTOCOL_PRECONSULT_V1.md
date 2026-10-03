# AT0-EN V2.4 — PRE-GATE-C End-to-End Holdout Protocol V1 (PRE-CONSULTATION)

Date: 2026-10-03
Status: PRE-CONSULTATION DRAFT / NO HOLDOUT CREATED OR OPENED

## 1. Purpose

Gate C is the first untouched, authentic, end-to-end validation of the frozen V2.4 verifier pipeline.

It tests whether the complete verifier can correctly:
- automatically PASS faithful academic rewrites;
- REJECT material scientific drift;
- REVIEW genuinely unresolved/ambiguous cases;
- preserve evidence/provenance and critical relation ownership.

Gate C does NOT test a live transformation generator.
Candidate benchmark construction is separate from the verifier.

## 2. Pipeline freeze prerequisite

Pipeline identity must be frozen and integrity-verified before holdout source sampling or candidate construction.

Canonical pipeline-freeze run:
`37150864483`

Artifact:
`11284520199`

Artifact SHA-256:
`74f765f614b616da2eb101c30d669de0c0931b304a377944be2a4039fe5a844c`

Any change to a frozen runtime component after protocol freeze creates a new pipeline version and invalidates direct comparison with old Gate C predictions.

## 3. Proposed authentic source design

Proposed number of independent source clusters:
**80**

Domains:
1. computer science / engineering
2. biomedical / life sciences
3. physical / materials sciences
4. environmental / earth sciences
5. social / behavioral sciences

Proposed allocation:
**16 independent source passages per domain**

Source eligibility:
- English;
- peer-reviewed journal or conference paper;
- authentic academic prose;
- exact provenance recoverable;
- sufficient local context available;
- contains at least one material scientific assertion or relation;
- no malformed OCR;
- not previously used in ACAD_PASS development, consultation examples, research examples, A/B gates, or qualitative B2.2 checks.

Freshness/decontamination preference:
- prioritize recent 2026 publications not used in development;
- exclude exact papers/passages already cited or inspected during V2.4 development;
- source selection occurs only after pipeline and protocol freeze.

Do not inspect full candidate passages during pipeline development.

## 4. Proposed transaction design

For each of the 80 source clusters:

### Faithful transaction
One authentic faithful academic rewrite:
- gold class intended: PASS_CANDIDATE;
- non-trivial paraphrase/split/merge/organization change;
- scientific meaning and all critical bindings preserved.

Count:
**80**

### Material-drift transaction
One controlled material change:
- gold class intended: REJECT;
- preferably one dominant material fault;
- exact altered relation/slot documented for later adjudication.

Count:
**80**

### Ambiguity transaction
For 40 of the 80 source clusters, balanced across domains:
- deliberately insufficient/ambiguous context or relation;
- should require REVIEW rather than automatic PASS.

Count:
**40**

Total proposed transactions:
**200**

Primary statistical independence unit:
**source cluster, not transaction**.

Transaction-level metrics are reported, but confidence intervals and inferential statements must account for source clustering.

## 5. Coverage matrix

Across the holdout, require coverage of:
- quantitative value/unit binding;
- population/group ownership;
- baseline/comparison relation;
- temporal relation;
- negation/scope;
- modality/evidential strength;
- causality vs association;
- citation/attribution binding;
- equation/symbol binding;
- procedure/dependency/order;
- omission/new information;
- split/merge equivalence.

Families may overlap.

No single family should dominate the holdout.
Proposed minimum diagnostic coverage:
at least 8 independent source clusters exposing each critical family where naturally available.

## 6. Candidate construction separation

The benchmark-construction process must be separated from verifier execution.

Candidate constructor:
- receives source passage and permitted local context;
- does NOT receive verifier predictions;
- does NOT receive implementation-specific failure IDs;
- does NOT tune examples after verifier inspection.

Model-assisted candidate construction is permitted only if:
- model/version/prompt are recorded;
- output is independently adjudicated;
- the constructor's intended label is not treated as gold.

## 7. Gold adjudication

Gold is based on source/candidate meaning, not construction intent.

Preferred:
- two independent qualified reviewers;
- blind to verifier prediction;
- blind to each other's labels;
- disagreement adjudicated by a third reviewer.

Required gold fields:
- transaction outcome;
- critical assertion/relation changes;
- minimal supporting source span(s);
- minimal supporting candidate span(s);
- ambiguity reason for REVIEW;
- materiality/criticality.

If the preferred human-adjudication requirement cannot be met:
Gate C may be run only as PROVISIONAL research evidence and cannot support strong-adoption claims.

Report:
- raw agreement;
- Cohen's kappa or suitable agreement statistic where applicable;
- adjudication counts.

## 8. Sealed-label / prediction-first execution

Before verifier predictions:
1. Freeze unlabeled holdout inputs.
2. Freeze gold labels in a sealed artifact inaccessible to the implementation/prediction process.
3. Publish/hash both artifacts.
4. Verify pipeline-freeze hashes.

Prediction stage:
5. Run frozen verifier on unlabeled inputs.
6. Freeze predictions and all evidence traces.
7. Publish/hash prediction artifact.
8. No rerun or repair after predictions.

Evaluation stage:
9. Open/decrypt/reveal the already-frozen gold.
10. Score with a frozen scorer.
11. Preserve every failure.

Predictions first, labels second.

## 9. Proposed Gate C progression gates

These are progression gates, not final product-adoption proof.

### Non-compensatory safety
- dangerous REJECT -> automatic PASS:
  **0/80**
- gold REVIEW -> automatic PASS:
  **0/40**
- critical silent scientific error:
  **0**
- unsupported critical evidence trace used for PASS/REJECT:
  **0**

### Usability
Frozen architecture minimum:
- faithful safe automatic acceptance:
  **>=75% = >=60/80**

Proposed additional usability gate for consultation:
- material-drift decisive REJECT rate:
  **>=75% = >=60/80**

### Ambiguity handling
Proposed:
- exact REVIEW preservation:
  **>=90% = >=36/40**

### Evidence fidelity
- critical automatic-decision evidence-trace completeness:
  **100%**
- every critical PASS/REJECT relation must be independently supportable from frozen evidence.

## 10. Required reporting

Report separately:
- automatic PASS precision;
- safe automatic acceptance / coverage;
- adversarial automatic-PASS escape;
- material-drift REJECT rate;
- REVIEW recall;
- INVALID_VERIFICATION rate;
- overall outcome accuracy;
- critical evidence-trace fidelity;
- by-domain results;
- by-relation-family results;
- source-cluster bootstrap 95% CIs where appropriate;
- exact binomial interval for zero-event safety outcomes.

No aggregate score may compensate for a safety failure.

## 11. Proposed domain/family diagnostics

Always report domain and relation-family breakdowns.

Pre-consultation proposal:
- no separate domain/family threshold except zero dangerous automatic PASS;
- use domain/family results to detect concentrated failure;
- any concentrated critical failure blocks strong-adoption claims even if aggregate Gate C progression passes.

## 12. Strong-adoption targets after Gate C

Current ACAD_PASS strong-adoption targets remain:

- adversarial automatic acceptance: **0%**
- critical silent scientific errors: **0**
- automatic-PASS selective precision: **>=99%**
- authentic in-domain safe automatic acceptance: **>=90%**
- extracted-graph/end-to-end decision accuracy: **>=95%**
- critical relation/ownership correctness: **100%**
- evidence/provenance completeness for critical decisions: **100%**

Gate C with 80 independent source clusters is NOT by itself sufficient to statistically establish a true <1% error rate.

For a later independent strong-adoption study, under simple independent-binomial assumptions, approximately 299 zero-error independent decisions are needed for a one-sided 95% upper error bound below 1%.

If multiple transactions share a source, do not count them as independent for that claim.

## 13. Anti-leakage safeguards

- no holdout source text before pipeline/protocol freeze;
- no item-level repair after predictions;
- source/candidate/gold hashes frozen;
- exclude all development/example sources;
- prefer recent unseen publications;
- holdout gold sealed until prediction hash is frozen;
- record all exclusions under pre-registered eligibility rules;
- no replacement of difficult items because verifier fails them.

## 14. Result classes

Proposed:

`PASS_GATE_C_RESEARCH_PROGRESSION`
- all non-compensatory safety gates pass;
- safe acceptance >=75%;
- any finalized additional usability/REVIEW gates pass.

`MIXED_GATE_C_RESEARCH_ONLY`
- safety passes but usability or ambiguity handling fails.

`FAIL_GATE_C_SAFETY`
- any dangerous automatic PASS;
- any critical silent scientific error;
- unsupported critical evidence used to justify automatic PASS.

`INVALID_GATE_C_EVALUATION`
- pipeline identity mismatch;
- label leakage;
- broken sealing;
- protocol violation;
- insufficient gold integrity.

## 15. Current authorization

Authorized now:
- pipeline freeze;
- protocol design;
- higher-model protocol/construct-validity review.

Not authorized before protocol closure:
- source sampling;
- holdout candidate construction;
- gold labeling;
- prediction run;
- opening any untouched Gate C data.
