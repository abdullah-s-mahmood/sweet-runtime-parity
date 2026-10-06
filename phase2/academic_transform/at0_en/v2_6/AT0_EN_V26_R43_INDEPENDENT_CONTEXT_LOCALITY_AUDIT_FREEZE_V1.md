# AT0 EN V2.6 — Independent Context-Locality Audit Result Freeze V1

Date: 2026-10-07
Scope: FIT-only exploratory, non-decision evidence

## Identity

Run: `37539816534`
Conclusion: `success`
Head: `9342566ab0f49c50359e04d4e4ca11ef9690fff9`

Artifact:
- ID `11448172538`
- digest `sha256:f1a69ebce503b40bf598e4abeb4ec334098207a8684e37c52556568bfc1aa29a`

No Stage-A outputs, SELECT, historical DEV, test, other folds, FactPICO, or consumed 60-RCT holdout were used.

## FIT construction

- documents = 320
- total examples after gold precedence = 8071
- labels include NONE/P/I/C/O under the exploratory local/composite/background construction

## Surface-only ambiguity

Surface-only keys:
- conflicting keys = 42
- conflict rate = 0.0058059165 (~0.581%)

These conflicts include:
- entity versus NONE ambiguity;
- PICO class ambiguity such as I versus C or I versus O.

## Local context resolution

With +/-1 token of outside context:
- unique contextual keys = 7991
- conflicts = 2
- conflict rate = 0.0002502816 (~0.0250%)

With +/-2 tokens:
- unique contextual keys = 8054
- conflicts = 1
- conflict rate = 0.0001241619 (~0.0124%)

With +/-4 tokens:
- unique contextual keys = 8069
- conflicts = 0

Full sentence + candidate coordinates:
- unique keys = 8071
- conflicts = 0

The two +/-1 conflicts are C/I cases. One remains at +/-2 and disappears by +/-4.

## Interpretation

In this FIT-only construction, almost all label ambiguity visible from cropped span text disappears with even a small amount of surrounding context, and all observed collisions disappear by +/-4 tokens.

This independently strengthens the missing-context hypothesis.

Because Stage-B H0/H1 use contextual representations generated from the complete sentence, their input representation has access to at least the contextual information that resolves these deterministic surface collisions in principle.

This does NOT prove a learned classifier will achieve the frozen gate. It only shows the conflicting labels are not generally irreducible once context is included.

## Governance

Exploratory only. This result does not alter the frozen H0/H1 Stage-B protocol, thresholds, gate, split, or model-selection rule.
