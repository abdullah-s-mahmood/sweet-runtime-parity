# ACAD_PASS Methods Registry

Last updated: 2026-10-07

Purpose: durable registry of every materially considered or executed architecture/method so that no research path is lost across chats or checkpoints.

| Method / Path | Status | Evidence / Rationale | Keep for future? |
|---|---|---|---|
| R4.2B source-aligned BIO candidate model | EXECUTED / FROZEN | Strong source-aligned baseline; dev precision insufficient | YES, as ancestor/reference |
| R4.2C independent boundary localizer + cropped type classifier | EXECUTED / FROZEN | Improved structural diagnostics; dev gate failed; 56 FP at t=.90 | YES, components useful |
| Threshold-only rescue | REJECTED | Raising threshold did not solve P/I/O; C collapsed at .95 | NO |
| R4.2D content-only VALID/INVALID span guard | EXECUTED / REJECTED | Removed 11 TP vs 2 FP; FP mean validity > TP mean validity | NO as standalone |
| Local boundary-shift hard negatives | EXECUTED in R4.2D / RETAIN | Useful but insufficient alone | YES as one negative family |
| Non-overlap/background negatives | EXECUTED / RETAIN | Useful regularization, weak match to dominant near-boundary errors | YES as fallback only |
| PICOX-style composite negatives | LITERATURE-SUPPORTED / PLANNED | Directly targets start/end mixing and PICO exact-span FP | YES, included in R4.3 |
| Native FIT-model error hard negatives | PLANNED / FROZEN PROSPECTIVELY | Matches actual model error distribution without SELECT leakage | YES |
| Contextual typed MLP (H0) | CURRENT PLANNED COMPARATOR | Tests whether missing outside context explains R4.2D failure | YES, current R4.3 |
| Biaffine contextual start-end scorer (H1) | CURRENT PLANNED COMPARATOR | Tests explicit endpoint interaction beyond identical contextual features | YES, current R4.3 |
| Triaffine boundary modeling | RESEARCHED / DEFERRED | Strong biomedical NER precedent; larger architectural change | YES, later candidate |
| BOPN / boundary-offset prediction | RESEARCHED / HIGH-PRIORITY ALTERNATIVE | Repairs near-miss boundaries instead of only rejecting them | YES, likely next if H0/H1 fail |
| Locate-and-Label / boundary regression | RESEARCHED / ALTERNATIVE | Candidate-boundary repair family | YES |
| MRC-style start/end matching | RESEARCHED / ALTERNATIVE | Explicit start-end matching matrix; larger reformulation | YES |
| GlobalPointer / token-pair / grid tagging | RESEARCHED / ALTERNATIVE | Joint token-pair representation; potentially strong exact-span modeling | YES |
| Joint NONE/P/I/C/O span-pair classifier | RESEARCHED / PART OF R4.3 DIRECTION | Unifies validity and type; avoids separate content-only validity stage | YES |
| Hybrid pair scorer + boundary repair | RESEARCHED / DEFERRED | Potential final architecture if rejection and repair solve complementary errors | YES |
| CRF / semi-Markov CRF | RESEARCHED / LOWER PRIORITY | Less direct fit to observed pair/boundary mechanism and overlap flexibility | MAYBE |
| Stronger biomedical encoder | RESEARCHED / DEFERRED | Could improve representation but confounds architecture diagnosis | YES after structural diagnosis |
| Ensemble / stacked uncertainty gating | RESEARCHED / DEFERRED | Could improve precision, but adds complexity and calibration burden | YES if single architecture insufficient |
| LLM extraction / teacher or distillation | RESEARCHED / COMPARATOR ONLY | Potential teacher/comparator, weaker fit for frozen exact-span reproducibility | MAYBE |

## Current scientific sequence

1. R4.3 Stage A: train FIT-only ancestors under frozen TRAIN-internal split.
2. R4.3 Stage B: compare H0 contextual MLP vs H1 biaffine on identical candidates/features/negatives.
3. If neither is adequate, prefer evidence-driven next branch:
   - BOPN-style boundary repair, or
   - broader joint span-pair scorer with composite/native hard negatives,
   selected from the frozen R4.3 failure decomposition.
4. If complementary error reduction is observed, evaluate a prospectively frozen hybrid:
   candidate generation -> boundary repair -> contextual joint pair scoring -> typed accept/review.

## Governance

- Do not discard a method merely because it was not selected immediately.
- Record every executed result, rejection reason, and reusable component.
- Do not reuse exposed SELECT/DEV adaptively without a newly frozen evaluation protocol.
- Protected external tests remain closed until a separately frozen model/protocol is ready.


## 2026-10-07 independent evidence update

### Boundary-repair feasibility audit

Run `37539123038` completed successfully on FIT only.

Frozen result:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_INDEPENDENT_BOUNDARY_REPAIR_FEASIBILITY_FREEZE_V1.md`

Key evidence:
- local perturbation candidates = 105,766;
- unique nearest gold target = 101,487 (~95.95%);
- ambiguous nearest target = 4,279 (~4.05%);
- repairable within +/-4 = 100,768 (~95.28%);
- composite spans = 2,822;
- composite ambiguous nearest target = 753 (~26.68%);
- composite repairable within +/-4 = 615 (~21.79%).

Registry implication:
- BOPN / boundary-offset repair remains HIGH priority for local near-boundary errors;
- composite/far spans should preferentially be handled by contextual joint pair scoring / reject-review;
- a future repair + contextual-verifier hybrid is now supported by TRAIN-only structural evidence, but remains contingent on Stage-B error decomposition.


### Context-signal and locality evidence

Independent FIT-only runs:
- context-signal probe `37539134852`
- context-locality audit `37539816534`

Frozen results:
- `AT0_EN_V26_R43_INDEPENDENT_CONTEXT_SIGNAL_FREEZE_V1.md`
- `AT0_EN_V26_R43_INDEPENDENT_CONTEXT_LOCALITY_FREEZE_V1.md`

Key evidence:
- frozen-base contextual probe macro-F1 = 0.6414445653 vs cropped probe = 0.5634747631; delta +0.0779698022;
- on ambiguous surfaces, contextual macro-F1 = 0.5777777778 vs cropped = 0.3866666667; delta +0.1911111111;
- cropped surface-only representation had 42 conflicting keys;
- +/-1 word context reduced conflicts to 2;
- +/-2 reduced conflicts to 1;
- +/-4 reduced conflicts to 0.

Registry implication:
- missing context is now supported by direct TRAIN/FIT-only evidence;
- contextual scoring remains HIGH priority;
- this does not by itself establish biaffine necessity, so H0 versus H1 remains scientifically necessary.


## 2026-10-07 independent context evidence

### Frozen-base contextual signal probe

Run `37539134852`, FIT-only exploratory.

Frozen result:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_INDEPENDENT_CONTEXT_SIGNAL_PROBE_FREEZE_V1.md`

Same simple 5-way probe task, cropped versus contextual frozen-base representations:
- cropped macro F1 = 0.563475;
- contextual macro F1 = 0.641445;
- delta = +0.077970 (+7.797 pp);
- ambiguous-surface subset macro F1 delta = +0.191111 (+19.111 pp), n=14.

Strong gains:
- P F1 0.4583 -> 0.7368;
- O F1 0.4685 -> 0.6398;
- I F1 0.5841 -> 0.6245.

Risk:
- C F1 0.4483 -> 0.3529;
- C precision 0.5652 -> 0.2687.

Registry implication:
context is now directly supported as useful, but C must be treated as a distinct stability risk; no class-specific SELECT tuning is authorized.

### Context locality audit

Run `37539816534`, FIT-only exploratory.

Frozen result:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_INDEPENDENT_CONTEXT_LOCALITY_AUDIT_FREEZE_V1.md`

Conflicting label keys:
- surface only: 42;
- +/-1 outside token: 2;
- +/-2: 1;
- +/-4: 0;
- full sentence + coordinates: 0.

Registry implication:
the cropped-surface ambiguity is overwhelmingly contextual rather than irreducible annotation contradiction in this FIT construction.

### Stage-B mechanics readiness

Run `37540302867` PASS.
Freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_STAGE_B_MECHANICS_FREEZE_V1.md`

H0/H1 implementation is mechanics-ready but MUST remain unlaunched until Stage A successfully freezes its FIT-only ancestors.

### Additional retained alternative

Diffusion-style boundary denoising / DiffusionNER is retained as a later alternative for exact-boundary recovery. It is lower priority than the already source-audited BOPN / Locate-and-Label repair family unless later evidence shows iterative denoising is specifically warranted.
