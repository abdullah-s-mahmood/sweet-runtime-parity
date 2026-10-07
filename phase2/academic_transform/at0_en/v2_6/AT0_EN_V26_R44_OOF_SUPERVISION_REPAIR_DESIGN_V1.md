# ACAD_PASS — R4.4 OOF Supervision Repair Design V1

Date: 2026-10-07
Status: DESIGN + READ-ONLY PREFLIGHT AUTHORIZED; SCIENTIFIC TRAINING NOT YET AUTHORIZED.

## 1. Why R4.4 exists

R4.3 Stage-B technical execution was valid but scientific gate failed.

Causal audits established:
- Stage-A B emits 2371/2371 exact correct entities and zero FP on its own FIT, yet on the already-exposed SELECT it emits 447 exact-type correct + 250 false proposals among 697 predictions.
- This explains why R4.3 native-error training slots were zero.
- R4.3 H0/H1 trained on feature distributions made artificially easy by in-sample upstream supervision.
- C_TYPE was trained only on exact gold spans but used as a validity veto.
- H0/H1 could reject only; they could not correct B type or boundaries.
- Source pipeline entity semantics are 3000 B-start entities in full fold1 TRAIN, while prior ACAD_PASS local-continuation logic counted 3011; future semantics are frozen separately.

R4.4 tests whether **realistic out-of-fold candidate supervision + label-independent contextual representations** materially improve exact precision before any repair or large architecture escalation.

## 2. Data governance

Input universe:
- only the 320 documents previously assigned to R4.3 FIT.
- the old 80-document SELECT is EXCLUDED from all R4.4 design/training/calibration/verification.
- historical DEV, fold1 test, all other folds, external EBM/COVID/AD tests, FactPICO and consumed 60-RCT holdout remain closed.

R4.4 creates:
- DESIGN = 256 documents.
- VERIFY_INTERNAL = 64 documents.

Within DESIGN, 5 OOF folds are constructed deterministically. After greedy assignment, a deterministic exhaustive pair-swap search between folds may accept only strict improvements to the same frozen balance objective while enforcing the already-frozen constraints:
- every fold C support >=15;
- every class deviation from its fold target <=25%;
- fold sizes unchanged;
- seed, data universe, targets and tolerances unchanged;
- no model outcomes participate.

VERIFY_INTERNAL:
- frozen before any R4.4 model training;
- never used for architecture, threshold, epoch, negative mix or calibration decisions;
- opened exactly once only if a DESIGN model passes all predeclared design gates.
- this is a phase-internal holdout, NOT a pristine external benchmark because the parent FIT documents were used in earlier R4.3 training/audits.

## 3. Gold semantic contract

Use `AT0_EN_V26_R43_GOLD_SOURCE_SEMANTIC_CONTRACT_FREEZE_V1.md`.

Core rules:
- source-compatible entity starts are B-P/B-I/B-C/B-O only.
- valid example-initial I-X continuations are linked to the previous same-type entity and never counted as independent entities.
- invalid initial I-X is an explicit data-quality event, never silently normalized.
- the 17 tokenizer-empty raw rows are removed as the original source preprocessing does.
- preserve document/fragment provenance.

Legacy R4.3 outputs are not recomputed.

## 4. DESIGN/VERIFY split

Deterministic document-grouped split with seed 44.

Balance objective includes:
- document count;
- source-compatible P/I/C/O entity counts;
- total tokens;
- goldless example count;
- TITLE/METHODS example counts where recognized.

No exact token duplicate group may cross DESIGN/VERIFY.

Target VERIFY_INTERNAL = 64 docs (~20% of parent FIT).
DESIGN = remaining 256.

Split construction is deterministic and fixed:
- greedy initialization minimizes the predeclared normalized balance objective;
- a deterministic exhaustive single pair-swap local search then accepts only strict improvements to that **same objective**;
- seed remains 44;
- target size, balance variables and tolerances remain unchanged;
- no downstream model result, SELECT metric or protected data participates in the optimization;
- stop when no improving pair swap exists.

Freeze:
- every document ID;
- class counts;
- token hashes;
- group hashes;
- manifest SHA256.

## 5. OOF upstream generation inside DESIGN

Create 5 deterministic document-grouped cross-fit folds using seed 44.
Each document appears in exactly one OOF fold.

For fold k:
- train B_CANDIDATE_k on the other four DESIGN folds only;
- train C_BOUNDARY_k on the other four folds only;
- no C_TYPE ancestor in the primary R4.4 path;
- final fixed epoch only; no within-fold validation selection.

Default frozen ancestors:
- same safe BiomedBERT base identity as R4.3;
- B: lr 5e-5, wd 0, batch 8, 10 epochs;
- Boundary: lr 5e-5, wd .01, batch 8, 3 epochs;
- seed = 44 + fold index only for deterministic initialization/shuffling; no seed shopping.

For held-out fold only:
- decode B with a NEW source-compatible constrained decoder:
  - only predicted `B-X` may start a candidate;
  - only following `I-X` of the same type may extend it;
  - `I-X` after O, at sequence start without explicit document carry, or after another type is recorded as a BIO violation and DOES NOT manufacture a candidate;
  - optional DOCUMENT_CONTINUITY carry is tracked separately and never changes SOURCE_COMPATIBLE benchmark entity count.
- infer B candidate spans + B predicted type + B confidence;
- infer boundary START/BOTH and END/BOTH probabilities;
- generate no labels with the ancestor itself;
- never use a model to create features for a document that participated in that model's supervised training.

Freeze per-fold:
- decoder-unit-test evidence for B-start, valid I extension, initial-I, O->I and cross-type-I;
- count of raw BIO violations by fold;
- train/held-out doc IDs;
- model hashes;
- inference roster;
- candidate roster;
- candidate/gold match labels assigned AFTER inference;
- access guards.

## 6. Stable contextual representation

Do NOT use the fine-tuned C_BOUNDARY hidden state as the primary contextual vector in R4.4.

Use the immutable converted BiomedBERT base encoder:
- same model for all DESIGN and VERIFY_INTERNAL docs;
- no label supervision;
- frozen;
- full current example context.

For every actual B proposal [s,e):
- start base vector;
- end base vector;
- mean interior base vector;
- previous base vector/edge marker;
- following base vector/edge marker.

This removes the major in-sample representation leakage found in R4.3.

Boundary model contributes only OOF scalar evidence:
- start boundary probability;
- end boundary probability.

## 7. Candidate-distribution training set

Primary head training population is **actual OOF B proposals**, not arbitrary synthetic spans.

For each OOF B proposal:
- if coordinates exactly match a gold entity, target its gold P/I/C/O class, regardless of B's predicted type;
- otherwise target NONE.

This explicitly permits type correction.

Record:
- B proposed type;
- B confidence;
- exact-coordinate match;
- typed match;
- overlap taxonomy;
- goldless-example flag;
- source section;
- width;
- provenance.

Do not automatically add gold spans that B failed to propose to the verifier training set; the verifier cannot act on absent candidates at inference.

Do not add synthetic local/composite negatives in the primary J0/J1 comparison.
They remain a prospectively separable ablation only after native OOF error coverage is known.

## 8. Section and structural features

Derive section metadata from source text without labels:
- TITLE
- METHODS
- UNKNOWN

Propagate current section across blank-delimited examples within each DOCSTART document.
Preflight reports coverage and ambiguity.
If >1% DESIGN examples are UNKNOWN or section transitions are inconsistent, section embedding is disabled for the primary diagnostic and the anomaly is investigated first.

Other deterministic features:
- candidate width embedding;
- B predicted-type embedding;
- B confidence scalar;
- boundary start/end scalar;
- normalized example index in document;
- normalized span start in example.

## 9. Primary heads

Both heads receive identical candidate rows, frozen-base context and scalar features.

### J0 — Contextual Joint Typed Existence
Classes:
`NONE/P/I/C/O`

Architecture:
- five separate 768->128 projections for start/end/interior/previous/following;
- learned edge vectors;
- width embedding 16;
- B-type embedding 16;
- section embedding 8 if preflight permits;
- normalized scalar features;
- concatenate -> LayerNorm -> Linear 128 -> GELU -> Dropout .1 -> 5 logits.

Loss:
- ordinary 5-way cross entropy in V1.
- no class weighting/focal loss in the primary diagnostic; class imbalance is reported.
- if class C is inadequate, stop and redesign prospectively rather than posthoc retuning.

### J1 — J0 + Biaffine
Exact J0 plus class-specific biaffine interaction between projected start/end vectors.

No triaffine, GlobalPointer, BOPN, MRC, stronger encoder, pseudo-labeling or LLM teacher in R4.4 primary comparison.

## 10. Head model selection on DESIGN only

Head evaluation uses document-grouped 5-fold CV over the frozen OOF candidate bank:
- for evaluation fold k, head trains on OOF rows from other four folds;
- held-out fold rows are never used in that head fit.
- aggregate all held-out predictions into one DESIGN-OOF prediction table.

Threshold grid remains:
`{0.80,0.85,0.90,0.95}`.

Candidate acceptance:
- top joint class must be non-NONE;
- top probability >= threshold.
- B proposed type agreement is NOT required; head may correct type.

Report both:
- coordinate ceiling (exact coordinates irrespective of B type);
- typed-B ceiling (exact coordinates+original B type);
- head exact typed performance.

Scientific DESIGN gate:
- every P/I/C/O precision >= .90;
- every recall >= .20;
- every accepted >=10;
- macro precision >= .90.
- exact span + exact final class.

Architecture selection:
- if neither passes DESIGN gate: `R44_NO_HEAD_READY`; VERIFY_INTERNAL stays closed.
- if one passes: nominate it.
- if both pass: prefer J0 unless J1 macro recall exceeds J0 by >=.02 absolute while preserving all gates.
- choose the LOWEST threshold in frozen grid that passes all gates.
- no posthoc threshold expansion.

## 11. Calibration diagnostics

Because J0/J1 produce one coherent 5-way softmax, report:
- multiclass Brier score;
- ECE;
- reliability bins;
- class-wise precision-recall at frozen thresholds;
- risk-coverage curve for accept vs REVIEW.

These are diagnostics; they cannot alter the primary frozen selection after predictions are seen.

## 12. Single VERIFY_INTERNAL confirmation

Only after DESIGN nomination:
1. train one B and one Boundary ancestor on all 256 DESIGN docs at fixed epochs;
2. use frozen base encoder for context;
3. train nominated joint head on ALL frozen DESIGN OOF candidate rows (not in-sample full-refit rows);
4. apply final ancestors/head once to the 64 VERIFY_INTERNAL docs;
5. apply the previously selected threshold unchanged.

PASS requires the same scientific gate on VERIFY_INTERNAL.
Also report bootstrap CIs by document.

If VERIFY fails:
- do not tune on VERIFY;
- freeze failure and return to DESIGN with a new version.

## 13. Refit-distribution audit

Because DESIGN head is trained on OOF B/Boundary evidence but VERIFY uses ancestors refit on all DESIGN:
- before looking at VERIFY labels, compare unlabeled feature distributions between DESIGN OOF and VERIFY inference (B confidence, boundary probs, candidate width/type distribution, base-embedding norms);
- predefined shift alerts: standardized mean difference >0.25 for any scalar or PSI >0.20 triggers `R44_REFIT_SHIFT_ALERT`.
- an alert is reported; it does not authorize tuning using VERIFY labels.

## 14. What R4.4 does NOT solve

R4.4 cannot repair wrong coordinates or recover candidates B never proposes.
If R4.4 passes precision but recall/coverage remains operationally insufficient, the next branch is:
- local repairability gate + bounded offset repair (BOPN/Locate-and-Label style), or
- boundary-pair proposal union.

If native candidate precision remains poor after corrected verifier:
- consider contrastive/self-paced hard-negative learning.

If context/type confusion remains:
- section/document context, FinePICO-style SSL, PEFT/LLM teacher or triaffine/global pair model can be prospectively tested later.

## 15. Stop boundary

Current authorization stops at:
- design;
- read-only split/section/count preflight;
- adversarial protocol review.

NO R4.4 B/Boundary/head training until those artifacts pass and the protocol is frozen.

NEXT_ACTION:
`RUN_R44_READ_ONLY_PREFLIGHT -> ADVERSARIAL_REVIEW -> FREEZE_OR_REPAIR_PROTOCOL -> ONLY_THEN_AUTHORIZE_OOF_TRAINING`.
