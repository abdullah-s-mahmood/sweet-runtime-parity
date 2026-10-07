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


## 2026-10-07 causal forensic verdict — IMPORTANT

Canonical audit:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_CAUSAL_FORENSIC_AUDIT_AND_RESEARCH_V1.md`

R4.3 Stage B run `37566553994` technical SUCCESS, frozen scientific gate FAILED for both heads.
At t=.90: baseline C-style macro precision .833404; H0 .841786 (348TP/85FP); H1 .843930 (362TP/87FP).
H1 still has 46 spurious no-overlap FP and 34 same-class wrong-boundary overlap FP.
Candidate ceiling recall: P .815, I .648, C .730, O .710, so a candidate repair step is not essential for the current >=.20 recall gate.

**Confirmed major supervision gap:** native model error negative slots = ZERO; 1982 background fallback, 6157 static local/composite negatives. Mining source in `r43_stage_b_h0_h1_diagnostic.py` loops only through FIT gold positives, excluding goldless sentence FP candidates by construction. In-sample B inference can also hide errors. READ-ONLY FIT causal replay script prepared but not yet executed.

**Confirmed positive-only C Type**: cropped type head trained only exact gold spans, not NONE/hard negatives.
**Actual-code synthetic BIO bug proof**: run `37568400156` SUCCESS; an I-P after O is silently treated as new P entity. Real FIT incidence NOT YET MEASURED.
**Other risks:** duplicated accepted predictions could bias future candidate-union evaluation; whole-sentence context not full RCT abstract; original EBM-NLP annotation disagreements; exposed SELECT cannot serve as fresh model-selection benchmark.

New retained literature:
- NoiseBench EMNLP 2024 real annotation noise
- CMiNER 2025 missing/noisy labels
- BEAN 2025 triaffine type/boundary
- BGNER 2025 boundary-aware GlobalPointer
- Multi-head Tri-Affine Attention 2026
- GLiNER-biomed 2025 preprint
- OpenBioNER-v2 2026
- source-specific PICO section learning and corrected EBM-PICO labels.

**New highest priority**: FIT-only read-only causal replay + protocol audit, THEN prospectively frozen OOF TRAIN-only hard negatives, joint contextual NONE/P/I/C/O, and only later bounded repair/hybrid or stronger model if justified.

DO NOT prematurely train triaffine/BOPN or use SELECT/historical DEV/protected tests to choose architecture.


### 2026-10-07 provenance and newer PICO paper addendum

- SOURCE PROVENANCE VERIFIED: EBM-NLPmod is the 500 reannotated RCT abstract, flat P/I/C/O, section-specific dataset from *Bioinformatics* 2023 DOI `10.1093/bioinformatics/btad542` (not JAMIA). Its C is deliberately distinct from I. Source authors' exact entity-level micro-F1 0.712 is not directly comparable to the ACAD_PASS exact macro precision scientific gate.
- **FinePICO** (JAMIA 2025, DOI `10.1093/jamia/ocae326`): semi-supervised fine-grained PICO extraction from 2,511 abstracts; high-priority candidate if scarcity/partial labels are established as a dominant problem.
- **Generative versus extractive RCT abstract IE** (2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11036632/): includes Longformer/Flan-T5 full-document context rather than isolated BERT chunks. Preserve as prospective domain-context comparator only after corpus section-selection provenance is validated.
- Original section-specific research estimated 96.7% PICO mention coverage for title+methods in a 30-abstract sample. Verify if our current CoNLL already contains only these sections; do not blindly add full abstract text as context.
- Actual-code synthetic BIO contract audit run `37568400156` passed and confirmed invalid I transitions produce normal-looking proposals. FIT frequency remains unmeasured.

The canonical forensic report was updated at commit `d6f7f6bed04b5234564aeff65b80b7171a4a19f0`.


### 2026-10-07 verified FIT-only B model replay — major causal finding

Read-only run `37568769890` SUCCESS. Artifact `11460495207` digest `sha256:e76de599341742c69c3202cfd299c9677d4f07c914c255d1c9b3b32ae175e9c0`.

On 320 FIT docs, frozen B yielded **2371 exact correct proposals out of 2371 gold and ZERO FP**. Of 1292 FIT sentences, 299 were gold-empty and emitted zero predictions. Original Stage-B SELECT roster instead contained 447 exact correct plus 250 FP; same-model raw native precision ~=64.13% and recall ~=69.84%. This confirms a substantial in-sample vs unseen-document gap and fully explains `native_slots=0`; no FIT native B errors existed to mine.

Goldless sentence error omission is a latent future mining coverage defect, not the observed current zero-native cause. Seven predicted I-after-O transitions occurred only at sequence initial positions, potentially legitimate corpus continuation segments; do NOT call them 7 genuine failures.

**Highest-priority method upgraded from OOF_B only to group-disjoint OOF B candidate AND C_BOUNDARY contextual representation (and C_TYPE if retained)** plus true native error-bank on held-out FIT folds, class NONE/P/I/C/O, calibration, and a separately frozen evaluation.

Canonical freezes:
- `AT0_EN_V26_R43_FIT_B_NATIVE_ERROR_CAUSAL_RESULT_FREEZE_V1.md`
- `AT0_EN_V26_R43_CAUSAL_FORENSIC_AUDIT_AND_RESEARCH_V1.md` updated commit `57f51c51e3059655ca8b1960d659d9bf92259b89`.
