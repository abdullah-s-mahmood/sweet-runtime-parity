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
