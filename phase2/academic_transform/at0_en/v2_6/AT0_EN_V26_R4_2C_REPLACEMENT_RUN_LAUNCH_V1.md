# AT0 EN V2.6 R4.2C Replacement Run Launch V1

Date: 2026-10-06

## Durable pre-retry verification

- Active branch: `at0-en-v2.6-dev`
- Verified head before trigger: `b655341a55144407ea73d02c72e65442c2ce53cd`
- No replacement R4.2C train-calibration run already existed.
- Previous run `37451685278` remains preserved as a pre-training technical implementation failure.

## Replacement launch

- Trigger commit: `b70d40b3f86738c2cdcb1e7864fd507fd1eedde3`
- Workflow run: `37464774424`
- Workflow: `AT0 EN V2.6 R4.2C ONE boundary-consensus train calibration`
- Trigger head SHA: `b70d40b3f86738c2cdcb1e7864fd507fd1eedde3`
- Initial observed state: `IN_PROGRESS`

The workflow explicitly checks out branch `at0-en-v2.6-dev`, so this replacement run uses the corrected source-aligned trainer. The frozen R4.2C scientific protocol is unchanged.

## First observed step state

- job setup: PASS
- checkout: PASS
- Python setup: PASS
- frozen runtime installation: IN_PROGRESS
- scientific train/calibration step: NOT STARTED at this observation

## Interpretation

Engineering state: IMPROVED — a valid replacement run has been launched from the corrected durable branch state.

Scientific-performance state: NOT COMPARABLE — no replacement training/calibration result exists yet.

## Next authorized operation

Monitor run `37464774424`, inspect its terminal artifact and PROCESS_STATUS, freeze the result, and stop before any external test inference.
