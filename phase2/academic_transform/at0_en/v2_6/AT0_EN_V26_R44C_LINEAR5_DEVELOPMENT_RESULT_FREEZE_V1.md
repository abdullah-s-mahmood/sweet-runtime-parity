# ACAD_PASS — R44C LINEAR5 L2 DEVELOPMENT Result Freeze V1

Date: 2026-10-08

**State:** `R44C_LINEAR5_L2_DEVELOPMENT_RESULT_FROZEN`

**Scientific verdict:** `R44C_LINEAR5_L2_SCIENTIFIC_FAIL`

**Decision:** `NO_ARCHITECTURE_NOMINATED`

**Attempt:** `R44C_LINEAR5_L2_DEV_ATTEMPT_1`

The single authorized R44C adaptive DEVELOPMENT attempt is complete and consumed.

No R44C rerun, replacement fold, alternate penalty, factorization, calibration, boundary repair, hard-negative objective, new threshold, new seed or successor model on DESIGN is authorized.

## 1. Official one-shot execution

Workflow run:
- `37726111765`
- trigger head SHA: `57790d0fedcc0f42707584ca44118bcbe2fba531`
- workflow run_number: 1
- workflow run_attempt: 1

Execution:
- immutable precheck: SUCCESS
- outer fold 0: SUCCESS
- outer fold 1: SUCCESS
- outer fold 2: SUCCESS
- outer fold 3: SUCCESS
- outer fold 4: SUCCESS
- DEVELOPMENT aggregate: SUCCESS
- reruns: 0
- replacement folds: 0

The first real optimizer update consumed the attempt.

## 2. Fold artifacts

- outer 0:
  - artifact `11527569388`
  - digest `sha256:3539ae839d2a496f6f641aae54b5f4b3cc3ba0cc6637a9df2f52979b193da8a1`

- outer 1:
  - artifact `11527986600`
  - digest `sha256:20b46555823c97c4a74f99887f6755a31dc88678c8d2055bc95b89931b708e64`

- outer 2:
  - artifact `11528011444`
  - digest `sha256:d6475fe29b991963b49531c644b8e2e7ac9e00e80709d97cc670218aefe04275`

- outer 3:
  - artifact `11527413405`
  - digest `sha256:9cf633a15905a8ffc5d30c8aefb10ace839d2fd6e00f106f6356f4895d4ea00e`

- outer 4:
  - artifact `11527034104`
  - digest `sha256:be72eaa6e892db2b69390f8621933d4d2f97ecfe77be1d93bf21b0f8b7a5615c`

All five fits converged under the prospectively frozen L-BFGS rule.

Optimizer steps:
- fold 0: 149
- fold 1: 147
- fold 2: 150
- fold 3: 147
- fold 4: 145

Final gradient infinity norms:
- fold 0: `6.56185930187745e-07`
- fold 1: `9.204440275047311e-07`
- fold 2: `8.781405323478038e-07`
- fold 3: `6.03064664165035e-07`
- fold 4: `9.40503795944352e-07`

Every fold is below the frozen `1e-6` numerical convergence threshold.

Final META_TRAIN CE:
- fold 0: 0.01451704044483049
- fold 1: 0.013769255378609785
- fold 2: 0.014130328240790897
- fold 3: 0.014096510285683421
- fold 4: 0.013543037039365956

Final penalized objective:
- fold 0: 0.04364898587967564
- fold 1: 0.04186122887427236
- fold 2: 0.04270856314055776
- fold 3: 0.04271099332148882
- fold 4: 0.041273610188009846

## 3. Aggregate artifact

Aggregate:
- artifact ID `11528185923`
- name `r44c-linear5-development-aggregate-attempt1`
- ZIP digest `sha256:e2d1c4fec6106dd56c26e4f781428919dbef2e4e000565bb2563ec5800eee426`

Internal file SHA256:
- `R44C_LINEAR5_DEVELOPMENT_AGGREGATE.json`
  `108b41b0271be5e876daf63183436ed1c79894e94ba03ccc3d94a37f57f29314`

- `R44C_LINEAR5_ALL_OUTER_PROBS_WITH_FROZEN_TARGETS.jsonl`
  `212fe1fe695f1c26b67453cb84f4a091784368ddbd3cf46e6714628526ae6da3`

- `OUTPUT_SHA256.txt`
  `8775ee4896a1244a7224b75c5408860269f2dece3ba8a5b69e3f4daafdfa2648`

- `SOURCE_SHA256.txt`
  `81a57083406f145cd56a8e54c2592f7a516fc3fcbd946ac4ef1dabe2581a3b1f`

Population:
- aggregate probability rows: 1,942
- unique candidate identities: 1,942
- missing rows: 0
- duplicate rows: 0

Independent read-only recomputation reproduced every threshold metric and the no-pass decision.

## 4. Frozen gates

Thresholds:
`{0.80,0.85,0.90,0.95}`

Acceptance:
- five-way argmax over NONE/P/I/C/O;
- reject NONE;
- accept non-NONE iff joint predicted-class probability >= threshold.

Authoritative gold denominators:
- P=271
- I=829
- C=115
- O=677

Required for every P/I/C/O:
- precision >= .90
- recall >= .20
- accepted >= 10

Also:
- macro precision >= .90

No frozen threshold passes.

## 5. Threshold 0.80

Macro precision:
`0.8350528000333263`

Accepted total:
1178

TP:
969

Per class:
- P: accepted 191, TP 164, FP 27, precision 0.8586387434554974, recall 0.6051660516605166
- I: accepted 471, TP 374, FP 97, precision 0.7940552016985138, recall 0.451145958986731
- C: accepted 55, TP 47, FP 8, precision 0.8545454545454545, recall 0.40869565217391307
- O: accepted 461, TP 384, FP 77, precision 0.8329718004338394, recall 0.5672082717872969

FAIL.

## 6. Threshold 0.85

Macro precision:
`0.8447520348899735`

Accepted total:
1116

TP:
929

Per class:
- P: accepted 179, TP 155, FP 24, precision 0.8659217877094972, recall 0.5719557195571956
- I: accepted 445, TP 357, FP 88, precision 0.802247191011236, recall 0.43063932448733416
- C: accepted 52, TP 45, FP 7, precision 0.8653846153846154, recall 0.391304347826087
- O: accepted 440, TP 372, FP 68, precision 0.8454545454545455, recall 0.5494830132939439

FAIL.

## 7. Threshold 0.90

Macro precision:
`0.8544744539271003`

Accepted total:
1038

TP:
874

Per class:
- P: accepted 171, TP 149, FP 22, precision 0.8713450292397661, recall 0.5498154981549815
- I: accepted 403, TP 328, FP 75, precision 0.8138957816377171, recall 0.3956574185765983
- C: accepted 50, TP 44, FP 6, precision 0.88, recall 0.3826086956521739
- O: accepted 414, TP 353, FP 61, precision 0.8526570048309179, recall 0.5214180206794683

FAIL.

## 8. Threshold 0.95 — strongest frozen operating point

Macro precision:
`0.8767348592080204`

Accepted total:
897

TP:
767

FP:
130

Per class:
- P:
  - accepted 148
  - TP 132
  - FP 16
  - precision `0.8918918918918919`
  - recall `0.4870848708487085`
  - precision gate FAIL

- I:
  - accepted 339
  - TP 277
  - FP 62
  - precision `0.8171091445427728`
  - recall `0.3341375150784077`
  - precision gate FAIL

- C:
  - accepted 44
  - TP 41
  - FP 3
  - precision `0.9318181818181818`
  - recall `0.3565217391304348`
  - class gate PASS

- O:
  - accepted 366
  - TP 317
  - FP 49
  - precision `0.8661202185792349`
  - recall `0.46824224519940916`
  - precision gate FAIL

Macro precision gate also FAIL because 0.8767348592080204 < .90.

Therefore:
`NO_ARCHITECTURE_NOMINATED`.

## 9. Threshold .95 error composition

Accepted FP taxonomy:
- SAME_CLASS_WRONG_BOUNDARY = 72
- SPURIOUS_NO_OVERLAP = 49
- WRONG_TYPE_EXACT_COORD = 6
- DIFFERENT_CLASS_WRONG_BOUNDARY = 2
- EXACT_TYPED changed wrong = 1

Total FP:
130

Target-NONE wrong-boundary/spurious groups:
- 72 + 49 + 2 = 123
- 123/130 = 94.61538461538461%

Thus invalid-candidate acceptance remains the dominant observed precision burden.

This does not authorize factorization, repair or a new model on DESIGN.

## 10. Diagnostic-only metrics

R44C:
- outer five-way NLL = `0.9456049077876719`
- validity AUROC using 1-p_NONE = `0.7357526910256682`
- validity AP = `0.8674648312474645`
- multiclass Brier = `0.4516047536380924`
- top-class ECE = `0.17694525120735866`
- conditional type accuracy = `0.9559032716927454`
- conditional type correct = 1344 / 1406
- copy-B conditional accuracy = `0.9637268847795164`
- copy-B correct = 1355 / 1406
- R44C type-only fixes of B errors = 16
- R44C type-only breaks of correct B types = 27

Per-fold validity AUROC:
- outer 0 = 0.7506072417104446
- outer 1 = 0.7308467741935484
- outer 2 = 0.7361454725383474
- outer 3 = 0.7643359951030856
- outer 4 = 0.6823931503470632

## 11. Predeclared mechanistic comparison to frozen J0

Historical J0:
- validity AUROC = 0.7328427209613384
- outer five-way NLL = 1.210236485360117
- best macro precision at t=.95 = 0.845308610324185
- t=.95 FP = 189

R44C:
- validity AUROC = 0.7357526910256682
- outer NLL = 0.9456049077876719
- best macro precision at t=.95 = 0.8767348592080204
- t=.95 FP = 130

Changes:
- validity AUROC: +0.0029099700643298
- outer NLL: -0.2646315775724451
- macro precision: +0.0314262488838354
- FP: -59, a 31.21693121693122% reduction

Per-class precision change at t=.95 versus J0:
- P: +0.0189637150963118
- I: +0.0171091445427728
- C: +0.0518181818181818
- O: +0.0378139540780748

Interpretation:
- lower-capacity regularized joint modeling materially improved NLL and high-confidence precision;
- validity ranking improved only marginally;
- C crosses the .90 class precision gate;
- P approaches but remains below .90;
- I and O remain materially below .90;
- the predeclared operational sufficiency claim is therefore falsified for this exact protocol.

A pass was NOT achieved.

## 12. Calibration and representation interpretation

R44C top-class ECE improved relative to frozen J0:
- J0 ECE = 0.20785530979613684
- R44C ECE = 0.17694525120735866

But fitted calibration remains unauthorized and cannot turn this failed frozen experiment into a pass.

The failure is not caused by insufficient recall:
all class recalls at t=.95 remain above .33.

Precision remains the blocker.

## 13. Scientific meaning

### Improved
Compared with the large J0/J1 heads:
- much lower trainable capacity;
- deterministic convex optimization;
- better outer NLL;
- lower ECE;
- higher best macro precision;
- 31.2% fewer high-confidence FPs;
- C precision now passes .90.

### Still failed
At the best frozen threshold:
- P precision = .89189 < .90
- I precision = .81711 < .90
- O precision = .86612 < .90
- macro precision = .87673 < .90.

Therefore the exact frozen acceptance objective is not met.

## 14. Guards

Confirmed:
- VERIFY_INTERNAL used = false
- old SELECT used = false
- protected data used = false
- fitted calibration = false
- boundary repair = false
- factorization = false
- hard-negative weighting = false
- new thresholds = false
- score-driven retry = false
- replacement fold = false
- scientific rerun = false

## 15. Attempt ledger

`R44C_LINEAR5_L2_DEV_ATTEMPT_1` is CONSUMED.

It MUST NOT be rerun.

The R44B J0/J1 attempt is also already consumed and remains frozen.

## 16. Sole predeclared fallback now activates

The independently reviewed R44C protocol predeclared exactly one fallback if R44C fails:

`STOP_FURTHER_MODEL_THRESHOLD_LOSS_ADAPTATION_ON_DESIGN_AND_ACQUIRE_GENUINELY_FRESH_INDEPENDENTLY_ANNOTATED_DATA_UNDER_A_SEPARATELY_FROZEN_PLAN`.

This fallback is now active.

Therefore the following are NOT authorized on the current DESIGN data:
- factorized validity/type fit
- boundary repair fit
- calibration fit
- hard-negative/IoU objective
- alternate L2 coefficient
- alternate linear model
- nonlinear successor
- threshold extension
- new seed
- extra fold/model rerun
- post-hoc acceptance rule

## 17. VERIFY_INTERNAL remains closed

Do NOT open VERIFY_INTERNAL now.

Its historical exposure means it is not an external fresh benchmark, and the current frozen fallback specifically calls for genuinely fresh independently annotated data before further adaptive model development/final generalization claims.

Any later VERIFY_INTERNAL use requires a separate decision after a full future procedure is frozen; it cannot rescue R44C.

## 18. Exact checkpoint

`R44C_LINEAR5_L2_ONE_SHOT_COMPLETE_SCIENTIFIC_FAIL -> STOP_ADAPTING_DESIGN -> PREPARE_FRESH_INDEPENDENT_DATA_ACQUISITION_PROTOCOL`

No further scientific fit on DESIGN is authorized.
