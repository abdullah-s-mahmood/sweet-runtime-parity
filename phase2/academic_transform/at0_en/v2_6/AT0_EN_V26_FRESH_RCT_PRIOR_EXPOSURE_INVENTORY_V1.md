# ACAD_PASS — Fresh RCT Prior-Exposure Inventory V1

Date: 2026-10-08

State:
`PARTIAL_PROVENANCE_INVENTORY_INCOMPLETE`

Acquisition authorization:
`BLOCKED`

Purpose:
build the prior-exposure ledger required by the frozen fresh-RCT acquisition protocol **without opening protected corpora** and without retrieving any new RCT records.

This file records only exposures/provenance that are currently evidenced from repository history and frozen manifests. Missing entries remain blockers; absence from this file MUST NOT be interpreted as proof of non-exposure.

## 1. EBM-NLP_mod — definite prior R43/R44 project exposure

Source repository:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO`

Pinned source commit:
`bc4b878773192f38b2600ec830ca4208b82f7dc0`

Pinned source file:
`data/EBM-NLPmod/fold1/train.txt`

Pinned TRAIN SHA256:
`6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`

Authoritative repository evidence:
- `AT0_EN_V26_R43_GOLD_SOURCE_SEMANTIC_CONTRACT_FREEZE_V1.md`
- `AT0_EN_V26_R44_PREFLIGHT_FREEZE_V1.md`

This corrects the superseded inventory wording that incorrectly placed the R4.3/R44 320-document lineage under PICO-Corpus.

### R43/R44 lineage

Pinned EBM-NLP_mod fold1 TRAIN contains:
- 400 documents before the R43/R44 FIT/SELECT lineage.

Later frozen source-compatible FIT inventory:
- 320 documents;
- 1,292 examples;
- 33,244 tokens;
- P/I/C/O = 339/1036/144/846.

R44 split:
- DESIGN = 256 docs;
- VERIFY_INTERNAL = 64 docs.

DESIGN:
- 1,034 examples;
- 26,595 tokens;
- P/I/C/O = 271/829/115/677.

VERIFY_INTERNAL:
- 258 examples;
- 6,649 tokens;
- P/I/C/O = 68/207/29/169.

R44 manifest SHA256:
`799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`

Status:
- R43/R44 EBM-NLP_mod lineage: `DEFINITE_PROJECT_EXPOSURE`
- DESIGN: `KNOWN_EXPOSED_AND_CONSUMED_FOR_ADAPTIVE_DEVELOPMENT`
- VERIFY_INTERNAL: `PROTECTED_HISTORICAL / MUST_DEDUP_INSIDE_CUSTODY / DO_NOT_OPEN`

Important:
A public copy of a protected VERIFY_INTERNAL record is NOT permission to read, train on, score, or otherwise expose that record in the developer process. Alias/trial-family deduplication must occur through protected custody.

### Source-compatible semantic contract

Source exact-evaluation entity starts use raw `B-X` starts.
Example-initial `I-X` fragments with a valid same-type predecessor are continuation fragments, not new independent entities.
Future source-compatible scoring/preprocessing must preserve this contract.

### EBM-NLP_mod benchmark role

Because the R43/R44 lineage is definitively exposed:
- exposed unprotected EBM-NLP_mod records may be TRAIN/DEVELOPMENT;
- protected VERIFY_INTERNAL remains CLOSED;
- no whole-corpus or five-fold EBM-NLP_mod claim may be described as new independent evidence in the first federation campaign.

Exact record/family aliases across original EBM-NLP and derived EBM-NLP_mod must be materialized before first successor fit.

## 1B. PICO-Corpus — definite but separate prior project exposure

Source repository:
`sociocom/PICO-Corpus`

Frozen source commit evidenced by the R4 internal-holdout manifest:
`482b7d8f135fe6ea424961c2812e8d214c3f4a5f`

Evidence file:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_INTERNAL_HOLDOUT_MANIFEST_V1.json`

Manifest Git blob:
`2959279b075a8f24c9eea31402896af74f9a2377`

Known project exposure to PICO-Corpus remains real and must be inventoried separately from the EBM-NLP_mod R43/R44 lineage.

The prior inventory's statement assigning the R43/R44 320-document source-compatible inventory to PICO-Corpus is RETIRED.

Current role:
`TRAIN_DEVELOPMENT_ONLY_AFTER_RECORD_LEVEL_PROVENANCE_AUDIT`

No PICO-Corpus record or alias may be used as new independent benchmark evidence merely because the R43/R44 lineage has now been corrected to EBM-NLP_mod.

## 2. FactPICO — definite prior project exposure

Primary resource:
FactPICO, ACL 2024.

Frozen raw archive SHA256:
`ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`

Frozen primary gold:
`data/all_evaluations.csv`

Primary gold SHA256:
`1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd`

Prediction universe:
- 345 records;
- 115 source RCT abstract clusters.

Frozen V5 build manifest:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_H1_V5_BUILD_MANIFEST.json`

Manifest Git blob:
`0635e5ce1aa59727c2e4f4aa43d4285262a420e8`

Source-cluster hash reference:
`phase2/academic_transform/at0_en/v2_6/FACTPICO_V25_SOURCE_CLUSTER_HASHES_FOR_R4_OVERLAP_V1.json`

Hash-reference Git blob:
`dcdee40445c379b7589c1140e74cf2206a79de93`

Frozen scoring artifact evidence:
- scoring run `37325138336`;
- artifact `11351451888`;
- artifact digest `sha256:105534207a4566c38d76174e9cd263244b87e37358b6007c76502bc250d67e77`;
- joined rows SHA256 `144b778ae9ea1ee2c511dca862f1f0fe937e9b922d0e64df94eb0174c4f0e10f`.

Exactly 115 SHA256 source-cluster identities are already available without reopening source abstracts.

Status:
`KNOWN_EXPOSED_AND_CONSUMED`

Fresh-acquisition requirement:
the independent custodian must compare all new candidate trial families against these 115 cluster identities plus available PMID/DOI/title/registry provenance.

## 3. AT0-EN V2.3 second unseen holdout — definite project exposure

Manifest:
`phase2/academic_transform/at0_en/v2_3/holdout/SECOND_UNSEEN_HOLDOUT_V1_MANIFEST.json`

Manifest Git blob:
`9c196b0e0d493fb1379303c9f402aa17eeb6e00e`

Counts:
- total 36;
- 12 safe controls;
- 24 adversarial;
- 12 cases.

Input SHA256:
`b1633df5e0418082a990945dfc92a267f6cdc8c943b385d7edc2d8b9181f551c`

Label SHA256:
`9936377336708dbeaf88b7ee83a8ae5fb4272013129041332094dfa625345a9b`

This set is not established here as an RCT corpus, but it is prior project text exposure and therefore belongs in the global provenance ledger.

Status:
`KNOWN_PROJECT_EXPOSURE / CLINICAL_TRIAL_OVERLAP_RELEVANCE_TO_BE_CLASSIFIED`

## 4. Old R4.3 SELECT / historical DEVELOPMENT material

Project continuity records establish:
- old R4.3 SELECT is exposed/closed;
- historical development/test/protected sets are closed;
- old SELECT was explicitly excluded from R44 fresh-internal splitting.

Status:
`KNOWN_EXPOSED / IDENTIFIER_AND_FINGERPRINT_LEDGER_STILL_REQUIRED`

No fresh-acquisition candidate may be certified independent until the custodian can compare against these identities without developer reopening protected content.

## 5. Public/related PICO corpora named by the independent review

The frozen acquisition review requires the exposure inventory to address at least:

- EBM-NLP;
- EBM-NLP_mod;
- PICO-Corpus;
- Alzheimer-disease 150-RCT corpus;
- COVID-19 150-RCT corpus;
- PICO-Corpus/FinePICO-related material;
- FactPICO.

Current status in this inventory:

| Resource | Current project-exposure status | Required before acquisition |
|---|---|---|
| PICO-Corpus | DEFINITE_EXPOSURE_SEPARATE_FROM_R43_R44 | complete PMID/title/text/trial-family ledger |
| FactPICO | DEFINITE_EXPOSURE | connect 115 hashes to all available identifiers/families |
| EBM-NLP | UNRESOLVED_INVENTORY | determine whether raw text/examples were used/viewed |
| EBM-NLP_mod | DEFINITE_R43_R44_EXPOSURE | materialize exposed/protected IDs through custody; propagate aliases into original EBM-NLP and derived corpora |
| AD 150-RCT | UNRESOLVED_INVENTORY | prove use/non-use and freeze identifiers |
| COVID-19 150-RCT | UNRESOLVED_INVENTORY | prove use/non-use and freeze identifiers |
| FinePICO/PICO-Corpus-related material | LITERATURE/METHOD EXPOSURE KNOWN; DATA EXPOSURE UNRESOLVED | distinguish paper/examples from corpus rows |

Any unresolved resource remains a readiness blocker.

## 6. Arabic-track/project material

Known project history includes:
- 41 Arabic Nahw passages;
- 150 Arabic development targets derived from those passages;
- 12 stress cases;
- adjudication queues and Arabic evaluation artifacts.

These are not expected to be clinical RCT sources, but the governing review requires relevant Arabic-project original sources, transformations and translations to be inventoried because translated/paraphrased exposure can defeat literal-only deduplication.

Status:
`KNOWN_NON_RCT_PROJECT_EXPOSURE / CROSS_LANGUAGE_RELEVANCE_REQUIRES_CLASSIFICATION`

## 7. Prompts, attachments, manual examples and literature examples

The independent review explicitly requires inventorying:
- prompts;
- conversation attachments;
- manual examples;
- transformed/translated versions;
- texts encountered in literature/examples during project work.

Repository-only scanning cannot prove completeness for these surfaces.

Status:
`INCOMPLETE_OUTSIDE_REPOSITORY`

Required:
- enumerate project conversation/library attachments relevant to PICO/RCT work;
- hash/canonicalize any RCT abstract or trial-specific example text;
- record PMID/DOI/registry IDs when recoverable;
- keep EVAL developers blind to protected identities.

## 8. Annotation-guideline examples

The new annotation protocol will pin:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO`
annotation guidelines revision:
`bc4b878773192f38b2600ec830ca4208b82f7dc0`

Any concrete RCT snippets/examples appearing in the manual or addendum are prior exposure for annotators/developers and must be included in the provenance ledger when they can map to a trial/report.

Status:
`KNOWN_METHOD_EXPOSURE / EXAMPLE_IDENTITY_EXTRACTION_PENDING`

## 9. Base-model training provenance

Verified frozen encoder:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract`

Revision:
`d673b8835373c6fa116d6d8006b33d48734e305d`

Official Flax SHA256:
`2048c0dca92fe54cf2bec6c36972511ca04e546060307098139b19221dd4e93f`

Revision metadata date:
`2023-11-06T18:04:15.000Z`

The complete pretraining PMID inventory is NOT established.

Status:
`TEMPORAL_SEPARATION_EVIDENCE_PRESENT / EXACT_PRETRAINING_RECORD_PROVENANCE_INCOMPLETE`

A genuinely first-public 2026 result report is temporally separated from this checkpoint, but prior trial-family registrations/preprints/related publications still require screening.

## 10. Current completeness judgment

Repository evidence already proves multiple prior RCT/PICO exposures.

However, the complete governing requirement is NOT yet satisfied because the following remain unresolved:
- exact first-30 R4 diagnostic PMID/fingerprint list in this ledger;
- exact full R44 DESIGN/VERIFY identifier/fingerprint manifest available to the custodian;
- old R4.3 SELECT identities;
- historical DEV/test identifiers;
- EBM-NLP / EBM-NLP_mod exposure status;
- AD/COVID 150-RCT exposure status;
- FinePICO-related row/example exposure;
- prompts/attachments/literature-example text exposure;
- relevant translated/paraphrased RCT exposure;
- complete trial-registration/family aliases;
- exact pretraining record provenance is unavailable.

Therefore:

`PRIOR_EXPOSURE_INVENTORY_NOT_COMPLETE`

and:

`FRESH_RCT_ACQUISITION_REMAINS_BLOCKED`

## 11. Next allowed provenance work

Without opening VERIFY_INTERNAL to developers, allowed next work is:

1. materialize metadata/fingerprints for all unprotected exposed corpora;
2. create protected-custody comparison manifests for protected sets;
3. recover first-30 R4 diagnostic identities from frozen source ordering;
4. enumerate historical SELECT/DEV/test metadata;
5. reconcile EBM-NLP/EBM-NLP_mod/AD/COVID/FinePICO exposure;
6. inventory project attachments/prompts containing identifiable RCT text;
7. map known PMID/DOI/registry IDs into trial-family components;
8. independently review completeness.

No new PubMed retrieval is authorized by this inventory.


## 2026-10-09 lineage correction

Independent federation review identified a material source-attribution error in the previous inventory.

Corrected:
`R43/R44_SOURCE = EBM-NLP_mod fold1/train.txt @ bc4b878773192f38b2600ec830ca4208b82f7dc0`

The earlier attribution of the 320-document R43/R44 lineage to PICO-Corpus is superseded.

PICO-Corpus remains separately exposed for other project experiments and remains TRAIN/DEVELOPMENT only unless a record-specific provenance audit establishes a different role.

This correction changes provenance attribution only.
It does NOT:
- open VERIFY_INTERNAL;
- change R44C results;
- restore any previously exposed record to unseen status;
- certify AD/COVID as independent benchmarks.
