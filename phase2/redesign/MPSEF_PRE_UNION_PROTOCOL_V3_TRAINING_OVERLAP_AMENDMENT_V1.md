# MP-SEF PRE-UNION PROTOCOL V3 — TRAINING-OVERLAP AMENDMENT V1

Date: 2026-09-30
Status: FROZEN BEFORE ANY CANDIDATE METRIC

Applies to:
phase2/redesign/MPSEF_PRE_UNION_PROTOCOL_V3.md

Evidence:
phase2/redesign/MPSEF_TRAINING_OVERLAP_AUDIT_V1.md

## 1. Reason for amendment

After V3 was frozen but before any candidate-union / R_joint metric was computed, a required training-overlap audit established:

CALIBRATION:
- total: 6,888
- original QALB-2014 train: 6,571
- original QALB-2014 dev: 317

Both P1 and P2 are public QALB-2014 fine-tuned systems.

Therefore a generic random 30/40/30 role split across all CALIBRATION records would contaminate the primary feasibility population with direct proposer-training records.

This amendment is prospective.
No P1+P2 feasibility metric was observed before the change.

## 2. Sections superseded

This amendment supersedes V3 Section 12 for the first proposer-feasibility measurement and modifies the required artifacts in V3 Sections 24, 25, and 27.

All other V3 sections remain unchanged unless explicitly stated here.

## 3. Primary feasibility population

Primary population identifier:
D_DEV_FEAS_V1

Membership:
all frozen CALIBRATION records with original split == "dev".

Expected record count:
317.

These records:
- are excluded from the QALB-2014 train-origin records;
- remain historically development-exposed;
- remain ACAD_PASS-CALIBRATION-exposed;
- are NOT an independent test set;
- are NOT valid for AUTO_SAFE certification.

The future feasibility result must be labeled:

**DEVELOPMENTAL / DEV-ORIGIN / NOT INDEPENDENT**

## 4. Duplicate/near-duplicate cluster rule

Clustering is computed across all 6,888 CALIBRATION records before selecting D_DEV_FEAS_V1.

Source-only key:
- Unicode NFC;
- whitespace normalization for duplicate detection only;
- whitespace tokenization.

Near duplicate:
- token-set Jaccard >=0.90;
- shorter/longer token-count ratio >=0.90.

Connected components define clusters.

Pre-freeze audit result:
- total connected clusters: 6,871;
- non-singleton clusters: 15;
- maximum cluster size: 4;
- clusters containing dev records: 317;
- clusters crossing original train/dev split: 0.

Therefore no dev-origin record is linked by this frozen duplicate rule to a train-origin record.

This result must be reproduced by the manifest-generation preflight before measurement.

## 5. Train-origin population

Identifier:
D_TRAIN_INTERNAL_V1

Membership:
all frozen CALIBRATION records with original split == "train".

Expected count:
6,571.

Use:
- development engineering;
- future selector fitting/development if separately authorized;
- debugging;
- internal in-sample diagnostics.

Do not use D_TRAIN_INTERNAL_V1 as the primary proposer-feasibility denominator.

## 6. Future selector role separation

The higher-model recommendation to separate selector-development and risk-calibration roles remains valid, but it is deferred.

No 40/30 split of D_TRAIN_INTERNAL_V1 is materialized before candidate feasibility because selector training is not yet authorized.

If later authorized, a new frozen protocol must define:
- selector-training role;
- internal risk-calibration role;
- cluster-level separation;
- exact proportions;
- whether sufficient data independent of proposer training exist.

No future split of QALB-2014 train-origin records may be described as independent proposer validation.

## 7. Primary endpoint

V3 R_joint remains the primary endpoint.

For the first feasibility cycle:

R_joint is computed only on D_DEV_FEAS_V1.

The >=95% candidate-availability gate remains unchanged.

Passing means:
candidate availability is sufficient on this consumed development/dev-origin population to justify considering a later selector research protocol.

Passing does NOT establish:
- independent generalization;
- performance on unseen academic documents;
- AUTO_SAFE safety;
- 98% precision.

## 8. Training-origin diagnostic metrics

Primary decision rules must not use D_TRAIN_INTERNAL_V1.

No train-origin R_joint is required for the first decision.

If a train-origin diagnostic is ever computed later, it must be:
- separately authorized;
- clearly labeled in-sample;
- excluded from the >=95% primary gate decision.

## 9. Exposure ledger requirement

The full 6,888-record exposure ledger remains required.

Minimum per-record fields:
- case_id;
- uid;
- original_split;
- cluster_id;
- feasibility_population;
- source_only_exposed;
- gold_exposed;
- aggregate_result_exposed;
- error_analysis_exposed;
- fit_exposed;
- threshold_selection_exposed;
- unknown_exposure;
- proposer_training_overlap_status;
- independence_claim_allowed.

Conservative current status:
- all CALIBRATION records: gold_exposed=true;
- all CALIBRATION records: aggregate_result_exposed=true;
- all CALIBRATION records: source-level development exposure=true;
- detailed historical per-record error-analysis exposure: unknown unless reconstructible;
- original train records: proposer_training_overlap_status=KNOWN_OR_HIGHLY_EXPECTED_DIRECT_TRAIN_OVERLAP;
- original dev records: proposer_training_overlap_status=MODEL_DEVELOPMENT_EVALUATION_EXPOSURE;
- independence_claim_allowed=false for all 6,888.

## 10. Revised required artifacts before feasibility

The following must exist and be frozen:

1. MPSEF_PRE_UNION_PROTOCOL_V3.md
2. MPSEF_PRE_UNION_PROTOCOL_V3_TRAINING_OVERLAP_AMENDMENT_V1.md
3. MPSEF_TRAINING_OVERLAP_AUDIT_V1.md
4. MPSEF_EXPOSURE_LEDGER_V1.jsonl
5. MPSEF_EXPOSURE_LEDGER_SUMMARY_V1.json
6. MPSEF_FEASIBILITY_POPULATION_V1.jsonl
7. MPSEF_FEASIBILITY_POPULATION_SUMMARY_V1.json
8. MPSEF_CLUSTER_MAP_V1.jsonl
9. MPSEF_CLUSTER_MAP_SUMMARY_V1.json
10. MPSEF_BUNDLE_CONTRACT_V1.md
11. MPSEF_TARGET_AND_MATCHING_CONTRACT_V1.md
12. MPSEF_PROTECTED_INVARIANTS_CONTRACT_V1.md
13. P1 runtime lock
14. P2 runtime lock
15. exact generator/preflight source hashes
16. preflight proof that:
    - CALIBRATION count=6,888;
    - train count=6,571;
    - dev count=317;
    - total clusters=6,871;
    - dev clusters=317;
    - train/dev crossing clusters=0;
    - D_DEV_FEAS_V1 contains exactly the 317 dev-origin records;
    - D_DEV_FEAS_V1 has no record from train;
    - every CALIBRATION record appears exactly once in exposure ledger and cluster map;
    - no hidden/reserved data was opened;
    - no candidate feasibility metric was computed.

## 11. Stop rule addition

If preflight reproduces any different:
- original split counts;
- cross-split cluster count;
- D_DEV_FEAS_V1 membership count;

stop before proposer execution and investigate provenance.

Do not change duplicate thresholds after inspecting candidate metrics.

## 12. Current scientific classification

Relative to generic V3 split design:

**IMPROVED / TRAINING-OVERLAP CONFOUND REMOVED FROM PRIMARY FEASIBILITY POPULATION**

Remaining limitation:
D_DEV_FEAS_V1 is development-exposed and not independent.

## 13. Exact next authorized step

Generate only the revised manifests and contracts.

Do not run P1/P2 candidate feasibility until:
- manifests;
- contracts;
- preflight;
are frozen and verified.

Reserved/internal datasets remain closed.
