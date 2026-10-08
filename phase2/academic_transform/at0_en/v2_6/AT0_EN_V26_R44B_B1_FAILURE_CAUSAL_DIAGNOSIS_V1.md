# ACAD_PASS — R44-B B1 Frozen Failure Causal Diagnosis V1

Date: 2026-10-08

**State:** `R44B_B1_READ_ONLY_CAUSAL_DIAGNOSIS_COMPLETE`

Input evidence is exclusively the frozen one-shot DEVELOPMENT artifact from run `37706558889`.

No new fit, threshold, seed, calibration, boundary repair, protected access or scientific retry was performed.

## 1. Frozen result being diagnosed

Result freeze:
`AT0_EN_V26_R44B_B1_DEVELOPMENT_RESULT_FREEZE_V1.md`

Decision:
`NO_ARCHITECTURE_NOMINATED`.

J0 best frozen macro precision:
- t=.95: 0.845308610324185

J1 best frozen macro precision:
- t=.95: 0.8258277690482774

All frozen recalls exceed the .20 floor. Precision is the blocking metric.

## 2. High-confidence accepted-error composition

At t=.95, J0:
- TP = 903
- FP = 189

FP taxonomy:
- SAME_CLASS_WRONG_BOUNDARY = 93
- SPURIOUS_NO_OVERLAP = 78
- WRONG_TYPE_EXACT_COORD = 14
- EXACT_TYPED changed to wrong type = 2
- DIFFERENT_CLASS_WRONG_BOUNDARY = 2

Thus:
- SAME_CLASS_WRONG_BOUNDARY + SPURIOUS_NO_OVERLAP = 171 / 189 = 90.47619047619048% of accepted J0 false positives.
- all target-NONE boundary/spurious groups including DIFFERENT_CLASS_WRONG_BOUNDARY = 173 / 189 = 91.53439153439153%.

At t=.95, J1:
- FP = 207
- SAME_CLASS_WRONG_BOUNDARY = 106
- SPURIOUS_NO_OVERLAP = 81
- WRONG_TYPE_EXACT_COORD = 16
- EXACT_TYPED changed wrong = 2
- DIFFERENT_CLASS_WRONG_BOUNDARY = 2.

The dominant failure is therefore candidate validity/rejection, not insufficient recall.

## 3. Direct validity-separation diagnostic

Binary target:
- valid candidate = target in P/I/C/O;
- invalid candidate = target NONE.

Using the already-frozen softmax only as a read-only diagnostic:

### J0
- validity score `1-p_NONE` AUROC = 0.7328427209613384
- validity AP = 0.8595765835906929
- max-nonNONE AUROC = 0.7333575720260717
- max-nonNONE AP = 0.8605264730159162

### J1
- validity score `1-p_NONE` AUROC = 0.7263745727266937
- validity AP = 0.8586457116780261
- max-nonNONE AUROC = 0.7265908632513111
- max-nonNONE AP = 0.8598347880064632

Interpretation:
- validity ranking itself is only moderate;
- this is not merely a threshold-grid problem;
- monotone probability calibration cannot repair poor rank overlap, so calibration is not the first causal intervention.

## 4. Valid-span type discrimination is much stronger

There are 1,406 exact-coordinate valid candidates.

If NONE is ignored only for diagnosis and the type is chosen among P/I/C/O:

### J0
- type-only accuracy on valid candidates = 0.9509246088193457
- five-way accuracy on valid candidates = 0.813655761024182
- valid candidates whose five-way argmax is NONE = 0.1600284495021337

### J1
- type-only accuracy = 0.9516358463726885
- five-way accuracy = 0.8172119487908962
- valid candidates whose five-way argmax is NONE = 0.15860597439544807

This provides direct project-specific evidence that:
- P/I/C/O discrimination is substantially stronger than entity-validity discrimination;
- folding `NONE` and type into one five-way objective is a plausible structural bottleneck.

## 5. Oracle-validity diagnostic — NOT an achieved result

This is a read-only counterfactual diagnostic, not a model result and not authorization to use an oracle.

At t=.95, if every target-NONE candidate were perfectly rejected while preserving the existing accepted non-NONE predictions:

### J0
- macro precision = 0.9748970729655007
- P precision = 1.0
- I precision = 0.9717514124293786
- C precision = 0.9361702127659575
- O precision = 0.9916666666666667
- frozen gate would pass.

### J1
- macro precision = 0.9760094405163829
- P precision = 0.9875776397515528
- I precision = 0.9721448467966574
- C precision = 0.9545454545454546
- O precision = 0.989769820971867
- frozen gate would pass.

This establishes that the dominant precision deficit is in invalid-candidate rejection.

It does NOT establish that a practical validity model can achieve oracle behavior.

## 6. Type-only oracle-validity diagnostic

If invalid candidates are perfectly rejected and the existing type logits are used only among P/I/C/O:

### J0
- P precision = 0.9768518518518519
- I precision = 0.9441624365482234
- C precision = 0.8493150684931506
- O precision = 0.9619771863117871
- macro precision = 0.9330766358012532
- C still fails.

### J1
- P precision = 0.9859154929577465
- I precision = 0.9444444444444444
- C precision = 0.9230769230769231
- O precision = 0.949438202247191
- macro precision = 0.9507187656815763
- all four precision gates would pass, and recalls remain above .20.

This makes a factorized validity + type hypothesis materially stronger, while also explaining why J1's extra interaction is not useful when validity and type are forced into one five-way decision.

Again, this is diagnostic only and not a selectable result.

## 7. Existing B type is insufficient for C even with oracle validity

If target-NONE candidates are perfectly rejected but the original upstream B type is retained:
- P precision = 0.9906976744186047
- I precision = 0.9671848013816926
- C precision = 0.8795180722891566
- O precision = 0.9621928166351607
- macro precision = 0.9498983411811537.

Therefore a pure validity veto that always keeps B type is insufficient under the frozen C>=.90 precision gate.

Some type correction remains necessary.

## 8. Wrong-type exact-coordinate correction remains difficult

There are 51 `WRONG_TYPE_EXACT_COORD` candidates.

At t=.95:

J0:
- correctly corrected + accepted = 2
- rejected = 35
- accepted with wrong type = 14

J1:
- correctly corrected + accepted = 4
- rejected = 31
- accepted with wrong type = 16

These are a minority of the current FP burden, but a future verifier cannot simply ignore type correction.

## 9. Invalid-candidate rejection rates at t=.95

J0 false-accept rate:
- SAME_CLASS_WRONG_BOUNDARY: 93 / 264 = 35.22727272727273%
- DIFFERENT_CLASS_WRONG_BOUNDARY: 2 / 30 = 6.666666666666667%
- SPURIOUS_NO_OVERLAP: 78 / 242 = 32.231404958677686%
- all target-NONE: 173 / 536 = 32.276119402985074%

J1:
- SAME_CLASS_WRONG_BOUNDARY: 106 / 264 = 40.15151515151515%
- DIFFERENT_CLASS_WRONG_BOUNDARY: 2 / 30 = 6.666666666666667%
- SPURIOUS_NO_OVERLAP: 81 / 242 = 33.47107438016529%
- all target-NONE: 189 / 536 = 35.26119402985075%.

J1 makes candidate-validity rejection worse despite extra capacity.

## 10. Training-fit versus DEVELOPMENT generalization

All 10 jobs trained exactly 10 epochs.

Final mean training CE:

J0:
- outer 0 = 0.008525488572462624
- outer 1 = 0.008029467133171195
- outer 2 = 0.012095851216992094
- outer 3 = 0.01571586098801041
- outer 4 = 0.006047885027022937

J1:
- outer 0 = 0.0008617554563270013
- outer 1 = 0.0010200008496515198
- outer 2 = 0.0009845193976831818
- outer 3 = 0.0008088513872819779
- outer 4 = 0.0006722713235219572

J1 fits the meta-training banks almost perfectly yet has worse frozen DEVELOPMENT macro precision than J0 at every threshold.

This is strong direct evidence against responding to R44-B failure by adding more unfocused head capacity.

It is consistent with overfitting / representation-objective mismatch.

## 11. Boundary-only versus validity-wide diagnostic

At J0 t=.95:

If only SAME_CLASS_WRONG_BOUNDARY accepted FPs were oracle-rejected:
- macro precision rises to 0.9053834139813682
- but I precision remains 0.8935064935064935
- C precision remains 0.8979591836734694
- frozen gate still fails.

If only SPURIOUS_NO_OVERLAP accepted FPs were oracle-rejected:
- macro precision = 0.9035319454414932
- but I precision = 0.86
- O precision = 0.8969849246231156
- gate still fails.

If all target-NONE candidates were oracle-rejected:
- all frozen precision gates pass.

Therefore:
- boundary repair alone is not currently the narrowest sufficient causal hypothesis;
- spurious-only rejection is also insufficient;
- the evidence favors a general candidate-validity mechanism capable of learning both hard boundary negatives and spurious negatives.

## 12. Literature triangulation

### PICOX — JAMIA 2024
Zhang et al., "A span-based model for extracting overlapping PICO entities from randomized controlled trial publications", DOI 10.1093/jamia/ocae065.

Relevant mechanism:
- separates span localization from span classification;
- explicitly notes that not all candidate spans are valid entities;
- augments span-classifier training with invalid/composite spans;
- reports reduced false positives / improved precision from this negative-span strategy.

Project relevance:
- direct PICO extraction evidence;
- supports treating invalid-span discrimination as a first-class problem.

Source:
https://pmc.ncbi.nlm.nih.gov/articles/PMC11031223/

### Handling negative samples in span-based nested NER — Neurocomputing 2022
DOI 10.1016/j.neucom.2022.07.012.

Relevant mechanistic evidence:
- separates entity identification from entity classification;
- reports entity-identification error dominating type-classification error in its baseline;
- uses multi-task factorization and hard-negative emphasis.

Although older than the preferred 2024-2026 window, its mechanism directly matches the newly observed ACAD_PASS failure mode and is retained as mechanistic precedent, not as current SOTA proof.

### TSBECL — Expert Systems with Applications 2025
Liu et al., DOI 10.1016/j.eswa.2025.126707.

Relevant mechanism:
- two-stage boundary-enhanced candidate span classification;
- explicitly addresses candidate-span imbalance;
- uses boundary information, contrastive discrimination and multi-task learning.

Source:
https://www.sciencedirect.com/science/article/pii/S095741742500329X

### BGNER — 2025
He et al., "BGNER: A boundary guidance framework for enhanced named entity recognition", DOI 10.1007/s44443-025-00059-6.

Relevant mechanism:
- span-based systems can fail when boundary context is not used strongly enough;
- boundary-aware representations validate candidate predictions.

Source:
https://doi.org/10.1007/s44443-025-00059-6

### OpenBioNER-v2 — 2026
Relevant disconfirming evidence:
- exact boundary detection remains materially harder than type recognition;
- confidence calibration is poorer for rare entity types.

This supports retaining calibration as a diagnostic concern, but it does not show calibration alone can fix the observed ACAD_PASS validity-ranking overlap.

Source:
https://huggingface.co/blog/alecocc/openbioner-v2

## 13. Independent causal verdict

`VALIDITY_IDENTIFICATION_IS_THE_PRIMARY_NEXT HYPOTHESIS`

More precisely:

`FACTORIZE_CANDIDATE_VALIDITY_FROM_PICO_TYPE_BEFORE_BOUNDARY_REPAIR_OR_CALIBRATION`

Evidence hierarchy:
1. 90.48% of high-confidence J0 accepted FPs are same-boundary or spurious invalid spans.
2. binary validity AUROC is only ~0.733.
3. valid-span P/I/C/O type-only accuracy is ~95%.
4. J1 type-only + oracle validity would pass all frozen class precision gates.
5. J1's additional capacity nearly annihilates training loss but worsens DEVELOPMENT precision.
6. boundary-only oracle removal does not satisfy every class gate.
7. PICOX and broader span-NER literature explicitly treat candidate validity / hard negatives as a distinct problem.

## 14. Narrowest recommended next scientific design direction

Do NOT launch it yet.

Recommended next design for independent review:

A prospectively frozen **factorized verifier**:
- binary `VALID / INVALID` head trained on all nested meta candidates;
- separate 4-way P/I/C/O type head trained only on valid exact-coordinate candidates;
- retain the same immutable upstream candidate banks and context inputs initially;
- do not add calibration, boundary repair, external data, pseudo-labels, new encoder fine-tuning or extra candidate generation in the same experiment;
- explicitly control model capacity/regularization because current J0/J1 training losses show severe memorization;
- predefine how validity probability and type prediction form the acceptance rule;
- predefine thresholds before fitting;
- continue to treat DESIGN as adaptive development evidence;
- preserve VERIFY_INTERNAL unopened for R44-specific verification until a full procedure is frozen.

A regularized low-capacity factorized head should be considered alongside, or preferably before, reusing the large J0/J1 trunk because the present parameter-to-meta-sample ratio and training losses demonstrate overfit risk.

The exact architecture and threshold contract are NOT authorized by this diagnosis and require separate adversarial review before implementation/training.

## 15. Current stop boundary

Allowed:
- read-only analysis;
- literature review;
- protocol design;
- synthetic mechanics;
- higher-model/adversarial consultation.

Not authorized:
- any new scientific fit;
- any J0/J1 retry;
- VERIFY_INTERNAL;
- fitted calibration;
- boundary repair training;
- factorized-head training;
- alternate-model training;
- final refit.

Exact checkpoint:

`R44B_B1_FROZEN_FAILURE_DIAGNOSED -> PREPARE_PROSPECTIVE_FACTORIZED_VALIDITY_TYPE_PROTOCOL_FOR_INDEPENDENT_REVIEW`
