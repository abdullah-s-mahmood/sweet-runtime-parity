# MP-SEF P2 REPAIRABILITY ASSESSMENT V1

Date: 2026-10-01
Status: SOURCE-ONLY ROOT-CAUSE AND REPAIRABILITY RECORD

## Current frozen result

Frozen P2 proposal SHA256:
`f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

Population:
- 1,918 cases
- GED word-label count mismatch: 1,918 / 1,918
- exact word-label count matches: 0 / 1,918
- total excess/dropped GED predictions under frozen zip semantics: 30,341
- minimum excess: 2
- maximum excess: 87
- median excess: 15
- mean excess: 15.8191
- frozen-output reproduction: 1,918 / 1,918 exact
- generation ceiling cases: 24
- missing terminal EOS cases: 0

Current legalizer outcome:
- P2_EXECUTION_FAILED = 1,918

No gold/reference content or R_joint was used to establish this defect.

## Root cause

The frozen runner takes GED predictions after stripping only model special tokens:

`preds = ...[1:-1]`

These are subword-level positions.

It then consumes them as though they were one label per morphology word:

`for word, label in zip(morph.split(), ged_labels)`

When a source word is split into multiple BERT wordpieces, GED labels cease to be aligned one-to-one with morphology words. The Python zip then silently truncates the longer GED list.

The official Arabic-GEC ErrorIdentifier implementation demonstrates the appropriate word-level pattern:
- tokenize each source word into wordpieces;
- keep the real GED supervision/prediction position for the first wordpiece;
- mark remaining wordpieces with ignore index;
- align predictions back only through retained word-level positions.

Therefore the defect is implementation/provenance alignment, not evidence that the model itself has poor linguistic quality.

## Root-cause confidence

Engineering confidence that the observed failure mechanism is correctly identified:

HIGH.

The failure is:
- universal in the frozen population;
- reproducible;
- quantitatively measured;
- consistent with subword expansion;
- consistent with the robust word-level alignment implementation in the same upstream project;
- independent of gold/reference quality.

## Repairability

Primary class:

`FIXABLE_NEXT_VERSION_ONLY`

The alignment defect itself is technically repairable with high confidence.

A corrected P2 implementation should:
1. derive one GED prediction per source/morphology word using explicit first-wordpiece alignment;
2. prohibit silent zip truncation;
3. assert exact word coverage;
4. record wordpiece-to-word mapping;
5. fail closed on any unaligned word;
6. record GED/GEC input lengths and truncation metadata;
7. preserve decoder start/EOS/PAD/max_length evidence;
8. include regression tests for split-word cases and exact coverage.

## Why not repair P2 in the current frozen cycle

The current P2 proposals are already frozen and have been used as immutable inputs to the source-only legalizer.

Replacing them with corrected outputs would create a new candidate set after the defect was discovered and after the current cycle was frozen.

Therefore:
- the current P2 artifact remains non-executable;
- it MUST NOT be silently repaired, regenerated, or partially salvaged;
- the corrected P2 must receive a new explicit version/cycle and new hashes.

This protects the scientific provenance of the current cycle.

## What can be repaired now

Allowed now:
- improve diagnostics;
- add synthetic regression tests;
- specify the corrected alignment algorithm;
- build a source-only P2-v2 implementation in a separate versioned path;
- independently review that implementation before any new measurement.

Not allowed now:
- overwrite frozen P2 outputs;
- selectively keep only cases with smaller mismatch;
- use gold to decide which P2 outputs to retain;
- reinterpret EXECUTION_FAILED as linguistic failure;
- lower the legalizer gate.

## Expected repair outcome

The specific GED word-alignment defect is considered highly repairable at the implementation level.

This does NOT imply:
- repaired P2 will have high linguistic accuracy;
- repaired P2 will improve R_joint;
- repaired P2 will pass the 95% candidate-availability gate.

Those are separate scientific questions requiring a new authorized versioned evaluation.

## Recommendation

Continue the current cycle with P2 blocked so that Second Preflight remains scientifically clean.

In parallel only at the design/specification level, prepare `P2_V2` as the next-version repair path.

Do not execute a new gold-aware P2 evaluation until the current Second Preflight decision and version-boundary rules are complete.
