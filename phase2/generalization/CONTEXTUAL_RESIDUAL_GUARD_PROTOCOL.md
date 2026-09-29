# Phase 2 — Contextual Residual-Risk Guard Diagnostic

Date: 2026-09-29
Status: PRE-REGISTERED DIAGNOSTIC ON CONSUMED TRI-MODEL SLICE

## Motivation

UNANIMOUS_3 failed its promotion contract on a fresh disjoint QALB15 TRAIN slice:
- 142 accepted events;
- 126 supported / supported alternative;
- 12 partial;
- 4 wrong.

The unsafe taxonomy is dominated by context-governed residuals: valency, tense/aspect, clitics, prepositions, complementizers, numerals, determiner/gender/number agreement, lexical semantics, and proper-name transliteration.

This gate does NOT add another generator. It tests whether an interpretable contextual veto can carve a narrow high-precision lane from exact three-model agreement.

## Evidence reuse

Reuse frozen artifacts from canonical successful run:
- workflow run 36517205396
- trimodel-sweet-q14
- trimodel-sweet-zaebuc
- trimodel-arabart-q14

No model inference is rerun.

QALB15 TRAIN raw text is read ephemerally only for contextual morphology.
Gold and manual labels are unavailable until runtime decisions are frozen.

## Runtime analyzer

CAMeL Tools BERT unfactored MSA disambiguator.

For source and candidate sentences, inspect the changed token's top contextual analysis only.

Persist no Arabic text and no lexical analysis strings. Persist only:
- hashes / IDs;
- character-edit family;
- source/candidate POS tags;
- booleans for analysis availability;
- booleans for lemma identity;
- booleans for selected morph/clitic-feature identity;
- neighboring-edit risk;
- runtime decision.

## Frozen edit families

SAFE_SURFACE_FAMILY is true only for a single-character, equal-length substitution in one of:
- Arabic alif/hamza set: ا أ إ آ
- final alif-maqsura / ya: ى ي
- final ha / ta-marbuta: ه ة

All insertions, deletions, multi-character substitutions, and other character classes are REVIEW.

## Context/morph identity

Required unchanged features when analyses exist:
- POS
- person
- gender
- number
- aspect
- mood
- voice
- state/definiteness
- proclitics prc0..prc3
- enclitic enc0

Lemma identity is required after analyzer-provided lexical normalization.
If either analysis is missing or backoff/no-analysis, REVIEW.

## Neighborhood isolation

For the candidate source token, REVIEW if ANY of the three voters proposes any other non-KEEP event whose source span lies within ±2 lexical tokens.

This is independent runtime evidence; gold is not used.

## Frozen policies

### ORTHO_ISOLATED_COMMON_NOUN_V1 — primary
PASS only when ALL hold:
1. candidate is already UNANIMOUS_3;
2. SAFE_SURFACE_FAMILY;
3. source and candidate contextual analyses are reliable;
4. source POS == candidate POS == noun;
5. lemma identity;
6. selected morphology/clitics identical;
7. no neighboring edit within ±2 from any voter.

Otherwise REVIEW.

### ORTHO_MORPH_COMMON_NOUN_V1 — diagnostic
Same as primary but without the neighboring-edit isolation requirement.

### ORTHO_ISOLATED_NOUN_ADV_V1 — diagnostic
Same as primary but candidate/source POS may be noun or adv.

No threshold or rule tuning is allowed after labels are opened.

## Evaluation

After runtime output is hashed/frozen:
- 94 exact-gold UNANIMOUS_3 events count as supported;
- the 48 non-exact events use the already persisted same-agent contextual adjudication;
- report PASS count, supported PASS, partial PASS, wrong PASS, unnecessary PASS, precision, and review burden.

## Diagnostic advancement criterion

A policy is eligible for an unchanged fresh disjoint validation only if:
- PASS >= 10;
- wrong PASS = 0;
- partial PASS = 0;
- unnecessary PASS = 0.

Because this rule was designed after inspecting the prior failure taxonomy, success here is NOT generalization evidence.

## Constraints

- No QALB15 TEST.
- No new sealed benchmark.
- No Phase 3.
- No model/voter rerun.
- No QALB text persisted.
- No lexical exception list derived from individual cases.
