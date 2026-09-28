# Phase 2 — AraBART Edit Brainstorm after adjudication

Date: 2026-09-28

| Idea | Decision | Reason / next falsifiable test |
|---|---|---|
| Full AraBART sentence as product output | DROP | 33/67 new local substitutions are wrong; source fidelity would be unacceptable. |
| AraBART as second candidate generator | INTEGRATE | Adds 29 supported/alternative new local edits in development, including 19/23 target-overlap rows. |
| AraBART-only auto acceptance | DROP | Supported rate is only 43.28% on new edits. |
| Edit-level agreement across independent generators | PROTOTYPE | Supported by BEA 2026; must remain local and target-agnostic. |
| Ta-marbuta→ha veto | INTEGRATE AS PROTOTYPE | Recurrent unambiguous degradation pattern in this sample. |
| Hamza-loss veto | PROTOTYPE | Strong recurring pattern; must distinguish genuine hamzat-wasl correction from destructive deletion. |
| Alif-maqsura/ya validator | PROTOTYPE | Repeated wrong directions are structurally testable. |
| Five-verbs mood/nun validator | PROTOTYPE | Multiple correct recoveries; can provide positive/negative typed evidence. |
| Defective noun validator | PROTOTYPE | Already blocked وساعا failure; retain and generalize carefully. |
| Lexical-substitution auto accept | DROP | Speech-act/meaning drift observed; route to semantic/minimality review. |
| Alignment quality gate | INTEGRATE | One-to-one queue can hide multiword events; complex alignment must be resolved before patching. |
| GED hard gate | DROP | Prior evidence shows coverage loss; keep as soft evidence only. |
| GED soft evidence | TEST | Combine with typed rule evidence and independent agreement. |
| Reference-free LLM judge as sole verifier | DROP | 2025 reliability evidence plus project safety requirements make it unsuitable as oracle. |
| LLM/closest-gold assistance for development adjudication | WATCH | Useful for alternative-reference analysis, never as runtime proof. |
| Small learned verifier on current 79/67 edits | DROP FOR NOW | Too small and repeatedly inspected; high overfitting/leakage risk. |
| Learned edit-aware verifier after data expansion | HIGH-PRIORITY FUTURE PROTOTYPE | Train on disjoint passages/corpora; keep sealed evaluation untouched. |
| Error-type-conditioned selective acceptance | PROTOTYPE | Evidence suggests orthography, morphology, case/mood and lexical edits have very different risk profiles. |
| Strict Scientific mode | INTEGRATE | Linguistic acceptance must still pass protected-span and semantic/scientific verification. |
| Review-forward UX | INTEGRATE | REVIEW is a first-class product state, not a failure state. |

## Proposed next architecture

Generator layer:
SWEET surgical + normalized fallback + AraBART local edits

→ Alignment-quality gate

→ Typed candidate evidence:
operation family + SWEET confidence + GED soft score + AraBART agreement + morphology + deterministic validators

→ ACCEPT / REVIEW / REJECT

→ morphology/surface realization

→ scientific locks + semantic fidelity verification

→ exact source-local patch.

The immediate next experiment should remain target-agnostic and retrospective on development evidence: test typed deterministic veto/evidence features, then complete adjudication of all 106 AraBART edit events including the 10 complex events. Do not freeze a production policy yet.
