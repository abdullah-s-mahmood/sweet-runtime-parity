# AT0 EN V2.6 — Boundary-Repair Source-Code Audit and Adaptation Note V1

Date: 2026-10-07
Status: EXPLORATORY DESIGN NOTE; NOT AUTHORIZED FOR TRAINING

## 1. Purpose

Translate literature-supported boundary-repair ideas into an ACAD_PASS-compatible implementation hypothesis while R4.3 Stage A is running.

No Stage-A outputs, SELECT, historical DEV, protected test, other folds, FactPICO, or consumed holdout were used.

## 2. BOPN official implementation audit

Official repository:
`mhtang1995/BOPN@7bc0fb9e88f034c9a331b6ec7b99dc9f079df055`

Paper:
Tang et al., "A Boundary Offset Prediction Network for Named Entity Recognition", Findings of EMNLP 2023.
DOI: `10.18653/v1/2023.findings-emnlp.989`

Important implementation facts:

1. Gold entities are represented in a type-aware 2D start/end grid.
2. Exact entity positions are labeled as center `c:0`.
3. `encode_offset()` adds offset labels around each exact entity:
   - start offsets: `s:+/-k`
   - end offsets: `e:+/-k`
   - bounded by a fixed `window_size`.
4. The GENIA configuration uses:
   - `window_size = 2`
   - `offset_mode = both`
   - `parse_offset = true`
   - BioBERT backbone.
5. Decoding does not blindly accept every offset prediction. It aggregates/votes offset evidence before adding an offset-derived entity.

Interpretation:
BOPN is best understood as a bounded local correction mechanism, not an unrestricted long-distance span-rewrite rule.

## 3. Locate-and-Label official implementation audit

Official repository:
`tricktreat/locate-and-label@0e05376fb0174e7eacf66d3c6443a8f1dcab8d5d`

Paper:
Shen et al., "Locate and Label: A Two-stage Identifier for Nested Named Entity Recognition", ACL-IJCNLP 2021.
DOI: `10.18653/v1/2021.acl-long.216`

Important implementation facts from `identifier/sampling.py` and configuration:

1. Candidate spans are compared with gold spans using IoU.
2. A candidate is assigned to the highest-IoU gold entity when IoU exceeds a configured proposal threshold.
3. Regression targets are:
   - left offset = `gold_left - proposal_left`
   - right offset = `gold_right - proposal_right`.
4. Low-IoU proposals are treated as negatives rather than forced into boundary regression.
5. Offset regression supports Smooth-L1 loss; example configuration uses `smoothl1loss`.
6. The model separates proposal filtering/quality from later entity labeling.

Interpretation:
A repair system should have an eligibility/filtering stage before applying offset regression.

## 4. ACAD_PASS TRAIN-only structural evidence

Independent FIT-only run:
`37539123038`

Frozen result:
`AT0_EN_V26_R43_INDEPENDENT_BOUNDARY_REPAIR_FEASIBILITY_FREEZE_V1.md`

Local perturbations:
- 105,766 candidates
- ~95.95% unique nearest gold target
- ~4.05% ambiguous
- ~95.28% repairable within +/-4

Composite candidates:
- 2,822 total
- ~26.68% ambiguous nearest target
- only ~21.79% repairable within +/-4

## 5. Prospective ACAD_PASS repair hypothesis

If Stage-B evidence later indicates candidate/boundary repair is needed, do NOT apply repair to every candidate.

Preferred gated architecture:

`CANDIDATE -> REPAIR_ELIGIBILITY -> {LOCAL_OFFSET_REPAIR | JOINT_VERIFIER/REVIEW}`

### Repair eligibility

A candidate is eligible for offset repair only when frozen TRAIN-derived criteria indicate a local/high-overlap near miss.

Potential features:
- proposal/gold-like boundary confidence pattern;
- candidate width;
- contextual start/end representations;
- local boundary-support probabilities;
- proposal confidence;
- learned repairability probability.

During training only, IoU/known gold may define the repairability target.
At inference, gold is unavailable; repairability must be predicted from candidate/context features.

### Local repair head

Output:
- start offset
- end offset

Prefer a bounded output space initially.

The official BOPN GENIA configuration uses window size 2. ACAD_PASS should not copy this blindly; the final window must be frozen prospectively from TRAIN-only repair-target distribution and later native FIT-error analysis, not SELECT.

Loss candidates:
- categorical bounded offset labels (BOPN-like), or
- Smooth-L1 left/right regression (Locate-and-Label-like).

A future design comparison should choose one prospectively; do not tune both on SELECT.

### Non-repair branch

Composite/far/ambiguous candidates should be sent to:
- contextual joint NONE/P/I/C/O scoring;
- reject/review if validity/type agreement is insufficient.

They should not be coerced toward an arbitrary nearest entity.

## 6. Strong hybrid candidate

If future diagnostics confirm complementary error families:

`BIO CANDIDATE GENERATOR
 -> REPAIRABILITY GATE
 -> LOCAL BOUNDARY OFFSET REPAIR
 -> CONTEXTUAL JOINT START/END + TYPE SCORER
 -> ACCEPT / REVIEW`

This combines:
- repair for recoverable near-boundary false negatives/near misses;
- contextual joint verification for spurious/composite/type-confused spans.

## 7. Disconfirming evidence that would reject this branch

Do not pursue repair if Stage-B/native FIT-error analysis shows:
- candidate ceiling already comfortably passes recall/support;
- most remaining errors have exact boundaries but wrong type;
- actual native boundary errors are not local;
- repair eligibility cannot separate near-misses from spurious spans;
- repair creates more new FP than recovered TP.

## 8. Governance

This note is exploratory only.

It does NOT modify:
- Stage A;
- frozen H0/H1 Stage-B design;
- threshold grid;
- scientific gate;
- protected-data boundaries.

It exists so the boundary-repair path is not forgotten and can be implemented rapidly only if later evidence authorizes it.
