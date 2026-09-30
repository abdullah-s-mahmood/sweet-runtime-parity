# MP-SEF PREMEASUREMENT INDEPENDENT REVIEW PACKAGE V1

Date: 2026-09-30
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `phase2-arabic-eval`
Review point: **AFTER P1/P2 C_F PROPOSAL FREEZE, BEFORE ANY R_joint MEASUREMENT**

## 1. Review objective

Perform an independent adversarial review of the MP-SEF V3 feasibility protocol and its frozen P1/P2 source-only proposal artifacts.

The reviewer must decide whether the experiment is sufficiently protected against:
- gold leakage;
- gold-guided action construction;
- population drift;
- proposer/runtime drift;
- hidden denominator shrinkage;
- protected-invariant leakage;
- incomplete failure accounting;
- alignment ambiguity;
- truncation/non-reversibility;
- optimistic interpretation of development-only evidence.

The reviewer must NOT calculate or estimate R_joint from the frozen gold/reference data.

Allowed verdicts:
- **GO TO SECOND PREFLIGHT**
- **MODIFY BEFORE SECOND PREFLIGHT**
- **STOP / INVALID DESIGN**

A GO verdict authorizes only implementation of the frozen scorer and second premeasurement preflight. It does NOT authorize selector training, AUTO_SAFE, reserved-set opening, or Phase 3.

---

## 2. Frozen claim scope

Any eventual C_F result must be labeled:

**DEVELOPMENT FEASIBILITY / ADAPTIVELY CONSUMED QALB-2014 ORIGIN / NOT INDEPENDENT GENERALIZATION EVIDENCE**

Historical exposure audit:
- total CALIBRATION: 6,888
- train-origin: 6,571
- dev-origin: 317
- historically independent: false
- gold/reference historically exposed: true
- record-level manual exposure: unknown

C_F is future-role separation only, not restored historical independence.

---

## 3. Frozen future-role split

Full CALIBRATION role split:
- C_F: 1,918 records / 764 clusters
- C_T: 2,898 / 1,020
- C_R: 2,072 / 768

Frozen UID/role/cluster digest:
`85a5dcb1b26a9773ea0ef7e04bb42e8e56dde5d44f1e63fcbe54141dbcb47dfc`

Cluster overlap across roles:
**0**

C_F is the only primary feasibility population for this cycle.

---

## 4. Frozen action-space contract

Primary executable action space per source sentence:

- KEEP
- whole `P1_FINAL` if executable
- whole `P2_FINAL` if executable

Not authorized:
- edit-level fusion;
- P1 pass-1 as an independent action;
- P2 n-best;
- gold-guided bundle splitting;
- partial rescue of a protected-touch bundle;
- third proposer;
- selector training before the candidate-availability gate.

P1 final trace:
`x0 -> x1 -> x2`

Executable P1 action:
`x0 -> x2` as one inseparable whole hypothesis.

P2 trace:
`x0 -> morphology -> GED -> generated y`

Executable P2 action:
`x0 -> y` as one inseparable whole hypothesis.

---

## 5. Frozen primary endpoint

For frozen C_F targets:

`R_joint(P) = sum_s max_{y in A_primary,s(P)} TP_fixed(y,G_s) / sum_s |G_s|`

Primary gate:

`R_joint(P1,P2) >= 0.95`

Interpretation:
- >= 0.95: PASS candidate availability only
- >= 0.90 and < 0.95: FAIL; one diagnostic memo allowed
- < 0.90: FAIL current high-coverage P1+P2 cycle
- interval crossing 0.95: INCONCLUSIVE

Threshold must not change after measurement.

R_joint is an oracle whole-hypothesis availability ceiling. It is NOT selector performance, precision, semantic safety, or complete deployment proof.

---

## 6. Frozen protected-invariants policy

Active hard categories include:
- numbers;
- number-unit structures;
- citations / DOI;
- equations/formulas;
- URL/email;
- code/Latin technical fragments;
- document-structure markers.

High-confidence named-entity detector:
**NOT ACTIVE**

Any inseparable proposal altering a hard-protected span:
- remains recorded diagnostically;
- becomes `PROTECTED_BLOCKED`;
- is excluded from the legal executable action space;
- does not shrink the target denominator.

Unauthorized protected alteration in any legal executable action:
**must equal 0**

---

## 7. P1 C_F frozen evidence

Lock:
`phase2/redesign/MPSEF_P1_CF_PROPOSAL_LOCK_V1.md`

Workflow run:
`36765798233`

Artifact:
- id: `11123050529`
- ZIP digest:
  `sha256:e4020418ca2f2793d4bb79bc766e26838398fb9affba6d0f1c704255cd5aed46`

Exact shared C_F source-manifest SHA256:
`051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`

P1:
- 1,918 / 1,918 cases
- 764 clusters
- batch-vs-single parity: 64 / 64
- changed-vs-source activity: 1,838 / 1,918 = 95.83%
- protected-touch proposals: 19 / 1,918 = 0.99%
- empty outputs: 0
- proposal JSONL SHA256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`

P1 model revision:
`21286e56ce98a86362db540863f91c083b8970f9`

P1 weight SHA256:
`9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d`

Gold/reference consulted during proposal generation:
**false**

R_joint computed:
**false**

---

## 8. P2 C_F frozen evidence

Lock:
`phase2/redesign/MPSEF_P2_CF_PROPOSAL_LOCK_V1.md`

Workflow run:
`36768378938`

Artifact:
- id: `11124303107`
- ZIP digest:
  `sha256:5209633d389db02054456a42710a96a1d6e573cefca308254747897969c7d41c`

P2 consumed the exact same C_F source-manifest SHA256:
`051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`

P2:
- 1,918 / 1,918 cases
- 764 clusters
- batch-vs-single all-field parity: 32 / 32
- morphology parity: 32/32
- GED-label parity: 32/32
- subword-token parity: 32/32
- input-ID parity: 32/32
- GED-label-ID parity: 32/32
- generated-text parity: 32/32
- changed-vs-source activity: 1,906 / 1,918 = 99.37%
- protected-touch proposals: 21 / 1,918 = 1.10%
- empty outputs: 0
- proposal JSONL SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

GED weight SHA256:
`23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f`

GEC weight SHA256:
`5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f`

Gold/reference consulted during proposal generation:
**false**

R_joint computed:
**false**

---

## 9. Measurement remains blocked

At this review point:
- P1 frozen: yes
- P2 frozen: yes
- selector trained: no
- R_joint computed: no
- INTERNAL_EVALUATION opened: no
- STRESS_DIAGNOSTIC opened: no
- Confirmation/Holdout opened: no
- A7'ta reserve opened: no
- QALB15 TEST opened: no

Required remaining sequence:
1. independent protocol review;
2. implement scorer without measuring;
3. freeze scorer and workflow hashes;
4. second premeasurement preflight;
5. explicit authorization decision;
6. only then one C_F measurement.

---

## 10. Mandatory adversarial audit questions

The independent reviewer MUST address each item below.

### A. Gold-blind action construction

Confirm whether the current V3 design guarantees that:
- P1/P2 final hypotheses are fully frozen before gold scoring;
- no target/reference information can modify bundle boundaries;
- no gold can repair a failed alignment;
- KEEP/P1/P2 is the complete primary action set.

Identify any path by which scorer implementation could accidentally create a favorable action after viewing gold.

### B. Source-to-output alignment ambiguity

Current proposal runners use deterministic source-to-output diagnostic alignment based on Python `difflib.SequenceMatcher(..., autojunk=False)`.

Review whether this is sufficient under the frozen Bundle Contract, which states that materially different valid decompositions must not be resolved in a gold-favorable way.

Important:
- primary execution is whole-hypothesis;
- diagnostic decomposition affects protected-touch accounting and R_raw;
- ambiguity must not silently increase executability or target reachability.

Decide whether a pre-gold ambiguity detector or a stronger exact protected-preservation test must be added before measurement.

### C. Protected-span veto correctness

Review the current source-only protected precheck.

Questions:
- Can insertions at protected-span boundaries alter number/unit/citation semantics while evading the current overlap rule?
- Is exact protected-span preservation proven robustly enough for whole-hypothesis legality?
- Should number-unit coupling use a stricter structural invariant than raw character overlap?
- Can alignment ambiguity cause a protected modification to be missed?

Any required strengthening must occur BEFORE gold scoring.

### D. Truncation accounting

P2 uses frozen generation parameters including:
- `num_beams=5`
- `max_length=100`

Current frozen P2 proposal summary reports empty outputs but does not itself prove that no output was truncated at the generation ceiling.

Bundle Contract V1 requires accountable `TRUNCATED` states.

Decide whether the premeasurement legalizer must:
- detect generated sequences hitting the length ceiling;
- detect source/input truncation;
- mark uncertain cases non-executable;
- preserve them in denominators.

No post-result rescue is allowed.

### E. Full failure-state accounting

Before gold measurement, every C_F proposer hypothesis must terminate in a frozen source-only legality state covering at least:
- OK;
- ALIGNMENT_AMBIGUOUS;
- ALIGNMENT_FAILED;
- TRUNCATED;
- EMPTY_OUTPUT;
- SOURCE_MISMATCH;
- NONREVERSIBLE;
- PROTECTED_BLOCKED;
- EXECUTION_FAILED.

Current proposal generation explicitly records empty/protected prechecks but may leave some final legality states for the upcoming legalizer/scorer layer.

Decide whether a separate **gold-blind executable-action legalizer artifact** is required before scorer authorization.

### F. Reversibility

Review whether whole P1/P2 text transformations need an explicit deterministic reversibility check beyond retaining original source and final output.

If reversibility is required by the contract, define the minimum source-only proof needed before scoring.

### G. R_joint exactness

Because each sentence has at most KEEP/P1/P2, exact maximization should be trivial.

Review:
- target matching;
- complete-target credit;
- duplicate-credit prevention;
- mixed punctuation handling;
- blocked-action handling;
- denominator integrity;
- reference-incompatible extra edits for R_clean;
- complete-sentence repair definition.

No heuristic point estimate may be called exact R_joint.

### H. R_raw separation

Verify that diagnostic components can be used for R_raw without becoming executable actions.

Ensure:
- R_raw cannot leak back into R_joint action construction;
- R_raw >= R_joint is diagnostic, not a rescue mechanism;
- any decomposition/fusion opportunity remains future work.

### I. Runtime parity sufficiency

P1 batch/single parity:
64/64.

P2 batch/single all-field parity:
32/32.

Review whether these are adequate implementation preflights for this development-only cycle, given that:
- full proposals are frozen by artifact hashes;
- parity is not being used as a statistical quality claim;
- no runtime change is allowed after measurement begins.

### J. Claim discipline

Confirm that even a PASS at R_joint >=95% would support only:
**candidate availability feasibility on adaptively consumed development-origin data**

It must NOT be translated into:
- independent generalization;
- 95% correction accuracy;
- AUTO_SAFE readiness;
- semantic safety;
- scientific-document safety;
- product-level deployment readiness.

---

## 11. Required reviewer output

Return a structured report containing:

1. **VERDICT**
   - GO TO SECOND PREFLIGHT
   - MODIFY BEFORE SECOND PREFLIGHT
   - STOP / INVALID DESIGN

2. **CRITICAL FINDINGS**
   Each with:
   - severity: BLOCKER / MAJOR / MINOR
   - exact contract section affected
   - evidence
   - whether it must be fixed before measurement

3. **LEAKAGE AUDIT**
   Explicit YES/NO findings for:
   - gold leakage
   - action-space leakage
   - population drift
   - denominator leakage
   - protected-policy leakage
   - reserved-set leakage

4. **EXECUTABILITY AUDIT**
   Explicit assessment of:
   - alignment
   - ambiguity
   - truncation
   - reversibility
   - protected spans
   - failure-state completeness

5. **SCORER AUDIT REQUIREMENTS**
   Exact invariants the scorer/legalizer must enforce before any measurement.

6. **GO/NO-GO CHECKLIST**
   A finite checklist that can be converted directly into the second premeasurement preflight.

7. **CLAIM SCOPE**
   State the strongest scientifically defensible claim if the candidate-availability gate later passes.

8. **WHAT NOT TO DO**
   List any tempting post-result rescue steps that would invalidate the experiment.

Do not calculate R_joint.
Do not recommend weakening the 95% gate.
Do not open reserved/internal sets.
Do not propose gold-guided bundle splitting.
