# ACAD_PASS — Master Product Architecture

Version: 2.0.0 · Decision date: 2026-10-03 · Strategy: ENGLISH_FIRST / MULTILINGUAL_READY_CORE

Status: architecture baseline authored; repository adoption, implementation and validation are separate events. This document records no new experiment. It supersedes the active bilingual roadmap in the 2026-10-02 study and V1.1 amendment, while retaining their non-conflicting reasoning and historical evidence.

## 1. Product and governing priorities

ACAD_PASS transforms academic prose into writing that qualified academics find natural, clear, coherent and appropriate to its discipline, while preserving the author's scientific content. English is the first Language Pack. English grammar, metrics and detector behavior are not the architecture. Arabic is a future first-class Language Pack; its active research is frozen, its evidence preserved.

The product supports abstracts, introductions, literature reviews, methods, results, discussions, conclusions, technical explanations, thesis prose and reviewer responses. Support is released by validated scope rather than claimed universally.

Decision priority: scientific meaning → semantic meaning → required information → academic quality → approximate length. Voice, detector behavior, document fidelity, cost and latency have separate measurements; none can compensate for a critical scientific error. Natural writing is not simulated with errors, noise, arbitrary synonyms or perplexity manipulation. GEC belongs in Verify/Repair, not at the center of transformation.

## 2. Authority and durable records

Read this file first, then [Language Extension Contract](ACAD_PASS_LANGUAGE_EXTENSION_CONTRACT.md), [Arabic Preservation Snapshot](ACAD_PASS_ARABIC_RESEARCH_PRESERVATION_SNAPSHOT.md), and [Architecture Changelog](ACAD_PASS_ARCHITECTURE_CHANGELOG.md). [Evidence Manifest](ACAD_PASS_EVIDENCE_MANIFEST.json) records machine-readable identities and preservation states. The manifest indexes evidence; it does not decide scientific validity.

The [English-first decision memo](ACAD_PASS_ENGLISH_FIRST_REBASELINE_V2.md) provides research and rationale. The [AT0-EN packet](ACAD_PASS_AT0_EN_EXECUTION_PACKET_V2.md) defines the sole next implementation phase when assigned to the implementation agent. Preview roadmaps do not authorize subsequent experiments. Original studies and closure reports remain historical records, not competing current instructions.

Every architecture change updates this file or the extension contract, the changelog, and the Arabic snapshot if reuse, exposure or portability changes. Do not erase superseded decisions. Each release records Core, adapter, policy, prompt, model and evidence versions.

## 3. System boundaries

| Responsibility | Shared CORE | LANG_EN now | Future LANG_AR |
|---|---|---|---|
| Document | Immutable source, structural IR, IDs, spans, versions, direction metadata | English segmentation and locale preferences | Arabic segmentation, clitics, mixed-direction interpretation |
| Scientific constraints | Claim/quantity/citation/equation schemas and orchestration | English extraction and language-aware validation | Arabic extraction and validation |
| Transform | Transaction protocol, proposal lifecycle, scope and permissions | English models, prompts, rhetorical conventions | Arabic models, prompts, discourse conventions |
| Linguistics | Capability/result envelopes; no compulsory English grammar tags | Tokenization, syntax, morphology, punctuation, style diagnostics | Arabic morphology, orthography, punctuation, discourse, stylometry |
| Length | Versioned policy schema and metric storage | English counter, sentence segmenter, empirically calibrated limits | Explicit Arabic counting conventions and local limits |
| Voice | Tenant isolation, profile lifecycle, provenance, retrieval permissions | English features and similarity calibration | Arabic features and separate calibration |
| Detectors | Frozen-output evaluation jobs and reporting schema | Current English protocols and eligibility rules | Then-current Arabic protocols and eligibility rules |
| Models | Provider transport, usage accounting, retries, routing interface | Language/task model selection and prompts | Independent Arabic model comparison |
| Documents/tools | DOCX package preservation, Word bridge, LaTeX structure, plugin permissions | English fidelity suites | RTL/bidi/mixed-script fidelity suites |
| Commercial | Projects, storage, review, API, billing, audit, SSO, institutions | English release scope and support | Arabic capability activation in the same product |

Core can represent a negation or a quantity relation without knowing how a language expresses it. Extracting or verifying that relation is language-dependent evidence. A universal-looking NLI model is not a universal proof service. A shared detector runner must not embed English word limits or thresholds. Scientific evidence matching may need language-aware retrieval even when DOI lookup and provenance storage are shared.

## 4. Document representation and transaction model

Maintain two linked layers:

1. **Lossless source/container layer:** original bytes or original package parts, document version, hash, paragraph/run IDs, tables, fields, citations, equations, footnotes, comments and tracked changes. Unsupported content stays opaque and protected.
2. **Analysis IR:** document/section/paragraph/span nodes, language and direction, content units, claims, quantity relations, citation links, equation identities and cross-references. Every extracted relation points to source spans and records method, confidence and uncertainty.

Core text spans use half-open Unicode code-point offsets over the exact versioned text. UTF-8 byte and UTF-16 code-unit coordinates require explicit conversion maps. A range cannot silently split a surrogate pair or grapheme cluster. Normalized text is a derived view with a reversible alignment map or an explicit unresolved mapping. No normalization overwrites original text. DOM positions, PDF coordinates, Word positions and model token indices are not interchangeable.

A transaction contains source/version hashes, permitted scope, input context hashes, proposal, language/adapter version, policy and model identity, verification findings and output hash. Define canonical serialization and its version; distinguish content identity from event identity. Identical outputs may be deduplicated without losing separate provenance events.

Use states `DRAFT → VERIFIED_FOR_REVIEW | REVIEW | REJECTED → ACCEPTED → APPLIED`, with `KEEP` as an explicit no-change outcome. Uncertain evidence cannot produce automatic scientific approval. All changes within a paragraph transaction are atomic. Split/merge/reorder uses many-to-many content links; positional independence does not establish semantic independence. Replay reconstructs stored operations without inference or network access. Rollback restores exact source content and retains the audit event.

## 5. Transformation and Verify/Repair pipeline

1. Capture source and supported document structure. Resolve explicit language and task scope; unsupported or mixed input is routed to review/preservation, not silently to English.
2. Obtain LanguageAdapter capabilities and language-specific constraints. Identify protected elements and uncertainty; distinguish pre-annotated fixtures from automatically extracted facts.
3. Form an editorial brief: intended improvement, allowable scope, retained content, voice preference, length policy. Read-only adjacent context cannot become writable scope.
4. Produce a direct proposal or a short explicit editorial plan followed by a proposal. Planning is an experimentally compared option, not a permanent superiority assumption. Plans contain editing operations, not private chain-of-thought.
5. Run structural checks, protected-element checks, relation checks, language quality checks and calibrated semantic/scientific review. Preserve disagreements and unavailable checks.
6. Return a proposed revision, clear findings, and KEEP/REVIEW options. Future localized repair is bounded and separately evaluated; do not run an open-ended generate/judge/repair loop.
7. Apply an accepted transaction atomically; export only a supported document subset and verify round-trip fidelity.

The hierarchy of evidence is explicit: byte/structure checks are deterministic; known synthetic relation checks test machinery; learned relation extraction and semantic judgments remain fallible; qualified human assessment is required for academic quality and scientific validation. Neither generator self-confidence nor source-token preservation proves unchanged meaning.

## 6. LanguageAdapter and portability

Adapters expose stable outcomes through the [extension contract](ACAD_PASS_LANGUAGE_EXTENSION_CONTRACT.md). Core selects adapters from a registry and negotiates capabilities. It must not import a language-specific tokenizer or prompt. Detection can return multiple spans or `UNKNOWN`; it is not a forced English default.

AT0-EN implements only the thin required slice. Unused interfaces are declared `NOT_IMPLEMENTED`, not filled with misleading pass-through success. Morphology or a specific grammar formalism is not required for all languages. Required checks unavailable for a requested operation cause review or a blocked capability.

Run `LANGUAGE_PORTABILITY_AUDIT` at AT0 closure, benchmark/adapter schema freeze, long-document/DOCX architecture freeze, public API freeze and before a language port. Cheap contract and synthetic Unicode tests are allowed during English work; Arabic linguistic generation, evaluation and reserved-data access remain frozen.

## 7. LengthPreservationPolicy

The Core stores a versioned policy; the active Language Pack defines counting and calibrated ranges.

| Mode | Intended behavior |
|---|---|
| PROOFREAD | Very small changes; no rhetorical expansion |
| CLARITY | Minor variation needed for clearer expression |
| ACADEMIC_REWRITE | Similar information volume; initial experimental soft band 0.85–1.15 of source words |
| VOICE_ADAPT | Similar required information; author style never overrides science |
| EXPAND / CONDENSE | Future explicit modes with a separately agreed scope |

The band is a starting hypothesis, not a literature-proven optimum or a universal hard gate. Out-of-band text receives `LENGTH_REVIEW`; no automatic truncation, padding or repeated generation. Determine English distributions in HW1 by section, domain and edit need before adopting product thresholds.

Record `source_words`, `output_words`, raw counts, counter version, `length_ratio`, signed/absolute change, `sentence_count_delta`, segmenter version, `token_ratio`, and `information_unit_retention`. Token ratio counts source and output paragraph text with the same named/versioned tokenizer; provider-billed request tokens are separate and include other material. If a comparable tokenizer is unavailable, token ratio is null with a reason. Empty source and failed outputs produce null ratios, not artificial zeros.

Information-unit retention uses frozen source units, not new units selected by the generator. Each unit is preserved/changed/omitted/uncertain with judgment provenance; additions are separate. Uncertain units remain in the denominator and are reported. A length ratio cannot establish information retention.

## 8. Human-writing and VoiceProfile tracks

`HW0` defines authentic provenance, signals and rubric; keep its initial scope within HW1 preparation. `HW1-EN` compares original/direct/ACAD_PASS/human revision on authentic permitted prose. `HW2` tests paragraph discourse; `HW3` voice; `HW4` section/document consistency; `HW5` cross-domain and EAL generalization. These tracks overlap where evidence permits; infrastructure must not postpone the first real human preference test.

Human evaluation scores naturalness, academic appropriateness, clarity, coherence, argument flow, rhythm, lexical choices, formulaic phrasing and verbosity separately from scientific/semantic fidelity, quantities and citations. LLM judges are auxiliary calibrated instruments, not substitutes for qualified humans. There is no single `human_score` release oracle.

`VoiceProfile` contains authorized corpus provenance, author/tenant identity, language and domain, feature schema/version, uncertainty, sample adequacy, retrieval permissions and revocation rules. Use author-disjoint/content-separated evaluation to distinguish topic copying from voice. STYLE RETRIEVAL is isolated from SCIENTIFIC EVIDENCE RETRIEVAL by storage, permissions and prompt channels. Style exemplars cannot supply new facts. Do not automatically train on generated outputs or reuse another tenant's style. Voice remains unvalidated until the author and blinded reviewers assess it.

## 9. Detector Robustness

DR evaluates already frozen outputs. Record detector identity, available version, observation date, model-release information, language, document eligibility, scoring denominator, report hash and uncertainty. An opaque vendor version is recorded as opaque, not invented.

Use Turnitin, another available commercial detector, a reproducible open detector and stylometric diagnostics where permitted and appropriate. Score genuine human, weak human, AI-generated, AI-polished, professionally edited and human-edited AI classes separately, including EAL. Detector disagreement and update drift are findings. A lower score is not evidence of scientific fidelity or authorship. No detector result feeds a rewrite/retry loop, and no product claim guarantees evasion.

## 10. Source intelligence and plugin architecture

The plugin contract declares capabilities, inputs/outputs, language support, evidence requirements, permissions, network/storage access, cost limits, idempotency and failure behavior. Plugins propose changes through Core transactions; they cannot silently overwrite source. Treat retrieved text as evidence/data rather than executable instructions.

Source services distinguish reference existence, DOI metadata correctness, claim support, exact supporting passage, unsupported claims, suggested sources, retractions and citation drift. A DOI match does not prove claim support. Missing full text is `UNVERIFIED`; never invent a supporting quote or reference. Store provider/time/source version and access rights. Source discovery does not insert a citation without review.

Document services preserve unsupported objects, field relationships and identity. DOCX import/export precedes deep Word integration. Support tracked changes/comments/tables/equations/footnotes/citations by tested scope. LaTeX preserves source ranges/macros and protects unsupported syntax; conversion to generic text is not a lossless round trip. Source intelligence, document tools and reference-manager integrations remain addable without changing transformation semantics.

## 11. Commercial platform and roadmap

`AT0-EN → HW1-EN / Research Beta → English Academic Beta → supported DOCX → Paid SaaS → Word Add-in → public API → Institutional integrations`.

An internal API boundary exists early; public API packaging comes after measured user value and stable contracts. Paid SaaS requires protected manuscript storage, tenant isolation, usage/cost controls, retention/deletion, review UX and observed usefulness. Word adds faithful in-document review. Institutions add SSO, policy controls, audit/export, reference managers and journal workflows; private deployment is conditional on demand.

Insert `LANG_AR PORT` after a scoped English maturity gate and an explicit decision to resume Arabic. English maturity means a versioned supported scope with confirmed human-writing benefit, scientific/semantic safety evidence, document fidelity, stable operations and real user usefulness. It does not require perfection across every discipline or completion of every institutional integration. Language support is capability-scoped, not a blanket multilingual marketing claim.

## 12. Current state and release reporting

As of this architecture record: four master documents and the next packet are authored; repository promotion and AT0-EN execution are not reported complete. Existing Arabic engineering/evaluation closures remain Arabic development evidence. No English quality claim follows from them. Remote evidence inventory does not equal an independently verified backup.

| Required status | Current English state | Required independent evidence |
|---|---|---|
| ENGINEERING_STATUS | NOT_RUN for AT0-EN | Transaction/harness/portability closure |
| HUMAN_WRITING_STATUS | NOT_ASSESSED | Blinded qualified human preference/rubric |
| SCIENTIFIC_FIDELITY_STATUS | NOT_ASSESSED | Claim, quantity, citation and semantic assessment |
| VOICE_STATUS | NOT_ASSESSED | Authorized author corpus and isolated voice evaluation |
| LENGTH_PRESERVATION_STATUS | POLICY_DEFINED / NOT_MEASURED | Versioned counts and information retention |
| DETECTOR_ROBUSTNESS_STATUS | NOT_RUN | Frozen-output DR report |
| DOCUMENT_FIDELITY_STATUS | NOT_RUN | Supported-format round-trip fixtures and user documents |
| COMMERCIAL_USEFULNESS_STATUS | NOT_ASSESSED | User acceptance, revision burden, repeat use and viable cost |

Each status is indexed by language, release, dataset and scope. Semantic fidelity, cost and latency are additional explicit report fields. A PASS on one row never supplies another. Thresholds for later release experiments must be preregistered before their evaluation data are opened.

## 13. Principal risks and controls

The largest risks are fluent scientific drift, insufficient advantage over a strong direct model, and English assumptions entering Core. Control them with retained source and relationships, blinded comparisons, adapter contracts and portability audits. Further risks are lost/expired Arabic artifacts, reused contaminated data, overconfident detectors, hidden document loss, style leakage, and infrastructure expansion that delays human-quality evidence. Preservation states, exposure manifests, frozen DR outputs, scope-specific export tests, tenant isolation and bounded phase packets address these risks.

The next return point is AT0-EN closure or its first hard blocker/timebox end. No automatic HW1, DR, Arabic restart or paid product release follows that engineering gate.