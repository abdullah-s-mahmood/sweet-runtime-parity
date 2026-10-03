# AT0-EN V2.4 B2.1 — Higher-Model Architecture Response V1

Date: 2026-10-03
Role: Independent Chief Architect / Research Reviewer

## Verdict

`HYBRID_RELATION_AWARE_EXTRACTION_REPAIR`

Disposition:
- GO for extraction/representation repair.
- NO-GO for progressing beyond B2 yet.
- Do NOT redesign the full architecture.
- Do NOT modify the aligner to compensate for missing semantics.

## Blocking capabilities

The following capabilities are blocking B2 progression:

1. Predicate / paraphrase normalization.
2. Negation and semantic-operator scope ownership.
3. Owner-to-value / owner-to-meaning binding across split/merge.
4. Citation-to-claim binding.
5. Equation/symbol/coefficient binding.

Not currently required as independent blockers:
- generic procedural-order parsing;
- generic local coreference resolution.

Candidate/source extraction symmetry is required at the semantic-contract level, but GE vs EG differences alone do not prove asymmetric implementation.

## Deterministic vs semantic boundary

- Predicate/paraphrase normalization: HYBRID.
  Use controlled normalization where equivalence is explicit; otherwise abstaining semantic extraction.

- Negation/scope: HYBRID.
  Surface negation markers are useful but insufficient alone for determining scope ownership.

- Owner/value and owner/meaning binding: HYBRID.
  Deterministic when ownership is explicit; semantic with abstention when context is required.

- Citation binding: primarily DETERMINISTIC HIGH-PRECISION when explicit.
  Ambiguous attribution remains unresolved.

- Equation/symbol binding: primarily DETERMINISTIC HIGH-PRECISION for supported structures.
  No need for general mathematical equivalence proving.

Normalization must never conflate:
- association with causation;
- absence of evidence with negation;
- uncertainty with assertion;
- scientific attribution with unattributed text.

## Keep or replace A2

Decision:
`KEEP_A2_AND_ADD_RELATION_AWARE_STRUCTURED_LAYER`

Conditions:
- the new layer may read original text, allowed local context, exact evidence, and deterministic anchors;
- it must not rely only on A2 output when the required relation was never represented there;
- A2 remains responsible for anchor/provenance extraction and assertion proposals;
- derived representation may repair decomposition or role assignment only when supported by explicit evidence and audit trace;
- broad semantic-parser replacement is not justified by current evidence.

## Minimum repair scope

1. Define a limited structured relation contract for the five blocking capability families.
2. Add predicate/operator normalization while preserving negation, modality, attribution and causality.
3. Add canonical ownership facts that survive split/merge.
4. Extract explicit citation and supported equation/symbol relations.
5. Apply the same semantic contract independently to source and candidate, preserving missing/uncertain information.
6. Freeze and version all repairs before revalidation; no pair-ID-specific patches and no aligner changes to hide extraction loss.

## Minimum revalidation gate

Rerun the same frozen four-arm B2 experiment.

EE safety must remain:
- adversarial acceptance: 0/6
- dangerous critical false preserve: 0
- critical uncertainty promotion: 0
- ambiguous pair remains REVIEW

EE usability must reach:
- safe acceptance >= 4/5 = 80%
- pair accuracy >= 11/12 = 91.67%
- faithful false rejection <= 1/5

Additional requirements:
- GG hard gates remain 100%
- deterministic anchor/provenance checks do not regress
- critical relations used in decisions are audited against source text independently on each side
- GE and EG remain separately reported

Passing the existing B2 development gates is sufficient to move to the next research stage.

The stronger project targets:
- extracted-graph accuracy >=95%
- authentic safe acceptance >=90%
- automatic-PASS selective precision >=99%

remain later strong-adoption targets, not current B2 progression gates.

No new untouched holdout is required at B2 repair time.

## Authentic-text timing

`IMMEDIATELY_AFTER_RELATION_AWARE_REPAIR_PROTOTYPE_BEFORE_SYNTHETIC_B2_REVALIDATION`

Use a small qualitative set of authentic academic excerpts with context to detect contract blind spots before overfitting the repair around consumed synthetic examples.

This authentic-text check is:
- developmental;
- qualitative;
- not a new benchmark;
- not an additional numeric gate.

## Shared-error safeguards

1. Extract source and candidate independently from their own allowed text/context only.
2. Audit textual support and coverage independently per side.
3. Keep deterministic anchor checks independent from semantic extraction.
4. Never promote uncertain+uncertain agreement or shared omission to PASS.
5. Retain all four arms; unexpected EE success while GE/EG degrade must trigger review for shared error or representation interaction.

These safeguards reduce shared-error risk but do not guarantee its absence.

## Final rationale

The repair is justified by specific semantic losses demonstrated in B2, not by aggregate overmerge alone.

GG=100% localizes priority to extraction/representation on the current development set.

B2 safety-conservatism is encouraging but not sufficient:
0 adversarial acceptance together with 0 safe acceptance is not a usable automatic-verification system.

The correct next action is a limited relation/ownership repair followed by the unchanged frozen B2 gates.
