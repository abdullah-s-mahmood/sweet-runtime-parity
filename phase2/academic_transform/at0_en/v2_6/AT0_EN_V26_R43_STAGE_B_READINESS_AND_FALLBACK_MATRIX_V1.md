# AT0 EN V2.6 — R4.3 Stage-B Readiness and Fallback Decision Matrix V1

Date: 2026-10-07
Status: PROSPECTIVE / NO STAGE-B TRAINING EXECUTED

## 1. Purpose

Use Stage-A wall-clock time to freeze the Stage-B implementation contract and the post-diagnostic decision tree BEFORE any H0/H1 result exists.

This file does not authorize a second concurrent scientific run.

## 2. Stage-A output contract required before Stage B

Stage B may start only if Stage A terminates successfully and freezes:

- FIT-only B candidate model safetensors hash;
- FIT-only C-boundary model safetensors hash;
- FIT-only C-type model safetensors hash;
- converted-base hash;
- exact split-manifest SHA256:
  `fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`;
- FIT inventory = 320 documents;
- B final fixed epoch = 10;
- C-boundary final fixed epoch = 3;
- C-type final fixed epoch = 3;
- no SELECT/historical DEV/test checkpoint selection;
- access guards proving protected evidence was not read.

Any model/hash/manfiest mismatch blocks Stage B.

## 3. Stage-B implementation invariants

### Shared data / ancestry
- Use the exact Stage-A ancestor artifacts only.
- Use the frozen FIT/SELECT manifest only.
- H0 and H1 receive identical FIT examples in identical deterministic order.
- H0 and H1 receive identical cached contextual features.
- Encoder remains frozen.
- No SELECT-derived hard-negative mining.
- No historical DEV use.

### Native FIT-error negative slot
Materialize only from FIT predictions produced by the frozen Stage-A B model.

For each gold-source example:
1. eligible native errors are B proposals that are not exact gold span+class;
2. exact coordinates matching another gold class keep the gold class rather than NONE;
3. prioritize overlap with source gold;
4. otherwise any same-sentence native error;
5. deterministic SHA256 tie-break;
6. if absent, use the already-reserved deterministic background fallback.

After materialization:
- apply gold precedence;
- deduplicate coordinates;
- freeze one final FIT example manifest SHA256;
- use the identical manifest for H0 and H1.

### Contextual features
From the frozen Stage-A C-boundary encoder on the complete sentence:
- start contextual vector;
- end contextual vector;
- span-interior contextual mean;
- previous word contextual vector;
- following word contextual vector;
- sentence-edge vector where needed;
- frozen width embedding scheme.

No cropped-content-only substitute is permitted.

### Heads
H0:
- contextual typed MLP only.

H1:
- exact same H0 path;
- plus the frozen class-specific biaffine start/end term.

No triaffine, repair, MRC, GlobalPointer, encoder fine-tuning, or auxiliary losses in this diagnostic.

## 4. Candidate-ceiling stop rule

Before judging H0/H1, compute native SELECT proposal ceiling from the FIT-only B model.

For each P/I/C/O report:
- gold count;
- exact span+class candidate TP availability;
- maximum candidate recall;
- candidate count;
- candidate FP count.

If for ANY class:
- maximum candidate recall < 0.20, OR
- fewer than 10 exact candidate TPs are even available,

then:
`STOP_H0_H1_AS_INSUFFICIENT_CANDIDATE_CEILING`

Interpretation:
the bottleneck is candidate generation/repair, not pair verification.

Preferred next branch:
`BOUNDARY/CANDIDATE_REPAIR` (BOPN / Locate-and-Label style).

## 5. Frozen H0/H1 scientific decision

Threshold grid:
`{0.80,0.85,0.90,0.95}`

Gate:
- exact span + exact class;
- precision >=0.90 for every P/I/C/O;
- recall >=0.20 for every P/I/C/O;
- accepted >=10 for every P/I/C/O;
- macro precision >=0.90.

For each H0/H1:
choose the LOWEST threshold that passes all gates.

Decision:
- neither passes -> `DIAGNOSTIC_NO_ARCHITECTURE_READY`
- H0 only -> nominate H0
- H1 only -> nominate H1
- both pass -> prefer H0 unless H1 improves macro recall >=0.02 absolute while preserving every gate.

No post-result threshold invention.

## 6. Prespecified diagnostic decomposition

Regardless of PASS/FAIL, freeze:

- exact TP/FP/FN per class;
- same-class wrong-boundary FP;
- different-class exact-boundary FP;
- different-class wrong-boundary overlap FP;
- spurious/no-overlap FP;
- TP retention versus pre-head C-style accepted roster;
- FP rejection versus pre-head C-style accepted roster;
- pair-head confidence distributions for TP and FP;
- candidate ceiling;
- errors stratified by negative-provenance analog where identifiable;
- document-cluster bootstrap descriptive uncertainty (2000 replicates, seed 42).

These analyses explain mechanism; they do not change selection.

## 7. Prospective fallback decision matrix

### Case A — H0 improves strongly and H1 adds little
Evidence pattern:
- H0 substantially improves precision/FP rejection versus legacy C;
- H1 difference is small or within uncertainty.

Interpretation:
missing contextual information / negative-distribution mismatch dominates; explicit biaffine interaction is not necessary.

Preferred next architecture if gate still missed:
`CONTEXTUAL JOINT NONE/P/I/C/O SPAN SCORER + STRONGER TRAIN-ONLY HARD NEGATIVES`

Do NOT escalate to triaffine merely for complexity.

### Case B — H1 materially outperforms H0
Evidence pattern:
- H1 has clearly better FP rejection or exact precision at comparable TP retention;
- especially same-class wrong-boundary FP reduction.

Interpretation:
explicit endpoint interaction contributes beyond context alone.

Preferred next architecture if gate still missed:
`BIAFFINE/TRIAFFINE JOINT PAIR SCORER`
with the same contextual and hard-negative principles.

### Case C — H0 and H1 both fail primarily because candidate ceiling is low
Interpretation:
verification is downstream of the real bottleneck.

Preferred next architecture:
`BOPN / BOUNDARY-OFFSET REPAIR`
or
`LOCATE-AND-LABEL STYLE CANDIDATE REPAIR`.

### Case D — precision becomes high but recall falls below the gate
Interpretation:
rejection is too conservative or native candidate recovery is insufficient.

Preferred next branch:
boundary repair before verification, not looser dev-tuned thresholds.

Potential final hybrid:
`B CANDIDATES -> BOUNDARY REPAIR -> CONTEXTUAL PAIR SCORER -> TYPED ACCEPT/REVIEW`.

### Case E — recall is adequate but P/I/O precision remains <0.90
Interpretation:
remaining error is verifier/type discrimination.

Preferred next branch:
- expand TRAIN-only native hard-negative coverage;
- joint NONE/P/I/C/O scoring;
- if H1 evidence supports it, biaffine/triaffine pair interaction.

### Case F — class C is the sole unstable class because of support
Do not introduce class-specific thresholds from SELECT.

Use:
- uncertainty reporting;
- future independently frozen resampling protocol if a new selection phase becomes scientifically necessary.

### Case G — H0/H1 both show little improvement over R4.2C
Interpretation:
context and simple pair interaction are not the dominant missing ingredients.

Next candidates, ranked prospectively:
1. BOPN boundary-offset prediction / repair;
2. GlobalPointer or broader token-pair/grid formulation;
3. MRC start-end matching;
4. triaffine joint boundary modeling;
5. stronger biomedical encoder only after structural alternatives.

## 8. Hybrid rule

A hybrid is justified only if frozen diagnostics show complementary error correction.

Example:
- repair recovers exact boundaries / recall;
- contextual pair scorer rejects residual false candidates.

Do not build a hybrid merely because two methods individually exist.

## 9. Methods retained for future comparison

Retain without forgetting:
- PICOX composite negatives;
- native model-error hard negatives;
- contextual MLP;
- biaffine;
- triaffine;
- BOPN;
- Locate-and-Label;
- MRC matching;
- GlobalPointer / grid / token-pair;
- joint NONE/P/I/C/O span scoring;
- boundary-repair + pair-scoring hybrid;
- stronger biomedical encoder;
- ensemble/uncertainty gating;
- LLM teacher/distillation as comparator/teacher only.

Canonical registry:
`ACAD_PASS_METHODS_REGISTRY.md`

## 10. Current stop boundary

While Stage A run `37535183682` is active:
- do not launch Stage B;
- do not launch another scientific training/evaluation;
- literature/design/code-readiness work is allowed;
- protected data remain closed.

NEXT_ACTION after successful Stage A:
`FREEZE_STAGE_A_IDENTITIES -> MATERIALIZE_FIT_NATIVE_ERRORS -> FREEZE_FINAL_H0_H1_MANIFEST -> RUN_ONE_STAGE_B_H0_VS_H1_DIAGNOSTIC`
