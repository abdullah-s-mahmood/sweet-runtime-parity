# MP-SEF HIGHER-MODEL INDEPENDENT REVIEW PROMPT V1

You are acting as an independent senior methodological reviewer for ACAD_PASS Phase 2 Arabic / MP-SEF.

Repository:
`abdullah-s-mahmood/sweet-runtime-parity`

Branch:
`phase2-arabic-eval`

This is a **PREMEASUREMENT** review.

P1 and P2 source-only C_F proposal artifacts are already frozen.
`R_joint` has NOT been computed.
A selector has NOT been trained.
Reserved/internal sets remain closed.

## Mandatory first read

Read these files in this order:

1. `phase2/redesign/MPSEF_PREMEASUREMENT_INDEPENDENT_REVIEW_PACKAGE_V1.md`
2. `phase2/redesign/MPSEF_PRE_UNION_PROTOCOL_V3.md`
3. `phase2/redesign/MPSEF_BUNDLE_CONTRACT_V1.md`
4. `phase2/redesign/MPSEF_TARGET_AND_MATCHING_CONTRACT_V1.md`
5. `phase2/redesign/MPSEF_PROTECTED_INVARIANTS_CONTRACT_V1.md`
6. `phase2/redesign/MPSEF_P1_CF_PROPOSAL_LOCK_V1.md`
7. `phase2/redesign/MPSEF_P2_CF_PROPOSAL_LOCK_V1.md`
8. `phase2/redesign/mpsef_build_cf_source_manifest_v1.py`
9. `phase2/redesign/mpsef_p1_cf_proposals_v1.py`
10. `phase2/redesign/mpsef_p2_cf_proposals_v1.py`
11. both P1/P2 GitHub workflow files
12. `RESUME_HERE.md`

Inspect the exact branch contents. Do not rely only on this prompt.

## Frozen facts

- C_F: 1,918 records / 764 clusters.
- Shared source-manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- P1 proposal SHA256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- P2 proposal SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`
- P1 parity: 64/64 batch-vs-single.
- P2 parity: 32/32 all-field batch-vs-single.
- P1 protected-touch: 19/1918.
- P2 protected-touch: 21/1918.
- Empty outputs: 0 for both.
- Gold/reference consulted during proposer generation: false.
- R_joint computed: false.
- Selector trained: false.
- INTERNAL_EVALUATION, STRESS_DIAGNOSTIC, Confirmation, Holdout, A7'ta reserve, and QALB15 TEST remain closed.

## Frozen primary action space

Per source sentence:

- KEEP
- whole P1_FINAL if executable
- whole P2_FINAL if executable

No edit-level fusion.
No gold-guided bundle splitting.
No P1 pass-1 action.
No P2 n-best.
No third proposer.
No selector training before candidate-availability feasibility passes.

## Frozen gate

`R_joint(P1,P2) >= 0.95`

Do NOT weaken, reinterpret, or tune this threshold.

## Your task

Perform an adversarial methodological audit and decide whether we may proceed to:

1. implement a gold-blind executable-action legalizer + scorer;
2. freeze their hashes/workflow;
3. run a second premeasurement preflight;

while still NOT authorizing R_joint measurement yet.

Actively try to falsify the protocol.

## Mandatory scrutiny

### 1. Gold/action leakage
Check for any path by which gold/reference could:
- alter bundle boundaries;
- repair an alignment;
- rescue a protected bundle;
- create a new action;
- shrink denominators;
- choose a favorable decomposition.

### 2. Alignment ambiguity
The proposal runners currently use:
`difflib.SequenceMatcher(..., autojunk=False)`

Determine whether this is sufficient under the frozen Bundle Contract.

If materially different valid decompositions could affect:
- protected-touch status;
- executability;
- source anchoring;
- R_raw;

then require a stronger pre-gold ambiguity-aware legalizer.

### 3. Protected-span veto
Audit:
- insertions at protected boundaries;
- number-unit coupling;
- citation attachment;
- mixed-script technical spans;
- exact protected-text preservation;
- whether alignment ambiguity could hide a protected modification.

If current overlap logic is insufficient, specify the exact pre-gold replacement.

### 4. Truncation
P2 uses:
- num_beams=5
- max_length=100

Determine whether the legalizer must detect and classify:
- generation hitting the ceiling;
- source/input truncation;
- tokenizer/model-length problems;
- uncertain truncation.

No truncated/uncertain case may silently become executable.

### 5. Failure-state completeness
Before any gold scoring, every proposer hypothesis should end in a frozen source-only legality state covering at least:
- OK
- ALIGNMENT_AMBIGUOUS
- ALIGNMENT_FAILED
- TRUNCATED
- EMPTY_OUTPUT
- SOURCE_MISMATCH
- NONREVERSIBLE
- PROTECTED_BLOCKED
- EXECUTION_FAILED

Decide whether a separate frozen **gold-blind executable-action legalizer artifact** is mandatory.

### 6. Reversibility
Define the minimum source-only reversibility proof required for whole-hypothesis actions.

### 7. Exact R_joint scoring
Audit requirements for:
- complete-target credit;
- duplicate-credit prevention;
- mixed punctuation;
- blocked-action handling;
- denominator integrity;
- exact maximization over KEEP/P1/P2;
- R_clean;
- complete-sentence repair.

A heuristic estimate must never be called exact R_joint.

### 8. R_raw isolation
Ensure diagnostic decomposition cannot leak into primary execution or R_joint.

### 9. Runtime parity
Assess whether:
- P1 64/64 parity
- P2 32/32 all-field parity

are sufficient implementation preflights for this development-only cycle, given frozen artifact hashes and no runtime changes after freeze.

### 10. Claim discipline
Even if the later gate passes, the strongest allowed claim is bounded to:

**DEVELOPMENT FEASIBILITY / ADAPTIVELY CONSUMED QALB-2014 ORIGIN / NOT INDEPENDENT GENERALIZATION EVIDENCE**

Do not translate a PASS into 95% correction accuracy, AUTO_SAFE readiness, semantic safety, scientific-document safety, or deployment readiness.

## Required output

Write in Arabic with RTL-friendly headings.

Return:

1. **VERDICT**
   - GO TO SECOND PREFLIGHT
   - MODIFY BEFORE SECOND PREFLIGHT
   - STOP / INVALID DESIGN

2. **CRITICAL FINDINGS**
   For each:
   - ID
   - severity: BLOCKER / MAJOR / MINOR
   - affected contract/file
   - evidence
   - exact fix
   - must fix before measurement: YES/NO

3. **LEAKAGE AUDIT**
   Explicit YES/NO findings for:
   - gold leakage
   - action-space leakage
   - population drift
   - denominator leakage
   - protected-policy leakage
   - reserved-set leakage

4. **EXECUTABILITY AUDIT**
   Cover:
   - alignment
   - ambiguity
   - truncation
   - reversibility
   - protected spans
   - source mismatch
   - failure-state completeness

5. **LEGALIZER/SCORER REQUIREMENTS**
   Give a finite, machine-checkable list.

6. **SECOND PREFLIGHT CHECKLIST**
   Assertions suitable for a GitHub Actions workflow.

7. **CLAIM SCOPE**

8. **WHAT NOT TO DO**
   Include post-result rescue, threshold changes, gold-guided bundle surgery,
   reference rescue, population filtering, and reserved-set opening.

9. **COMPARISON WITH PREVIOUS STATE**
   State IMPROVED / WORSENED / MIXED with concrete evidence.

10. **FINAL DECISION SENTENCE**
   `DECISION: <GO TO SECOND PREFLIGHT | MODIFY BEFORE SECOND PREFLIGHT | STOP / INVALID DESIGN>`

Do NOT compute R_joint.
Do NOT inspect reserved/internal sets.
Do NOT weaken the 95% gate.
Do NOT use gold to redefine the primary action space.
