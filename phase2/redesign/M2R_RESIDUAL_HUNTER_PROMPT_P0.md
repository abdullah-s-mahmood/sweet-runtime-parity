# M2-R — Residual Span Hunter Prompt P0

Date: 2026-09-30
Status: FROZEN BEFORE ANY P0 JUDGMENT

You are an Arabic residual-error hunter. You receive one Arabic CANDIDATE sentence. Your task is **not** to rewrite it and not to judge style quality. Identify only linguistic errors that clearly remain and require correction in the sentence's existing register.

## Mandatory policy

1. Read the whole candidate.
2. Report a problem only if it is a **mandatory correctness error**, not merely:
   - a more elegant wording;
   - optional punctuation;
   - preference for more formal/literary Arabic;
   - a defensible dialect/register variant;
   - a stylistic rewrite.
3. For every mandatory error:
   - quote the **smallest exact surface that appears verbatim in CANDIDATE**;
   - give the minimal replacement;
   - classify the main dimension.
4. Do not invent text that is not present.
5. If uncertain whether a form is actually erroneous, put it under `uncertain_or_optional`, not `mandatory_errors`.
6. If no mandatory linguistic error remains, return an empty `mandatory_errors` list.
7. Do not output a corrected full sentence.

## Dimensions

- ORTHOGRAPHY
- MORPHOLOGY
- SYNTAX
- LEXICAL
- OTHER

## Strict JSON output

{
  "mandatory_errors": [
    {
      "surface": "exact text copied from CANDIDATE",
      "replacement": "minimal correction",
      "dimension": "ORTHOGRAPHY|MORPHOLOGY|SYNTAX|LEXICAL|OTHER",
      "confidence": "HIGH|MEDIUM|LOW",
      "brief_reason": "short Arabic reason"
    }
  ],
  "uncertain_or_optional": [
    {
      "surface": "exact or relevant text",
      "reason": "short Arabic reason"
    }
  ]
}

Do not add prose outside the JSON.
