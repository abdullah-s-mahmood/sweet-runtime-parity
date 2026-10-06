# AT0-EN V2.6 R4.2C — Boundary-Consensus Training Protocol V1

Date: 2026-10-06
Status: FROZEN BEFORE R4.2C TRAINING
Branch: `at0-en-v2.6-dev`

## 1. Authorization basis

R4.2C design:
`AT0_EN_V26_R4_2C_BOUNDARY_CONSENSUS_DESIGN_V1.md`

R4.2C preflight:
- run `37447124232`
- artifact `11404450510`
- artifact digest `sha256:f975a0f251bcfd392af49b7227678f7162ad55f7cd970d530083fdf5202868b1`
- canonical pre-hash `e27f70e2db357f289b00d174f1ac7a2d2685c2ad57ee02d841e3c850e3d2fbb5`
- state `R4_2C_PREFLIGHT_READY`

No R4.2C training occurred before this protocol freeze.

## 2. Scientific objective

R4.2C is NOT a replacement extractor and does NOT relax the exact-span gate.

It is a selective, architecturally different verifier for frozen R4.2B candidates.

Primary target:
`HIGH_CONFIDENCE_BOUNDARY_AND_TYPE_DISAGREEMENT`

R4.2B remains the candidate BIO witness.
R4.2C may only reduce automatic acceptance by requiring independent boundary/class consensus.
Any disagreement becomes REVIEW.

## 3. External architecture anchor

The implementation is source-inspired by PICOX:
- class-agnostic boundary localization;
- separate span classification;
- low boundary threshold for candidate generation;
- downstream span-class evidence.

PICOX source code uses five boundary labels:
`OUT / START / END / BOTH / IN`.

PICOX boundary model source settings:
- learning rate `5e-5`
- epochs `3`
- weight decay `0.01`
- default Trainer batch size `8`

PICOX span-classifier source settings:
- learning rate `2e-5`
- train/eval batch size `16`
- epochs `3`
- weight decay `0.01`
- best checkpoint selected on frozen validation loss.

PICOX explores low boundary thresholds and includes `0.25`.
For ACAD_PASS, `0.25` is frozen solely as a boundary-candidate-generation threshold, NOT as an automatic-acceptance threshold.

References:
- Zhang G et al. JAMIA 2024. DOI: 10.1093/jamia/ocae065.
- Official implementation: WengLab-InformaticsResearch/PICOX.

## 4. Frozen model identity and safety path

Do NOT switch to PubMedBERT-large.

Use the already validated ACAD_PASS base:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract`
revision:
`d673b8835373c6fa116d6d8006b33d48734e305d`

Safe loading:
`Flax base -> BertModel -> safetensors -> task head`

Expected converted base safetensors:
`3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68`

Forbidden:
- pickle `pytorch_model.bin`
- silent model-family change
- test-driven model selection.

Boundary localizer and span classifier MUST be independently initialized from the same frozen safe base rather than from R4.2B fine-tuned weights.

## 5. Frozen data

Train:
SHA-256 `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`
1576 sentences.

Development:
SHA-256 `3b12534fedec35660587e6a5084b0b8ff11267c1da4a2f5afe9aa16c4941340a`
205 sentences.

R4.2B candidate model:
SHA-256 `3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c`

All EBM/COVID/AD future test files remain CLOSED.
FactPICO and the consumed 60-RCT holdout remain CLOSED.

## 6. Module A — boundary localizer

Task:
five-way token boundary classification:
- `OUT`
- `START`
- `END`
- `BOTH`
- `IN`

Gold construction is deterministic from train BIO spans and does not use development examples.

Hyperparameters:
- seed `42`
- learning rate `5e-5`
- epochs `3`
- weight decay `0.01`
- train batch `8`
- eval batch `8`
- AdamW
- linear scheduler
- max sequence length `256`
- deterministic algorithms where supported
- selected checkpoint: lowest frozen-dev boundary loss; ties -> earliest epoch.

Boundary probabilities:
- start probability = `P(START) + P(BOTH)`
- end probability = `P(END) + P(BOTH)`

Candidate-generation threshold:
`BOUNDARY_GENERATION_THRESHOLD = 0.25`

For an R4.2B candidate span `[start,end)` to receive boundary consensus:
- `start_prob[start] >= 0.25`
- `end_prob[end-1] >= 0.25`
- span width <= `64`.

The 64-token capacity is frozen from preflight:
- train max gold width = 54
- dev max gold width = 30
therefore all observed train/dev gold spans fit without truncating gold span width.

The boundary threshold is binary feasibility evidence only; it is NOT part of the final scientific precision gate.

## 7. Module B — span class verifier

Input:
the exact token sequence of each candidate span.

Classes:
`P / I / C / O`

Do NOT collapse `C` into `I`.
Do NOT add a test-tuned class.

Training positives:
all exact gold train spans.

Classifier:
four independent sigmoid outputs (one-hot targets in this non-overlapping CoNLL representation), preserving the source-inspired multi-label formulation while keeping `C` explicit.

Hyperparameters:
- seed `42`
- learning rate `2e-5`
- epochs `3`
- weight decay `0.01`
- train batch `16`
- eval batch `16`
- AdamW
- linear scheduler
- max sequence length `64` span tokens plus model special tokens
- selected checkpoint: highest frozen-dev macro-F1; tie -> lower dev loss; second tie -> earlier epoch.

No lexical rules or dev-specific span rewrites are permitted.

## 8. Frozen consensus rule

Evaluate only frozen R4.2B candidate entities.

For threshold `t` in the pre-existing frozen grid:
`{0.80, 0.85, 0.90, 0.95}`

An R4.2B candidate can become R4.2C automatic witness evidence only if ALL are true:

1. R4.2B entity confidence >= `t`.
2. Exact candidate start has boundary start probability >= `0.25`.
3. Exact candidate end has boundary end probability >= `0.25`.
4. Candidate width <= `64`.
5. Span classifier probability for the SAME R4.2B class >= `t`.
6. No other span class has probability >= `t`.
7. No deterministic critical contradiction exists.

Final consensus confidence:
`min(R4.2B_entity_confidence, span_classifier_same_class_probability)`

Boundary probabilities are not multiplied into this confidence; they are an independently frozen candidate-generation/consensus gate.

Any failed condition -> `REVIEW`.
R4.2C cannot create a new candidate absent from R4.2B and cannot override REJECT caused by a critical deterministic contradiction.

## 9. Frozen development calibration gate

Choose the LOWEST `t` in:
`{0.80,0.85,0.90,0.95}`
that satisfies all:

- precision >= `0.90` for each P/I/C/O
- recall >= `0.20` for each P/I/C/O
- accepted >= `10` for each P/I/C/O
- macro precision >= `0.90`

Exact span + exact class is the only TP definition.

Partial overlap remains diagnostic only.

If no threshold passes:
`R4_2C_BOUNDARY_CONSENSUS_NOT_READY`

If one passes:
`R4_2C_BOUNDARY_CONSENSUS_CALIBRATED`

No threshold, gate, data split, or metric may be changed after observing R4.2C development results.

## 10. Progress observability

Training workflow MUST persist and emit `PROCESS_STATUS.json`.

Required fields:
- state
- progress_percent
- current_stage
- active_module
- current_epoch / max_epochs
- global_step / total_steps when available
- latest_loss
- latest_dev_metric
- best_metric/checkpoint
- completed_units / total_units
- elapsed_seconds
- last_progress_at
- next_expected_step
- failure_or_stall_reason.

Overall progress:
- boundary training = units 1–3 of 7
- span classifier training = units 4–6 of 7
- consensus calibration = unit 7 of 7.

## 11. Evidence and stop boundary

Always freeze:
- runtime
- trainer script SHA
- train/dev hashes
- model base hashes
- boundary model safetensors hash
- span classifier safetensors hash
- R4.2B source model hash
- calibration summary
- PROCESS_STATUS
- output manifest.

After development calibration:
STOP.

Do NOT open EBM/COVID/AD tests until a separate explicit authorization after a passing R4.2C development gate.

## 12. Exact next step

Implement the frozen R4.2C trainer/evaluator and a mechanics/smoke workflow.

No scientific training trigger may be launched until:
1. implementation exists;
2. mechanics/smoke passes;
3. all identity/guard checks pass.
