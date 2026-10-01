# HIGHER-MODEL CORRECTED MP-SEF PRE-AUTHORIZATION REVIEW PROMPT V2

Act as an independent senior methodological and reproducibility reviewer.

Repository:
`abdullah-s-mahmood/sweet-runtime-parity`

Branch:
`phase2-arabic-eval`

The user will separately provide:
- the exact SECOND_PREFLIGHT_CODE_COMMIT_SHA;
- the exact SECOND_PREFLIGHT_RUN_ID.

You MUST review that exact commit/run, not a later moving HEAD.

Start with:
`phase2/redesign/MPSEF_CORRECTED_PREAUTH_REVIEW_PACKAGE_V2.md`

Then read all files it references, plus:
- the second-preflight workflow;
- the second-preflight C01-C22 checker;
- the exact second-preflight artifact/summary;
- the one-shot measurement workflow.

This is a PRE-AUTHORIZATION review.

Do NOT:
- compute, estimate, infer, or request R_joint;
- inspect old numerical measurement outputs;
- open reserved/internal sets;
- recommend changing C_F, P1/P2 frozen text, or the >=95% threshold;
- authorize selector training or AUTO_SAFE.

Adversarially verify whether the previous 10 findings are genuinely remediated.

Pay special attention to:
1. whether legality is fully source-only and frozen;
2. whether P2's 1918/1918 GED provenance failure is handled honestly rather than rescued;
3. protected-span boundary/attachment/ambiguity behavior;
4. truncation and failure-state semantics;
5. target-scope and denominator integrity;
6. separation of execution alignment, diagnostic evidence, and gold-aware evaluation matching;
7. R_raw isolation;
8. scorer-failure [L,U] semantics;
9. per-sentence/family/weak-route accounting;
10. exact commit/hash binding;
11. durable consumed-experiment guard BEFORE gold access;
12. whether push/dispatch/rerun paths can bypass the same guard;
13. whether Second Preflight actually implements C01-C22 rather than merely declaring them.

Required Arabic output:
- verdict;
- remaining BLOCKER/MAJOR/MINOR findings;
- C01-C22 audit;
- leakage audit;
- one-shot guard audit;
- claim-scope audit;
- what must not change after authorization.

Choose exactly one final verdict:
- GO TO MEASUREMENT AUTHORIZATION
- MODIFY BEFORE AUTHORIZATION
- STOP / INVALID DESIGN

End with exactly:
`DECISION: <chosen verdict>`
