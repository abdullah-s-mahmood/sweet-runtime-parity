# H1 Official-Alignment Audit v1 — Tatweel Char-Alignment Amendment

Date: 2026-09-30
Status: FROZEN BEFORE RE-RUN
Scope: CALIBRATION only

## Root cause established

Targeted diagnostic run 36713242262 showed that representative tatweel failures pass official word-level alignment and fail inside official `char_level_alignment` at its exact surface-reconstruction assertions.

The frozen upstream code calls `norm_pnx_nums()`, whose `remove_kashida()` removes U+0640 before character alignment. The raw surface characters are retained separately, causing reconstruction length/content mismatch when tatweel is present.

QALB treats elongation/kashida as an orthographic error type; therefore stripping tatweel from source/reference before gold construction is forbidden.

## Frozen repair

Create a tatweel-preserving character aligner that is identical to the frozen official character aligner except for one change:

- punctuation normalization: unchanged;
- digit normalization: unchanged;
- weighted alignment and post-processing: unchanged;
- kashida removal: disabled.

Use the frozen upstream `_gen_alignments` and `post_process_alignment(..., is_char_align=True)` unchanged.

## Mandatory cross-validation

For every CALIBRATION case where the original official `char_level_alignment` succeeds, the tatweel-preserving char aligner must produce the exact same character alignment.

Required mismatch count:
**0**

If any mismatch occurs:
- stop the audit;
- do not use the repair.

## Tatweel cases

For a case containing U+0640 in source or reference:
- if official char alignment fails and tatweel-preserving char alignment reconstructs source and target exactly, use the tatweel-preserving alignment;
- build both word-level and subword-level edit paths as previously frozen;
- if subword projection fails because the tokenizer removes tatweel, word-level NoPnx output may be used only under the already-frozen cross-path validation rule.

No case may be dropped.

## Required reporting

Report:
- official char-alignment success count;
- official char-alignment tatweel failures;
- tatweel-preserving alignment success count;
- char-alignment cross-validation mismatches;
- subword projection failures;
- word-level tatweel fallbacks;
- final gold-construction failures.

## Unchanged scientific protocol

No changes to:
- H1 model/revision;
- one-pass top-1 inference;
- CALIBRATION population;
- 80% recall gate;
- M2 settings;
- punctuation separation semantics;
- protected/reserved datasets.
