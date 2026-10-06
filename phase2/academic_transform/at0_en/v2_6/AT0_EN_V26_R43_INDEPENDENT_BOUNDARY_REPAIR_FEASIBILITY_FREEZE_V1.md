# AT0 EN V2.6 — Independent Boundary-Repair Feasibility Result Freeze V1

Date: 2026-10-07
Scope: FIT-only exploratory, non-decision evidence

## Identity

Run: `37539123038`
Conclusion: `success`
Head: `3f6cbe05a56de6dbfb31b5b0d5ca887489b7d952`

Artifact:
- ID `11448196366`
- digest `sha256:f51f6490079bd50218e7e467a7853e5a5391261ce0a5303ced53f4648085da2c`

No Stage-A outputs, SELECT, historical DEV, test, other folds, FactPICO, or consumed 60-RCT holdout were used.

## FIT scope

- documents = 320
- P = 342
- I = 1038
- C = 144
- O = 847

## Local-perturbation repair target audit

Radius: +/-4 words per boundary.

Deduplicated candidate spans:
- total = 105,766
- unique nearest gold target = 101,487 (~95.95%)
- nearest-target tie/ambiguity = 4,279 (~4.05%)

Repair range among all candidates:
- within +/-1 = 16,103 (~15.22%)
- within +/-2 = 41,172 (~38.93%)
- within +/-4 = 100,768 (~95.28%)

This is strong TRAIN-only evidence that local boundary perturbations usually have a clean nearest-gold correction target.

## Composite-span contrast

Composite candidates:
- total = 2,822
- unique nearest target = 2,069 (~73.32%)
- ambiguous nearest target = 753 (~26.68%)

Repairable:
- within +/-1 = 1 (~0.04%)
- within +/-2 = 220 (~7.80%)
- within +/-4 = 615 (~21.79%)

Interpretation:
composite spans are structurally different from local near-boundary errors. Treating them as offset-repair examples would introduce substantially more ambiguity and large-distance targets.

## Prospective implication

If future R4.3 evidence supports a repair branch, the preferred architecture should NOT apply one repair mechanism indiscriminately.

More defensible hybrid hypothesis:

`LOCAL/NEAR-BOUNDARY CANDIDATE -> OFFSET REPAIR`

while

`COMPOSITE/FAR/AMBIGUOUS CANDIDATE -> JOINT CONTEXTUAL PAIR SCORE / REJECT-REVIEW`

This supports a repair-plus-verification hybrid if Stage-B failure decomposition shows complementary error families.

This result is exploratory only and does not modify the frozen H0/H1 Stage-B protocol.
