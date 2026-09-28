# Midphase brainstorm after adjudication

Decision labels are hypotheses for the next bounded experiments, not architecture changes or a freeze.

## NoPnx iteration 1 only — PROTOTYPE

Same 29 exact target states as iteration 2, avoids documented ITEM-077 regression; still faces rendering loss.

## NoPnx ×2 — WATCH

One additional exact recovery (ITEM-467) and one regression (ITEM-077); blanket second pass lacks observed net target gain.

## Selective second iteration — TEST

Trigger only where first output has a relevant unresolved target and no unknown-token hazard; record tradeoff.

## Pnx only when punctuation explicitly required — PROTOTYPE

Pnx changes 25 passages after NoPnx and gives no additional exact target; route by requested task and review punctuation.

## Confidence-based abstention — PROTOTYPE

Use tag confidence and rendering/lexical-loss invariants to abstain; current top-1 confidence is not calibrated correctness.

## Target/error-type routing — TEST

Orthographic hamza and agreement differ; route after cluster-aware error-type evidence rather than guessed thresholds.

## Scientific protected-span routing — PROTOTYPE

Numbers, terms, negation, citations, names require explicit preservation in scientific text; not measured here.

## Source-preserving surgical edit application — PROTOTYPE

Urgent because [UNK] and fragments often appear without a supporting edit. Build only after this gate, per user instruction.

## Candidate generation + safety filter + quality ranker — TEST

Allow alternatives while rejecting lexical loss; independent filter must inspect whole resulting passage.

## Alternative Arabic GEC models — TEST

Compare AraT5/AraBART-family candidates only after defining matched inputs and output-preservation controls.

## Error classes bypassing SWEET — PROTOTYPE

Deterministic punctuation spacing and protected-term handling can avoid unknown-token rewrite; difficult syntax can escalate.

## Challenge to current pipeline

The immediate bottleneck in these inputs is destructive unknown-token rendering and collateral lexical deletion. A higher local recovery count is insufficient if the output damages passages. First make edit attribution and source preservation testable; then compare candidate pipelines on the same 41 clusters and separate scientific stress invariants. No SWEET weights, safety stack or benchmark changed.
