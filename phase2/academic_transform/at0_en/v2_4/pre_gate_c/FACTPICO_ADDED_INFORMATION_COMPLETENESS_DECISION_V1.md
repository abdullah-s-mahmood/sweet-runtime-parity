# ACAD_PASS — FactPICO Added Information Completeness Decision V1

Date: 2026-10-05
Status: CLOSED FOR V5 SAFE-CONTROL INTERPRETATION / NO V2.4 EXECUTION

## 1. Question

Can absence of a row in the released FactPICO Added Information span-event files be used in V5 safe-control eligibility?

The allowed claim is deliberately narrow:

`NO_HIGHLIGHTED_ADDED_INFORMATION_SPAN_IN_THE_RELEASE`

It is NOT:

`THE SUMMARY CONTAINS NO POSSIBLE ADDED INFORMATION`

and NOT:

`ALL ADDED INFORMATION IS SOURCE-SUPPORTED`.

## 2. Primary-source annotation evidence

FactPICO Section 2.2 states that generated summaries are evaluated using questions addressing:
- factuality of PICO;
- information added by LLMs during simplification.

For Added Information specifically, annotators are instructed to:
1. highlight addition spans;
2. determine whether each identified addition is factual;
3. provide a free-text rationale.

Therefore Added Information is represented natively as a SPAN-EVENT annotation task, not a one-row-per-summary binary label.

FactPICO Section 2.3 additionally states that, for all 75 doubly annotated summaries, Added Information questions were annotated independently and without discussion.

The released README describes:
- `rest_added_information.csv` as the added-information annotations from the single-annotated set;
- `doubly_annotated_split_added_information.csv` as the added-information annotations from the doubly annotated set.

The released files contain span-event rows rather than explicit negative summary rows.

## 3. Artifact evidence

Frozen FactPICO release:
- 345 canonical summaries;
- 270 nominal single-annotation summaries;
- 75 double-annotation summaries.

Added Information release files:
- single file: 350 span-event rows across 158 canonical source/candidate pairs;
- double file: 165 span-event rows across 73 canonical source/candidate pairs.

There is no released explicit `NO_ADDITION` row type.

Therefore the event-table representation is sparse by construction.

## 4. Export-integrity limitation

The release also contains 15 source clusters in which at least one auxiliary Added Information candidate string cannot be matched exactly to canonical `all_evaluations.csv` candidate text.

Those source clusters remain:

`ADDED_INFO_STATUS = UNKNOWN`

for positive safe-control eligibility.

They are never converted to negative/no-addition evidence.

## 5. Frozen interpretation

For a canonical FactPICO source/candidate record, V5 may assign:

`NO_HIGHLIGHTED_ADDED_INFORMATION_SPAN_IN_THE_RELEASE`

only when:

1. the record belongs to the frozen 345-record FactPICO universe;
2. exact source/candidate identity is valid;
3. no exact Added Information span-event row exists for that source/candidate pair;
4. the source cluster is not among the 15 unresolved auxiliary Added Information identity clusters.

This is an annotation-release statement only.

It does NOT assert that:
- a human could not identify another addition;
- the summary contains no external elaboration;
- absence of a highlighted span proves complete source entailment.

## 6. Why this satisfies the focused review requirement

The higher-model review required evidence that missing Added Information rows are not silently treated as negative labels under incomplete annotation coverage.

The combination of:
- full FactPICO human-evaluation protocol covering added information;
- explicit span-highlighting task definition;
- all 75 double-annotated summaries receiving Added Information evaluation;
- released files being span-event annotation tables;
- conservative exclusion of unresolved identity clusters;

is sufficient for the narrow V5 control statement:

`no highlighted added-information span in the released annotation artifact`.

It is NOT sufficient for any stronger semantic statement, and V5 does not make one.

## 7. Decision

`ADDED_INFORMATION_NEGATIVE_EVENT_INTERPRETATION = PASS_WITH_NARROW_CLAIM`

No V5 denominator change is required.

SAFE_STRICT_CONTROL remains:
- 34 records
- 33 source clusters

No prediction has been run.

## 8. Future improvement

A stronger future benchmark or source-native verification track may directly distinguish:
- source-supported elaboration;
- externally true but source-unsupported elaboration;
- false elaboration.

FactPICO V5 does not attempt to collapse those constructs.

## 9. Exact next action

Proceed to:
`H1 FACTPICO PRE-PREDICTION INTEGRITY GATE`

No V2.4 execution is authorized by this decision.
