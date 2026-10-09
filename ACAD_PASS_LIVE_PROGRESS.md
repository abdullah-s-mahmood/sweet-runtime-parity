# ACAD_PASS — LIVE PROGRESS

Last updated: 2026-10-09
Branch: `at0-en-v2.6-dev`

## CURRENT STATE

`PREFIT_CLOSURE_ADVANCED / NO_SUCCESSOR_SCIENTIFIC_FIT_YET`

Execution status:
`ACTIVE — CONTINUING PREFIT CLOSURE`

Scientific-training status:
`NOT_STARTED`

VERIFY_INTERNAL:
`CLOSED`

R44C:
`FROZEN / CONSUMED / NOT_RERUN`

## 1. MAIN READINESS PERCENTAGE

Current first-fit readiness:
`73.5%`

Previous checkpoint:
`44.0%`

Absolute improvement:
`+29.5 percentage points`

Relative improvement from the previous checkpoint:
`+67.05%`

Official target before first successor scientific fit:
`100% PREFIT CLOSURE`

Operational threshold for final independent pre-fit review:
`95–100% with no unresolved hard blocker`

Remaining distance to 100%:
`26.5 percentage points`

## 2. INDEPENDENT-REVIEW FINDINGS F01–F06

Current closure:
`90.0%`

Previous closure:
`80.83%`

Absolute improvement:
`+9.17 percentage points`

Relative improvement:
`+11.34%`

Breakdown:
- F01 exposure lineage + protected identity custody: 80%
- F02 DISTANT-CTO / I-C semantics: 100%
- F03 gold-independent preprocessing: 85%
- F04 benchmark eligibility: 75%
- F05 incompatible-comparison handling: 100%
- F06 finite first-campaign protocol: 100%

Target:
`100%`

## 3. WHAT IMPROVED

Since the earlier 44% readiness checkpoint:

- R43/R44 lineage corrected to EBM-NLP_mod.
- Exact-text AD/COVID split audit PASS.
- Protected registry custody audit PASS at the visible-registry layer.
- EBM-NLP_mod -> original EBM PMID mapping recovered:
  - 359/400 = 89.75% overall;
  - 250/256 = 97.65625% DESIGN;
  - 49/64 = 76.5625% VERIFY_INTERNAL;
  - 60/80 = 75.0% OLD_SELECT.
- AD PMID resolution:
  - 118/150 = 78.67% whole corpus;
  - 64/75 = 85.33% official TEST union.
- COVID PMID resolution:
  - 116/150 = 77.33% whole corpus;
  - 61/75 = 81.33% official TEST union.
- Shared resolved PMID with checked DESIGN / VERIFY_INTERNAL / OLD_SELECT / PICO-Corpus / EvidenceOutcomes:
  `0`.
- Gold-independent text-windowing synthetic preflight PASS.
- Strict occurrence-level exact scorer synthetic preflight PASS.
- Source-schema audit PASS.
- Adapter semantic/fail-closed synthetic preflight PASS.
- PICOX four-class adapted comparator protocol frozen.
- Software/runtime/model/tokenizer identity preflight PASS.
- 54 development-attempt slots frozen before any scientific fit.
- Public-human-gold federation protocol frozen.

## 4. WHAT WORSENED / NEW RISKS

No scientific model-performance deterioration has occurred because no successor model has been trained yet.

Newly clarified risks:

1. Some AD/COVID records remain unresolved at PMID level.
2. Same-PMID non-overlap is not the same as complete same-trial-family independence.
3. Protected identity mapping is partial, especially VERIFY_INTERNAL.
4. Real-source offset/window integration still needs end-to-end closure.
5. D5 DISTANT-CTO weak stream needs final file SHA/license/type manifest.
6. GPU/VRAM/weight/mixed-precision feasibility is not yet qualified.
7. PICOX real candidate/negative construction still needs preflight.
8. Third-party raw-data redistribution rights are not assumed when licenses are not explicit.

These are controlled blockers, not evidence that the scientific hypothesis has worsened.

## 5. CURRENT SCIENTIFIC PERFORMANCE

No federation successor fit has been run yet.

Therefore the latest real model-performance evidence remains frozen R44C:

At t=.95:
- macro precision = 87.6735%
- P precision = 89.1892%
- I precision = 81.7109%
- C precision = 93.1818%
- O precision = 86.6120%

Important:
the current 73.5% readiness work has NOT yet changed these accuracy numbers.

## 6. PERFORMANCE TARGET

Primary target:
`MATCH OR EXCEED THE STRONGEST REPRODUCIBLE COMPARABLE SYSTEM UNDER THE SAME DATASET / SCHEMA / SPLIT / METRIC`

Preferred stronger target:
`BEST REPRODUCIBLE STRICT EXACT-SPAN P/I/C/O SYSTEM ON COMPARABLE PUBLIC HUMAN-GOLD BENCHMARKS`

High-precision operating target:
- precision >= 90% for P;
- precision >= 90% for I;
- precision >= 90% for C;
- precision >= 90% for O;
- useful recall retained;
- no class suppression used merely to pass precision.

Cross-corpus target:
robust performance on both AD and COVID and leave-one-corpus-out transfer, not one benchmark only.

## 7. ENGINEERING / RESEARCH OPTIMISM

These are informed forecasts, NOT statistical probabilities.

- Build a very strong practical PICO system:
  `92–95% optimism`

- Reach the level of the strongest genuinely comparable reproducible system:
  `88–92% optimism`

- Beat the strongest comparable system on at least one strict benchmark:
  `80–85% optimism`

- Beat strongest comparators consistently across multiple primary benchmarks:
  `65–75% optimism`

- Pass the strict high-precision P/I/C/O operating gate with useful recall:
  `70–78% optimism`

Current direction of confidence:
`IMPROVING`

Reason:
the remaining failure mechanisms are concentrated and increasingly measurable:
boundary validity, I/C role distinction, provenance, cross-corpus robustness and execution reproducibility.

## 8. FIRST-FIT READINESS BREAKDOWN

1. Source identity/file/license/ontology/split closure: 70%
2. Global alias/trial-family graph: 60%
3. Protected custody: 60%
4. AD/COVID benchmark eligibility: 75%
5. Gold-independent preprocessing: 85%
6. Dataset adapter semantics/mechanics: 80%
7. Strict scorer: 90%
8. Comparator recipes: 70%
9. Runtime/software/model determinism: 60%
10. Attempt manifest: 85%

Arithmetic mean:
`73.5%`

## 9. NEXT BLOCKERS — PRIORITY ORDER

1. Complete remaining provenance/trial-family closure.
2. Complete real-source offset/window integration.
3. Freeze admitted-record manifests per source.
4. Freeze D5 official DISTANT-CTO file identity / SHA / semantic-type manifest.
5. Qualify GPU / VRAM / model-weight identity / mixed precision / batch feasibility.
6. Complete real PICOX candidate-generation preflight.
7. Bind final data/runtime hashes to every one of the 54 development attempt slots.
8. Run final independent pre-fit review.
9. Only after PASS: begin D0–D5 scientific fitting.

## 10. STOP / GO RULE

Current:
`NO-GO FOR SCIENTIFIC FIT`

Reason:
pre-fit readiness = 73.5%, with unresolved hard blockers.

GO requires:
- closure state explicitly changed to PASS;
- no unresolved hard blocker;
- final independent pre-fit review completed;
- immutable attempt/data/runtime manifests bound before first training job.

## 11. EXPECTED NEXT DIRECTION

Expected next percentage:
`~80–85% first-fit readiness`
after real-source adapters/offset integration + D5 source closure + GPU/runtime qualification.

Expected subsequent percentage:
`~90–95%`
after per-fit manifests + PICOX execution closure + residual provenance closure.

Final:
`100%`
only after final independent pre-fit review signs off.

## 12. UPDATE RULE

Update THIS SAME FILE after every meaningful checkpoint.

Every update must state:
1. current percentage;
2. previous percentage;
3. absolute improvement or deterioration;
4. new evidence;
5. new risks;
6. active/stopped execution state;
7. next blocker;
8. scientific-performance change, if any;
9. optimism change, if justified.

Do not increase percentages merely because time passed.
Percentages change only when evidence closes or reopens a requirement.
