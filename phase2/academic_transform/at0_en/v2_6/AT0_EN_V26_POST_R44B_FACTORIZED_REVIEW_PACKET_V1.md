# ACAD_PASS — Post-R44-B Factorized-Verifier Higher-Model Review Packet V1

Date: 2026-10-08

Purpose:
independent adversarial review of the **next scientific hypothesis only** after the frozen one-shot R44-B B1 failure.

No new scientific fit is authorized by this packet.

## 1. Frozen result

Official one-shot scientific run:
- `37706558889`
- attempt: `R44B_B1_DEV_J0J1_ATTEMPT_1`
- 10/10 fold/head jobs SUCCESS
- aggregate SUCCESS
- reruns: 0

Frozen result:
`AT0_EN_V26_R44B_B1_DEVELOPMENT_RESULT_FREEZE_V1.md`

Decision:
`NO_ARCHITECTURE_NOMINATED`.

Aggregate artifact:
- `11520076582`
- digest `sha256:f2375a772cc045b2aad6e207747cfec9724b6e84549b3987855ae78e3565e761`

Do not reopen or rerun this experiment.

## 2. Frozen gate outcome

Best J0:
- t=.95
- macro precision = 0.845308610324185
- P precision = 0.8729281767955801
- I precision = 0.8
- C precision = 0.88
- O precision = 0.8283062645011601
- all recalls remain > .38.

Best J1:
- t=.95
- macro precision = 0.8258277690482774.

J1 has worse macro precision than J0 at every frozen threshold.

## 3. Frozen read-only causal diagnosis

Read first:
`AT0_EN_V26_R44B_B1_FAILURE_CAUSAL_DIAGNOSIS_V1.md`.

Key project-specific evidence:

### High-confidence FP composition
J0 t=.95 FP = 189:
- 93 SAME_CLASS_WRONG_BOUNDARY
- 78 SPURIOUS_NO_OVERLAP
- 14 WRONG_TYPE_EXACT_COORD
- 2 exact-typed candidates changed to wrong type
- 2 DIFFERENT_CLASS_WRONG_BOUNDARY

90.48% of J0 accepted FPs are SAME_CLASS_WRONG_BOUNDARY or SPURIOUS_NO_OVERLAP.

### Validity ranking
J0:
- `1-p_NONE` validity AUROC = 0.7328427209613384
- validity AP = 0.8595765835906929

J1:
- AUROC = 0.7263745727266937
- AP = 0.8586457116780261

### Type discrimination conditional on valid coordinates
On 1,406 target P/I/C/O candidates:

J0:
- 5-way accuracy = 0.813655761024182
- P/I/C/O-only accuracy = 0.9509246088193457

J1:
- 5-way accuracy = 0.8172119487908962
- P/I/C/O-only accuracy = 0.9516358463726885

### Oracle diagnostic — not an achieved model result
If target-NONE were perfectly rejected:

Existing J1 type-only argmax:
- P precision = 0.9859154929577465
- I precision = 0.9444444444444444
- C precision = 0.9230769230769231
- O precision = 0.949438202247191
- macro precision = 0.9507187656815763
- all frozen precision/recall/count gates would pass.

Existing B type with oracle validity still fails C:
- C precision = 0.8795180722891566.

Thus type correction remains necessary.

### Capacity/overfit signal
Final meta-training CE:

J0 folds:
- .00852549
- .00802947
- .01209585
- .01571586
- .00604789

J1 folds:
- .00086176
- .00102000
- .00098452
- .00080885
- .00067227

J1 nearly memorizes meta training but generalizes worse than J0.

## 4. Literature already reviewed

### PICOX, JAMIA 2024
DOI 10.1093/jamia/ocae065
- direct PICO span model;
- treats invalid candidate spans as a first-class classification problem;
- augments span-classifier data with invalid/composite spans;
- reports false-positive/precision benefit.

### Liu et al., Neurocomputing 2022
DOI 10.1016/j.neucom.2022.07.012
- mechanistic precedent for separating entity identification from entity classification;
- hard-negative problem in span NER;
- entity-identification errors dominated their baseline.
Older than preferred window, so use only as mechanistic support.

### TSBECL, Expert Systems with Applications 2025
DOI 10.1016/j.eswa.2025.126707
- two-stage/boundary-enhanced span classification;
- candidate imbalance/hard discrimination;
- multi-task and contrastive mechanisms.

### BGNER 2025
DOI 10.1007/s44443-025-00059-6
- explicit boundary-aware span validation.

### OpenBioNER-v2 2026
DOI 10.1016/j.eswa.2026.131725
- exact boundaries remain difficult;
- rare-entity calibration is weaker.

## 5. Current internal recommendation — challenge it

Current recommendation is:

`FACTORIZE_CANDIDATE_VALIDITY_FROM_PICO_TYPE_BEFORE_BOUNDARY_REPAIR_OR_CALIBRATION`.

Candidate minimal design family:

### Factorized verifier concept
- binary VALID/INVALID task on every candidate;
- 4-way P/I/C/O type task only for valid exact-coordinate candidates;
- same immutable upstream candidate banks;
- same immutable context cache/features initially;
- no new upstream candidate generation;
- no boundary repair in the same experiment;
- no fitted calibration;
- no external data/pseudo-labels;
- no VERIFY_INTERNAL.

Potential acceptance concept:
- validity score controls candidate acceptance;
- type comes from 4-way head;
- exact acceptance/threshold rule must be prospectively frozen before fitting.

### Capacity concern
Do NOT assume the old 584k/668k head trunk should be reused.
Current near-zero training loss + worse J1 generalization makes a low-capacity/regularized factorized head a serious option.

## 6. Alternatives that must be compared adversarially

A. **Low-capacity factorized validity + type**
- e.g. regularized linear/small MLP binary validity head and separate 4-way type head.

B. **Factorized old J0/J1-style representation**
- same contextual projection machinery, separate losses/outputs.

C. **Boundary repair first**
- could convert wrong-boundary NONE candidates into exact coordinates;
- but same-boundary-only oracle rejection did NOT pass all class gates.

D. **Explicit hard-negative / IoU-aware loss**
- may target same-boundary negatives;
- but spurious negatives are also a major FP source.

E. **Calibration first**
- current ECE is high;
- but validity AUROC is only ~.73, so calibration cannot by itself create missing rank separation.

F. **Simpler non-factorized linear five-way head**
- tests overcapacity;
- but does not directly address the observed entity-validity/type asymmetry.

## 7. Critical adaptive-development issue

All 256 DESIGN documents have now contributed to observed nested outer DEVELOPMENT results.

Therefore:
- no new partition of DESIGN becomes statistically fresh merely by rearrangement;
- any next DESIGN experiment is adaptive development;
- its result must not be called unbiased validation.

VERIFY_INTERNAL:
- remains closed for R44-specific candidate verification;
- is historically exposed through parent R4.3 FIT/audits and split aggregate counts;
- can only be a later one-time prospective phase-internal checkpoint after a full procedure is frozen.

Review whether continuing hypothesis-driven DEVELOPMENT on DESIGN is defensible under this explicit interpretation, or whether another data source is required before any further fitting.

## 8. Questions for the higher model

Perform Deep Research + adversarial review + genuine brainstorming.

Return a decisive answer:

1. Does the frozen evidence genuinely justify factorizing VALID/INVALID from P/I/C/O type?
2. Is the current evidence strong enough that factorization should precede boundary repair?
3. Does J1's near-zero train loss + worse DEVELOPMENT precision justify reducing capacity?
4. What is the **single narrowest next architecture/objective** that best tests the diagnosed mechanism?
5. Should the next experiment use:
   - a binary validity head + valid-only 4-way type head,
   - a shared or separate trunk,
   - linear/logistic heads or a small MLP?
6. How should the two losses be defined/weighted without tuning after observing scores?
7. What acceptance rule should be prospectively frozen?
   - validity threshold only + type argmax?
   - product/joint confidence?
   - another mathematically defensible rule?
8. Should the old threshold grid `{.80,.85,.90,.95}` be reused for validity probability, or is that unjustified because its semantic scale changed?
9. Is temperature/isotonic calibration still properly deferred?
10. Should any hard-negative weighting be included now, or would that confound the factorization test?
11. Is boundary repair still properly deferred after seeing that 90.48% of J0 t=.95 FPs are same-boundary/spurious?
12. How should model capacity/regularization be frozen to reduce the demonstrated memorization risk?
13. Is another nested DESIGN run scientifically useful despite adaptive exposure? If yes, how must it be interpreted?
14. Should we preserve VERIFY_INTERNAL for later, or is a new external/fresh source required before investing further?
15. Identify any overlooked explanation that could make the factorized hypothesis wrong.
16. Search 2024-2026 literature/systems for a stronger minimal alternative.
17. Recommend exactly **one primary next experiment**, plus at most one predeclared fallback.
18. State what evidence would falsify the hypothesis.

Return one verdict:
- `PROCEED_FACTORIZED_LOW_CAPACITY`
- `PROCEED_FACTORIZED_EXISTING_REPRESENTATION`
- `PROCEED_BOUNDARY_FIRST`
- `PROCEED_OTHER_SINGLE_INTERVENTION`
- `STOP_AND_ACQUIRE_FRESH_DATA`
- `BLOCK_FOR_OTHER_REASON`

Do not recommend a broad architecture sweep.
Do not open VERIFY_INTERNAL.
Do not propose post-hoc threshold shopping on R44-B outputs.
