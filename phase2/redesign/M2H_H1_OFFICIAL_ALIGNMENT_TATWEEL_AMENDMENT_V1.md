# H1 Official-Alignment Audit v1 — Tatweel Operational Amendment

Date: 2026-09-30
Status: FROZEN BEFORE RE-RUN
Scope: CALIBRATION only

## Trigger

Run 36709572337 completed the 256-case public inference parity test with 256/256 exact matches, but NoPnx gold construction raised AssertionError on 99/6888 cases.

Forensic inspection established:
- all 99/99 failed cases contain Arabic tatweel U+0640;
- 97/99 contain tatweel in source;
- 15/99 contain tatweel in reference;
- 0 failed cases lack tatweel;
- full-reference reconstruction mismatch count was 0.

The failure is therefore treated as an operational tokenizer/restoration edge case, not H1 scientific underperformance.

## Frozen repair

Do NOT strip tatweel from source or reference, because tatweel removal may itself be a legitimate non-punctuation correction.

Construct the same official word/character alignment once, then derive both:
1. official subword-level edit path;
2. official word-level edit path using SubwordEdits.create(..., tokenizer=None).

For both paths:
- convert insertion-only edits to append edits;
- apply the same frozen punctuation separation logic;
- derive the NoPnx target.

### Cross-validation requirement

For every case where the official subword path succeeds:
- word-level NoPnx target MUST equal subword-level NoPnx target exactly after whitespace normalization.

Required cross-path mismatch count:
**0**

If any mismatch occurs:
- audit stops;
- word-level fallback is invalid.

### Tatweel fallback

Only when:
- subword path raises AssertionError; AND
- source or reference contains U+0640; AND
- global cross-path validation on all subword-success cases has zero mismatches,

the word-level NoPnx target may be used for that case.

No failed case may be silently excluded.

### Required reporting

Report:
- subword-success cases;
- subword AssertionError cases;
- tatweel fallback cases;
- non-tatweel failures;
- word/subword NoPnx mismatches;
- final gold-construction failures.

Headline M2 scoring remains unchanged.

## No scientific changes

Unchanged:
- H1 checkpoint/revision;
- one-pass top-1 mode;
- 80% H1 recall gate;
- M2 scorer settings;
- CALIBRATION population;
- INTERNAL_EVALUATION remains unopened.
