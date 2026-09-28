# Phase 2 — AraBART-only edit failure taxonomy

Date: 2026-09-28

Scope: 67 AraBART one-to-one substitutions not already represented by the existing 79 SWEET/normalized candidate word locations. Development-only same-agent two-pass adjudication.

## Main result

- Supported correction: 27
- Supported alternative: 2
- Partial correction: 2
- Unnecessary edit: 2
- Wrong correction: 33
- Alignment uncertain: 1

Supported/alternative rate: 43.28%.

Target-overlap supported rate: 82.61% (19/23).
Non-target supported rate: 22.73% (10/44).
Non-target wrong rate: 68.18% (30/44).

## Recurrent failure families

1. **Ta marbuta → ha degradation**: correct forms such as الطلبة / الفاضلة / النصيحة / القراءة are rewritten with ه. This is a high-value deterministic veto candidate.
2. **Hamza deletion/corruption**: correct أ/إ/ء forms are frequently stripped (أطيعوا, شأن, نشأت, آخرتك, etc.).
3. **Alif-maqsura / ya confusion**: المنى→المني, قصارى→قصاري, يرتدي→يرتدى.
4. **Speech-act / person / tense drift**: أتسألا→اسألاه, فاعمل→فأعمل, فاسعى→فاسعي, داعي→دعا.
5. **Non-minimal lexical rewriting**: فأصغي→فاستمع and ينأَ→يغفل can be linguistically acceptable alternatives but should be REVIEW_ONLY under Strict Fidelity.
6. **Partial correction**: وانطلاقًا→وانطلاقا loses an existing source mark; يتركون→يتركن resolves local agreement with اللائي while the larger ذوو...اللائي mismatch remains.
7. **Alignment collapse**: ولا بد→ولابد is a multiword SUB+DEL event, so the derived one-word ولا→ولابد record is not patch-safe.

## Architecture implication

AraBART should remain an independent candidate/evidence source, never a full-sentence writer and never a sole acceptance oracle. Typed deterministic vetoes can reject several recurring high-frequency failure modes before any learned verifier. Lexical alternatives require review unless a separate semantic/minimality verifier proves equivalence and necessity.

No source text or safety stack was modified.
