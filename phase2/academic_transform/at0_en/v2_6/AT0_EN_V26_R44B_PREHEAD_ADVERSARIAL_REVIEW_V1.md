# ACAD_PASS — R44-B B1 Pre-Head Adversarial Review V1

Date: 2026-10-08
Status: INDEPENDENT PRE-HEAD REVIEW COMPLETE / NO DISQUALIFYING LEAKAGE DEFECT FOUND / HIGHER-MODEL REVIEW RECOMMENDED BEFORE FIRST J0-J1 SCIENTIFIC RUN

## 1. Evidence reviewed

Durable upstream freeze:
- `AT0_EN_V26_R44B_B1_UPSTREAM_BANK_FREEZE_V1.md`
- R44-B run `37683637815`
- nested-bank artifact `11515434193`
- context-cache artifact `11510422862`

Code-level audit:
- `r44b_b1_preflight.py`
- `r44b_pair_aggregate.py`
- `r44b_base_context_cache.py`
- frozen protocol `AT0_EN_V26_R44B_B1_NESTED_PROTOCOL_FREEZE_V1.md`

External methodological check:
- Bates, Hastie & Tibshirani, JASA 2024, DOI 10.1080/01621459.2023.2197686.
- Contemporary span/biaffine nested-NER literature through 2025-2026 was checked for competing mechanisms and boundary-risk evidence.

## 2. Leakage/adaptation audit

### Upstream pair isolation
PASS.

For outer fold k and inner fold j:
- pair model training excludes both k and j;
- prediction-side j supplies only meta-training rows;
- outer fold k is absent from all upstream models that generate its meta-training evidence.

The aggregate physically verifies:
- 10 unique unordered pair banks;
- 20 logical inner edges;
- exact pair/document provenance;
- no VERIFY_INTERNAL;
- no old SELECT;
- no historical DEV/test/protected data;
- no head training.

### Outer evaluation
PASS as development-selection evidence.

Outer evaluation rows come from frozen R44-A OOF predictions where the upstream model excluded outer fold k.
They are not used in head fitting for that outer fold.

### Context cache
PASS.

The cache:
- uses immutable BiomedBERT;
- performs only per-sentence frozen forward inference;
- reads tokens but intentionally never reads labels;
- performs no cross-document fitting, normalization, calibration, adaptation, pseudo-labeling, or representation learning;
- is float32 and indexed by immutable token hashes;
- base model/design identities are fixed.

Therefore caching all DESIGN documents is not supervised/transductive leakage under this implementation.

## 3. Selection/evaluation caveat — MUST REMAIN EXPLICIT

The aggregated nested outer predictions will be used to:
- evaluate the fixed threshold set {0.80,0.85,0.90,0.95};
- determine whether J0 passes;
- otherwise determine whether J1 passes;
- freeze the selected architecture/threshold.

Therefore the resulting R44-B B1 numbers are:
`DEVELOPMENT MODEL-SELECTION EVIDENCE`

They must NOT be represented as a final unbiased/generalization estimate.

After architecture + threshold are frozen, a separate prospective evaluation is required.
The currently reserved `VERIFY_INTERNAL` remains unopened and is the natural next internal prospective gate if later authorized.

No threshold outside the frozen set may be introduced after observing B1 results.

## 4. Head architecture audit

J0:
- contextual start/end/interior/previous/following vectors;
- width, B-type, section and frozen scalar evidence;
- MLP 5-way NONE/P/I/C/O;
- 584,631 trainable parameters.

J1:
- exactly J0 plus class-specific biaffine start/end interaction;
- 667,836 parameters;
- +83,205 parameters over J0.

Selection rule remains scientifically appropriate:
1. if J0 passes all frozen gates, choose J0;
2. else if J1 passes, choose J1;
3. else STOP for causal diagnosis.

This protects against selecting J1 merely for a small numerical gain.

## 5. Disconfirming evidence / residual risks

1. Candidate-coordinate ceiling remains:
   the head can reject invalid candidates and correct type on exact coordinates, but cannot recover a gold span never proposed by B.

2. Raw-softmax confidence:
   primary B1 deliberately fits no temperature/isotonic calibration. Frozen thresholds therefore test raw model confidence only.
   Brier/ECE/reliability/risk-coverage must remain diagnostics and cannot change the frozen selection rule.

3. Class C:
   C support is much smaller than P/I/O. However every nested outer meta bank currently has C support 66-71, materially better than a single small HEAD_SELECT split.

4. Selection optimism:
   because architecture and threshold are selected from nested DESIGN evidence, B1 must not be promoted into a final validation claim.

5. Annotation/granularity uncertainty:
   some biomedical span disagreements can reflect annotation incompleteness/granularity, not purely model error. This affects later interpretation, not the mechanical exact-span frozen gate.

6. Boundary limitation:
   if B1 achieves high precision but operationally weak recall, boundary repair should be a separate prospectively frozen branch, not folded retrospectively into B1.

## 6. Parallelization audit for head phase

Safe maximum parallel plan:
- 5 outer folds x 2 architectures = 10 independent head-training jobs;
- all read immutable nested banks + immutable context cache;
- each has disjoint output namespace;
- no job consumes another head job;
- no shared mutable state;
- same frozen seed/schedule;
- aggregate only after all jobs complete.

This preserves scientific semantics while maximizing GitHub Actions utilization.

## 7. Independent verdict

`PROCEED_AFTER_HIGHER_MODEL_ADVERSARIAL_REVIEW_OR_EXPLICIT_BYPASS`

No defect was found that requires redesigning the frozen B1 protocol before head training.

However this is a consequential architecture/selection boundary and exactly matches the standing criterion for higher-model consultation:
- leakage-sensitive nested evaluation;
- J0 versus J1 model selection;
- threshold freeze before prospective VERIFY_INTERNAL;
- retained boundary-repair alternative.

Recommended next:
1. obtain one focused higher-model adversarial review using the prepared packet;
2. critically reconcile it against durable evidence;
3. if no material defect is identified, implement/freeze the 10-job head execution;
4. run J0/J1 once;
5. aggregate and apply the deterministic frozen decision rule;
6. freeze architecture + threshold;
7. STOP before VERIFY_INTERNAL access.


---

## 8. 2026-10-08 superseding clarification after higher-model review

The independent higher-model review returned:
`PROCEED_WITH_NONSCIENTIFIC_IMPLEMENTATION_FIXES_ONLY`.

No scientific redesign is authorized.

Corrections to this review:
- the 10 fold/pair computations are computationally separable, NOT statistically independent;
- shared training documents/fitted ancestors create dependence and folds must not be interpreted as independent replicates;
- context-cache computation is label-independent, but the frozen source JSON contains tags; the correct claim is `NO_LABEL_DEPENDENT_CONTEXT_COMPUTATION`;
- `VERIFY_INTERNAL` is historically exposed through earlier parent R4.3 FIT training/audits and split-statistic balancing, although it has not been used for R44 candidate-specific verification/tuning;
- run `37702502662` computed gradients on a small mixed meta/eval development mechanics sample but made no optimizer update and retained no trained state. Those objects/gradients MUST NEVER initialize the scientific run.

The scientific J0/J1 experiment remains prospectively unconsumed.

Before it may run, non-scientific executor closure must prove:
- fresh model/optimizer/scheduler/RNG per fold/head;
- meta-only optimizer updates;
- evaluation under `model.eval()` + `torch.no_grad()`;
- canonical manifest-hash recomputation;
- pinned source/artifact identities;
- complete probability serialization;
- exactly 1,942 aggregated outer probability rows per head;
- failure on missing/duplicate/nonfinite outputs;
- authoritative gold recall denominators P=271, I=829, C=115, O=677;
- synthetic correctness of NONE rejection, type correction, exact-boundary accounting, `>=` thresholds, all-class gates, lowest passing threshold and J0-first precedence;
- frozen calibration diagnostic definitions only, with no fitted calibration;
- no score-driven retry/checkpoint shopping.

Current verdict:
`PROCEED_ONLY_AFTER_I1_EXECUTOR_AND_I2_DOCUMENTATION_CLOSURE_PASS`.
