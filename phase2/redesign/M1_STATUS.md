# M1 Status

Date: 2026-09-30

## Current state

M1 — Edit Contract & Independent Labeling Protocol is ACTIVE.

Completed:
- fresh research/brainstorming start;
- ACAD_PASS Edit Contract v1 frozen for pilot;
- machine-readable M1 label schema;
- independent two-reviewer + adjudicator protocol;
- deterministic 24-case blinded pilot materialized from already-consumed Nahw surgical evidence;
- no QALB15 TEST, reserved/sealed data, or fourth slice consumed.

Not completed:
- no independent human Reviewer A labels;
- no independent human Reviewer B labels;
- no adjudication;
- no inter-annotator agreement report;
- no main M1 queue yet;
- no M2 frontier-verifier run.

Tooling ready:
- validate_m1_reviewer_response.py validates schema, case IDs and blinding declarations;
- analyze_m1_agreement.py reports per-axis raw agreement, nominal Cohen kappa and nominal Krippendorff alpha;
- derive_m1_disposition.py derives study disposition only after adjudication.

## Next legitimate action

Export the blinded pilot to two qualified Arabic reviewers. Their primary judgments must be locked before any historical/reference labels are revealed. The agent can validate returned JSONL and compute disagreement, but it must not impersonate the independent humans.

## Decision state

Arabic remains REVIEW-first. No new auto-accept capability has been established by M1 yet.


## M1-A expert-grounded path — 2026-09-30

Because two independent Arabic reviewers are not currently available, M1 now includes an expert-grounded bootstrap substage.

Pre-registered:
- fresh research start;
- adversarial brainstorming;
- QALB14 TRAIN+DEV only (already consumed);
- frozen Nahw development targets only;
- evidence-tiered partial labels;
- no arbitrary wrong/unnecessary synthesis;
- no QALB15, TEST, reserved/sealed material.

Files:
- M1A_RESEARCH_START.md
- M1A_BRAINSTORM_START.md
- M1A_EXPERT_GROUNDED_PROTOCOL.md
- M1A_EXPERT_EVIDENCE_SCHEMA.json
- m1a_build_expert_bootstrap.py
- workflow: phase2-m1a-expert-bootstrap.yml

The original 24-case blinded project pilot remains preserved as M1_LOCAL_PROJECT_CHALLENGE_SET; it is not promoted to human gold.


## M1-A v1 result and v1.1 redesign

v1 run 36640207701: NOT_READY.
- 20,380 changed QALB14 TRAIN+DEV lines
- 19,758 reconstructable multi-edit lines
- only 48 naturally unchanged raw lines
- sole failed gate: source==reference >=100
- no forbidden/test data read; no raw QALB text persisted

The threshold was not reduced. M1-A v1.1 is pre-registered with a corrected evidence definition:
- CLEAN_REFERENCE_KEEP from expert-corrected references;
- ERRONEOUS_SOURCE_KEEP from changed raw sources;
- independent professional ZAEBUC TRAIN evidence;
- independent A7'ta expert-book evidence with 20% reserved for later M2 validation.

See M1A_V1_TO_V11_CHANGELOG.md and M1A_EXPERT_GROUNDED_PROTOCOL_V11.md.
