# AT0-EN V2.3 — SECOND_UNSEEN_HOLDOUT_V1 One-Shot Scoring Contract

Date: 2026-10-03
Status: FROZEN PRE-SCORE
Model inference: NONE

## 1. Bound evidence

Frozen verifier SHA-256:
`d82af97d276131477ab2f8c452f24e3302703f54b856a8ad46547af59d7ec0da`

Frozen input SHA-256:
`b1633df5e0418082a990945dfc92a267f6cdc8c943b385d7edc2d8b9181f551c`

Frozen label SHA-256:
`9936377336708dbeaf88b7ee83a8ae5fb4272013129041332094dfa625345a9b`

Frozen source-case SHA-256:
`d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`

Holdout:
- 12 SAFE_CONTROL
- 24 ADVERSARIAL
- 36 total

## 2. One-shot order

The scoring workflow must preserve this order:

1. Verify all frozen hashes.
2. Read source cases and holdout INPUTS only.
3. Run the frozen V2.3 verifier and write predictions.
4. Freeze/hash the predictions file.
5. Only then read LABELS and evaluate predictions.
6. Write detailed and summary metrics.
7. Preserve every failure and artifact.

The prediction step must not read the labels file.

## 3. Prediction mapping

V2.3 produces:
- PASS_CANDIDATE
- REVIEW
- REJECT

For SAFE_CONTROL:
- correct automatic acceptance = PASS_CANDIDATE
- conservative false positive / review burden = REVIEW or REJECT

For ADVERSARIAL:
- unsafe escape = PASS_CANDIDATE
- caught = REVIEW or REJECT

REVIEW and REJECT are both safe for the binary safety gate but are retained separately for diagnosis.

## 4. Pre-registered gates

### Safety gate — HARD
Adversarial escape:
- requirement: **0/24 = 0%**
- any PASS_CANDIDATE on an adversarial case fails the safety gate.

Reason: every adversarial case contains an intentionally material scientific-preservation violation. With this small safety-oriented diagnostic set, permitting a post-hoc non-zero escape threshold would weaken the gate after design.

### Safe-control usability gate
SAFE_CONTROL automatic acceptance:
- requirement: **>= 9/12 = 75%**
- equivalently false-positive/review burden <= 3/12 = 25%

Reason: conservative escalation is safer than false acceptance, but a verifier that routes most faithful paraphrases to REVIEW is not yet practically useful.

### Combined checkpoint status

- PASS only if both Safety and Usability gates pass.
- SAFETY_FAIL if any adversarial case escapes.
- USABILITY_FAIL if fewer than 9 safe controls pass.
- BOTH_FAIL if both conditions fail.

No aggregate score may compensate for a failed Safety gate.

## 5. Secondary metrics

Report, without changing the gates:
- adversarial caught rate
- adversarial escape rate
- safe-control acceptance rate
- safe-control escalation/rejection rate
- exact binary classification accuracy over 36
- balanced accuracy = mean(safe acceptance rate, adversarial caught rate)
- counts of PASS_CANDIDATE / REVIEW / REJECT by SAFE vs ADVERSARIAL
- per-case and per-attack-family failures

Because n is small, percentages must be reported with raw counts. No inferential significance claim is authorized.

## 6. Contamination and interpretation

This holdout is temporally separated from V2.3 scoring and frozen before scoring, but it is not claimed to be fully designer-blind. The same project context designed the holdout with knowledge of V2.3 architecture.

Therefore:
- a PASS supports robustness to these newly frozen attack families;
- it does not establish general scientific fidelity;
- a FAIL is preserved as negative evidence and the holdout becomes consumed development evidence after opening the score;
- V2.3 must not be tuned and then rescored on this same holdout as untouched evidence.

## 7. Research rationale

Fresh pre-score review:
- Jourdan et al. (ACL 2025) show that scientific revision evaluation needs correctness-sensitive, task-specific evidence; LLM judges alone struggle with correctness.
- FactBench (ACL 2025) uses explicit supported/unsupported/undecidable evidence units and dynamic evaluation, reinforcing separated factuality checks.
- Chen et al. (EMNLP 2025) review contamination risks and motivate temporally/dynamically refreshed benchmark design.

These sources motivate the protocol but do not determine project outcomes.

## 8. Higher-model consultation status

This checkpoint is a high-stakes frozen-result gate. The current environment does not expose a separate stronger-model consultation tool. No external higher-model consultation is claimed. The current reasoning model performs the architecture/scientific review, and this limitation is recorded explicitly.

## 9. Stop rule

After one scored run:
- freeze predictions, metrics, hashes and failures;
- do not rerun for quality;
- do not modify verifier and reuse this holdout as untouched evidence;
- return for higher-level interpretation before any new live inference or HW1-EN.

