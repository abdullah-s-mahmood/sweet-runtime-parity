# AT0-EN Offline Execution Report

Date: 2026-10-03

## Status

- PRESERVATION_GATE: PASS for four critical byte-verified artifacts (P1, P2_V2, P3, V4.2).
- HARNESS_STATUS: PASS_OFFLINE
- FIXTURES: 30/30 PASS
- LANGUAGE_PORTABILITY_AUDIT: 10/10 PASS
- EXPERIMENT_STATUS: NOT_RUN
- BLOCKER: MODEL_ACCESS / BUDGET AUTHORIZATION
- HUMAN_WRITING_STATUS: NOT_ASSESSED
- SCIENTIFIC_FIDELITY_STATUS: NOT_ESTABLISHED
- VOICE_STATUS: NOT_ASSESSED
- LENGTH_PRESERVATION_STATUS: POLICY_DEFINED / OFFLINE_DIAGNOSTICS_READY
- DETECTOR_ROBUSTNESS_STATUS: NOT_RUN
- DOCUMENT_FIDELITY_STATUS: NOT_RUN
- COMMERCIAL_USEFULNESS_STATUS: NOT_ASSESSED
- PRODUCTION_READINESS: NOT_ESTABLISHED

## Engineering findings

The first offline run produced 29/30 PASS and exposed a real scope-protection defect: a transaction could declare a wider scope than the pre-authorized paragraph and still pass source matching. The harness was repaired by making `authorized_scope` an independent invariant. After the repair, all 30 frozen fixtures passed. No live generation was repeated because none was started.

## Live matrix accounting

The 48 slots are preallocated and explicitly marked `NOT_RUN_MODEL_ACCESS`. No model call was made. The packet requires two already-authorized distinct model identities and a frozen cost ceiling. Neither is available through the current execution environment, so starting the live matrix would violate the execution contract.

## Arabic preservation

No new Arabic dataset was opened and no Arabic experiment was rerun. Local byte copies were verified against the recorded SHA-256 values for P1, P2 V2 Stage2, P3 V1 Stage2, and the V4.2 final measurement artifact.

## Recommendation

Adopt the architecture and offline AT0-EN harness in the repository now. Do not start HW1-EN or DR. Resume the live 48-slot matrix only when two exact authorized model identifiers and an explicit cost ceiling are available; otherwise return this blocked-but-engineering-ready state to the higher-model architect.