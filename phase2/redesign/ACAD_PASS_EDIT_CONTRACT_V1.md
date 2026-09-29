# ACAD_PASS Edit & Transformation Contract v1

Date: 2026-09-30  
Status: FROZEN FOR M1 PILOT. This contract may be revised only after the pilot, with versioning; pilot labels remain tied to v1.

## 1. Purpose

ACAD_PASS evaluates a proposed change as a **reversible edit transaction** inside a linguistic and document context. The contract deliberately separates:
1. whether the edit is needed;
2. whether the edit itself is correct;
3. whether related repair is complete;
4. whether errors remain;
5. whether meaning/scientific content is preserved;
6. whether protected content and document structure remain safe.

A locally correct edit is not automatically a complete repair. A remaining independent error is not automatically damage caused by the edit. Historical labels remain historical evidence and are never rewritten to make v1 appear better.

## 2. Units

- **EDIT**: one atomic text operation.
- **EDIT_GROUP**: edits that must be judged together because accepting only part can be linguistically invalid.
- **DECLARED_SCOPE**: the unit ACAD_PASS claims to have repaired (edit, sentence, paragraph, or document element).
- **DOCUMENT_TRANSACTION**: the applied edit/group plus location, provenance, protection checks, reversibility, and post-application verification.

## 3. Primary annotation axes

### A. Edit necessity
- REQUIRED_ERROR_FIX
- OPTIONAL_IMPROVEMENT
- UNNECESSARY
- AMBIGUOUS_INTENT
- INSUFFICIENT_CONTEXT

### B. Local edit correctness
- CORRECT
- INCORRECT
- VALID_ALTERNATIVE
- AMBIGUOUS
- NOT_APPLICABLE

### C. Contextual correctness
- CORRECT_IN_CONTEXT
- INCORRECT_IN_CONTEXT
- AMBIGUOUS_READING
- INSUFFICIENT_CONTEXT

### D. Edit-group status
- ATOMIC_COMPLETE
- GROUP_REQUIRED_COMPLETE
- GROUP_REQUIRED_INCOMPLETE
- GROUP_BOUNDARY_UNCERTAIN
- NOT_APPLICABLE

### E. Residual-error relation
- NO_RELEVANT_RESIDUAL
- RELATED_RESIDUAL
- INDEPENDENT_RESIDUAL
- POSSIBLE_RESIDUAL_UNCERTAIN
- OUT_OF_SCOPE

### F. Semantic fidelity
- PRESERVED
- CHANGED_BUT_EQUIVALENT
- SEMANTIC_DRIFT
- AMBIGUOUS
- INSUFFICIENT_CONTEXT

### G. Scientific fidelity
Use NOT_APPLICABLE for ordinary learner-text cases.
- PRESERVED
- AT_RISK
- VIOLATED
- AMBIGUOUS
- NOT_APPLICABLE

Scientific fidelity includes, where relevant: negation, modality/degree of certainty, causal claims, comparison direction, population/group linkage, numeric/statistical linkage, terminology, citation-to-claim linkage, and author attribution.

### H. Protected invariants
- PASS
- FAIL
- NOT_TESTED
- NOT_APPLICABLE

### I. Surface/document integrity
- PASS
- FAIL
- UNKNOWN
- NOT_APPLICABLE

### J. Ambiguity / author intent
- RESOLVED
- MATERIAL_AMBIGUITY
- AUTHOR_REQUIRED
- INSUFFICIENT_CONTEXT

## 4. Derived outcome for M1 analysis

The reviewer does **not** assign production auto-apply permission. M1 derives one of:

- ELIGIBLE_FOR_LATER_VERIFIER_STUDY: necessity REQUIRED_ERROR_FIX; local/contextual correctness positive; edit-group complete; no RELATED_RESIDUAL; no semantic/scientific violation; no known invariant/document failure; no material ambiguity.
- REVIEW_REQUIRED: any ambiguity, insufficient context, possible residual, scientific AT_RISK, unknown required protection, or unresolved group boundary.
- REJECT_EDIT: incorrect edit, semantic/scientific violation, unnecessary edit in conservative proofreading mode, or known protection/document failure.

An INDEPENDENT_RESIDUAL does not automatically make the edit wrong. It does prevent a claim that the whole declared unit is fully proofread unless the product scope explicitly allows partial verified edits.

## 5. Severity

- LOW: cosmetic/local issue with no plausible semantic/scientific effect.
- MEDIUM: linguistic degradation or incomplete repair that may mislead a reader.
- HIGH: material semantic, referential, terminology, factual-relation, or structural risk.
- CRITICAL: likely corruption of a protected scientific claim, numeric/statistical relationship, citation/attribution, or document integrity with serious downstream impact.

Severity is separate from confidence.

## 6. Historical compatibility

Historical fields such as SUPPORTED_CORRECTION, SUPPORTED_ALTERNATIVE, PARTIAL_CORRECTION, WRONG_CORRECTION, UNNECESSARY_EDIT and REVIEW_REQUIRED are retained under historical provenance. They are not automatically mapped to v1 outcomes.

Examples:
- historical PARTIAL_CORRECTION may become CORRECT local edit + RELATED_RESIDUAL;
- an exact gold match may still have INDEPENDENT_RESIDUAL elsewhere;
- a valid local alternative may be acceptable even when it differs from one reference.

## 7. Review principles

1. Judge source vs candidate first, without historical label, model identity, confidence, or rationale.
2. Do not equate reference mismatch with error.
3. Do not equate reference match with complete repair.
4. Distinguish error introduced by the edit from error already present in the source.
5. Prefer the smallest context that resolves the judgment; escalate to wider context if needed.
6. Do not invent author intent.
7. Scientific correctness external to the text is a separate task; M1 judges preservation of the author's stated claim unless external verification is explicitly part of the case.
8. A fluent explanation is not evidence that a judgment is correct.
