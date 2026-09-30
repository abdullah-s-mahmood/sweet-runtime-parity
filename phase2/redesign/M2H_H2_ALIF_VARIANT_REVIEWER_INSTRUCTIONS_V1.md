# M2-H H2 ALIF_VARIANT Reviewer Instructions v1

Date: 2026-09-30  
Status: **FROZEN BEFORE PRIMARY REVIEW**

## Reviewer role

You are reviewing Arabic correction candidates independently.

Do not attempt to infer which rows are controls, which rows match a published reference, or which model produced the candidate.

Do not consult the project repository, QALB reference files, model outputs, or another reviewer before submitting your primary pass.

## What you receive

For each blinded row you receive:
- packet_id
- source_sentence
- source_span_token_indices
- source_surface
- candidate_replacement
- candidate_sentence

You do NOT receive:
- QALB reference
- gold-support status
- model identity
- model confidence
- ARETA labels
- previous judgments

## Judgment order

For every row:

1. Read the original sentence.
2. Locate the source surface.
3. Read the candidate replacement.
4. Read the candidate sentence.
5. Decide necessity.
6. Decide whether the replacement is correct in this exact sentence.
7. Decide whether meaning/fidelity is preserved.
8. Assign exactly one final blinded disposition.
9. Give a brief linguistic rationale.

Do not judge based on whether the candidate merely looks common or stylistically preferable.

## Allowed labels

### necessity
- REQUIRED_CORRECTION
- OPTIONAL_OR_STYLISTIC
- NO_CORRECTION_NEEDED
- UNCERTAIN

### candidate_correctness
- CORRECT_IN_CONTEXT
- ACCEPTABLE_ALTERNATIVE
- INCORRECT
- UNCERTAIN

### meaning_fidelity
- PRESERVED
- CHANGED
- UNCERTAIN

### final_blinded_disposition
- SUPPORTED_MANDATORY
- SUPPORTED_OPTIONAL_OR_ALTERNATIVE
- UNNECESSARY_EDIT
- WRONG_CORRECTION
- UNCERTAIN_REVIEW

## Meaning of SUPPORTED_MANDATORY

Use `SUPPORTED_MANDATORY` only when all are true:
- the source form needs correction in this sentence;
- the proposed replacement is correct;
- the replacement preserves intended meaning;
- accepting the edit automatically is justified.

A merely acceptable spelling alternative is NOT enough.

## Meaning of SUPPORTED_OPTIONAL_OR_ALTERNATIVE

Use this when the candidate is linguistically acceptable but:
- the source is also acceptable, or
- the correction is stylistic/optional, or
- more than one form is defensible and automatic mandatory correction is not justified.

## Uncertainty

Use `UNCERTAIN_REVIEW` rather than guessing when:
- sentence context is insufficient;
- orthography depends on unresolved lexical identity;
- intended meaning is ambiguous;
- you are not confident that the source truly requires correction.

## Independence

Reviewer A and Reviewer B must complete their passes independently.

Do not reconcile disagreements until both primary outputs are frozen and hashed.

## Output

Return one JSON object per input row with exactly:

- packet_id
- necessity
- candidate_correctness
- meaning_fidelity
- final_blinded_disposition
- brief_rationale

Do not add gold guesses or model comments.
