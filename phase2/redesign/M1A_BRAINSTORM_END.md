# M1-A — End Brainstorming and Adversarial Review

Date: 2026-09-30

## What changed after execution

The initial idea was “find a replacement for two unavailable reviewers.” The stronger formulation is now:

> Do not replace the reviewers with one surrogate. Build an evidence federation from prior human correction work, test only the claims each source can support, and reserve independent material for later confirmation.

## Ideas retained

### 1. Multi-source expert evidence federation
KEEP.

QALB, ZAEBUC, A7'ta and frozen Nahw serve complementary purposes:
- QALB: scale + edit structure + controlled incompleteness;
- ZAEBUC: professional university-writing correction;
- A7'ta: explicit expert linguistic error/correction rules;
- Nahw: local correction plus explanation.

### 2. CLEAN_REFERENCE_KEEP
KEEP.

A human-corrected reference can be fed unchanged as a clean input to test whether a verifier/corrector unnecessarily edits it. This is a stronger overcorrection-control family than relying on the rare naturally unchanged raw QALB lines.

### 3. ERRONEOUS_SOURCE_KEEP
KEEP.

When a raw source differs from its expert-corrected reference, leaving the raw source unchanged gives a defensible incomplete-repair example relative to the reference.

### 4. Controlled partial repairs
KEEP, but label explicitly as counterfactual.

ONE_OF_MANY and ALL_BUT_ONE are ideal for testing whether a verifier can distinguish a locally valid edit from sentence-level completeness. They are not natural model outputs and must not be reported as such.

### 5. Frontier LLM as future verifier
KEEP FOR M2, not as gold.

The verifier should be evaluated against expert-grounded evidence; its own rationale/consensus is not a substitute for that evidence.

## Ideas rejected or demoted

### Single-reference mismatch = wrong
REJECT.

QALB's own multi-annotator evidence shows acceptable variation.

### Majority vote of several LLM personas = human consensus
REJECT.

Correlated models/personas do not create independent linguistic expertise.

### Synthetic random wrong edits as core negative gold
DEMOTE.

They may be useful for robustness, but controlled withheld-human-edit negatives are more faithful to the actual “correct-but-incomplete” bottleneck.

### Tibyan as primary gold
DEMOTE TO GENERALIZATION/STRESS.

Expert review is valuable, but ChatGPT augmentation reduces independence for the exact frontier-LLM question.

### Immediate return to the 24 local project cases and let the agent judge them
REJECT AS GOLD.

Keep them as an unconfirmed project challenge set until external evidence has calibrated M2 and, eventually, a human expert becomes available.

## New high-value opportunities

1. **M2 verifier evaluation should be split by evidence source**, not pooled only:
   QALB, ZAEBUC and A7'ta each expose different distributional failure modes.

2. **Use the 88 reserved A7'ta pairs as a true untouched M2 external confirmation set.**
   Do not expose them during prompt/rubric tuning.

3. **Add a source-held-out test**:
   tune a verifier rubric on QALB/ZAEBUC bootstrap evidence, then evaluate on reserved A7'ta. This is stronger than random in-corpus splits.

4. **Use Mohi et al. 2026 rubric dimensions in M2**:
   grammatical correctness, fluency, meaning preservation—but ACAD_PASS should add repair completeness and abstention.

5. **Treat scientific fidelity as a distinct future challenge set**, not a label inferred from learner corpora.
   Scientific text needs protected claims, quantities, citations, negation, modality, attribution, causal/comparative relations.

6. **Human expert acquisition remains useful but can be small and strategic later**:
   rather than asking experts to label thousands of examples, ask them to adjudicate only disagreement/ambiguity cases selected after M2. This can reduce future expert burden dramatically.

## Next recommended move

Proceed to an **M1 evidence-coverage audit / M2 pre-registration**, not to new training.

M2 should test one strong frontier verifier on frozen expert-grounded candidates with:
- source held out where possible;
- exact prompt/rubric frozen before reserved evidence;
- KEEP as a first-class option;
- correctness and completeness scored separately;
- no QALB15 TEST or sealed ACAD_PASS benchmark.
