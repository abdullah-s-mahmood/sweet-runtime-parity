# AT0-EN V2.6 R4.2 — Safe-path full training Run 4 timeout freeze V1

Date: 2026-10-05

Run: `37355935421`
Head: `6560caab57427fdde86009ad4cd0a0ed02d600a6`
Artifact: `11369815711`
Artifact digest: `sha256:85c5b10756576313fb3ae6c82d08c1039e6fead60fe41344f19f4a78b5dcdbad`

Classification:
`TECHNICAL_EXECUTION_TIMEOUT_AFTER_VALID_TRAINING_PROGRESS`

This is NOT a scientific model-performance failure.

Evidence:
- safe Flax conversion succeeded;
- all Flax base weights initialized `BertModel`;
- only classifier head was newly initialized;
- GitHub cancelled at the frozen 120-minute job limit;
- surviving output hashes prove `checkpoint-591` and `checkpoint-788`;
- approximately 197 steps/epoch means at least 4 full epochs completed;
- no final selected model or calibration summary exists;
- test sets, FactPICO and consumed 60-RCT holdout remained unopened.

Authorized recovery is execution-only:
- timeout 120 -> 360 minutes;
- scientific protocol unchanged;
- add `PROCESS_STATUS.json` heartbeat every 10 optimizer steps and at log/eval/save;
- record epoch, step, total steps, progress %, best metric/checkpoint and timestamps;
- enable unbuffered Python output;
- upload status plus checkpoint trainer-state JSON even on terminal interruption.

The incomplete run does not consume a valid completed scientific training result.
