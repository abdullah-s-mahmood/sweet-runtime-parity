# ACAD_PASS — SURUS Admission Protocol Amendment V2

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `at0-en-v2.6-dev`

Status:
`FROZEN_PROTOCOL_AMENDMENT / NO_SCIENTIFIC_FIT_AUTHORIZED`

Governing independent review:
`FINAL_SURUS_ADMISSION_REVIEW_V1.md`

Independent review verdict:
`PROCEED_SURUS_ADMISSION_WITH_CHANGES`

This document prospectively amends only the SURUS-related auxiliary-data, loss/sampler, custody, implementation-preflight, and claim boundaries of:
`AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_V1.md`.

All non-conflicting V1 rules remain in force.

---

## 1. Scientific authorization boundary

Authorized now:
- implement this amendment;
- repair and rerun non-scientific schema/coordinate, adapter, custody, architecture/loss, executable-schedule/resume, and GPU/runtime preflights;
- regenerate/rebind source, ontology, admission, fold, runtime, and attempt manifests;
- perform final independent pre-fit review.

Not authorized now:
- any D0-D4 scientific fit;
- any protected benchmark scoring;
- any VERIFY_INTERNAL access;
- AD/COVID external benchmark scoring;
- SURUS OOD scoring;
- any SURUS-only scientific arm;
- any four-source-vs-five-source scientific ablation;
- any seventh adaptive arm;
- coefficient/threshold/seed search.

R44C remains frozen and consumed.
D5 remains canceled without replacement.

---

## 2. SURUS source identity

Pinned repository:
`surus-ai/dataset`

Pinned commit:
`3a61790d5c304dea95fb278f76cc3b1a0ca07564`

License:
`CC-BY-NC-4.0`

Research-use policy:
- preserve attribution, revision, license link, and change notices;
- do not infer unrestricted commercial-use rights;
- do not redistribute raw SURUS records in ACAD_PASS public artifacts unless separately justified by the license and project policy;
- prefer hashes, provenance, aggregate counts, and derived audit evidence.

---

## 3. Partition policy

Candidate training membership:
`Dataset == Indomain`

Initial candidate count:
`400`

This is 400 candidates BEFORE exclusions, not 400 guaranteed admitted training documents.

Reserved SURUS OOD:
- indication OOD = 90;
- study-type OOD = 33;
- total released OOD = 123.

The two OOD strata remain separate.

OOD restrictions:
- no training;
- no source-weight selection;
- no thresholding;
- no model/architecture selection;
- no stopping decisions;
- no interactive error inspection;
- no development feedback.

SURUS OOD is not authorized for evaluation by this amendment.
Any later evaluation requires a separately frozen evaluation population and scoring/checkpoint protocol after model/procedure selection.

Previously exposed OOD families do not become unseen by resealing.

No replacement sampling.
No split search.
No disease balancing.

---

## 4. Release-vs-publication discrepancy

The peer-reviewed publication partition annotation counts sum to:
`49,538`

The pinned public release audit currently contains:
`48,833`

Difference:
`705`

This discrepancy is explicitly unresolved.

Rules:
- the pinned release is the computational source of truth for this amendment;
- do not claim the released rows are identical to the paper's evaluated annotation set;
- do not invent an explanation;
- freeze release-specific counts after corrected schema/coordinate audit.

---

## 5. Canonical SURUS ontology

Do NOT key the ontology by label name.

Canonical primary identity:
`(source_commit, released_LabelID)`

Source tables:
- `label.csv`;
- `label_class.csv`.

Channel order:
numeric released LabelID 1 through 25.

Canonical channels:

1. `DISEASE::INDICATION`
2. `DRUG::CLASS`
3. `DRUG::DEVICE`
4. `DRUG::FORMULATION`
5. `DRUG::FUNDER`
6. `DRUG::MOLECULE`
7. `DRUG::TREATMENT_GROUP`
8. `ID::TRIAL`
9. `METHODOLOGY::DETERMINATION`
10. `METHODOLOGY::INCLUSION_CRITERIA`
11. `METHODOLOGY::OUTCOME`
12. `METHODOLOGY::STUDY_DESIGN`
13. `METHODOLOGY::STUDY_DURATION`
14. `METHODOLOGY::STUDY_SIZE`
15. `PARAMETER::BASELINE`
16. `PARAMETER::DETERMINATION`
17. `PARAMETER::EFFECT`
18. `RESULT::BASELINE`
19. `RESULT::DETERMINATION`
20. `RESULT::SIGNIFICANCE`
21. `RESULT::UNIT`
22. `RESULT::VALUE`
23. `RESULT::VARIABILITY`
24. `THERAPY::DOSE_REGIME`
25. `THERAPY::METHOD_OF_ADMINISTRATION`

The annotation manual opening reference to 26 does not supersede the released 25-ID table.

Store and validate:
- LabelID;
- LabelClassID;
- class name;
- label name.

Same label name under different classes remains distinct.

---

## 6. SURUS auxiliary head

SURUS is admitted only as a separate auxiliary human-gold task.

Architecture:
- one 25-channel span head;
- 64-dimensional start projection;
- 64-dimensional end projection;
- dropout 0.1;
- scale by `sqrt(64)`;
- legal contiguous pairs only;
- source-scope masking;
- restore/implement the protocol's explicit relative-position operation before implementation closure.

No:
- native P/I/C/O mapping;
- automatic mapping of CLASS, placebo, TREATMENT_GROUP, or any SURUS label to C;
- shared-label softmax with native P/I/C/O;
- SURUS head use at native inference;
- gold-dependent windowing;
- boundary snapping;
- span union.

Preserve:
- genuine overlap/nesting;
- distinct typed spans;
- identical typed duplicate spans only once.

---

## 7. Exact five-source auxiliary loss

Existing four-source loss is prospectively amended.

Freeze:

`L_aux = (L_EBM + L_TrialSieve + L_EvidenceOutcomes + L_PICO + L_SURUS) / 5`

`L = L_native + 0.25 * L_aux`

Therefore each source coefficient in total loss is:
`0.05`

Historical four-source coefficient:
`0.0625`

Prospective relative reduction per prior source:
`20%`

This change is an explicit component of the amended intervention.

No:
- coefficient sweep;
- arbitrary SURUS fraction;
- dynamic loss weighting;
- GradNorm;
- validation-driven source weighting;
- post-result reweighting.

Each source loss:
- document mean of the existing stable positive/negative log-sum-exp span loss;
- average over fully annotated applicable classes for that document;
- fully annotated class with zero positives remains valid negative supervision;
- unknown/unannotated scope contributes neither loss nor denominator;
- every positive must be representable and inside its valid mask;
- missing/masked positive is a hard failure;
- empty admitted source in any fold is STOP, never automatic renormalization.

---

## 8. Exact auxiliary source sampler

Preserve:
`8 auxiliary documents TOTAL per optimizer update`

Fixed source order:
1. EBM
2. TrialSieve
3. EvidenceOutcomes
4. PICO
5. SURUS

At update index t:
- one document from every source;
- one additional document from sources `t, t+1, t+2 mod 5`.

Per-update allocation rotates:
`2/2/2/1/1`

Across five consecutive updates:
each source contributes exactly 8 auxiliary documents.

Compute each source mean first.
Then average the five source losses equally.

Document ordering:
freeze label-independent deterministic permutations using domain-separated hashes over:
- protocol ID;
- fold;
- existing scientific seed;
- source;
- cycle;
- canonical record ID.

Consume without replacement within source cycle.

Checkpoint/resume must preserve:
- source cursors;
- cycle counters;
- source permutations;
- RNG states;
- optimizer/model/scheduler state;
- native ordering.

Matched D2/D3/D4 fold/seed instances use identical auxiliary source membership and source schedules.

Appending SURUS must not shift paired native initialization through RNG call-order changes.

---

## 9. Global provenance / decontamination graph

Construct one custody identity graph spanning:
- SURUS;
- every approved auxiliary source;
- all native development folds;
- protected/reserved partitions;
- historical exposure registry;
- entire original EBM auxiliary train;
- reserved original-EBM expert test;
- TrialSieve reserved test;
- SURUS reserved OOD;
- AD/COVID benchmark identity custody without opening protected evaluation labels.

Identity edges:
- exact PMID;
- normalized DOI;
- normalized title fingerprint;
- normalized abstract fingerprint;
- validated trial registry identifier.

Compute connected components transitively.

Normalization is for identity custody only and MUST NOT alter stored scoring text.

Conservative suspicious-match trigger:
- NFKC/casefold/whitespace-normalized word five-gram Jaccard >= 0.90; OR
- containment >= 0.95;
- at least 20 shared five-grams.

These thresholds trigger custody review/quarantine.
They are NOT scientific prediction thresholds and do NOT by themselves prove same-trial identity.

A registry ID links a family only when it identifies the reported study rather than an unrelated cited trial.

Missing metadata is not evidence of independence.
Irreducibly unresolved suspicious matches remain excluded or closure stays open.

---

## 10. Fixed precedence

Apply globally before per-fold exclusions.

Priority 1:
existing protected/forbidden families exclude any new training admission.

Native DESIGN membership remains fixed.

An OOD collision with DESIGN loses eligibility for an independence claim.

Priority 2:
clean reserved SURUS-OOD families exclude aliases from EVERY auxiliary training source.

Priority 3:
a SURUS in-domain family colliding with:
- native DESIGN;
- any reserved test;
- any existing approved auxiliary candidate family

is removed from SURUS.

Existing approved sources win over the new SURUS source.

Priority 4:
for fold f, remove every held-out native family from every auxiliary training source.

Never merge annotations from different corpora into synthetic gold.

Known exact-PMID overlap counts are custody evidence only:
- SURUS ALL vs EvidenceOutcomes: 7;
- SURUS ALL vs PICO-Corpus: 2;
- SURUS ALL vs TrialSieve train/validation: 1.

Do not infer retained SURUS count by naive subtraction.
Use connected-component set unions and final reason-coded exclusion counts.

Exact duplicate SURUS records:
retain one canonical representative ordered by:
1. numeric PMID;
2. released ArticleID.

Distinct publications in one trial remain one family for custody but remain distinct documents when admitted.

If a newly discovered family bridges native folds:
`STOP_FOR_EXPLICIT_FOLD_PROTOCOL_REVIEW`

Do not silently move native records or shrink native evaluation denominators.

---

## 11. Fit budget and attempt identities

Retain:
`45 scientific fits = D0-D4 * 3 folds * seeds {44,45,46}`

D5:
`CANCELED_WITHOUT_REPLACEMENT`

No:
- SURUS-only arm;
- four-source-vs-five-source arm;
- seventh arm.

Archive old attempt manifest.
Create a versioned successor while preserving:
- same 45 active attempt identities;
- nine D5 cancellation records;
- historical consumption state.

Bind each active slot to:
- amended protocol hash;
- SURUS source release hash;
- ontology manifest hash;
- admission/exclusion manifest hash;
- fold identity manifest hash;
- adapter/code hash;
- loss/sampler contract hash;
- scientific runtime hash;
- qualified GPU/runtime hash.

Scientific attempt consumption remains:
`CONSUMED WHEN THE SCIENTIFIC TRAINING JOB STARTS`

Not after first optimizer update.

Current 45 active slots are unstarted/unconsumed according to the independent review snapshot.

Mechanical/synthetic preflights do not consume scientific attempts.

---

## 12. Mandatory preflights before any optimizer update

### P1 — Corrected SURUS schema/coordinate closure
Repair `federation_surus_schema_audit.py`.

Required:
- ID-based label joins;
- class foreign-key validation;
- duplicate/unknown ID rejection;
- exact text/coordinate round-trip validation;
- source-text bounds;
- token/character consistency where released data provides it;
- representability checks;
- fail-closed state;
- per-partition/per-LabelID frozen counts;
- explicit release/publication 705-row discrepancy.

### P2 — SURUS adapter closure
Extend:
- `federation_adapters.py`;
- `federation_adapter_preflight.py`.

Required:
- canonical released LabelID identity;
- source-specific scope masking;
- no native promotion;
- exact-boundary fixtures;
- Unicode;
- punctuation;
- repeated mentions;
- same-name/different-class;
- overlap/nesting;
- window crossings;
- exact released coordinate origin;
- exact source text serialization.

Any unrepresentable positive:
`FAIL`

### P3 — Custody closure
Repair:
- `federation_surus_overlap_custody.py`;
- `federation_per_fold_data_manifest_custody.py`.

Required:
- global protected exclusions;
- full auxiliary/reserved identity graph;
- OOD alias exclusions across ALL training sources;
- transitive connected components;
- unresolved suspicious-match quarantine;
- reason-coded aggregate exclusions;
- no protected identity emission.

### P4 — Architecture/loss closure
Update and verify:
- `AuxSpanHeads`;
- `TypedSpanHead.forward`;
- `multilabel_categorical_loss`.

Required:
- 25 SURUS channels;
- explicit relative-position operation;
- actual D4 auxiliary integration;
- intended gradient routing;
- zero native supervision from SURUS labels;
- source-specific applicable-class denominators;
- exact equal-five-source gradient calculation;
- fail if a positive is masked out.

### P5 — Executable five-source schedule/resume closure
Use synthetic/source-safe fixtures exercising the actual scientific data path.

Required:
- 2/2/2/1/1 rotating schedule;
- equal source means;
- fixed native ordering;
- shared component initialization parity;
- full interrupted/resumed equivalence;
- preserved source cursors/permutations/RNG state;
- no TinyModel-only certification.

### P6 — Real GPU/runtime closure
Qualify amended shapes/masks on real GPU.

Freeze:
- GPU identity;
- VRAM;
- software/runtime;
- deterministic settings;
- mixed precision policy;
- realized effective batch;
- memory behavior;
- checkpoint hashes.

No hidden truncation.
No batch reduction.
No scientific schedule change for memory rescue.

### P7 — Manifest closure
Rebind:
- source pins;
- protocol;
- SURUS ontology;
- admission/exclusion;
- fold manifests;
- runtime contract;
- development attempt manifest;
- latest-state and continuity records.

### P8 — Final independent pre-fit review
Required before first scientific job.

---

## 13. Sealed evidence

Remain sealed:
- VERIFY_INTERNAL;
- AD/COVID protected texts/labels;
- AD/COVID external scoring;
- reserved original EBM expert test;
- TrialSieve test;
- SURUS OOD texts, labels, and record-level errors except existing isolated identity custody.

R44C remains consumed.

Previously exposed evidence remains exposed.

Record public SURUS paper/manual worked-example exposure in the exposure ledger.

---

## 14. Claim boundary

Allowed:
"A prospectively amended five-source auxiliary federation was compared with native-only controls under matched native development folds and schedules."

Not allowed:
- "SURUS caused the gain";
- "five sources are better than four";
- "SURUS supplied new native comparator gold";
- "the 123 OOD records are newly independent native-PICO tests";
- "SURUS published 0.95 F1 predicts ACAD_PASS precision";
- causal marginal SURUS claims from the 45-fit campaign.

D2-D0 and D3-D1 evaluate the amended federation package, not isolated SURUS contribution.

---

## 15. Falsification / stop conditions

Admission closure fails if any of:
- unresolved ontology identity;
- unrecoverable positive span;
- open protected-family path;
- empty admitted SURUS source in a fold;
- incompatible license purpose;
- inability to execute exact loss/sampler;
- inability to bind exact runtime/manifest;
- unresolved mandatory preflight.

Scientific hypothesis later weakened if:
- both prespecified native contrasts D2-D0 and D3-D1 are nonpositive after outputs are frozen;
- auxiliary scores improve while native precision worsens, supporting negative transfer;
- existing precision/recall gates fail.

Do not rescue by:
- post-hoc SURUS ablation;
- new threshold;
- new seed;
- new arm;
- new weighting;
- alternate subset.

---

## 16. Current checkpoint

`SURUS_ADMISSION_PROTOCOL_AMENDMENT_V2_FROZEN / NO_SCIENTIFIC_FIT`

Exact next sequential operation:
`P1_CORRECT_SURUS_SCHEMA_AND_COORDINATE_AUDIT -> RUN_READ_ONLY_PREFLIGHT -> FREEZE_RESULT`

Only after P1 PASS:
continue P2, then P3, P4, P5, P6, P7, P8 sequentially.

First scientific fit remains forbidden until P8 PASS.
