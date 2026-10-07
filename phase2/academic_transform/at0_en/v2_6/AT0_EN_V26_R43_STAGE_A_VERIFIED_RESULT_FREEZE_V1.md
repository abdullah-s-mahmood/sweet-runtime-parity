# AT0 EN V2.6 — R4.3 Stage-A FIT-only Ancestors Result Freeze V1

Date: 2026-10-07
Status: STAGE_A_COMPLETE_VERIFIED; STAGE_B_NOT_YET_EXECUTED_AT_THIS_CHECKPOINT

## 1. Source identity
- Repo: `abdullah-s-mahmood/sweet-runtime-parity`
- Branch: `at0-en-v2.6-dev`
- Original Stage-A run: `37535183682`, success
- Stage-A head: `ad058bc856c280914158e005b07ffe6a0834aa13`
- Stage-A artifact ID: `11455753005`
- Stage-A artifact SHA256 digest: `f2a0352cc4668faf180c4486f496d5bf6ccfd0e39d57fe8144b1b55808d3c2b6`
- Final process: `COMPLETED`, 100%, no technical error
- Finished ~2026-10-07 01:49:57 UTC (04:49:57 Asia/Baghdad)

## 2. Independent physical artifact verification
- Read-only run: `37566322559`, SUCCESS
- Compact verification artifact: `11458734036`
- Compact artifact SHA256 digest: `0b873b366b1267cc86d29b49d60d7982ad65914a78e4011d003abd651a3184c7`
- Witness state: `R43_STAGE_A_COMPACT_IDENTITY_PASS`.
- Verification physically rehashed all 3 Stage-A model.safetensors files and matched the immutable Stage-A summary. No artifact substitution, missing checkpoint or prohibited pickle file.
- Original summary SHA256: `e5e4663bc03d0c67e947c209148b10f8f7eee93beb1bf415cf59b50ce2c161ab`
- Original status SHA256: `e8fd44e8fd1c753239469c1b4b91139cadc0a97a90dadbb8e58d9fd4fad1044b`

## 3. Frozen data identity
- TRAIN SHA256: `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`
- FIT/SELECT manifest SHA256: `fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`
- Converted BiomedBERT base SHA256: `3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68`
- FIT docs = 320, sentences = 1292, gold spans = 2371
- FIT gold P/I/C/O: 342/1038/144/847

## 4. Final fixed-epoch ancestors

### B_CANDIDATE
- fixed epochs 10
- global steps 1620
- final train loss `0.11106746030157938`
- final model SHA256 `4e4852b847be5bf64cd707ed62f770e13d64ee6becea3ce049f69bde220bfb05`
- model.safetensors bytes 435617620

### C_BOUNDARY
- fixed epochs 3
- global steps 486
- final train loss `0.27630300139203484`
- final model SHA256 `8c0848e798dd2b2409a81931b7bac496f88fceec2c8bd589e95a186d67dacebb`
- model.safetensors bytes 435605316

### C_TYPE
- fixed epochs 3
- global steps 447
- final train loss `0.17973474314815513`
- final model SHA256 `c7d5e4d2eb1632ac39c944e28232f8addff6c037b1ea80a09436a885101aed1a`
- model.safetensors bytes 437964800

These train losses are not SELECT/DEV precision or scientific gate outcomes.

## 5. Verified guards
- FIT-only training = true
- SELECT used for training = false
- historical DEV read = false
- test read = false
- other folds read = false
- FactPICO used = false
- consumed 60-RCT holdout used = false
- checkpoint selection = FINAL_FIXED_EPOCH_ONLY

## 6. Independent exploratory H0/H1 probes (not architecture selection)
- Run `37540851386` found H1 macro-F1 +0.0156412788 versus H0 on one FIT-only inner split.
- Run `37541116791` found H1 macro-F1 -0.0180306503 versus H0 on a different FIT-only inner split.
- Their rankings reverse; they cannot preselect the Stage-B winner.
- Detailed freeze: `AT0_EN_V26_R43_INDEPENDENT_H0_H1_PROBES_FREEZE_V1.md`.

## 7. Decision
`ACCEPT_STAGE_A_AS_PHYSICALLY_VERIFIED_AND_FREEZE`

Authorize the previously frozen single Stage-B H0-vs-H1 diagnostic. Its workflow must verify all ancestor artifact model hashes and guard/status identity again before scientific evaluation.

No parallel scientific run, alternative architecture, threshold modification, exposed historical DEV use, protected external test, FactPICO, or consumed holdout is authorized.

NEXT_ACTION:
`TRIGGER_EXACTLY_ONE_R43_STAGE_B_H0_VS_H1_DIAGNOSTIC_AND_STOP_AT_FROZEN_GATE`
