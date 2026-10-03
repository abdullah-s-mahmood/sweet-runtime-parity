# AT0-EN V2.4 — Gate B1 First Human-Correct Aligner Score Closure

Date: 2026-10-03
Status: CLOSED CHECKPOINT / FIRST SCORE FROZEN / REPAIR NOT STARTED

## Execution identity

Workflow:
`AT0-EN V2.4 B1 First Human-Correct Alignment Score`

Run:
`37145678669`

Trigger commit:
`3c3ccde1637cb819cd20987a224bbcfe2354dea1`

Artifact:
- id: `11281074678`
- SHA-256: `245593d8e6af433713553e2cd6489f3b68e92015239ad1e7edafa4323b169647`

No model inference occurred.

## Frozen first result

Status:
**FAIL_B1_HUMAN_CORRECT**

Pairs:
12

Pair-level outcome:
- correct: 10/12
- accuracy: **83.33%**

Critical alignment:
- gold critical alignments: 22
- covered: 20/22 = **90.91%**
- status accuracy on covered critical alignments: **95%**

Safety diagnostics:
- dangerous false-preserve: **0**
- faithful safe-pair rejection: **1**
- material adversarial acceptance: **1**
- uncertainty preservation: **100%**
- critical evidence-trace completeness: **100%**

Mapping shape performance:
- ONE_TO_ONE: 6/7 = **85.71%**
- ONE_TO_MANY: 2/2 = **100%**
- MANY_TO_ONE: 1/2 = **50%**
- MIXED: 1/1 = **100%**

## Hard-gate result

Passed:
- dangerous false-preserve = 0
- critical uncertainty preservation = 100%
- critical evidence trace completeness = 100%

Failed:
- pair outcome accuracy = 100% required; observed 83.33%
- critical gold alignment coverage = 100% required; observed 90.91%
- critical alignment-status accuracy = 100% required; observed 95%
- faithful safe-pair rejection = 0 required; observed 1
- material adversarial acceptance = 0 required; observed 1

Progression to extracted-graph alignment is therefore BLOCKED.

## Frozen failures

### B1-P03 — faithful many-to-one merge falsely rejected

Expected:
`PASS_CANDIDATE`

Predicted:
`REJECT`

Failure:
source definitions:
- U_i -> utilization
- D_i -> normalized deadline pressure

were faithfully merged into one candidate assertion with equivalent bindings.

The aligner compared flattened/structural binding representations too strictly and concluded:
`Material value/symbol binding differs.`

Interpretation:
binding equivalence across split/merge representation is under-modeled.

This is a false rejection, not a dangerous false preserve.

### B1-P04 — relation/value rebinding falsely accepted

Expected:
`REJECT`

Predicted:
`PASS_CANDIDATE`

Source:
- Group A -> 42.0 s
- Group B -> 51.5 s

Candidate:
- Group A -> 51.5 s
- Group B -> 42.0 s

The assignment procedure cross-matched assertions by value similarity strongly enough to pair:
- source Group A / 42.0 with candidate Group B / 42.0
- source Group B / 51.5 with candidate Group A / 51.5

Thus the swapped ownership disappeared from the comparison.

Interpretation:
entity/owner identity must constrain candidate assignment before or more strongly than value similarity.

This is the most important B1 failure because it produced one material adversarial acceptance.

## End-stage research interpretation

Fresh review supports the diagnosis:

- entity and relation structure are core claim variables in scientific verification; canonical entity normalization and relation constraints matter;
- correct final labels are insufficient without aligned evidence/rationales;
- claim-evidence linking remains difficult on scientific text;
- graph structure can help but does not guarantee correct ownership alignment.

Relevant reviewed literature includes:
- Wuehrl et al., EACL 2024, entity/relation properties for scientific fact verification;
- Ho et al., Findings EMNLP 2025, table-text alignment and faithful rationale alignment;
- CLAIM-BENCH, IJCNLP/AACL 2025, scientific claim-evidence reasoning remains challenging.

## Repair direction — NOT YET IMPLEMENTED

Next repair must be principle-based, not pair-ID-based:

1. owner/entity-first assignment:
   stable owner/subject identity and critical context constrain matching before values.

2. relation-aware assignment:
   candidate assignment should consider incident graph relations, not only assertion-local similarity.

3. split/merge binding canonicalization:
   represent equivalent bindings as normalized ownership facts so:
   `U_i -> utilization`
   and a merged mapping carrying the same binding are recognized as equivalent.

4. non-compensation:
   identical values cannot compensate for wrong owners.

5. preserve all B1-P03/P04 failures as development regressions without adding ID-specific branches.

No threshold will be weakened.

## Cumulative V2.4 success ledger

Historical pre-V2.4 end-to-end baseline:
- adversarial escape: 37.5%
- safe automatic acceptance: 25%
- BOTH_FAIL

Gate 0 contract integrity:
- 326/326 PASS
- contract only, not verifier accuracy

Gate A1 deterministic anchors:
- precision: 100%
- recall: 100%
- exact provenance: 35/35

Gate A2 source structural prototype:
- structural sentence representation: 100%
- observed decimal-boundary defects: 5 -> 0 after repair
- semantic accuracy not established in A2

Gate A3 source extractor development:
- gold coverage: 100%
- critical coverage: 100%
- false additions: 0%
- atomic one-to-one: 88%
- certain precision: 92.86%
- error-abstention recall: 87.5%
- unnecessary abstention: 23.53%
- critical silent semantic errors: 0
- PASS_DEVELOPMENT

Gate A4:
- GO_ALIGNMENT_RESEARCH_DEVELOPMENT_ONLY

Gate B1 reference integrity:
- 363/363 PASS
- 12 human-correct graph pairs

Gate B1 first aligner score:
- pair outcome: 83.33%
- critical coverage: 90.91%
- critical status accuracy: 95%
- dangerous false-preserve: 0
- material adversarial acceptance: 1
- faithful false rejection: 1
- FAIL_B1_HUMAN_CORRECT

## Improvement / worsening

Compared with the old V2.3 end-to-end failure, B1 is not directly comparable because it isolates human-correct graph alignment rather than full generation/extraction/verification.

Within B1:
- positive:
  - uncertainty preservation 100%
  - evidence-trace completeness 100%
  - 0 dangerous false-preserve under the scorer definition
  - 10/12 pair outcomes correct
- negative:
  - one material adversarial pair was accepted
  - one faithful pair was rejected
  - hard gate therefore fails

No system-level improvement percentage is claimed.

## Completion

Current checkpoint:
**100% COMPLETE**

Gate B1 overall:
**approximately 70% complete**

Whole ACAD_PASS:
**approximately 27% ±5% complete**

The whole-system estimate does not increase materially because B1 did not pass its hard gate.

## Exact next authorized checkpoint

`AT0-EN V2.4 GATE B1.1 — PRINCIPLE-BASED ALIGNER REPAIR + REVALIDATION`

Scope:
- repair owner-first assignment;
- repair split/merge binding equivalence;
- add relation-aware assignment constraints where needed;
- keep frozen B1 reference and hard thresholds unchanged;
- rerun versioned B1 score;
- preserve first-score failure as canonical negative evidence.

Not authorized:
- extracted-graph alignment
- candidate extraction
- live generation
- HW1-EN
- untouched holdout
- production claims

Higher-model consultation is not required at B1.1 start because the two failure mechanisms are already well localized and remain within the frozen architecture. If repair exposes a new construct-validity issue, stop and consult.
