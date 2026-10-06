# AT0 EN V2.6 — R4.3 FIT/SELECT H0-vs-H1 Diagnostic Training Authorization V1

Date: 2026-10-07
Status: AUTHORIZED FOR EXACTLY ONE TRAIN-INTERNAL DIAGNOSTIC EXECUTION

## Basis

Higher-model verdict:
`RUN_ONE_MORE_TRAIN_ONLY_DIAGNOSTIC_BEFORE_ARCHITECTURE_SELECTION`

Canonical design:
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V1.md`
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V2.md`

Frozen preflight:
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_PREFLIGHT_FREEZE_V1.md`
- successful run `37534110955`
- artifact `11446235369`
- digest `sha256:84f9688be55f46dfc6d05cee638c7552e12e6ed0ccae63e3b6f2fc99a4478c94`
- state `R43_CONTEXTUAL_PAIR_PREFLIGHT_PASS`

No preflight blocker remains.

## Authorization

Authorize exactly one scientific TRAIN-internal H0-vs-H1 diagnostic under the frozen packet.

Execution is split into TWO SEQUENTIAL technical stages solely to stay within hosted-run time limits:

### Stage A — FIT-only ancestor construction
Train exactly once from the verified safe base:
- B candidate generator: FIT only, 10 fixed epochs;
- C boundary localizer: FIT only, 3 fixed epochs;
- C cropped type verifier: FIT only, 3 fixed epochs.

No SELECT, historical DEV, test, other-fold, FactPICO or consumed-holdout outcome may select an ancestor checkpoint.

Final fixed epoch only.

Freeze ancestor model hashes and the frozen FIT/SELECT manifest identity.

### Stage B — frozen H0/H1 comparison
Using ONLY the Stage-A frozen ancestors:
- materialize the prospectively specified native FIT-error negative slot;
- train H0 and H1 on the exact same FIT contextual example manifest;
- 10 fixed head epochs each;
- evaluate native SELECT proposals only;
- use only the existing threshold grid {0.80,0.85,0.90,0.95};
- apply the unchanged exact scientific gate;
- apply the frozen H0-vs-H1 tie-break;
- freeze all results.

No design/hyperparameter/negative-policy change is permitted between Stage A and Stage B based on intermediate model behavior.

## Split identity

Frozen split-manifest SHA256:
`fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`

FIT:
- 320 documents
- P/I/C/O = 342/1038/144/847

SELECT:
- 80 documents
- P/I/C/O = 92/290/37/221

## Stop rules

Technical failure:
freeze evidence; permit only a narrow scientifically neutral repair after root-cause audit.

Scientific diagnostic result:
- if neither H0/H1 passes -> STOP and use the frozen diagnostic to choose the next architecture;
- if one passes -> nominate it and STOP;
- if both pass -> use the already frozen H0/H1 tie-break and STOP.

In ALL cases:
STOP before historical DEV regression/readiness use and before every protected external test.

## Explicit prohibitions

Do not:
- redraw FIT/SELECT;
- use global historical B/C artifacts for SELECT;
- use historical DEV for checkpoint/threshold/model choice;
- tune head thresholds outside the frozen grid;
- alter the gate;
- perform seed shopping;
- unfreeze contextual encoder;
- add triaffine/repair/MRC/grid components during this diagnostic;
- read fold1 TEST or other folds;
- read EBM/COVID/AD protected external tests;
- use FactPICO;
- rerun the consumed 60-RCT holdout.

Current exact checkpoint:
`AUTHORIZED_R43_STAGE_A_FIT_ONLY_ANCESTORS_THEN_STAGE_B_H0_VS_H1_DIAGNOSTIC`
