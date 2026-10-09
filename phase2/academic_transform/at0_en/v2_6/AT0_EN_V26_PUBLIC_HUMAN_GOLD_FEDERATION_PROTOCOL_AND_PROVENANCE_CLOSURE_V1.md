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
| F01 exposure lineage | DOCUMENTARY_CORRECTION_COMPLETE / RECORD_ALIAS_CUSTODY_PENDING | Inventory corrected: R43/R44 = EBM-NLP_mod fold1/train; must still materialize exposed/protected aliases without opening VERIFY_INTERNAL |
| F02 DISTANT-CTO / role semantics | CORRECTED | Packet now restricts DISTANT-CTO to role-agnostic semantic-type weak ablation; TrialSieve/C-TrO not mapped to C |
| F03 gold-independent preprocessing | SYNTHETIC_WINDOWING_PASS / TOKENIZER_INTEGRATION_PENDING | Text-only planner synthetic closure PASS in run 37879437844; no gold consumed; pinned-tokenizer/end-to-end offset integration still required |
| F04 benchmark eligibility | TEXT_FINGERPRINT_PARTIAL_PASS / FAMILY_CUSTODY_PENDING | Aggregate-only audit: each corpus has 150 unique docs; every fold 120/15/15 with zero within-fold text overlap; 75/75 unique test docs across five folds; AD-vs-COVID exact text overlap 0; overlap with exposed EBM_mod fold1 TRAIN 0. Trial-family/prior-exposure custody audit still required |
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
Need:
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
Need synthetic-tested immutable adapters for:
- EBM-NLP_mod native P/I/C/O;
- original EBM P/I/O;
- TrialSieve 20-type;
- EvidenceOutcomes O;
- PICO-Corpus native BRAT ontology;
- DISTANT-CTO 11-type weak semantic mentions.

Status:
`NOT_YET_CLOSED`

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
Need:
- Python;
- PyTorch;
- Transformers;
- tokenizer;
- CUDA;
- deterministic settings;
- hardware qualification;
- mixed precision;
- gradient accumulation;
- artifact/checkpoint serialization;
- resume contract.

Status:
`PENDING`

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
