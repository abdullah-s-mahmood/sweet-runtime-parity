# M2-R v2 — Final Forensic Analysis: P1 versus P0

Date: 2026-09-30
Status: FINAL FORENSIC ANALYSIS BEFORE M2-R CLOSURE

This analysis was recomputed directly from the frozen P0/P1 blind packets, gold keys, and committed prediction outputs.

No Confirmation, Holdout, or A7'ta reserve was opened.

## Comparable design

P0 and P1 both use:
- QALB14 complete human corrections;
- DEVELOPMENT only;
- 120 cases each;
- 60 NATURAL_QALB_SOURCE;
- 30 CLEAN_QALB_REFERENCE;
- 30 QALB_ALL_BUT_ONE_STRICT.

P1 is fully disjoint from P0: overlap = 0.

Therefore aggregate P0/P1 comparison is materially more interpretable than the earlier ArabiGEE-to-QALB comparison.

## Primary metric change

| Metric | P0 | P1 | Change |
|---|---:|---:|---:|
| CRR | 82.22% | 86.67% | +4.44 pp |
| GELR | 29.14% | 48.88% | +19.74 pp |
| CFPR | 60.00% | 33.33% | -26.67 pp |
| Strict residual recall | 63.33% | 76.67% | +13.33 pp |
| Claim precision | 63.47% | 65.50% | +2.03 pp |
| Invalid-surface rate | 0% | 0% | unchanged |

P1 passes:
- CRR >=85%;
- invalid-surface rate <=2%.

P1 still fails:
- GELR >=80%;
- CFPR <=5%;
- strict residual recall >=90%.

## Natural sentence completeness

P0 NATURAL_QALB_SOURCE:
- complete: 3/60 = 5.00%;
- some but incomplete: 52/60 = 86.67%;
- zero gold edits found: 5/60 = 8.33%;
- gold edits: 447;
- gold hits: 120;
- verifier claims: 159.

P1 NATURAL_QALB_SOURCE:
- complete: 4/60 = 6.67%;
- some but incomplete: 51/60 = 85.00%;
- zero gold edits found: 5/60 = 8.33%;
- gold edits: 506;
- gold hits: 239;
- verifier claims: 337.

Interpretation:
P1 nearly doubled the number of matched natural edits (120 -> 239), but complete-sentence coverage improved only one case (3 -> 4).

This is the central M2-R result:
**better edit discovery did not become reliable proof of sentence completeness.**

## Gold operation recall

P0:
- Edit: 129/409 = 31.54%
- Split: 7/31 = 22.58%
- Merge: 3/30 = 10.00%
- Delete: 0/5 = 0%
- Move: 0/1 = 0%

P1:
- Edit: 252/436 = 57.80%
- Split: 7/14 = 50.00%
- Merge: 2/83 = 2.41%
- Delete: 0/1 = 0%
- Other: 1/2 = 50.00%

The denominators differ because P0 and P1 are disjoint samples; operation-specific deltas are therefore descriptive rather than causal estimates.

Still, two conclusions are robust:
1. ordinary Edit detection improved strongly;
2. structural operations, especially Merge/Delete, remain a major weakness.

## Clean false positives

P0:
- false-positive clean cases: 18/30 = 60.00%;
- false-positive claims: 24.

P1:
- false-positive clean cases: 10/30 = 33.33%;
- false-positive claims: 16.

Verifier-assigned false-positive dimensions:
P0:
- ORTHOGRAPHY 11
- MORPHOLOGY 8
- SYNTAX 4
- LEXICAL 1

P1:
- ORTHOGRAPHY 4
- MORPHOLOGY 5
- SYNTAX 5
- OTHER 2
- LEXICAL 0

All 16 P1 clean false-positive claims were marked HIGH confidence.

Thus the two-pass mandatory/optional/uncertain decomposition substantially reduced over-assertion, but model self-confidence remains uncalibrated.

## Claim behavior within error-containing contexts

P0 matched claims by verifier-assigned dimension:
- ORTHOGRAPHY 135
- MORPHOLOGY 3
- LEXICAL 1
- SYNTAX 0

P1:
- ORTHOGRAPHY 244
- OTHER 11
- MORPHOLOGY 3
- LEXICAL 4
- SYNTAX 0

P1 unmatched claims in error-containing contexts:
- ORTHOGRAPHY 73
- MORPHOLOGY 21
- SYNTAX 14
- LEXICAL 7
- OTHER 7

The residual hunter remains heavily orthography-dominant and does not demonstrate reliable syntax-level verification.

## What improved

**IMPROVED materially**
- CRR passed its development gate.
- GELR improved by +19.74 pp.
- CFPR improved by -26.67 pp.
- strict residual recall improved by +13.33 pp.
- ordinary Edit and Split discovery improved substantially.
- clean false-positive cases dropped from 18 to 10.

## What did not improve enough

**Still unacceptable**
- CFPR remains 33.33%, versus <=5%.
- GELR remains 48.88%, versus >=80%.
- strict residual recall remains 76.67%, versus >=90%.
- complete natural-sentence coverage is only 4/60 = 6.67%.
- Merge detection is 2/83 = 2.41% on P1.
- Delete remains 0%.
- syntax-tagged exact hits remain 0.
- HIGH confidence remains poorly calibrated.

## Scientific interpretation

The single structural P1 revision succeeded in proving that task decomposition helps:
broad candidate enumeration followed by independent mandatory-error adjudication improved both recall and false-positive suppression simultaneously.

However, the experiment falsifies the stronger hypothesis that a general LLM residual hunter can serve as a standalone sentence-completeness oracle under the current development requirements.

The supported conclusion is narrower:
**structured LLM reasoning is useful as one residual-risk signal, not as final proof that no mandatory error remains.**
