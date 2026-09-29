# M1 Human Adjudication Protocol

Date: 2026-09-30  
Status: PILOT PROTOCOL FROZEN

## Goal

Determine whether ACAD_PASS Edit Contract v1 is understandable and consistently applicable before any new verifier/model development.

## Reviewers

- Two independent qualified Arabic reviewers for the primary pass.
- A third qualified adjudicator (or a documented consensus session led by a qualified adjudicator) for disagreements.
- The AI agent may prepare packets, run consistency checks, and summarize disagreement. It does not count as either independent human reviewer.

## Blinding

Primary reviewers receive only source text, candidate text, proposed span/group, declared scope/context, and any protection inventory legitimately part of the product input.

They do NOT receive historical classification, model/generator name, model confidence, previous agent rationale, gold/reference correction, or gate outcome.

Reviewers should not browse the project repository before submitting the primary pass because historical judgments are already present there.

## Two-stage judgment

### Stage A — reference-blind
Each reviewer independently fills all v1 axes and a short rationale.

### Stage B — reference-aware check
Only after both Stage-A forms are frozen may the adjudicator see published/reference edits, when available. The reference can reveal a missed dependency or a legitimate alternative; it is not an oracle. Stage-A judgments are preserved.

## Pilot population

The first packet contains 24 already-consumed Nahw surgical edit transactions:
- every historical minority class from the 60-edit surgical audit (wrong/partial/unnecessary);
- plus 13 historical supported cases selected deterministically for diversity.

Historical labels were used only to stratify the calibration packet and are not exposed in the blinded rows.

The pilot is **not** a performance estimate. It tests taxonomy usability, reviewer disagreement, context sufficiency, and whether the derived disposition rules are coherent.

## Annotation order per case

1. Read source and candidate without reference.
2. Identify exactly what changed.
3. Necessity.
4. Local correctness.
5. Contextual correctness.
6. Decide whether the edit is atomic or belongs to a required group.
7. Search for a residual error related to this repair; distinguish it from unrelated residual errors.
8. Semantic fidelity.
9. Scientific fidelity if applicable.
10. Protected/document checks only if evidence is supplied.
11. Material ambiguity/author intent.
12. Severity if applied.
13. Brief rationale citing words/relations, not model behavior.

## Disagreement analysis

Before adjudication, calculate raw agreement for every axis and Krippendorff's alpha or Cohen's kappa where the category structure/sample supports it. Do not collapse categories solely to inflate agreement.

Flag disagreements caused by insufficient context; RELATED vs INDEPENDENT residual error; OPTIONAL vs REQUIRED; cases where the reference changes Stage-A judgment; and cases requiring author intent.

## Pilot acceptance criteria

M1 does not require an arbitrary global kappa threshold to claim “success.” Continue to the main queue only if:
- no axis has systematic definitional confusion;
- adjudication can resolve disagreements without silently changing the contract per example;
- RELATED vs INDEPENDENT residual error is operationally distinguishable for most applicable cases;
- reviewers can separate local correctness from complete repair;
- no critical missing category is discovered.

If not, publish Contract v1.1 with a change log and re-run a small calibration packet. Never overwrite v1 labels.

## Main M1 queue after pilot

After the contract is stable:
- materialize a deduplicated, stratified queue from already-consumed Nahw + QALB development evidence;
- rehydrate QALB text only from the pinned TRAIN/DEV sources already consumed for those exact IDs;
- keep QALB15 TEST, reserved/sealed data and any fourth slice unread;
- sample/group by document/passage/event identity to avoid treating correlated edits as independent observations.

## Outputs

- reviewer_A.jsonl
- reviewer_B.jsonl
- adjudicated.jsonl
- agreement_report.json
- M1_END_REVIEW.md

Until those exist, M1 is not human-validated.
