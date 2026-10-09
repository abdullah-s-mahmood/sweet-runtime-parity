# ACAD_PASS — Public Benchmark PubMed DOI/Registry Custody Freeze V1

Date: 2026-10-09

State:
`FEDERATION_PUBMED_DOI_REGISTRY_CUSTODY_AUDIT_PASS_WITH_UNRESOLVED_RECORDS`

Run:
`37886862460`

Artifact:
`11596787832`

Digest:
`sha256:1242a4b5794fdfb4298de85b4f8517e239fd2e1db989ffbee103a65d306ec7ff`

No PMIDs, DOIs, registry IDs, titles, raw text or gold labels were emitted.

## AD

Canonical documents:
150

Resolved unique-exact-title PubMed records:
116

Unresolved:
34

Official TEST documents:
75

Resolved TEST PMIDs:
62

Unique resolved DOIs:
107 overall / 58 TEST

Unique registry IDs found in PubMed record:
31 overall / 16 TEST

Compared against mapped historical:
- DESIGN: 250 PubMed records
- VERIFY_INTERNAL: 49
- OLD_SELECT: 60

Shared DOI count:
0 for whole corpus and TEST against every historical role.

Shared registry-ID count:
0 for whole corpus and TEST against every historical role.

## COVID-19

Canonical documents:
150

Resolved unique-exact-title PubMed records:
114

Unresolved:
36

Official TEST documents:
75

Resolved TEST PMIDs:
60

Unique resolved DOIs:
114 overall / 60 TEST

Unique registry IDs:
73 overall / 37 TEST

Shared DOI count against DESIGN / VERIFY_INTERNAL / OLD_SELECT:
0

Shared registry-ID count against DESIGN / VERIFY_INTERNAL / OLD_SELECT:
0

## Interpretation

This adds publication-identity and registry-family evidence to the earlier:
- exact text audit;
- target PMID audit;
- protected in-text registry audit.

No resolved collision has been observed between AD/COVID and the mapped historical ACAD_PASS EBM-NLP_mod roles.

However:
- 34 AD and 36 COVID records remain unresolved by the exact-title PubMed resolver;
- DOI identity alone does not detect all multiple-publication reports of one trial;
- historical protected PMID coverage is partial.

Therefore:
`NO_RESOLVED_CONTAMINATION_FOUND`

but not:
`COMPLETE_TRIAL_FAMILY_INDEPENDENCE_PROVEN`.

Unresolved records must remain conservative in per-fit decontamination and claim language.
