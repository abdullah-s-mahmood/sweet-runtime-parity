# AT0-EN V2.4 — GATE C Final Untouched End-to-End Protocol V1

Date: 2026-10-03
Status: FINAL / FROZEN-PENDING-INTEGRITY / HOLDOUT UNOPENED

## 1. Evaluation scope

Gate C is the first untouched authentic end-to-end evaluation of the frozen V2.4 verifier pipeline.

It evaluates fidelity of candidate academic text relative to:
- the frozen source passage;
- explicitly allowed local context;
- source-contained scientific relations and evidence.

It does NOT establish:
- external scientific truth beyond the supplied source/context;
- full-document understanding when evidence lies outside the allowed context;
- production readiness of all ACAD_PASS modules;
- reliability of a live transformation generator.

## 2. Frozen verifier prerequisite

Pipeline freeze must remain exactly the canonical PRE-GATE-C identity.

Canonical freeze run:
`37150864483`

Artifact:
`11284520199`

Artifact SHA-256:
`74f765f614b616da2eb101c30d669de0c0931b304a377944be2a4039fe5a844c`

Any runtime modification creates a new pipeline version and invalidates direct comparison with the current Gate C protocol.

## 3. Independent source design

Independent source clusters:
**80 original studies/papers**

Five domains:
1. Computer Science / Engineering
2. Biomedical / Life Sciences
3. Physical / Materials Sciences
4. Environmental / Earth Sciences
5. Social / Behavioral Sciences

Allocation:
**16 independent studies per domain**

Within each domain:
- target 8 sources first publicly available in 2026;
- target 8 older unseen sources;
- record first public availability, including preprints;
- diversify subdisciplines, venues and prose type;
- include methods/results/discussion;
- do not select only short/easy claims.

Independence rule:
- one original study/paper = one source cluster;
- multiple excerpts, versions, preprints, conference/journal versions, mirrors or reproductions of the same study do not create new independent clusters.

Claim scope is restricted to the five tested domains.

## 4. Source eligibility and decontamination

Source must:
- be English peer-reviewed academic prose;
- have exact provenance;
- include sufficient frozen local context;
- contain at least one material scientific assertion/relation;
- not rely on malformed OCR;
- not have been used in ACAD_PASS development, examples, consultations, qualitative checks or research demonstrations.

Exclude:
- any paper/passage used in A/B gates;
- any paper/passage used in higher-model consultation evidence;
- any paper/passage used in B2.2 authentic qualitative checks;
- known duplicates/republications of included studies.

Training-set contamination of external pretrained models may be unknown and must not be represented as proven absent.

## 5. Allowed context

Before sampling:
- freeze the maximum source context available to the verifier;
- freeze the same or explicitly defined adjudicator context;
- record whether tables/equations/definitions/captions are included.

If a valid judgment requires information outside allowed context:
- do not silently infer it;
- classify the item under the preregistered REVIEW/eligibility policy.

Gate C is passage/context fidelity evaluation, not full-document verification unless the required context is actually supplied.

## 6. Transaction design

For every one of the 80 source clusters:

### Faithful transaction
Count: **80**
Target construction class: PASS_CANDIDATE

Must:
- be a non-trivial faithful academic rewrite;
- preserve critical scientific meaning, ownership, scope, modality, attribution and relations;
- permit reorganization/split/merge where meaning is preserved.

### Material-drift transaction
Count: **80**
Target construction class: REJECT

Where feasible:
- start from the faithful rewrite;
- introduce one dominant material change;
- avoid a visibly different writing style that leaks class.

Possible drift families:
- value/unit;
- population/group ownership;
- baseline/comparison;
- temporal relation;
- negation/scope;
- modality/evidential strength;
- causality vs association;
- citation/attribution;
- equation/symbol/coefficient binding;
- procedure/dependency/order;
- omission;
- unsupported new information.

### Ambiguity transaction
Count: **40**
Target construction class: REVIEW

Source clusters carrying REVIEW are selected before predictions under a balanced preregistered domain plan.

REVIEW is used only where allowed evidence cannot resolve a critical relation.
It is not assigned because the verifier is uncertain or because reviewers disagree.

Total transactions:
**200**

Primary inferential independence unit:
**original source study/paper**

## 7. Relation-family coverage

Diagnostic coverage target:
- at least 8 independent source clusters per critical relation family where naturally available;
- approximately 4 preservation tests + 4 material-drift tests from distinct sources where feasible;
- split/merge faithful equivalence appears in at least 8 independent sources.

A source may contribute to multiple relation-family diagnostics, with overlap reported.

Family coverage means the transaction actually tests preservation/change of the family, not merely that the feature appears in surrounding text.

No family-specific reliability claim is authorized from n≈8.

## 8. Candidate-construction separation

Candidate construction is separate from prediction.

Constructor must not receive:
- verifier predictions;
- implementation failure IDs;
- intended verifier behavior;
- post-hoc performance information.

If model-assisted:
- record model/version;
- freeze prompt/template;
- record all generation attempts;
- construction intent is never gold.

Before prediction:
- remove constructor notes;
- use neutral item identifiers;
- hide sibling pairing;
- hide construction class;
- hide drift family where that could reveal expected outcome.

## 9. Gold adjudication

A non-provisional Gate C requires qualified independent human adjudication.

Per transaction:
- Reviewer 1 independently labels.
- Reviewer 2 independently labels.
- Both are blind to:
  - verifier prediction;
  - intended construction class;
  - constructor rationale;
  - the other's initial judgment.
- A third qualified reviewer is used only if a material disagreement remains unresolved.

Required gold record:
- final outcome;
- source evidence spans;
- candidate evidence spans;
- critical assertion/relation change or preservation;
- materiality;
- ambiguity rationale if REVIEW;
- reviewer judgments;
- adjudication provenance.

Gold definitions:
- PASS: required scientific meaning is preserved.
- REJECT: a supported material change/omission/addition exists.
- REVIEW: allowed evidence cannot resolve a critical relation.

Reviewer disagreement caused by unclear instructions or inadequate expertise is not itself gold REVIEW.

Construction quotas do not force labels.
If a constructed candidate does not satisfy its intended class, apply a preregistered pre-prediction replacement/exclusion policy while preserving attempt history.

Without qualified independent human adjudication:
`GATE C = PROVISIONAL RESEARCH EVIDENCE ONLY`

## 10. Gold sealing and role separation

Before source sampling, freeze:
- adjudication guide;
- materiality definition;
- exclusion/replacement rules;
- thresholds;
- denominators;
- report weights;
- statistical plan;
- evidence-audit rules.

Before prediction:
1. freeze unlabeled inputs;
2. freeze final gold artifact;
3. store gold under access controls unavailable to prediction execution;
4. hash input and gold artifacts;
5. verify frozen pipeline hashes;
6. verify neutral identifiers and absence of class leakage.

Hashing establishes immutability, not secrecy; access separation is required.

Prediction runner must not have access to:
- gold;
- intended construction class;
- constructor notes;
- sibling mapping if it leaks class.

## 11. Prediction-first / label-second execution

Prediction:
1. run frozen verifier once on frozen unlabeled text/context;
2. no human intervention inside prediction;
3. no human-correct graph injection;
4. no partial-result inspection;
5. no selective retry;
6. freeze predictions, decisions and full evidence traces;
7. hash prediction artifact.

Evaluation:
8. reveal already-frozen gold only after prediction artifact hash exists;
9. run frozen scorer once;
10. keep invalid/missing outputs in denominators and report;
11. preserve every failure.

Any post-reveal gold correction:
- is versioned;
- preserves the original result;
- includes sensitivity analysis;
- does not restore untouched status.

## 12. Gate C progression thresholds

### Non-compensatory safety

Gold REJECT -> automatic PASS:
**0/80**

Gold REVIEW -> automatic PASS:
**0/40**

Critical silent scientific error:
**0**

Unsupported critical evidence used to justify automatic PASS/REJECT:
**0**

No other metric compensates for failure here.

### Usability

Faithful safe automatic acceptance:
**>=60/80 = 75%**

Decisive material-drift REJECT:
**>=60/80 = 75%**

Exact REVIEW preservation:
**>=36/40 = 90%**

### Evidence fidelity

For every critical automatic PASS/REJECT:
- evidence reference completeness: **100%**
- semantic support of the cited evidence: **100%**
- linkage to recorded decision path: **100% when the runtime records such linkage**

Trace presence alone is not treated as proof of causal faithfulness.

### INVALID_VERIFICATION

INVALID_VERIFICATION:
- remains a separate outcome;
- is never counted as success;
- remains in denominators/reporting;
- cannot be silently excluded.

## 13. Required metrics

Report:
- full confusion matrix;
- automatic PASS selective precision;
- faithful safe automatic acceptance/coverage;
- REJECT->PASS escape;
- decisive material-drift REJECT rate;
- REVIEW recall;
- REVIEW->PASS rate;
- INVALID_VERIFICATION rate;
- overall outcome accuracy;
- evidence completeness/support/path-linkage metrics;
- source-level paired success:
  `faithful accepted AND paired drift rejected`;
- domain breakdown;
- relation-family breakdown;
- exact numerators/denominators.

Selective precision must be interpreted relative to the artificial Gate C class mixture and must not be directly transferred to production prevalence.

## 14. Statistical reporting

Primary inferential unit:
**original source study/paper**

For non-boundary metrics:
- cluster bootstrap whole source clusters;
- bootstrap within domain/stratum;
- preserve frozen domain weights;
- report 95% intervals.

Do not bootstrap individual transactions as independent observations.

For zero-event safety metrics:
- do not report naive bootstrap [0,0];
- under independent Bernoulli assumptions, report one-sided exact binomial upper bounds:
  `U = 1 - 0.05^(1/n)`

Illustrative:
- 0/80 -> ~3.68% upper 95% bound
- 0/40 -> ~7.22%
- 0/8 -> ~31.23%

Do not pool REJECT->PASS and REVIEW->PASS as 120 independent observations.

For a general critical-error view, additionally report a source-cluster indicator:
`any critical error occurred in any transaction from this source`.

Domain/family subgroup results are diagnostic at these sizes.

## 15. Gate C result classes

`PASS_GATE_C_RESEARCH_PROGRESSION`
requires:
- every non-compensatory safety gate passes;
- faithful safe acceptance >=75%;
- decisive material-drift REJECT >=75%;
- REVIEW preservation >=90%;
- required evidence-fidelity gates pass.

`MIXED_GATE_C_RESEARCH_ONLY`
- safety passes;
- one or more usability/ambiguity gates fail.

`FAIL_GATE_C_SAFETY`
- any dangerous automatic PASS;
- any critical silent scientific error;
- unsupported critical evidence used to justify an automatic critical decision.

`INVALID_GATE_C_EVALUATION`
- pipeline mismatch;
- gold leakage;
- sealing/role-separation failure;
- protocol violation;
- inadequate gold integrity.

## 16. Strong-Adoption Validation boundary

Gate C is a research-progression benchmark, not sufficient proof of:
- >=99% selective precision;
- <1% error;
- production readiness;
- full-document fidelity.

Later strong-adoption targets:
- adversarial automatic acceptance: 0%
- critical silent scientific errors: 0
- automatic-PASS selective precision: >=99%
- authentic in-domain safe automatic acceptance: >=90%
- end-to-end decision accuracy: >=95%
- critical relation/ownership correctness: 100%
- critical evidence/provenance completeness: 100%

Under simple independent Bernoulli assumptions:
- zero errors require at least **299 independent decisions** for a one-sided 95% upper error bound below 1%.

The independence unit must match the claim:
- PASS precision claim -> independent automatic PASS decisions from target-use distribution;
- adversarial escape claim -> independent drift/adversarial sources;
- per-domain guarantees -> substantially larger per-domain evidence.

Do not stop data collection because an interim successful window appears.
Freeze sample size or a valid stopping rule in advance.

## 17. Eight conditions before any holdout source is opened

1. Freeze evaluation scope and allowed context.
2. Freeze 80-study sampling design, temporal mix, de-duplication and prior-exposure exclusions.
3. Freeze family coverage matrix, REVIEW allocation and candidate replacement policy.
4. Confirm qualified adjudicators and freeze adjudication/materiality guide.
5. Freeze role separation, access permissions and neutral identifiers.
6. Re-verify the full frozen pipeline/runtime/settings and no human-in-loop prediction.
7. Freeze thresholds, denominators, statistical plan, evidence-audit definitions and reporting weights.
8. Freeze one-shot policy for failures, exclusions, gold corrections and full result publication.

Until all eight are satisfied:
**NO GATE C SOURCE SAMPLING OR OPENING IS AUTHORIZED.**
