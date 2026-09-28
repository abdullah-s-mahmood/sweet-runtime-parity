# Phase 2 — WAW_ALIF Morphosyntactic Recovery Gate: End Review

Date: 2026-09-28

## Decision

**WORSENED / MODIFY for the WAW_ALIF auto-accept hypothesis.**

The project is epistemically improved because a new natural-data failure mode was exposed before promotion.

Canonical natural-data run:
- GitHub Actions: 36480900219
- conclusion: success
- ZAEBUC-v1.0 Arabic TRAIN
- fresh raw-selected slice, excluding the prior 30 consumed train lines
- 60 selected lines from 111 raw terminal-waw-eligible lines
- runtime decisions frozen before gold
- ZAEBUC DEV not used
- ZAEBUC TEST not used

Counterfactual verifier run:
- GitHub Actions: 36482011651
- conclusion: success
- 15 authored cases
- not a generalization benchmark

## QALB15 coverage diagnosis

The earlier QALB15 100-line slice contained only **one** generator event of shape:
source ends و; candidate = source + ا.

That source was contextually analyzed as `noun_prop`.

Therefore the earlier WAW_ALIF_VERB_ONLY result of zero accepts was **coverage-zero / UNPROVEN**, not a quality failure.

## Fresh natural ZAEBUC WAW slice

### SOURCE_SHAPE_ONLY — diagnostic

- events: 7
- exact gold: 6
- nonexact same-span: 1
- exact rate: 85.71%

The one nonexact event was unsafe after contextual review.

### WAW_ALIF_MORPH_RECOVERY — diagnostic

- events: 4
- exact gold: 3
- contextual wrong: 1
- supported after review: 3/4 = 75.0%
- wrong accepted: 1/4 = 25.0%

The policy reduced 7 shape candidates to 4, but it **did not remove the only unsafe event**. It therefore did not improve observed precision on this slice.

### WAW_ALIF_MORPH_STRICT — promotion candidate

- accepted: 0
- preferred minimum in pre-registration: 3

Decision:
**UNPROVEN_LOW_COVERAGE**.

A zero-error rate on zero accepts is not success.

## Natural counterexample

Bounded source context:
`نشر شي خطأ و كل الناس شافو في هذه الحاله`

Candidate:
`شافو → شافوا`

Gold:
`شافو → شافوه`

Judgment:
**WRONG_CORRECTION / MEDIUM**

Failure:
**OBJECT_CLITIC_OMISSION_AMBIGUITY**

Why:
the candidate assumes the final waw is terminal واو الجماعة and appends differentiating alif. In the intended correction the verb carries the attached object pronoun `ـه`; the waw is therefore not terminal and the differentiating alif is not written.

This falsifies the stronger assumption:
"candidate is plural verb + source has no valid singular/nominal analysis" is sufficient proof for adding final alif.

## Counterfactual verifier

WAW_ALIF_MORPH_RECOVERY:
- MUST_NOT_ACCEPT false accepts: 0/7
- accepted unambiguous positives: 4/6
- accepted locally ambiguous positives: 0/2

This was encouraging but insufficient. The natural corpus exposed an ambiguity absent from the authored challenge: **missing object clitic vs missing differentiating alif**.

WAW_ALIF_MORPH_STRICT:
- false accepts: 0/7
- positive accepts: 0/8

It is safe by abstention but not useful.

## Research interpretation

Arabic orthographic descriptions state that the differentiating alif follows terminal group waw attached to a verb and is not written when the waw is non-terminal. This makes clitic structure part of the correctness proof, not merely POS/number.

CAMeL morphology provides POS/number/person/aspect/mood and enclitic features, but a malformed source can be unanalyzable while multiple repairs remain morphologically plausible.

Therefore:
- candidate analyzability is evidence, not proof;
- source unanalyzability is evidence, not proof;
- context can distinguish missing alif from a missing enclitic/object;
- dependency/complement structure or independent edit agreement is required before expanding this family.

## Comparison with prior stage

Previous ZAEBUC disjoint generic structural policy:
- 5/6 supported after contextual review = 83.33%
- 1 wrong = 16.67%

Targeted WAW Recovery:
- 3/4 supported = 75.0%
- 1 wrong = 25.0%

These are different populations, so the percentage comparison is descriptive rather than a controlled head-to-head. Still, the WAW rule did not solve the contextual-safety problem.

## Frozen post-gate status

- NUN insertion/deletion: **REVIEW_ONLY**
- generic accusative/final-alif: **REVIEW_ONLY**
- WAW_ALIF_MORPH_RECOVERY: **REVIEW_ONLY**
- WAW_ALIF_MORPH_STRICT: **UNPROVEN / do not auto-accept**
- destructive vetoes remain candidates for separate validation
- no Phase 3
- no final sealed benchmark

## Recommended next technical direction

Do **not** add more local character thresholds.

Highest-value next hypotheses:

1. **Cross-corpus independent edit agreement**
   Run the independent correction generators on a fresh external population and test exact edit-event agreement directly. This is the most direct generalization test of the project's best existing acceptance idea.

2. **Context-aware syntactic evidence**
   Explore CamelParser2.0/dependency evidence for controller/subject/complement structure, but validate parser mistakes as a separate safety layer before use.

3. **Counterfactual context suite**
   Expand authored tests to include:
   - root-waw vs group-waw;
   - nominal construct waw;
   - missing object clitic vs missing final alif;
   - number/controller changes;
   - VSO/SVO agreement differences.

4. **Source-validity veto**
   Preserve the useful observation that a valid source singular-verb or nominal analysis blocks destructive `+ا` rewrites. Treat it as a veto, not a positive acceptance oracle.

The architecture remains:
candidate generation -> complete edit event -> independent evidence -> context/morphosyntax -> ACCEPT/REVIEW/REJECT -> downstream scientific/semantic/document verification.
