# ACAD_PASS — SURUS Schema/Coordinate Audit Attempt 1 Freeze V1

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

Run:
`37914385700`

Workflow:
`Federation SURUS public schema audit`

Trigger head:
`14f92084bf18570765d51298179c8a4581fcdc44`

Conclusion:
`FAIL`

Classification:
`MECHANICAL_PREFLIGHT_FAIL / NO_SCIENTIFIC_ATTEMPT_CONSUMED`

No model training, protected benchmark scoring, VERIFY_INTERNAL access, AD/COVID scoring, or scientific attempt occurred.

## What improved

The corrected audit repaired the prior ontology-keying defect:

- released LabelID count = 25;
- released ClassID count = 7;
- ontology identity is now `(source_commit, released_LabelID)`;
- repeated names across classes are preserved as distinct channels;
- numeric character coordinates were valid;
- token index numeric invariants were valid;
- article and label foreign-key misses = 0;
- release/publication annotation discrepancy explicitly recorded as 705 rows.

The previous name-keyed corruption is no longer accepted as ontology evidence.

## Exact coordinate finding

Released annotation rows:
`48,833`

Exact candidate coordinate matches:
- `Abstract:half_open = 44,643`
- `Abstract:inclusive_end = 1`
- `Title:half_open = 14`
- `Title:inclusive_end = 0`

No single released Title/Abstract coordinate model explains all 48,833 rows.

Therefore:
`coordinate_roundtrip_certified = false`

The audit correctly failed closed.

## Important interpretation

This is not a scientific failure and does not consume a development attempt.

The 4,190 rows not explained by exact Abstract half-open slicing MUST NOT be silently:
- dropped;
- snapped;
- normalized into apparent agreement;
- treated as valid positives;
- used in training.

The next operation is a read-only mismatch-mechanism diagnostic that emits only aggregate counts/hashes and no raw article text, PMID values, protected identities, or model metrics.

## Next authorized operation

`SURUS_COORDINATE_MISMATCH_MECHANISM_DIAGNOSTIC`

The diagnostic should distinguish at minimum:
- exact annotation text occurrence elsewhere in the released Abstract;
- unique vs multiple occurrences;
- offset delta distributions;
- Title-vs-Abstract scope;
- whitespace/Unicode/HTML-normalization-only differences;
- source-text serialization ambiguity;
- duplicate annotation behavior;
- any relation between mismatch and Dataset/EvalType/LabelID.

No adapter closure until the coordinate mechanism is prospectively resolved.
