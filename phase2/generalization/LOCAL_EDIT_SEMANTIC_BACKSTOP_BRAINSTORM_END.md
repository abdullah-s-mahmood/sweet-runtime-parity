# Local-Edit Semantic Backstop — End Brainstorm

Date: 2026-09-29

## Main finding

Generic multilingual semantic NLI is not the missing Arabic proofreading acceptance layer.

## Integrate / preserve

- exact edit-event representation;
- independent generator agreement as evidence;
- protected scientific/document invariants;
- downstream semantic/scientific verifier;
- REVIEW as first-class state;
- strict anti-leakage ordering.

## Drop for Arabic auto-accept

- whole-sentence entailment threshold as the primary GEC gate;
- local-window entailment threshold as the primary GEC gate;
- contradiction-only semantic veto;
- further threshold tuning on the 159 consumed events.

## Highest-value next hypotheses

1. Four-system cross-training vote: test whether architecture + training-corpus diversity reduces correlated wrong edits.
2. Three-of-four edit-level majority voting with architecture-family diversity constraint.
3. Four-of-four unanimity as a high-precision low-coverage candidate.
4. Error-type-conditioned voting only after the pure voting baselines are measured.

## Research alignment

- ACL 2025 Arabic text-editing work reports gains from combining text-editing models.
- BEA 2026 edit-level majority voting reports reduced over-correction from edit-level system combination.
- TACL 2026 argues for edit-representation-centric GEC evaluation rather than whole-sentence embedding similarity.
- Arabic multi-system combination work in 2025 also points toward edit-selection/system-combination, but any non-peer-reviewed evidence remains secondary.

## Forecast

The next likely improvement is not a better global semantic threshold. It is a higher-quality candidate subset created by independent edit voting before semantic verification.

Primary risk: model errors can still be correlated because systems share Arabic corpora, preprocessing, or pretrained encoders.

Therefore training-corpus diversity must be treated as an explicit evidence dimension, not assumed independence.