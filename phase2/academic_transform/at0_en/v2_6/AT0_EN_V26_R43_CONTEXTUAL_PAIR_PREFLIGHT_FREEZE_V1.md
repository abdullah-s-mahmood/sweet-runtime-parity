# AT0 EN V2.6 — R4.3 Contextual Pair Preflight Freeze V1

Date: 2026-10-07

## 1. Decision state

Higher-model architecture review verdict:

`RUN_ONE_MORE_TRAIN_ONLY_DIAGNOSTIC_BEFORE_ARCHITECTURE_SELECTION`

Frozen diagnostic candidates:
- H0 = contextual typed MLP
- H1 = identical contextual path + class-specific biaffine start/end interaction

Current state after this checkpoint:

`R43_CONTEXTUAL_PAIR_PREFLIGHT_PASS / STOP_BEFORE_TRAINING`

No H0/H1 or ancestor scientific training has been performed.

## 2. First preflight stop and source-semantics correction

Initial preflight:
- run `37533646474`
- conclusion: failure
- classification: PRE-TRAINING SEMANTICS PREFLIGHT STOP
- no model training
- no DEV/test access

Reason:
11 blank-delimited source examples begin with an `I-*` label.

Direct TRAIN-only source audit established:
- within-example invalid I transitions = 0
- sequence-initial I cases = 11
- all 11/11 are preceded in the same `-DOCSTART-` document by a previous example ending with the same entity type
- I-P = 8
- I-I = 2
- I-O = 1

Therefore these are source continuation segments rather than arbitrary malformed labels.

Frozen amendment:
`AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V2.md`

Design V2 commit:
`8d3a50e5ece33df9d00c7037d204155a1067778d`

Raw labels remain unchanged.
For exact per-example span scoring, an initial I-X becomes the start coordinate of an example-local continuation segment only when the previous example in the same document ends with the same type.

## 3. Successful replacement preflight identity

Run:
`37534110955`

Run head:
`4ca858fcd8b632bc67748bfe1e8fdb0d9d6f8dbd`

Conclusion:
`success`

Artifact:
`11446235369`

Artifact digest:
`sha256:84f9688be55f46dfc6d05cee638c7552e12e6ed0ccae63e3b6f2fc99a4478c94`

State:
`R43_CONTEXTUAL_PAIR_PREFLIGHT_PASS`

## 4. Exact TRAIN inventory

TRAIN SHA256:
`6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`

Recovered:
- documents = 400
- sentences = 1576
- tokens = 41070
- gold entity segments = 3011
- max gold span width = 54 words

Gold class counts:
- P = 434
- I = 1328
- C = 181
- O = 1068

Source-aligned literal-empty rows removed:
- O = 5
- I-I = 5
- I-P = 6
- I-O = 1
- total = 17

Flat representation checks:
- invalid BIO continuations after V2 semantics = 0
- gold coordinate/class conflicts = 0
- source continuation segments = 11
- max-width guard = PASS

## 5. Document grouping

Exact token-identical duplicate document groups:
- 0

Documents inside duplicate groups:
- 0

Token-identical documents with conflicting tag sequences:
- 0

Therefore the source contains 400 unique token-level document groups under the frozen exact-duplicate definition.

## 6. Frozen FIT / SELECT partition

Split manifest SHA256:
`fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`

Document overlap:
- 0

FIT:
- documents = 320
- sentences = 1292
- tokens = 33244
- P = 342
- I = 1038
- C = 144
- O = 847
- total gold = 2371

SELECT:
- documents = 80
- sentences = 284
- tokens = 7826
- P = 92
- I = 290
- C = 37
- O = 221
- total gold = 640

Relative SELECT deviation from exact 20% class targets:
- P = +5.99%
- I = +9.19%
- C = +2.21%
- O = +3.46%

All classes exceed the frozen minimum SELECT-support preflight requirement.

The manifest is now immutable for this diagnostic.

## 7. TRAIN-only negative-construction feasibility

FIT gold positives:
- 2371

Local perturbation selections:
- raw = 4742

Composite selections:
- raw total = 2042
- same-class composite = 1239
- different-class composite = 803

Unique static LOCAL + COMPOSITE NONE coordinates:
- 6157

Prospective length-matched background fallback:
- source gold spans with an available fallback = 1982
- unique reserved fallback coordinates = 1908

Gold/synthetic coordinate collisions after gold precedence:
- 0

Static example manifest SHA256:
`1ac4b4dd2ca3c1dbc42b5dc0530cafc93fb289f1646b518e305a3d7c20d5d8d2`

Native FIT-model error negatives:
- deliberately NOT materialized in preflight
- remain deferred until a future FIT-only B replica exists
- generation algorithm is frozen prospectively in Design V1

## 8. Context-necessity / input-label collision audit

Complete TRAIN gold-only:
- identical cropped token strings assigned multiple entity classes = 14
- identical tokenizer-ID sequences assigned multiple entity classes = 14

FIT gold versus prospective synthetic NONE:
- cropped gold strings with multiple entity classes = 9
- tokenizer-ID sequences with multiple entity classes = 9
- cropped token strings appearing as both entity and synthetic NONE = 43
- tokenizer-ID sequences appearing as both entity and synthetic NONE = 48

Interpretation:
cropped span content alone is provably non-separable for a nontrivial subset of TRAIN under the proposed negative construction.

This materially strengthens the missing-context hypothesis and explains why a content-only guard such as R4.2D can fail even when optimization succeeds.

It does NOT prove that biaffine interaction is necessary; H0 versus H1 remains the bounded test.

## 9. Architecture size audit

Shared contextual projections + sentence-edge vectors + width embedding:
- 494,720 trainable parameters

H0 total trainable head parameters:
- 579,461

H1 biaffine additional parameters:
- 83,205

H1 total trainable head parameters:
- 662,666

Therefore H1 adds exactly 83,205 trainable parameters over H0 while keeping data, contextual features and MLP path identical.

## 10. Ancestry isolation frozen for any future diagnostic

Existing globally-trained B/C artifacts are reference-only and MUST NOT produce SELECT proposals/features.

Future diagnostic, if separately authorized, must train from the verified base using FIT only:
- B candidate generator: 10 fixed epochs
- boundary model: 3 fixed epochs
- type model: 3 fixed epochs
- final fixed epoch only
- no SELECT or historical DEV checkpoint selection

H0/H1 contextual encoder:
`FROZEN_FINAL_FIT_ONLY_BOUNDARY_ENCODER`

## 11. Access guards

Verified:
- TRAIN only = true
- historical DEV read = false
- fold1 TEST read = false
- other folds read = false
- external EBM/COVID/AD tests read = false
- FactPICO used = false
- consumed 60-RCT holdout used = false
- scientific training performed = false

## 12. Scientific interpretation

What improved:
- architecture-selection protocol is now insulated from the exposed historical DEV;
- document-level FIT/SELECT isolation is feasible and frozen;
- class support, including C, is adequate for the bounded internal diagnostic;
- the missing-context hypothesis now has direct TRAIN evidence;
- both same-class and different-class composite negatives are available at substantial scale;
- H0 and H1 can be compared with only one controlled architectural difference.

What worsened / new risk:
- 14 identical cropped strings carry different gold entity classes across contexts;
- 43 cropped strings can be both an entity and synthetic NONE depending on context;
- therefore any future cropped-content-only classifier is structurally disadvantaged;
- SELECT is still internal TRAIN-derived evidence, not a fresh external test.

No result yet establishes that H0 or H1 will pass the scientific gate.

## 13. Stop boundary

STOP NOW.

Do not train:
- FIT-only B
- FIT-only boundary
- FIT-only type
- H0
- H1

until the frozen packet is reviewed and a separate training authorization is made.

Protected external tests remain closed.

Exact next checkpoint:

`REVIEW_R43_PREFLIGHT_PACKET_THEN_DECIDE_IF_ONE_FIT_SELECT_H0_VS_H1_DIAGNOSTIC_IS_AUTHORIZED`
