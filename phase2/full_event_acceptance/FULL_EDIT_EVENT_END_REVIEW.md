# Phase 2 — Full Edit-Event Acceptance Prototype: End Review

Date: 2026-09-28

## Decision

**IMPROVED — materially, but development-only.**

Canonical successful workflow run:
- 36469814686
- conclusion: success

## Results

Population:
- 106 complete AraBART edit events
- 62 supported/alternative by development adjudication
- 35 wrong
- 7 partial
- 2 unnecessary

### EVENT_STRUCTURAL_TYPED

Runtime decision features were materialized before labels were read.

- accepted: 24
- supported correction: 24
- supported alternative: 0
- wrong: 0
- partial: 0
- accepted HIGH/CRITICAL wrong: 0
- development precision: 100%
- supported-event coverage: 24/62 = 38.71%

### EVENT_STRUCTURAL_STRICT

- accepted: 23
- supported: 23
- wrong: 0
- partial: 0
- development precision: 100%
- supported-event coverage: 23/62 = 37.10%

The one additional typed-policy event is ABEV-92-96 (حبًّ -> حبا). Its correction direction is supported, but source vocalization must be restored/preserved by downstream surface realization. Therefore STRICT is the safer product candidate until surface-mark preservation is explicitly enforced on event output.

### Narrow destructive veto

- 14 rows rejected
- 14/14 are wrong in current development adjudication
- 0 supported rows rejected

The narrow veto intentionally covers only:
- ta marbuta -> ha;
- alif maqsura -> ya;
when the rest of the local token is unchanged.

## Incremental value

Of 24 supported accepted events:
- 17 duplicate corrections already covered by the current conservative local acceptance path;
- 7 are incremental event units.

Incremental events:
1. بيت جميل -> بيتا جميلا
2. غاضب -> غاضبا
3. موعد مناسب -> موعدا مناسبا
4. رجل نافع -> رجلا نافعا
5. بيت واحد -> بيتا واحدا
6. عابِس -> عابسا
7. جميل -> جميلا

Four of the seven are multiword events, proving that complete event representation adds value beyond isolated word acceptance.

Do not add 7 directly to the previous 29 local-edit count as if the units are identical. The 7 events contain 11 token-level transformations, but event units and local-edit units serve different accounting purposes.

## What improved

1. The architecture now safely represents bounded multiword grammatical corrections.
2. Event-level acceptance recovers useful changes that wordwise decomposition cannot express safely.
3. Narrow structural rules achieve useful coverage without accepting a known wrong/partial event in development.
4. A narrow destructive veto achieves perfect wrong-only separation on its current 14-row development subset.
5. The runtime/evaluation separation remains anti-leakage: decisions are materialized before labels are read.

## What did not improve / remains risky

1. 68 events still require review under EVENT_STRUCTURAL_TYPED.
2. Hamza corrections remain context/lexicon sensitive and are not auto-accepted.
3. Lexical alternatives and speech-act/tense/person changes remain review-only.
4. This is the same repeatedly inspected development population.
5. Same-agent adjudication is not independent human validation.
6. Scientific, semantic and DOCX safety are downstream requirements and remain mandatory.

## Fresh end-of-gate research

- Alhafni & Habash (ACL 2025): Arabic edit-tagging supports efficient/interpretable local editing and ensembles.
- Goto et al. (BEA 2026): edit-level majority voting mitigates over-correction.
- Goto et al. (TACL 2026): edit representations provide a more interpretable GEC evaluation unit than sentence embedding similarity.
- Wang et al. (Findings ACL 2026, COCOGEC): GEC predictions can fail under subtle context perturbations; counterfactual context variation is a direct robustness test.
- RobustGEC (EMNLP 2023): context robustness is a distinct reliability problem.
- Goto et al. (Findings EMNLP 2025): reference-free/LLM metrics cannot be trusted as sole GEC judges.

## End-of-gate brainstorming

### Integrate / preserve
- Complete edit-event representation.
- Structural typed acceptance.
- Multiword all-final-alif case/agreement events.
- Narrow destructive ta-marbuta/alif-maqsura vetoes.
- Review-first lexical handling.
- Independent downstream semantic/scientific verification.

### Do not integrate yet
- broad hamza auto-acceptance;
- learned verifier trained on current 41 passages;
- GED mandatory thresholds;
- morphology as correctness oracle;
- LLM judge as sole verifier;
- further same-data threshold tuning.

## Next gate recommendation

**Phase 2 — Disjoint / Counterfactual Generalization Gate**

Purpose:
test whether the currently frozen structural event rules survive new contexts and/or a disjoint Arabic GEC population without changing the rules.

Priority order:
1. freeze EVENT_STRUCTURAL_STRICT and EVENT_STRUCTURAL_TYPED definitions;
2. create a disjoint, non-sealed generalization development slice that does not reuse the 41 inspected passages;
3. where feasible, add counterfactual context variants that preserve the same local error/correction relationship;
4. run candidate generation + frozen acceptance without rule tuning;
5. adjudicate only after decisions are materialized;
6. report precision, useful coverage, failure families, passage-cluster uncertainty;
7. if rules fail, MODIFY; if they hold, only then consider a true sealed benchmark.

Do not start Phase 3.
Do not create the final sealed benchmark yet.
