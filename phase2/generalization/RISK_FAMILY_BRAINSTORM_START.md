# Phase 2 — Risk-Family Audit: Brainstorm Start

Date: 2026-09-29

## Hypothesis

Aggregate 90.57% precision may hide heterogeneous families:
- some may be effectively safe under exact agreement;
- others may concentrate wrong/partial edits.

If so, a selective product can auto-apply only validated low-risk families and route the rest to REVIEW.

## Why this is preferable to another global threshold

A global threshold assumes all edit types share the same error mechanism.
Our evidence contradicts that:
- nun changes failed through controller context;
- WAW+ALIF failed through clitic ambiguity;
- lexical/derivational errors remained morphologically valid;
- GED failed to detect semantic wrongness.

## Failure condition

If no pre-registered family with >=10 examples has zero unsafe events, surface family alone is insufficient and we should stop mining the consumed slice for positive acceptance rules.

Then parser/context evidence becomes the next justified step.
