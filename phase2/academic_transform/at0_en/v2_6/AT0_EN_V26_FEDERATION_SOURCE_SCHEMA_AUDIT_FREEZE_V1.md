# ACAD_PASS — Federation Source Schema Audit Freeze V1

Date: 2026-10-09

State:
`FEDERATION_PUBLIC_SOURCE_SCHEMA_AUDIT_PASS`

Canonical run:
`37881568479`

Artifact:
`11595010629`

Digest:
`sha256:a74ee3c8bc87a2f1ab9f15b81ea0c1f65c08245ad0a447daf65499e8d6e5517f`

No benchmark metric was computed.
No raw example was emitted.

## Original EBM-NLP

Revision:
`bepnye/EBM-NLP@43a4a1ea3f0a21cfb8820c040b843dfaf66192d0`

Archive:
`ebm_nlp_2_00.tar.gz`

SHA256:
`b7357503911ba9f708d04e24c1ab3fe9e0a79833910e53e2472ed21214a44e3f`

Documents:
- 4,993 token files;
- 4,993 numeric PMID identities.

Contains:
- starting_spans;
- hierarchical_labels.

First-campaign role:
training-side auxiliary P/I/O only.
Medical-professional test annotations remain reserved.

Repository has no explicit top-level data license detected.
Use is limited to research/citation context; no raw redistribution by ACAD_PASS.

## EvidenceOutcomes

Revision:
`ebmlab/EvidenceOutcomes@bafa355449b6b6feb64f3ca46c1d3268dead13d4`

License:
MIT (repository LICENSE blob `5d7db46bbbcd393c2db7e745d2de4df61262b2ae`).

### 500RCT-CoNLL.tsv

SHA256:
`ef1fc6157842c021b24c90b596924a114f97f7ea9ec111d2e4d91884318afc98`

Rows:
205,455

PMIDs:
500

Columns:
`token, PMID, start, end, label`

Labels:
- B-Outcome
- I-Outcome
- O

Malformed rows:
0

First-campaign role:
`O_AUXILIARY_TRAINING_POOL`

### 140EBMNLP-CoNLL.tsv

SHA256:
`3693a69ba5ae80ddeaa28cb587dc0d207287635bd56b5fb8c504403a4302df76`

Rows:
50,289

PMIDs:
140

Same O-only label set.

First-campaign role:
`RESERVED_NOT_USED`

Reason:
direct parentage from EBM-NLP creates avoidable overlap/provenance complexity with historical exposed/protected EBM-derived records.
No freed data slot may be replaced by another source after result visibility.

## TrialSieve

Revision:
`pathology-dynamics/trialsieve_final@62dd931124e36a8c1d9dc4a2469893553d90d2e4`

License:
CC0 1.0 Universal
LICENSE blob:
`0e259d42c996742e9e3cba14c677129b2c1b6311`

Raw annotation table:
`data/final_schema_data.csv`

SHA256:
`e51c152f4c7eae7bdea8465c6314178b4f7d88db2c638828608ac1329d96ec1b`

Rows:
175,964

Raw-table PMIDs:
1,826

Text metadata:
`data/pmid_title_abstract.csv`

SHA256:
`ec7d0e24d23716802ab4f52d2b8442e3e0e96c82fcafda1b2337ad1c0de2312a`

Unique metadata PMIDs:
3,167

Canonical final modeling file:
`data/processed_for_modeling.json`

SHA256:
`376854be993257dacde3abc5c3d53a1d08462b5d954fcbbc568d17905b5d9de5`

Final documents:
1,609

Final spans:
52,638

Zero-span documents:
0

Native tag count:
20

Native tags:
1. Disease/Condition of Interest
2. Dosage
3. Drug Intervention
4. Follow-up period
5. Group Characteristic
6. Group Name
7. Intervention Administration
8. Intervention Duration
9. Intervention Frequency
10. Non-Pharmaceutical Intervention
11. Non-Study Drug
12. Outcome (Study Endpoint)
13. Quantitative Measurement
14. Sample Size
15. Side Effects
16. Statistical Significance
17. Study Duration
18. Study Years
19. Type of Quant. Measure
20. Units

Stored source split counts:
- train 1,148
- validation 223
- test 238

These stored split labels are NOT used by ACAD_PASS because they were generated through the upstream random splitting path and TrialSieve is auxiliary-only in the first campaign.

ACAD_PASS candidate pool:
all 1,609 final documents before ACAD_PASS trial-family/provenance exclusions.

No TrialSieve tag is mapped to native P/I/C/O.

## PICO-Corpus

Revision:
`sociocom/PICO-Corpus@482b7d8f135fe6ea424961c2812e8d214c3f4a5f`

Files:
- 1,011 .txt
- 1,011 .ann
- 1,011 paired PMIDs
- no unmatched txt/ann files
- no malformed text-bound annotation rows.

Native text-bound spans:
17,739

Native entity types:
26

Types are frozen lexicographically from the source:
- age
- condition
- control
- control-participants
- cv-bin-abs
- cv-bin-percent
- cv-cont-mean
- cv-cont-median
- cv-cont-q1
- cv-cont-q3
- cv-cont-sd
- eligibility
- ethinicity
- intervention
- intervention-participants
- iv-bin-abs
- iv-bin-percent
- iv-cont-mean
- iv-cont-median
- iv-cont-q1
- iv-cont-q3
- iv-cont-sd
- location
- outcome
- outcome-Measure
- total-participants

Important:
the released type string `ethinicity` and case-sensitive `outcome-Measure` are preserved exactly; no silent correction.

Repository/paper make the corpus publicly available for research, but no explicit repository license was found during this audit.

First-campaign policy:
- research use only;
- citation required;
- do not redistribute raw corpus in ACAD_PASS artifacts;
- one auxiliary channel per native released type;
- no collapse to native four-class P/I/C/O;
- records remain TRAIN/DEVELOPMENT only because project exposure is definite.

## DISTANT-CTO

First-campaign D5 source is NOT the GitHub dummy link.

Official dataset:
Zenodo record `10.5281/zenodo.6497284`, version 1.0, 2022-04-27.

Weak file:
`extraction1_pos_posnegtrail_conf09.txt`

Size:
~360.2 MB

Zenodo MD5:
`e95e3984a9b46e340b90aeed262e12cc`

Status:
`METADATA_PINNED / FULL_FILE_SHA256_AND_ADAPTER_PREFLIGHT_PENDING`

Semantic role:
11-way weak intervention subtype auxiliary head only.
No direct I/C role label.

## Admission summary

Admitted subject to family-exclusion manifests:
- EBM-NLP training starting-spans P/I/O auxiliary
- TrialSieve final 1,609-doc 20-type auxiliary
- EvidenceOutcomes 500RCT O auxiliary
- PICO-Corpus 26-type auxiliary
- DISTANT-CTO only D5 weak semantic-type stream after file/admission closure

Reserved/not used:
- EBM-NLP medical-professional test
- EvidenceOutcomes 140EBMNLP
- TrialSieve upstream random split semantics
- C-TrO first campaign
- FinePICO labels
- LLM/pseudo labels
