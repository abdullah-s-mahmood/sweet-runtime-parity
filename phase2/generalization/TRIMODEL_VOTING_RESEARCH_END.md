# Cross-Training Tri-Model Voting — Research End

Date: 2026-09-29

## Fresh research interpretation

- Arabic text-editing remains an efficient and interpretable GEC architecture, but Arabic morphology makes local correctness difficult even when edit proposals are stable.
- BEA 2026 shows edit-level majority voting can mitigate over-correction, but the method is not a guarantee that consensus edits are contextually complete or correct.
- COCOGEC (Findings ACL 2026) and RobustGEC show that GEC correctness can flip under subtle context changes, which is directly relevant to the residual failures observed here.
- ACL 2026 multilingual GEC evaluation work emphasizes that fixed references can undervalue valid alternatives; therefore this gate used bounded contextual adjudication rather than treating non-exact gold mismatch as automatic error.

## ACAD_PASS implication

The evidence now distinguishes two problems:
1. Model disagreement / over-correction, which voting can reduce.
2. Context-dependent residual correctness, which voting does not solve.

The second problem is now the dominant blocker. More voters alone are unlikely to provide a principled safety boundary unless the additional voter contributes genuinely independent contextual evidence.