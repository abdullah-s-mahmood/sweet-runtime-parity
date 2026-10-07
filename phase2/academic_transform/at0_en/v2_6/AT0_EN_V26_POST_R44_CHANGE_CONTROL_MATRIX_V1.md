# ACAD_PASS — Post-R44 Change-Control Matrix V1

Date: 2026-10-07
Status: GOVERNANCE / NO ADDITIONAL SCIENTIFIC TRAINING

Purpose: ensure every important finding from R4.3/R4.4 is either implemented, explicitly conditioned on evidence, or explicitly deferred. No method may disappear silently.

## A. Mandatory before any R44-B head training

1. SOURCE semantics
- Use SOURCE_COMPATIBLE B-start entity inventory.
- Initial valid I-X = continuation metadata, not a new entity.
- Invalid initial I-X logged separately.
- Exact source evaluator parity frozen.

2. Realistic upstream supervision
- Use document-disjoint OOF B candidates from R44-A.
- Include proposals from goldless examples.
- Freeze false-positive taxonomy and high-confidence error distribution.
- Do not use in-sample B errors as the primary hard-negative source.

3. Upstream feature isolation
- Do not train a downstream head on fine-tuned Boundary hidden states generated in-sample.
- Use frozen label-independent BiomedBERT contextual vectors as the primary representation.
- OOF Boundary contributes only explicitly recorded held-out scalar evidence unless a future nested design proves otherwise.

4. Head target semantics
- 5-way target NONE/P/I/C/O.
- Exact-coordinate gold class overrides B proposed type so type correction is learnable.
- Wrong-boundary proposal remains NONE in the primary verifier; repair is a separate later stage.

5. Leakage-safe R44-B selection
- Ordinary CV over the same OOF bank is forbidden for clean model-selection estimation.
- Freeze either:
  B1 nested outer/inner document CV; or
  B2 prospectively disjoint UPSTREAM_META_TRAIN / HEAD_SELECT.
- Choice only after R44-A bank audit and without VERIFY_INTERNAL/old SELECT.

6. Calibration separation
- Representation/head fitting, calibration, and selection must be isolated.
- Report multiclass Brier, ECE, reliability, risk-coverage.
- No posthoc threshold expansion on exposed labels.

7. Evaluation invariants
- Exact span + exact class remains primary scientific gate.
- Deduplicate candidate coordinates before counting if any future generator can produce duplicates.
- Emit semantic mode, per-class entity inventory, continuations, invalid BIO runs and provenance.

## B. Mandatory immediately after R44-A aggregate

Audit:
- candidate rows;
- coordinate and typed candidate ceilings;
- per-class P/I/C/O coverage;
- NONE/P/I/C/O target ratio;
- FP taxonomy;
- goldless candidate errors;
- B confidence TP vs FP distributions;
- BIO violation breakdown with valid continuation separation;
- fold variability;
- class C support;
- model hashes / access guards;
- aggregate inventory P271/I829/C115/O677 and 256 DESIGN docs.

Then STOP and freeze the R44-B protocol. No head training before this audit.

## C. Conditional changes — execute only if measured mechanism warrants

1. Boundary repair (BOPN / Locate-and-Label style)
Trigger:
- substantial same-type wrong-boundary errors;
- local offset repairability is high;
- corrected verifier precision is already acceptable or separable.
Do not apply repair to spurious/no-overlap candidates.

2. Section/discourse context
Trigger:
- I/C/O confusion persists after corrected verifier;
- source section provenance remains deterministic;
- ablation is prospectively frozen.
Possible approaches: section embedding, document-level contextualization.

3. Stronger span interaction
Trigger:
- corrected simple J0 underfits on clean OOF supervision;
- H1/biaffine increment is insufficient;
- remaining errors show pair/interior interaction mechanism.
Candidates: triaffine, GlobalPointer/grid, span-pair scorer.

4. Stronger biomedical encoder / GLiNER-BioMed / OpenBioNER-v2
Trigger:
- representation error persists after supervision repair;
- comparison is prospectively frozen and ontology-aligned.

5. FinePICO / semi-supervised or weakly supervised augmentation
Trigger:
- labeled-data scarcity / class C support is the limiting factor;
- pseudo-labeling quality and contamination safeguards are separately validated.

6. LLM teacher / adjudication helper
Trigger:
- used only for candidate/support/adjudication assistance with provenance;
- never treated as ground truth without an evidence contract.

7. Annotation ambiguity / incomplete reference handling
Trigger:
- high-confidence gold-absent spans systematically look plausible under source guidelines.
Action:
- flag ambiguity/review; preserve frozen exact gate; do not silently relabel benchmark outcomes.

## D. Production-oriented mandatory later

- Accept / Review / Reject or abstain policy.
- Evidence span offsets and exact substring restoration.
- Reversible/versioned decisions.
- Calibrated risk-coverage.
- Separate scientific benchmark metrics from downstream safety/utility.

## E. Explicitly forbidden now

- opening VERIFY_INTERNAL during R44-A;
- old R4.3 SELECT tuning;
- historical DEV/test/other folds/protected tests;
- concurrent scientific training;
- architecture/model zoo before the OOF bank is understood;
- threshold shopping;
- seed shopping;
- retroactive rewriting of R4.3 evidence.

## F. Forecast gates

After R44-A:
1. If OOF native errors are abundant and structurally similar to R4.3 unseen-document errors -> proceed to leakage-safe joint verifier.
2. If OOF B collapses catastrophically -> first diagnose upstream generalization/capacity/data size before verifier training.
3. If OOF candidate recall ceiling falls below the required recall floor for any class -> candidate-generation/repair becomes a prerequisite.
4. If class C support becomes too sparse -> stop and redesign sampling/validation before fitting a head.
5. If fold-to-fold variance is very high -> prefer stronger nested evaluation / uncertainty reporting over a single head-selection split.

This matrix is binding as a continuity checklist, not an authorization to execute all branches automatically.
