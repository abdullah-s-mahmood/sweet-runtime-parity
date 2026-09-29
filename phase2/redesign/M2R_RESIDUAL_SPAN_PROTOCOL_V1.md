# M2-R — Residual Span Hunter Protocol v1

Date: 2026-09-30
Status: FROZEN BEFORE DATA FEASIBILITY RESULT

## Scope

Primary task: Arabic non-punctuation residual error localization.

No production auto-apply claim is possible from M2-R alone.

## External expert data

Primary:
- ArabiGEE public dataset, `contexts_nopnx` + `annotations`.
- Dataset identity: `khaled44/arabigee-data`.
- Public dataset viewer reports ~1.21k annotation rows and structured lexical/orthographic/morphological/syntactic labels.

Secondary development evidence:
- already-consumed QALB14 TRAIN/DEV, only if needed for replication after ArabiGEE feasibility.
- no QALB14 TEST, QALB15, ZAEBUC DEV/TEST, reserved Nahw, A7'ta 88 reserve, or sealed benchmark.

## Partition

Partition by `context_id`, never by annotation row:
- DEVELOPMENT: hash(context_id, "M2R-V1") mod 100 < 70
- CONFIRMATION: 70–84
- HOLDOUT: 85–99

The workflow may read all public rows to create the partition, but:
- no raw HOLDOUT text or labels are persisted in development artifacts;
- prompt design may use DEVELOPMENT only;
- CONFIRMATION opens only if the development gate passes;
- HOLDOUT remains unopened to the assistant/model until a later separately authorized gate.

## Prompt output schema

Given only one CANDIDATE sentence, return strict JSON:

{
  "mandatory_errors": [
    {
      "surface": "...",
      "replacement": "...",
      "dimension": "ORTHOGRAPHY|MORPHOLOGY|SYNTAX|LEXICAL|OTHER",
      "confidence": "HIGH|MEDIUM|LOW",
      "brief_reason": "..."
    }
  ],
  "uncertain_or_optional": [
    {
      "surface": "...",
      "reason": "..."
    }
  ]
}

Rules:
- report only errors that require correction, not style improvements;
- quote the exact candidate surface;
- use the smallest sufficient surface;
- do not rewrite the full sentence;
- if no mandatory error is present, `mandatory_errors=[]`.

## Data families

### NATURAL_ERROR_CONTEXT
ArabiGEE erroneous context with its expert error annotations.

### CLEAN_TARGET_CONTEXT
ArabiGEE corrected target context; expected zero mandatory residuals relative to the expert annotation task.

### ALL_BUT_ONE_RESIDUAL
For multi-error contexts, apply all expert corrections except one, leaving exactly one expert-supported residual where construction is unambiguous.

## Primary scoring

1. **Context Residual Recall (CRR)**
   Error-containing candidates for which at least one gold residual surface is localized.

2. **Gold Error Localization Recall (GELR)**
   Gold residual error instances localized by a predicted mandatory-error surface.

3. **Clean False Positive Rate (CFPR)**
   CLEAN_TARGET_CONTEXT candidates with >=1 predicted mandatory error.

4. **Near-Complete Withheld Recall (NCWR)**
   ALL_BUT_ONE_RESIDUAL cases where the withheld expert error is localized.

5. **Claim Precision (CP)**
   Predicted mandatory-error surfaces that overlap/match a gold erroneous span or are subsequently adjudicated as valid alternatives.

6. Error-dimension breakdown:
   orthography / morphology / syntax / lexical.

Exact replacement match is secondary and is not required for localization success.

## Development gate

On DEVELOPMENT only:
- CFPR <= 5%;
- CRR >= 85%;
- GELR >= 80%;
- NCWR >= 90%;
- orthographic residual recall >= 95% when n >= 20;
- no major non-orthographic dimension with n >= 20 has recall <70%;
- invalid surface claims (surface not found in candidate) <=2%.

If any gate fails:
- no prompt tuning beyond one preregistered structural revision;
- no CONFIRMATION/HOLDOUT;
- no multi-agent panel;
- M2-R result is FAIL/MIXED according to metrics.

## Prompt revision

P0 first.
If P0 fails, one P1 revision may improve:
- instruction ordering;
- explicit mandatory-vs-style checklist;
- exact-surface requirement.

No examples from failed development cases may be inserted.
No threshold changes.

## Interpretation

PASS means the residual-hunter component is promising.
It does **not** mean the full Arabic verifier or auto-apply system is safe.

Only after residual detection passes may ACAD_PASS revisit a hybrid decision layer.
