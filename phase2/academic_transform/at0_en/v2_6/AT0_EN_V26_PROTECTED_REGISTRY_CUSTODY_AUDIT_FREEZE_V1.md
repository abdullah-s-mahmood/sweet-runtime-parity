# ACAD_PASS — Protected Registry Custody Audit Freeze V1

Date: 2026-10-09

State:
`FEDERATION_PROTECTED_REGISTRY_CUSTODY_AUDIT_PASS_WITH_LIMITED_COVERAGE`

Canonical run:
`37880937020`

Artifact:
`11594715629`

Digest:
`sha256:3759163014b2214ff5bc8d4792835d0e0583b8102a3654e51d7c825f776f074f`

R44 manifest:
`799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`

Privacy/custody guarantees:
- no protected registry ID emitted;
- no protected raw text emitted;
- no gold labels emitted;
- only aggregate counts/digests exported.

Canonicalization:
NFC + whitespace-collapsed text fingerprinting aligned with the prior public split audit.

## Findings

For every comparison between each protected/exposed historical partition:
- DESIGN (256 docs)
- VERIFY_INTERNAL (64 docs)
- OLD_SELECT (80 docs)

and each public target:
- AD whole 150
- AD official TEST union 75
- COVID whole 150
- COVID official TEST union 75

the number of shared registry identifiers visible in source text was:
`0`.

Observed registry-ID coverage:
- DESIGN: 2/256 documents with visible registry IDs; 2 unique IDs.
- VERIFY_INTERNAL: 2/64 documents; 2 unique IDs.
- OLD_SELECT: 2/80 documents; 2 unique IDs.
- AD whole: 3/150 documents; 5 unique IDs.
- AD TEST union: 1/75 documents; 2 unique IDs.
- COVID whole: 24/150 documents; 23 unique IDs.
- COVID TEST union: 12/75 documents; 11 unique IDs.

## Interpretation

Positive:
no registry-identity collision was found, including against protected VERIFY_INTERNAL, without exposing protected identities.

Limitation:
coverage is too sparse to certify different trial families for all records.

Therefore:
`REGISTRY_LEVEL_CONTAMINATION_NOT_OBSERVED`

but NOT:
`TRIAL_FAMILY_INDEPENDENCE_PROVEN`.

Required next:
PMID/DOI/title/family mapping or equivalent protected-custody provenance closure.

VERIFY_INTERNAL remains closed.
No scientific training is authorized.
