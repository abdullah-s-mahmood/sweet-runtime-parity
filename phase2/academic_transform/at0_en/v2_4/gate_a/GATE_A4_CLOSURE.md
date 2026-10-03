# AT0-EN V2.4 — Gate A4 Readiness Closure

Date: 2026-10-03
Status: CLOSED / GO_ALIGNMENT_RESEARCH_DEVELOPMENT_ONLY

## Final decision

Higher-model verdict:
`ACCEPT_AND_PROCEED_TO_ALIGNMENT`

Project final disposition:
`GO_ALIGNMENT_RESEARCH_DEVELOPMENT_ONLY`

The source extractor is accepted only as a development input for alignment research.

It is NOT:
- production-approved;
- generally validated;
- validated on authentic academic documents;
- validated on candidate-side extraction;
- proof of end-to-end V2.4 safety.

## Evidence entering the decision

A1:
- deterministic anchor precision/recall: 100% / 100%
- exact provenance: 35/35

A3:
- gold assertion coverage: 100%
- critical coverage: 100%
- false additions: 0%
- atomic one-to-one: 88%
- overmerge: 12%
- certain precision: 92.86%
- error-abstention recall: 87.5%
- unnecessary abstention: 23.53%
- context dependency detection: 100%
- critical silent semantic errors: 0
- assertion-type accuracy: 86.36%

## Decision change

Pre-consultation:
`REPAIR_TARGETED_FIRST`

Post-consultation:
`ACCEPT_AND_PROCEED_TO_ALIGNMENT`

Reason:
The preliminary decision over-weighted overmerge as a blocker.

The independent review correctly distinguishes:
- atomicity imperfections,
from
- material semantic loss.

The frozen architecture explicitly supports 1:N and N:1 alignment. Therefore overmerge is not a blocker unless it is shown to lose/rebind ownership, scope, negation, relation identity, or other material semantics.

No such CERTAIN critical silent failure was observed in A3.

## Accepted consultation conditions

1. Begin alignment on development data only.
2. Use human-correct/reviewed source and candidate representations first.
3. Report gold-graph alignment separately from extracted-graph alignment.
4. Keep uncertainty explicit; graph agreement does not cancel uncertainty.
5. Keep overmerged and abstained cases in denominators/diagnostics.
6. Do not force zero overmerge.
7. Defer assertion-type optimization unless it affects semantic routing.
8. Defer unnecessary-abstention optimization.
9. Introduce authentic academic text after a diagnosable alignment prototype, but before integrated system freeze/validity claims.

## Active risks carried forward

- small synthetic development set;
- CERTAIN precision based on only 14 predictions;
- candidate-side extraction unknown;
- shared source/candidate extraction bias;
- harmful merge may only become visible during alignment;
- uncertainty propagation can be mishandled;
- authentic-document structure/context not yet represented.

## Alignment constraints

The next stage must:
- isolate alignment error using correct/human-reviewed graphs first;
- support 1:1, 1:N, and N:1 mappings;
- preserve ownership, scope, polarity, modality, causality, time, population, baseline, citation/equation/symbol binding;
- never treat similarity alone as PASS evidence;
- never let many correct alignments compensate for one critical wrong relation;
- retain traceable evidence for each critical alignment;
- prevent uncertain+uncertain agreement from becoming CERTAIN automatically.

## Fresh research conclusion

Current research supports proceeding:
- ACL 2025 decomposition work shows atomicity should be evaluated in interaction with downstream verification rather than in isolation;
- EACL 2026 work further supports explicit decomposition/verifier alignment;
- Claimify supports independent attention to ambiguity, coverage and decontextualization.

The evidence supports limited alignment research, not generalization or safety claims.

## Quality delta

End-to-end scientific-fidelity performance:
**UNCHANGED**

Last full verifier result:
- adversarial escape: 37.5%
- safe automatic acceptance: 25%
- BOTH_FAIL

Readiness delta:
- pre-consultation recommendation: REPAIR_TARGETED_FIRST
- final readiness: ACCEPT_AND_PROCEED_TO_ALIGNMENT

This is a decision change, not a performance improvement percentage.

Methodological status:
**IMPROVED**

## Completion

Gate A4:
**100% COMPLETE**

Gate A overall:
**100% COMPLETE**

Whole ACAD_PASS planning completion:
**approximately 26% ±5%**

## Exact next authorized stage

`AT0-EN V2.4 GATE B1 — ALIGNMENT PROTOTYPE WITH HUMAN-CORRECT GRAPHS`

Initial B1 scope:
- development-only;
- no model inference required initially;
- construct a small fixed set of human-correct source/candidate assertion graphs;
- implement alignment mechanics only;
- support 1:1, 1:N, N:1;
- score alignment independently from extractor quality;
- preserve uncertainty and evidence traces;
- include faithful paraphrases, split/merge, relation rebinding, scope/negation changes and ambiguity;
- do NOT use extracted source/candidate graphs until gold-graph alignment behavior is understood.

Not authorized:
- live generation
- HW1-EN
- new untouched holdout
- production claims
- authentic-document integrated validation before a diagnosable B1 prototype exists

Higher-model consultation is not required at B1 start unless a new construct-validity/architecture issue appears.
