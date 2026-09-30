# MP-SEF TRAINING-OVERLAP AUDIT V1

Date: 2026-09-30
Status: FROZEN PRE-MEASUREMENT AUDIT
Scope: allowed CALIBRATION metadata + public proposer provenance
No candidate-union metric was computed.

## 1. CALIBRATION composition

Frozen CALIBRATION artifact:
- run: 36654588477
- artifact: 11070819539
- digest: sha256:ab5f303b4405162684d9a8ece23c0ed378b25e7863129a284f3e65ca0844058a
- total records: 6,888

By original QALB-2014 split:
- train: 6,571
- dev: 317

Percentages:
- train: 95.3978%
- dev: 4.6022%

No QALB-2014 test records are present in this CALIBRATION artifact.

## 2. P1 training provenance

P1:
CAMeL-Lab/text-editing-qalb14-nopnx

Public model card states the model was fine-tuned using QALB-2014.

ACL 2025 SWEET paper states that for QALB-2014 the edit taggers are trained exclusively on QALB-2014 using the public splits, with QALB-2014 Train/Dev/Test reported separately.

The training-edit vocabulary and OOV analysis explicitly distinguish training edits from the QALB-2014 Dev set.

Therefore:
- QALB-2014 train records in CALIBRATION must be treated as known training-domain overlap and likely direct fine-tuning overlap for P1;
- QALB-2014 dev records are not treated as training records, but are model-development/evaluation-exposed in the published workflow.

Primary public sources:
- https://huggingface.co/CAMeL-Lab/text-editing-qalb14-nopnx
- https://aclanthology.org/2025.acl-long.875/

## 3. P2 training provenance

P2:
CAMeL-Lab/arabart-qalb14-gec-ged-13
with CAMeL-Lab/camelbert-msa-qalb14-ged-13.

Public P2 model card states the GEC model was fine-tuned using QALB-2014.

EMNLP 2023 paper reports QALB-2014 as:
- Train-L1;
- Dev-L1;
- Test-L1;
and uses the public train/dev/test organization for model development/evaluation.

Therefore:
- QALB-2014 train records in CALIBRATION must be treated as known training-domain overlap and likely direct fine-tuning overlap for P2;
- QALB-2014 dev records are not treated as training records, but are model-development/evaluation-exposed.

Primary public sources:
- https://huggingface.co/CAMeL-Lab/arabart-qalb14-gec-ged-13
- https://aclanthology.org/2023.emnlp-main.396/

## 4. Consequence for the proposed 30/40/30 split

A blind 30/40/30 split across all 6,888 CALIBRATION records would place approximately 95% training-split records in every role.

That would be acceptable only for:
- implementation development;
- action-space debugging;
- selector training/development;
- explicitly in-sample capacity diagnostics.

It is not a defensible primary measure of proposer generalization.

In particular, a high R_joint on a role partition dominated by QALB-2014 train could reflect memorization or fine-tuning exposure.

## 5. Revised role principle

The higher-model recommendation to separate future roles remains valid, but training-split provenance must be incorporated.

The first candidate-availability feasibility endpoint should not mix QALB-2014 train and dev as if they have the same evidential status.

Proposed role use before any measurement:

### D_DEV_FEAS

Population:
the 317 CALIBRATION records whose original split is dev.

Purpose:
developmental proposer-feasibility measurement only.

Limitations:
- not historically untouched;
- already used by prior ACAD_PASS CALIBRATION work;
- model developers used QALB-2014 Dev for evaluation/model development;
- therefore not an independent test of generalization.

Nevertheless, it avoids direct QALB-2014 training-split contamination and is more interpretable than a train-dominated random feasibility split.

### D_TRAIN_DEV

Population:
the 6,571 CALIBRATION records whose original split is train.

Purpose:
future selector development / engineering diagnostics only if later authorized.

Do not use as primary proposer-generalization evidence.

### D_RISK_INTERNAL

If a future risk-calibration partition is carved from D_TRAIN_DEV, it is internal development calibration only.

It cannot certify AUTO_SAFE 98% precision independently because proposer training overlap remains.

## 6. Independent certification

No currently allowed CALIBRATION subset can support an independent generalization or AUTO_SAFE certification claim.

Any future independent certification requires separately authorized evidence not used for proposer training/model selection and not adaptively consumed by ACAD_PASS.

This audit does not authorize opening:
- QALB14 test;
- QALB15 TEST;
- INTERNAL_EVALUATION;
- STRESS_DIAGNOSTIC;
- Confirmation;
- Holdout;
- A7'ta reserve;
- reserved Nahw IDs.

## 7. Decision

The previously proposed generic 30/40/30 split over all CALIBRATION records is:
**MODIFIED BEFORE MEASUREMENT**

Reason:
training-overlap confounding.

The 30/40/30 principle may still be used later inside development-only data for selector-role separation, but it must not define the primary P1+P2 proposer-feasibility population.

## 8. Exact next protocol amendment

Before any union/candidate metric:
1. set the primary feasibility population to the frozen QALB-2014 dev-origin subset within CALIBRATION;
2. label the result DEVELOPMENTAL / NOT INDEPENDENT;
3. keep all QALB-2014 train-origin records out of the primary feasibility denominator;
4. keep training-origin records available only for later development roles if separately authorized;
5. retain the higher-model bundle, R_joint, exposure, stop-rule, and protection requirements unchanged.

No candidate metric has been observed during this audit.
