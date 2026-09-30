# M2-R — FINAL DECISION

Date: 2026-09-30
Status: CLOSED

## Decision

**M2-R final classification: IMPROVED SCIENTIFICALLY / PARTIALLY SUPPORTED TECHNICALLY / FAIL AS A STANDALONE SAFETY VERIFIER.**

No P2 is permitted.
No development threshold is changed.
Confirmation and Holdout remain CLOSED.
A7'ta reserve remains CLOSED.
M3 is NOT authorized by this closure.

## Why M2-R closes

P1 was the single preregistered structural revision after P0.

P1 improved every principal aggregate direction except invalid-surface rate, which was already perfect:
- CRR: 82.22% -> 86.67% (+4.44 pp)
- GELR: 29.14% -> 48.88% (+19.74 pp)
- CFPR: 60.00% -> 33.33% (-26.67 pp)
- strict residual recall: 63.33% -> 76.67% (+13.33 pp)
- claim precision: 63.47% -> 65.50% (+2.03 pp)
- invalid surface: 0% -> 0%

This is a genuine improvement on a disjoint but comparable QALB14 complete-gold design.

Nevertheless, P1 fails three safety-critical gates:
- GELR >=80%: FAIL at 48.88%
- CFPR <=5%: FAIL at 33.33%
- strict residual recall >=90%: FAIL at 76.67%

Only 4/60 natural P1 sentences had every detectable expert edit recovered.

Therefore more prompt-only iteration is not scientifically justified inside M2-R.

## What M2-R established

1. A monolithic LLM judge is not adequate.
2. Explicit residual span enumeration is better than global accept/reject judgment.
3. Two-pass decomposition is materially better than the P0 one-pass residual prompt.
4. LLM self-confidence is not a safe calibration signal.
5. Edit-level discovery and sentence-level completeness are distinct tasks.
6. Structural edits (especially Merge/Delete) require capabilities not supplied reliably by the current residual LLM.
7. The LLM residual hunter can remain useful as a review/risk feature, but not as the final safety oracle.

## Relation to the previous M2 result

M2 monolithic frontier verifier failed because the safety/coverage tradeoff moved sharply between P0 and P1.

M2-R improved the scientific decomposition of that problem:
- local residual discovery became much stronger;
- over-assertion was reduced;
- the remaining bottleneck is now clearly sentence-completeness proof plus structured edit coverage.

Therefore, versus the end of M2:
**scientific understanding: IMPROVED substantially.**
**Arabic auto-apply readiness: UNCHANGED — REVIEW-first.**

## Architecture implication

Do not continue with another generic LLM gate.

The next research target, if separately authorized, should test a **specialized / hybrid edit-verification architecture** with explicit separation of responsibilities:

1. **Structured edit candidate layer**
   - explicit spans and edit operations;
   - word-boundary / Split / Merge support;
   - morphology/syntax-aware signals.

2. **Specialized edit validators**
   - deterministic orthographic rules where high precision is achievable;
   - morphology/syntax analyzers or specialized learned classifiers;
   - invariant and protected-token checks.

3. **Calibrated risk fusion**
   - combine heterogeneous independent evidence;
   - do not use LLM textual confidence as probability.

4. **LLM residual reasoning**
   - retained only for ambiguous/contextual cases;
   - not trusted as the sole accept/reject oracle.

5. **Sentence-completeness layer**
   - independently verify whether any mandatory residual remains;
   - must be evaluated separately from local edit correctness.

6. **Escalation**
   - unresolved/disagreeing cases remain REVIEW.

This direction is consistent with the broader ACAD_PASS contract:
UNDERSTAND -> PROTECT -> TRANSFORM/PROOFREAD -> INDEPENDENTLY VERIFY -> DETECT RISK -> REPAIR -> RE-VERIFY -> ESCALATE/REVIEW -> PRESERVE DOCUMENT -> DELIVER.

## Research context retained

The M2-R start/end research found converging external evidence that:
- explicit edit representations are effective and interpretable for Arabic GEC;
- strong LLMs still show important Arabic grammar limitations;
- LLM-as-judge reliability and raw confidence are not sufficient guarantees.

These findings support the hybrid direction, but do not by themselves validate any specific future architecture.

## Improvement / magnitude / forecast

### Overall M2-R versus P0
**IMPROVED substantially**, but below safety requirements.

Largest comparable gains:
- CFPR improved 26.67 pp.
- GELR improved 19.74 pp.
- strict residual recall improved 13.33 pp.
- CRR improved 4.44 pp.

### Deployment
**UNCHANGED: REVIEW-first.**

### Forecast
A specialized/hybrid verifier is more promising than further generic prompt engineering because M2-R isolated distinct failure modes:
- edit discovery;
- structural edit detection;
- mandatory-vs-optional discrimination;
- sentence completeness;
- calibration.

Main risks:
- correlated errors across components;
- morphology/syntax coverage remaining weak;
- valid-alternative corrections being penalized by single-reference exact matching;
- increased system complexity without independent safety gain;
- overfitting development evidence;
- confusing strong local edit precision with complete sentence repair.

## Data governance after closure

Remain CLOSED:
- QALB15 TEST
- reserved Nahw evidence
- M2 Confirmation
- M2 Holdout
- M2-R Confirmation
- M2-R Holdout
- A7'ta reserved 88
- final sealed benchmark

No Phase 3.
No M3 generator x verifier factorial.

## Next legitimate action

Only if separately authorized:
**pre-register a new specialized/hybrid verifier feasibility stage** using already-authorized development evidence first.

It must begin with fresh research and maximum-effort brainstorming, define independent component hypotheses, calibration criteria, sentence-completeness criteria, and explicit stop rules before execution.

It is not M2-R P2 and must not silently inherit or weaken failed M2-R gates.
