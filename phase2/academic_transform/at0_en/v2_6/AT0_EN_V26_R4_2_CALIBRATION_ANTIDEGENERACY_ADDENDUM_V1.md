# AT0-EN V2.6 R4.2 — Calibration Anti-Degeneracy Addendum V1

Date: 2026-10-05
Status: FROZEN BEFORE TRAINING / INFERENCE

This addendum tightens the R4.2 calibration rule before any model inference.

## Entity confidence

For each predicted BIO entity span:
- reconstruct the entity from first-subtoken word predictions;
- entity confidence = MINIMUM softmax probability among all words in that predicted entity.

Rationale:
a multi-token entity is only as reliable as its weakest included token; this is conservative and deterministic.

## Exact entity matching

A predicted entity is correct only if:
- class P/I/O matches gold;
- start word index matches exactly;
- end word index matches exactly.

No partial-overlap credit is used for calibration threshold selection.

## Frozen candidate thresholds

`{0.80, 0.85, 0.90, 0.95}`

Choose the LOWEST threshold satisfying ALL:

1. precision >= 0.90 for each P, I, O;
2. no class precision < 0.85;
3. recall >= 0.20 for each P, I, O;
4. at least 10 accepted predicted entities in each P, I, O;
5. macro precision >= 0.90.

If no threshold satisfies all five:
`R4_2_WITNESS_NOT_READY`

No test set may be inspected to alter these rules.

## Test reporting

After threshold freeze, report both:
- raw argmax entity metrics;
- thresholded witness metrics and abstention/coverage.

The threshold is a witness-evidence threshold only.
It is NOT a PASS_CANDIDATE threshold and cannot override deterministic contradictions.
