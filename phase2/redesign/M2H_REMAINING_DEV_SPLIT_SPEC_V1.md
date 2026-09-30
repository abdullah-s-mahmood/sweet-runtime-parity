# M2-H Remaining DEVELOPMENT Split Specification v1

Date: 2026-09-30
Status: FROZEN BEFORE MATERIALIZATION

## Scope

Source:
- QALB14 TRAIN+DEV only.
- existing M2-R v2 DEVELOPMENT partition only.

Exclusions before any M2-H split:
- every UID consumed by M2-R v2 P0;
- every UID consumed by M2-R v2 P1;
- any UID outside DEVELOPMENT;
- any source failing the existing reconstructability contract.

Reserved/forbidden evidence remains unopened.

## Salt

`M2H-REMAINING-DEV-SPLIT-V1-20260930-A`

## Deterministic algorithm

1. Construct the eligible remaining UID set after exclusions.
2. For each UID compute:
   `SHA256("M2H-REMAINING-DEV-SPLIT-V1-20260930-A|" + UID)`
3. Sort ascending by the full hexadecimal digest; UID is the deterministic tie-breaker.
4. Let N be the total eligible count.
5. Assign exact counts:
   - CALIBRATION: first `floor(0.50 * N)`
   - INTERNAL_EVALUATION: next `floor(0.40 * N)`
   - STRESS_DIAGNOSTIC: all remaining UIDs
6. Persist only safe metadata/hash manifests before any text packet is materialized.

This creates approximately 50/40/10 while keeping membership deterministic.

## Independence requirements

- UID overlap among the three subsets must equal zero.
- overlap with M2-R P0/P1 must equal zero.
- INTERNAL_EVALUATION content must remain unseen during calibration.
- STRESS_DIAGNOSTIC cannot be used to tune thresholds for INTERNAL_EVALUATION.

## Calibration permissions

CALIBRATION may be used to freeze:
- component thresholds;
- H4 rule subset already present in v1;
- risk-fusion weights/model;
- abstention threshold.

CALIBRATION may NOT:
- add rules inspired by INTERNAL_EVALUATION;
- weaken preregistered success gates.

## INTERNAL_EVALUATION lock

Before its gold is opened:
- all components frozen;
- all artifact hashes committed;
- fusion/calibration frozen;
- prediction outputs hashed.

## STRESS_DIAGNOSTIC

Purpose:
- characterize rare/structural failures after primary internal evaluation.

It cannot rescue a failed INTERNAL_EVALUATION headline result.
