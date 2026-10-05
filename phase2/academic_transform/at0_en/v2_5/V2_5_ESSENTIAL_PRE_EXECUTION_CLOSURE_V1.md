# ACAD_PASS — V2.5 Essential Pre-Execution Closure V1

Date: 2026-10-05
Status: CLOSED / READY FOR FINAL HIGHER-MODEL RE-REVIEW / NO FACTPICO EXECUTION

## 1. Trigger

Independent V2.5 pre-prediction review verdict:

`B. READY_WITH_ESSENTIAL_PRE_EXECUTION_CHANGES`

No demonstrated matcher defect was reported.

Required closures:
1. objective/numeric boundary cases;
2. fresh-process reproducibility;
3. end-to-end mixed-batch failure accounting;
4. max-tie and near-envelope unequal-count scalability;
5. one-shot/output replacement protection.

## 2. What changed

Matcher:
`UNCHANGED`

FactPICO V5 scientific contract:
`UNCHANGED`

Changed:
- batch runner refuses existing output path;
- narrowly isolated `SYN-*` accounting-test mechanism;
- one-shot guard;
- one-shot execution-control specification;
- expanded regression tests;
- new Runtime Freeze V2;
- new FactPICO Execution Identity Amendment V2.

## 3. Final successful evidence

Run:
`37289569561`

Head:
`29e3abe5ccb708cb88d94ae00630eaa0fdc2b123`

Conclusion:
`SUCCESS`

Artifact:
`11335647986`

Artifact ZIP SHA-256:
`61d82aa30de89e84aa5bc0433bdfa528259269c0b3630648df5c0d4c95573b63`

Report SHA-256:
`e0ccf3dd45a7e20f9df7b4086779b2d2846d539c67564ecee2e6a8720b419c87`

## 4. Objective/numeric closure

Synthetic oracle cases:
`205`

Explicit exact-objective checks:
`205`

Observed legacy-float vs exact-rational selected-mapping discrepancies:
`0`

Characterized supplemental cases:
- priority conflict: PASS
- partial tie: PASS
- semantic near-tie: PASS
- full tie / earliest tuple: PASS

Near-tie gap:
`5/51`

No tolerance was used to hide a difference.

## 5. Integration/safety unchanged

B1:
- 12/12 exact behavior retained

B2 four-arm differences:
`0`

EE:
- 12/12 correct
- 5/5 safe PASS
- 0/6 unsafe PASS
- 1/1 REVIEW preserved

No new unsafe PASS.
No lost safe-control acceptance.
No uncertainty regression.

## 6. Fresh-process reproducibility

Two fresh processes produced byte-identical complete runner outputs:

`PASS`

## 7. Mixed-batch failure accounting

Actual batch entry path tested with an isolated synthetic-only accounting mechanism.

Results:
- exact order: PASS
- one output per ID: PASS
- synthetic timeout -> one visible INVALID: PASS
- synthetic crash -> one visible INVALID: PASS
- unaffected neighboring records survive: PASS

No retry behavior introduced.

## 8. Prediction replacement controls

Batch output overwrite refusal:
`PASS`

One-shot guard:
`PASS`

The guard:
- claims the attempt before inference;
- refuses an existing attempt directory;
- invokes runner once;
- freezes prediction SHA-256;
- refuses second use of same attempt location.

Future real attempt ledger MUST use durable storage.

## 9. Scalability closure and preserved negative evidence

New required max-shape tests exposed variability in the old 10-second synthetic matcher criterion.

Preserved failed run:
`37289060156`

Failure:
new `128x128 full-tie` elapsed above the old 10 s synthetic assertion.

This was:
- synthetic only;
- pre-FactPICO;
- not a semantic failure;
- not a production 60 s timeout failure.

A later run passed at approximately:
`5.3285 s`

The internal synthetic criterion was then refrozen at:
`30 s`

Production per-record timeout remains unchanged:
`60 s`

Final run repeated full-tie n=128:
- 7.3144 s
- 7.0391 s
- 7.0154 s

Max:
`7.3144 s`

Near-envelope:
- 127x128: 1.2717 s
- 128x127: 1.2707 s

All final max-shape cases:
`PASS`

The 30 s criterion is benchmark-independent and was selected without FactPICO profiling.

## 10. Memory claim correction

`tracemalloc` values are Python-tracked allocations only.

They are NOT:
- process RSS;
- OS-enforced memory cap.

No stronger memory claim is retained.

## 11. FactPICO status

Prediction:
`NOT_RUN`

Scoring:
`NOT_RUN`

Assertion-count profiling:
`NOT_RUN`

Timing:
`NOT_RUN`

Gold join:
`NOT_RUN`

No FactPICO data were used to close these implementation gaps.

## 12. Quality delta

Compared with the state before the higher-model review:

Improved:
- objective coverage: mapping-only -> mapping + exact objective checks;
- boundary coverage: generic -> characterized priority/tie/near-tie;
- process reproducibility: in-process -> fresh-process;
- failure accounting: helper-only -> mixed batch;
- output replacement: unguarded -> refused;
- attempt control: absent -> claim-before-inference guard;
- max-shape coverage: absent -> 128 full tie + unequal near envelope.

Worsened/new risk:
- old 10 s synthetic criterion shown unstable across runner conditions.

Resolution:
- preserve failure;
- distinguish synthetic budget from production timeout;
- freeze 30 s synthetic criterion;
- retain 60 s production timeout unchanged.

Net assessment:
`IMPROVED / NO NEW SCIENTIFIC REGRESSION OBSERVED`

## 13. Current verdict

`READY_FOR_FINAL_HIGHER_MODEL_PRE_PREDICTION_RE_REVIEW`

This is NOT execution authorization.

Exact next step:
independent review of the bounded closure only.

Maximum later authorization if approved:
`ONE PROSPECTIVE V2.5 FACTPICO PREDICTION RUN + IMMUTABLE PREDICTION ARTIFACT FREEZE ONLY`

Gold join/scoring remains separate.
