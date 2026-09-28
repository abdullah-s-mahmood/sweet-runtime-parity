# Architecture brainstorming after adjudication — development only

The candidate view adds coverage signal but does not authorize application. Decisions below prioritize independent grammatical checks and original-source preservation; these are proposals, not implementations.

| Idea | Decision | Evidence and next bounded test |
|---|---|---|
| Current Mn/tatweel normalized candidate view | INTEGRATE | Keep as a provenance-preserving review-only candidate source after the 19/98 yield, with explicit no-op filtering. |
| Normalized candidates only after base surgical abstention | INTEGRATE | Avoid displacing the existing supported base surgical edits; use former UNK locations only. |
| Camel Morph morphology validator | PROTOTYPE | Enumerate analyses and reject impossible forms such as وساعا; require context for case selection. |
| Controlled diacritic restoration | PROTOTYPE | Map surviving source marks and require explicit mark deletion/migration/insertion before any patch. |
| Base-letter patch plus existing-diacritic preservation | TEST | Test only span-disjoint cases such as إشتدادًا and إستشعِر, including round-trip exactness. |
| Case-ending reconstruction | PROTOTYPE | Resolve كريمٌ/باسمٌ/واقعٌ and مالًا with context-aware case, not automatic default tanween. |
| Confidence as a soft feature | WATCH | 0.974 wrong وساعا and 0.427 useful حبا overlap strong correct predictions; no threshold. |
| Operation-family routing | TEST | Inspect INSERT/REPLACE/DELETE by this new population; do not import previous DELETE veto. |
| GED as a soft feature | TEST | Use independent detection as supporting evidence, never as correction or automatic application. |
| AraBART or AraT5 second GEC generator | TEST | Coverage remains 79/98 without candidates; test on existing development data only in later gate. |
| Multi-model edit selection | WATCH | Requires independently useful and source-aligned second generator, with review of disagreement. |
| Strict Scientific mode | INTEGRATE | Keep normalized candidates review-only; SCI-DEV-03 threatens confidence-interval term and SCI-DEV-12 citation punctuation. |
| General Arabic proofreading mode | PROTOTYPE | Distinct review choices and visible vocalization uncertainty; no production acceptance from 19 cases. |
| Limit normalization to Mn/tatweel | INTEGRATE | Maintain current internal reversible view; no broader orthographic collapse in this gate. |
| Broader Alef/Ya/Teh Marbuta normalization | DROP | These distinctions are themselves correction targets; current evidence does not justify lossy mapping. |
| Identity-edit filter | TEST | One nominal R label left فتأن unchanged; pre-screen candidate effect before review queue, without changing this run. |
| Inflectional defective-noun gate | PROTOTYPE | Require full stem reconstruction and case validation before any وساعٍ-type suggestion. |
| Citation and technical-term span firewall | PROTOTYPE | Block punctuation deletion near citation and technical words under strict scientific mode; test exact source spans. |

## Competing configurations

1. Base surgical path → former-UNK normalized candidate → morphology/context validation → source-preserving realization → reviewer: PROTOTYPE the missing validation/realization stages; keep normalized output review only.
2. Strict Scientific: offer candidate metadata only, with protected citation/term spans and no automatic patch. Two harmful diagnostic proposals already exist in 12 project-authored cases.
3. If the 79 no-candidate hazard words dominate future workloads, TEST AraBART/AraT5 as a second candidate source on the same development passages, requiring exact edit extraction and no unsolicited rewriting.

## Falsifiable gates

- A realization prototype should reproduce the published target's full Unicode form without altering unrelated letters or existing marks; abstain when case/mood is underdetermined.
- Morphology should reject وساعا while preserving supported يا/واو/نون alternations; report coverage and false rejections, clustered by passage.
- A second generator must increase supported unique target coverage with measured added review burden and harmful edits, rather than only improve whole-passage fluency.

Nothing here tunes SWEET, modifies existing safety rules, freezes a normalization policy, or starts a sealed evaluation.
