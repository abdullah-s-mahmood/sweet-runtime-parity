# AT0-EN V2.4 — Gate B2 First Four-Arm Degradation Score Closure

Date: 2026-10-03
Status: CLOSED CHECKPOINT / MIXED_B2_REPAIR_REQUIRED / FIRST SCORE FROZEN

## Execution

Workflow:
`AT0-EN V2.4 B2 First Four-Arm Score`

Run:
`37147162271`

Trigger commit:
`a9ddba31771f562dfd728fd09270994e7047007a`

Artifact:
- id: `11282800994`
- SHA-256: `a65a76ccd0fa819e819ff9bf6c94529b0e893ad94261d64e3c14bdb301c43a96`

No model inference occurred.

## Four-arm result

### GG — Gold source -> Gold candidate
- pair accuracy: **12/12 = 100%**
- safe acceptance: **5/5 = 100%**
- adversarial acceptance: **0/6**
- REVIEW preservation: **100%**

### GE — Gold source -> Extracted candidate
- pair accuracy: **5/12 = 41.67%**
- safe acceptance: **0/5 = 0%**
- adversarial acceptance: **0/6**
- REVIEW preservation: **100%**

Degradation vs GG:
- pair accuracy: **-58.33 pp**
- safe acceptance: **-100 pp**

### EG — Extracted source -> Gold candidate
- pair accuracy: **6/12 = 50%**
- safe acceptance: **1/5 = 20%**
- adversarial acceptance: **0/6**
- REVIEW preservation: **100%**

Degradation vs GG:
- pair accuracy: **-50 pp**
- safe acceptance: **-80 pp**

### EE — Extracted source -> Extracted candidate
Primary B2 arm.

- pair accuracy: **4/12 = 33.33%**
- safe acceptance: **0/5 = 0%**
- adversarial acceptance: **0/6**
- faithful false rejection: **2**
- REVIEW preservation: **100%**
- critical uncertainty promotion: **0**
- dangerous critical false preserve: **0**

Degradation vs GG:
- pair accuracy: **-66.67 pp**
- safe acceptance: **-100 pp**

Interaction:
- EE pair accuracy vs GE: **-8.33 pp**
- EE pair accuracy vs EG: **-16.67 pp**

## Gate disposition

Result:
`MIXED_B2_REPAIR_REQUIRED`

Safety gates:
**PASS**
- 0/6 adversarial acceptance
- 0 dangerous critical false preserve
- ambiguous pair remains REVIEW
- 0 critical uncertainty promotion

Usability gates:
**FAIL**
- safe acceptance required >=80%; observed 0%
- pair accuracy required >=91.67%; observed 33.33%
- faithful false rejection required <=1; observed 2

No safety threshold was weakened.

## Primary diagnosis

The B1.1 aligner remains mechanically strong on human-correct graphs.

The dominant B2 problem is extraction representation.

Observed failure classes:

1. Predicate/paraphrase coverage gaps:
   faithful text often becomes AMBIGUOUS/UNCERTAIN and therefore REVIEW.

2. Missing semantic relations:
   the frozen A2 extractor emits no semantic relation edges.
   Citation binding, procedure order, and equation/symbol relationships therefore cannot be represented decisively after extraction.

3. Quantitative split/merge ownership:
   deterministic anchors survive, but owner-to-value ownership is not always preserved across merged/split structures.

4. Candidate-side extraction is descriptively weaker than source-side extraction on this fixed set:
   GE 41.67% vs EG 50%.

5. Joint extraction introduces additional interaction degradation:
   EE falls to 33.33%.

## Important qualitative failures

Safe pairs:
- B1-P01 -> REVIEW: paraphrase/predicate and citation-evidence extraction uncertainty.
- B1-P02 -> REJECT: split count/seed binding representation mismatch.
- B1-P03 -> REVIEW: `denotes` definition paraphrase not recognized.
- B1-P11 -> REJECT: merged quantitative owner/value binding not preserved.
- B1-P12 -> REVIEW: second explicit non-causality paraphrase not recognized.

Adversarial pairs:
- B1-P05 -> REVIEW instead of REJECT: negated scope change becomes uncertain rather than decisive.
- B1-P06 -> REVIEW instead of REJECT: citation swap loses relation-level representation.
- B1-P07 -> REVIEW instead of REJECT: equation binding change remains ambiguous.

These are conservative failures, not adversarial accepts.

## Interpretation

This result is both positive and negative:

Positive:
- extraction noise did not create a dangerous automatic PASS on any adversarial pair;
- uncertainty was preserved rather than silently promoted;
- B1.1 alignment mechanics remain validated independently.

Negative:
- extracted representations are currently too weak for useful automatic acceptance;
- safe acceptance collapses from 100% to 0%;
- EE pair accuracy loses 66.67 percentage points.

Therefore the current extraction-to-alignment stack is:
`SAFETY-CONSERVATIVE / USABILITY-NOT-READY`

## Research interpretation

Fresh review remains consistent with the result:
- decomposition and verification quality interact; decomposition that is not aligned with verifier needs can strongly degrade downstream performance;
- entity/relation disambiguation is central in complex claim verification;
- graph structure is useful only when semantic relations and ownership are actually represented.

This supports repairing the representation/extraction boundary rather than weakening the aligner or thresholds.

## Cumulative V2.4 success ledger

- V2.3 end-to-end baseline: 37.5% escape / 25% safe acceptance / BOTH_FAIL
- Gate 0: 326/326 PASS
- A1: precision 100% / recall 100% / provenance 35/35
- A2: structural representation 100%; decimal defects 5 -> 0
- A3: coverage 100%; critical coverage 100%; false additions 0%; atomicity 88%; certain precision 92.86%; error-abstention 87.5%; critical silent errors 0
- A4: GO alignment development
- B1 reference: 363/363 PASS
- B1 first aligner: 83.33% FAIL
- B1.1 repaired aligner: 100% on all hard gates
- B2 EE first score: **33.33% pair accuracy / 0% safe acceptance / 0 adversarial acceptance / MIXED_B2_REPAIR_REQUIRED**

## Quality delta

Against B1.1 human-correct baseline:
- EE pair accuracy: 100% -> 33.33% = **-66.67 pp**
- safe acceptance: 100% -> 0% = **-100 pp**
- adversarial acceptance: remains **0%**
- REVIEW preservation: remains **100%**

Classification:
**WORSENED ON EXTRACTED-GRAPH USABILITY / SAFETY PRESERVED**

No end-to-end V2.4 product claim is authorized.

## Completion

First B2 score checkpoint:
**100% COMPLETE**

Gate B2 overall:
**approximately 70% complete**

Whole ACAD_PASS planning estimate:
**approximately 29% ±5%**

## Exact next authorized checkpoint

`AT0-EN V2.4 B2.1 — EXTRACTION/RELATION REPRESENTATION REPAIR DECISION`

This is an architecture/readiness checkpoint before implementation.

It must decide the minimum repair boundary among:
- predicate/paraphrase normalization;
- explicit relation extraction;
- anchor ownership representation;
- split/merge semantic binding;
- candidate-side extraction symmetry;
- timing of authentic academic-text introduction.

Because the first extracted-graph result shows a large 66.67 pp degradation while safety remains conservative, higher-model consultation is justified before changing the representation.

Do NOT repair extractor, bridge, or aligner before that decision is frozen.
