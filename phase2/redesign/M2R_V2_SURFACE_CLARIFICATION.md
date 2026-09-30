# M2-R v2 — Surface-Localization Technical Clarification

Date: 2026-09-30
Status: FROZEN BEFORE PACKET MATERIALIZATION

The P0 verifier returns exact text surfaces, not character/token offsets.

Therefore packet construction must avoid ambiguous gold:
- every primary gold surface in a NATURAL_QALB_SOURCE case must occur exactly once in that candidate;
- the withheld strict surface in QALB_ALL_BUT_ONE_STRICT must occur exactly once in the resulting candidate;
- a withheld edit whose source span overlaps another M2 edit is ineligible.

This does not alter thresholds, family sizes, data partitions, or allowed sources. It only makes exact-surface localization objectively scoreable.
