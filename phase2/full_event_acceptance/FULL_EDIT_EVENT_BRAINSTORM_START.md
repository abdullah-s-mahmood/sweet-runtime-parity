# Phase 2 — Full Edit-Event Acceptance Prototype: Brainstorm Start

Date: 2026-09-28

| Candidate approach | Decision | Reason |
|---|---|---|
| Whole AraBART sentence acceptance | DROP | Full audit contains substantial wrong edits. |
| Single-word-only verifier | MODIFY | Misses valid coordinated multiword events. |
| Complete edit-event unit | PROTOTYPE | Full audit showed event context can change validity. |
| Narrow typed structural rules | PROTOTYPE | Interpretable and compatible with Strict Fidelity. |
| Broad hamza rules | REVIEW-ONLY | Hamzat-wasl and hamzat-al-qat' require lexical/morphological context. |
| Ta-marbuta->ha destructive veto | PROTOTYPE | Recurrent clear degradation pattern. |
| Alif-maqsura->ya destructive veto | PROTOTYPE | Recurrent clear degradation pattern. |
| GED mandatory gate | DROP | Earlier gates lost useful coverage without improving observed precision. |
| GED soft evidence | WATCH | Useful later in evidence fusion. |
| Morphology as correctness oracle | DROP | Prior counterexamples proved analyzability/consensus is insufficient. |
| LLM judge as sole verifier | DROP | Reference-free reliability concerns + strict-fidelity requirement. |
| Event-level independent consensus | NEXT | Strong candidate after event boundary quality is stabilized. |
| Learned verifier on current dev | DROP FOR NOW | Repeatedly inspected, too small, leakage/overfit risk. |
| Review-first for lexical alternatives | INTEGRATE | Correct grammar can still violate minimality/voice/meaning. |

## Architectural intent

The goal is not maximal correction coverage.
The goal is to widen safe automatic correction only where evidence is structurally strong, while preserving REVIEW as a first-class product outcome.
