# Phase 2 — Dependency/Governor Feature Diagnostic Protocol

Date: 2026-09-29
Status: PRE-REGISTERED FEATURE DIAGNOSTIC ON CONSUMED FRESH-V1 PASS EVENTS

## Purpose

Test whether Arabic dependency/governor structure contains a useful contextual-completeness signal for the two partial corrections that passed ORTHO_ISOLATED_COMMON_NOUN_V1.

This is hypothesis-generation on consumed evidence only. No acceptance rule, threshold, whitelist, or promotion decision is defined before the features are materialized.

## Population

Exactly the 14 frozen PASS events from canonical fresh ORTHO validation run 36520233398.

The population is already consumed:
- 8 exact-gold supported;
- 6 previously bounded-review events.
Labels MUST NOT be read by the feature materializer.

## Parser

- CAMeL-Lab/camel_parser
- pinned commit: 66f29f7e34e3b5b38780d08bd56cf481635bf1c6
- CATiB model
- preprocessed_text mode
- Python 3.11.13

The mapping smoke established:
- tokenized mode preserves whitespace input 1:1;
- preprocessed_text produces clitic-aware extra parser tokens;
- therefore this diagnostic uses preprocessed_text plus an explicit deterministic whitespace-word -> parser-token span map.

## Deterministic mapping

For each source/candidate sentence:
1. split into whitespace words;
2. run the same CAMeL BERT disambiguator used by CamelParser;
3. use CamelParser feature extraction to determine the exact parser-token sequence emitted per whitespace word;
4. accumulate parser-token spans per whitespace word;
5. parse the same sentence with preprocessed_text;
6. assert the reconstructed parser-token sequence exactly matches the parser input forms after the same normalization.

If the assertion fails, the event is not interpretable and the diagnostic must fail rather than guess alignment.

## Candidate construction

For each frozen V1 PASS event:
- recover the exact candidate surface from the frozen AraBART voter artifact from run 36520233398;
- replace only the target whitespace word;
- do not apply gold or manual repairs;
- parse source and candidate independently.

## Label-free dependency features

Persist only non-text categories, booleans, counts and hashes:
- target parser-token count;
- baseword-anchor count and mapping reliability;
- target anchor CATiB POS;
- target dependency relation;
- head kind (ROOT / TARGET / EXTERNAL);
- external head POS and dependency relation;
- head direction/distance bucket;
- immediate external dependent relation multiset;
- previous/next whitespace-word anchor POS and relation;
- hashes of target/head forms;
- source-to-candidate change flags for all above;
- structural fingerprint hash.

No Arabic source/candidate text or raw forms may be persisted.

## Anti-leakage order

1. Download frozen V1 features and voter artifacts.
2. Download QALB15 TRAIN RAW only.
3. Materialize and hash dependency features.
4. Run leakage audit.
5. Only after feature freeze may the existing manual-review labels be read for descriptive evaluation.
6. Do not tune a rule on these 14 events.

## Interpretation

This diagnostic may:
- falsify dependency change as useful;
- identify candidate structural features for a later pre-registered rule;
- justify a separate consumed-slice replication.

It cannot authorize fresh validation or production promotion by itself.

QALB15 TEST remains unread. No sealed benchmark. No Phase 3.
