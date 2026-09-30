# MP-SEF TARGET AND MATCHING CONTRACT V1

Date: 2026-09-30
Status: FROZEN BEFORE FEASIBILITY MEASUREMENT
Parent:
phase2/redesign/MPSEF_PRE_UNION_PROTOCOL_V3.md

## 1. Population and scope

Primary feasibility population:
C_F only, as frozen by MPSEF_ROLE_SPLIT_V1.

C_F is a future-role development partition.
It is NOT historically untouched and is NOT an independent generalization set.

Cycle scope:
NoPnx linguistic correction.

No selector is trained or calibrated on C_F in this cycle.

## 2. Source of truth

Targets derive only from:
- the frozen CALIBRATION source/reference records;
- the already established official-alignment NoPnx construction rules.

No new annotation, reference repair, alternative-reference adjudication, or
gold-driven candidate decomposition is introduced.

## 3. Target unit

A target is a COMPLETE frozen NoPnx reference correction unit under the frozen
official-alignment representation.

A target is not:
- an arbitrary character difference;
- a proposer tag;
- half of a complete correction;
- a gold-guided fragment extracted from a proposer hypothesis.

Each target must have:
- target_id;
- source uid/case id;
- frozen source-span/effect identity;
- complete reference replacement/effect;
- operation family;
- punctuation scope;
- matching-version identity.

## 4. Punctuation scope

Primary denominator excludes punctuation-only reference targets.

Mandatory reporting still includes:
- punctuation-only target count;
- mixed punctuation+linguistic target count;
- representation of mixed targets.

A mixed target is not partially stripped using proposer output or gold-guided
post-hoc decomposition.

No punctuation target disappears from product-level accounting.

## 5. Frozen action spaces

### A_primary

Defined by MPSEF_BUNDLE_CONTRACT_V1:

- KEEP;
- whole P1_FINAL if executable;
- whole P2_FINAL if executable.

No edit-level fusion.

### A_diagnostic

Contains proposer diagnostic component evidence only.

It is not executable and is used only for R_raw/family diagnostics.

Gold/reference is consulted only after both action spaces are frozen.

## 6. Frozen matching principle

For each legal final output y in A_primary, score the transformation from the
ORIGINAL source x0 to y using one frozen representation-invariant official
alignment/matching implementation.

Proposer-specific internal tags are irrelevant to correctness credit.

No gold/reference may:
- alter candidate alignment;
- repair a failed proposal;
- split a bundle;
- create a candidate;
- choose a source span that was not frozen beforehand.

## 7. TP_fixed

TP_fixed(y,G_s) counts COMPLETE frozen reference targets achieved by legal
output y.

Rules:
- one target receives at most one credit;
- no duplicate credit;
- no half-credit;
- no credit for incomplete target realization;
- no gold-driven candidate split;
- no gold-driven alignment repair.

## 8. Primary endpoint: R_joint

For C_F:

R_joint(P) =
sum_s max_{y in A_primary,s(P)} TP_fixed(y,G_s)
/
sum_s |G_s|

where G_s is the frozen in-scope target set.

Interpretation:
R_joint is an oracle candidate-availability ceiling over the WHOLE-HYPOTHESIS
primary action space.

It is not:
- expected selector performance;
- edit-level fusion performance;
- precision;
- semantic safety;
- sentence-level grammaticality proof.

Because A_primary has at most KEEP/P1_FINAL/P2_FINAL, exact maximization should
be trivial once the frozen scorer is available.

If exact evaluation nevertheless cannot be established and only [L,U] is
provable:
- PASS only if L >= 0.95;
- FAIL only if U < 0.95;
- otherwise INCONCLUSIVE.

A heuristic point estimate is never called exact R_joint.

## 9. R_P1 and R_P2

Using the identical target and matching semantics:

R_P1 = R_joint({P1})
R_P2 = R_joint({P2})
R_pair = R_joint({P1,P2})

Leave-one-out gains:

Delta_P1 = R_pair - R_P2
Delta_P2 = R_pair - R_P1

## 10. Diagnostic R_raw

R_raw asks, target by target, whether the COMPLETE target effect is present
within the frozen diagnostic source-to-proposer component evidence of either
P1 or P2.

R_raw does NOT require all reachable targets to occur in one executable output.

It does not make diagnostic components executable.

Expected:

R_raw >= R_joint

Report:

R_raw - R_joint

as the decomposition/fusion opportunity gap.

A target counts in R_raw only if its complete frozen effect is represented;
partial fragments receive no credit.

## 11. R_clean

R_clean is the maximum target recall over A_primary when the selected legal
final output contains no extra reference-incompatible edit under the SAME
frozen reference comparison.

R_clean is a reference-based over-correction diagnostic.

It is not proof of semantic or scientific safety, because valid unannotated
alternatives may be penalized and reference-compatible changes may still have
domain-specific risk.

## 12. Complete-sentence repair

Among erroneous C_F sentences:

complete_sentence_repair =
sentences with one A_primary output that achieves all frozen in-scope targets
and introduces no reference-incompatible edit
/
erroneous sentences.

Reference-clean sentences are excluded from this denominator and reported
separately.

## 13. Clean-sentence proposal rate

Among reference-clean C_F sentences:

clean_proposal_rate =
clean sentences with >=1 raw non-KEEP proposer output
/
reference-clean sentences.

Also report:
- P1 clean proposal count;
- P2 clean proposal count;
- either-proposer clean proposal count.

## 14. Four-way reachability

For each COMPLETE target, using diagnostic reachability:

- BOTH;
- P1_ONLY;
- P2_ONLY;
- NEITHER.

This is not a joint-realizability classification.

## 15. Family reporting

Report for every frozen non-empty operation/error family:
- targets;
- sentences;
- document clusters;
- R_P1;
- R_P2;
- R_pair;
- R_raw.

Report:
- micro recall;
- macro average across non-empty frozen families.

Empty family:
N/A.

No family definition may change after measurement.

Frozen proposer-retention weak-family routes:
- INSERT;
- MERGE/SPLIT.

Any mapping from official target labels to these families must be frozen before
scoring.

## 16. Protected-policy accounting

Protected-span policy never improves recall by silently shrinking denominators.

Report:
- raw proposer hypotheses touching protected spans;
- executable hypotheses blocked by protection;
- in-scope reference targets affected by protection;
- resulting unreachable targets.

These targets remain visible in product accounting.

## 17. Failure accounting

Every C_F record must terminate in an accountable state.

Mandatory failure categories include:
- proposer execution failure;
- truncation;
- empty output;
- source mismatch;
- alignment failure;
- alignment ambiguity;
- nonreversible transformation;
- protected blocked;
- scoring failure.

Failed/blocked records remain in C_F denominators.

No complete-case-only analysis is permitted.

## 18. Historical H1 residual

H1-v1 historical recall 69.39% remains unchanged.

Primary V3 denominator is all frozen in-scope C_F NoPnx targets.

A secondary historical-residual target set may be reported only if a
compatibility mapping is frozen BEFORE pair metrics are inspected.

Do not infer residual recall from overall R_joint by subtraction unless:
- population matches;
- target unit matches;
- punctuation scope matches;
- alignment/matching semantics match.

Otherwise:
NOT COMPARABLE.

## 19. Alternative references

The first cycle uses the already frozen CALIBRATION reference representation.

Do not:
- select reference alternatives based on proposer output;
- synthesize hybrid gold;
- conduct rescue adjudication after weak results and then rerun the gate.

Later blinded adjudication may diagnose reference limitations but cannot
retroactively change the first-cycle decision.

## 20. Primary gate

Candidate availability PASS:

R_joint(P1,P2) >= 0.95

Diagnostic interpretation:
- >=0.95: PASS candidate availability only;
- >=0.90 and <0.95: FAIL, one diagnostic memo permitted;
- <0.90: FAIL current high-coverage P1+P2 cycle;
- interval crossing 0.95: INCONCLUSIVE.

No post-result threshold change.

## 21. Scientific claim scope

Any V3 C_F result is labeled:

DEVELOPMENT FEASIBILITY / ADAPTIVELY CONSUMED QALB-2014 ORIGIN /
NOT INDEPENDENT GENERALIZATION EVIDENCE

Passing does not authorize:
- selector training automatically;
- AUTO_SAFE;
- opening reserved/internal sets;
- a third proposer.
