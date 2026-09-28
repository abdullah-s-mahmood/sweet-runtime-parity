# Phase 2 — Full Edit-Event Acceptance Prototype: Research Start

Date: 2026-09-28

## Continuity

This gate continues the bilingual Academic Document Intelligence & Transformation Platform architecture defined before the Arabic GEC work:
UNDERSTAND -> PROTECT -> PROOFREAD/POLISH/TRANSFORM -> INDEPENDENTLY VERIFY -> DETECT RISK -> REPAIR -> RE-VERIFY -> REVIEW -> PRESERVE DOCUMENT -> DELIVER.

This prototype is only the Arabic proofreading candidate-acceptance sublayer. It does not supersede Scientific Integrity Guard, semantic fidelity verification, DOCX protection, mixed-language safeguards, or review-state enforcement.

## Fresh research signals

1. Alhafni & Habash, ACL 2025, Arabic text editing GEC:
   - edit-tagging is efficient and interpretable;
   - Arabic-specific morphology remains difficult;
   - local edits are a practical alternative to full generative rewriting.
   https://aclanthology.org/2025.acl-long.875/

2. Goto et al., BEA 2026:
   - edit-level majority voting reduces over-correction compared with whole-output decisions;
   - reinforces edit-level/event-level acceptance rather than trusting a generated sentence.
   https://aclanthology.org/2026.bea-1.60/

3. Goto et al., Findings EMNLP 2025:
   - reference-free and LLM-based GEC metrics can be adversarially unreliable;
   - do not use an LLM/reference-free score as the sole runtime acceptance oracle.
   https://aclanthology.org/2025.findings-emnlp.1356/

4. Rozovskaya & Roth, ACL 2026:
   - fixed references underestimate valid alternative corrections;
   - evaluation must distinguish valid alternatives from wrong corrections.
   https://aclanthology.org/2026.acl-long.2193/

5. Mubarak et al., EACL 2026 Nahw:
   - Arabic grammatical understanding/correction remains difficult even for strong models;
   - natural, high-quality data remains important.
   https://aclanthology.org/2026.eacl-long.296/

## Pre-registered design

The runtime gate MUST NOT read:
- Nahw target positions/corrections;
- human adjudication labels;
- prior ACCEPT/REJECT truth labels.

The gate operates on complete AraBART edit events.

Policy family:

### NARROW_DESTRUCTIVE
REJECT only highly specific destructive surface patterns:
- ta marbuta -> ha on otherwise local token replacement;
- alif maqsura -> ya on otherwise local token replacement.

All other non-accepted edits remain REVIEW rather than being over-rejected.

### EVENT_STRUCTURAL_TYPED
ACCEPT only when:
- event has equal source/output token count;
- primitive operations are substitution-only;
- every aligned token pair is a narrow structural edit:
  - exactly one nun inserted;
  - exactly one nun deleted;
  - or exactly one final alif appended;
- event_cost <= 0.60;
- no narrow destructive veto applies.

This naturally permits bounded multiword events where every token follows the same narrow structural pattern, e.g. noun/adjective accusative agreement.

### EVENT_STRUCTURAL_STRICT
Same, but:
- single-token events require event_cost <= 0.25;
- multiword events are accepted only when every token is a final-alif addition and there are at most two tokens.

## Explicit exclusions

Do not auto-accept in this gate:
- lexical substitutions;
- speech-act changes;
- tense/person reframing;
- hamza additions/removals or seat changes;
- word-boundary merges/splits;
- events with INS/DEL primitive operations;
- morphology-only consensus;
- GED-only confidence;
- full-sentence AraBART output.

## Success criterion

Development-only success:
- no accepted known HIGH/CRITICAL wrong event;
- no accepted partial event;
- observed accepted wrong = 0;
- incremental supported events beyond the current conservative local-edit path;
- all runtime decisions materialized before labels are read.

No sealed claim and no Phase 3.
