# ACAD_PASS — R44-B B1 DEVELOPMENT Result Freeze V1

Date: 2026-10-08
User-facing completion time: approximately 03:15 Asia/Baghdad (UTC+3)

**State:** `R44B_B1_DEVELOPMENT_RESULT_FROZEN`

**Attempt:** `R44B_B1_DEV_J0J1_ATTEMPT_1`

**Final decision:** `NO_ARCHITECTURE_NOMINATED`

Reason:
`NEITHER_HEAD_PASSED_FROZEN_GATES`

This is a frozen DEVELOPMENT model-selection result. It is not an unbiased final generalization estimate.

## 1. One-shot execution identity

Workflow run:
- run ID: `37706558889`
- head SHA: `2f34066a16ec8b6540a4fae12cbf8b2d329a170f`
- workflow run number: 1
- workflow attempt: 1
- precheck: SUCCESS
- 10/10 scientific fold/head jobs: SUCCESS
- aggregate: SUCCESS
- reruns: 0
- replacement attempts: 0

Scientific attempt is now consumed.

No second J0/J1 attempt is authorized.

## 2. Aggregate artifact

Artifact:
- name: `r44b-head-development-aggregate-attempt1`
- artifact ID: `11520076582`
- ZIP digest: `sha256:f2375a772cc045b2aad6e207747cfec9724b6e84549b3987855ae78e3565e761`

Aggregate internal file SHA256:
- `R44B_HEAD_DEVELOPMENT_AGGREGATE.json`:
  `ee7000defd8e3bd357e94184f23c92f664082030461b368058116dd2205c7e9c`
- `R44B_J0_ALL_OUTER_PROBS.jsonl`:
  `e252cc6dddb43ab49b8fa9296f4e4ed9a77aa429e3c1453c9ca6cc97bf6e9a3e`
- `R44B_J1_ALL_OUTER_PROBS.jsonl`:
  `baada715ace50b989d9fb097cddb4b901d8c2ba4cf08c2cc5808b0d2371ed8c6`

Population:
- J0 rows: 1,942
- J0 unique candidate identities: 1,942
- J1 rows: 1,942
- J1 unique candidate identities: 1,942
- J0/J1 population identity: exact
- missing rows: 0
- duplicate rows: 0
- aggregate completeness checks: PASS

Canonical manifest SHA256:
`799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`

## 3. Frozen gate

Thresholds only:
`{0.80,0.85,0.90,0.95}`

Acceptance:
- five-way argmax;
- NONE is rejected;
- non-NONE accepted iff predicted-class probability `>= threshold`.

Authoritative recall denominators:
- P=271
- I=829
- C=115
- O=677

Per-class requirements:
- precision >= 0.90
- recall >= 0.20
- accepted >= 10

Overall:
- macro precision >= 0.90

Selection:
1. lowest passing threshold for J0;
2. if no J0 pass, lowest passing threshold for J1;
3. otherwise no nomination.

## 4. J0 frozen DEVELOPMENT results

No frozen threshold passed.

### threshold 0.80
- macro precision = 0.822526056434568
- accepted = 1286
- TP = 1040
- P: accepted 204, TP 174, FP 30, precision 0.8529411764705882, recall 0.6420664206642066
- I: accepted 514, TP 404, FP 110, precision 0.7859922178988327, recall 0.4873341375150784
- C: accepted 63, TP 53, FP 10, precision 0.8412698412698413, recall 0.4608695652173913
- O: accepted 505, TP 409, FP 96, precision 0.80990099009901, recall 0.604135893648449

### threshold 0.85
- macro precision = 0.8298353693417031
- accepted = 1240
- TP = 1009
- P: accepted 200, TP 173, FP 27, precision 0.865, recall 0.6383763837638377
- I: accepted 495, TP 391, FP 104, precision 0.7898989898989899, recall 0.47165259348612787
- C: accepted 61, TP 52, FP 9, precision 0.8524590163934426, recall 0.45217391304347826
- O: accepted 484, TP 393, FP 91, precision 0.8119834710743802, recall 0.5805022156573116

### threshold 0.90
- macro precision = 0.8349326756342574
- accepted = 1187
- TP = 972
- P: accepted 194, TP 169, FP 25, precision 0.8711340206185567, recall 0.6236162361623616
- I: accepted 467, TP 371, FP 96, precision 0.7944325481798715, recall 0.44752714113389624
- C: accepted 56, TP 48, FP 8, precision 0.8571428571428571, recall 0.41739130434782606
- O: accepted 470, TP 384, FP 86, precision 0.8170212765957446, recall 0.5672082717872969

### threshold 0.95
- macro precision = 0.845308610324185
- accepted = 1092
- TP = 903
- P: accepted 181, TP 158, FP 23, precision 0.8729281767955801, recall 0.5830258302583026
- I: accepted 430, TP 344, FP 86, precision 0.8, recall 0.4149577804583836
- C: accepted 50, TP 44, FP 6, precision 0.88, recall 0.3826086956521739
- O: accepted 431, TP 357, FP 74, precision 0.8283062645011601, recall 0.5273264401772526

Diagnostics:
- multiclass Brier = 0.48032509859898354
- top-class ECE = 0.20785530979613684
- candidate AP:
  - P = 0.9039410043841313
  - I = 0.7966668289840236
  - C = 0.7442626505780913
  - O = 0.8618450539746372

## 5. J1 frozen DEVELOPMENT results

No frozen threshold passed.

### threshold 0.80
- macro precision = 0.81798548512863
- accepted = 1314
- TP = 1057
- P: accepted 212, TP 179, FP 33, precision 0.8443396226415094, recall 0.6605166051660517
- I: accepted 515, TP 399, FP 116, precision 0.7747572815533981, recall 0.4813027744270205
- C: accepted 56, TP 47, FP 9, precision 0.8392857142857143, recall 0.40869565217391307
- O: accepted 531, TP 432, FP 99, precision 0.8135593220338984, recall 0.638109305760709

### threshold 0.85
- macro precision = 0.8222312725860149
- accepted = 1279
- TP = 1036
- P: accepted 203, TP 174, FP 29, precision 0.8571428571428571, recall 0.6420664206642066
- I: accepted 507, TP 393, FP 114, precision 0.7751479289940828, recall 0.47406513872135103
- C: accepted 54, TP 45, FP 9, precision 0.8333333333333334, recall 0.391304347826087
- O: accepted 515, TP 424, FP 91, precision 0.8233009708737864, recall 0.6262924667651403

### threshold 0.90
- macro precision = 0.8241715644154742
- accepted = 1227
- TP = 999
- P: accepted 197, TP 170, FP 27, precision 0.8629441624365483, recall 0.6273062730627307
- I: accepted 484, TP 376, FP 108, precision 0.7768595041322314, recall 0.45355850422195415
- C: accepted 52, TP 43, FP 9, precision 0.8269230769230769, recall 0.3739130434782609
- O: accepted 494, TP 410, FP 84, precision 0.8299595141700404, recall 0.6056129985228951

### threshold 0.95
- macro precision = 0.8258277690482774
- accepted = 1144
- TP = 937
- P: accepted 185, TP 159, FP 26, precision 0.8594594594594595, recall 0.5867158671586716
- I: accepted 448, TP 349, FP 99, precision 0.7790178571428571, recall 0.4209891435464415
- C: accepted 51, TP 42, FP 9, precision 0.8235294117647058, recall 0.3652173913043478
- O: accepted 460, TP 387, FP 73, precision 0.841304347826087, recall 0.5716395864106352

Diagnostics:
- multiclass Brier = 0.4789554448039467
- top-class ECE = 0.21391444913390736
- candidate AP:
  - P = 0.8852646532985539
  - I = 0.7864725461883513
  - C = 0.7235997958379051
  - O = 0.8706928026951172

## 6. Independent read-only recomputation

The aggregate raw-probability files were independently recomputed after artifact download.

Independent checks confirmed:
- 1,942 unique rows per head;
- same J0/J1 population;
- all four threshold tables above;
- exact frozen decision `NO_ARCHITECTURE_NOMINATED`.

No threshold, model, seed, checkpoint or population was changed.

## 7. First frozen failure localization

At threshold 0.95, J0 is the strongest frozen configuration by macro precision but still fails.

J0 accepted false positives at t=0.95:
- total FP = 189
- SAME_CLASS_WRONG_BOUNDARY = 93
- SPURIOUS_NO_OVERLAP = 78
- WRONG_TYPE_EXACT_COORD = 14
- EXACT_TYPED candidates changed to a wrong class by the head = 2
- DIFFERENT_CLASS_WRONG_BOUNDARY = 2

Thus:
- 171/189 = 90.47619047619048% of J0 accepted false positives at t=0.95 are either same-class wrong-boundary or spurious/no-overlap candidates.
- boundary/spurious rejection is therefore the dominant observed precision failure in the frozen high-confidence output.
- this does NOT yet prove that boundary repair is the correct next intervention; it establishes the dominant error composition requiring causal diagnosis.

J1 at t=0.95 is worse on macro precision and has 207 false positives:
- SAME_CLASS_WRONG_BOUNDARY = 106
- SPURIOUS_NO_OVERLAP = 81
- WRONG_TYPE_EXACT_COORD = 16
- EXACT_TYPED changed wrong = 2
- DIFFERENT_CLASS_WRONG_BOUNDARY = 2

## 8. Scientific interpretation

### What improved
The repaired nested OOF supervision and executor are now validly tested, with complete real upstream error exposure and no demonstrated stacking leakage.

Recall is not the immediate bottleneck:
- all per-class recalls at all frozen thresholds remain well above 0.20.

### What did not improve enough
Precision remains materially below the frozen 0.90 per-class floor.

Even J0 at t=0.95:
- macro precision = 0.845308610324185
- best per-class precision = 0.88 (C)
- P = 0.8729281767955801
- I = 0.8
- O = 0.8283062645011601.

J1 adds capacity but does not solve the gate:
- J1 is below J0 in macro precision at every frozen threshold.

### Calibration/ranking signal
The raw models are overconfident:
- J0 top-class ECE = 0.20785530979613684;
- J1 top-class ECE = 0.21391444913390736.

However this frozen experiment does NOT authorize post-hoc calibrated replacement or new thresholds.
These values are causal-diagnostic evidence only.

## 9. Guards

Confirmed:
- VERIFY_INTERNAL used = false
- old SELECT used = false
- protected data used = false
- fitted calibration = false
- boundary repair = false
- new thresholds = false
- score-driven retry = false
- second scientific attempt = false

## 10. Exact next boundary

The one-shot J0/J1 scientific comparison is consumed and MUST NOT be repeated.

Current authorized next work is read-only causal diagnosis of the frozen result.

STOP before:
- VERIFY_INTERNAL;
- final refit;
- calibration fitting;
- boundary repair training;
- alternative architecture training;
- changing thresholds/seed/epochs.

Any next scientific intervention must be prospectively justified and separately frozen after causal diagnosis.

Exact checkpoint:

`R44B_B1_ONE_SHOT_COMPLETE_NO_ARCHITECTURE_NOMINATED -> READ_ONLY_CAUSAL_DIAGNOSIS_ONLY`
