# ACAD_PASS — R44-A Final OOF Result Freeze V1

Date: 2026-10-07
Status: FINAL R44-A RESULT / R44-A COMPLETE / STOP BEFORE R44-B TRAINING UNTIL SEPARATE FREEZE

## Identity
Official run:
- run: `37581447046`
- conclusion: SUCCESS
- state: `R44A_OOF_BANK_COMPLETE`
- aggregate artifact: `11506754163`
- aggregate artifact digest: `sha256:166f9ad326efbb52a9945171e15bc7f39011fe469f50cb80e3bd0435e0e7b669`
- candidate bank SHA256: `6f20f12e8bcb814067f689f5acc27918b98de93e6e88dd1ebb53d7689bc1d946`
- design documents: 256
- manifest SHA256: `799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`

Full artifact audit:
- run: `37682327706`
- conclusion: SUCCESS
- state: `R44A_FULL_OOF_AUDIT_PASS`
- artifact: `11509711022`
- digest: `sha256:1fad91a76bd3a64cd972f535eb61625cd2b8618119396f30c010694976edbb63`
- recommendation: `B1_NESTED_OUTER_INNER_DOCUMENT_CV`

## Aggregate candidate bank
Gold inventory:
- P 271
- I 829
- C 115
- O 677
- total 1892

Candidate rows:
- total 1942
- exact-coordinate 1406
- exact-typed 1355
- NONE targets 536
- goldless-example candidates 112

Native B:
- typed precision 0.6977342945
- typed recall 0.7161733615
- typed F1 0.7068335942
- coordinate precision 0.7239958805
- coordinate recall 0.7431289641

Target population:
- NONE 536
- P 213
- I 591
- C 87
- O 515

Taxonomy:
- EXACT_TYPED 1355
- WRONG_TYPE_EXACT_COORD 51
- SAME_CLASS_WRONG_BOUNDARY 264
- DIFFERENT_CLASS_WRONG_BOUNDARY 30
- SPURIOUS_NO_OVERLAP 242

Accounting identity:
- every NONE row is one of the boundary/spurious taxonomies:
  264 + 30 + 242 = 536.
- all 51 wrong-type exact-coordinate rows remain positive P/I/C/O targets and can be corrected by a joint typed head.
- non-exact-typed total = 587.
- boundary/spurious among non-exact-typed = 536/587 = 91.31%.

## Per-class action ceiling
P:
- gold 271
- exact-coordinate available 213
- coordinate recall ceiling 0.7859778598
- native typed available 213
- native typed recall 0.7859778598

I:
- gold 829
- exact-coordinate available 591
- coordinate recall ceiling 0.7129071170
- native typed available 560
- native typed recall 0.6755126659

C:
- gold 115
- exact-coordinate available 87
- coordinate recall ceiling 0.7565217391
- native typed available 73
- native typed recall 0.6347826087

O:
- gold 677
- exact-coordinate available 515
- coordinate recall ceiling 0.7607090103
- native typed available 509
- native typed recall 0.7518463811

All coordinate ceilings are far above the frozen 0.20 recall floor.
Therefore boundary repair is NOT a prerequisite before the corrected verifier.

## Error mechanism
The complete OOF bank establishes:
1. realistic unseen-document errors are abundant;
2. the dominant negative mechanisms are wrong boundaries and spurious/no-overlap proposals;
3. simple B-confidence thresholding is inadequate because high-confidence errors repeat across all five folds;
4. type correction is directly actionable on 51 exact-coordinate wrong-type candidates;
5. a verifier can theoretically satisfy the frozen recall floor without adding new candidate coordinates.

## Fold stability
Native typed precision across folds:
- minimum 0.6756097561
- maximum 0.7228260870

Native typed recall:
- minimum 0.7002652520
- maximum 0.7347480106

Overall behavior is stable.

Class C is materially more variable:
- C coordinate ceiling range: 0.6521739130 to 0.8260869565
- C target support total: 87
- per-fold C target support is approximately 15-19.

This makes a single fixed HEAD_SELECT split less desirable than nested outer evaluation.

## BIO diagnostics
Aggregate BIO violation count: 140.
Across folds, one recorded initial-I run was a valid source continuation; unmatched/invalid events remain explicitly separated in fold evidence.
No invalid I-run manufactures a SOURCE_COMPATIBLE candidate.

## Access guards
All five folds report:
- DESIGN-only training;
- held-out fold excluded from its upstream training;
- no VERIFY_INTERNAL;
- no old R4.3 SELECT;
- no historical DEV/test;
- no other protected folds;
- no FactPICO;
- no consumed 60-RCT holdout;
- no downstream head training;
- fixed final epoch only.

## Scientific interpretation
R44-A successfully repaired the supervision-distribution diagnosis:
R4.3's in-sample-perfect upstream distribution has been replaced with a real OOF error bank.

The next experiment should NOT introduce boundary repair, stronger encoders, triaffine/global-pointer models or synthetic negatives yet.

The minimum scientifically justified next step is a leakage-safe joint verifier/type-corrector evaluated with nested upstream isolation.

## Decision
`R44A_COMPLETE_AND_AUDITED`

Recommended next:
`FREEZE_R44B_B1_NESTED_PROTOCOL -> PREFLIGHT -> AUTHORIZE_PARALLEL_PAIR_EXCLUSION_UPSTREAM_GENERATION`

Protected evaluation remains closed.
