# ACAD_PASS — Gate C EXT/META Pre-Execution Review Decision V2

Date: 2026-10-04
Status: ACCEPTED WITH ESSENTIAL CHANGES / NO EXECUTION AUTHORIZED

## 1. Independent review verdict

Higher-model verdict:

`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

Interpretation:
- proceed to dataset/version/split/adapter/metric/overlap freezing;
- zero new-human recruitment at this stage;
- do not execute external benchmarks yet;
- do not modify V2.4;
- do not open the original custom 80-study holdout.

## 2. Five required changes accepted

1. H1 must be defined by two required functions, not by a minimum number of dataset names:
   - output-content support/factuality;
   - preservation/completeness of required source content.

2. H2 and H3 are valid only if their labels can be compared to actual frozen V2.4 outputs without inserting a new semantic inference layer.

3. Evidence-location correctness must be separated from semantic-support correctness.
   Matching a span/reference is not proof that the evidence semantically supports the decision.

4. META oracle validity must be independent not only from verifier outputs but also from the semantic assumptions/rules of the extractor being tested.

5. Per-track denominators, sample-size targets, success criteria and missing/invalid-output handling must be frozen before prediction.
   Empty denominators, unmatched relations or missing outputs cannot be silently dropped.

## 3. Hard-gate interpretation

H1:
scientific transformation fidelity, explicitly separating:
- support of generated content;
- preservation of required source content.

H2:
scientific claim/evidence support or contradiction only.
No full-rewrite completeness claim.

H3:
fine-grained local relation/argument support and localization.
No full-source coverage claim.

H4:
deterministic ACAD_PASS metamorphic behavior under independently justified semantic oracles.
No natural-distribution prevalence claim.

All four hard gates must pass.
A MIXED state is not a full progression PASS.

## 4. H1 resource decision

- FactPICO: `CONDITIONAL SUBSTITUTE`
- FaReBio: `CONDITIONAL SUBSTITUTE`
- LongSciVerify: `DIAGNOSTIC ONLY`

Minimum H1 principle:
use the minimum non-redundant set of human/expert-labeled resources that jointly establishes both:
1. supported output content; and
2. preservation of required source content.

Current preferred candidates for freezing:
- human-annotated real-system CLEF SimpleText material;
- eligible PLABA/TREC units whose actual human judgments establish the required preservation/completeness property.

If those exact labels do not jointly cover both H1 functions, add a targeted substitute:
- FactPICO where PICO/finding preservation is the missing construct;
- FaReBio where source-faithfulness/support is the missing construct.

Resource count alone is not a validity criterion.

## 5. H2/H3 boundaries

SciFact:
- SUPPORT is support for the specified claim/evidence pair only;
- NO EVIDENCE is not ACAD_PASS REVIEW by default;
- gold-selected evidence cannot be used to claim full evidence-retrieval evaluation.

QASemConsistency:
- use relation-level semantics only;
- unsupported may contain different semantic failure types and must not be forced into one ACAD_PASS decision without exact justification;
- background-knowledge policy must be reconciled with V2.4 source-bounded context;
- gold QA decomposition is evaluation material, not inference-time assistance;
- unmatched system relations remain in the frozen denominator where applicable.

If a valid comparison requires a new semantic component, the track is:
`NOT_READY`

## 6. META/REVIEW decision

No new human labels are currently required for controlled REVIEW testing.

Each META case must have:
- pre-prediction applicability conditions;
- oracle independent from V2.4/extractor semantic rules;
- proof of expected preservation, violation or unresolved relation;
- matched anti-degenerate controls;
- fixed exclusion rules.

REVIEW requires:
- at least two materially different critical interpretations remain possible under allowed context;
- no higher-precedence REJECT or INVALID condition applies.

This supports controlled REVIEW behavior only, not natural-world ambiguity prevalence.

## 7. Adapter boundary

A legitimate adapter may:
- select/freeze records;
- serialize/rename fields;
- preserve offsets;
- perform preregistered arithmetic/format conversion;
- apply mappings whose semantic equivalence is already demonstrated;
- compute metrics after predictions are frozen.

An adapter becomes a new semantic model if it:
- resolves reference/coreference/entailment/ambiguity;
- generates semantic claims/relations needed for success;
- repairs negation, ownership, equations or relation binding;
- retrieves evidence using gold rationale to make the verifier succeed;
- infers missing labels;
- disables required coverage.

Deterministic/rule-based does not automatically mean adapter-safe.

## 8. Statistical decision

No universal N is frozen now.

For every hard track, before execution freeze:
- primary source-cluster unit;
- exact denominator(s);
- required safe/error classes;
- target confidence precision or error bound;
- sample-size calculation/justification;
- cluster-aware uncertainty method;
- zero-event upper-bound reporting;
- invalid/missing-output treatment;
- confirmatory vs diagnostic subgroup status.

Multiple relations/examples/annotators from one source do not create independent source clusters.

## 9. Public-gold independence claim

Prediction-first / label-second remains useful as procedural anti-leakage control.

Allowed description:
`prospectively executed under frozen procedures, with predictions fixed before joining them to previously published external human/expert labels`

Not allowed:
- secret holdout;
- unseen-to-developers;
- no prior benchmark exposure.

## 10. Diagnostic promotion decision

No diagnostic dataset is promoted to a hard gate now.

Current diagnostic set remains:
- DeFacto
- USB
- PlainFact
- QASPER
- FENICE
- TRUE or AggreFact
- LongSciVerify
- other optional transfer/long-document resources

Promotion is allowed only before predictions and only to close a documented construct gap.

## 11. Readiness decision

The existing ten readiness conditions remain sufficient as the top-level framework.
No eleventh condition is added.

The second independent review completes condition 1 only after the required protocol changes are incorporated.

Conditions 2-10 remain unfulfilled until evidence is frozen.

## 12. Current authorization

AUTHORIZED NEXT:
`dataset / version / split / adapter / metric / overlap freezing`

NOT AUTHORIZED:
- external benchmark prediction/execution;
- original custom 80-study Gate C opening;
- new-human recruitment;
- V2.4 runtime modification.

Quality delta:
`IMPROVED`

Reason:
construct boundaries, adapter boundaries, META oracle independence, denominator rules and statistical precommitment are now stricter than V1.
