# Phase 2 — Reversible Normalized Candidate View: Research Start

Date: 2026-09-28

Status: DEVELOPMENT ONLY. This gate does not auto-apply normalized edits, does not freeze a production policy, does not create a sealed benchmark, and does not start Phase 3.

## Why this gate exists

The previous Selective Surgical Gate established:
- operation-aware NoPnx1 retained 38 edits: 37 supported, 0 wrong, 1 partial;
- scientific stress preservation was 12/12 exact protected spans and 12/12 source unchanged;
- 98 NoPnx1 hazards suppressed specifically because of tokenizer [UNK] became tokenizable after an internal reversible diacritic/tatweel-stripped view.

Coverage remains the main bottleneck. The question is therefore whether normalized internal views can generate **review-only correction candidates** at currently abstained source locations while preserving exact original-source provenance.

## Fresh research check

1. Arabic diacritics can materially increase subword fragmentation and degrade downstream model performance, especially under heavier diacritization. This supports testing dediacritized internal model views while keeping original text authoritative.
   - Inoue et al., Findings of EACL 2026:
     https://aclanthology.org/2026.findings-eacl.22/

2. CAMeL Tools exposes explicit Arabic dediacritization and Unicode/Arabic normalization utilities. This confirms that reversible normalization is a standard Arabic NLP preprocessing operation, but some normalizers (e.g. Alef, Alef Maksura, Teh Marbuta normalization) are **lossy for our correction task** and therefore must not be used in this bounded gate.
   - Dediacritization:
     https://camel-tools.readthedocs.io/en/latest/api/utils/dediac.html
   - Normalization:
     https://camel-tools.readthedocs.io/en/latest/api/utils/normalize.html

3. CAMeL morphology's default normalization is intentionally broader (e.g. Alef variants, Alef Maksura, Teh Marbuta). That is useful for morphology lookup, but too destructive for a source-fidelity correction view. This prototype therefore removes only combining marks and tatweel and records an exact source-index map.
   - https://camel-tools.readthedocs.io/en/stable/api/morphology/analyzer.html

4. SWEET remains an edit-tagging model; edit-level candidate extraction is therefore preferable to replacing the source with a fully normalized/detokenized output.
   - https://aclanthology.org/2025.acl-long.875/

## Fixed design before execution

The prototype MUST:
- keep the original source string immutable;
- create a normalized model-view by removing only Unicode combining marks (Mn) and Arabic tatweel;
- keep a character-level normalized-index → original-source-index map;
- run official pinned NoPnx1 on the normalized model-view;
- inspect only word locations that were previously suppressed by TOKENIZER_UNK_WORD;
- emit candidate edits for REVIEW only;
- never write a normalized model output back into the source;
- classify mapping as SAFE_PROJECTABLE or UNSAFE_PROJECTABLE;
- preserve the exact removed characters and their source positions;
- quantify candidate generation and incremental target-recovery diagnostics without treating automated matching as linguistic adjudication.

## Pre-execution hypotheses

- H1: A meaningful subset of the 98 formerly-UNK locations will now receive non-K NoPnx candidates.
- H2: Some candidates will align with previously missed Nahw corrections, increasing potential coverage.
- H3: Not all candidates will be safely projectable back to exact source spans; unsafe projections must remain review-only metadata.
- H4: Dediacritization may expose useful model signal, but it can also erase grammatically meaningful case endings; no candidate may be auto-applied before adjudication.
- H5: If incremental useful coverage is small, the next better investment is a second Arabic GEC candidate generator rather than progressively broader normalization.

## Brainstorming carried into this gate

- normalized internal NoPnx view: PROTOTYPE
- exact source-offset round trip: INTEGRATE as an invariant
- auto-apply normalized candidates: REJECT
- Alef/Ya/Teh-Marbuta normalization in this gate: REJECT
- review-only normalized candidates: PROTOTYPE
- morphology validator after candidate generation: WATCH / NEXT PROTOTYPE
- AraBART/AraT5 second candidate source: WATCH / TEST if coverage gain is inadequate
- ensemble/voting: WATCH until two candidate sources are independently useful
