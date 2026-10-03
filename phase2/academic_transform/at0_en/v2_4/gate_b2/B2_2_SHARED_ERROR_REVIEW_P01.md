# AT0-EN V2.4 B2.2 — Shared-Error Safeguard Review: B1-P01

Date: 2026-10-03
Status: REVIEW CLOSED / NO SHARED SEMANTIC ERROR OBSERVED / NO REPAIR

## Trigger

B2.2 revalidation produced:
- GG = 100%
- GE = 91.67%
- EG = 91.67%
- EE = 100%

Both GE and EG missed only B1-P01 while EE passed it.

The higher-model safeguard explicitly required review when EE succeeds while one or both mixed arms degrade.

## Finding

The mismatch is representational, not semantic.

The frozen B2 raw-text derivation concatenates:
1. assertion evidence;
2. relation evidence.

For B1-P01, the source/candidate gold graphs contain:
- one critical assertion expressing the distinct-mechanism limitation;
- one critical DISTINCT_FROM relation with evidence:
  `The findings concern different subsystems.`

Because this relation evidence is appended as a standalone sentence in the B2 raw fixture, the relation-aware extractor legitimately emits:
- the critical DISTINCT_FROM assertion;
- the critical DISTINCT_FROM relation;
- an additional MATERIAL assertion:
  `The findings CONCERN different subsystems.`

This extra MATERIAL assertion is:
- directly supported by exact text;
- semantically compatible with the gold relation;
- present symmetrically on source and candidate extracted graphs;
- not a hidden omission;
- not an unsupported addition;
- not a critical uncertainty promotion.

The human-correct gold graph represents the same material only as a relation/evidence trace, not as an additional assertion.

Thus:
- EE passes because both extracted sides use the same defensible redundant representation;
- GE/EG fail because the frozen aligner groups unequal assertion counts and the gold side lacks that redundant MATERIAL assertion.

## Decision

Classification:
`CANONICALIZATION_FIXTURE_MISMATCH / NOT_SHARED_SEMANTIC_ERROR`

No extractor repair is authorized.

No aligner repair is authorized.

No fixture rewrite is authorized.

Reason:
changing the extractor or fixture now specifically to make GE/EG reach 100% would risk consumed-case overfitting and would not improve scientific meaning preservation.

## Safety interpretation

The B2.2 representation audit remains clean:
- 24 sides audited
- 102 checks
- 0 failures

B1-P01 critical assertions and critical relations are preserved in EE with exact evidence support.

This review does NOT establish generalization.
It only resolves the specific shared-error safeguard triggered by the mixed-arm discrepancy.

## Consequence

The frozen B2.2 progression result remains:
`PASS_B2_EXTRACTED_DEVELOPMENT`

The mixed-arm discrepancy must remain visible in all reporting:
- GE = 91.67%
- EG = 91.67%
- EE = 100%

Do not rewrite these to 100%.

Proceed only to pipeline freeze / Gate C preparation.
