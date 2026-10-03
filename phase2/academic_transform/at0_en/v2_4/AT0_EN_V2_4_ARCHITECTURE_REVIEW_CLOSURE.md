# AT0-EN V2.4 — Architecture Review Integration Closure

Date: 2026-10-03
Status: CLOSED CHECKPOINT / ARCHITECTURE FROZEN / IMPLEMENTATION NOT STARTED

Higher-model verdict:
PROCEED_WITH_CHANGES

Project disposition:
- 8/8 required architecture changes accepted
- 5/5 top risks accepted as active design risks
- validation plan accepted
- do-not-do list accepted
- no recommendation rejected outright
- two clarifications added:
  1. INVALID_VERIFICATION is transaction-level, not a scientific judgment on candidate truth.
  2. deterministic token presence does not imply deterministic semantic ownership.

Final architecture:
phase2/academic_transform/at0_en/v2_4/AT0_EN_V2_4_FROZEN_ARCHITECTURE_V2.md

Final architecture commit:
14db09677fb6df90e6aa688601cfe071e8138ee6

Consultation response:
phase2/academic_transform/at0_en/v2_4/HIGHER_MODEL_CONSULTATION_RESPONSE_V1.md

Consultation-response commit:
758efae6af159a5fa9e9f50021357db1c069724c

Decision matrix:
phase2/academic_transform/at0_en/v2_4/CONSULTATION_DECISION_MATRIX_V1.md

Decision-matrix commit:
046f5aca0f4af85eb725c1bedf9f73dc31fc6245

Core frozen decisions:
- small task-specific Scientific Assertion Frame + Assertion Relation Graph;
- explicit relation ownership rather than flat attribute presence;
- deterministic and semantic verification lanes separated;
- source extraction frozen before independent candidate extraction;
- joint-context alignment only after both are frozen;
- independent coverage checks;
- bidirectional many-to-many alignment;
- four transaction outcomes: PASS_CANDIDATE / REJECT / REVIEW / INVALID_VERIFICATION;
- critical ambiguity blocks automatic PASS;
- every critical PASS/REJECT dependency requires a traceable minimal evidence rationale;
- no case-ID patching against consumed V2.3 holdout;
- no new untouched holdout before V2.4 pipeline freeze.

Fresh end-stage research reinforced:
- table-text verification needs evidence/rationale alignment, not label correctness alone;
- event relations such as coreference, temporal and causal relations remain challenging and require explicit treatment;
- factuality metrics remain brittle under paraphrase and dense claims.

Performance delta:
- experimental performance: UNCHANGED from V2.3 holdout;
- adversarial escape remains 9/24 = 37.5%;
- safe automatic acceptance remains 3/12 = 25%;
- no quantitative V2.4 performance claim is authorized.

Methodological delta:
IMPROVED — architecture now explicitly handles ownership, scope operators, evidence traces, coverage, independent extraction, many-to-many alignment, and invalid-verification state before implementation.

Next authorized stage:
AT0-EN V2.4 GATE 0 — OFFLINE SCHEMA / CRITICALITY / OUTCOME CONTRACT PROTOTYPE

Gate 0 only:
- define machine-readable schema;
- define criticality rules;
- define four outcome rules;
- create small fixed development reference material;
- no model inference required initially;
- no new generation;
- no HW1-EN;
- no untouched holdout.

Whole-system planning estimate remains approximately 20% ±5% because no validated V2.4 implementation exists yet.
