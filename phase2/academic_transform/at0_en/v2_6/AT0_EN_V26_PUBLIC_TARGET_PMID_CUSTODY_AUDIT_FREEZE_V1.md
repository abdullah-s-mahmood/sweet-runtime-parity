# ACAD_PASS — Public Target PMID Custody Audit Freeze V1

Date: 2026-10-09

State:
`FEDERATION_PUBLIC_TARGET_PMID_CUSTODY_AUDIT_PASS_WITH_PARTIAL_RESOLUTION`

Run:
`37881398971`

Artifact:
`11594971856`

Digest:
`sha256:5968ab204711dbe54f10e593339a8408c7fc2d1a160ee2148ec4103e7da7b639`

No PMIDs, titles, raw text or gold labels were emitted.

## AD
- canonical documents: 150
- exact normalized PubMed-title PMID resolutions: 118/150 = 78.6666666667%
- official TEST union: 75
- resolved TEST PMIDs: 64/75 = 85.3333333333%
- duplicate resolved PMID assignments: 0
- shared PMID count against DESIGN / VERIFY_INTERNAL / OLD_SELECT / PICO-Corpus / EvidenceOutcomes 140 / EvidenceOutcomes 500: all 0

## COVID-19
- canonical documents: 150
- exact normalized PubMed-title PMID resolutions: 116/150 = 77.3333333333%
- official TEST union: 75
- resolved TEST PMIDs: 61/75 = 81.3333333333%
- duplicate resolved PMID assignments: 0
- shared PMID count against DESIGN / VERIFY_INTERNAL / OLD_SELECT / PICO-Corpus / EvidenceOutcomes 140 / EvidenceOutcomes 500: all 0

## Cross-target
Resolved AD vs COVID shared PMID count: 0

## Interpretation
Among records whose PubMed identity was resolved conservatively by exact normalized title, no same-PMID contamination was observed against the checked exposed/protected resources.

Unresolved titles remain unresolved.
Same PMID is weaker than same trial-family.
Protected historical PMID mapping remains partial.

Therefore:
`SAME_PMID_CONTAMINATION_NOT_OBSERVED_ON_RESOLVED_SUBSET`

but not:
`TRIAL_FAMILY_INDEPENDENCE_FULLY_PROVEN`.

No scientific fit is authorized by this audit.
