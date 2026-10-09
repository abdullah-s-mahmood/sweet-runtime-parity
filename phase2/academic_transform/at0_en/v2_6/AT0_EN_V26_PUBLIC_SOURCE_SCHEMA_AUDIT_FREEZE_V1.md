# ACAD_PASS — Public Source Schema Audit Freeze V1

Date: 2026-10-09

State:
`FEDERATION_PUBLIC_SOURCE_SCHEMA_AUDIT_PASS`

Run:
`37884140956`

Artifact:
`11595364822`

Digest:
`sha256:8e3a33499bfdff8b76d8c8a4e4e2272a40ed951985f81403acd39ea4529b1164`

No benchmark metrics were computed.
No raw examples were exported.

## EvidenceOutcomes

500RCT:
- 500 unique PMIDs
- 205,455 token rows
- labels exactly B-Outcome / I-Outcome / O
- malformed rows = 0
- SHA256 `ef1fc6157842c021b24c90b596924a114f97f7ea9ec111d2e4d91884318afc98`

140EBMNLP:
- 140 unique PMIDs
- 50,289 token rows
- labels exactly B-Outcome / I-Outcome / O
- malformed rows = 0
- SHA256 `3693a69ba5ae80ddeaa28cb587dc0d207287635bd56b5fb8c504403a4302df76`

Adapter role:
`OUTCOME_AUXILIARY_ONLY`

Absent labels MUST NOT create negative P/I/C supervision.

## PICO-Corpus

Paired text/annotation documents:
1,011

Native BRAT entity types:
26

Total textbound spans:
17,739

Malformed textbound rows:
0

Adapter role:
`NATIVE_26_TYPE_AUXILIARY_HEAD`

Do NOT flatten into four-class P/I/C/O gold in the first federation campaign.

## TrialSieve

Raw annotation table:
- 175,964 rows
- 1,826 unique PMIDs
- 20 released annotation types

Canonical modeling subset:
`data/processed_for_modeling.json`

Canonical subset:
- 1,609 documents
- 20 span types
- zero zero-span documents
- splits:
  - train 1,148
  - validation 223
  - test 238

Canonical file SHA256:
`376854be993257dacde3abc5c3d53a1d08462b5d954fcbbc568d17905b5d9de5`

All canonical PMIDs are subsets of:
- the raw annotation table;
- the repository text metadata.

Adapter role:
`NATIVE_20_TYPE_AUXILIARY_HEAD`

NonStudyDrug is NOT C.

The 1,826-PMID raw table and 3,167-PMID metadata universe MUST NOT be substituted for the canonical 1,609-document human modeling subset.

## Original EBM-NLP

Pinned archive:
`ebm_nlp_2_00.tar.gz`

The source includes:
- numeric PMID identities;
- token files;
- starting-span annotations;
- hierarchical annotations.

Adapter role:
`NATIVE_P_I_O_AUXILIARY_HEAD`

Do NOT manufacture separate C from original EBM labels.

## Scientific consequence

The audit validates the federation design and blocks invalid label collapses:
- EvidenceOutcomes -> O only;
- TrialSieve -> 20 native types;
- PICO-Corpus -> 26 native types;
- original EBM-NLP -> native P/I/O.

Remaining before source admission:
- explicit license/usage status per source;
- executable adapter synthetic closure;
- cross-source record/family exclusion manifests;
- DISTANT-CTO official weak-data file pin/hash and 11-type audit.

No successor training is authorized.
