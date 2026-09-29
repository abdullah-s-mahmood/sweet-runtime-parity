# M2-R — Adversarial Brainstorming Before Data Feasibility

Date: 2026-09-30

## Alternatives considered

### 1. P2 of the monolithic verifier
REJECT.
Explicitly prohibited and scientifically weak after the observed safety–coverage instability.

### 2. Add deterministic Hamza correction and declare success
REJECT AS GENERAL SOLUTION.
Hamza caught three observed misses, but patching only the last failure sample would be post-hoc overfitting.

### 3. Multi-agent judge panel
DEFER.
It adds correlated complexity before we know whether the core missing capability—residual localization—can be measured reliably.

### 4. Residual binary classifier
INSUFFICIENT.
A binary “error remains” decision is not auditable and repeats the sentence-level opacity problem.

### 5. Residual span hunter
SELECTED.
For every remaining mandatory error, return the exact erroneous surface, minimal replacement, error dimension and confidence. If no mandatory error exists, return an empty list.

## Why ArabiGEE is high-value

It gives direct human-annotated pairs of erroneous and target words/phrases plus structured explanation dimensions. This allows:
- localization scoring independent of exact correction wording;
- error-type breakdown;
- clean target contexts for false-positive measurement;
- multi-error contexts for controlled near-complete candidates.

## Mandatory vs optional policy

Primary M2-R excludes punctuation by using `contexts_nopnx`.

Within non-punctuation data:
- orthographic, morphological, syntactic and lexical annotated corrections are treated as expert-supported mandatory reference errors for the feasibility task;
- non-reference alternatives remain possible, so exact replacement match is secondary to localization;
- dialect/register normalization must be flagged for separate audit when the explanation indicates register/lexical variation.

## Near-complete construction

For contexts with >=2 independently annotated error pairs:
1. start from erroneous context;
2. apply all expert corrections except one;
3. require each replacement to map uniquely/unambiguously in the context;
4. verify that applying all corrections reconstructs the target context after normalization;
5. persist only hashes/metadata, not raw Arabic text.

This creates a candidate with one withheld expert-supported residual error and mirrors the failure mode that broke P1.

## Clean controls

Use the expert target context unchanged.
The residual hunter should return zero mandatory errors.

## What would falsify M2-R

A useful residual hunter must not merely flag everything:
- high residual recall with high clean false positives is not success;
- high clean precision with low recall repeats P0;
- large class-specific blind spots, especially simple orthography, fail the safety objective.
