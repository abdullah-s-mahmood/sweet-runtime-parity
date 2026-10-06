# ACAD_PASS CHAT HANDOFF — CANONICAL RESUME SNAPSHOT

Last updated: 2026-10-06
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Active branch: `at0-en-v2.6-dev`

> PURPOSE
>
> This file is the compact, canonical handoff for starting a new ChatGPT conversation without losing project state.
> In a new chat, paste this file (or ask ChatGPT to read it from the repository) and instruct it to continue ACAD_PASS from the exact current checkpoint.
>
> UPDATE RULE
>
> Update this file after every material checkpoint, including:
> - experiment/run result;
> - failure or negative evidence;
> - scientific/architecture decision;
> - implementation change;
> - protocol/threshold/data-boundary change;
> - important artifact/hash/commit;
> - user governance agreement;
> - exact next authorized step;
> - forbidden action boundary.
>
> This file complements, but does not replace:
> - `ACAD_PASS_MASTER_CONTINUITY.md`
> - `RESUME_HERE.md`
>
> If there is a discrepancy, inspect durable GitHub state first. The most recent verified commit/run/artifact outranks stale prose.

---

# 1. PERMANENT USER GOVERNANCE

## Sequential execution
- Never run project operations in parallel.
- Multiple operations are allowed only sequentially.
- Freeze evidence before moving to the next scientific checkpoint.
- Do not repeat one-shot experiments.
- UI/stream interruptions are not scientific failures.

## Deep reasoning / consultation
- Perform deep internal analysis, competing-hypothesis reasoning, disconfirming-evidence search, and external research when materially useful.
- Higher-model consultation is exceptional, not default.
- Use higher-model review only for irreversible/high-stakes scientific boundaries, unresolved construct-validity ambiguity, materially divergent scientific paths, or explicit user request.
- Objective: `BEST DEFENSIBLE RESULT, NOT FASTEST AGREEMENT`.

## Reporting
At material checkpoints report:
- `IMPROVED / WORSENED / MIXED / NOT COMPARABLE`;
- scientifically valid numeric change when possible;
- current stage completion;
- coarse project maturity/progress;
- blockers;
- exact next step.

## Progress observability
Long-running processes should expose:
- progress_percent;
- state;
- current_stage;
- completed_units / total_units;
- last_successful_checkpoint;
- last_progress_at;
- next_expected_step;
- failure_or_stall_reason;
and for training: epoch, global step, latest loss/metric, best checkpoint when feasible.

## Time display
All user-facing clock times must be shown in:
`Asia/Baghdad (UTC+3)`
unless the user explicitly requests another timezone.

## UI resilience
Permanent rule:
`DURABLE_STATE_BEFORE_RETRY`

If the UI says:
- “Our systems are thinking a bit more about this request before responding.”
- “Connection interrupted. Waiting for the complete answer”
- stream recovery/network timeout

then:
1. inspect GitHub durable state first;
2. do not repeat an operation that already committed/executed;
3. preserve failed/partial runs as evidence.

---

# 2. GLOBAL SCIENTIFIC BOUNDARIES

Project:
`ACAD_PASS — Academic Document Intelligence & Transformation Platform`

Current strategy:
`ENGLISH_FIRST / MULTILINGUAL_READY_CORE`

Arabic track:
- preserved/frozen research evidence;
- do not restart Arabic work unless explicitly authorized.

FactPICO V2.5:
- one-shot prediction and scoring are complete/frozen;
- exposed diagnostic evidence only;
- never use FactPICO again as a prospective independent validation set;
- no prediction rerun;
- no scoring rerun;
- no threshold/gold/population changes.

Frozen V2.5 FactPICO result:
- exact join 345/345;
- unsafe PASS = 0;
- negative utility REJECT micro = 10.7383%, macro = 9.4378%;
- SAFE anti-degeneracy PASS = 0%;
- mechanical decision: `H1_FULL_PASS_NOT_ACHIEVED`.

Failure localization:
`EXTRACTION/REPRESENTATION UNCERTAINTY + UNEQUAL-COUNT GROUPING AMPLIFICATION + FAIL-CLOSED REVIEW GATE`

R1-R3 on V2.6 development branch:
- R1 biomedical-aware boundary/markup normalization;
- R2 atomic/local assertion confidence;
- R3 exact partial Hungarian alignment with explicit unmatched nodes;
- development mechanics eventually PASS 260/260;
- FactPICO records used = 0.

---

# 3. R4 DEVELOPMENT HISTORY — KEY DURABLE STATES

## R4.1 / internal holdout
Consumed one-time 60-RCT internal holdout:
run `37340581937`
artifact `11358256711`
digest `sha256:808bce1258ccb2493385d81681b83bc2dbca010b0697f46909a84ab3db27f98c`

Observed:
- unresolved = 300/715 = 41.9580% FAIL vs <=40%;
- non-CERTAIN = 304/715 = 42.5175% PASS vs <=45%;
- short evidence <=3 chars = 2 FAIL vs 0;
- empty documents = 0 PASS;
- over-128 documents = 0 PASS;
- docs non-CERTAIN <=50% = 49/60 = 81.6667% PASS vs >=80%.

Overall:
`FAIL_INTERNAL_HOLDOUT_GATE`

The 60-RCT holdout is CONSUMED and MUST NOT be rerun or tuned against.

## R4.2 / first auxiliary witness path
Several technical attempts occurred; preserve all as negative evidence.

Safe train run 4:
run `37355935421`
- valid progress to >=4 epochs/checkpoints;
- cancelled by 120-minute GitHub timeout only;
- classified `TECHNICAL_EXECUTION_TIMEOUT_AFTER_VALID_TRAINING_PROGRESS`.

V5 valid run:
run `37372306905`
- valid training/calibration;
- scientific frozen-dev calibration FAIL;
- best exact entity macro-F1 = 0.6841077577;
- exact micro-F1 = 0.665;
- at threshold .95 precision P/I/C/O =
  0.7400 / 0.843137 / 0.941176 / 0.831325.

Deep source-code audit found training-protocol mismatch vs pinned source:
- weight_decay .01 vs source 0.0;
- warmup_ratio .10 vs source warmup_steps 0;
- seed 20261005 vs source 42;
- eval batch 16 vs source 8;
- early stopping/best model vs fixed 10-epoch source execution.

## R4.2B source-aligned run
Run:
`37409097042`

Training:
- 10/10 epochs;
- 1970/1970 steps;
- 100%;
- runtime 15282.3433 s;
- train loss 0.1087133559;
- final checkpoint-1970.

Artifact:
`11397202598`
digest:
`sha256:45d204d5f073aa5ecc5944dc49bee88be5bb677e0160b8c17720f2250de6fa71`

Scientific result:
`R4_2B_SOURCE_ALIGNED_WITNESS_NOT_READY`
classification:
`SCIENTIFIC_FROZEN_DEV_CALIBRATION_GATE_FAIL`

## R4.2B dev-only boundary diagnostic
Run:
`37445035553`
Artifact:
`11402997860`
Digest:
`sha256:6718d7007ed8b16f9644a33879e540ebadd26bcdbb248f98f21d5a74c8e0f5b1`

At threshold 0.95:
- accepted = 326;
- exact TP = 249;
- errors = 77;
- same-type boundary errors = 47;
- overlap-related boundary/type errors = 59/77 = 76.623%;
- spurious = 18.

Exact precision:
- P 0.769231
- I 0.780303
- C 0.933333
- O 0.724409

Diagnostic partial-overlap micro-F1:
0.831658
vs exact:
0.678392
delta:
+15.33 pp

Conclusion:
`REJECT_THRESHOLD_ONLY_RESCUE`

Chosen architecture:
`R4_2C_INDEPENDENT_BOUNDARY_AND_TYPE_AGREEMENT_GUARD`

---

# 4. R4.2C FROZEN ARCHITECTURE / PROTOCOL

Design:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2C_BOUNDARY_CONSENSUS_DESIGN_V1.md`

Training protocol:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2C_TRAINING_PROTOCOL_V1.md`

Preflight:
run `37447124232`
artifact `11404450510`
digest `sha256:f975a0f251bcfd392af49b7227678f7162ad55f7cd970d530083fdf5202868b1`

Frozen architecture:
`FROZEN_R4_2B_BIO_CANDIDATE + CLASS_AGNOSTIC_BOUNDARY_LOCALIZER + INDEPENDENT P/I/C/O SPAN_CLASSIFIER`

Boundary module:
- labels OUT/START/END/BOTH/IN;
- lr 5e-5;
- batch 8;
- 3 epochs;
- weight decay .01;
- max sequence length 256;
- boundary generation threshold .25.

Span classifier:
- independent P/I/C/O sigmoid outputs;
- lr 2e-5;
- batch 16;
- 3 epochs;
- weight decay .01;
- max span width 64 words.

Final threshold grid:
`{0.80,0.85,0.90,0.95}`

Exact frozen gate:
- per-class precision >= .90;
- per-class recall >= .20;
- accepted >=10;
- macro precision >= .90.

No threshold relaxation.
Exact span + exact class only.
Disagreement -> REVIEW.

Future test sets:
EBM/COVID/AD remain CLOSED.

Forbidden:
- FactPICO;
- consumed 60-RCT holdout;
- opened-30 diagnostic reuse as validation;
- threshold relaxation;
- dev-specific lexical boundary patches.

---

# 5. R4.2C IMPLEMENTATION SMOKE

Smoke run:
`37451040508`

Artifact:
`11406382749`

Digest:
`sha256:d51cd634ff242ef11805de77c57560259457572a64c30ebb97533477bb891eea`

Result:
`R4_2C_SMOKE_PASS`

Observed:
- boundary loss = 1.8232231140 finite;
- span loss = 0.6865816712 finite;
- exact scorer fixtures PASS;
- R4.2B model SHA =
  `3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c`;
- finite gradients and one optimizer step for both modules;
- no full scientific training;
- no forbidden test/holdout access.

Authorization after smoke:
`AUTHORIZE_ONE_R4_2C_DEVELOPMENT_TRAINING_AND_FROZEN_DEV_CALIBRATION_RUN`

---

# 6. MOST RECENT RUN — IMPORTANT FAILURE

Trigger commit:
`2edc17456fde57b76914c076c5a1c267e3c90db8`

Workflow:
`AT0 EN V2.6 R4.2C ONE boundary-consensus train calibration`

Run:
`37451685278`

Conclusion:
`failure`

Job:
`112229491860`

Artifact:
`11406449018`

Artifact digest:
`sha256:a515ebe81649f456f669b4da32679de4f6ebaa342388bc51978bc2cb33240ad5`

Important classification:
`PRE-TRAINING TECHNICAL IMPLEMENTATION FAILURE`

Evidence:
- dependency install succeeded;
- exact train/dev acquisition succeeded;
- exact R4.2B model download succeeded;
- safe base conversion/model initialization succeeded;
- failure occurred about 6 seconds after entering full training step;
- completed_units = 0;
- no boundary epoch completed;
- no span epoch completed;
- no calibration result;
- no scientific result was produced.

Exact traceback:
`RuntimeError: boundary truncation: 54 != 55`

Location:
`phase2/academic_transform/at0_en/v2_6/r4_2c_boundary_consensus_train.py`
inside `BoundaryDataset.__init__`

Mechanism:
the frozen `max_length=256` tokenizer path truncated at least one full train/dev sentence so one word token was absent after wordpiece tokenization.

This failure MUST NOT be interpreted as a scientific calibration failure.

Do NOT rerun the training workflow unchanged.

---

# 7. CURRENT RECOVERY DECISION

The frozen protocol specifies boundary max sequence length = 256.

Therefore:
- do NOT silently raise max_length;
- do NOT change hyperparameters before measuring exact tokenizer capacity;
- do NOT split or rewrite sentences based on dev performance;
- do NOT trigger another full training run yet.

Chosen narrow recovery:
1. freeze the failed run as negative evidence;
2. perform a read-only tokenizer-capacity audit over the exact frozen train/dev using the exact pinned tokenizer;
3. measure:
   - max wordpieces with special tokens;
   - number of sentences >256;
   - number >512;
   - exact number of word tokens lost at 256;
4. only after evidence, choose the smallest execution-only correction consistent with the frozen scientific design;
5. pass mechanics/preflight again;
6. only then authorize a replacement full development training run.

A diagnostic script was created:
`phase2/academic_transform/at0_en/v2_6/r4_2c_tokenizer_capacity_audit.py`

Creation commit:
`73ddde65ef851b7ca99bd2615923da95a6f8940d`

The associated GitHub Actions workflow had NOT yet been successfully created at the moment this handoff file was first written because the prior tool call hit a JavaScript string/syntax issue before any GitHub mutation.

---

# 8. EXACT CURRENT CHECKPOINT

`R4_2C_PRETRAIN_TRUNCATION_FAILURE -> READ_ONLY_TOKENIZER_CAPACITY_AUDIT`

Next authorized operation:
create the read-only tokenizer-capacity audit workflow, trigger it once, inspect its artifact, then freeze the execution-only recovery decision.

Do NOT:
- rerun run 37451685278 unchanged;
- change threshold grid/gates;
- open EBM/COVID/AD tests;
- touch FactPICO;
- rerun consumed 60-RCT holdout;
- perform new scientific training before the tokenizer-capacity audit is frozen.

---

# 9. NEW-CHAT START PROMPT

Recommended minimal instruction in a new conversation:

`Continue ACAD_PASS. Read ACAD_PASS_CHAT_HANDOFF.md first, then ACAD_PASS_MASTER_CONTINUITY.md, then the latest end of RESUME_HERE.md from repository abdullah-s-mahmood/sweet-runtime-parity. Determine the active branch from durable GitHub state. Continue exactly from the authorized current checkpoint. Do not repeat completed or one-shot work.`

If this file itself is pasted into the new chat, say:

`Continue ACAD_PASS from this handoff. Verify durable GitHub state before any retry and continue the exact current checkpoint.`
