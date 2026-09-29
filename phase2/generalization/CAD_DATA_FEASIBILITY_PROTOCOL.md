# Phase 2 — CAD-Inspired QALB14 Data Feasibility Probe

Date: 2026-09-29
Status: PRE-REGISTERED BEFORE QALB14 COUNTS ARE MATERIALIZED

## Purpose

Determine whether QALB14 contains enough externally grounded examples to train a leakage-free local repair-completeness discriminator before implementing any model.

## Source

Pinned repository:
CAMeL-Lab/arabic-gec @ 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

Files:
- QALB-2014-L1-Train.sent.no_ids
- QALB-2014-L1-Train.cor.no_ids
- QALB-2014-L1-Dev.sent.no_ids
- QALB-2014-L1-Dev.cor.no_ids

No QALB15 corrected data is read.
No current Phase-2 adjudication labels are read.

## Gold edit derivation

Whitespace-token source/gold alignment uses Python difflib.SequenceMatcher with autojunk=false.

Eligible target edits are one-source-token -> one-gold-token replacements.

Approved narrow orthographic equivalence:
- Arabic alif/hamza group: ا أ إ آ ٱ
- final ya/alif-maqsura group: ي ى only at final character
- final ha/ta-marbuta group: ه ة only at final character

## Example classes

POS_ISOLATED_ORTHO:
- source->gold target replacement differs only through approved orthographic equivalence;
- no other gold edit locus lies within +/-2 source-token positions of the target.

NEG_NEARBY_RESIDUAL:
- target replacement itself is approved orthographic-only;
- at least one additional gold edit locus lies within +/-2 source-token positions;
- candidate would apply only the target edit and leave the nearby repair unresolved.

NEG_ORTHO_SUBEDIT:
- source and gold target tokens have equal character length;
- at least one differing character pair is approved orthographic equivalence;
- at least one other differing character pair is non-orthographic;
- candidate is formed by applying only approved orthographic character changes toward gold;
- candidate differs from both source and gold.

## Feasibility criterion

Proceed to model training only if:
- QALB14 train POS_ISOLATED_ORTHO >= 500;
- combined train negatives >= 500;
- QALB14 dev POS_ISOLATED_ORTHO >= 50;
- combined dev negatives >= 50.

No class balancing or threshold decisions are made until counts are frozen.

## Persistence

Persist counts, source file hashes, deterministic rule version, and example-ID hashes only.
Do not persist licensed Arabic text.

No Phase 3.
No QALB15 TEST.
