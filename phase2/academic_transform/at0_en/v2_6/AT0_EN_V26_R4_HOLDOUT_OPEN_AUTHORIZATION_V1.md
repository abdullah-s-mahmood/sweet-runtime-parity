# AT0-EN V2.6 — R4 Internal Holdout Open Authorization V1

Date: 2026-10-05
Status: AUTHORIZED FOR ONE INTERNAL HOLDOUT OPEN/EVALUATION

## Preconditions satisfied

Frozen pre-open thresholds on the already-open 30-RCT development diagnostic:
- unresolved <= 35%
- non-CERTAIN <= 40%
- short fragments <=3 chars = 0
- empty documents = 0
- >128 assertion documents = 0

Observed after R4.1B:
- unresolved = 114 / 377 = 30.24%
- non-CERTAIN = 114 / 377 = 30.24%
- short fragments <=3 chars = 0
- empty documents = 0
- >128 assertion documents = 0

Safety/mechanics:
- legacy mechanics = 260/260 PASS
- R4 biomedical surface suite = 120/120 PASS
- safe = 30/30 PASS_CANDIDATE
- critical mutations = 40/40 REJECT
- compression = 20/20 PASS_CANDIDATE
- unsafe critical PASS = 0

## Holdout

Manifest:
`AT0_EN_V26_R4_INTERNAL_HOLDOUT_MANIFEST_V1.json`

Documents:
60

State before trigger:
`UNOPENED`

## FactPICO overlap guard

Reference:
`FACTPICO_V25_SOURCE_CLUSTER_HASHES_FOR_R4_OVERLAP_V1.json`

Count:
115 frozen source-cluster SHA-256 identities.

Evaluator must:
1. fetch immutable holdout bytes;
2. verify each expected Git blob SHA-1;
3. compute raw SHA-256;
4. compare with all 115 FactPICO source hashes;
5. if overlap >0, STOP before extractor invocation.

## Frozen evaluator

`phase2/academic_transform/at0_en/dev_support/v2_6_r4_internal_holdout_eval.py`

Freeze commit:
`708693efdefea38f857d027797fddab3892daa09`

The evaluator emits no holdout sentence text, only identities and numeric diagnostics.

## Frozen holdout acceptance criteria

- short evidence <=3 chars = 0
- empty documents = 0
- >128 assertions/doc = 0
- aggregate unresolved predicate rate <= 40%
- aggregate non-CERTAIN rate <= 45%
- >=80% of documents have non-CERTAIN rate <=50%

No threshold changes after opening.

## Interpretation

PASS:
R4.1B has passed this internal development holdout. Freeze results and stop before external validation.

FAIL:
Preserve failure. Do not tune R4.1B against holdout text and do not loosen thresholds. Move to the preregistered R4.2 architecture decision path.

This is NOT external validation and NOT a FactPICO rerun.

## Execution

The holdout workflow is authorized to run only from creation of:
`phase2/academic_transform/at0_en/v2_6/V26_R4_HOLDOUT_OPEN_TRIGGER_V1.txt`

After that first execution, the holdout is classified as CONSUMED.
