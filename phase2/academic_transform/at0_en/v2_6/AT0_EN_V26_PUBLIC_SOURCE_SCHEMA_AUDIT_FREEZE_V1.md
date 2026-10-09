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

No benchmark metric was computed and no raw examples were emitted.

## EvidenceOutcomes
Released CoNLL files are headerless: token, PMID, start, end, label.

500RCT:
- rows 205455
- unique PMIDs 500
- labels B-Outcome / I-Outcome / O
- malformed rows 0
- SHA256 ef1fc6157842c021b24c90b596924a114f97f7ea9ec111d2e4d91884318afc98

140EBMNLP:
- rows 50289
- unique PMIDs 140
- labels B-Outcome / I-Outcome / O
- malformed rows 0
- SHA256 3693a69ba5ae80ddeaa28cb587dc0d207287635bd56b5fb8c504403a4302df76

Role:
`OUTCOME_AUXILIARY_HUMAN_GOLD_ONLY`

## PICO-Corpus
- 1011 annotation files
- 1011 text files
- 1011 paired PMIDs
- 17739 text-bound spans
- 26 native entity types
- malformed text-bound rows 0

Role:
`NATIVE_ONTOLOGY_AUXILIARY_HEAD / TRAIN_DEVELOPMENT_ONLY`

No forced 26->P/I/C/O collapse.

## TrialSieve
Raw annotation table:
- 175964 rows
- 1826 unique PMIDs
- 20 released tags

Canonical processed modeling set:
- 1609 documents / unique PMIDs
- train 1148
- validation 223
- test 238
- zero-span documents 0
- all 20 tags represented

Authorized first-campaign source:
`processed_for_modeling.json` 1609-document set only.

Role:
`20_TYPE_AUXILIARY_HUMAN_GOLD_HEAD`

No automatic native P/I/C/O mapping.

## Original EBM-NLP
Role:
`P/I/O_AUXILIARY_HEAD_ON_AUTHORIZED_TRAINING_PARTITION_ONLY`

No automatic separate-C mapping.

## Adapter implications
- EBM-NLPmod/AD/COVID -> native P/I/C/O
- EBM-NLP -> auxiliary P/I/O
- TrialSieve -> auxiliary 20 types
- EvidenceOutcomes -> auxiliary Outcome only
- PICO-Corpus -> auxiliary native 26-type ontology
- DISTANT-CTO -> weak semantic intervention-type only

No scientific fit is authorized until adapter synthetic closure passes.
