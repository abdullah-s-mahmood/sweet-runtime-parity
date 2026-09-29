# Contextual Residual-Risk Guard — Brainstorm Start

Date: 2026-09-29

| Idea | Decision | Reason |
|---|---|---|
| Add a fourth GEC model | DROP | Three-model consensus already failed the safety contract. |
| Retune voting | DROP | Would overfit inspected development evidence. |
| Broad morphology gate | DROP | Morphology alone previously produced false confidence. |
| Narrow pure-orthography lane | TEST | Most defensible place to search for unattended corrections. |
| CAMeL contextual morphology identity | TEST | Independent structured evidence already supported in current runtime stack. |
| Neighboring edit isolation | TEST | Partial repairs often occur inside larger local error clusters. |
| Accept verbs/function words | DROP V1 | Dominant source of tense, valency, preposition and complementizer failures. |
| Accept adjectives | DROP V1 | Gender/number agreement remains unresolved. |
| Accept proper names | DROP V1 | Transliteration residual already observed. |
| CamelParser2.0 dependency guard | DEFER ONE STEP | Add only if morphology-preserving lane is insufficient. |
| Arabic LM score as oracle | DROP | Frequency preference is not grammatical correctness. |
| Human REVIEW lane | KEEP | Required for all context-governed edits. |

## Falsification target

If even this narrow common-noun orthographic lane contains a wrong or partial edit on the consumed diagnostic population, do not spend a fresh slice on it; escalate to dependency-aware validation instead.
