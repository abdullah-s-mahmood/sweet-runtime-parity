# ACAD_PASS — Public Human-Gold Federation Protocol and Provenance Closure V1

Date: 2026-10-09

State:
`CLOSURE_IN_PROGRESS / FIRST_FIT_NOT_AUTHORIZED`

Governing protocol:
`AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_V1.md`

Canonical independent review:
`FINAL_PUBLIC_HUMAN_GOLD_FEDERATION_REVIEW_V1.md`

## Mandatory review findings

| Finding | Current status | Evidence / remaining action |
|---|---|---|
| F01 exposure lineage | DOCUMENTARY_CORRECTION_COMPLETE / PMID_CUSTODY_PARTIAL_PASS | Inventory corrected. Protected mapping recovered original PMID identity for 250/256 DESIGN, 49/64 VERIFY_INTERNAL and 60/80 OLD_SELECT records with zero duplicate assignments; unresolved records remain conservatively unresolved |
| F02 DISTANT-CTO / role semantics | CORRECTED | Packet now restricts DISTANT-CTO to role-agnostic semantic-type weak ablation; TrialSieve/C-TrO not mapped to C |
| F03 gold-independent preprocessing | SYNTHETIC_WINDOWING_PASS / TOKENIZER_INTEGRATION_PENDING | Text-only planner synthetic closure PASS in run 37879437844; no gold consumed; pinned-tokenizer/end-to-end offset integration still required |
| F04 benchmark eligibility | MULTILAYER_PROVENANCE_PARTIAL_PASS / FAMILY_CLOSURE_PENDING | Exact-text split audit PASS; registry custody overlap 0; exact-title PMID resolution AD 118/150 (test 64/75), COVID 116/150 (test 61/75), with 0 resolved PMID overlap against DESIGN/VERIFY_INTERNAL/OLD_SELECT/PICO-Corpus/EvidenceOutcomes. Unresolved identities and same-trial distinct-publication linkage remain open |
| F05 incompatible headline comparisons | DOCUMENTARY_CLOSED | AlpaPICO string-set scorer verified; FinePICO/PICOX/GPT-4o results remain task-qualified, not direct strict-span ranks |
| F06 finite study | PROTOCOL_FROZEN / EXECUTION_BLOCKED | Six development arms, finite seeds/folds/weights/budget now frozen; no fit yet |

## Required before first fit

### Source identity
Repository/model revisions are now pinned in `AT0_EN_V26_FEDERATION_SOURCE_PIN_MANIFEST_V1.json`.
No floating scientific source is permitted.

Still need immutable:
- release URL;
- commit/tag;
- file SHA256;
- license;
- exact counts;
- ontology;
- official split membership
for every authorized native/auxiliary/weak source.

Status:
`INCOMPLETE`

### Global alias / family graph
EBM-NLP_mod -> original EBM PMID mapping is now partial PASS:
- all 400: 359/400 (89.75%);
- DESIGN: 250/256 (97.65625%);
- VERIFY_INTERNAL: 49/64 (76.5625%);
- OLD_SELECT: 60/80 (75%).
No PMID values were emitted outside custody.

Still need:
- PMID;
- DOI;
- registry IDs;
- raw-text SHA256;
- normalized-text fingerprint;
- title fingerprint;
- trial-family edges;
- translated/derived aliases;
- ambiguity ledger.

Status:
`INCOMPLETE`

### Protected custody
Aggregate-only protected registry custody is now operational and PASS at the registry-ID layer.
Canonical run `37880937020`, artifact `11594715629`, digest `sha256:3759163014b2214ff5bc8d4792835d0e0583b8102a3654e51d7c825f776f074f`.

No shared visible registry IDs were found between DESIGN/VERIFY_INTERNAL/OLD_SELECT and AD/COVID. No protected IDs/text/gold were emitted.

Coverage is sparse, so PMID/DOI/title/trial-family custody remains required.

Status:
`REGISTRY_CUSTODY_PASS / PMID_DOI_TITLE_FAMILY_CUSTODY_PENDING`

### Benchmark eligibility
AD/COVID:
`CANDIDATE_ONLY`

Do not certify before:
- split file hashes;
- document membership audit;
- repeated-test membership audit;
- trial-family graph;
- exposure audit;
- training-side decontamination manifest.

### Preprocessing
Text-only, gold-independent source-compatible processor:
`SYNTHETIC_WINDOW_PLANNER_PASS / PINNED_TOKENIZER_AND_OFFSET_INTEGRATION_PENDING`

### Adapters
A1-A5 native/human auxiliary source preflight PASS in run `37881966232`, artifact `11594457041`, digest `sha256:156a8ccd6471a410bdc7dd230d98575f3f5fc6fca015d1041fb52adbdc2b804f`.

Closed structurally:
- EBM-NLP_mod native P/I/C/O;
- original EBM training P/I/O auxiliary;
- TrialSieve 20-type auxiliary;
- EvidenceOutcomes 500RCT O auxiliary;
- PICO-Corpus 26-type native auxiliary ontology.

Still pending:
- D5 DISTANT-CTO official weak-file hash/schema/admission preflight;
- per-fit family-decontamination manifests.

Status:
`A1_A5_PASS / D5_WEAK_AND_PER_FIT_DECONTAMINATION_PENDING`

### Scorer
Synthetic mechanics PASS in run `37879727833`, artifact `11594166539`, digest `sha256:1ca17f8f0403d405195d776d93d6e97a6e893b48de4ab48953d712c1096fa32d`.

Closed synthetically:
- strict occurrence-level typed exact matching;
- duplicate/nonfinite/coordinate/document guards;
- both-empty zero-TP policy;
- wrong-type/boundary accounting;
- selective threshold grid/selection/no-pass path;
- deterministic paired family-cluster bootstrap mechanics.

Still required before real scoring:
- source-compatible continuation integration;
- expected-document manifests per fit;
- exact fold/seed aggregation wiring against frozen manifests.

Status:
`SYNTHETIC_MECHANICS_PASS / REAL_MANIFEST_INTEGRATION_PENDING`

### Comparators
Need frozen recipes/hashes for:
- D0 native BIO reference;
- data-matched BIO;
- PICOX four-class adapted comparator.

Status:
`PICOX_RECIPE_PENDING`

### Runtime
Closed model/tokenizer identity:
- Python 3.11.16 identity preflight;
- Transformers 4.57.3 / HF Hub 0.36.0 / tokenizers 0.22.1 validated for config/tokenizer identity;
- BiomedBERT-base, BioClinical ModernBERT-base and PICOX PubMedBERT-large full revisions/weight SHA256/tokenizer fingerprints frozen.

Still need GPU training runtime:
- PyTorch CUDA build;
- actual CUDA/cuDNN/GPU;
- deterministic settings;
- mixed precision;
- gradient accumulation realization;
- artifact/checkpoint serialization;
- resume contract.

Current GitHub repo is user-owned; GitHub-hosted GPU larger-runner availability is not established. See `AT0_EN_V26_FEDERATION_COMPUTE_BACKEND_READINESS_V1.md`.

Status:
`MODEL_TOKENIZER_IDENTITY_PASS / GPU_RUNTIME_BACKEND_PENDING`

### Attempt manifest
Immutable 54-slot D0-D5 x 3 folds x seeds 44/45/46 ledger created:
`AT0_EN_V26_FEDERATION_DEVELOPMENT_ATTEMPT_MANIFEST_V1.json`.

Slots are NOT_STARTED and scientific_training_authorized=false; data/runtime hashes remain pending closure.

Status:
`SLOT_LEDGER_FROZEN / DATA_RUNTIME_BINDING_PENDING`

## Closed evidence

Canonical independent review archived in repository.

R44C:
consumed and frozen.

VERIFY_INTERNAL:
closed.

No successor model has been trained.

## Authorization rule

First successor fit is authorized only when this file is superseded by:

`PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_AND_PROVENANCE_CLOSURE_PASS`

with:
- all source/manifests/hashes fixed;
- benchmark eligibility explicitly decided;
- synthetic-only preflight PASS;
- runtime/attempt manifest fixed;
- no protected-data leakage.

Until then:
`NO_SUCCESSOR_TRAINING`


## 2026-10-09 windowing and split-audit update

Run:
`37879437844`

Windowing artifact:
`11594086484`
digest `sha256:22f09221c98e374bc20d035c6e4cce5ecf0328d7381ef86c394ea2652efbff0a`.

Public split aggregate artifact:
`11594006897`
digest `sha256:a7cc367fdb669d9a01c4575133dbf8dcfcf2d2b0eff22c614bfbd68278120510`.

Freeze:
`AT0_EN_V26_FEDERATION_PREFIT_WINDOWING_SPLIT_AUDIT_FREEZE_V1.md`.

Important positive findings:
- AD: 150 unique documents; five disjoint 15-document TEST subsets = 75 unique TEST docs;
- COVID: same structure;
- all within-fold train/dev/test exact-text overlaps = 0;
- AD/COVID full-corpus exact-text overlap = 0;
- AD and COVID exact-text overlap with exposed EBM-NLP_mod fold1 TRAIN = 0.

This materially improves F04 confidence but does NOT certify trial-family independence.

Overall state remains:
`CLOSURE_IN_PROGRESS / FIRST_FIT_NOT_AUTHORIZED`.


## 2026-10-09 scorer/source-pin update

Strict scorer synthetic preflight:
PASS.

Run:
`37879727833`

Artifact:
`11594166539`

Source/model revision pin manifest:
`AT0_EN_V26_FEDERATION_SOURCE_PIN_MANIFEST_V1.json`

Pinned public repositories now include:
- BIDS section-specific PICO source;
- original EBM-NLP;
- PICO-Corpus;
- TrialSieve;
- EvidenceOutcomes;
- DISTANT-CTO;
- PICOX.

Pinned model revisions:
- BiomedBERT reference;
- BioClinical ModernBERT challenger.

Revision pinning does not equal full source admission; licenses/file hashes/ontologies/dedup remain pending.

Overall:
`CLOSURE_IN_PROGRESS / FIRST_FIT_NOT_AUTHORIZED`.


## 2026-10-09 protected registry custody update

Canonicalized rerun resolved the earlier COVID 153-vs-150 representation discrepancy.

Freeze:
`AT0_EN_V26_PROTECTED_REGISTRY_CUSTODY_AUDIT_FREEZE_V1.md`.

Registry collision:
0 across all protected/exposed historical partitions versus AD/COVID whole/test-union targets.

This is supportive but not sufficient for trial-family independence.


## 2026-10-09 EBM PMID mapping custody update

Run `37881123349`:
`FEDERATION_EBM_MOD_TO_ORIGINAL_PMID_MAPPING_FEASIBILITY_PASS`

Artifact:
`11594720967`

Freeze:
`AT0_EN_V26_EBM_MOD_PMID_MAPPING_CUSTODY_FREEZE_V1.md`

This strengthens F01/protected identity substantially but leaves 41/400 derived records unresolved and does not yet map AD/COVID identities.


## 2026-10-09 public target PMID + adapter update

Public target PMID custody:
- AD 118/150 resolved; TEST 64/75;
- COVID 116/150 resolved; TEST 61/75;
- zero resolved PMID overlap against protected/exposed historical roles or PICO-Corpus/EvidenceOutcomes;
- no PMIDs/titles/raw text/gold emitted.

Freeze:
`AT0_EN_V26_PUBLIC_TARGET_PMID_CUSTODY_AUDIT_FREEZE_V1.md`.

Adapter source preflight:
PASS for A1-A5.

Freeze:
`AT0_EN_V26_FEDERATION_ADAPTER_SOURCE_PREFLIGHT_FREEZE_V1.md`.

Benchmark family closure and D5 remain pending.


## 2026-10-09 model/tokenizer identity update

Run `37882354519` PASS.
Artifact `11594613594`.
Digest `sha256:48cdb8bc6b82567f2e1ec38fe5a3fb13c449c32419053ef5d8ac6dfb07a40e50`.

Freeze:
`AT0_EN_V26_FEDERATION_MODEL_TOKENIZER_IDENTITY_PREFLIGHT_FREEZE_V1.md`.

All three encoder revisions and weight SHA256 identities matched Hugging Face metadata; fast-tokenizer fixtures are frozen.


## 2026-10-09 source-schema and target-PMID closure update

Public target PMID custody:
- run `37881398971` PASS;
- artifact `11594971856`;
- AD resolved 118/150 overall and 64/75 official TEST-union PMIDs;
- COVID resolved 116/150 overall and 61/75 official TEST-union PMIDs;
- zero resolved-PMID collisions with DESIGN, VERIFY_INTERNAL, OLD_SELECT, PICO-Corpus or EvidenceOutcomes;
- AD/COVID cross-resolved-PMID overlap = 0.

Public source schema:
- run `37884140956` PASS;
- artifact `11595364822`;
- EvidenceOutcomes = outcome-only auxiliary;
- PICO-Corpus = native 26-type auxiliary;
- TrialSieve canonical modeling subset = 1,609 docs / 20 tags / 1,148 train + 223 validation + 238 test;
- original EBM-NLP = native P/I/O auxiliary.

Freeze files:
- `AT0_EN_V26_PUBLIC_TARGET_PMID_CUSTODY_AUDIT_FREEZE_V1.md`;
- `AT0_EN_V26_PUBLIC_SOURCE_SCHEMA_AUDIT_FREEZE_V1.md`.

These strengthen F01/F04 and adapter-role closure but do not yet prove complete same-trial-family independence for unresolved records.


## 2026-10-09 model/tokenizer identity closure update

Freeze:
`AT0_EN_V26_FEDERATION_MODEL_TOKENIZER_IDENTITY_PREFLIGHT_FREEZE_V1.md`

The three primary encoder/tokenizer identities are reproducibly pinned:
- D0-D3 BiomedBERT-base;
- D4 BioClinical-ModernBERT-base;
- adapted PICOX BiomedBERT-large.

No floating model revision remains in the frozen first-campaign design.
