# MP-SEF P3_V1 STAGE1 RUNTIME DEPENDENCY FAILURE TRIAGE V1

Date: 2026-10-01
Run: `36876431628`
Head SHA: `9e7e2e0c2a32f6a62cc2e473260644e1359aa4a3`
Conclusion: FAILURE BEFORE FIRST P3 INFERENCE

## Observed failure

The Stage1 workflow successfully completed:
- frozen Stage1 packet download and identity verification;
- frozen P1 parent artifact download and identity verification;
- SWEET runtime base installation;
- frozen text-editing revision checkout;
- exact Pnx revision download and weight verification.

The monitored P3 runner then failed before creating the first progress state and before any P3 proposal inference.

Primary exception:

`ModuleNotFoundError: No module named 'datasets'`

Additional runtime warning:

PyTorch 1.12.1 reported failure to initialize NumPy because the environment had an incompatible NumPy API version.

## Classification

Primary:
`RUNTIME / DEPENDENCY PARITY FAILURE`

Not:
- P3 model-quality failure;
- Pnx model failure;
- P1 parent-identity failure;
- packet identity failure;
- batch/single parity failure;
- source-length/truncation failure;
- gold/reference failure.

## Execution progress

P3 Stage1 inference work units completed:
`0 / 144 = 0%`

No P3 proposal row was produced.

No Stage1 output artifact was produced.

## Root cause

The new P3 workflow installed only the minimal direct model packages:

- torch 1.12.1+cpu
- transformers 4.30.0
- huggingface_hub 0.16.4
- sentencepiece 0.1.99

However, the frozen `CAMeL-Lab/text-editing` code path imported by `install_rewrite_compat()` transitively imports `datasets` through `gec/utils/data_utils.py`.

The historical frozen P1 workflow had already established a working runtime containing:

- numpy==1.23.5
- pandas==1.5.3
- pyarrow==14.0.2
- datasets==2.14.7
- editdistance==0.8.1

The P3 workflow failed because it did not reproduce that already-proven frozen P1 dependency stack.

## Reproducibility

Failure run:
`36876431628`

Failure occurred deterministically during import of frozen text-editing code, before model inference.

## Scope

Affected:
P3 V1 Stage1 runtime bootstrap only.

Not affected:
- frozen P1 artifact;
- frozen P3/Pnx identity;
- P2_V2 Stage1 result;
- Stage1 packet;
- V3 historical artifacts;
- scorer V3;
- any gold/reference data.

## Confidence

Root-cause confidence:
**HIGH**

The missing dependency is explicit in the traceback, and the historical P1 workflow provides the exact previously successful dependency set.

## Repairability

`CURRENT_CYCLE_PRE_OUTPUT`

The repair is allowed because:
- no P3 project-source output has yet been produced;
- no P3 parity result exists;
- no P3 Stage1 artifact has been frozen;
- the repair restores dependency parity with the already-frozen P1 runtime rather than changing model behavior or evaluation thresholds.

## Safe repair

Update the P3 workflow to install the exact additional packages used by the frozen P1 workflow:

`numpy==1.23.5 pandas==1.5.3 pyarrow==14.0.2 datasets==2.14.7 editdistance==0.8.1`

Do not change:
- P1 parent artifact;
- Pnx revision/weights;
- packet;
- batch size;
- parity subset;
- protection policy;
- quality/evaluation policy.

Then rerun P3 Stage1 from 0/144.

## Scientific interpretation

This failure is neutral with respect to linguistic performance.

It is an implementation/reproducibility defect and does not reduce confidence in P3 model quality.

It does strengthen the need to bind new workflows to historically proven dependency locks.
