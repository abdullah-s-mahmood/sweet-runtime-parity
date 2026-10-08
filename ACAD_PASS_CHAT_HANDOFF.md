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


---

# 10. LATEST VERIFIED UPDATE — R4.2C RECOVERY SMOKE PASS

Date: 2026-10-06

Read-only tokenizer audit:
- run `37454434658`
- artifact `11408961382`
- digest `sha256:fd43fccc9b7dc60664af21ac9178a2d59dea557462b2f99dc43a0a0be141da33`
- max encoded train/dev length = 141 wordpieces with specials;
- sentences >256 = 0;
- sentences >512 = 0;
- root cause was NOT sequence capacity.

Exact root cause:
- 17 literal zero-length surface-token rows in pinned train data across 12 sentences;
- tag distribution: O=5, I-I=5, I-P=6, I-O=1;
- source implementation explicitly filters tokenized-empty rows before training.

Source-aligned trainer correction:
- commit `a74f064b473a5065886afb39926369305532b778`
- max_length remains 256;
- no scientific hyperparameter/gate change.

Recovery record:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2C_PRETRAIN_EMPTY_TOKEN_RECOVERY_V1.md`

Recovery smoke:
- run `37455086281` SUCCESS
- artifact `11409796452`
- digest `sha256:fd53c2eac731e7eb023f83efb2a646c76052fd5f99e7868648e0d5485551aae9`
- trainer SHA `56b2d77d548c3980700664e58557b33bc0dbde66f99bdff529812fe301e95ca8`
- smoke-result SHA `57da2eb93574f09d7d84efd800c885863567db3455195595b61a81e77a174a94`
- train full token alignment = 1576/1576 PASS
- dev full token alignment = 205/205 PASS
- boundary loss = 1.8232231140 finite
- span loss = 0.6865816712 finite
- exact scorer fixtures PASS
- scientific_training_performed = false
- forbidden test/FactPICO/holdout access = false

Recovery smoke freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2C_RECOVERY_SMOKE_FREEZE_V1.md`
commit:
`893122f344535850fa226358cdf763398a267ac3`

Quality delta:
`IMPROVED — TECHNICAL FAILURE ROOT CAUSE IDENTIFIED AND SOURCE-ALIGNED RECOVERY VALIDATED`

Scientific-performance delta:
`NOT COMPARABLE / NO NEW FULL TRAINING RESULT YET`

CURRENT EXACT CHECKPOINT — THIS SUPERSEDES EARLIER CHECKPOINT TEXT ABOVE:
`R4_2C_RECOVERY_SMOKE_PASS / READY_FOR_ONE_REPLACEMENT_DEVELOPMENT_TRAINING_AND_FROZEN_DEV_CALIBRATION_RUN`

Next authorized operation:
trigger exactly one replacement R4.2C development training + frozen-dev calibration run using the corrected trainer, monitor PROCESS_STATUS, freeze its result, then STOP before any EBM/COVID/AD test inference.

Do NOT:
- rerun the failed pre-training run unchanged;
- change max_length, thresholds, gates, data, model family or hyperparameters;
- open EBM/COVID/AD tests;
- touch FactPICO;
- rerun consumed 60-RCT holdout.


---

# 11. LATEST VERIFIED UPDATE — R4.2C DEV GATE FAIL + FP DECOMPOSITION

Date: 2026-10-06

Replacement R4.2C run:
- run `37464774424`
- artifact `11417809920`
- digest `sha256:1144116b0f5bc026fa1f96eb2def07e4e640455e011a01b5b8f184732b900218`
- final state `COMPLETED_WITH_GATE_FAIL`
- failure class `SCIENTIFIC_FROZEN_DEV_CONSENSUS_GATE_FAIL`
- not a technical failure.

Training:
- boundary selected epoch 2, eval_loss 0.3318938017
- span selected epoch 3, eval_macro_f1 0.8962295847, eval_accuracy 0.8903061224

Best frozen calibration:
- threshold 0.90
- macro precision 0.8254464286
- P/I/C/O precision = 0.770833 / 0.812500 / 0.937500 / 0.780952
- chosen calibration = null

Threshold-only rescue remains rejected.

Dev-only FP diagnostic:
- run `37477106239`
- artifact `11420250305`
- digest `sha256:269736b2bfa42d3ca877dad42b26cbb8d0f77bf40de8d56074f9538c196110df`
- 404 candidates
- at t=0.90: 225 TP, 56 FP
- 48/56 FP = 85.71% individually plausible but jointly invalid span-boundary pairs
- 33/56 FP = 58.93% same-class wrong-boundary overlap
- span confidence does not separate TP from FP: TP mean 0.96918 vs FP mean 0.97025.

Oracle diagnostic only:
if the 48 joint-invalid FPs were perfectly rejected with current TPs preserved, approximate precision would be P 1.000, I 0.938, C 1.000, O 0.976. This is not an achieved result; it demonstrates mechanism sufficiency.

Frozen evidence:
- `AT0_EN_V26_R4_2C_DEV_GATE_RESULT_FREEZE_V1.md`
- `AT0_EN_V26_R4_2C_FP_DECOMPOSITION_FREEZE_V1.md`

Architecture direction:
`R4_2D = FROZEN_R4_2C + TRAIN_ONLY_HARD_NEGATIVE_SPAN_VALIDITY_GUARD`

Rationale:
the R4.2C type classifier learned only gold spans and has no explicit invalid/non-entity span rejection objective. R4.2D must add a separate validity guard trained strictly from TRAIN-only positives and hard negative spans. Do not mine dev FPs for training.

CURRENT EXACT CHECKPOINT:
`DESIGN_AND_PREFLIGHT_R4_2D_HARD_NEGATIVE_SPAN_VALIDITY_GUARD`

Do not:
- open EBM/COVID/AD tests;
- touch FactPICO;
- rerun consumed 60-RCT holdout;
- tune the old R4.2C threshold grid as a rescue;
- train R4.2D before its negative-generation policy and fixed decision rule are frozen.


---

# 12. LATEST VERIFIED UPDATE — R4.2D PREFLIGHT PASS / FULL RUN STARTED

Date: 2026-10-06

R4.2D design:
`FROZEN_R4_2C + TRAIN_ONLY_HARD_NEGATIVE_SPAN_VALIDITY_GUARD`

Design file:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2D_SPAN_VALIDITY_DESIGN_V1.md`

Frozen validity rule:
- VALID / INVALID binary span classifier
- train only
- one deterministic boundary-shift negative plus one deterministic length-matched non-overlap negative per gold when available
- fixed validity threshold `P(VALID) >= 0.50`
- existing R4.2C threshold grid and scientific gate unchanged.

Preflight:
- run `37479013072` SUCCESS
- artifact `11419504487`
- digest `sha256:576f52d692efc41a93a1b5a6500b6a79040db392a0d06751d1e7f49ca536b863`
- positives 3011
- unique boundary-shift negatives 3011
- unique non-overlap negatives 2431
- total unique invalid 5442
- total examples 8453
- collisions 0
- dataset SHA256 `6038f5dd905271b27ad7be8f86118aa583f5adc06158b3adcbd9a7f02b724461`
- max wordpieces 58
- smoke loss 0.761030376 finite
- finite gradients true
- dev/test not read.

Preflight freeze:
`AT0_EN_V26_R4_2D_PREFLIGHT_FREEZE_V1.md`

Authorized full run was launched:
- trigger commit `fb3644e2f01189a0f5c0c676fa0f26d4d8ef2116`
- run `37479970741`
- workflow `AT0 EN V2.6 R4.2D ONE span validity train calibration`
- state at this checkpoint `IN_PROGRESS`
- start 2026-10-06 17:33:33 Asia/Baghdad
- setup/checkout/Python PASS
- frozen runtime installation active at first observation
- scientific training had not yet started at that observation.

CURRENT EXACT CHECKPOINT:
`R4_2D_RUN_37479970741_IN_PROGRESS`

Exact next operation:
monitor the SAME run, inspect PROCESS_STATUS and artifact at terminal state, freeze exact result, and STOP before EBM/COVID/AD external test inference.

Do not rerun or change protocol automatically.


---

# 12. LATEST VERIFIED UPDATE — R4.2D DEV GATE FAIL

Date: 2026-10-06

R4.2D run:
- run `37479970741`
- artifact `11422811514`
- digest `sha256:7fd6cf920ff98bb19770a8a55efaae35ce73c11a5e4bf5a122b732238bc951e7`
- final state `COMPLETED_WITH_GATE_FAIL`
- scientific failure, not technical
- epochs 3/3, steps 1587/1587
- validity model SHA `14a70d925cfff7959cba4afa4a10b8f30413961eaea24ba308754dfc6d36f146`

Best frozen calibration at t=0.90:
- macro precision 0.8239836029
- P/I/C/O precision = 0.770833 / 0.801887 / 0.937500 / 0.785714

Compared with R4.2C at t=0.90:
- macro precision changed 0.8254464286 -> 0.8239836029
- delta = -0.0014628257 (-0.1463 pp)
- accepted/TP/FP changed 281/225/56 -> 268/214/54
- guard removed 13 candidates: 11 TP and only 2 FP.

Critical evidence:
- accepted TP mean P(VALID) = 0.9537864043
- accepted FP mean P(VALID) = 0.9662910192
- therefore the content-only validity classifier does not separate exact-valid spans from false candidates and is rejected.

Frozen result:
`AT0_EN_V26_R4_2D_DEV_GATE_RESULT_FREEZE_V1.md`

Decision:
`REJECT_CONTENT_ONLY_SPAN_VALIDITY_GUARD`

CURRENT EXACT CHECKPOINT:
`DESIGN_AND_PREFLIGHT_R4_2E_TRAIN_ONLY_JOINT_BOUNDARY_PAIR_VALIDATOR`

R4.2E direction:
preserve frozen R4.2C and train a small pair validator using contextual start/end representations from the frozen R4.2C boundary encoder, so validity is modeled as a JOINT boundary-pair decision instead of candidate-span semantic content.

Do not:
- tune R4.2D validity threshold on dev;
- rerun R4.2D unchanged;
- open EBM/COVID/AD tests;
- touch FactPICO;
- rerun the consumed 60-RCT holdout.


---

## 2026-10-07 — R4.3 contextual pair preflight PASS / STOP BEFORE TRAINING

Independent higher-model verdict:
`RUN_ONE_MORE_TRAIN_ONLY_DIAGNOSTIC_BEFORE_ARCHITECTURE_SELECTION`

Bounded future comparison:
- H0 contextual typed MLP
- H1 same contextual path + biaffine start/end interaction

Critical correction:
R4.2C `48/56 joint_invalid_fp` must not be read as 48 literal cross-entity pairs. Literal gold-boundary cross-pairs were only 3 across all 404 candidates. Competing explanations are missing context, negative mismatch, and endpoint interaction.

Design:
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V1.md`
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V2.md`

Initial preflight run `37533646474` stopped pre-training on 11 source sequence-initial I-* labels. TRAIN-only audit proved all 11 are valid same-type continuation segments across source example boundaries; zero invalid within-example I transitions. V2 freezes explicit continuation-segment semantics without rewriting raw labels.

Successful replacement preflight:
- run `37534110955` SUCCESS
- head `4ca858fcd8b632bc67748bfe1e8fdb0d9d6f8dbd`
- artifact `11446235369`
- digest `sha256:84f9688be55f46dfc6d05cee638c7552e12e6ed0ccae63e3b6f2fc99a4478c94`
- freeze file `AT0_EN_V26_R43_CONTEXTUAL_PAIR_PREFLIGHT_FREEZE_V1.md`
- freeze commit `fca998366cd246b68e13469e1a27d538a66eec88`

Source TRAIN:
- 400 documents, 1576 sequences, 41070 tokens
- gold P/I/C/O = 434/1328/181/1068; total 3011
- max gold width 54
- duplicate document groups 0
- tag-conflicting duplicate docs 0
- invalid BIO after frozen continuation semantics 0

Frozen FIT/SELECT:
- manifest SHA `fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`
- FIT 320 docs; P/I/C/O = 342/1038/144/847; total 2371
- SELECT 80 docs; P/I/C/O = 92/290/37/221; total 640
- overlap 0
- SELECT deviations from exact 20% targets: P +5.99%, I +9.19%, C +2.21%, O +3.46%

TRAIN-only negative feasibility:
- local raw 4742
- composites raw 2042 = 1239 same-class + 803 different-class
- unique local+composite NONE 6157
- reserved background fallback unique 1908
- gold/synthetic coordinate collisions 0
- static manifest SHA `1ac4b4dd2ca3c1dbc42b5dc0530cafc93fb289f1646b518e305a3d7c20d5d8d2`
- native FIT-model errors intentionally deferred until a future FIT-only B replica exists

Critical context evidence:
- complete TRAIN: 14 identical cropped token strings/tokenizer sequences occur with multiple entity classes
- FIT prospective construction: 43 cropped token strings (48 tokenizer-ID sequences) can be both entity and synthetic NONE depending on context
This directly strengthens the missing-context hypothesis and explains why content-only R4.2D can fail. It does NOT prove biaffine necessity.

Head sizes:
- H0 trainable = 579,461
- H1 trainable = 662,666
- H1-H0 = 83,205 biaffine parameters

Access guards:
- TRAIN only
- historical DEV false
- fold1 TEST false
- other folds false
- external EBM/COVID/AD false
- FactPICO false
- consumed 60-RCT holdout false
- scientific training false

CURRENT EXACT CHECKPOINT:
`R43_CONTEXTUAL_PAIR_PREFLIGHT_PASS / REVIEW_FROZEN_PACKET_BEFORE_ANY_TRAINING_AUTHORIZATION`

Do NOT train FIT-only B/boundary/type/H0/H1 yet.


---

## 2026-10-07 — R4.3 Stage A FIT-only ancestors launched

Higher-model review + successful TRAIN-only preflight are now frozen.

Canonical R4.3 packet:
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V1.md`
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V2.md`
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_PREFLIGHT_FREEZE_V1.md`
- `AT0_EN_V26_R43_DIAGNOSTIC_TRAINING_AUTHORIZATION_V1.md`

Frozen split manifest:
`fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`

FIT = 320 documents; P/I/C/O = 342/1038/144/847.
SELECT = 80 documents; P/I/C/O = 92/290/37/221.

Stage A run:
- workflow `AT0 EN V2.6 R4.3 FIT-only ancestors`
- run `37535183682`
- head `ad058bc856c280914158e005b07ffe6a0834aa13`
- state at launch: IN_PROGRESS
- started 2026-10-07 00:37:25 Asia/Baghdad
- current observed step: frozen runtime installation; scientific training not yet entered.

Stage A trains ONLY FIT:
- B candidate generator 10 fixed epochs
- C boundary 3 fixed epochs
- C type 3 fixed epochs
- final fixed epoch only
- SELECT is not training/checkpoint-selection data.

Governance hardening:
generic `at0_en_v2_6_dev_representation.yml` no longer automatically runs real-RCT stress or the already-open 30-RCT audit. Those diagnostics now require separate explicit authorization. The hardening mechanics run `37535069562` passed.

Current exact checkpoint:
`R43_STAGE_A_RUN_37535183682_IN_PROGRESS`

Exact next operation:
monitor THIS SAME Stage-A run; do not relaunch. On success freeze ancestor hashes/evidence, then separately execute the already-authorized Stage B H0-vs-H1 comparison. On technical failure, root-cause and only scientifically neutral repair.

Do not access historical DEV, fold1 TEST, other folds, external EBM/COVID/AD tests, FactPICO, opened-30 diagnostic, or consumed 60-RCT holdout.


---

## 2026-10-07 — TEMPORARY PARALLEL WINDOW DURING R4.3 STAGE A

User explicitly authorized a temporary exception to the usual sequential-only rule UNTIL Stage A finishes:
independent, non-conflicting work may run in parallel while Stage A is active. As soon as Stage A terminates, revert immediately to sequential-only execution.

Canonical Stage A:
- run `37535183682`
- workflow `AT0 EN V2.6 R4.3 FIT-only ancestors`
- status at latest checkpoint: `IN_PROGRESS`
- active scientific step: FIT-only ancestor training
- no live logs available during run; do not infer failure from missing log blob.

Independent work completed during the temporary window:

### 1. Boundary-repair feasibility
Run `37539123038` SUCCESS.
Artifact `11448196366`.
Digest `sha256:f51f6490079bd50218e7e467a7853e5a5391261ce0a5303ced53f4648085da2c`.

Local perturbations:
- 105,766 candidates
- 101,487 unique nearest gold (~95.95%)
- 4,279 ambiguous (~4.05%)
- ~95.28% repairable within +/-4

Composite spans:
- 2,822 total
- 753 ambiguous (~26.68%)
- only 615 (~21.79%) repairable within +/-4

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_BOUNDARY_REPAIR_FEASIBILITY_FREEZE_V1.md`

Interpretation:
near-boundary errors are suitable for gated offset repair; composite/far spans are better suited to contextual verification/review.

### 2. Frozen-base context-signal probe
Run `37539134852` SUCCESS.
Artifact `11447393744`.
Digest `sha256:ffdfee805e32a500403ef5a1fd1f219f96f799b675a1eaf037f1e1bd5607af76`.

FIT-only internal probe:
- cropped macro F1 = 0.563475
- contextual macro F1 = 0.641445
- delta = +0.077970 (+7.797 pp)
- ambiguous-surface subset delta = +0.191111 (+19.111 pp), n=14

Important risk:
- C precision fell 0.5652 -> 0.2687 in the simple contextual linear probe.

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_CONTEXT_SIGNAL_PROBE_FREEZE_V1.md`

Interpretation:
context is materially useful, but C remains a stability risk.

### 3. Context-locality audit
Run `37539816534` SUCCESS.
Artifact `11448172538`.
Digest `sha256:f1a69ebce503b40bf598e4abeb4ec334098207a8684e37c52556568bfc1aa29a`.

Conflict keys:
- surface only: 42
- +/-1 context: 2
- +/-2 context: 1
- +/-4 context: 0
- full sentence + coordinates: 0

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_CONTEXT_LOCALITY_AUDIT_FREEZE_V1.md`

Interpretation:
most cropped-surface ambiguity is contextual, not irreducible.

### 4. Stage-B mechanics
Run `37540302867` SUCCESS.
Artifact `11447889249`.
Digest `sha256:d35ad79f82cb64d75f9e1f25a3367f1b329962945ec47e07bdac5d49e6647a9c`.

H0:
- 579,461 params
- finite mechanics PASS

H1:
- 662,666 params
- finite mechanics PASS

Difference:
- 83,205 params

Prepared Stage-B implementation:
`r43_stage_b_h0_h1_diagnostic.py`

It has a mandatory candidate-ceiling STOP before H0/H1 scientific training if native SELECT proposals cannot meet recall/support floors.

Frozen mechanics:
`AT0_EN_V26_R43_STAGE_B_MECHANICS_FREEZE_V1.md`

Stage B has NOT been launched.

### 5. Additional independent probe currently running
Run `37540851386`:
`AT0 EN V2.6 R4.3 independent base H0-H1 probe`
FIT-only, frozen-base, no Stage-A outputs, SELECT/DEV/TEST/protected data.
Exploratory only; cannot modify frozen Stage B.

### Durable method registry
`ACAD_PASS_METHODS_REGISTRY.md`
records all tried/researched/retained methods including contextual MLP, biaffine, triaffine, PICOX composites, BOPN, Locate-and-Label, MRC, GlobalPointer/grid, hybrid repair+verification, stronger encoders, ensembles, and DiffusionNER as a retained lower-priority alternative.

### Source-code-audited repair fallback
`AT0_EN_V26_R43_BOUNDARY_REPAIR_SOURCE_AUDIT_V1.md`
documents official BOPN and Locate-and-Label mechanisms.

### Post-Stage-B prospective decision matrix
`AT0_EN_V26_R43_STAGE_B_READINESS_AND_FALLBACK_MATRIX_V1.md`

CURRENT GOVERNANCE:
- while Stage A active: temporary parallel independent work allowed by explicit user authorization;
- when Stage A reaches terminal state: STOP launching parallel work and revert immediately to sequential-only;
- first operation after Stage A terminal: inspect/freeze Stage-A identities and guards;
- only then consider the already-authorized Stage B sequentially.


---

## 2026-10-07 — Parallel exploratory evidence while R4.3 Stage A remains active

Temporary user-authorized exception allowed independent, non-conflicting exploratory work in parallel with Stage A. Scientific processing returns to strictly sequential after Stage A ends.

### Stage A current exact run

- run `37535183682`
- workflow `AT0 EN V2.6 R4.3 FIT-only ancestors`
- status `IN_PROGRESS`
- current step: `Train FIT-only frozen ancestors`
- all setup/acquisition/identity-freeze steps completed successfully
- live job log blob still unavailable while active; no fabricated epoch/step percentage
- automatic watch remains attached to this exact run

### Independent FIT-only boundary-repair feasibility

Run `37539123038` SUCCESS.
Artifact `11448196366`, digest `sha256:f51f6490079bd50218e7e467a7853e5a5391261ce0a5303ced53f4648085da2c`.

Local perturbations:
- candidates 105,766
- unique nearest gold target 101,487 (~95.95%)
- ambiguous nearest target 4,279 (~4.05%)
- repairable within +/-4 = 100,768 (~95.28%)

Composite spans:
- total 2,822
- ambiguous nearest target 753 (~26.68%)
- repairable within +/-4 = 615 (~21.79%)

Implication: future hybrid should preferentially repair local/near-boundary spans, while composite/far/ambiguous spans should be contextually scored/rejected rather than blindly repaired.

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_BOUNDARY_REPAIR_FEASIBILITY_FREEZE_V1.md`

### Independent FIT-only context signal probe

Run `37539134852` SUCCESS.
Artifact `11447393744`, digest `sha256:ffdfee805e32a500403ef5a1fd1f219f96f799b675a1eaf037f1e1bd5607af76`.

All eval:
- cropped accuracy 0.7586423755, macro-F1 0.5634747631
- contextual accuracy 0.7730987072, macro-F1 0.6414445653
- delta macro-F1 +0.0779698022

Ambiguous-surface subset:
- cropped macro-F1 0.3866666667
- contextual macro-F1 0.5777777778
- delta +0.1911111111

Implication: missing context is now directly supported by FIT-only evidence. This supports H0/H1 but does not prove biaffine necessity.

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_CONTEXT_SIGNAL_FREEZE_V1.md`

### Independent FIT-only context locality audit

Run `37539816534` SUCCESS.
Artifact `11448172538`, digest `sha256:f1a69ebce503b40bf598e4abeb4ec334098207a8684e37c52556568bfc1aa29a`.

Representation conflicts:
- cropped surface only: 42
- +/-1 context: 2
- +/-2 context: 1
- +/-4 context: 0
- full sentence + coordinates: 0

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_CONTEXT_LOCALITY_FREEZE_V1.md`

### Stage-B mechanics/readiness

Mechanics run `37540302867` SUCCESS.
- H0 params = 579,461
- H1 params = 662,666
- H1-H0 = 83,205
- both forward/backward finite

Prepared but NOT TRIGGERED:
- trainer `r43_stage_b_h0_h1_diagnostic.py`
- workflow `.github/workflows/at0_en_v2_6_r43_stage_b_h0_h1.yml`

The Stage-B workflow is pinned to Stage-A run `37535183682`, verifies Stage-A summary/model hashes/guards, uses the frozen split, enforces candidate-ceiling stop, then performs only the authorized H0-vs-H1 diagnostic.

Do NOT create `.github/diagnostics/r43_stage_b_trigger_v1.txt` until Stage A is terminal SUCCESS and its artifact is fully verified.

CURRENT EXACT CHECKPOINT:
`R43_STAGE_A_IN_PROGRESS / INDEPENDENT_EVIDENCE_FROZEN / STAGE_B_READY_BUT_NOT_TRIGGERED`


---

## 2026-10-07 — R4.3 Stage A terminal verification and Stage B launch

CURRENT STATUS:
`R43_STAGE_A_100_PERCENT_PHYSICALLY_VERIFIED / R43_STAGE_B_H0_H1_RUNNING`

### Stage A — COMPLETE, SUCCESS, VERIFIED

- Source run: `37535183682`, final success at ~2026-10-07 01:50Z (04:50 Baghdad).
- Head `ad058bc856c280914158e005b07ffe6a0834aa13`.
- Main ancestor artifact `11455753005`; digest `sha256:f2a0352cc4668faf180c4486f496d5bf6ccfd0e39d57fe8144b1b55808d3c2b6`.
- Physical hash verification run `37566322559` SUCCESS, artifact `11458734036` digest `sha256:0b873b366b1267cc86d29b49d60d7982ad65914a78e4011d003abd651a3184c7`.
- Witness `R43_STAGE_A_COMPACT_IDENTITY_PASS`.
- TRAIN SHA `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`.
- Immutable split SHA `fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`.
- FIT docs320, sentences1292, gold2371 (P342/I1038/C144/O847).
- B_CANDIDATE: 10/10 epochs, steps1620, loss0.1110674603, SHA `4e4852b847be5bf64cd707ed62f770e13d64ee6becea3ce049f69bde220bfb05`.
- C_BOUNDARY: 3/3 epochs, steps486, loss0.2763030014, SHA `8c0848e798dd2b2409a81931b7bac496f88fceec2c8bd589e95a186d67dacebb`.
- C_TYPE: 3/3 epochs, steps447, loss0.1797347431, SHA `c7d5e4d2eb1632ac39c944e28232f8addff6c037b1ea80a09436a885101aed1a`.
- FIT-only and final-epoch-only guards confirmed; no SELECT training, historical DEV, test, other folds, FactPICO, consumed 60-RCT.
- Canonical freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_STAGE_A_VERIFIED_RESULT_FREEZE_V1.md`.

### Independent FIT-only H0/H1 probes — terminal but NOT selection

- Probe A run `37540851386`: H0 macro-F1 0.8054956, H1 0.8211369, H1-H0 +0.0156413.
- Probe B run `37541116791`: H0 macro-F1 0.8457483, H1 0.8277176, H1-H0 -0.0180307.
- Different FIT-only inner partitions and candidate construction; opposite signs. Neither can be used to tune/select the main Stage B.
- Frozen details: `AT0_EN_V26_R43_INDEPENDENT_H0_H1_PROBES_FREEZE_V1.md`.

### Stage B — ONE RUN LAUNCHED

- Run `37566553994`
- Head SHA `a53cc67017d9973c4a76c4c99abdf34e2e329bb3`.
- Workflow `.github/workflows/at0_en_v2_6_r43_stage_b_h0_h1.yml`
- Trainer `phase2/academic_transform/at0_en/v2_6/r43_stage_b_h0_h1_diagnostic.py`
- Trigger `.github/diagnostics/r43_stage_b_trigger_v1.txt`.
- Last confirmed initial status `IN_PROGRESS`.
- Reads only pinned TRAIN and frozen 320-FIT/80-SELECT; uses exact Stage-A ancestor artifacts with SHA verification, makes native FIT-error negatives, computes candidate ceiling, and compares frozen H0 contextual typed MLP versus H1 identical+biaffine using frozen threshold grid `{0.80,0.85,0.90,0.95}`.
- Frozen scientific gate: precision>=0.90 each P/I/C/O, recall>=0.20 each, accepted>=10 each, macro precision>=0.90.
- Candidate ceiling can stop before head training; do not override.
- Stage B monitoring automation `6ac4142f5a1c8191aa1d615ea7e5bf81` updated to exact run `37566553994`, once hourly with state-change notifications.
- Strictly sequential scientific processing REINSTATED; temporary parallel permission expired once A finished.
- Do NOT relaunch Stage A, Stage B, independent probes or consume any closed tests.

NEXT_ACTION:
`WATCH_RUN_37566553994 -> ON_TERMINAL_VERIFY_ARTIFACT_AND_FREEZE_H0_VS_H1_RESULT -> APPLY_FROZEN_DECISION_RULES`.


---

## 2026-10-07 — R4.3 forensic causal review (supersedes tentative architecture escalation)

**CANONICAL REPORT:**
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_CAUSAL_FORENSIC_AUDIT_AND_RESEARCH_V1.md`
Commit `b72b013c17411e94dc0f61772684e3754c3c4853`.

**R4.3 STAGE B completed:** run `37566553994`, technical SUCCESS, scientific verdict `DIAGNOSTIC_NO_ARCHITECTURE_READY`. No additional scientific training or protected tests were run in this audit.

- Candidate ceiling: 697 proposals = 447 exact+type TP available / 250 FP; all P/I/C/O reachability floors possible.
- At t=.90, C-style pre-head 371 TP / 100 FP / macro P .8334036915.
- H0 348 TP / 85 FP / macro P .841786177.
- H1 362 TP / 87 FP / macro P .843930214.
- H1 FP taxonomy: 46 spurious/no-gold overlap; 34 same-type wrong-boundary overlap; 5 exact-boundary wrong-type; 2 overlap wrong-type.
- To pass every class precision >=.90 at fixed H1 t=.90 TPs, P must lose >=3 FP, I >=26 FP, O >=20 FP: >=49 P/I/O FPs total without TP loss.

**NEW ROOT FINDINGS:**
1. `native_slots=0` and 1982 fallback slots: no actual FIT B model errors were in head negative training. In-sample B mining plus code that seeds candidates only from gold-containing sentences creates a real training-distribution mismatch; exact relative contribution remains to be measured.
2. Cropped C-type head was trained on exact positive gold spans only, not invalid/NONE spans, but is used as a validity veto.
3. Actual-code synthetic unit test `37568400156` SUCCESS proves invalid predicted I-P after O becomes a candidate span without transition check; occurrence on real FIT remains unmeasured.
4. Current H0/H1 heads can only accept/reject frozen B coordinate/type; no boundary/type repair, no missing entity recovery.
5. A common t across unrelated sigmoid/softmax probabilities is not scientifically calibrated.
6. Full context here means one sentence, not an entire RCT abstract or section.
7. Some gold-absent spans may be annotation-incomplete, not necessarily clinically incorrect; EBM-NLP annotation noise/granularity is literature documented.
8. The current FP taxonomy is operational, not proof of one dominant pathology; R4.3 46 spurious FP differ from older R4.2C distributions.
9. Duplicate-count hazard is future only; current B spans unique. Overlap boundary label overwrite is future nested-entity hazard only.
10. SELECT now exposed; do not treat a further adaptive run on it as a fresh independent test.

**LITERATURE REVIEWED:** PICOX 2024, section-specific PICO 2023, NoiseBench 2024, CMiNER 2025, BEAN 2025, BGNER 2025, OpenBioNER-v2 2026, Multi-head Tri-Affine 2026, Trialstreamer operational workflow, Elicit and independent Elicit evaluation, GLiNER-biomed, BOPN and Locate-and-Label. Exact PICO gate outcomes are not directly comparable to vendor narrative extraction accuracy.

**IMPLEMENTED:** report freeze, methods registry update, `r43_semantic_contract_audit.py` tested SUCCESS, `r43_fit_b_native_error_causal_audit.py` prepared but NOT EXECUTED. A workflow creation attempt for the FIT-only replay was blocked, so no real-world B FIT error counts have been claimed.

**NEW NEXT_ACTION:**
`COMPLETE_FIT_ONLY_CAUSAL_REPLAY_AND_PROTOCOL_AUDIT -> FREEZE_RESULT -> ADVERSARIAL_HIGHER_MODEL_REVIEW -> DESIGN_OOF_NEGATIVE_MINING_WITH_GOLDLESS_COVERAGE -> PROSPECTIVE_TRAIN_ONLY_MODEL_COMPARISON`

Do NOT:
- reinterpret R4.3 as a scientific PASS;
- tune R4.3 thresholds on exposed SELECT;
- train BOPN, triaffine, MRC, GlobalPointer or larger encoder now;
- open historical DEV, protected tests, FactPICO, 60-RCT consumed holdout;
- perform concurrent training.

Maintain strictly sequential scientific execution.


---

## 2026-10-07 — R4.4-A LAUNCHED AFTER FORENSIC/SOURCE-PARITY REVIEW

### Correct source protocol confirmation

Newest corrected source-parity run:
- run `37580279584` SUCCESS
- artifact `11464027321`
- digest `sha256:86ca5a0efa626df59261884e70b95eea7cee8ee0f196f05b35d222c9bd1bfabe`
- freeze: `AT0_EN_V26_R43_SOURCE_PROTOCOL_PARITY_V2_FREEZE.md`

It executes the original `update_data_to_max_len(256)` plus the actual combined-file `evaluate.py -lf` path.
Official/manually independent strict-B source inventory matches exactly:
- P426 / I1326 / C181 / O1067 = 3000 total.
Legacy local-continuation parser = P434 / I1328 / C181 / O1068 = 3011.
All +11 are example-initial continuation fragments (+8P/+2I/+1O).
17 raw tokenizer-empty rows are removed by source preprocessing; no additional max-length split is created.
Run `37570558785` remains superseded tooling error and must not be cited scientifically.

### R44 design state

Canonical files:
- `AT0_EN_V26_R44_OOF_SUPERVISION_REPAIR_DESIGN_V1.md`
- `AT0_EN_V26_R44_ADVERSARIAL_PROTOCOL_REVIEW_V1.md`
- `AT0_EN_V26_R44_PREFLIGHT_FREEZE_V1.md`
- `AT0_EN_V26_R44A_OOF_BANK_AUTHORIZATION_V1.md`
- `AT0_EN_V26_R44A_PRELAUNCH_FORENSIC_AUDIT_V1.md`

Read-only preflight:
- run `37572165532` SUCCESS
- R44 manifest SHA `799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`
- parent = prior R4.3 FIT only; old R4.3 SELECT excluded.
- DESIGN = 256 docs / 1034 examples / 26,595 tokens / P271 I829 C115 O677.
- VERIFY_INTERNAL = 64 docs / P68 I207 C29 O169. It is INTERNAL only, not a pristine external benchmark, and remains unopened by R44-A.
- 5 OOF folds = 52/51/51/51/51 docs with balanced classes and C>=23 each.

DESIGN source-only package:
- run `37572893091` SUCCESS
- artifact `11461097651`
- design_source SHA `f8b49420cb17a5cb3f67f3120f9362b5e6b15fbb148176eab20105790bab1e18`
- contains neither VERIFY_INTERNAL nor old SELECT.

### Adversarial correction

Ordinary head CV over one OOF bank is blocked due to second-order stacking leakage.
R44 is split:
- R44-A = OOF B + Boundary candidate/evidence bank ONLY.
- STOP.
- R44-B must later use leakage-safe nested outer/inner CV or a fully disjoint stack-development selection protocol.
No J0/J1/head selection is authorized during R44-A.

### Neutral code hardening before launch

- `r44a_oof_fold_train.py`: BIO diagnostics changed from token-level orphan-I overcount to contiguous run-level `INITIAL_I_RUN/O_TO_I_RUN/CROSS_TYPE_I_RUN`; initial-I additionally flags source-gold valid document continuation. Candidate generation semantics unchanged.
- `r44a_aggregate_bank.py`: exact DESIGN document/gold guards P271/I829/C115/O677, plus candidate-row and target-count consistency checks.
- final mechanics/invariants run `37581258498` SUCCESS at current prelaunch code lineage.

### R44-A live execution

Workflow:
`.github/workflows/r44a_oof_bank.yml`

Run:
`37581447046`

Head:
`67c91c0c0f0155ca443bdfef80133cd0700dec14`

State at launch checkpoint:
- fold 0 = IN_PROGRESS
- folds 1/2/3/4 = QUEUED
- max-parallel=1 confirmed operationally; no concurrent scientific fold.
- aggregate waits until all five fold jobs succeed.

Each fold:
- B_CANDIDATE fixed 10 epochs
- C_BOUNDARY fixed 3 epochs
- train = DESIGN minus that fold
- infer = held-out fold only
- gold labels assigned only AFTER inference to candidate targets/taxonomy
- no C_TYPE, no downstream head, no threshold selection
- temporary model weights are not uploaded
- frozen candidate bank / summary / model hashes / guards only.

Automation:
`6ac4142f5a1c8191aa1d615ea7e5bf81`
now watches run `37581447046` hourly for meaningful progress/terminal state and MUST NOT start follow-on work.

### Mandatory stop

After aggregate:
`STOP_BEFORE_R44B_HEAD_TRAINING_OR_VERIFY_INTERNAL_ACCESS`

NEXT:
`COMPLETE_R44A_OOF_BANK -> FREEZE_AND_AUDIT_REAL_OOF_ERROR_DISTRIBUTION -> SELECT/FREEZE_LEAKAGE_SAFE_R44B_PROTOCOL -> ONLY_THEN_CONSIDER_HEAD_TRAINING`.


---

## 2026-10-08 — PERMANENT GOVERNANCE CORRECTION: SAFE MAXIMAL GITHUB RESOURCE UTILIZATION

This section supersedes any earlier blanket `strictly sequential` / `never run in parallel` rule.

New permanent rule:
- maximize safe use of available GitHub Actions resources and concurrency when doing so cannot change scientific meaning or reduce result accuracy/reproducibility;
- parallel execution is explicitly allowed for independent jobs with immutable inputs, disjoint output namespaces, no shared mutable state, no cross-job dependency, no evaluation leakage/contamination, and fully attributable deterministic outputs;
- keep dependent scientific stages sequential at their decision boundaries: a downstream stage must not start before all required upstream evidence is complete, verified, frozen, and authorized;
- operations touching the same branch/ref/file, consuming one-shot state, opening protected data, or capable of altering another job's inputs/outputs/decisions must be serialized;
- if concurrency could make values non-exact, ambiguous, non-reproducible, or scientifically confounded, do not parallelize it;
- preserve per-job hashes, guards, artifacts, process state, and provenance so parallel execution remains independently auditable.

Current R44-B interpretation:
- the already-running 10 pair-exclusion upstream jobs plus the label-independent context-cache job are scientifically independent by the frozen B1 protocol and therefore are VALID under this governance rule;
- no need to cancel or relaunch them merely because they are parallel;
- J0/J1 head training remains blocked until all required pair banks + aggregate + context-cache verification are complete and frozen.

Higher-model consultation remains exceptional rather than automatic, but should be explicitly requested from the user when a consequential architecture/protocol decision, ambiguous evidence, difficult failure, or high-value alternative warrants it. When requested, the packet should ask for deep research, adversarial review, genuine brainstorming, alternative hypotheses, failure analysis, and best-possible next design.

Permanent objective remains:
`BEST DEFENSIBLE RESULT / MAXIMUM SCIENTIFIC RIGOR / BEST ACHIEVABLE RESULT`.


---

## 2026-10-08 01:09 Asia/Baghdad — R44-B B1 partial live progress

Official run remains:
`37683637815` — `R44-B B1 parallel pair-exclusion upstream`.

Current durable state:
- frozen precheck: SUCCESS;
- immutable base context cache: SUCCESS, artifact `11510422862`, digest `sha256:4fdceb511c2067cf81a1ad6c64c039febf99e3c11b9d8baa32b2d73569faa91c`;
- pair `1-2`: SUCCESS, artifact `11512599487`, digest `sha256:d0db8ec0b12048993e721967999cc1b59385984ee45a3decda70e1f3a21e811d`;
- pair `1-4`: SUCCESS, artifact `11514343182`, digest `sha256:2649a8cfa94b3068a0a9ff322586af2ff1b285a7d1a8b144075fd608e1d3abeb`;
- remaining 8/10 pair jobs: IN_PROGRESS;
- failures: 0;
- queued pair jobs: 0;
- aggregate has not started because it waits for all ten pair jobs.

Completed-pair runtime evidence:
- pair 1-2 total B+Boundary train runtime ~61.46 min; wall time ~64.7 min;
- pair 1-4 total B+Boundary train runtime ~84.71 min; wall time ~87.0 min.
Runner-speed variance is therefore material; active jobs exceeding the faster completed pair is not evidence of a stall.

Current next action:
`CONTINUE_WATCH_RUN_37683637815 -> WHEN_ALL_10_PAIRS_SUCCESS VERIFY_PAIR_ARTIFACTS -> RUN/VERIFY_AGGREGATE -> VERIFY_CONTEXT_CACHE -> FREEZE_RESULT -> STOP BEFORE J0/J1 UNTIL SEPARATE DECISION/AUTHORIZATION`.


---

## 2026-10-08 — R44-B B1 upstream COMPLETE / pre-head review boundary

Official upstream run `37683637815` is terminal SUCCESS.

Verified:
- all 10/10 pair-exclusion jobs SUCCESS;
- pair aggregate SUCCESS with state `R44B_PAIR_AGGREGATE_PASS`;
- nested-bank artifact `11515434193`, digest `sha256:98383b4bec040f19d6e4076fea1a70dcb406366dfd4bd724d1ad2fac6d2018fb`;
- outer meta rows = 1567 / 1519 / 1499 / 1535 / 1551;
- outer meta C support = 68 / 66 / 71 / 69 / 71;
- immutable context cache state `R44B_BASE_CONTEXT_CACHE_PASS`;
- context artifact `11510422862`, digest `sha256:4fdceb511c2067cf81a1ad6c64c039febf99e3c11b9d8baa32b2d73569faa91c`;
- context shape 26,595 x 768 float32;
- labels_used=false; VERIFY_INTERNAL=false; old SELECT=false; protected=false.

Canonical upstream freeze:
`AT0_EN_V26_R44B_B1_UPSTREAM_BANK_FREEZE_V1.md`
commit `705bfa17b472fc3de096423908ed5414a2b41cfc`.

Independent pre-head review:
`AT0_EN_V26_R44B_PREHEAD_ADVERSARIAL_REVIEW_V1.md`
commit `2f3a2dca8400f4cc11e360c1918cd8e9a3dc2608`.

Key review conclusion:
- no disqualifying leakage defect found;
- nested DESIGN J0/J1 result must be treated as DEVELOPMENT MODEL-SELECTION EVIDENCE, not final unbiased generalization performance;
- architecture + threshold must be frozen before any later prospective VERIFY_INTERNAL access;
- boundary repair remains a separate later branch.

Higher-model review packet:
`AT0_EN_V26_R44B_HIGHER_MODEL_REVIEW_PACKET_V1.md`
commit `c7e72cc34af1033e0db55f04528c97e83a605267`.

Technical-only actual-data head mechanics run launched:
- run `37702502662`;
- workflow `R44-B actual nested-bank head mechanics`;
- trigger head `8830305f0c75c23d1a2443fa30d8f5d24cbf5916`;
- NO scientific head training;
- NO threshold evaluation;
- NO VERIFY_INTERNAL.

CURRENT EXACT CHECKPOINT:
`R44B_UPSTREAM_COMPLETE_AND_FROZEN -> ACTUAL_HEAD_MECHANICS_AUDIT_IN_PROGRESS -> HIGHER_MODEL_REVIEW_RECOMMENDED BEFORE FIRST J0_J1 SCIENTIFIC_RUN`.


---

## 2026-10-08 — R44-B actual head mechanics PASS

Technical-only run:
- run `37702502662`
- conclusion: SUCCESS
- state: `R44B_HEAD_ACTUAL_MECHANICS_PASS`
- artifact: `11517764421`
- digest: `sha256:80d77e63701c9ff80b6b4fc7e571b7b089fbd2120c3bf00693a1c9c9ce570455`

Actual frozen-data audit:
- candidate rows audited across all outer meta/eval files: `9,613`
- context physical SHA: `6bb548884cafb2a14e19b7d691b393dcf0ab9b5cc6add14e6ab0a873be33361b`
- context index SHA: `db9a6bae51a4db38d244e9e0a98f44b5dbfb246f694db5397c6e204cd58881dd`
- context shape: `26,595 x 768`, float32
- max observed candidate width: `45` (frozen embedding capacity =64)
- J0 parameters: `584,631`
- J1 parameters: `667,836`
- actual forward/backward finite on all five outer folds for both J0/J1
- scalar feature ranges valid and finite
- scientific head training performed: false
- threshold evaluation performed: false
- VERIFY_INTERNAL used: false
- old SELECT used: false
- protected data used: false

Quality delta:
`IMPROVED — ACTUAL FROZEN BANK/CACHE FEATURE MECHANICS FULLY VALIDATED`.

CURRENT EXACT CHECKPOINT:
`R44B_UPSTREAM_COMPLETE + ACTUAL_HEAD_MECHANICS_PASS -> HIGHER_MODEL_ADVERSARIAL_REVIEW -> RECONCILE -> IF CLEAR AUTHORIZE FIRST FROZEN J0/J1 NESTED SCIENTIFIC RUN`.

No J0/J1 scientific run has been consumed yet.


---

## 2026-10-08 — HIGHER-MODEL VERDICT ACCEPTED / I1-I2 CLOSURE IN PROGRESS

Higher-model independent verdict:
`PROCEED_WITH_NONSCIENTIFIC_IMPLEMENTATION_FIXES_ONLY`.

Durable adjudication:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R44B_HIGHER_MODEL_ADJUDICATION_V1.md`.

Scientific design remains frozen and unchanged:
- pair-exclusion B1;
- J0-first / J1-only-if-J0-fails;
- ordinary 5-way CE;
- seed 44;
- 10 fixed epochs;
- thresholds {0.80,0.85,0.90,0.95};
- no fitted calibration;
- no boundary repair;
- no VERIFY_INTERNAL.

### I2 documentation closure
Superseding clarifications were appended to:
- `AT0_EN_V26_R44B_B1_NESTED_PROTOCOL_FREEZE_V1.md`;
- `AT0_EN_V26_R44B_HIGHER_MODEL_REVIEW_PACKET_V1.md`;
- `AT0_EN_V26_R44B_PREHEAD_ADVERSARIAL_REVIEW_V1.md`.

Permanent corrected interpretation:
- pair jobs are computationally separable, statistically dependent;
- 10 physical pair fits are fixed-seed fitting equivalence to 20 logical directions, not independent replication;
- context computation is label-independent although source JSON physically contains tags;
- VERIFY_INTERNAL is historically exposed through parent R4.3 FIT/audits and split-statistic use; no R44 candidate-specific verification/tuning has occurred;
- mechanics run 37702502662 computed gradients on a tiny mixed development sample but made no optimizer/scheduler update and retained no learned state;
- mechanics objects/gradients/RNG continuation are forbidden from scientific initialization.

### I1 implementation created
- `r44b_head_train.py`
- `r44b_head_aggregate.py`
- `r44b_head_synthetic_closure.py`
- `.github/workflows/r44b_head_executor_closure.yml`

Executor invariants now include:
- canonical manifest-hash recomputation;
- fixed scientific attempt ID `R44B_B1_DEV_J0J1_ATTEMPT_1`;
- fresh model/optimizer/scheduler/RNG per fold/head;
- meta-only optimizer updates;
- eval + no_grad outer inference;
- final fixed epoch only;
- safetensors checkpoint;
- raw 5-way probability serialization;
- live epoch/step/loss/progress PROCESS_STATUS logs;
- physical checkpoint SHA verification;
- fail closed on missing/duplicate/nonfinite/unnormalized outputs;
- exactly 1942 aggregate probability rows per head;
- recall denominators P=271 I=829 C=115 O=677;
- deterministic >= thresholds, all-class gate, lowest passing threshold, J0-first rule;
- frozen Brier/ECE/reliability/risk-coverage diagnostic definitions;
- no score-driven retries/checkpoint shopping.

### Synthetic closure evidence
Earlier simpler closures:
- run `37704956922`: SUCCESS, superseded;
- run `37705160972`: SUCCESS, superseded.

Full-validator closure attempts:
- run `37705311699`: FAILURE;
- run `37705508807`: FAILURE.

Both failures are NONSCIENTIFIC fixture failures caused by writing literal `\\n` after synthetic JSON instead of a real newline, producing `JSONDecodeError: Extra data`. No real DESIGN nested head training occurred and no scientific attempt was consumed. The fixture encoding was repaired only; scientific trainer/evaluator semantics were not changed because of scores.

Current authoritative closure candidate:
- run `37705640579`;
- head `a20da0098d035a80219171b469033179830392a5`;
- state at this checkpoint: IN_PROGRESS;
- source-free/synthetic only.

CURRENT EXACT CHECKPOINT:
`R44B_UPSTREAM_FROZEN + HIGHER_MODEL_REVIEW_COMPLETE + I2_CLOSED + I1_EXECUTOR_IMPLEMENTED -> AUTHORITATIVE_SYNTHETIC_CLOSURE_37705640579_IN_PROGRESS`.

Scientific J0/J1 attempts consumed:
`0 / 1`.

NEXT:
`IF_37705640579_PASS -> FREEZE_EXECUTOR + CREATE/PIN SCIENTIFIC WORKFLOW -> ONE-SHOT 10-JOB DEVELOPMENT J0/J1 -> AGGREGATE -> FREEZE -> STOP BEFORE VERIFY_INTERNAL`.


---

## 2026-10-08 — R44-B B1 ONE-SHOT COMPLETE / NO ARCHITECTURE NOMINATED / CAUSAL DIAGNOSIS COMPLETE

### One-shot scientific result
Official scientific run:
- `37706558889`
- attempt ID: `R44B_B1_DEV_J0J1_ATTEMPT_1`
- workflow run_number=1
- run_attempt=1
- immutable precheck SUCCESS
- 10/10 fold/head jobs SUCCESS
- aggregate SUCCESS
- reruns=0
- replacement attempts=0

Scientific attempt is consumed and MUST NOT be repeated.

Aggregate artifact:
- `11520076582`
- digest `sha256:f2375a772cc045b2aad6e207747cfec9724b6e84549b3987855ae78e3565e761`

Frozen result:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R44B_B1_DEVELOPMENT_RESULT_FREEZE_V1.md`
commit `ce12eb09cec41b4d4eb7e22fa5584f8d5d590d89`.

Decision:
`NO_ARCHITECTURE_NOMINATED`
because neither J0 nor J1 passed the frozen gates.

Best J0:
- t=.95
- macro precision 0.845308610324185
- P precision 0.8729281767955801
- I precision 0.8
- C precision 0.88
- O precision 0.8283062645011601
- recalls all > .38.

Best J1:
- t=.95
- macro precision 0.8258277690482774.

No VERIFY_INTERNAL / old SELECT / protected data / fitted calibration / boundary repair / new thresholds / score-driven retry.

### Read-only causal diagnosis
Frozen diagnosis:
`AT0_EN_V26_R44B_B1_FAILURE_CAUSAL_DIAGNOSIS_V1.md`
commit `f7893debaea87a2763963d57e8c9a4276d3d9170`.

Dominant failure:
- J0 t=.95 FP=189;
- SAME_CLASS_WRONG_BOUNDARY=93;
- SPURIOUS_NO_OVERLAP=78;
- WRONG_TYPE_EXACT_COORD=14;
- EXACT_TYPED changed wrong=2;
- DIFFERENT_CLASS_WRONG_BOUNDARY=2;
- 90.48% of accepted J0 FPs are SAME_CLASS_WRONG_BOUNDARY or SPURIOUS_NO_OVERLAP.

Validity-separation diagnostic:
- J0 validity AUROC ~0.73284; AP ~0.85958.
- J1 validity AUROC ~0.72637; AP ~0.85865.

Type-only on the 1,406 valid exact-coordinate candidates:
- J0 P/I/C/O-only accuracy ~0.95092 vs five-way ~0.81366.
- J1 P/I/C/O-only accuracy ~0.95164 vs five-way ~0.81721.

Oracle-validity + existing J1 type-only argmax would satisfy all frozen class precision gates:
- P .98591549
- I .94444444
- C .92307692
- O .94943820
- macro .95071877.
This is DIAGNOSTIC ONLY, not an achieved model.

Existing B type + oracle validity still fails C precision (.87951807), so a pure validity veto keeping B type is insufficient.

Capacity/overfit evidence:
- J0 final per-fold train CE roughly .0060-.0157;
- J1 final per-fold train CE roughly .00067-.00102;
- J1 nearly memorized training but generalizes worse than J0 at every frozen threshold.

Causal verdict:
`VALIDITY_IDENTIFICATION_IS_THE_PRIMARY_NEXT_HYPOTHESIS`
and
`FACTORIZE_CANDIDATE_VALIDITY_FROM_PICO_TYPE_BEFORE_BOUNDARY_REPAIR_OR_CALIBRATION`.

This is a recommendation for review only. No new scientific fit is authorized.

### Literature triangulation
Read-only literature review considered:
- PICOX, JAMIA 2024, DOI 10.1093/jamia/ocae065 — invalid/composite span supervision and FP reduction;
- Liu et al., Neurocomputing 2022, DOI 10.1016/j.neucom.2022.07.012 — entity identification vs entity classification + hard negatives (mechanistic precedent);
- TSBECL, Expert Systems with Applications 2025, DOI 10.1016/j.eswa.2025.126707 — two-stage boundary-enhanced span classification;
- BGNER 2025, DOI 10.1007/s44443-025-00059-6 — boundary-aware span validation;
- OpenBioNER-v2 2026, DOI 10.1016/j.eswa.2026.131725 — boundary difficulty and rare-entity calibration risk.

### Next higher-model consultation packet
Prepared:
`AT0_EN_V26_POST_R44B_FACTORIZED_REVIEW_PACKET_V1.md`
commit `aa5d4e85d25ce371c48b5839b6cf6b97fab9802e`.

The packet asks the higher model to choose exactly one primary next intervention, explicitly comparing:
- low-capacity factorized VALID/INVALID + P/I/C/O type;
- factorized existing representation;
- boundary-first;
- hard-negative loss;
- calibration;
- simpler non-factorized head;
- fresh-data stop.

CURRENT EXACT CHECKPOINT:
`R44B_B1_ONE_SHOT_COMPLETE_NO_ARCHITECTURE_NOMINATED -> READ_ONLY_CAUSAL_DIAGNOSIS_COMPLETE -> HIGHER_MODEL_REVIEW_OF_FACTORIZED_NEXT_PROTOCOL_REQUIRED_BEFORE_ANY_NEW_SCIENTIFIC_FIT`.

Still CLOSED:
- VERIFY_INTERNAL;
- final refit;
- calibration fitting;
- boundary repair training;
- factorized-head training;
- alternate model training;
- all consumed FactPICO / 60-RCT evidence.


---

## 2026-10-08 — Late original R44-B independent-review archive reconciled

The user supplied the original external-review deliverables after the R44-B one-shot result was already frozen:
- standalone review Markdown;
- complete independent-review ZIP.

Verification:
- standalone and ZIP-embedded review are byte-identical;
- review SHA-256 `ec18268fc33ee18d4546bdf5a0c3b4480e4578ab411c7ba401ab70d4f30c3f1e`;
- included `verify_frozen_artifacts.py` was re-executed and reproduced `INDEPENDENT_ARTIFACT_IDENTITY_AND_NESTED_ROW_AUDIT_PASS`;
- all four retained evidence ZIP hashes matched;
- no contradiction with I1/I2 implementation, scientific run `37706558889`, frozen no-pass result, or causal diagnosis was found.

Durable audit:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R44B_LATE_INDEPENDENT_REVIEW_ARCHIVE_AUDIT_V1.md`
commit `e2aae5192100929393de7cd65b709fa16d28874b`.

The post-R44-B higher-model packet was updated to require reading this reconciliation before deciding the next experiment.

No scientific result was reopened and no new fit was authorized.


---

## 2026-10-08 — POST-R44B REVIEW RECONCILED / R44C LINEAR5 ONE-SHOT DISPATCHED

### Higher-model post-R44B review
Verdict:
`PROCEED_OTHER_SINGLE_INTERVENTION`.

The review rejected factorization as the next isolated intervention and selected exactly one regularized five-way linear verifier.

Key new counterevidence:
- five-way CE already contains validity supervision algebraically;
- on the same 1,406 exact-coordinate valid candidates, copy frozen upstream B type is correct 1,355/1,406 = 96.37268847795164%;
- J0 type-only = 1,337/1,406 = 95.09246088193457%;
- J1 type-only = 1,338/1,406 = 95.16358463726885%;
- J0 fixes 10 B-type errors but breaks 28 previously correct types;
- J1 fixes 12 but breaks 29;
- frozen outer NLL J0=1.210236485360117, J1=1.3734881421278318;
- tiny meta-training CE + worse J1 DEVELOPMENT generalization supports a bounded capacity/regularization test, not proof that factorization is required.

Independent reconciliation accepted the narrower intervention:
`R44C_LINEAR5_L2_V1`.

### R44C frozen design
- same nested META_TRAIN/EVAL banks;
- same five-way NONE/P/I/C/O target;
- exactly 3,918 fixed input dimensions;
- one linear W(5,3918)+b(5) model = 19,595 parameters;
- fold-local META-only scaling of 3,840 contextual + 5 scalar coordinates;
- mean 5-way CE + (0.01/2)||W||^2, bias unpenalized;
- deterministic float64 full-batch persistent L-BFGS;
- zero initialization;
- thresholds only {.80,.85,.90,.95};
- same per-class precision/recall/count + macro precision gates;
- no calibration, factorization, boundary repair, hard-negative weighting, alternate seed/model/lambda.

Reconciliation:
`AT0_EN_V26_R44C_LINEAR5_RECONCILIATION_V1.md`.

Protocol:
`AT0_EN_V26_R44C_LINEAR5_L2_PROTOCOL_FREEZE_V1.md`.

### Non-scientific implementation preflight
Historical implementation-only run `37725085094`:
- synthetic failed because test fixture lacked target;
- input audit failed because of output-directory ownership;
- no real scaler/model/optimizer; no attempt consumed.

Historical run `37725269768`:
- synthetic PASS;
- input audit failed on same output-directory lineage;
- no scientific attempt consumed.

Authoritative run:
`37725529491`
head `da82e68a796139fa67bec2f858d99dc604754473`.

All authoritative jobs SUCCESS:
- source-free synthetic closure;
- frozen-input structural audit;
- implementation closure.

Authoritative preflight artifacts:
- synthetic `11527033325`, digest `sha256:0797f900bfc01f769098b945d3bf9968d26a19d78b696b6f0a163679a158480d`;
- frozen input `11527950745`, digest `sha256:4b7cc1eadac2989784af900c08502ca1f433b1084c8a8af33e3b37302cc990dd`;
- implementation closure `11527138040`, digest `sha256:b3286ec5308d413dbc8c1c6a1705688c09464a958b3793022d8a76e32499521d`.

Synthetic verified:
- 3918 features;
- 19595 parameters;
- 3845 scaled coordinates;
- L2 excludes bias;
- analytic/autograd gradient agreement ~1e-16;
- L-BFGS convergence and nonconvergence fail-closed;
- logits/logp/probability consistency;
- complete synthetic aggregate;
- checkpoint tamper fail-closed;
- >= threshold and NONE-first ties.

Frozen-input audit:
- 9,613 rows structurally audited;
- EVAL total 1,942;
- max width 45;
- real META scaler computed=false;
- optimizer/model created=false;
- VERIFY_INTERNAL=false;
- scientific attempt consumed=false.

Execution freeze:
`AT0_EN_V26_R44C_LINEAR5_EXECUTION_FREEZE_V1.md`.

Authorization:
`AT0_EN_V26_R44C_LINEAR5_SCIENTIFIC_AUTHORIZATION_V1.md`.

### CURRENT SCIENTIFIC RUN
Run:
`37726111765`

Attempt:
`R44C_LINEAR5_L2_DEV_ATTEMPT_1`

Trigger head:
`57790d0fedcc0f42707584ca44118bcbe2fba531`

Workflow run_number=1 / run_attempt=1.

Immutable precheck:
SUCCESS.

Five fold jobs:
currently dispatched in parallel; no aggregate result yet at this handoff checkpoint.

Attempt consumption:
- pre-dispatch preflight consumed 0/1;
- once any fold performs its first real optimizer update, attempt is consumed and must never be automatically rerun.

NEXT:
`MONITOR_37726111765 -> IF_5_FOLDS_SUCCESS RUN_ONE_AGGREGATE -> FREEZE_PASS_OR_FAIL -> STOP`.

VERIFY_INTERNAL and all other protected/consumed evidence remain CLOSED.


---

## 2026-10-08 — R44C LINEAR5 one-shot COMPLETE / SCIENTIFIC FAIL / DESIGN ADAPTATION STOP

Official R44C scientific run:
- `37726111765`
- attempt `R44C_LINEAR5_L2_DEV_ATTEMPT_1`
- run_number=1 / run_attempt=1
- immutable precheck SUCCESS
- 5/5 outer folds SUCCESS
- aggregate SUCCESS
- reruns=0
- replacement folds=0

Aggregate:
- artifact `11528185923`
- digest `sha256:e2d1c4fec6106dd56c26e4f781428919dbef2e4e000565bb2563ec5800eee426`

Frozen result:
`AT0_EN_V26_R44C_LINEAR5_DEVELOPMENT_RESULT_FREEZE_V1.md`
commit `ae5f3ea563fda14e6beb71212d0d2c10562de044`.

Decision:
`NO_ARCHITECTURE_NOMINATED`.

Scientific verdict:
`R44C_LINEAR5_L2_SCIENTIFIC_FAIL`.

Best frozen operating point t=.95:
- macro precision = 0.8767348592080204
- P precision = 0.8918918918918919
- I precision = 0.8171091445427728
- C precision = 0.9318181818181818 PASS
- O precision = 0.8661202185792349
- P recall = 0.4870848708487085
- I recall = 0.3341375150784077
- C recall = 0.3565217391304348
- O recall = 0.46824224519940916
- accepted=897, TP=767, FP=130

Compared with frozen J0 t=.95:
- macro precision +0.0314262488838354
- FP reduced 189 -> 130 (-31.2169%)
- outer NLL improved 1.210236485360117 -> 0.9456049077876719
- validity AUROC improved only 0.7328427209613384 -> 0.7357526910256682
- ECE improved 0.20785530979613684 -> 0.17694525120735866
- C now passes precision .90, but P/I/O and macro still fail.

R44C t=.95 FP taxonomy:
- SAME_CLASS_WRONG_BOUNDARY 72
- SPURIOUS_NO_OVERLAP 49
- WRONG_TYPE_EXACT_COORD 6
- DIFFERENT_CLASS_WRONG_BOUNDARY 2
- EXACT_TYPED changed wrong 1
- target-NONE boundary/spurious = 123/130 = 94.6154%.

All five deterministic fits converged under the frozen gradient criterion in 145-150 LBFGS steps.

R44C attempt is consumed and MUST NOT be rerun.

Per the prospectively reviewed sole fallback, current policy is now:
`STOP_FURTHER_MODEL_THRESHOLD_LOSS_ADAPTATION_ON_DESIGN_AND_ACQUIRE_GENUINELY_FRESH_INDEPENDENTLY_ANNOTATED_DATA_UNDER_A_SEPARATELY_FROZEN_PLAN`.

NOT AUTHORIZED on current DESIGN:
- factorization;
- calibration;
- boundary repair;
- hard-negative/IoU loss;
- alternate lambda/model/seed;
- threshold expansion;
- any successor fit.

VERIFY_INTERNAL remains CLOSED.

CURRENT:
`R44C_ONE_SHOT_FAIL_FROZEN -> DESIGN_ADAPTATION_STOPPED -> PREPARE_FRESH_INDEPENDENT_DATA_ACQUISITION_PROTOCOL_ONLY`.
