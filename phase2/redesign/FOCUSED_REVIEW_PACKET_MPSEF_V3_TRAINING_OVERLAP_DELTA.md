# FOCUSED DELTA REVIEW PACKET — MP-SEF V3 Training-Overlap Amendment

Date: 2026-09-30
Purpose: independent review of one protocol change discovered AFTER the first higher-model review but BEFORE any P1+P2 feasibility metric.

Status:
- no candidate-union measurement run;
- no R_joint observed;
- no selector trained;
- no reserved/internal dataset opened.

## 1. Prior independent review decision

The prior higher-model review concluded:

MODIFY PROTOCOL BEFORE UNION MEASUREMENT

It recommended, among other changes:
- R_joint as primary candidate-availability endpoint;
- bundle/dependency representation;
- explicit exposure ledger;
- exact stop rules;
- a future role split of CALIBRATION proposed as 30% feasibility / 40% selector development / 30% risk calibration.

The reviewer explicitly noted that repartitioning previously consumed CALIBRATION would not restore historical independence.

## 2. New fact discovered after that review

The frozen CALIBRATION artifact was inspected by allowed metadata only.

Total:
6,888 records.

Original QALB-2014 split composition:
- train-origin: 6,571
- dev-origin: 317

Thus:
- 95.3978% train-origin
- 4.6022% dev-origin

No QALB-2014 test records are in this artifact.

## 3. New proposer-training provenance verification

### P1

Model:
CAMeL-Lab/text-editing-qalb14-nopnx

Public model card states:
the model was fine-tuned using QALB-2014.

ACL 2025 SWEET paper states:
for QALB-2014, edit taggers are trained exclusively on QALB-2014 under the public train/dev/test setup; the paper explicitly distinguishes training edits from QALB-2014 Dev OOV evaluation.

Sources:
- https://huggingface.co/CAMeL-Lab/text-editing-qalb14-nopnx
- https://aclanthology.org/2025.acl-long.875/

### P2

Model:
CAMeL-Lab/arabart-qalb14-gec-ged-13
with CAMeL-Lab/camelbert-msa-qalb14-ged-13

Public GEC model card states:
the model was fine-tuned using QALB-2014.

EMNLP 2023 paper explicitly describes:
- QALB-2014 Train-L1
- Dev-L1
- Test-L1

Sources:
- https://huggingface.co/CAMeL-Lab/arabart-qalb14-gec-ged-13
- https://aclanthology.org/2023.emnlp-main.396/

## 4. Consequence

A blind 30/40/30 partition over all 6,888 CALIBRATION records would put approximately 95% QALB-2014 train-origin records in each role.

Therefore the originally proposed feasibility subset would be dominated by records from the training split used to fine-tune the proposers.

A high candidate-availability result on such a subset could be materially optimistic.

No P1+P2 feasibility metric was observed before identifying this problem.

## 5. Additional duplicate audit

Frozen source-only duplicate rule:
- Unicode NFC;
- whitespace-normalized duplicate key;
- token-set Jaccard >=0.90;
- shorter/longer word-count ratio >=0.90;
- connected components.

Observed across all 6,888:
- total clusters: 6,871
- non-singleton clusters: 15
- max cluster size: 4
- near-duplicate edges: 20
- dev-origin clusters: 317
- train/dev crossing clusters: 0

Therefore none of the 317 dev-origin records is linked to a train-origin record by this frozen duplicate rule.

## 6. Amendment made BEFORE measurement

Primary candidate-feasibility population was changed to:

D_DEV_FEAS_V1

Membership:
- exactly the 317 dev-origin CALIBRATION records;
- 317 clusters;
- zero train-origin records;
- zero frozen duplicate-cluster overlap with train-origin population.

Label:
DEVELOPMENTAL / DEV-ORIGIN / NOT INDEPENDENT

Why not independent:
- ACAD_PASS already used CALIBRATION adaptively;
- QALB-2014 Dev was used by original model developers for model development/evaluation;
- this is not a blind test.

Train-origin records are moved out of the primary gate:

D_TRAIN_INTERNAL_V1
- 6,571 records;
- development/internal use only if later authorized;
- not primary candidate-generalization evidence.

The prior 30/40/30 split is deferred to future selector-role design and is NOT applied before candidate feasibility.

## 7. What remains unchanged from the first review

Still frozen:
- P1+P2 only;
- no third proposer;
- R_joint primary endpoint;
- >=95% candidate-availability floor;
- bundles/dependencies;
- original-source anchoring;
- protected-invariant contract;
- raw/joint/clean and family secondary metrics;
- no selector if candidate gate fails;
- no AUTO_SAFE authorization;
- no reserved data;
- strict anti-loop stop rules.

## 8. Manifest/preflight status

Source-only manifest generation has already been completed without running P1 or P2 on the feasibility population and without computing any candidate metric.

Preflight:
PASS

Verified:
- total 6,888
- train 6,571
- dev 317
- total clusters 6,871
- dev clusters 317
- cross-split clusters 0
- D_DEV_FEAS_V1 size 317
- training-origin records in D_DEV_FEAS_V1: 0
- candidate_metric_computed=false
- reference_content_used_for_manifest_generation=false
- gold_edit_content_used_for_manifest_generation=false
- INTERNAL_EVALUATION opened=false
- STRESS_DIAGNOSTIC opened=false
- reserved_data_opened=false

## 9. Exact methodological questions

Please review ONLY this delta and its implications.

1. Is replacing a generic 30/40/30 CALIBRATION split with D_DEV_FEAS_V1 (317 dev-origin cases) methodologically preferable for the first P1+P2 candidate-availability measurement?

2. Given both models were developed on QALB-2014 and QALB-2014 Dev was used for evaluation/model development, is a dev-origin measurement still scientifically interpretable as:
   DEVELOPMENTAL candidate feasibility,
   while explicitly NOT claiming independent generalization?

3. Is 317 dev-origin sentences an acceptable primary population for a one-shot R_joint feasibility gate, provided:
   - exact target counts are reported;
   - cluster-aware uncertainty is reported as diagnostic only;
   - family routes become N/A when support is insufficient;
   - no threshold is changed afterward?

4. Should the >=95% R_joint floor remain unchanged on D_DEV_FEAS_V1?

5. Would using any QALB-2014 train-origin record in the primary R_joint gate be methodologically worse because of direct proposer-training overlap?

6. Should train-origin data remain entirely outside the primary feasibility decision and be reserved only for possible future selector development?

7. Is an external corpus that neither proposer was trained on REQUIRED BEFORE this developmental feasibility measurement, or only before stronger generalization/AUTO_SAFE claims?

8. Does the absence of frozen near-duplicate train/dev clusters materially reduce one contamination risk, while still leaving model-development exposure?

9. Does this delta require any change to:
   - R_joint definition;
   - bundle contract;
   - protected-invariant contract;
   - stop rules;
   - proposer-retention rules?

10. Choose one:
   A. ACCEPT AMENDMENT — proceed later with one D_DEV_FEAS_V1 R_joint feasibility run under the frozen V3 protocol.
   B. MODIFY AMENDMENT BEFORE MEASUREMENT.
   C. REQUIRE A NEW NON-QALB DEVELOPMENT CORPUS BEFORE ANY P1+P2 FEASIBILITY MEASUREMENT.
   D. ABANDON THE CURRENT P1+P2 FEASIBILITY DESIGN.

Tie the decision to construct validity and exposure, not to implementation convenience.

## 10. Required response

Write in Arabic, RTL-friendly.

Return:
1. executive delta decision;
2. whether D_DEV_FEAS_V1 is acceptable;
3. whether 317 cases are sufficient for this limited developmental question;
4. whether >=95% remains appropriate;
5. treatment of D_TRAIN_INTERNAL_V1;
6. whether external data is required now or only later;
7. any REQUIRED BEFORE MEASUREMENT changes;
8. final next authorized step;
9. confidence and remaining uncertainty;
10. sources used.

Do not:
- run or simulate P1+P2;
- estimate unseen R_joint;
- open reserved datasets;
- alter H1-v1;
- add a proposer;
- train a selector.
