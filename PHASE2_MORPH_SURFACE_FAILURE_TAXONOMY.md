# Morphology surface failure taxonomy — Phase 2 development

## Distinct failure modes

| Failure | Observed evidence | Why it matters |
|---|---|---|
| Upstream wrong direction survives morphology | `وساعٍ → وساعا`: unique morphology surface and BERT top-two consensus, but the defective noun needs `وساعيًا`. | Proper-name fallback is analyzability, not contextual correction proof; a consensus acceptor would make 1/9 wrong. |
| Lexical and sentence-function confusion | For `باسمًا`, BERT proposes `باسْمٍ`, reading **ب + اسم** instead of the predicate `باسمٌ`. | Candidate lattice/ranker can select the wrong lexeme and case. |
| Speech-act change | `إستشعِر` is an imperative; both morphology top-one methods propose past `اِسْتشعَرَ`. The direct patch `استشعِر` preserves intent. | Contextual morphology does not guarantee mood or imperative status. |
| Wrong case from out-of-context prior | MLE `واقِعٍ` after `فالخطر`, and `متقِنٍ` after `فلا`. | Case choice requires syntax; MLE top-one correct only 9/18 selected surfaces by conservative review. |
| Unnecessary source-mark loss | MLE `اشتدادا،` loses original tanween, `عابِسا،` fails to restore it, and `كريم؛` leaves explicit nominative unresolved. | Partial vocalization is part of the source, not disposable preprocessing. |
| Unicode serialization difference | `نَفْساً`, `خَطراً`, `حبّاً`, `مالاً`, `عابِساً` place fathatan after final alif. | Orthographically accepted alternate order is not exact source serialization. |
| Correct but excessive diacritics | `يقدِّمونَ`, `المصريُّونَ`, `الإرهابيِّينَ`, `الباسلُونَ` add final fatḥa absent from the partly marked source. | Valid grammar can still violate minimal source-fidelity editing. |
| No morphological candidate | `واجبة` has no analyses in this gate although a feminine predicate is plausible. | Absence in analyzer is not proof of error. |
| Label-conditioned development selection | Nine bounded proposals were selected using previous human candidate judgments. | Their 0/9 wrong count is not independent runtime precision. |

## Severity and review routing

The defective-noun failure and imperative-to-past substitution change grammatical meaning (HIGH). The morphological proper-name fallback must never grant acceptance; surface consensus is a ranker signal. Under Strict Scientific mode, even grammatically valid forms stay behind citation, term, numeric/unit/equation, named-entity, protected-span, and semantic checks. No scientific text was changed. Passage clustering and the small 19-row sample rule out naive independent-case uncertainty estimates.
