# M2-R — Residual Span Hunter Protocol v1.1

Date: 2026-09-30
Status: FROZEN BEFORE v1.1 PACKET MATERIALIZATION OR MODEL JUDGMENT

This supersedes only the failed v1 near-complete construction. All core safety intent remains unchanged.

## Task

Given one Arabic candidate sentence, enumerate exact spans for remaining **mandatory** linguistic errors. Do not rewrite the whole sentence and do not flag optional style/register/punctuation preferences.

## Data source

ArabiGEE public dataset:
- annotations.csv
- contexts_nopnx.csv

Primary test excludes punctuation contexts.

Partition by context_id:
- DEVELOPMENT: hash mod 100 <70
- CONFIRMATION: 70–84
- HOLDOUT: 85–99

Only DEVELOPMENT may be exposed to P0/P1.

## Development families

- NATURAL_ERROR_CONTEXT: original ArabiGEE erroneous context; gold errors are the manually annotated error pairs available for that context.
- CLEAN_TARGET_CONTEXT: expert-corrected target context; expected zero mandatory residuals relative to this task.
- EXPERT_REINSERTED_RESIDUAL: expert-corrected target context with exactly one documented ArabiGEE error pair reversed, using a unique target surface.

The third family is explicitly a controlled counterfactual.

## Packet

120 unique context IDs:
- 60 NATURAL_ERROR_CONTEXT
- 30 CLEAN_TARGET_CONTEXT
- 30 EXPERT_REINSERTED_RESIDUAL

No context appears in more than one family.

## Metrics

1. Context Residual Recall (CRR)
2. Gold Error Localization Recall (GELR)
3. Clean False Positive Rate (CFPR)
4. Controlled Single Residual Recall (CSRR)
5. Claim Precision (diagnostic)
6. Invalid-surface rate
7. Dimension recall: ORTHOGRAPHY / MORPHOLOGY / SYNTAX / LEXICAL

Exact replacement match remains secondary; localization is primary.

## Development gate

- CFPR <=5%
- CRR >=85%
- GELR >=80%
- CSRR >=90%
- orthographic recall >=95% when n>=20
- no major non-orth dimension with n>=20 has recall <70%
- invalid-surface claims <=2%

No threshold is changed from the intent of v1; CSRR replaces NCWR because the controlled construction changed.

## Prompt revision

P0 first.
If P0 fails, exactly one structural P1 revision is allowed:
- ordering;
- mandatory-vs-optional checklist;
- exact-surface discipline.

No failed-case examples.
No threshold changes.
No second judge.
No CONFIRMATION/HOLDOUT.

## Interpretation

PASS supports only the residual-hunter component.
It does not authorize Arabic auto-apply or prove scientific/document fidelity.
