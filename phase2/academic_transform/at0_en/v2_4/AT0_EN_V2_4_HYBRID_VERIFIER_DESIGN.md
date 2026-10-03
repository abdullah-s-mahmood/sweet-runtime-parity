# AT0-EN V2.4 Hybrid Claim Verifier — Preregistered Design

Date: 2026-10-03
Status: DESIGN FROZEN / NO SEMANTIC MODEL INFERENCE YET

## Objective

Repair the precision/coverage trade-off exposed by V2.3 without weakening scientific safety.

The verifier is not an LLM judge and does not assign one holistic quality score. It verifies atomic source claims and candidate claims with multiple independent evidence channels.

## Evidence motivating the design

1. Hao & Wu, EMNLP Findings 2025, Programmatic Graph Reasoning:
   https://aclanthology.org/2025.findings-emnlp.293/
   Explicit graph reasoning improves transparency over implicit claim verification.

2. Godbole & Jia, ACL Findings 2025, Verify with Caution:
   https://aclanthology.org/2025.findings-acl.1175/
   Factuality metrics disagree, can misestimate factuality, and can be biased against highly paraphrased outputs. Domain-specific validation is required.

3. Javaji et al., IJCNLP-AACL 2025, CLAIM-BENCH:
   https://aclanthology.org/2025.ijcnlp-long.127/
   Scientific claim-evidence reasoning remains difficult; multi-pass and claim-by-claim verification improves results but costs more computation.

4. Kolli et al., Widening NLP 2025, Hybrid Fact-Checking:
   https://aclanthology.org/2025.winlp-main.19/
   Hybrid rule/graph/model pipelines can combine interpretability with broader semantic coverage and fallback behavior.

These sources motivate the architecture but do not prove ACAD_PASS performance.

## Layer A — Source assertion graph

The full immutable source text is authoritative. Frozen content_units are helper annotations only.

Each source assertion has:
- assertion_id
- source spans
- subject/entity
- predicate/relation
- object/value
- quantity and unit
- qualifiers: group/time/baseline/population/scope
- polarity
- modality/hedge strength
- causality class
- comparison direction
- citation links
- equation/symbol identity
- ordering/dependency
- uncertainty

No assertion may be silently dropped because it was absent from an older content-unit list.

## Layer B — Deterministic hard guard

V2.3 is retained only for checks with defensible deterministic semantics:
- exact quantities/units when mapped;
- equation/symbol identity;
- exact citation IDs and claim-citation bindings when spans are known;
- explicit group/time/baseline binding;
- explicit scope escape;
- explicit polarity contradiction;
- explicit order violation;
- forbidden document/scope writes.

A hard contradiction yields REJECT regardless of semantic-model score.

Absence of a lexical pattern does NOT by itself yield scientific REJECT when a semantic paraphrase may exist; it yields unresolved evidence for Layer C.

## Layer C — Semantic claim verification

Candidate semantic witnesses are frozen before inference; no threshold is selected after seeing blind results.

Initial research candidates:
1. Vectara HHEM-2.1-Open
   - task: source/summary factual consistency
   - approximately 0.1B parameters
   - license: Apache-2.0
   - model card: https://huggingface.co/vectara/hallucination_evaluation_model

2. MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli
   - task: NLI entailment/neutral/contradiction
   - trained on MultiNLI + FEVER-NLI + ANLI
   - license: MIT
   - model card: https://huggingface.co/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli

Neither candidate is yet accepted as a scientific oracle.

### Required directions

For every source assertion A_i:
- premise = candidate paragraph or aligned candidate span
- hypothesis = normalized source assertion A_i
- purpose = retention / contradiction check

For every candidate claim C_j:
- premise = source paragraph
- hypothesis = C_j
- purpose = unsupported-addition check

This bidirectional design prevents a candidate from passing merely because all source tokens appear somewhere.

## Layer D — Fusion / abstention

Provisional dispositions:
- HARD_REJECT: deterministic contradiction or protected invariant failure
- SEMANTIC_REJECT: independently supported contradiction/unsupported claim after calibration
- REVIEW: missing evidence, semantic disagreement, uncertain alignment, or threshold gray zone
- VERIFIED_FOR_REVIEW: hard guard passes and required bidirectional semantic checks pass
- KEEP: exact/no-change path

No automatic manuscript application is authorized by V2.4.

A semantic verifier may not override a deterministic hard contradiction.

## Calibration and frozen evaluation

Consumed development evidence:
- V2.1 48-slot outputs
- V2.2 known audit
- V2.2 24-attack independent red-team
- V2.3 known external gate
- V2.3 unseen holdout V1

These are no longer clean confirmation populations.

Before semantic inference:
1. freeze exact model revisions, model artifact hashes, tokenizer revisions, runtime and licenses;
2. freeze inference direction and label mapping;
3. freeze calibration population;
4. freeze thresholds using CALIBRATION only;
5. create/freeze a new untouched confirmation population after thresholds are locked.

### Required confirmation composition

At least:
- 60 safe scientific paraphrases spanning all 12 cases and multiple lexical/syntactic forms;
- 60 adversarial variants spanning quantity, binding, direction, polarity, modality, causality, scope, citation, equation, order and unsupported-addition errors;
- explicit critical subset for protected invariants;
- source-derived labels independently audited before opening model results.

Public NLI/factuality datasets may be used as auxiliary sanity checks but cannot replace the project-specific confirmation set.

## Primary V2.4 metrics

Report separately:
- critical unsafe auto-pass count
- overall unsafe auto-pass rate
- safe VERIFIED_FOR_REVIEW coverage
- safe hard-reject rate
- REVIEW/abstention rate
- assertion retention recall
- contradiction recall
- unsupported-addition recall
- per-relation-family performance
- witness disagreement rate

No single composite score decides safety.

## Preregistered gate for considering a later live generation experiment

On untouched confirmation:
- critical protected-invariant unsafe auto-pass: 0
- overall adversarial unsafe auto-pass: <=5%
- safe VERIFIED_FOR_REVIEW coverage: >=70%
- safe hard-reject rate: <=10%
- remaining safe uncertainty may route to REVIEW
- no post-hoc threshold changes on confirmation
- all model/runtime/hash identities reproducible
- independent higher-model review required after results

Failure of the gate means repair/redesign, not threshold weakening.

## Current authorization

Authorized now:
- model/revision/license/resource research
- source-free implementation of the hybrid harness
- deterministic tests
- construction and freeze of calibration/confirmation contracts
- preparation of model-download/hash workflow

NOT authorized yet:
- semantic model inference
- new generator inference
- HW1-EN
- detector robustness
- Arabic restart
- reserved Arabic data access
- V2.1 rerun

Return for higher-model review after V2.4 pre-inference package is frozen.
