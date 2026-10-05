# ACAD_PASS — AT0-EN V2.5 Runtime Freeze V2

Date: 2026-10-05
Status: PASS / FROZEN FOR FINAL PRE-PREDICTION HIGHER-MODEL RE-REVIEW / NO FACTPICO EXECUTION

Supersedes for future execution identity:
`AT0_EN_V2_5_RUNTIME_FREEZE_V1.md`

Parent scientific runtime:
`AT0-EN V2.4`

Matcher:
`HUNGARIAN_EXACT_INTEGER_LEXICOGRAPHIC_V1`

Numeric policy:
`EXACT_RATIONAL_FORMULA_V1`

FactPICO:
`NOT_RUN`

## 1. Why Freeze V2 exists

The independent V2.5 pre-prediction review returned:

`B. READY_WITH_ESSENTIAL_PRE_EXECUTION_CHANGES`

The matcher itself had no demonstrated defect, but the reviewer required bounded closure of:
- characterized objective/near-tie/partial-tie/priority-conflict tests;
- fresh-process reproducibility;
- mixed-batch INVALID accounting;
- max-tie and near-envelope unequal-count scalability;
- durable one-shot/output-replacement controls.

Those controls changed execution/test files after Runtime Freeze V1, so a new execution freeze is required.

## 2. Final regression execution identity

GitHub Actions run:
`37289569561`

Head SHA:
`29e3abe5ccb708cb88d94ae00630eaa0fdc2b123`

Run attempt:
`1`

Conclusion:
`SUCCESS`

Workflow:
`.github/workflows/at0_en_v2_5_scalable_matcher_regression.yml`

Artifact:
`at0-en-v2-5-scalable-matcher-regression`

Artifact ID:
`11335647986`

Artifact ZIP SHA-256:
`61d82aa30de89e84aa5bc0433bdfa528259269c0b3630648df5c0d4c95573b63`

No FactPICO data were used.

## 3. Frozen file SHA-256 identities

- matcher specification:
  `8fe6203b266f86e2e147cf65b4e55d15b8dc25b344b466ac5d0f75ca461f888f`

- matcher implementation:
  `ac36409cd32c9a759a3e962ee6a86aa30d0a52299f2a19ccc8206d7b54e248ea`

- batch runner:
  `7a3383e6108272b641e8f4bcda553a5d97aad7a873616341c3493d425fec6def`

- one-shot guard:
  `3d19fab7be1d1ebee647552bec309be3249e144a86abe1b4d19205f7636e1656`

- one-shot control specification:
  `89dbc7d84df8b1e7e8df5237bc5a0ef7655ea71fd25fe6389c8fc1e18fdd78ab`

- regression test:
  `e2ddd2c283bef5bb15828d195acd93ef04ba0a7b91c8b420d75f0ef58a113169`

- regression report:
  `e0ccf3dd45a7e20f9df7b4086779b2d2846d539c67564ecee2e6a8720b419c87`

Matcher bytes remain unchanged from Runtime Freeze V1.

## 4. Canonical development regression

B1:
- 12 canonical pairs
- exact output differences: 0

B2.2:
- exact four-arm output differences: 0

EE:
- 12/12 correct
- 5/5 safe PASS
- 0/6 unsafe adversarial PASS
- 1/1 REVIEW preserved

GG:
- 12/12 correct
- 5/5 safe PASS
- 0 unsafe PASS
- 1/1 REVIEW preserved

GE:
- 11/12 correct
- 4/5 safe PASS
- 0 unsafe PASS
- 1/1 REVIEW preserved

EG:
- 11/12 correct
- 4/5 safe PASS
- 0 unsafe PASS
- 1/1 REVIEW preserved

No canonical behavior regression was observed.

## 5. Exact assignment/objective closure

Synthetic brute-force oracle cases:
`205`

All 205 now explicitly check:
- selected mapping;
- exact declared objective optimum.

Legacy-float vs exact-rational observed discrepancies:
`0`

Additional characterized cases:
1. priority conflict — PASS
2. partial tie on first two priorities — PASS
3. semantic near-tie — PASS
4. exact full tie / earliest candidate-index tuple — PASS

Near-tie exact semantic gap:
`5/51`

No tolerance-based hiding was used.

## 6. Fresh-process reproducibility

Complete runner output from two fresh processes on fixed synthetic/development-derived input:

`BYTE-IDENTICAL = PASS`

This is separate from in-process matcher repetition.

## 7. Mixed-batch failure accounting

A mixed synthetic batch was executed through the actual batch entry point using the explicitly isolated `SYN-*` test-only fault mechanism.

Contained:
- unaffected valid synthetic records;
- one synthetic TIMEOUT;
- one synthetic CRASH.

Results:
- exact input order preserved;
- exactly one output per ID;
- TIMEOUT -> one visible `INVALID_VERIFICATION / RECORD_TIMEOUT`;
- CRASH -> one visible `INVALID_VERIFICATION / CHILD_PROCESS_CRASH`;
- unaffected records survived and remained non-INVALID.

Verdict:
`PASS`

The synthetic fault mechanism is inert unless explicit synthetic test mode is enabled and rejects non-`SYN-*` IDs.

It is forbidden in future FactPICO execution.

## 8. Output-replacement and one-shot controls

Batch runner:
`REFUSES EXISTING OUTPUT PATH = PASS`

One-shot guard:
- creates exclusive attempt directory;
- creates `ATTEMPT_CLAIM.json` before inference;
- state = `CONSUMED_BEFORE_INFERENCE`;
- executes runner once;
- freezes prediction SHA-256;
- creates `PREDICTION_FREEZE.json`;
- second invocation against same attempt directory is refused.

Synthetic one-shot test:
`PASS`

Future real attempt directory must be on durable storage that survives parent-process cancellation/failure for experiment duration.

An ephemeral-only attempt ledger is not acceptable.

## 9. Scalability closure

Production operational limits remain:
- max assertions per side: `128`
- per-record timeout: `60 s`
- strictly sequential
- retries: `0`

The earlier `10 s` matcher budget was a synthetic regression criterion, not the production record deadline.

New evidence found that this 10 s synthetic criterion was sensitive to GitHub runner variability:
- run `37289060156`: FAIL at the new `128x128 full-tie` <=10s assertion;
- no FactPICO involved;
- this failure is preserved as negative execution evidence.

A subsequent run passed the same case at:
`5.3285 s`

To avoid pretending that a volatile synthetic sub-budget is a production property, the synthetic matcher regression budget was refrozen at:
`30 s`

The actual production per-record deadline remains unchanged at:
`60 s`

Final run repeated `128x128 full tie` three times:
- 7.3144 s
- 7.0391 s
- 7.0154 s

Maximum:
`7.3144 s`

Tracemalloc peak:
`4,878,670 bytes`

Near-envelope unequal prefix grouping:
- 127x128: `1.2717 s`
- 128x127: `1.2707 s`

All:
`PASS`

The 30 s synthetic budget was chosen using synthetic evidence only, before any FactPICO runtime profiling.

It does not change the 60 s external execution deadline.

## 10. Memory qualification

Reported memory values are Python `tracemalloc` tracked allocations.

They are NOT whole-process RSS and are NOT an enforced 512 MiB operating-system memory cap.

No stronger memory claim is made.

## 11. FactPICO exposure

FactPICO used in this closure:
`FALSE`

No FactPICO:
- text;
- extraction;
- assertion counts;
- timing;
- mapping;
- predictions;
- scoring

was used.

Prospective prediction status:
`NOT_RUN`

## 12. Current verdict

Implementation/regression closure:
`PASS_V2_5_ESSENTIAL_PRE_EXECUTION_CLOSURE`

Scientific/execution authorization:
`NOT YET GRANTED`

Exact next checkpoint:
`FINAL HIGHER-MODEL PRE-PREDICTION RE-REVIEW`

No FactPICO prediction or scoring is authorized by this freeze.
