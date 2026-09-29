# M1 — Research and Brainstorming Start

Date: 2026-09-30  
Status: STARTED, consumed-evidence-only. No new benchmark slice consumed.

## Why M1 exists

The independent audit found that historical labels such as SUPPORTED_CORRECTION / PARTIAL_CORRECTION do not by themselves answer the product question. A locally supported edit can still be an incomplete repair, an independent residual error may remain, or a transformation can preserve surface tokens while changing semantic/scientific relations. M1 therefore fixes the decision contract before any new verifier is trained or tuned.

## Evidence constraints

- Phase 2 only.
- Historical labels remain immutable and are carried as provenance, not silently reinterpreted.
- QALB15 TEST, reserved/sealed data, and a fourth QALB15 TRAIN slice remain untouched.
- The first calibration material is drawn only from already-consumed Phase-2 evidence.
- Agent judgments are not independent human gold.
- M1 is a measurement redesign, not a claim that Arabic auto-accept has improved.

## Fresh research informing the annotation design

1. Östling et al. (LREC-COLING 2024), *Evaluation of Really Good Grammatical Error Correction*: motivates human post-editing and separate assessment of grammaticality, fluency, and meaning preservation.
2. Kobayashi et al. (TACL 2024), *Revisiting Meta-evaluation for Grammatical Error Correction (SEEDA)*: shows why edit-level and sentence-level judgments must not be conflated.
3. Jourdan et al. (ACL 2025), *Identifying Reliable Evaluation Metrics for Scientific Text Revision*: reports that LLM judges are useful for instruction-following but struggle with correctness, supporting hybrid/task-specific verification for scientific revision.
4. Vadehra et al. (HCI+NLP 2025), *Time Is Effort*: motivates post-editing effort and reviewer time as product metrics rather than precision alone.
5. Alabdullah et al. (VarDial 2026), *Ara-HOPE*: provides an Arabic human-centric precedent for an explicit error taxonomy and decision-tree annotation protocol.
6. Magdy et al. (Findings ACL 2026), *LQM*: supports multi-level Arabic error diagnosis spanning semantics, morphosyntax, orthography and other layers with severity-aware human annotation.
7. Goto et al. (TACL 2026), *Grammatical Error Correction Evaluation by Optimally Transporting Edit Representation*: reinforces edit-aware evaluation rather than source-dominated sentence similarity.

## Brainstorming result

The core M1 unit is not “is this candidate good?” but a reversible edit transaction evaluated on separable axes:
- necessity;
- local correctness;
- contextual correctness;
- edit-group completeness;
- residual-error relation;
- semantic fidelity;
- scientific fidelity;
- ambiguity/author intent;
- protected invariants;
- document/surface integrity.

Final disposition is derived from the axes and must not replace them.

## Immediate M1 plan

1. Freeze ACAD_PASS_EDIT_CONTRACT_V1.
2. Validate the labeling instructions on a 24-case blinded pilot drawn from consumed Nahw surgical edits.
3. Use two independent qualified Arabic reviewers plus adjudication; the agent may prepare, validate schemas, and analyze disagreement but does not count as an independent human reviewer.
4. Only after annotation reliability and taxonomy usability are acceptable, materialize the larger M1 consumed-evidence queue, including already-consumed QALB populations where text can be lawfully rehydrated from pinned non-TEST sources.
5. M2 begins only after M1 produces a stable human-reviewed contract.

## Stop conditions

Do not train a new CAD/verifier merely to improve historical metrics. If qualified reviewers cannot apply the contract consistently even with adequate context, narrow the scope/categories before modeling.
