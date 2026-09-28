# Phase 2 — WAW_ALIF Morphosyntactic Recovery Gate

Date: 2026-09-28
Status: PRE-REGISTERED BEFORE READING THE NEW ZAEBUC TRAIN GOLD SLICE

## Trigger

The previous QALB-2015 L2 DEV 100-line hash slice produced zero candidates for the source-top-POS policy `WAW_ALIF_VERB_ONLY`. That result is **UNPROVEN / coverage-zero**, not evidence of correctness or failure.

Arabic orthographic references agree that the differentiating alif is written only after terminal **واو الجماعة attached to a verb**, not after:
- an original/root waw in a verb such as `يدعو`;
- nominal plural/construct waw such as `معلمو المدرسة`.

CAMeL morphology exposes POS, number, person, aspect and mood, so the next hypothesis uses candidate and source morphosyntactic evidence rather than terminal characters alone.

## External population

Corpus:
ZAEBUC-v1.0 Arabic TRAIN

License:
CC BY-NC-SA 4.0

Previously consumed train lines:
the 30 line IDs recorded in `PHASE2_FINAL_ALIF_GENERALIZATION_RESULTS.json`.

Fresh selection:
1. read TRAIN raw only;
2. exclude those prior 30 line IDs;
3. retain lines containing at least one whitespace token whose normalized surface ends in `و` but not `وا`;
4. compute SHA-256(`phase2-waw-alif-morph-v1|<raw-line>`);
5. choose the 60 lowest hashes;
6. no corrected/gold text is read until runtime decisions are materialized.

ZAEBUC DEV and TEST are not used for this gate.

## Frozen generator

Same QALB14 stack:
- CAMeL-Lab/camelbert-msa-qalb14-ged-13
- CAMeL-Lab/arabart-qalb14-gec-ged-13
- upstream CAMeL-Lab/arabic-gec commit 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

No training or fine-tuning.

## Candidate event shape

A WAW_ALIF candidate event must be:
- exactly one source token and one output token;
- substitution-only;
- normalized source ends in `و` and not `وا`;
- normalized candidate == normalized source + `ا`;
- event_cost <= 0.25;
- no word-boundary change.

## Morphology evidence

Analyze both source and candidate.

Candidate must satisfy:
- contextual top analysis POS = `verb`;
- contextual top analysis NUM = `p`;
- candidate form is compatible with terminal group-waw spelling:
  - ASP = `p` (perfective), or
  - ASP = `c` (command), or
  - ASP = `i` and MOD in {`s`, `j`} (subjunctive/jussive);
- candidate analysis must not be a backoff-only nominal/foreign interpretation.

Also query the source token with the morphological analyzer to distinguish a valid singular/root-waw word from a malformed plural form.

## Policies

### WAW_ALIF_MORPH_STRICT

ACCEPT only if:
- candidate event shape passes;
- candidate contextual analysis is plural verb and morphologically licensed as above;
- source analyzer has at least one lexical plural-verb analysis;
- source analyzer has **no** lexical singular-verb analysis;
- source analyzer has no lexical noun/adjective/proper-noun analysis.

This is intentionally conservative.

### WAW_ALIF_MORPH_RECOVERY

Experimental comparator; not automatically promotable from this gate alone.

Candidate event shape + candidate plural-verb evidence, and:
- source has no lexical singular-verb analysis;
- source has no lexical noun/adjective/proper-noun analysis;
- source may have no lexical analysis / spelling-error backoff, allowing recovery of malformed plural verbs.

### SOURCE_SHAPE_ONLY

Diagnostic comparator only:
- source ends `و`;
- candidate = source + `ا`;
- cost <= 0.25.

Never promote this comparator.

## Critical counterexamples the policy must conceptually reject

- singular/root waw: `الطالب يدعو إلى...` → must not become `يدعوا`;
- nominal construct plural: `معلمو المدرسة` → must not become `معلموا`;
- any source with a valid singular verb analysis must remain REVIEW.

## Runtime / gold ordering

1. select raw-only slice;
2. run generator;
3. align events;
4. compute source/candidate morphology;
5. materialize policy decisions;
6. persist raw hashes/decision hashes;
7. only then open corrected lines;
8. classify exact-gold / overlap / no-overlap;
9. manually adjudicate only non-exact accepted events using bounded excerpts;
10. do not tune on this slice.

## Success

WAW_ALIF_MORPH_STRICT:
- at least 3 accepted events preferred for meaningful evidence;
- zero demonstrably wrong accepted events;
- zero partial accepted events.

If fewer than 3 events:
**UNPROVEN due to low coverage**, regardless of precision.

WAW_ALIF_MORPH_RECOVERY:
diagnostic only; may motivate a later fresh gate.

Any wrong accepted strict event => MODIFY.

## Data handling

Persist only:
- selected line IDs + hashes;
- aggregate counts;
- hashed event identities;
- morphology feature summaries;
- bounded non-exact excerpts only if manual adjudication is required.

Do not persist the full corpus.

No Phase 3.
No sealed benchmark.
