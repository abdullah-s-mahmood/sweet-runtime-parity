# ACAD_PASS — Public AD/COVID PMID Custody Audit Freeze V1

Date: 2026-10-09

State:
`FEDERATION_PUBLIC_TARGET_PMID_CUSTODY_AUDIT_PARTIAL_PASS`

Run:
`37881398971`

Artifact:
`11594971856`

Digest:
`sha256:5968ab204711dbe54f10e593339a8408c7fc2d1a160ee2148ec4103e7da7b639`

Custody guarantees:
- no PMID emitted;
- no title emitted;
- no raw text emitted;
- no gold label emitted;
- only aggregate resolution and overlap counts exported.

Resolution rule:
- PubMed ESearch restricted to Title;
- ESummary verification;
- only a unique exact normalized-title match is accepted;
- no fuzzy PMID acceptance.

## AD

Canonical documents:
150

Resolved exact-title PMIDs:
118 / 150 = 78.6666666667%

Official TEST-union documents:
75

Resolved TEST-union PMIDs:
64 / 75 = 85.3333333333%

Duplicate resolved PMID assignments:
0

Within resolved identities, PMID overlap counts were 0 against:
- DESIGN;
- VERIFY_INTERNAL;
- OLD_SELECT;
- PICO-Corpus;
- EvidenceOutcomes 500RCT;
- EvidenceOutcomes 140EBMNLP.

Resolution failures:
- MULTIPLE_EXACT_TITLE: 4
- NO_CANDIDATE: 14
- NO_EXACT_TITLE: 14

## COVID-19

Canonical documents:
150

Resolved exact-title PMIDs:
116 / 150 = 77.3333333333%

Official TEST-union documents:
75

Resolved TEST-union PMIDs:
61 / 75 = 81.3333333333%

Duplicate resolved PMID assignments:
0

Within resolved identities, PMID overlap counts were 0 against:
- DESIGN;
- VERIFY_INTERNAL;
- OLD_SELECT;
- PICO-Corpus;
- EvidenceOutcomes 500RCT;
- EvidenceOutcomes 140EBMNLP.

Resolution failures:
- MULTIPLE_EXACT_TITLE: 3
- NO_CANDIDATE: 14
- NO_EXACT_TITLE: 17

## AD vs COVID

Shared resolved PMID count:
0

## Interpretation

Evidence now agrees across three independent identity layers:

1. exact normalized source-text overlap: 0 against exposed EBM-NLP_mod fold1 TRAIN;
2. visible registry-ID overlap: 0 against DESIGN/VERIFY_INTERNAL/OLD_SELECT;
3. resolved exact-title PMID overlap: 0 in the resolvable portion against DESIGN/VERIFY_INTERNAL/OLD_SELECT/PICO-Corpus/EvidenceOutcomes.

This materially strengthens benchmark provenance.

It does NOT establish:
- PMID identity for unresolved target records;
- PMID identity for every protected EBM-derived record;
- absence of distinct-publication same-trial-family overlap;
- absence of prior prompt/attachment exposure.

Therefore AD/COVID remain:
`BENCHMARK_PROVENANCE_STRONGLY_SUPPORTED_BUT_FAMILY_CLOSURE_INCOMPLETE`

No benchmark metric may be released yet.
