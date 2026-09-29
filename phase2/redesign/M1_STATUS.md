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
- no M2 frontier-verifier run.\n\nTooling ready:\n- validate_m1_reviewer_response.py validates schema, case IDs and blinding declarations;\n- analyze_m1_agreement.py reports per-axis raw agreement, nominal Cohen kappa and nominal Krippendorff alpha;\n- derive_m1_disposition.py derives study disposition only after adjudication.

## Next legitimate action

Export the blinded pilot to two qualified Arabic reviewers. Their primary judgments must be locked before any historical/reference labels are revealed. The agent can validate returned JSONL and compute disagreement, but it must not impersonate the independent humans.

## Decision state

Arabic remains REVIEW-first. No new auto-accept capability has been established by M1 yet.
