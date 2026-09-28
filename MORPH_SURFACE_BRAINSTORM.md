# Morphology surface architecture brainstorming — after two-pass adjudication

The 9/9 label-bounded proposals do not validate an independent acceptor. The gold-independent consensus policy accepts `وساعا`, and standalone BERT top-one changes an imperative to a past verb. Decisions below concern future tests, not implementation in this task.

| Idea | Decision | Reason / bounded next test |
|---|---|---|
| Direct local patch | INTEGRATE | Retain narrow exact-offset patch mechanism; 2 recorded direct patches were source-safe in this sample. No universal correctness inference. |
| Morphology lattice validation | PROTOTYPE | Filter analyses by lexical class and case/mood; reject proper-name fallback for وساعا. |
| Contextual BERT morphology | INTEGRATE | Use only as surface ranker after upstream candidate acceptance; 13/18 correct as stand-alone top-one is insufficient. |
| BERT top-two consensus | TEST | Eight correct of nine selected, but one wrong defective noun; never a sole acceptor. |
| Morphology plus SWEET confidence | WATCH | No threshold tuning; previous high-confidence wrong forms mean confidence only a soft feature. |
| Morphology plus GED soft evidence | TEST | Compare independently detected error location without letting GED declare a particular replacement safe. |
| Deterministic Arabic grammar validators | PROTOTYPE | Target narrow checkable case/mood classes with explicit abstain for ambiguous syntax. |
| Defective noun validator | PROTOTYPE | Require final ي in accusative indefinite وساعيًا; flag proper-name fallback. |
| Masculine sound plural case validator | PROTOTYPE | Require ـون for nominative, ـين for accusative/genitive with aligned original shadda/vowel. |
| Five-verbs mood/nun validator | PROTOTYPE | Inspect indicative ن and licensed omission under subjunctive/jussive contexts. |
| Tanween/case-ending validator | PROTOTYPE | Separate case decision from Unicode order of terminal alif and from optional vocalization. |
| Second Arabic GEC generator | TEST | Measure independent incremental supported edits and disagreement on same clustered development passages. |
| AraT5 / AraBART | TEST | Candidate second source from Arabic GEC research; require alignment and source-local extraction. |
| Multi-model agreement | WATCH | Only useful if models are independent and agreement survives grammar/source constraints. |
| Candidate-quality verifier | PROTOTYPE | Most important missing component: verify direction without previous human labels or gold. |
| Semantic verifier | INTEGRATE | Keep independent scientific meaning check after candidate selection; grammar alone cannot protect claims. |
| Strict Scientific mode | INTEGRATE | Hold all morphology suggestions for review unless citation/term/number/unit/equation and semantic safeguards pass. |
| Abstention-first architecture | INTEGRATE | Expose review or reject when case, mood, lexical identity, serialization or source patch is unresolved. |
| Automatic full-document rediacritization | DROP | Conflicts with minimal source-preserving correction and adds unnecessary marks. |
| Canonical tanween/alif serializer | TEST | Compare exact Unicode round trips and renderer behavior before proposing a canonical output policy. |

## Competing system configurations

- **Conservative:** source-local direct patch plus separate candidate-quality verifier; morphology ranker used only after direction accepted. Best fidelity, lower coverage.
- **Review-forward:** morphology lattice and contextual top-two candidates presented with original diacritics and source diff; no silent source replacement. Higher useful suggestions, explicit burden.
- **Strict Scientific:** protected spans, citations, technical terms, numbers and quantities locked, independently verify semantic effect, and route unresolved cases to review. Correct morphology is insufficient.

## Falsifiable next gates

A future independent verifier must reject the defective-noun form `وساعا`, the false `باسْمٍ` reading, and the imperative-to-past substitution without consulting Nahw or earlier human labels. A serializer must retain unchanged Unicode clusters and surrounding punctuation exactly, distinguish `نفسًا`/`نفساً`, and choose whether optional final vowel is permitted. Evaluate coverage and review burden by passage clusters. No model or safety stack was changed here.
