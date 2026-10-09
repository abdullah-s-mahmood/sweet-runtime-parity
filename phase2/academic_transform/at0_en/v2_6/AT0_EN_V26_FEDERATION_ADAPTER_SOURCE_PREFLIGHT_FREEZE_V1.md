# ACAD_PASS — Federation Adapter Source Preflight Freeze V1

Date: 2026-10-09

State:
`FEDERATION_ADAPTER_SOURCE_PREFLIGHT_PASS`

Run:
`37881966232`

Artifact:
`11594457041`

Digest:
`sha256:156a8ccd6471a410bdc7dd230d98575f3f5fc6fca015d1041fb52adbdc2b804f`

Scientific training:
`FALSE`

Benchmark metrics:
`FALSE`

Auxiliary-to-native P/I/C/O conversion:
`FALSE`

## Native EBM-NLP_mod

Documents:
400

Observed label inventory exactly:
- B-P / I-P
- B-I / I-I
- B-C / I-C
- B-O / I-O
- O

Invalid/example-initial I observations under the source-compatible parser:
104

These are flagged by contract and are not silently promoted to new B entities.

## TrialSieve

Documents:
1609

Unique PMIDs:
1609

Spans:
52638

Native tag inventory:
exactly 20, matching the frozen schema.

All coordinates passed structural validation.

No native P/I/C/O labels are emitted.

## EvidenceOutcomes 500RCT

Verified:
- 500 PMIDs;
- labels exactly B-Outcome / I-Outcome / O;
- zero malformed rows;
- valid integer offsets.

Role:
O-only auxiliary head.

## PICO-Corpus

Verified:
- 1011 documents;
- 17739 text-bound spans;
- exact 26-type native ontology;
- source type spelling/case preserved.

No native four-class collapse.

## Original EBM-NLP

The released training-side starting-span annotation structure for:
- participants;
- interventions;
- outcomes

is present and admitted only as auxiliary training structure.

Medical-professional TEST material is present but explicitly excluded from first-campaign training.

## Synthetic semantic contract

Verified:
- source-compatible native spans start at B tags;
- standalone invalid I is flagged;
- forbidden conversions such as Non-Study Drug->C, control->C, Drug Intervention->I, TrialSieve Outcome->native O are not implemented.

## Conclusion

The A1-A5 source adapters are structurally ready subject to per-fit family-decontamination manifests.

A6 DISTANT-CTO remains pending the official full weak-file download/hash/schema preflight.

Status:
`NATIVE_AND_HUMAN_AUX_ADAPTERS_PASS / D5_WEAK_ADAPTER_PENDING`
