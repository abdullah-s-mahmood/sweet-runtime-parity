# AT0 EN V2.6 — Independent Context Locality Audit Result Freeze V1

Date: 2026-10-07
Scope: FIT-only exploratory, non-decision evidence

## Identity
Run: `37539816534`
Conclusion: `success`
Artifact: `11448172538`
Digest: `sha256:f1a69ebce503b40bf598e4abeb4ec334098207a8684e37c52556568bfc1aa29a`

No Stage-A outputs, SELECT, historical DEV, test, other folds, FactPICO, or consumed 60-RCT holdout were used.

## Scope
- FIT documents = 320
- examples = 8071

## Representation conflict counts

Cropped surface only:
- conflicting keys = 42
- conflict rate = 0.0058059165

Context +/-1 word:
- conflicting keys = 2
- conflict rate = 0.0002502816

Context +/-2 words:
- conflicting keys = 1
- conflict rate = 0.0001241619

Context +/-4 words:
- conflicting keys = 0
- conflict rate = 0.0

Full sentence + coordinates:
- conflicting keys = 0
- conflict rate = 0.0

## Interpretation
Most label ambiguity induced by cropped span content disappears with only a small amount of surrounding context.

In this FIT-only construction:
- one-word context removes 40/42 surface conflicts;
- two-word context removes 41/42;
- four-word context removes all 42.

This strongly supports preserving local/full sentence context in future exact-span verification architectures.

It does not establish that a +/-4 lexical window is itself the optimal model input; R4.3 correctly uses contextualized full-sentence representations rather than hard-coding a four-word window.

This result is exploratory only and does not modify the frozen Stage-B protocol.
