# M2-R v2 — QALB Complete-Gold Residual Localization Protocol

Date: 2026-09-30
Status: FROZEN BEFORE v2 FEASIBILITY RESULT / PACKET MATERIALIZATION

## Primary question

Can one strong reasoning verifier localize mandatory non-punctuation residual errors in Arabic while leaving fully human-corrected QALB sentences alone?

## Allowed data

QALB14 L1 TRAIN+DEV only, pinned CAMeL-Lab revision:
`8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf`.

Forbidden:
- QALB14 TEST;
- all QALB15;
- reserved Nahw;
- A7'ta 88 reserve;
- sealed benchmark.

## Complete-gold contract

Use only lines where:
1. source/corrected/M2 align by line;
2. M2 source matches source text after normalization;
3. applying all M2 edits reconstructs the human corrected line exactly.

QALB corrected lines are CLEAN under the QALB annotation contract because annotators were instructed to correct all errors.

## Primary-detectable error

An M2 edit is primary-detectable when:
- its source span is nonempty;
- source surface contains an Arabic letter or digit;
- it is not punctuation-only;
- it belongs to a fully reconstructable line.

Pure insertions are excluded because the verifier output must quote an existing candidate surface.

## Strict controlled residual

A withheld edit is STRICT when:
- source span covers exactly one token;
- replacement is exactly one nonempty token;
- both contain Arabic letters;
- neither contains whitespace;
- source != replacement.

Construct candidate by applying every other M2 edit and withholding exactly this one.
Require the withheld source surface to remain present.

## Partition

Partition by `split:line_number`:
- DEVELOPMENT: hash("M2R-V2|id") mod 100 < 70
- CONFIRMATION: 70–84
- HOLDOUT: 85–99

Only DEVELOPMENT is exposed during P0/P1.

## Development packet

120 unique sentence IDs:
- 60 NATURAL_QALB_SOURCE
- 30 CLEAN_QALB_REFERENCE
- 30 QALB_ALL_BUT_ONE_STRICT

No sentence ID appears in more than one family.

## P0 output

Same exact-surface residual-hunter interface:
- mandatory_errors[]
  - surface
  - replacement
  - dimension (diagnostic only)
  - confidence
  - brief_reason
- uncertain_or_optional[]

Dimension is not part of the primary gate in v2.

## Metrics

- CRR: context residual recall on NATURAL + STRICT.
- GELR: reference-edit surface recall on all primary-detectable gold errors.
- CFPR: proportion of CLEAN_QALB_REFERENCE with >=1 mandatory claim.
- SRR: recall of the single withheld strict residual.
- Claim Precision: diagnostic because valid non-reference corrections may exist.
- Invalid Surface Rate.

## Development gate

- CFPR <= 5%.
- CRR >= 85%.
- GELR >= 80%.
- SRR >= 90%.
- Invalid Surface Rate <= 2%.

All must pass.

## Prompt revision

If P0 fails, exactly one P1 is allowed.
P1 may change:
- scan order;
- exact-surface discipline;
- mandatory-vs-style wording.

P1 may not:
- contain failed-case examples;
- change thresholds;
- use confirmation/holdout;
- add a second judge.

If P1 fails, stop this frontier residual-hunter formulation.

## Confirmation

Open CONFIRMATION only after DEVELOPMENT passes.
HOLDOUT remains sealed for a later separately authorized gate.

PASS means residual localization is promising; it does not authorize Arabic auto-apply.
