# M2-H — Specialized/Hybrid Verifier Feasibility
## Fresh Research & Brainstorming Start

Date: 2026-09-30
Status: PREREGISTRATION START / NO EXPERIMENT RUN

## Trigger

M2-R closed with:
- P1 CRR 86.67%
- P1 GELR 48.88%
- P1 CFPR 33.33%
- P1 strict residual recall 76.67%
- P1 complete Natural sentences only 4/60 = 6.67%

Conclusion:
structured LLM reasoning improved residual edit discovery but failed as a standalone sentence-completeness oracle.

## Fresh external evidence

1. Alhafni & Habash, ACL 2025:
   Arabic GEC framed as explicit text editing / sequence tagging can achieve state-of-the-art or near-state-of-the-art results while being substantially faster and more interpretable than prior generation-first systems.
   https://aclanthology.org/2025.acl-long.875/

2. Mubarak et al., EACL 2026 (Nahw):
   strong LLMs still show substantial gaps in Arabic grammar understanding, detection, correction, and explanation. This argues against relying on a single general LLM judgment layer.
   https://aclanthology.org/2026.eacl-long.296/

3. Östling et al., BEA 2025:
   GEC evaluation is complicated by alternative valid corrections and the mismatch between one reference and the space of acceptable outputs. Exact-reference disagreement therefore remains diagnostic rather than absolute evidence of error.
   https://aclanthology.org/2025.bea-1.16/

4. Wang et al., COLING 2025:
   refined alignment-based edit extraction/evaluation is useful for end-to-end GEC and supports standardized structured error analysis rather than only whole-sentence comparison.
   https://aclanthology.org/2025.coling-main.52/

5. ERRANT remains a strong methodological precedent for explicit edit extraction and type-wise evaluation, though Arabic requires language-specific treatment rather than blind transfer.
   https://aclanthology.org/P17-1074/

## Core brainstorming conclusion

Do not build another generic LLM gate.

Decompose verification into heterogeneous components whose failure modes are intentionally different:

1. Structured edit candidate generation.
2. Orthographic/high-precision deterministic checks.
3. Morphology-aware validation.
4. Structural word-boundary validation.
5. Contextual/semantic ambiguity handling.
6. Calibrated risk fusion.
7. Independent sentence-completeness decision.
8. REVIEW escalation when evidence disagrees.

The objective is not to maximize one model score.
The objective is to test whether heterogeneous evidence can jointly reduce:
- missed residual errors;
- invented mandatory errors;
- sentence-level false-clean decisions.

## Alternatives challenged

### A. More LLM judges / majority vote
Not selected as the main feasibility hypothesis.
Correlated language-model errors can create false confidence and duplicate the M2 failure mode.

### B. Single deterministic grammar engine
Not selected.
Arabic morphology/syntax ambiguity is too rich for a single rule system to cover safely.

### C. Single text-edit model as final oracle
Not selected.
Strong candidate generation does not prove completeness or mandatory status.

### D. Hybrid evidence system
Selected for feasibility testing because it separates:
- finding possible edits;
- validating edits;
- estimating residual risk;
- proving/abstaining on sentence completeness.

## Permanent constraints

- No M3 generator×verifier factorial.
- No Phase 3.
- No QALB15 TEST.
- No reserved Nahw.
- No M2/M2-R Confirmation or Holdout.
- No A7'ta reserve.
- No final sealed benchmark.
- No threshold lowering after results.
- Start with DEVELOPMENT only.
- Existing consumed P0/P1 evidence may be used for design/diagnosis, not as independent confirmation.
