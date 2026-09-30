# M2-H H2 Evidence-Constrained Development Iteration v2

Date: 2026-09-30
Status: **FROZEN BEFORE H2-v2 METRICS**
Scope: **CALIBRATION only**
Parent: `M2H_COMPONENT_CALIBRATION_FREEZE_V1.md`

## 1. Why a v2 development iteration exists

H2-v1 tested surface families alone. None of the five non-diagnostic families cleared the frozen 98% precision gate.

This v2 iteration does **not** lower that gate and does not redefine observed examples. It introduces an explicitly versioned, narrower acceptance predicate for the already frozen `ALIF_VARIANT` surface family using independent morphology/lexicon evidence, as anticipated by the M2-H architecture.

No `REFERENCE_UNSUPPORTED` example from the blind packet has been inspected to design these predicates.

## 2. Human-review bottleneck decision

Human review is **not a prerequisite for H2-v2 automatic activation**.

The existing blind adjudication packet remains a useful optional external-validity study, but lack of accessible human reviewers must not block component development.

H2-v2 promotion is based only on preregistered automatic evidence and the unchanged CALIBRATION precision gate.

No claim of independent human validation may be made from H2-v2.

## 3. Candidate scope

Only H1 candidates already matching the frozen `ALIF_VARIANT` surface predicate are eligible.

All H2-v1 common exclusions remain:
- no boundary change;
- no insertion/deletion/reordering;
- no multi-token replacement;
- no punctuation-only edit;
- no protected-span overlap;
- no extraction invariant failure.

## 4. Frozen morphology source

CAMeL Tools / CALIMA MSA:
- CAMeL Tools git revision:
  `be79ca9fc493f0df795375a7255bafef246a802d`
- built-in morphology DB:
  `calima-msa-r13`
- frozen morphology.db SHA256:
  `195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70`

The morphology analyzer is independent of H1 predictions and H1 confidence.

## 5. H2-v2 automatic acceptance predicate

An `ALIF_VARIANT` candidate is `H2_V2_SUPPORTED_MANDATORY_CANDIDATE` only if **all** conditions hold:

1. the exact H2-v1 `ALIF_VARIANT` surface predicate passes;
2. source and candidate replacement are each exactly one whitespace token;
3. neither side contains digits, Latin letters, tatweel, or Arabic combining marks;
4. CALIMA-MSA returns **zero analyses** for the source token;
5. CALIMA-MSA returns **one or more analyses** for the candidate token;
6. every retained candidate analysis exposes a non-empty lexical lemma field (`lex`);
7. after standard CAMeL lexical suffix cleanup (remove analysis decoration after `_` or `-` only when it is metadata, not Arabic letters), all retained candidate analyses agree on **one lexical lemma identity**;
8. no retained candidate analysis has a POS label containing `prop` (proper-name risk);
9. no morphology exception/error occurs;
10. all common invariants remain satisfied.

If any condition fails, H2-v2 disposition is `REVIEW`, not forced acceptance.

## 6. Why the predicate is asymmetric

This v2 profile intentionally targets the high-precision pattern:

`source morphologically unattested → candidate morphologically attested`

It does not auto-correct when:
- both forms are analyzable;
- neither form is analyzable;
- candidate morphology is lexically ambiguous;
- candidate could be a proper name.

Those cases remain REVIEW even if the surface substitution looks plausible.

## 7. Frozen promotion gate

Report:
- eligible ALIF_VARIANT candidates;
- accepted H2-v2 candidates;
- exact QALB-supported accepted candidates;
- reference-unsupported accepted candidates;
- strict-reference precision lower bound;
- accepted case coverage;
- invariant failures.

Automatic activation requires:

- accepted candidates `n >= 50`;
- strict-reference precision lower bound **>= 98%**;
- zero invariant failures;
- zero analyzer execution failures among accepted rows.

The 98% threshold is unchanged.

If `n < 50`, the rule is diagnostic only even if observed precision is high.

If precision is below 98%, H2-v2 is disabled. Do not create another narrower rule from the same observed errors in this iteration.

## 8. Role of blind adjudication

The previously generated 250-row blind packet is retained and frozen.

It is no longer on the critical execution path.

If qualified independent Arabic reviewers later become available, their judgments may be reported as external validation. They are not required to proceed to H3/H4.

A higher-capability ChatGPT/model may receive only a small focused ambiguity packet if later needed for diagnostics; it does not convert H2-v2 into human validation.

## 9. Scientific interpretation

Passing H2-v2 means:
- a narrowly defined automatic ALIF_VARIANT subset cleared a conservative development precision gate;
- not that all ALIF_VARIANT edits are safe;
- not that human validation was performed.

Failing H2-v2 means:
- H2 automatic ALIF_VARIANT remains disabled;
- project proceeds to H3/H4 rather than blocking on reviewer recruitment.

## 10. Reserved data

Remain unopened:
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST
