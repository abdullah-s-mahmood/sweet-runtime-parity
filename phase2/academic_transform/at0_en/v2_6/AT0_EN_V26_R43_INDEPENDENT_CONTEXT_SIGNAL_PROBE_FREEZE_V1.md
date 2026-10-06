# AT0 EN V2.6 — Independent Context-Signal Probe Result Freeze V1

Date: 2026-10-07
Scope: FIT-only exploratory, non-decision evidence

## Identity

Run: `37539134852`
Conclusion: `success`
Head: `bb131195c7972144d9bc3ad5d6d73bdfb60f4553`

Artifact:
- ID `11447393744`
- digest `sha256:ffdfee805e32a500403ef5a1fd1f219f96f799b675a1eaf037f1e1bd5607af76`

No Stage-A outputs, SELECT, historical DEV, test, other folds, FactPICO, or consumed 60-RCT holdout were used.

## Probe design

Used FIT only, split independently inside FIT:
- probe-train documents = 256
- probe-eval documents = 64
- train examples = 6515
- eval examples = 1591

Frozen base BiomedBERT representations were compared with identical simple linear 5-way probes:
- cropped span representation
- contextual representation using start/end/interior/previous/following information

This is exploratory mechanism evidence only, not the scientific Stage-B evaluation.

## All-eval result

Cropped:
- accuracy = 0.7586423755
- macro F1 = 0.5634747631

Contextual:
- accuracy = 0.7730987072
- macro F1 = 0.6414445653

Delta contextual - cropped:
- accuracy = +0.0144563317 (+1.446 pp)
- macro F1 = +0.0779698022 (+7.797 pp)

Per-class F1, cropped -> contextual:
- P: 0.458333 -> 0.736842
- I: 0.584071 -> 0.624490
- C: 0.448276 -> 0.352941
- O: 0.468531 -> 0.639769
- NONE: 0.858162 -> 0.853180

Per-class precision, cropped -> contextual:
- P: 0.440000 -> 0.674699
- I: 0.545455 -> 0.546429
- C: 0.565217 -> 0.268657
- O: 0.496296 -> 0.566327
- NONE: 0.862007 -> 0.924352

Critical interpretation:
context provides substantial discriminative information overall and strongly helps P/O and recall for I. However, simple contextual linear probing materially worsens C precision. Therefore context is useful but not sufficient evidence that an unrestricted contextual classifier will satisfy the four-class precision gate.

## Ambiguous-surface subset

Probe-eval ambiguous-surface subset:
- n = 14

Cropped:
- accuracy = 0.642857
- macro F1 = 0.386667
- NONE recall = 0

Contextual:
- accuracy = 0.928571
- macro F1 = 0.577778
- NONE precision = 1.0
- NONE recall = 0.8
- C/I were perfectly classified within this very small subset

Delta macro F1:
+0.191111 (+19.111 pp)

Interpretation:
this small targeted subset strongly supports the missing-context hypothesis, particularly the inability of cropped content to distinguish entity from NONE when surface forms repeat across contexts.

Because n=14, this subset must not be treated as a performance estimate.

## Decision consequence

Evidence supports continuing the already-frozen H0/H1 contextual Stage-B experiment.

It does NOT:
- authorize altering Stage B;
- establish H0 or H1 will pass the frozen gate;
- justify class-specific thresholds;
- justify ignoring the C precision risk.

The C result is a prespecified risk to inspect carefully in Stage B.

This probe is exploratory only and does not modify the frozen Stage-B protocol.
