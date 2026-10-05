# AT0-EN V2.6 R4.2 — First Training Launch Technical Failure Freeze V1

Date: 2026-10-05
Status: TECHNICAL PRE-TRAINING FAILURE / SCIENTIFIC TRAINING NOT CONSUMED

Run:
`37343356342`

Artifact:
`11360130441`

Artifact digest:
`sha256:746ad34c4f047bb3e0c2fde5a0f0875deb43d3789ecc3af27f79e5ecb3988eee`

Succeeded before failure:
- frozen runtime installation
- exact model acquisition and hash verification
- exact EBM train/dev acquisition and hash verification
- runtime/trainer identity freeze

Failure:
`FileExistsError: ... /r42/out`

Root cause:
the workflow created `$RUNNER_TEMP/r42/out` before invoking a trainer that intentionally requires a fresh non-existing output directory via `mkdir(..., exist_ok=False)`.

Scientific boundary:
- base model conversion/loading: NOT REACHED
- training: NOT STARTED
- calibration inference: NOT STARTED
- EBM/COVID/AD test inference: NOT RUN
- FactPICO: NOT USED
- consumed 60-RCT holdout: NOT USED

Classification:
`TECHNICAL_LAUNCH_FAILURE_BEFORE_SCIENTIFIC_ATTEMPT`

Authorized correction:
remove only the premature workflow creation of the output directory.

Frozen and unchanged:
- model revision/files/hashes
- training and dev files/hashes
- seed
- hyperparameters
- label schema
- calibration thresholds/rules
- anti-degeneracy conditions
- stop boundary

A single technical retry is permitted because no scientific training/calibration occurred.
