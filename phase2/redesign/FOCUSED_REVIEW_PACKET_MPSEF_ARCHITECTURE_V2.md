# FOCUSED REVIEW PACKET — ACAD_PASS Arabic Correction v2 / MP-SEF

Date: 2026-09-30
Purpose: independent high-level methodological review before candidate-union evaluation
Status: REVIEW REQUEST — NO SELECTOR AUTHORIZED

## 1. What has already been established

The previous Arabic correction path M2-H is formally closed.

Frozen H1-v1 result:
- role: one-pass SWEET NoPnx candidate generator
- official-alignment representation-invariant recall: 69.39%
- frozen feasibility gate: >=80%
- deficit: -10.61 percentage points
- inference parity: 256/256
- CALIBRATION gold construction: 6888/6888
- construction failures: 0
- char-alignment cross mismatches: 0
- word/subword cross mismatches: 0

Therefore the failure was not attributed to runner mismatch or a known evaluation-construction bug.

H2:
- no deterministic orthographic family activated.

H3:
- morphology validator failed as a standalone safety validator.

H4:
- structural MERGE validator achieved high precision but insufficient recall; not activated.

M2-R:
- useful residual-risk signal but failed as a standalone verifier.

Current Arabic product policy:
REVIEW-first. Automatic correction is not the default.

## 2. New architecture under review

Architecture:
**MP-SEF — Multi-Proposer Selective Edit Fusion**

Core idea:
separate proposal generation from edit authorization.

No neural proposer is permitted to rewrite the document directly.

Pipeline concept:

source/invariant lock
→ heterogeneous proposers
→ canonical reversible source-anchored edit transactions
→ candidate union + conflict graph
→ independent evidence features
→ selective authorization / REVIEW / rejection
→ residual completeness check

## 3. Initial proposer pool

### P1 — SWEET iterative NoPnx proposer

Same public model weights as H1-v1, but separately versioned.

Difference:
- decode_iter=2
- top-1
- NoPnx
- no confidence threshold
- no top-k
- punctuation excluded from initial proposal experiment

Rationale:
the public SWEET usage pattern uses iterative NoPnx decoding.

P1 runtime parity:
- deterministic source-only CALIBRATION sample n=64
- pass 1 exact trace match: 64/64
- pass 2 exact trace match: 64/64
- all-field match: 64/64
- mismatches: 0

P1 is activated only as a proposer, not as an automatic corrector.

### P2 — AraBART + Morph + GED proposer

Public CAMeL-Lab Arabic GEC path:
- contextual morphological preprocessing
- CAMeLBERT multi-class GED
- GED-conditioned AraBART generation

Frozen identities:
- GEC model: CAMeL-Lab/arabart-qalb14-gec-ged-13
- GEC revision: 410588a318d988cdcfdbf64cf5745ed4adea0f6a
- GED model: CAMeL-Lab/camelbert-msa-qalb14-ged-13
- GED revision: 447179dc63d186e4bff09a993e90e73ad622d571
- arabic-gec repo revision: 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf
- CAMeL morphology DB SHA256:
  195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70
- CAMeL MSA BERT disambiguator weight SHA256:
  a1a22431cdc0934151e4039abbd7890f06ba7c1f914ca71a90eba218401ae539

P2 parity is currently being established and is not yet considered valid.

## 4. Candidate representation

Every proposer output must be converted to a common reversible edit transaction containing at least:
- source span
- source text
- replacement text
- operation family
- proposer provenance
- protected-span overlap
- reversible inverse
- alignment status

Candidate equivalence is based on applied source→output transformation, not proposer-specific internal edit decomposition.

## 5. Protected invariants

Automatic authorization must never silently modify protected material, including:
- numbers
- units
- equations
- citations
- URLs
- emails
- code/Latin fragments
- high-confidence named entities
- document structural markers

## 6. Proposed candidate-stage gate

Before building any selector:

Measure on frozen CALIBRATION only:
- P1 recall
- P2 recall
- union recall
- marginal unique recall
- operation-family recall
- conflict rate
- candidate volume
- canonicalization failure
- protected-span proposal rate

Proposed gate:
- union recall >=95% → proceed to selector design
- 90% to <95% → methodological review
- <90% → revisit proposer architecture

Reasoning:
the final selective layer will reject unsafe proposals; therefore the proposal stage needs headroom above the eventual >=90% strict residual recall target.

## 7. Proposed proposer-retention rule

Retain a proposer only if it:
- adds >=1.0 percentage point unique union recall; OR
- materially improves a preregistered weak operation family; OR
- supplies unique corroborating evidence that reduces uncertainty.

Otherwise remove it.

## 8. Proposed automatic-authorization safety target

For AUTO_SAFE edits:
- conservative mandatory-edit precision lower bound >=98%
- zero protected-invariant failures
- zero unauthorized number/unit/citation changes

Low-confidence valid edits should go to REVIEW rather than lowering the precision target.

## 9. Candidate future components NOT currently authorized

- cross-domain AraBART proposer
- MTAGEC
- STAGEET
- generic LLM proposer
- any learned selector
- any LLM authorizer

These require separate justification after P1+P2 union behavior is known.

## 10. Important anti-bias constraints

Please do NOT assume MP-SEF is the right architecture.

Actively look for reasons it should be rejected.

Do NOT recommend proceeding merely because individual papers report good benchmark F-scores.

Do NOT weaken frozen gates to fit observed results.

Do NOT use INTERNAL_EVALUATION, STRESS_DIAGNOSTIC, QALB15 TEST, Confirmation, Holdout, A7'ta reserve, or reserved Nahw IDs.

## 11. Questions for independent review

1. Is separating proposal generation from authorization the right abstraction for ACAD_PASS, given that the product prioritizes scientific/factual preservation over full-sentence GEC benchmark scores?

2. Is a two-proposer initial pool (iterative SWEET + GED-conditioned AraBART) sufficiently heterogeneous to make the first union-recall experiment meaningful?

3. Is >=95% representation-invariant candidate-union recall a defensible pre-selector feasibility gate, too strict, or too weak? Provide a principled alternative only if necessary.

4. Does the proposed union-recall design risk construct invalidity because seq2seq outputs may contain multi-edit coupled transformations that cannot be safely decomposed into independent source-anchored transactions?

5. Should candidate recall be measured at:
   - gold edit instance level,
   - sentence-level complete repair,
   - error-family level,
   - or a combination?
   Specify the primary endpoint and mandatory secondary endpoints.

6. Is proposer marginal gain >=1 pp a sound retention rule? If not, what should replace it?

7. What leakage or double-dipping risks exist when the same CALIBRATION set is used to:
   - assess proposer feasibility,
   - later calibrate a selector?
   Should a new split be preregistered before candidate-union evaluation?

8. Should the selector later be trained on proposer-generated candidate distributions from the same corpus, or should candidate generation/calibration be separated by sentence partitions?

9. What is the strongest reason NOT to use iterative SWEET as P1, given that H1-v1 failed one-pass recall?

10. What is the strongest reason NOT to use AraBART+Morph+GED as P2?

11. Is a simpler architecture likely to dominate MP-SEF for this product objective, for example:
    - GED-first REVIEW routing with conservative correction suggestions,
    - seq2seq suggestion-only with no learned selector,
    - staged typed editing,
    - or another architecture?

12. Before any selector is built, what exact stop rules should be frozen to prevent an endless proposer-adding loop?

13. Given the existing evidence, should the project:
    A. proceed with P1+P2 union feasibility,
    B. modify the candidate-stage protocol first,
    C. replace one proposer before measurement,
    D. abandon multi-proposer fusion in favor of a simpler REVIEW-first design?

Do not rank options unless justified by explicit methodological criteria. Explain the falsifiable conditions under which each option becomes preferable.

## 12. Requested output format

Return:
1. fatal methodological concerns, if any;
2. non-fatal design corrections;
3. whether P1+P2 union evaluation is scientifically interpretable as currently proposed;
4. exact metrics/gates that should be frozen before running it;
5. exact stop rules;
6. whether a selector should be allowed at all if the candidate stage passes;
7. any architecture that is materially better and why;
8. confidence and unresolved uncertainties.

Keep the review focused on methodology, construct validity, leakage, reproducibility, and safety—not implementation convenience.
