# Phase 2 — Selective Surgical Gate: Result Review

Date: 2026-09-28

Status: DEVELOPMENT GATE COMPLETED. Not sealed. No production threshold frozen.

## Canonical run

GitHub Actions:
- workflow: Phase 2 Selective Surgical Gate
- run: 36445652931
- conclusion: SUCCESS
- NoPnx SHA-256 verified:
  `584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6`
- official text-editing commit:
  `4d552ca3ae98029550f27fc52aa1b22883e16e61`

## Fixed operation-aware policy tested

Runtime-observable only:
- non-whitespace INSERT → allow
- REPLACE with NoPnx1 top-1 confidence >= 0.80 → allow
- DELETE → abstain
- other operations → abstain

This rule was chosen from prior development adjudication, so the replay is not an independent precision estimate.

## Main result

Operation-aware NoPnx1:
- retained edits: 38
- supported: 37
- wrong: 0
- partial: 1
- unnecessary: 0
- development supported precision: 97.37%
- changed passages: 26/41
- burden proxy from prior edit adjudication:
  - AUTO_ACCEPT_CANDIDATE: 25
  - UNCHANGED: 15
  - REVIEW_REQUIRED: 1
  - REJECT: 0
- automated exact target recoveries: 28/150 (diagnostic only)

Previous surgical NoPnx1:
- 60 applied edits
- 49 supported
- 7 wrong
- 2 partial
- 2 unnecessary
- 81.67% supported precision
- 33 changed passages

Thus selectivity materially reduces development risk while sacrificing some correction coverage.

## Arabic GED result

Two public GED-13 models were tested as localization probes on the same 150 published target locations.

ZAEBUC GED-13:
- target locations detected: 99/150
- recall: 66.0%
- source words flagged non-UC: 220/1931 = 11.39%

QALB14 GED-13:
- target locations detected: 79/150
- recall: 52.67%
- source words flagged non-UC: 187/1931 = 9.68%

A second ZAEBUC gate implementation using max subtoken error probability produced:
- top non-UC target recall: 101/150 = 67.33%
- p(error)>=0.30: 111/150 = 74.0%
- p(error)>=0.50: 102/150 = 68.0%
- p(error)>=0.70: 94/150 = 62.67%

### GED as a hard gate did NOT improve the main selective policy

Operation-aware only:
- 38 edits
- 37 supported
- 0 wrong
- 1 partial
- precision proxy: 97.37%

Operation-aware + ZAEBUC GED top-non-UC:
- 31 edits
- 30 supported
- 0 wrong
- 1 partial
- precision proxy: 96.77%

Operation-aware + ZAEBUC GED p(error)>=0.30:
- 35 edits
- 34 supported
- 0 wrong
- 1 partial
- precision proxy: 97.14%

Most importantly, the seven operation-aware edits classified as GED top-UC were all previously adjudicated as supported. Therefore the raw-source GED signal is not suitable as a hard acceptance gate in the current architecture.

Decision:
- hard GED gate: DROP for the next default prototype
- GED as a soft/ranking feature: WATCH / TEST
- full morph-preprocessed GED reproduction: TEST only if later evidence justifies the complexity

## Scientific stress result

For all tested selective variants:
- protected spans exact: 12/12
- source exact unchanged: 12/12
- [UNK] outputs: 0/12

This is a further improvement over the prior surgical NoPnx1 stress result, where 11/12 sources were unchanged.

These 12 project-authored cases remain invariant probes, not human-gold Arabic GEC accuracy.

## Reversible normalization probe

Among 98 NoPnx1 hazards suppressed specifically because of tokenizer [UNK]:
- 98/98 became tokenizable after removing combining marks/tatweel in an internal normalized model view
- 0/98 remained [UNK]

No normalized correction was applied.

This is a strong feasibility signal, but it does NOT prove that a normalized-model correction can be mapped back safely. Source text remains authoritative.

Decision:
- reversible normalized candidate view: PROTOTYPE NEXT
- irreversible normalization of delivered text: REJECT

## What improved versus the previous checkpoint

Improved:
- wrong applied edits reduced from 7/60 to 0/38 under the fixed operation-aware replay.
- development precision proxy rose from 81.67% to 97.37%.
- rejected passage proxy fell from 7 to 0.
- scientific stress source preservation improved from 11/12 to 12/12.
- all 98 tokenizer-UNK hazards proved tokenizable under a reversible normalized view.

Worsened / trade-off:
- operation-aware automated exact target recovery is 28/150 rather than the surgical queue's 32 automated flags.
- GED hard gating further reduces exact recovery to 24–26/150 without improving the existing 0-wrong edit profile.
- coverage remains the central bottleneck.

## Fresh end-of-gate research

Current external evidence remains consistent with the observed direction:

1. SWEET text editing is efficient and competitive for Arabic GEC, and its paper reports further gains from model ensembles.
   https://aclanthology.org/2025.acl-long.875/

2. The 2023 CAMeL-Lab Arabic GED/GEC work reports gains from GED-assisted GEC across three datasets, but its full setup includes contextual morphological preprocessing. Our raw-source hard-gate result should not be presented as a contradiction of that paper.
   https://aclanthology.org/2023.emnlp-main.396/

3. ZAEBUC* (LREC 2026) expands the bilingual Arabic-English benchmark and is a useful future independent corpus candidate for broader-domain evaluation.
   https://aclanthology.org/2026.lrec-1.137/

4. Nahw (EACL 2026) confirms substantial remaining difficulty in Arabic grammar understanding/correction and supports continued use of natural high-quality data.
   https://aclanthology.org/2026.eacl-long.296/

5. ArbESC+ (2025 preprint) reports gains from Arabic multi-system edit selection using AraT5, ByT5, mT5, AraBART, AraBART+Morph+GEC and text-editing candidates. This supports TESTING a second candidate generator later, but the evidence is preprint-level and should not drive immediate integration.
   https://arxiv.org/abs/2511.14230

## End-of-gate brainstorming decisions

- NoPnx1 + surgical renderer + operation-aware gate: **KEEP AS DEVELOPMENT REFERENCE**
- DELETE auto-application: **DROP**
- global confidence threshold alone: **DROP as sole policy**
- ZAEBUC GED hard gate on raw text: **DROP**
- GED as soft feature / reviewer signal: **WATCH / TEST**
- QALB14 GED: **WATCH; weaker target recall here**
- reversible normalized internal view: **PROTOTYPE NEXT**
- morphology-aware validator (Camel Morph): **PROTOTYPE after normalized-view feasibility**
- NoPnx2: **TEST_SELECTIVELY**
- Pnx: **TEST_SELECTIVELY only for explicit punctuation**
- AraBART/AraT5 second Arabic candidate: **TEST if normalized-view coverage remains inadequate**
- edit-level ensemble/voting / ArbESC-like combination: **WATCH until two independently useful candidate sources exist**
- separate Strict Scientific mode: **INTEGRATE architecturally**
- broad general-Arabic auto-proofreader claim: **DO NOT MAKE**

## Current interpretation

The project has improved from a renderer-safety problem to a precision/coverage optimization problem.

The selective source-preserving route is technically promising, but Phase 2 is not closed because:
1. the 97.37% figure is development replay on the same adjudicated set;
2. automated target coverage remains limited;
3. reversible normalization has only passed tokenization feasibility;
4. no new independent sealed evaluation has been run.

## Next bounded action

Before any sealed benchmark:

**Prototype a reversible normalized candidate view for the 98 tokenizer-UNK hazards, without auto-applying its corrections.**

Goal:
- determine whether normalized NoPnx can recover useful correction candidates among currently abstained locations;
- maintain exact original source and offset provenance;
- route normalized candidates to REVIEW only;
- quantify incremental target coverage and candidate quality before deciding whether a second Arabic GEC model is necessary.
