# ACAD_PASS — AT0-EN V2.5 Scalable-Matcher Regression + Runtime Freeze V1

Date: 2026-10-05
Status: PASS / FROZEN FOR PRE-PREDICTION REVIEW / NO FACTPICO EXECUTION

Parent:
`AT0-EN V2.4`

Reason:
canonical V2.4 B1.1 factorial matcher failed synthetic scalability preflight before any FactPICO prediction.

Higher-model decision:
`B. VERSION_BUMP_BEFORE_FACTPICO`

Decision file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_4_SCALABILITY_HIGHER_MODEL_DECISION_V1.md`

## 1. Runtime identity

Runtime:
`AT0-EN V2.5`

Freeze branch:
`phase2-arabic-eval`

Freeze execution commit / workflow head SHA:
`05e200461c1067c120e73acf4a6055383eb350b2`

GitHub Actions run:
`37279532576`

Workflow:
`.github/workflows/at0_en_v2_5_scalable_matcher_regression.yml`

Run conclusion:
`SUCCESS`

Run attempt:
`1`

Workflow environment:
- GitHub Actions `ubuntu-latest`
- Python `3.12`
- no model inference
- no FactPICO data

Artifact:
`at0-en-v2-5-scalable-matcher-regression`

Artifact ID:
`11331840770`

Artifact ZIP digest:
`sha256:ec012324b265b5e6be5e1aff5f5dd670547692fc9f8bb6a3f58c993ccbb2cba1`

Artifact expiry:
`2027-01-03T07:45:28Z`

## 2. Narrow V2.5 change

Only the one-to-one assertion assignment implementation is replaced.

Unchanged scientific logic from V2.4:
- tokenization/normalization;
- synonym table;
- owner extraction;
- owner incompatibility;
- semantic pair features/weights as mathematical formula;
- criticality;
- relation alignment;
- outcome engine;
- grouping behavior;
- unequal-count prefix matching + leftover append;
- B2.2 extractor;
- FactPICO V5 scientific gold/thresholds/input/gold artifacts.

## 3. Matcher algorithm

Algorithm:
`HUNGARIAN_EXACT_INTEGER_LEXICOGRAPHIC_V1`

Numeric policy:
`EXACT_RATIONAL_FORMULA_V1`

Priority:
1. minimize hard-owner mismatches;
2. maximize owner similarity;
3. maximize semantic similarity;
4. choose lexicographically earliest candidate-index tuple on exact higher-level tie.

The final tie objective reproduces V2.4's first-permutation-wins policy.

Unequal-count behavior remains intentionally identical to V2.4:
- square prefix only using `min(m,n)`;
- leftovers appended to final group.

No rectangular redesign.

## 4. Frozen V2.5 file hashes

From workflow freeze artifact:

- specification:
  `phase2/academic_transform/at0_en/v2_5/AT0_EN_V2_5_EXACT_SCALABLE_MATCHER_SPEC_V1.md`
  SHA-256:
  `8fe6203b266f86e2e147cf65b4e55d15b8dc25b344b466ac5d0f75ca461f888f`

- aligner:
  `phase2/academic_transform/at0_en/v2_5/gate_b1/b1_aligner.py`
  SHA-256:
  `ac36409cd32c9a759a3e962ee6a86aa30d0a52299f2a19ccc8206d7b54e248ea`

- guarded batch runner:
  `phase2/academic_transform/at0_en/v2_5/run_v2_5_batch.py`
  SHA-256:
  `ad2e996f0e76e8d6b80285d7059b072c53914f32d9d48fbf9af8f8076282b807`

- regression test:
  `phase2/academic_transform/at0_en/v2_5/tests/check_v2_5_scalable_matcher.py`
  SHA-256:
  `6633db047be337df27d1fad61eb8b33a473a6d69c60b73e35ec2611b1552a47a`

- regression report:
  `V2_5_SCALABLE_MATCHER_REGRESSION_REPORT.json`
  SHA-256:
  `2b0861f904448663b1eaff675ed79034bdccdb4c6ccee3ba08e7986fa5eb4b20`

## 5. Unchanged V2.4 inherited component identity

Inherited frozen B2.2 extractor:

`phase2/academic_transform/at0_en/v2_4/gate_b2/b2_2_relation_aware_extractor.py`

V2.4 frozen SHA-256:
`f44a4de5536dae62b8a65a4370d186c8f0087a6bf24e5e4f2d37d25ca3600478`

V2.4 historical factorial aligner remains frozen separately:
SHA-256:
`289d2898c89850f691d52313a1d2a2b12b37cef6b674549215579caedf84cd42`

It is NOT overwritten.

## 6. Existing-development exact regression

B1 canonical pairs:
`12`

Exact B1 output differences:
`0`

B2.2 four-arm exact output differences:
`0`

### GG
- correct: 12/12
- safe PASS: 5/5
- unsafe adversarial PASS: 0
- REVIEW preserved: 1/1

### GE
- correct: 11/12
- safe PASS: 4/5
- unsafe adversarial PASS: 0
- REVIEW preserved: 1/1

### EG
- correct: 11/12
- safe PASS: 4/5
- unsafe adversarial PASS: 0
- REVIEW preserved: 1/1

### EE
- correct: 12/12
- safe PASS: 5/5
- unsafe adversarial PASS: 0/6
- REVIEW preserved: 1/1

Therefore canonical B2.2 behavior is preserved exactly.

## 7. Assignment equivalence

Synthetic exhaustive-equivalence cases:
`205`

Oracle:
canonical V2.4 brute-force permutation matcher at manageable sizes.

Coverage includes:
- n=2..6;
- full ties;
- randomized graph-derived scoring cases;
- candidate reordering/mutation;
- downstream relation-sensitive tie case.

Differences:
`0`

Downstream tie case:
`PASS`

This provides empirical differential evidence that the declared exact V2.5 objective/tie policy reproduces V2.4 on the feasible oracle region.

## 8. Grouping/boundary regression

Covered:
- 1:3
- 3:1
- 3:4
- 4:3
- 4:4
- empty helper-level one-to-one boundary

Observed grouping differences vs V2.4:
`0`

Unequal-count semantics remain unchanged.

## 9. Scalability evidence

Matcher time budget:
`10.0 seconds`

Peak memory budget:
`512 MiB`

Supported maximum assertions per side:
`128`

Two repeated runs per synthetic size:

| n | run 1 | run 2 | peak memory max |
|---:|---:|---:|---:|
| 9 | 0.0321 s | 0.0314 s | 29,976 B |
| 10 | 0.0391 s | 0.0387 s | 34,759 B |
| 12 | 0.0560 s | 0.0555 s | 48,191 B |
| 16 | 0.0992 s | 0.0985 s | 76,811 B |
| 32 | 0.3944 s | 0.3948 s | 274,373 B |
| 64 | 1.5839 s | 1.5831 s | 1,095,926 B |
| 128 | 6.3148 s | 6.7295 s | 5,346,914 B |

All:
`PASS`

This replaces the known factorial execution bottleneck for the supported envelope.

It does NOT prove scientific correctness of the heuristic alignment objective.

## 10. Reproducibility and failure handling

Repeated matcher runs:
`IDENTICAL`

Guardrails:
- timeout: PASS
- crash: PASS
- valid child process: PASS
- empty input: PASS
- out-of-envelope assertion count: PASS
- retry count: 0

Runtime runner defaults:
- per-record timeout: `60 seconds`
- max assertions per side: `128`
- strictly sequential records
- no adaptive retry

Failure semantics:
- timeout -> `INVALID_VERIFICATION / RECORD_TIMEOUT`
- child crash -> `INVALID_VERIFICATION / CHILD_PROCESS_CRASH`
- >128 assertions on either side -> `INVALID_VERIFICATION / ASSERTION_COUNT_OUT_OF_SUPPORTED_ENVELOPE`
- empty/unusable extraction -> explicit INVALID

No best-so-far assignment may be accepted.

## 11. Numeric-policy qualification

V2.5 uses exact rational evaluation of the unchanged mathematical pair-score formula rather than V2.4 binary-float accumulation.

This is an explicit V2.5 identity change.

Observed differential tests:
- 12/12 B1 exact outputs equal;
- all B2 arms exact outputs equal;
- 205 feasible exhaustive-oracle synthetic cases equal;
- no observed mapping/outcome discrepancy.

This does NOT prove bitwise equivalence for every possible legacy floating near-tie.

Any future discrepancy attributable to numeric policy must remain visible and must not be silently reclassified.

## 12. FactPICO exposure

FactPICO used:
`FALSE`

No FactPICO:
- text;
- extraction;
- assertion count;
- timing;
- mapping;
- prediction;
- scoring

was used in V2.5 design or regression.

Prospective FactPICO prediction status remains:
`NOT_RUN`

## 13. Runtime-freeze verdict

`PASS_V2_5_SCALABLE_MATCHER_REGRESSION`

V2.5 is execution-ready for a separate pre-prediction review.

This file does NOT authorize FactPICO execution.

## 14. Exact stop condition

Current checkpoint reached:

`V2.5 SCALABLE-MATCHER REGRESSION + RUNTIME FREEZE / PRE-PREDICTION REVIEW`

Still forbidden:
- FactPICO prediction/scoring;
- FactPICO assertion-count profiling;
- H1 gold/threshold changes;
- broader runtime redesign;
- custom Gate C opening;
- human recruitment;
- Arabic-track work.
