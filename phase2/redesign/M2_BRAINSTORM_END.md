# M2 — End Brainstorming and Architecture Decision

Date: 2026-09-30

## P0 → P1 lesson

Prompt-level conservatism can trade safety for coverage, but did not find a stable operating point:
- P0 UAR 4.17%, SAC 22.22%.
- P1 UAR 18.75%, SAC 56.94%.

The direction of movement is exactly the wrong shape for unattended auto-accept: coverage rose by accepting many near-complete-but-not-fully-correct candidates.

## Options considered

### 1. P2 prompt tuning
STOP.
Explicitly prohibited by the preregistration, and scientifically likely to overfit development evidence.

### 2. Multiple frontier judge personas / majority vote
DO NOT RUN YET.
Recent work shows multilingual and repeated judge inconsistency; correlated judges can create false confidence.

### 3. Open A7'ta reserve anyway
DO NOT RUN.
Development gate failed. Preserve all 88 pairs untouched.

### 4. Lower the UAR requirement
REJECT.
The project safety objective has not changed.

### 5. Monolithic judge + deterministic Hamza spell check only
INSUFFICIENT AS FINAL DESIGN.
It would fix some observed misses but risks chasing this sample. It is useful as evidence that specialized checks have complementary failure modes.

### 6. Fundamental task decomposition
SELECTED FOR NEXT RESEARCH ITERATION.

Proposed next substage: **M2-R — Residual Span Hunter Feasibility**.

The model is no longer asked “ACCEPT/REJECT this candidate?” Instead:
1. enumerate every remaining **mandatory** error in CANDIDATE;
2. return exact span/surface, error type, proposed minimal fix, and confidence;
3. explicitly mark style/punctuation/register alternatives as OPTIONAL rather than mandatory;
4. abstain when necessity is uncertain.

Use QALB official edits as span-level reference evidence, but stratify by error class:
- mandatory orthographic/morphological/syntactic edits;
- punctuation/register/reference-sensitive edits reported separately.

Primary M2-R metrics:
- recall of withheld mandatory edit spans;
- false-positive residuals on CLEAN_REFERENCE_KEEP;
- precision of mandatory-error claims;
- coverage at zero/near-zero false-positive policy;
- error-type breakdown.

### 7. Hybrid verifier after M2-R
Only if M2-R demonstrates value:
- Edit Validator (source→candidate)
- Residual Span Hunter (candidate)
- deterministic protected-content and orthography checks
- semantic/scientific verifier
- selective decision layer

This is a different architecture, not P2.

## Why residual spans are the right next target

P1 accepted three clearly incorrect candidates solely because a single Hamza error remained. A global “is this complete?” judgment hid the failure. Requiring an explicit span forces the verifier to expose what it thinks remains wrong and makes the result auditable and composable with deterministic checks.

## M3 status

The originally envisioned 2×2 generator×verifier M3 is **not authorized yet**. M2 did not establish a sufficiently reliable verifier. M2-R is a prerequisite redesign experiment, not Phase 3.
