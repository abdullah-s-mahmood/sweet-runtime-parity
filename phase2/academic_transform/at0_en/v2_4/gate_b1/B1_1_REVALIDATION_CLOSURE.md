# AT0-EN V2.4 — Gate B1.1 Repair and Revalidation Closure

Date: 2026-10-03
Status: CLOSED / PASS_B1_HUMAN_CORRECT / B1 COMPLETE

## Final result

Run:
`37146333162`

Artifact:
- id: `11282215627`
- SHA-256: `cae7f304bf6ff6ac78b6dacd6c624be1a14fc74221032e2d59ee217b768c73ea`

Result:
`PASS_B1_HUMAN_CORRECT`

Hard gates:
- pair outcomes: 12/12 = 100%
- critical alignment coverage: 22/22 = 100%
- critical alignment-status accuracy: 100%
- dangerous false-preserve: 0
- faithful false rejection: 0
- material adversarial acceptance: 0
- critical uncertainty preservation: 100%
- critical evidence-trace completeness: 100%

Mapping shapes:
- 1:1 = 7/7
- 1:N = 2/2
- N:1 = 2/2
- mixed = 1/1

Repair regressions:
- 3/3 PASS

## Improvement from first B1 score

- pair outcome accuracy: 83.33% -> 100% = **+16.67 pp**
- critical coverage: 90.91% -> 100% = **+9.09 pp**
- critical status accuracy: 95% -> 100% = **+5 pp**
- material adversarial acceptance: 1 -> 0
- faithful false rejection: 1 -> 0

No threshold or gold reference was changed.

## Repairs

General, non-ID-specific repairs:
1. owner/entity-first matching;
2. canonical owner-value/meaning binding facts;
3. symbolic-key normalization;
4. scalar+unit canonicalization;
5. coordinated-owner normalization such as `Groups X and Y`.

## Preserved negative evidence

First B1 score remains frozen:
- run `37145678669`
- result: 83.33% / FAIL

First B1.1 regression attempt also remains negative evidence:
- run `37146262703`
- failed before B1 scoring because coordinated group owners were not normalized correctly.

No result was overwritten.

## Research interpretation

Current literature supports the repair direction:
- entity and relation alignment should be treated jointly, not as text similarity alone;
- precise evidence/subclaim alignment is a known bottleneck;
- conservative uncertainty handling reduces downstream error propagation.

Passing B1 proves only alignment mechanics on 12 human-correct development graph pairs.
It does NOT establish:
- extracted-graph alignment quality;
- candidate-side extraction quality;
- authentic-document validity;
- end-to-end V2.4 safety;
- production readiness.

## Cumulative V2.4 success ledger

- V2.3 end-to-end baseline: 37.5% escape / 25% safe acceptance / BOTH_FAIL
- Gate 0: 326/326 contract checks PASS
- A1: precision 100%, recall 100%, provenance 35/35
- A2: structural representation 100%; known decimal defects 5 -> 0
- A3: coverage 100%, critical coverage 100%, false additions 0%, atomicity 88%, certain precision 92.86%, error-abstention 87.5%, critical silent errors 0
- A4: GO_ALIGNMENT_RESEARCH_DEVELOPMENT_ONLY
- B1 reference: 363/363 PASS
- B1 first aligner: 83.33% FAIL
- B1.1 repaired aligner: **100% PASS on all B1 hard gates**

## Completion

B1.1:
**100% COMPLETE**

Gate B1:
**100% COMPLETE**

Whole ACAD_PASS planning estimate:
**approximately 28% ±5%**

## Exact next authorized stage

`AT0-EN V2.4 GATE B2 — EXTRACTED-GRAPH ALIGNMENT DEGRADATION TEST`

Purpose:
measure how much alignment performance degrades when human-correct graphs are replaced by graphs produced by the source/candidate extraction pipeline.

Initial B2 must keep gold-graph B1 results separate from extracted-graph results.

Not authorized:
- live generation
- HW1-EN
- untouched holdout
- production claims
- authentic integrated system claims before a diagnosable extracted-graph stage exists

Higher-model consultation is not required at B2 start unless a new construct-validity issue appears.
