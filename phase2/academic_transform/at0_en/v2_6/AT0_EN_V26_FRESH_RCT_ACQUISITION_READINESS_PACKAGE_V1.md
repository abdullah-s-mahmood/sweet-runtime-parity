# ACAD_PASS — Fresh RCT Acquisition Readiness Package V1

Date: 2026-10-08

Overall state:
`PROTOCOL_AND_SYNTHETIC_TOOLING_READY / HUMAN_CUSTODY_PROVENANCE_READINESS_INCOMPLETE / ACQUISITION_BLOCKED`

No new RCT records have been retrieved, sampled, annotated or scored.

No model has been run.

VERIFY_INTERNAL remains closed.

## 1. Independent review

File:
`FRESH_RCT_INDEPENDENT_ACQUISITION_REVIEW_V1.md`

Archived commit:
`a39e42faeafc44dcb5c78bc01fc4d008a60fa60b`

Review verdict:
`PROCEED_WITH_ACQUISITION_PROTOCOL_CHANGES`

Core condition:
protocol direction accepted, but retrieval must wait for:
- qualified human annotation resources;
- independent custodian;
- funding/resource feasibility;
- prior-exposure inventory;
- access controls.

## 2. Frozen acquisition protocol

File:
`AT0_EN_V26_FRESH_RCT_ACQUISITION_PROTOCOL_FREEZE_V1.md`

Commit:
`5a98ad9e7723b457144bda4e3c47bc0332b45861`

State:
`FRESH_RCT_ACQUISITION_PROTOCOL_FROZEN_PENDING_READINESS`

Frozen allocation:
- 80 QUALIFICATION;
- 400 FRESH_DEV;
- 5,000 SEALED_FRESH_EVAL;
- no C-enriched stratum.

Live acquisition:
`NOT_AUTHORIZED`

## 3. Readiness ledger

File:
`AT0_EN_V26_FRESH_RCT_ACQUISITION_READINESS_LEDGER_V1.md`

Latest readiness update commit:
`35f4dc1783c92368f0535ced9acb627fd998f7e5`

State:
`READINESS_INCOMPLETE_ACQUISITION_BLOCKED`

## 4. Prior-exposure inventory

File:
`AT0_EN_V26_FRESH_RCT_PRIOR_EXPOSURE_INVENTORY_V1.md`

Commit:
`0b4641100462bd646731a465acc445a7b0bd61da`

State:
`PARTIAL_PROVENANCE_INVENTORY_INCOMPLETE`

Already evidenced:
- PICO-Corpus definite prior exposure;
- 60-RCT internal holdout exact frozen manifest;
- R44 320-document source-compatible inventory with 256 DESIGN / 64 protected VERIFY_INTERNAL;
- FactPICO 345 records / 115 source clusters;
- FactPICO source-cluster hashes;
- V2.3 second unseen holdout exposure;
- historical SELECT/project exposure;
- Arabic/project exposure categories.

Still unresolved:
- complete first-30 R4 identity ledger;
- full protected-custody R44 identity/fingerprint manifest;
- old SELECT/historical DEV/test identities;
- EBM-NLP / EBM-NLP_mod exposure;
- AD/COVID 150-RCT exposure;
- FinePICO-related row/example exposure;
- prompt/attachment/literature-example exposure;
- cross-language/transformed RCT exposure;
- trial-family alias completeness.

## 5. Annotation contract

File:
`AT0_EN_V26_FRESH_RCT_ANNOTATION_ADDENDUM_V1.md`

Commit:
`26cd1573a1fc410f1209d1a5f5c38dec5ac54ce4`

Pinned source manual:
- repo `BIDS-Xu-Lab/section_specific_annotation_of_PICO`;
- commit `bc4b878773192f38b2600ec830ca4208b82f7dc0`;
- manual blob `f67df5da9507c562cbeab7ad497e816bde58a02a`;
- size `204547` bytes.

State:
annotation rules frozen for readiness only.
No real annotation authorized.

## 6. Statistical synthetic preflight

File:
`AT0_EN_V26_FRESH_RCT_STATS_SYNTHETIC_PREFLIGHT_FREEZE_V1.md`

Commit:
`df353430257610eb71c8cf9b1a94312feb520a24`

Run:
`37828307955`

Artifact:
`11572557395`

Digest:
`sha256:f9f8f5cd80b0936f8183aacfe008525949428a1f5b310f401c6b233838668926`

State:
`PASS`

Verified without EVAL:
- 95/100 -> lower bound 0.8772335911610268;
- 190/200 -> 0.9037442005509154;
- 475/500 -> 0.9235837897122915;
- selection label-blind;
- selection confidence-blind;
- HMAC-domain-separated;
- >=200-family support gate;
- trial-balanced estimand warning preserved.

## 7. Acquisition-tooling synthetic preflight

File:
`AT0_EN_V26_FRESH_RCT_ACQUISITION_TOOLING_SYNTHETIC_PREFLIGHT_FREEZE_V1.md`

Commit:
`42af7497a94f8026e7e2613a94318c05ab416deb`

Run:
`37828800778`

Artifact:
`11572806239`

Digest:
`sha256:c5bf089d064987692fa4b8780252c7e6283531a47b0dc47a71f19b0a8be36dbc`

State:
`PASS`

Verified synthetically:
- frozen query byte identity;
- incomplete pagination fail-closed;
- duplicate PMID fail-closed;
- partition reconciliation;
- exact PMID/DOI/title triggers;
- title Levenshtein >=.90 trigger;
- abstract 5-gram Jaccard >=.80 trigger;
- abstract 5-gram containment >=.90 trigger;
- registry-ID trigger;
- unrelated negative fixture;
- no PubMed contact.

## 8. Remaining hard blockers

### Human annotation staffing
Need evidence of:
- annotator A qualification;
- annotator B qualification;
- senior adjudicator qualification.

Current:
`NOT_ESTABLISHED`

### Independent custody
Need:
- custodian separate from model development;
- custody of allocation secret;
- custody of split membership;
- custody of SEALED_FRESH_EVAL text/IDs/labels/scope/derived representations;
- protected-corpus duplicate checking without developer exposure.

Current:
`NOT_ESTABLISHED`

### Resource feasibility
Need documented capacity for:
- 80 qualification;
- 400 DEV;
- 5,000 EVAL;
- dual independent annotation;
- 10% adjudicator independent audit;
- full disagreement/completeness adjudication.

Current:
`NOT_ESTABLISHED`

### Provenance completeness
Current inventory is partial.

Current:
`INCOMPLETE`

### Access-control implementation
Need auditable separation between:
- developer environment;
- custodian/annotation environment;
- SEALED_FRESH_EVAL.

Current:
`NOT_ESTABLISHED`

### Manual binary archival
Pinned upstream commit/blob exists.
Local immutable binary copy/hash still pending.

Current:
`PARTIAL`

## 9. What is already safe to continue

Allowed:
- provenance inventory completion from existing project evidence;
- protected-custody metadata design;
- staffing/custody documentation;
- access-control architecture;
- resource-budget/workload analysis;
- local archival of pinned annotation manual;
- synthetic-only tooling hardening;
- independent review of this package.

Not allowed:
- live PubMed search/retrieval;
- actual allocation seed;
- split membership;
- real RCT annotation;
- model adaptation;
- VERIFY_INTERNAL.

## 10. Next checkpoint

Before any retrieval, require a new explicit file:

`AT0_EN_V26_FRESH_RCT_ACQUISITION_READINESS_CLOSURE_V1.md`

It may be created only after every BEFORE_ACQUISITION blocker is evidenced and independently reviewed.

Until then:

`NO_ACQUISITION`
