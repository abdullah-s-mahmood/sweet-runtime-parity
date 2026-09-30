# M2-H H1 Candidate Contract v1

Date: 2026-09-30
Status: **FROZEN BEFORE H1 CALIBRATION INFERENCE**
Scope: **CALIBRATION only**

## 1. Purpose

H1 is a structured edit candidate generator. It is not a verifier and its confidence is never safety evidence.

This contract freezes how H1 predictions are converted into reversible candidate edit transactions before H2 calibration.

## 2. Frozen H1 identity

Model:
`CAMeL-Lab/text-editing-qalb14-nopnx`

Frozen model revision:
`21286e56ce98a86362db540863f91c083b8970f9`

Frozen model weight SHA256:
`9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d`

Official implementation repository:
`CAMeL-Lab/text-editing`

Frozen implementation revision:
`4d552ca3ae98029550f27fc52aa1b22883e16e61`

Environment:
- Python 3.10
- PyTorch 1.12.1
- Transformers 4.30.0
- huggingface_hub 0.16.4
- sentencepiece 0.1.99

## 3. Candidate-generation mode

Primary H1 candidate distribution is frozen as:
- top-1 label at each subword;
- one decoding pass only;
- NoPnx checkpoint only;
- no confidence threshold;
- no top-k expansion;
- no punctuation checkpoint;
- no second iterative rewrite pass.

Rationale:
H1 is being used to expose first-pass structured candidate edits anchored to the original source. Iterative decoding would make later edits depend on an already-modified intermediate sentence and would complicate exact reversible source-span attribution. Multi-pass SWEET behavior may be studied later as a separately versioned diagnostic, but cannot be silently substituted into this calibration.

## 4. Raw inference record

For each CALIBRATION case preserve:
- case_id
- uid
- original source
- H1 rewritten sentence
- subword sequence
- top-1 H1 labels
- top-1 probabilities
- model revision
- implementation revision
- truncation flag
- inference status

Probabilities are diagnostic only.

## 5. Structured candidate extraction

Candidates are derived deterministically by token-level alignment between:
- original source whitespace tokens;
- one-pass H1 rewritten whitespace tokens.

Each candidate transaction preserves:
- candidate_id
- case_id
- uid
- exact original source token span [start,end)
- source surface
- candidate replacement
- alignment opcode
- derived operation class
- relevant H1 subword labels/probabilities when recoverable
- exact-gold-match status
- invariant/alignment status

Derived operation labels are descriptive only; QALB M2 remains gold.

## 6. Gold support and single-reference limitation

A candidate is `EXACT_GOLD_SUPPORTED` only when its exact source span and normalized replacement match at least one recoverable QALB gold edit.

A candidate that does not exact-match QALB is `REFERENCE_UNSUPPORTED`, not automatically `WRONG`.

Reason:
QALB supplies an expert correction reference, not an exhaustive set of all linguistically acceptable alternatives.

For conservative automatic-family promotion, report:

`strict_reference_precision_lower_bound = EXACT_GOLD_SUPPORTED / all H2-accepted candidates`

This lower bound pessimistically treats every reference-unsupported accepted candidate as unsupported.

Consequences:
- if the lower bound itself is >=98% and all other H2 gates pass, the precision gate may be satisfied conservatively;
- if it is <98%, the family is NOT declared wrong solely from this metric;
- such a family remains REVIEW/not promoted unless reference-unsupported accepted candidates receive a separately frozen adjudication protocol.

No post-hoc adjudication rule may be invented after seeing INTERNAL_EVALUATION.

## 7. Exclusions and abstention

H1 candidate extraction must flag rather than silently accept:
- tokenizer/model truncation;
- failed deterministic source/output alignment;
- ambiguous candidate span recovery;
- empty/no-op replacements;
- protected-span handling not yet available at this stage.

No INTERNAL_EVALUATION, STRESS_DIAGNOSTIC, Confirmation, Holdout, A7'ta reserve, reserved Nahw IDs, or QALB15 TEST may be opened.

## 8. Required integrity checks

Before H2:
- exactly 6,888 CALIBRATION cases reconstructed;
- CALIBRATION UID SHA256 equals
  `3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9`;
- frozen H1 model revision matches;
- frozen implementation revision matches;
- model weight SHA256 matches;
- one output record per CALIBRATION case;
- candidate IDs unique;
- no reserved dataset markers;
- all candidate spans lie within original-source token boundaries.

## 9. H2 handoff

Only after this artifact passes integrity validation may H2 deterministic family classification be executed.

H1 confidence must not be used as an H2 approval condition.
