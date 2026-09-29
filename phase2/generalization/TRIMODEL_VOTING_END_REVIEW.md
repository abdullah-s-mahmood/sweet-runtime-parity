# Phase 2 — Cross-Training Tri-Model Voting End Review

Date: 2026-09-29

## Decision

**WORSENED as an auto-accept candidate policy; IMPROVED epistemically.**

Canonical fully corrected run:
- workflow: Phase 2 Cross-Training Tri-Model Voting Gate V2
- run: 36517205396
- conclusion: SUCCESS
- runtime votes frozen before gold: true
- QALB-2015 TEST read: false
- QALB text persisted: false

## Primary policy: UNANIMOUS_3

Fresh population: QALB-2015 L2 TRAIN deterministic 50-line raw-only slice, explicitly excluding the prior 50-line cross-model slice.

Automatic gold comparison:
- accepted events: 142
- exact-gold supported: 94
- non-exact requiring contextual review: 48
  - gold-overlap non-exact span: 23
  - same gold span / different output: 14
  - no gold edit overlap: 11

Bounded contextual adjudication of all 48 non-exact events:
- supported correction: 30
- supported alternative: 2
- partial correction: 12
- wrong correction: 4
- unnecessary: 0

Final primary-policy development-generalization evidence:
- supported total: 126 / 142
- supported precision: 88.7324%
- unsafe: 16 / 142 = 11.2676%
- wrong: 4
- partial: 12

Promotion contract:
- minimum >=10 accepts: PASS
- zero wrong: FAIL
- zero partial: FAIL
- zero unnecessary: PASS

**Decision: DO NOT PROMOTE UNANIMOUS_3.**

## Comparison with previous two-model exact agreement

Previous independent two-model slice:
- supported: 144 / 159
- supported precision: 90.5660%
- unsafe: 15 / 159 = 9.4340%

Tri-model fresh slice:
- supported: 126 / 142
- supported precision: 88.7324%
- unsafe: 16 / 142 = 11.2676%

Descriptive change:
- supported precision: -1.8336 percentage points
- unsafe rate: +1.8336 percentage points

The slices are different, so this is not a causal estimate of adding the third voter. It is sufficient, however, to falsify the hypothesis that cross-training 3/3 agreement is by itself a safe unattended lane.

## Why the third voter did not solve the problem

The unsafe set contains several qualitatively different failure modes:
- incomplete case/number/determiner repairs;
- residual preposition and valency errors;
- complementizer context change;
- possessive/clitic loss;
- lexical semantic substitution;
- tense/aspect drift;
- gender agreement residuals;
- proper-name or multi-part spelling that remains incomplete.

This means three models can converge on the same locally plausible edit while still sharing incomplete repair, context-insensitive orthographic bias, or semantic/morphosyntactic drift.

## Secondary policies

ARABART_PLUS_ANY_SWEET accepted 168 events.
BOTH_SWEETS accepted 202 events.

Both are supersets of the unsafe UNANIMOUS_3 accepts, so neither can satisfy the pre-registered zero-wrong / zero-partial promotion contract. Full manual adjudication of their extra lower-consensus events is not required to reject promotion.

## Implementation/reproducibility repairs

Two CI failures were metadata-only and occurred after successful inference:
- legacy torch wheel did not expose torch.__version__ in SWEET jobs;
- the same issue affected AraBART.

Both were repaired by recording the installed torch version via importlib.metadata.version("torch"). No model, source data, inference output, threshold, vote rule, or evaluation policy changed.

The legacy tri-model workflow was made manual-only; V2 is canonical.

## Fresh research interpretation

- Alhafni & Habash (ACL 2025) show Arabic text-editing models benefit from ensembling, but ensemble improvement does not imply zero-error acceptance.
- Goto et al. (BEA 2026) show edit-level majority voting can mitigate over-correction, not eliminate correlated edit errors.
- CLEME2.0 (ACL 2025) argues for disentangling correct, wrong, under-, and over-correction rather than relying on a single score.
- Multi-pass Decoding (EMNLP 2024) shows iterative refinement can improve GEC and motivates testing whether accepted edits are stable or require subsequent repair.
- COCOGEC (Findings ACL 2026) demonstrates context robustness is a distinct failure axis.

## Architectural conclusion

Do not add another voter merely to increase vote count.
Do not tune model-confidence thresholds on these inspected slices.
Do not return to NLI, GED, lexical-continuity, or simple character-family rules as sole gates.

The evidence points to two missing properties:

1. **Repair completeness / post-edit stability** — a supposedly safe edit should remain stable after accepted edits are applied and the sentence is re-evaluated.
2. **Morphological identity preservation** — an edit presented as orthographic/local should not silently change lemma, POS, person, tense/aspect, number/gender, or clitic structure unless explicitly supported.

## Next recommended gate

**Phase 2 — Post-Edit Stability & Morphological Identity Diagnostic**

First run on the consumed 142 UNANIMOUS_3 events only as a diagnostic:
- apply all unanimous accepted edits to each affected source line;
- rerun the three frozen voters on the corrected line;
- mark whether each original accepted target remains a fixed point or is edited again;
- compare source/candidate contextual morphology with CAMeL morphology;
- materialize stability/morphology evidence before reading the manual labels;
- measure capture of 16 unsafe vs retention of 126 supported.

No promotion from the consumed slice.

Only if a pre-registered policy is promising: freeze it unchanged and validate on a new disjoint raw-only slice.

## Constraints

- No QALB-2015 TEST.
- No final sealed benchmark.
- No Phase 3.
- No training on current manual labels.
- No QALB text persistence.
- Review remains a first-class outcome.