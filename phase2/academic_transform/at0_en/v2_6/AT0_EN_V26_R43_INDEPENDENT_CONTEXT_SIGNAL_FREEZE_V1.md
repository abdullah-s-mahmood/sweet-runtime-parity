# AT0 EN V2.6 — Independent Context Signal Probe Result Freeze V1

Date: 2026-10-07
Scope: FIT-only exploratory, non-decision evidence

## Identity
Run: `37539134852`
Conclusion: `success`
Artifact: `11447393744`
Digest: `sha256:ffdfee805e32a500403ef5a1fd1f219f96f799b675a1eaf037f1e1bd5607af76`

No Stage-A outputs, SELECT, historical DEV, test, other folds, FactPICO, or consumed 60-RCT holdout were used.

## Probe split
- train documents = 256
- eval documents = 64
- train examples = 6515
- eval examples = 1591
- ambiguous-surface eval examples = 14

## Cropped surface probe
All eval:
- accuracy = 0.7586423755
- macro-F1 = 0.5634747631

Ambiguous-surface subset:
- accuracy = 0.6428571343
- macro-F1 = 0.3866666667

## Contextual full-sentence probe
All eval:
- accuracy = 0.7730987072
- macro-F1 = 0.6414445653

Ambiguous-surface subset:
- accuracy = 0.9285714030
- macro-F1 = 0.5777777778

## Delta: contextual minus cropped
- accuracy = +0.0144563317
- macro-F1 = +0.0779698022
- ambiguous-subset macro-F1 = +0.1911111111

## Interpretation
This is direct FIT-only evidence that full-sentence contextual representation carries materially more useful discrimination than cropped span content, especially for input surfaces that are label-ambiguous across contexts.

It supports the missing-context hypothesis behind R4.3 H0/H1.

It does NOT prove that H1 biaffine interaction is necessary; that remains the purpose of the frozen Stage-B comparison.

This result is exploratory only and does not modify the frozen Stage-B protocol.
