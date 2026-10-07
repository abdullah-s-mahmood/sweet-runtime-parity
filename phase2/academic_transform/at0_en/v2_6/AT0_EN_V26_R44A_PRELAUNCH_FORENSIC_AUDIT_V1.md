# ACAD_PASS — R4.4-A Pre-Launch Forensic Audit V1

Date: 2026-10-07
Status: READY_TO_LAUNCH_R44A_ONLY

## Evidence reviewed

1. R4.3 Stage-B scientific failure and causal forensic report.
2. FIT-only B replay: run 37568769890; B is perfect in-sample (2371/2371 exact, 0 FP), while exposed SELECT had 250 false proposals.
3. Gold/source semantic contract.
4. Corrected official source protocol parity V2: run 37580279584; official B-start inventory P426/I1326/C181/O1067, exact match to independent strict-B count; 11 legacy local-continuation entities retired prospectively.
5. R4.4 read-only preflight: run 37572165532 PASS; manifest SHA256 799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720.
6. DESIGN-only materialization: run 37572893091 PASS; source SHA256 f8b49420cb17a5cb3f67f3120f9362b5e6b15fbb148176eab20105790bab1e18; no VERIFY_INTERNAL or old SELECT documents.
7. R4.4 adversarial protocol review.
8. R44-A mechanics run 37580770372 PASS after diagnostic repair.

## Frozen R44-A scope

Data:
- DESIGN only = 256 docs.
- Five held-out OOF folds: 52/51/51/51/51 docs.
- VERIFY_INTERNAL 64 docs remains absent from training source.
- old R4.3 SELECT remains absent.
- historical DEV, tests, other folds, external tests, FactPICO, consumed 60-RCT remain closed.

Each fold:
1. B_CANDIDATE trained on DESIGN minus held-out fold.
2. C_BOUNDARY trained on same training docs.
3. Both use fixed final epochs only (B=10, Boundary=3).
4. Inference only on held-out fold.
5. Held-out gold consulted only after inference to label candidate targets/taxonomy.
6. No C_TYPE and no downstream head training.
7. Candidate target = exact-coordinate gold P/I/C/O, otherwise NONE; proposed B type retained separately, so future joint head may learn type correction.

Stable context:
- R44-B must use immutable base context rather than label-fitted Boundary hidden vectors.
- R44-A freezes native candidate/evidence bank and scalar OOF boundary support; base contextual vectors can be deterministically rematerialized later from DESIGN source/candidate coordinates.

## Neutral code repairs before launch

### BIO violation diagnostic
Old R44-A code would record every orphan I-token in a run as a separate violation.
Prospectively fixed at commit 868a6bf300bded961f07076fb0e7fd4c0ba1f751:
- violation counted once per contiguous I-X run;
- taxonomy INITIAL_I_RUN / O_TO_I_RUN / CROSS_TYPE_I_RUN;
- initial-I run records whether it matches a valid source-gold document continuation.
Candidate generation behavior is unchanged: orphan I never manufactures a candidate.

Mechanics re-test:
- run 37580770372 SUCCESS.

### Aggregate identity guard
Aggregate bank now must equal exact frozen DESIGN inventory:
- documents = 256;
- P/I/C/O = 271/829/115/677.
Any drift blocks aggregate completion.

## Risks explicitly retained

1. VERIFY_INTERNAL is an internal holdout, not a pristine external benchmark: its parent documents were previously in R4.3 FIT, and class counts were used for deterministic balancing. Do not market it as independent external validation.
2. R44-A OOF bank is suitable for constructing realistic meta-training data, but ordinary CV over the same OOF bank is not a clean head-selection estimate because of second-order stacking dependency. R44-B remains blocked until a leakage-safe nested or disjoint protocol is frozen.
3. Candidate verifier cannot recover spans not proposed by B or repair boundaries. Candidate ceiling is measured before any repair branch.
4. Section metadata TITLE/METHODS is source-derived and preflight UNKNOWN rate is zero; it is metadata only in R44-A.
5. Class imbalance and native error composition are unknown before R44-A; do not freeze downstream loss/sampling based on R4.3 SELECT.
6. No threshold/model selection from old SELECT is permitted.

## Statistical basis

Nested/isolation logic is consistent with the literature on model-selection optimism and cross-validation:
- Varma & Simon-style nested CV principle;
- Bates, Hastie & Tibshirani on what CV estimates and uncertainty;
- out-of-sample prediction based stacking/model-selection literature.
This supports isolation; it does not predict R44-A performance.

## Launch decision

`AUTHORIZE_ONE_SEQUENTIAL_R44A_OOF_UPSTREAM_BANK_WORKFLOW`

The workflow must:
- set matrix max-parallel=1;
- fail-fast=true;
- upload no temporary model weights;
- aggregate only after all five folds pass;
- stop before J0/J1 or VERIFY_INTERNAL;
- preserve model hashes, candidate bank hashes, fold identities, guards and PROCESS_STATUS.

After aggregate:
`STOP -> AUDIT_REAL_OOF_ERROR_DISTRIBUTION -> FREEZE_R44B_PROTOCOL`.
