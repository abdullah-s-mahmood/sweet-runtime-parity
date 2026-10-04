# ACAD_PASS — Gate C External Human-Gold + Metamorphic Protocol Amendment V1

Date: 2026-10-04
Status: FROZEN FOR PRE-EXECUTION REVIEW / NOT EXECUTION-AUTHORIZED

## 1. Purpose

This amendment defines an alternative research-progression validation route for the frozen AT0-EN V2.4 verifier.

It does **not** delete, overwrite or retrospectively modify:

`GATE_C_PROTOCOL_FINAL_V1.md`

The original 80-study / newly-human-adjudicated Gate C remains:
- frozen;
- unopened;
- scientifically valid as a bespoke future option;
- not currently required for the next research-progression decision.

The alternative route is:

`Gate C-EXT + Gate C-META`

where:

- `Gate C-EXT` = multiple independent published human/expert-gold benchmarks with dataset-specific construct contracts;
- `Gate C-META` = deterministic ACAD_PASS-specific metamorphic relation testing with preregistered validity conditions.

## 2. Replacement scope

This amendment replaces the requirement for **newly recruited human adjudicators now** only for the next research-progression gate.

It does not establish:
- fresh bespoke human adjudication;
- deployment prevalence;
- universal academic-domain coverage;
- full-document meaning preservation unless directly measured;
- production readiness;
- >=99% general selective precision;
- <1% general critical-error risk.

Residual human adjudication status:

`DEFERRED — CONDITIONALLY REQUIRED FOR UNCOVERED CLAIMS`

If a necessary claim is not represented by valid external human-gold or deterministic oracle evidence, ACAD_PASS must either:
1. narrow the claim; or
2. run a targeted residual human study for that gap.

## 3. Frozen runtime prerequisite

The canonical AT0-EN V2.4 runtime remains frozen.

Canonical pre-Gate-C freeze:
- run: `37150864483`
- artifact: `11284520199`
- artifact SHA-256:
  `74f765f614b616da2eb101c30d669de0c0931b304a377944be2a4039fe5a844c`

Any semantic runtime change creates a new pipeline version.

External adapters may:
- select eligible records;
- normalize transport/format fields;
- expose source/candidate/context;
- map labels only where semantic equivalence is explicitly demonstrated;
- calculate metrics.

External adapters may **not**:
- add a new semantic classifier;
- repair verifier output;
- infer missing gold;
- use gold rationale to alter prediction;
- hide invalid or failed predictions.

## 4. Evidence hierarchy

External evidence is evaluated by construct, not by dataset count.

A benchmark contributes independent support only to the extent that:
- its human/expert labels directly support the measured construct;
- its source/example clusters are not duplicated elsewhere;
- the adapter does not strengthen the label meaning;
- its evaluation unit and statistical dependence are recorded.

Two datasets derived from the same underlying examples do not automatically provide two independent pieces of evidence.

## 5. HARD GATE H1 — Scientific transformation fidelity

Goal:
test authentic scientific transformation fidelity using qualified human/expert judgments.

The final frozen H1 package must contain:

### H1-A — direct scientific transformation evidence

At least one eligible source from:
- CLEF SimpleText 2025 manually annotated real system submissions;
- qualified PLABA/TREC human faithfulness/completeness judgments;
- another directly equivalent scientific rewrite benchmark approved before execution.

Synthetic SimpleText distortion training data is not external human gold.

PLABA references are not automatically PASS examples. Eligibility must be defined from the exact human judgment contract.

### H1-B — independent scientific factuality evidence

At least one independent expert-annotated resource from:
- FactPICO;
- FaReBio;
- LongSciVerify;
- another directly equivalent resource approved before execution.

Preference:
select a resource whose construction/granularity differs from H1-A to reduce common-mode bias.

### H1 progression rule

H1 passes only if:
- each selected subtrack passes its frozen native/adapter contract;
- no confirmed critical silent error is hidden by aggregate averaging;
- source-level duplication/dependence is accounted for.

No H1 global average may compensate one subtrack failure.

## 6. HARD GATE H2 — Scientific claim/evidence fidelity

Primary resource:
`SciFact`

Construct:
scientific claim support/contradiction relative to specified evidence.

Rules:
- SUPPORT may map to PASS-like support only for the exact claim/evidence pair;
- CONTRADICT may map to REJECT-like contradiction only where the semantic direction is exact;
- absence/no-evidence must not automatically map to REVIEW;
- H2 does not establish full-rewrite completeness.

Exact split/version/eligible labels and metric thresholds must be frozen before execution.

## 7. HARD GATE H3 — Fine-grained relation fidelity

Primary resource:
`QASemConsistency`

Construct:
predicate-argument/relation support and localized hallucination.

Rules:
- evaluate at relation level where possible;
- retain native semantics unless an exact ACAD_PASS relation adapter exists;
- do not infer full-document PASS from relation-level success;
- track underlying source datasets to prevent overlap with other composite tracks.

Exact split/version/metric thresholds must be frozen before execution.

## 8. HARD GATE H4 — ACAD_PASS deterministic metamorphic validation

Purpose:
cover critical ACAD_PASS relation classes not adequately represented by external human-gold.

### 8.1 REJECT-guaranteed families

Subject to explicit applicability predicates:
- owner/value swap;
- group-label swap;
- explicit negation flip;
- MAY/CAN -> IS or equivalent unsupported modality strengthening;
- association -> causation;
- citation-owner swap;
- equation coefficient-variable swap;
- denominator change;
- baseline/comparator change;
- temporal-scope change;
- critical qualifier deletion;
- unsupported critical insertion.

### 8.2 PASS-preserving families

Only where formal/textual preconditions guarantee preservation:
- proposition-preserving split/merge;
- safe clause reorder without reference change;
- format-only transformation;
- frozen safe synonym substitution;
- citation-style change preserving attribution/ownership.

### 8.3 REVIEW families

REVIEW may be constructed only when:
- allowed evidence leaves a critical relation genuinely unresolved;
- no higher-precedence condition implies REJECT or INVALID_VERIFICATION;
- matched resolvable controls exist.

Do not treat:
- generic truncation;
- missing evidence;
- annotator disagreement;
as REVIEW by default.

### 8.4 Anti-degenerate controls

H4 must include matched controls that prevent success by:
- reject-all;
- review-all;
- pass-all;
- lexical shortcut.

### 8.5 META validity

Every metamorphic family must freeze:
- applicability predicate;
- transformation operator;
- expected outcome;
- prohibited edge cases;
- source-cluster identity;
- random seed if stochastic selection is used;
- exclusion policy.

A metamorphic case with uncertain oracle is invalid and must not be used as a hard-gate observation.

## 9. Diagnostic tracks

Initial diagnostic-only candidates:
- DeFacto;
- USB;
- PlainFact;
- QASPER;
- FENICE;
- TRUE or AggreFact, not both as independent aggregates;
- expert-edited 2026 scientific simplification corpus;
- additional long-document resources not already counted in H1.

A diagnostic track may be promoted to hard before execution only if:
- it fills a documented construct gap;
- its adapter contract is frozen;
- the promotion occurs before any verifier result is inspected.

A confirmed critical safety defect found in a diagnostic track remains reportable evidence and cannot be discarded because the track was diagnostic.

## 10. Overlap and independence control

Maintain an overlap manifest with, where available:
- DOI;
- PMID;
- arXiv ID;
- S2ORC/native dataset ID;
- source URL;
- raw source SHA-256;
- normalized duplicate-detection SHA-256;
- candidate SHA-256;
- parent dataset;
- derived dataset lineage;
- source cluster ID.

Rules:
- exact source+candidate duplicates count once;
- different candidates from one study may remain useful but are one source cluster for independence;
- SciFact material inherited by SciFact-Open is not independent;
- TRUE/AggreFact components cannot be double-counted with originals;
- shared PLABA/TREC source articles are clustered;
- QASemConsistency underlying examples must be traced to parent sources;
- derivatives of DeFacto are not independent of the parent examples.

## 11. Gold exposure and prediction separation

Public benchmarks are not secret holdouts.

Therefore ACAD_PASS must distinguish:
- public benchmark exposure;
- prediction/gold leakage during the current evaluation.

Before execution:
1. document known prior exposure;
2. freeze dataset versions and eligible IDs;
3. freeze adapters and evaluation code;
4. create prediction inputs without gold/rationale/correction fields;
5. freeze/hide evaluation joins where technically feasible;
6. run V2.4 predictions once;
7. hash prediction artifacts;
8. only then join frozen predictions to frozen labels for scoring.

If labels cannot be technically hidden from the operator because they are public/in-file, report that limitation explicitly; do not call the suite untouched-secret holdout validation.

## 12. Outcome semantics and native metrics

Do not collapse every track to PASS/REJECT/REVIEW.

Each track must define:
- native label semantics;
- eligible ACAD_PASS decision/output;
- exact adapter mapping, if any;
- metric;
- denominator;
- source-cluster unit;
- threshold;
- confidence interval or exact uncertainty treatment;
- INVALID/missing-output handling.

The original Gate C thresholds:
- faithful safe acceptance >=75%;
- decisive material-drift reject >=75%;
- REVIEW preservation >=90%;
may be reused only for truly equivalent outcome semantics.

They must not be translated mechanically into unrelated F1, correlation or span metrics.

## 13. Non-compensatory safety

Across all eligible mapped hard-gate cases:

- unsafe automatic acceptance: `0`;
- critical silent scientific errors: `0`;
- critical uncertainty promoted to automatic PASS: `0`;
- unsupported critical evidence used to justify an automatic critical decision: `0`.

Where the runtime provides traceable evidence references:
- critical evidence reference completeness: `100%`;
- semantic support: `100%` for audited critical automatic decisions.

A confirmed safety failure in any hard gate -> `NO_GO`.

No other metric compensates.

## 14. Global decision rule

Possible overall states:

### `PASS_GATE_C_EXT_META_RESEARCH_PROGRESSION`

Requires:
- H1 PASS;
- H2 PASS;
- H3 PASS;
- H4 PASS;
- every non-compensatory safety rule PASS;
- dataset/access/adapter/overlap evidence complete;
- no protocol-integrity invalidation.

### `MIXED_GATE_C_EXT_META_RESEARCH_ONLY`

Safety passes but one or more non-safety usability/coverage requirements fail.

No progression claim beyond the passed constructs.

### `FAIL_GATE_C_EXT_META_SAFETY`

Any confirmed unsafe automatic PASS, critical silent scientific error, critical uncertainty promotion, or unsupported critical decision evidence.

### `INVALID_GATE_C_EXT_META_EVALUATION`

Examples:
- frozen runtime mismatch;
- adapter changed after results;
- label leakage alters prediction path;
- hidden exclusion after result inspection;
- duplicate evidence counted as independent;
- invalid metamorphic oracle;
- version/split provenance cannot be established.

### `NOT_READY_GATE_C_EXT_META`

Required access, labels, adapters, overlap controls, thresholds, or evidence are not frozen before execution.

## 15. Statistical reporting

Primary independence unit depends on the construct and source lineage.

Where multiple cases share a source study/document:
- use cluster-aware reporting;
- do not report sibling cases as independent studies.

For zero-event safety:
- report exact numerators/denominators;
- report suitable one-sided upper confidence bounds where assumptions support it;
- do not interpret zero observed errors as zero population risk.

Across heterogeneous tracks:
- report native track results separately;
- do not pool incomparable denominators into one pseudo-N;
- do not produce a weighted overall accuracy unless a later preregistered target-use mixture justifies it.

## 16. Evidence reporting

For each hard track freeze:
- dataset/version;
- license/access status;
- citation;
- native schema;
- human/expert provenance;
- selected split/IDs;
- eligible/removed counts with reasons;
- source clusters;
- duplicate/overlap findings;
- adapter hash;
- runtime hash;
- prediction hash;
- score/evidence artifact hashes.

All exclusions remain visible.

## 17. Allowed claims after a future pass

Permitted claim template:

“Frozen ACAD_PASS V2.4 passed preregistered research-progression gates across multiple published human/expert-labeled scientific fidelity, claim-evidence and relation-level benchmarks, complemented by deterministic ACAD_PASS-specific metamorphic tests, within the stated datasets, constructs and metrics.”

Per-track performance may be reported with exact source counts and uncertainty.

## 18. Prohibited claims

Do not claim:
- original custom 80-study Gate C passed;
- fresh bespoke human adjudication occurred;
- universal academic fidelity;
- all meanings in full academic documents were preserved;
- production readiness;
- >=99% general automatic-PASS precision;
- <1% general error;
- human writing quality unless separately evaluated;
- repair-module success unless separately evaluated;
- every human-authored reference is fidelity gold;
- multiple wrapper datasets equal independent evidence.

## 19. Preconditions before any external-suite verifier execution

All must be PASS:

1. this amendment independently reviewed;
2. actual dataset artifacts/versions/access/licenses verified;
3. eligible splits/IDs and human-label provenance frozen;
4. dataset-specific adapter contracts frozen;
5. overlap/source-cluster manifest frozen;
6. metrics/thresholds/sample sizes/statistical treatment frozen;
7. META oracle contracts/cases/seeds/exclusions frozen;
8. runtime + adapter hashes frozen;
9. prior exposure and prediction/gold separation documented;
10. one-shot failure/exclusion/retest/full-report policy frozen.

Until all ten pass:

`EXTERNAL_SUITE_EXECUTION_NOT_AUTHORIZED`

## 20. Current state

Original custom Gate C:
`FROZEN / UNOPENED / PRESERVED`

New human recruitment:
`DEFERRED / NOT REQUIRED NOW`

V2.4 runtime:
`FROZEN / UNCHANGED`

External composite:
`PROTOCOL AMENDMENT V1 FROZEN FOR REVIEW`

External benchmark execution:
`NOT AUTHORIZED`

Exact next checkpoint:
`PRE-EXECUTION READINESS CONTRACT + INDEPENDENT REVIEW`
