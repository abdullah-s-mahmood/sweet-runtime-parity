# M2-R v2 — Start Brainstorming

Date: 2026-09-30

## Candidate evidence designs

### ArabiGEE-only full sentence gate
REJECTED by v1.1.
Annotations are selective.

### QALB corrected sentence only
Useful for clean false positives, but insufficient to measure residual recall without edit spans.

### QALB source + corrected reference + verified M2
SELECTED.
It supplies:
- fully corrected clean sentence;
- full source error context;
- executable edit script on reconstructable lines;
- controlled all-but-one residuals.

## Detectable gold policy

The residual hunter must quote an exact surface present in the candidate. Therefore v2's primary localization gold excludes edits with no source surface (pure insertions) and excludes punctuation-only source surfaces.

A reference edit is primary-detectable when:
- source span is nonempty;
- the source surface contains at least one Arabic letter or digit;
- the edit is part of an M2 block that fully reconstructs the human corrected line.

Punctuation-only edits are retained in provenance but not primary recall.

## Controlled strict residual

For near-complete testing, select one edit that is:
- one source token;
- replacement is one nonempty token;
- both source and replacement contain Arabic letters;
- no whitespace inside either;
- not identical after normalization.

Apply every other M2 edit and withhold this one.
Require the withheld source surface to remain present in the candidate.

This includes high-value spelling/inflection errors without fabricating random corruption.

## Why not classify every edit now

ARETA is highly useful but not perfect (reported 85.8% micro-F1 on a blind ALC portion). First prove localization. Then use ARETA/ArabiGEE to stratify failures.
