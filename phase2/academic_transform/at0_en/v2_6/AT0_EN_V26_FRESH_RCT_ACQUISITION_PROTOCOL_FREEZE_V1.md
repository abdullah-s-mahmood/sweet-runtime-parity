# ACAD_PASS — Fresh RCT Acquisition Protocol Freeze V1

Date: 2026-10-08

State:
`FRESH_RCT_ACQUISITION_PROTOCOL_FROZEN_PENDING_READINESS`

Acquisition authorization:
`NOT_AUTHORIZED`

Model-development authorization:
`NOT_AUTHORIZED`

VERIFY_INTERNAL:
`CLOSED`

## 1. Governing independent review

The normative acquisition specification is the independently reviewed file:

`FRESH_RCT_INDEPENDENT_ACQUISITION_REVIEW_V1.md`

Archived in this repository at:
`phase2/academic_transform/at0_en/v2_6/FRESH_RCT_INDEPENDENT_ACQUISITION_REVIEW_V1.md`

Independent-review verdict:
`PROCEED_WITH_ACQUISITION_PROTOCOL_CHANGES`

This protocol adopts the review's 40 acquisition decisions **without scientific modification**.

The review authorizes protocol direction conditionally. It does NOT establish readiness to retrieve, sample, annotate, train or evaluate.

## 2. Frozen acquisition frame

PubMed candidate-frame query is exactly:

```text
(
  "randomized controlled trial"[Publication Type]
  OR "controlled clinical trial"[Publication Type]
  OR randomized[Title/Abstract]
  OR randomised[Title/Abstract]
  OR randomly[Title/Abstract]
  OR placebo[Title/Abstract]
)
AND ("2026/01/01"[Date - Publication] : "2026/09/30"[Date - Publication])
AND english[Language]
AND hasabstract
NOT (animals[MeSH Terms] NOT humans[MeSH Terms])
```

Retrieval date field:
`Publication Date [dp]`

Eligibility freshness field:
`EARLIEST_PUBLIC_RESULTS_DATE`

Eligibility temporal window:
`2026-01-01 through 2026-09-30 inclusive`

No hidden PubMed UI filters.

No retrieval may begin until readiness closure.

## 3. Frozen sample allocation

Sampling unit:
confirmed independent trial family.

Sampling:
simple random sampling without replacement after complete screening, provenance exclusion and trial-family deduplication.

Fixed allocation:
- QUALIFICATION: 80 families/documents;
- FRESH_DEV: 400;
- SEALED_FRESH_EVAL: 5,000;
- C-enriched challenge: 0.

Required eligible-family frame:
at least 5,480 families after all exclusions.

If fewer than 5,480 remain:
`STOP_FOR_ACQUISITION_REVIEW`

Do NOT:
- widen dates automatically;
- reduce sample size automatically;
- backfill from old corpora;
- enrich for C;
- reallocate between splits.

## 4. Frozen randomization design

Before retrieval, the independent custodian must generate one 256-bit secret S and publish only its SHA256 commitment.

Family allocation rank:
`HMAC-SHA256(S, UTF8("ACAD_PASS_FRESH2026_V1|allocation|" + canonical_family_id))`

Tie break:
lexical family ID.

Family ID:
lowest numeric PMID in the confirmed trial-family component.

No reseeding.

The secret and complete membership manifests remain outside developer access until the sealed evaluation is consumed.

## 5. Frozen annotation construct

Schema:
`FRESH_PICO_TITLE_METHODS_V1`

Classes:
- P: explicit enrolled/recruited participant descriptions;
- I: assigned experimental treatments/procedures;
- C: explicitly designated reference/control treatments;
- O: measured endpoints/tests used as endpoints.

Primary annotation scope:
`Title + Methods`

Title:
- P/I/C allowed;
- O forbidden in titles.

Full abstract may be retained only as role-disambiguation context.

The exact boundary, overlap, multi-arm, repeated-mention, projection and scope rules in governing review decisions 17–21 are normative and unchanged.

The primary task is supplied-scope extraction.
It MUST NOT be described as end-to-end full-abstract section retrieval.

## 6. Frozen human-gold requirement

Every corpus document requires:
- annotator A: qualified independent human;
- annotator B: qualified independent human;
- adjudicator C: senior independent clinical/evidence-synthesis reviewer.

Required independence:
- A and B blind to each other until lock;
- all annotators blind to model outputs/candidates/confidence;
- EVAL-visible annotation staff cannot later participate in model design/tuning;
- custodian is separate from model development.

Qualification set:
- 40 training/discussion;
- 40 blind qualification.

Qualification requirements per annotator:
- exact typed-span macro F1 >= .85;
- every class F1 >= .80;
- >=10 reference entities/class in blind qualification.

Failure:
`HOLD_ANNOTATION`

No semantic AI prelabels, LLM span suggestions, LLM adjudication or model-based section selection are permitted in independent gold creation.

AI-only gold is NOT an authorized fallback.

## 7. Frozen adjudication and annotation-quality contract

Before adjudication report:
- exact typed-span micro/macro/per-class F1;
- exact boundary-only F1;
- equal-coordinate type disagreements;
- omission/addition counts;
- section-boundary agreement;
- adjudication rates;
- overlap diagnostics with one-to-one character-IoU >= .5.

Main-corpus pre-adjudication quality gate:
- exact typed-span micro F1 >= .85;
- each class F1 >= .80;
- separately on DEV and EVAL;
- zero unresolved adjudication cases after adjudication.

The adjudicator independently annotates a preselected 10% audit:
- DEV: 40 documents;
- EVAL: 500 documents.

IAA/quality failure halts release.
Difficult records are not removed.

## 8. Frozen independence and sealing

Before sampling, perform provenance and overlap checks against every prior ACAD_PASS source.

The exposure inventory must cover:
- all training corpora;
- DESIGN;
- SELECT;
- VERIFY_INTERNAL;
- calibration/diagnostic corpora;
- FactPICO;
- EBM-NLP / EBM-NLP_mod;
- AD/COVID corpora;
- PICO-Corpus / FinePICO-related material;
- prompts and attachments;
- manual examples;
- transformations/translations;
- relevant Arabic-project originals;
- texts encountered during literature/example work.

Protected corpora are compared inside custody via identifiers/fingerprints.
Developers MUST NOT open VERIFY_INTERNAL to deduplicate.

No completeness claim is allowed when prior-corpus provenance is missing.

Trial-family deduplication must include:
- PMID;
- DOI;
- exact/normalized title;
- canonical/normalized abstract fingerprints;
- registry identifiers;
- preprints;
- secondary analyses;
- follow-ups;
- corrections;
- translations;
- shared participants;
- platform/master registrations.

No family may cross QUALIFICATION, DEV, EVAL or prior exposed data.

## 9. Frozen base-model provenance finding

Current verified encoder:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract`

Revision:
`d673b8835373c6fa116d6d8006b33d48734e305d`

Official Flax SHA256:
`2048c0dca92fe54cf2bec6c36972511ca04e546060307098139b19221dd4e93f`

Revision metadata time:
`2023-11-06T18:04:15.000Z`

This supports temporal separation from genuinely new 2026 text but does NOT eliminate trial-family, registry, related-report or other contamination.

Every future base/context/auxiliary checkpoint needs its own provenance audit.

## 10. Frozen post-annotation support floors

FRESH_DEV:
- >=50 primary gold entities/class;
- >=30 trial families/class.

SEALED_FRESH_EVAL:
- >=1,000 primary gold entities/class;
- >=500 trial families/class.

These are feasibility floors only.
They MUST NOT cause backfilling, replacement, enrichment or reallocation.

Support shortfall:
freeze corpus and STOP for review.

## 11. Frozen future evaluation gates

Pooled exact-span point-estimate gates remain:
- per-class precision >= .90;
- macro precision >= .90;
- per-class recall >= .20.

Future confirmatory output additionally requires, per class:
- >=200 accepted distinct spans;
- >=200 contributing trial families.

Trial-balanced confidence estimand is separate from pooled entity precision.

After immutable prediction hashes, but before gold join:
select one accepted span/class/family by the domain-separated HMAC rule:

`ACAD_PASS_FRESH2026_V1|precision-audit|class|family_id|document_id|start|end`

For class c:
- n_c = contributing trial families;
- k_c = exact-correct selected predictions;
- `L_c = BetaQuantile(0.0125; k_c, n_c-k_c+1)`;
- if k_c=0, L_c=0.

Require all:
`L_c >= .90`

This is a simultaneous one-sided Bonferroni-adjusted statement for the **trial-balanced** precision estimand under the specified independent representative trial-family sampling assumption.

It MUST NOT be described as an exact population lower confidence bound for pooled entity-weighted precision.

## 12. Independence-destroying events

Any of the following suspends the fresh-independent claim:
- developer access to EVAL text, IDs, scope maps or labels;
- training/pretraining/calibration/unsupervised adaptation on EVAL;
- model-informed sampling, annotation, exclusions or corrections;
- shared trial families with DEV/prior data;
- reseeding or reallocation;
- label/count-driven backfilling;
- EVAL-driven checkpoint or threshold selection;
- multiple models/operating rules tried on EVAL;
- record-level EVAL feedback to development;
- publishing reconstructable membership before final freeze;
- repeated/rescored/adapted results represented as the first prospective test.

No silent deletion/replacement restores the original independence claim.

## 13. One-way checkpoints

### BEFORE ACQUISITION
Must exist and be frozen:
- this protocol;
- qualified annotation staffing;
- independent custodian;
- funding/resources for the complete fixed corpus;
- prior-exposure inventory;
- access-control plan;
- annotation manual/addendum;
- statistical estimand;
- seed-commitment procedure.

### BEFORE ANNOTATION
Must freeze:
- complete retrieval snapshot;
- raw source hashes;
- screening evidence;
- deduplication/trial-family evidence;
- split/family manifests;
- access controls.

### BEFORE DEVELOPMENT
Must complete:
- qualification;
- independent DEV/EVAL annotation;
- adjudication;
- gold/text hashes;
- quality/support attestations;
- SEALED_FRESH_EVAL custody.

Only FRESH_DEV may then be released under a separately authorized bounded successor-development protocol.

### BEFORE SEALED EVALUATION
Freeze exactly one:
- model procedure;
- weights;
- preprocessing;
- scope contract;
- output schema;
- matcher;
- primary operating rule;
- statistical selection rule;
- runtime/environment;
- one-shot ledger.

### AFTER SEALED EVALUATION
- immutable full-population predictions first;
- deterministic pre-gold precision-audit selection second;
- separately authorized gold join/scoring once;
- freeze result;
- STOP.

## 14. Current readiness state

The independent review explicitly states that the following have NOT yet been demonstrated:
- qualified human annotation resources;
- independent custodian;
- funding/resource capacity;
- complete provenance inventory;
- access-control implementation.

Therefore:

`ACQUISITION_BLOCKED_PENDING_READINESS_ATTESTATION`

No PubMed retrieval, seed generation, family sampling, annotation, model development or VERIFY_INTERNAL access is authorized.

## 15. Exact next authorized work

Allowed now:
1. compile/freeze the prior-exposure provenance inventory;
2. document proposed qualified annotator/adjudicator roles;
3. document independent custodian role and access controls;
4. document resource feasibility for 80+400+5000 documents;
5. archive/pin the annotation manual and prospective addendum;
6. independently audit this readiness package.

Forbidden now:
- PubMed ESearch/EFetch;
- real seed generation;
- split membership generation;
- record sampling;
- annotation;
- model training;
- calibration;
- boundary repair;
- factorization;
- VERIFY_INTERNAL.

Checkpoint:

`PROTOCOL_FROZEN -> READINESS_EVIDENCE_REQUIRED -> ACQUISITION_NOT_YET_AUTHORIZED`
