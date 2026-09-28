# Phase 2 — Reversible Normalized Candidate View: Result Review

Date: 2026-09-28

Status: DEVELOPMENT PROTOTYPE COMPLETED. No normalized candidate was auto-applied. No sealed benchmark was created. Phase 3 was not started.

## Canonical execution

GitHub Actions:
- workflow: Phase 2 Reversible Normalized Candidate View
- run: 36447653438
- conclusion: SUCCESS

Pinned execution:
- NoPnx SHA-256:
  `584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6`
- official text-editing commit:
  `4d552ca3ae98029550f27fc52aa1b22883e16e61`

## Fixed architecture

Original source is authoritative and immutable.

Internal normalized model view removes only:
- Unicode combining marks (category Mn)
- Arabic tatweel

No Alef normalization, Alef-Maksura/Yeh normalization, Teh-Marbuta/Heh normalization, punctuation normalization, or whitespace rewriting is performed.

Official NoPnx1 runs on the internal normalized view.

Only word locations that were previously suppressed by `TOKENIZER_UNK_WORD` are examined.

Every normalized correction is emitted as **REVIEW_ONLY_NEVER_AUTO_APPLY**.

## Main result

Previously suppressed tokenizer-UNK hazards:
- 98 hazards
- 98 unique source word locations

After reversible normalization:
- 98/98 locations are tokenizable
- 19/98 locations produce a non-K NoPnx1 candidate = 19.39%
- 79/98 locations produce no candidate
- normalized candidate rows: 19
- passages containing candidates: 14
- all 19 candidate source spans were identified back in the original source
- unsafe projection candidates: 0
- original source was never modified

This is a critical distinction: normalization solved tokenization feasibility for all 98 hazards, but the model still chose KEEP/no correction at 79 locations. Therefore tokenization was only one part of the coverage bottleneck.

## Target diagnostic

Published Nahw targets overlapping the 98 hazard word locations:
- 32

Normalized candidate view:
- 13/19 generated candidates overlap at least one published target
- 6/19 are at locations without one of the extracted local Nahw targets
- 12 target words automatically match the normalized published correction after applying all normalized candidates for that word
- all 12 automated matches were targets previously classified as ERROR_PRESERVED by the surgical path

Diagnostic potential:
- 12/32 = 37.5% of published targets located on former-UNK words now have an automated normalized-word match
- 12/150 = 8.0 percentage points of the full 150-target development set are potential incremental recoveries if linguistic adjudication confirms them

These numbers are **not quality scores**. Automated matching ignores some diacritic distinctions by design and cannot determine whether collateral/non-target candidates are linguistically justified.

## Candidate composition

Among 19 review-only candidates:
- REPLACE: 8
  - 5 overlap a published target
  - 5 have automated normalized target-word matches
- DELETE: 4
  - 3 overlap a published target
  - 3 have automated normalized target-word matches
- INSERT: 7
  - 5 overlap a published target
  - 4 have automated normalized target-word matches

Candidate top-1 confidence:
- minimum: 0.4269
- maximum: 0.9999
- mean: 0.8729

Confidence is descriptive only. Prior Phase 2 evidence already showed that confidence alone is not a sufficient safety rule.

## Important examples

The normalized view exposed candidates that align with previously missed corrections such as:
- `مالٌ` → normalized candidate `مالا`, consistent with published `مالًا`
- `إشتدادًا` → normalized candidate `اشتدادا`, consistent with published `اشتدادًا`
- `نَفْس` → normalized candidate `نفسا`, consistent with published `نفسًا`
- `إستشعِر` → normalized candidate `استشعر`, consistent with published `استشعِر`
- `خَطر` → normalized candidate `خطرا`, consistent with published `خَطرًا`
- `يقدِّموا` → normalized candidate `يقدمون`, consistent after dediacritization with published `يقدِّمون`
- `المصريِّين` → normalized candidate `المصريون`, consistent after dediacritization with published `المصريُّون`
- `الإرهابيُّون` → normalized candidate `الإرهابيين`, consistent after dediacritization with published `الإرهابيِّين`
- `يرضَ` → normalized candidate `يرضى`, exact lexical recovery

There are also candidates with no extracted target at that location, and at least one target-overlapping candidate (`وساعٍ` → `وساعا`) that does not automatically reach the published `وساعيًا`. These require linguistic adjudication and must not be inferred correct or wrong from string matching alone.

## Scientific stress invariant

12 project-authored scientific stress cases:
- delivered original source unchanged by policy: 12/12
- protected source spans intact by policy: 12/12
- normalized model view produced 2 candidate edits

Those 2 candidates were not applied. This confirms why normalized candidates must remain behind REVIEW in Strict Scientific mode.

## What improved

Compared with the previous Selective Surgical Gate:
- a previously inaccessible candidate channel now exists for former tokenizer-UNK locations;
- 19 review-only candidates were recovered without changing source text;
- 12 previously preserved Nahw errors now show automated normalized-word recovery signals;
- all candidate spans round-trip to identifiable original-source spans;
- strict source/scientific invariants remain intact.

## What did not improve enough

- 79/98 former-UNK locations still produce no model correction after normalization.
- only 19 candidate locations were recovered, so normalization cannot solve the general 108/150 missed-target problem by itself.
- dediacritization removes grammatical information that can be essential for Arabic case/mood; automated normalized matches can overstate correctness.
- six candidates occur outside the extracted local target locations; they may be valid collateral corrections or over-corrections and require adjudication.
- candidate quality is not yet known.

## Fresh end-of-gate research

1. Arabic diacritics are known to increase subword fragmentation and can degrade model performance under heavier diacritization. The observed 98/98 tokenizability recovery is consistent with that mechanism, but it does not establish correction quality.
   - Inoue et al., Findings of EACL 2026:
     https://aclanthology.org/2026.findings-eacl.22/

2. CAMeL Tools explicitly supports Arabic dediacritization and normalization. Broader character normalization is available, but because Alef variants, Alef Maksura/Yeh and Teh Marbuta/Heh can themselves be correction targets, they remain excluded from this source-fidelity model view.
   - https://camel-tools.readthedocs.io/en/latest/api/utils/dediac.html
   - https://camel-tools.readthedocs.io/en/latest/api/utils/normalize.html

3. Minimal-edit GEC research reinforces the need to optimize correction behavior separately from general fluency rewriting and supports preserving untouched source text.
   - BEA 2025:
     https://aclanthology.org/2025.bea-1.9/

4. Camel Morph MSA is a strong open-source morphological analyzer/generator and is a plausible independent validator for normalized Arabic candidates after linguistic adjudication establishes which candidate classes are useful.
   - LREC-COLING 2024:
     https://aclanthology.org/2024.lrec-main.240/

5. ArbESC+ reports gains from multi-system Arabic edit selection using AraT5, ByT5, mT5, AraBART, AraBART+Morph+GEC and text-editing candidates. It is currently a preprint, so it supports testing a second candidate source rather than immediate integration.
   - https://arxiv.org/abs/2511.14230

## End-of-gate brainstorming

### Reversible normalized view limited to prior tokenizer hazards
**KEEP / PROTOTYPE SUCCESSFUL.**
It adds a new candidate channel without weakening source fidelity.

### Auto-apply normalized candidates
**REJECT.**
Dediacritization removes morphosyntactic information and two scientific normalized candidates already demonstrate the need for review.

### Adjudicate all 19 candidates before adding more heuristics
**NEXT REQUIRED GATE.**
Do not introduce confidence thresholds, morphology filters, or operation filters before observing normalized-candidate error modes.

### Restore/source-preserve original diacritics around a confirmed candidate
**TEST AFTER ADJUDICATION.**
Potential architecture: candidate identifies base-letter change → morphology/safety validator determines expected surface → surgical patch modifies only required base letters and explicitly handles diacritics.

### Camel Morph candidate validator
**PROTOTYPE IF adjudication is favorable.**
Especially useful for case endings, mood, agreement, broken spellings, and inflectional candidates.

### Broader Arabic normalization (Alef/Ya/Teh Marbuta)
**DO NOT TEST YET.**
Those distinctions overlap real GEC targets and would create label leakage/ambiguity in the model view.

### Use normalized candidates only when base surgical path abstains
**INTEGRATE architecturally.**
This prevents normalized candidates from competing unnecessarily with the higher-precision operation-aware route.

### Second Arabic GEC candidate generator
**TEST if normalized adjudication yields insufficient incremental coverage.**
AraBART/AraT5-family models are the next reasonable candidate source.

### Ensemble/edit voting
**WATCH.**
Useful only after a second independently valuable Arabic candidate source exists.

## Current forecast

The normalized candidate view is **promising as a secondary recovery channel**, not as a new default correction path.

The decisive next question is now empirical:

**Of the 19 newly recovered candidates, how many are linguistically supported, and how many of the 12 automated target matches survive adjudication?**

If a strong majority are supported with low wrong-edit burden, the next architecture should be:

operation-aware surgical NoPnx1
→ if abstained due tokenizer hazard: reversible normalized candidate view
→ morphology/safety validation
→ review/accept routing

If candidate quality is poor or incremental useful coverage is small, stop expanding normalization and test a second Arabic GEC model instead.
