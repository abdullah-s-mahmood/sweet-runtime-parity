# ACAD_PASS — Federation Pre-Fit Preflight Freeze V1

Date: 2026-10-09

State:
`FEDERATION_PREFIT_WINDOWING_AND_PUBLIC_SPLIT_AUDIT_PASS`

Scientific training:
`NOT_STARTED`

VERIFY_INTERNAL:
`CLOSED`

Official workflow:
- run `37879437844`
- conclusion `SUCCESS`

## 1. Gold-independent windowing synthetic closure

Artifact:
- ID `11594086484`
- digest `sha256:22f09221c98e374bc20d035c6e4cce5ecf0328d7381ef86c394ea2652efbff0a`

State:
`FEDERATION_TEXT_ONLY_WINDOWING_SYNTHETIC_PREFLIGHT_PASS`

Verified:
- planning consumes only text-derived piece counts;
- gold labels are not inputs;
- deterministic windows;
- complete source-word coverage;
- tokenizer-empty source word cannot be silently dropped;
- caller must substitute explicit UNK representation;
- oversized single word fails closed;
- deterministic occurrence selection under overlapping windows.

This closes the synthetic mechanics of F03.

It does NOT yet certify:
- actual pinned tokenizer integration;
- actual BiomedBERT/ModernBERT source files;
- end-to-end offset reconstruction on all corpora.

Those remain pre-fit closure work.

## 2. Aggregate-only public split text-fingerprint audit

Artifact:
- ID `11594006897`
- digest `sha256:a7cc367fdb669d9a01c4575133dbf8dcfcf2d2b0eff22c614bfbd68278120510`

State:
`FEDERATION_PUBLIC_SPLIT_TEXT_FINGERPRINT_AUDIT_PASS`

Source:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO@bc4b878773192f38b2600ec830ca4208b82f7dc0`

Fingerprint:
NFC + whitespace-collapsed source token column only.

Annotation columns were ignored for fingerprints.

No raw benchmark text or gold labels are present in the released aggregate artifact.

### AD

Whole corpus:
- 150 unique text documents.

Every fold:
- TRAIN = 120 unique;
- DEV = 15 unique;
- TEST = 15 unique;
- within-fold TRAIN/DEV overlap = 0;
- within-fold TRAIN/TEST overlap = 0;
- within-fold DEV/TEST overlap = 0.

Across five TEST files:
- sum test appearances = 75;
- unique test documents = 75;
- pairwise overlap across distinct test folds = 0.

Whole-corpus membership digest:
`3a16e36ed71e2274889038b5f18dfcebe4f16b629b3a2b6079968ebdcc6cb743`

Five-test-union digest:
`59410826998efa9519e72d17f0c7b44a1066958134047c7b86f5422b83422234`

Exact text overlap with exposed EBM-NLP_mod fold1 TRAIN:
- whole AD corpus = 0;
- union of AD official TEST documents = 0.

### COVID-19

Whole corpus:
- 150 unique text documents.

Every fold:
- TRAIN = 120 unique;
- DEV = 15 unique;
- TEST = 15 unique;
- within-fold TRAIN/DEV overlap = 0;
- within-fold TRAIN/TEST overlap = 0;
- within-fold DEV/TEST overlap = 0.

Across five TEST files:
- sum test appearances = 75;
- unique test documents = 75;
- pairwise overlap across distinct test folds = 0.

Whole-corpus membership digest:
`1221157e799b414826cc92851b3907d511454b195c1fc395f6a863061191c606`

Five-test-union digest:
`087759211a78e2d2ec9ab5e5d62cfce12eb4b07336ab1578a1b453604c5cad0e`

Exact text overlap with exposed EBM-NLP_mod fold1 TRAIN:
- whole COVID corpus = 0;
- union of COVID official TEST documents = 0.

### AD versus COVID

Exact normalized text overlap between the two full 150-document corpora:
`0`

## 3. What this DOES establish

- official file identity is pinned;
- each released fold is internally text-disjoint;
- the five official test subsets are text-disjoint within each corpus;
- AD and COVID are text-disjoint from each other under exact normalized-text fingerprinting;
- neither corpus exactly matches exposed EBM-NLP_mod fold1 TRAIN text.

## 4. What this DOES NOT establish

It does NOT prove:
- different publications are different randomized trial families;
- no shared registry/trial exists under different text;
- no prior project attachment/prompt exposed an AD/COVID record;
- no protected VERIFY_INTERNAL alias exists;
- no base-model pretraining exposure;
- benchmark independence is certified.

Therefore F04 remains:
`PARTIAL_PASS / TRIAL_FAMILY_AND_PRIOR_EXPOSURE_CUSTODY_AUDIT_PENDING`

AD/COVID remain:
`CANDIDATE_BENCHMARKS_NOT_YET_AUTHORIZED_FOR_SCORING`

## 5. Next

1. source/ontology/license/file manifest closure;
2. noninteractive PMID/DOI/registry/trial-family alias audit;
3. adapters synthetic closure;
4. exact scorer synthetic closure;
5. PICOX comparator recipe closure;
6. runtime/hardware closure;
7. immutable 54-fit attempt manifest;
8. final independent pre-fit closure review.

No scientific model fit is authorized by this PASS.
