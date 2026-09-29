# M2 — Frontier Reasoning Verifier Protocol v1

Date: 2026-09-30
Status: FROZEN BEFORE PRIMARY JUDGMENTS

## Objective

Falsify or support the hypothesis that a strong frontier reasoning verifier can safely distinguish acceptable Arabic edits from unchanged erroneous inputs and correct-but-incomplete repairs.

## Verifier input

The verifier receives only:
- case_id
- SOURCE Arabic text
- CANDIDATE Arabic text

Hidden:
- expert reference
- corpus/source family
- case family
- applied/withheld edit indices
- prior ACAD_PASS labels
- generator identity
- model confidence
- historical rationales

## Verifier prompt P0

System task:

You are an Arabic correction verifier, not a corrector. Compare SOURCE with CANDIDATE. Do not rewrite either text. Determine whether CANDIDATE should be accepted as a complete and contextually correct result for the sentence.

Important distinctions:
1. A locally valid edit may still leave another error; then it is REPAIR_INCOMPLETE and must not be ACCEPTed as complete.
2. An unchanged SOURCE can be correct; do not force a change.
3. An unchanged SOURCE can also still contain an error.
4. A fluent candidate can still change meaning or remain grammatically incomplete.
5. More than one Arabic formulation can be valid; do not reject solely because you can imagine another wording.
6. If the linguistic status genuinely depends on unresolved interpretation or missing context, choose REVIEW rather than guessing.
7. Judge the full sentence, not just the changed token.

Return strict JSON with:
- candidate_status: KEEP_CORRECT | REPAIR_COMPLETE | REPAIR_INCOMPLETE | CANDIDATE_WRONG | AMBIGUOUS
- necessity: CHANGE_NEEDED | NO_CHANGE_NEEDED | UNCERTAIN
- local_correctness: CORRECT | INCORRECT | NOT_APPLICABLE | UNCERTAIN
- contextual_correctness: CORRECT | INCORRECT | UNCERTAIN
- residual_error: NONE | PRESENT | UNCERTAIN
- meaning_preservation: PRESERVED | CHANGED | UNCERTAIN
- decision: ACCEPT | REVIEW | REJECT
- confidence: LOW | MEDIUM | HIGH
- brief_reason: max 35 Arabic words

Decision rules:
- ACCEPT only when the candidate is contextually correct and no relevant residual sentence error is detected.
- REVIEW when ambiguity/uncertainty prevents a safe decision.
- REJECT when candidate is wrong, unnecessary harmful change, or unchanged source still clearly needs correction.
- REPAIR_INCOMPLETE must never map to ACCEPT.

## Gold family → safety target

Safe ACCEPT families:
- CLEAN_REFERENCE_KEEP
- FULL_EXPERT_REPAIR
- SINGLE_EDIT_COMPLETE

Unsafe ACCEPT families:
- ERRONEOUS_SOURCE_KEEP
- ONE_OF_MANY_PARTIAL
- ALL_BUT_ONE_PARTIAL

A non-reference alternative is not used as a negative gold in M2.

## Primary metrics

1. Unsafe Acceptance Rate (UAR)
   unsafe cases predicted ACCEPT / all unsafe cases.

2. Safe Acceptance Coverage (SAC)
   safe cases predicted ACCEPT / all safe cases.

3. Review Burden
   REVIEW / all cases.

4. Safe Rejection Error
   safe cases predicted REJECT / all safe cases.

5. Unsafe Escape by family
   separate rates for unchanged erroneous and partial-repair families.

Secondary:
- structured-status accuracy against construction family where directly mappable;
- confidence-stratified UAR;
- source-family breakdown;
- confusion matrix.

## Development P0 gate

On the 120-case development packet:
- UAR <= 5% overall;
- zero ACCEPT on ALL_BUT_ONE_PARTIAL;
- zero ACCEPT on ONE_OF_MANY_PARTIAL OR at most 1 if all such accepts are independently auditable as valid alternatives rather than incompleteness;
- SAC >= 60%;
- CLEAN_REFERENCE_KEEP acceptance >= 60%;
- FULL_EXPERT_REPAIR acceptance >= 60%;
- no source family with UAR >10%.

The gate is intentionally stricter on unsafe acceptance than coverage.

## P1 rule if P0 fails

Only one revision allowed. P1 may change:
- rubric wording;
- order of diagnostic questions;
- explicit instruction to search for residual errors.

P1 may NOT:
- add case-specific examples from P0;
- reveal references;
- change success thresholds;
- use A7'ta reserve;
- add a second judge.

P1 is tested on a fresh disjoint 120-case development packet.

## Reserved A7'ta confirmation gate

If development passes, evaluate 264 cases from the untouched 88 A7'ta pairs.

Confirmation requirements:
- UAR <= 5%;
- SAC >= 60%;
- clean KEEP acceptance >=60%;
- expert repair acceptance >=60%;
- no post-hoc prompt change.

A7'ta confirmation cannot validate multi-edit completeness because the paired examples are not M2 multi-edit annotations; that property remains supported by QALB development evidence.

## Interpretation

PASS means the verifier is promising enough to enter M3/M2-expanded testing.
It does not authorize Arabic production auto-apply.

FAIL means:
- do not add more judge agents;
- Arabic remains Review-first;
- use the failure taxonomy to decide whether a fundamentally different verifier formulation is warranted.

## Reproducibility caveat

If the verifier is a proprietary product model without a pinned immutable API snapshot, record:
- model/product name;
- date;
- reasoning setting;
- prompt version;
- exact blinded packet and output.

Treat this as feasibility evidence, not bit-for-bit reproducibility.
