# ACAD_PASS — AT0-EN Execution Packet V2

Date: 2026-10-03 · Architecture: ENGLISH_FIRST 2.0.0

**SINGLE NEXT PHASE: AT0-EN — English Academic Transformation Feasibility Slice.**

This packet completely replaces the active bilingual AT0 instructions in V1 and V1.1. Retain those files as history. The current architect task creates documents only; execute this packet when the implementation task is assigned. HW1-EN and DR previews are not execution authorization.

## 1. Objective and bounded scope

Adopt the permanent architecture records, preserve the Arabic evidence, freeze active Arabic research, and implement a small English paragraph-transformation harness. Prove transactions, source protection, replay/rollback, provenance, length measurement, basic deterministic protections and experiment accounting. **Engineering PASS is not human-writing or scientific-quality PASS.**

Do not build the complete platform, a general NLP library, a full GEC verifier, a VoiceProfile service, a detector integration or document editing UI. Use the existing stack where suitable. Planning timebox: 1–2 actual working days in a ready environment; this is a stop-and-report bound, not a delivery guarantee or permission to weaken invariants.

## 2. Files to adopt and create

Default paths below are within the implementation repository. Respect an existing equivalent architecture directory if one is already established; record any path mapping. Preserve relative links when relocating this package.

| Path | Required content |
|---|---|
| `docs/architecture/ACAD_PASS_MASTER_PRODUCT_ARCHITECTURE.md` | Adopt supplied 2.0.0 baseline; update implementation state only with evidence |
| `docs/architecture/ACAD_PASS_LANGUAGE_EXTENSION_CONTRACT.md` | Adopt contract 1.0.0 |
| `docs/architecture/ACAD_PASS_ARABIC_RESEARCH_PRESERVATION_SNAPSHOT.md` | Adopt freeze; preserve immutable source history |
| `docs/architecture/ACAD_PASS_ARCHITECTURE_CHANGELOG.md` | Record adoption commit, not invented experimental progress |
| `docs/architecture/ACAD_PASS_EVIDENCE_MANIFEST.json` | Extend supplied preservation inventory with actual storage verification |
| `docs/architecture/evidence/2026-10-03/` | Supplied continuity and contract mirrors; retain all prior studies/packets nearby or remap links |
| `RESUME_HERE.md`, `ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md` | Append dated current-strategy pointers; retain old entries and hashes in snapshot |
| `phase2/academic_transform/at0_en/README.md` | Scope, exact reproducible offline and authorized-live commands, limits |
| `.../config.json`, `.../MODEL_MANIFEST.json` | Cases/arms/order/versions/budget; no secrets |
| `.../cases.jsonl`, `.../fixtures/`, `.../policies/` | 12 English cases, 30 fixtures, count/length/schema policies |
| `.../src/`, `.../tests/` | Thin Core/LanguageAdapter boundary, model transport, transactions, harness, meaningful tests |
| `.../results/<run_id>/` | Append-only requests/results/findings/manifests/report; respect repo data policy |

Model weights or restricted datasets belong in access-controlled artifact storage, not automatically in Git. Do not create a new branch of Arabic research. Do not discard another agent's uncommitted changes.

## 3. Stage A — Preservation and strategy adoption

Read the four master files, V2 memo and manifest. Reconcile the current repository against the supplied blob/commit anchors before modifying documentation. A changed HEAD is not itself a blocker: preserve its new records and identify whether it conflicts with the freeze. Do not reset to an old commit.

Carry out the snapshot's preservation procedure: inventory refs/locks/artifacts/runtime identities, preserve existing bytes without inspecting reserved text, and verify durable copies of critical V4.2 and proposer evidence. Capture missing/expired/access-restricted items explicitly. Record exact P3 punctuation and resource locks from existing metadata. Do not re-run a missing experiment to reconstruct evidence.

`PRESERVATION_GATE` requires adopted master records, byte-verified supplied continuity copies, exposure boundaries, a repository recovery point, and verified recoverability of the critical V4.2 result plus P1/P2_V2/P3 frozen outputs. The wider historical inventory may contain explicit pending items; do not call it a complete archive. If a critical item cannot be recovered within the timebox, return `PRESERVATION_BLOCKER`. Offline harness work may continue; do not start live generation while that gate is unresolved.

## 4. Stage B — Freeze twelve English cases

Write original synthetic English paragraphs, normally 3–6 sentences each, with plausible but explicitly synthetic scientific content. Use synthetic reference tokens such as `CIT_SYN_01`, not invented real publications or DOIs. No Arabic or mixed-language generation; technical symbols are allowed. All live cases use `ACADEMIC_REWRITE` to keep the comparison focused.

| Case | Main revision need | Protected challenge |
|---|---|---|
| EN01 | Repetitive introduction | Remove repeated wording without deleting a distinct claim |
| EN02 | Generic/promotional introduction | Improve specificity using only supplied facts; no new novelty claim |
| EN03 | Dense literature review | Distinguish multiple studies and their contrasting findings |
| EN04 | Citation-bearing argument | Keep each citation linked to the same supported claim |
| EN05 | Hedged claim | Preserve uncertainty, population restriction and negation |
| EN06 | Quantitative results | Preserve value/unit/group/time/baseline relationships |
| EN07 | Methodology | Preserve ordered steps, conditions, exclusions and reproducibility details |
| EN08 | Discussion | Association must not become causation or broader generalization |
| EN09 | Accurate but awkward technical prose | Preserve technical terms, symbols/equation identity and explanation |
| EN10 | Verbose AI-polished prose | Remove empty repetition without compression of required information |
| EN11 | Mechanically uniform sentences | Improve rhythm where useful without arbitrary variation |
| EN12 | Coherent but weak academic prose | Strengthen argument progression with justified local reorder/split/merge |

Each case records ID, `language=en`, source/raw hash, paragraph boundary, read-only adjacent context if needed, editorial brief, frozen content units, protected spans and known relations. Freeze cases/config/prompt/policy hashes before the first call. Synthetic text is known development material; do not call it human gold, an untouched holdout or representative academic usage.

## 5. Stage C — Models and two arms

Use **two already authorized, available models** with exact provider identifiers. Prefer independent families if available within existing access. A second temperature of the same model is not a second model. Do not buy new access or substitute a model midway. Record snapshot versus moving alias, observation timestamp, visible provider version, settings, limits and pricing date. No brand is mandated without verifying actual access and an approved cost cap in the execution environment.

Both arms receive the same source, context, editorial goal, scientific constraints and length policy:

- **DIRECT:** a strong direct academic-revision prompt and structured proposal response.
- **PLANNED:** one call for a short visible editorial plan using content IDs and allowed operations; a second call realizes it with the original source and constraints reattached. The plan is not proof of correctness. Do not request private chain-of-thought. A plan introducing an unsupported fact is failed/reviewed, not executed blindly.

Matrix: **12 cases ×2 models ×2 arms =48 slots**. DIRECT: 24 calls. PLANNED: 24 plan +24 realization calls. **Nominal maximum: 72 logical calls.** Failed plans skip realization and keep their slot as `PLAN_FAILED / REALIZATION_NOT_RUN`. No content regeneration, best-of-N, extra model judge, automated repair or live detector call.

Freeze a balanced order and seed before execution. Preserve all 48 slots including refusals, failures and NOT_RUN. If provider identity changes observably, stop before mixing versions; an opaque alias limits reproducibility and must be reported. One run per cell cannot estimate sampling variability.

## 6. Stage D — Thin transaction and adapter implementation

Implement language registration/capability reporting, source/paragraph/sentence units, transformation proposals, protected constraints and length measurement. Other LanguageAdapter methods may explicitly return `NOT_IMPLEMENTED`. Core uses contracts and cannot import English counters/prompts directly. Add a nonlinguistic stub pack with different feature/counting semantics to test the boundary; no Arabic prose or linguistic model is needed.

For every proposal: validate schema → check exact source version/hash/scope → store proposal/provenance → run checks → classify findings → stage a complete transaction or KEEP/REVIEW/REJECT. Do not apply partial structured responses. Source remains immutable. Protected fixture failures must prove **no write occurred**. Replay operates offline on stored operations. Rollback restores exact raw source.

Paragraph reorder in scope means sentence/content reorder within the one target paragraph. Moving whole paragraphs or writing adjacent context is outside this slice and must be rejected. Split/merge applies to sentences/content units within that paragraph, with many-to-many links and atomic review.

Known relation fixtures test assertions against a supplied relation graph or explicit mutation. Live language understanding is not established by those fixtures. Model-declared mappings are untrusted annotations. When actual semantic preservation cannot be determined, record `UNCERTAIN / REVIEW`, never a fabricated scientific PASS.

## 7. Thirty frozen engineering fixtures

Each row is a distinct fixture with explicit input, expected outcome and assertions; variants inside a row do not inflate the denominator. Additional tests for discovered code defects remain outside this fixed fixture count.

| ID | Required fixture |
|---|---|
| F01 | Canonical transaction identity recomputes; irrelevant serialization ordering does not change identity; content changes do |
| F02 | Identical outputs may deduplicate while retaining two distinct model/arm provenance events |
| F03 | Full valid rewrite then rollback restores exact source text/hash and retains audit events |
| F04 | Repeated deterministic replay produces identical output without network/model access |
| F05 | Incorrect source hash rejects without write |
| F06 | Stale source version rejects even if some visible text matches |
| F07 | Attempt to modify adjacent paragraph/read-only context rejects atomically |
| F08 | Multi-operation transaction with one invalid operation applies none of its operations |
| F09 | Protected quantity changed: known mutation detected; proposal cannot be approved |
| F10 | Same numbers swapped between groups: known relationship mismatch detected |
| F11 | Same values assigned to wrong time/baseline: known relationship mismatch detected |
| F12 | Unit or scale changed without authorized equivalent mapping: detected |
| F13 | Citation missing or reassigned to a different claim: known graph mismatch detected |
| F14 | Negation removed or scope reversed in known assertion: detected |
| F15 | Hedge/uncertainty strengthened in known assertion: detected |
| F16 | Comparison direction reversed while numbers stay fixed: detected |
| F17 | Association changed to causation in known assertion: detected |
| F18 | Valid within-paragraph content reorder preserves all content/citation links and supports rollback |
| F19 | Attempted cross-paragraph reorder rejects without source mutation |
| F20 | Valid sentence split retains one-to-many content and citation mapping |
| F21 | Valid sentence merge retains many-to-one mapping and scope |
| F22 | Sentence-count change is measured; abbreviation/decimal ambiguities are flagged rather than misrepresented as syntactic analysis |
| F23 | Length math: 100→85/115 inside soft band, 100→84/116 outside; zero/null cases; equal-tokenizer ratio; information-retention states; science failure cannot pass because length is in range |
| F24 | Protected technical term changed: detected; permissible unprotected stylistic variation does not trigger a blanket ban |
| F25 | Symbols/equations, combining marks and non-BMP character coordinates survive; UTF-8/code-point/UTF-16 maps and nonlinguistic direction metadata round-trip |
| F26 | No-op KEEP preserves source/hash, records outcome and gives zero length/sentence delta |
| F27 | Model refusal becomes an accounted failed/refused slot, not fabricated empty output |
| F28 | Malformed JSON/schema response is preserved as evidence and rejected without another model call |
| F29 | Truncated/partial transformation is not applied; raw response retained and text metrics null where undefined |
| F30 | Uncertain alignment, unknown language or unavailable required capability returns REVIEW/unsupported; it cannot silently use English defaults or certify quality |

Run all 30 offline before live generation. Apply schema/identity/source/scope/replay checks to all parseable live results as well. Atomic rollback on synthetic copies exercises engineering only; AT0 does not auto-apply revisions to user manuscripts.

## 8. Length and lightweight diagnostics

Freeze `LANG_EN` counter v1: count whitespace-delimited spans containing a Unicode letter or digit; a hyphenated span without spaces is one operational unit. This is a documented English engineering counter, not a universal linguistic word definition or a claim to match Word/Turnitin. Keep raw text and raw count. Exclude only predeclared citation/equation symbolic spans using independently mapped spans; retain ordinary numbers/technical terms. A missing/ambiguous protected span makes adjusted counts uncertain. Never let the generator choose exclusions.

Use a deterministic versioned English segmenter if available; otherwise call the measured entities `sentence_units` and flag known ambiguities. Count only the target paragraph, not prompt/context. Record:

`source_words`, `output_words`, raw counts, counter/status/version, signed/absolute/percent delta, `length_ratio`, within ±10% and ±15%, source/output sentence counts and lengths, `sentence_count_delta`, segmenter version, `token_ratio`, tokenizer identity, `information_unit_retention`, and reasons for unavailable values.

For token ratio, run the **same frozen tokenizer** on source and output paragraph text. Provider usage remains separate billable usage, not a substitute. If no matching tokenizer is available, record null rather than adding an unnecessary dependency or guessing from character counts.

Frozen content units have mutually exclusive preserved/changed/omitted/uncertain states. Report conservative confirmed retention `preserved / expected`, plus each count and the assessment method; unresolved units remain uncertain. New-information candidates are separate. For live outputs, mark unaudited semantic states uncertain. KEEP may inherit exact textual retention without claiming externally true science.

Count repeated openings and exact 3–5-word phrases, with witnesses and denominators. Do not penalize necessary technical repetition or use a banned-word list. Sentence-length variance is descriptive, not an objective. `syntactic_diversity`, voice similarity and human quality remain NOT_ASSESSED unless independently assessed under an appropriate later protocol. No perplexity/burstiness target.

## 9. Cost and execution controls

Before paid calls freeze `authorized_cost_ceiling`, `max_total_tokens`, per-call input/output limits, timeout, concurrency, model pricing snapshot and reservation accounting. Reuse existing authorization; do not seek it again. If a monetary cap/model access is absent, finish the offline work and return `BLOCKED_BUDGET`/`MODEL_ACCESS` with a concrete cost estimate; no paid calls are authorized by a blank config.

Reserve worst-case cost before dispatch and reconcile actual usage. At most one transport retry per logical request is allowed when the failure is unambiguously safe to retry; record every attempt and billable uncertainty. An ambiguous request must not be blindly replayed. Retries consume the same approved budget and do not increase the 72 logical-request ceiling. Do not retry malformed content, poor style, length violations or refusals to improve results.

Do not expose keys in logs/artifacts. No Arabic datasets—including C_F source text—are inputs to AT0-EN. Restrict data loading to the frozen synthetic allowlist. Preservation copying is separate and opaque; the generation harness has no Arabic data access.

## 10. Stop conditions and return gate

Stop new calls immediately for source corruption, scope escape, prohibited data access, hash/identity/replay failure, observable model-version drift or inability to guarantee the cost cap. Retain raw responses and remaining slot states. Local content failures are rejected/reviewed and counted; independent cases may continue while harness invariants hold.

Fix implementation defects offline with saved responses and versioned recalculation. Do not rerun the live generation matrix after a fix without returning for review. Return at the first hard blocker, at the 1–2-day timebox end, or when the bounded matrix is closed—whichever comes first.

Successful engineering closure requires: preservation gate satisfied for critical evidence; **30/30 fixtures**; source/scope/atomicity/replay/rollback checks pass; all 48 slots accounted; at most72 logical calls; traceable costs/failures; length metrics reproducible; and a cheap Language Portability Audit passed. A fully refused matrix can establish some harness behavior but is an experiment failure, not successful transformation feasibility. Report both dimensions separately.

## 11. Exact return package

Return `REPORT.md`, `PRESERVATION_REPORT.md`, model/case/prompt/policy manifests, file SHA-256 manifest, `slots.jsonl` (48 unique rows), raw response files, `transactions.jsonl`, `diagnostics.jsonl` (48 rows with null reasons as necessary), fixture results, portability audit, request/attempt/token/cost ledger and reproducible offline verification instructions. Include source/config versions, repository commit/diff and permitted artifact locations. Redact secrets, not failures.

Report:

```text
PRESERVATION_GATE: PASS | BLOCKED
HARNESS_STATUS: PASS | FAIL | NOT_RUN
EXPERIMENT_STATUS: COMPLETE | COMPLETE_WITH_FAILURES | PARTIAL | NOT_RUN
BLOCKER: NONE | PRESERVATION | MODEL_ACCESS | BUDGET | INVARIANT_FAILURE | OTHER
ENGINEERING_STATUS: <scope-specific result>
HUMAN_WRITING_STATUS: NOT_ASSESSED
SCIENTIFIC_FIDELITY_STATUS: NOT_ESTABLISHED; deterministic findings reported separately
VOICE_STATUS: NOT_ASSESSED
LENGTH_PRESERVATION_STATUS: MEASURED_DIAGNOSTIC | PARTIAL | NOT_MEASURED
DETECTOR_ROBUSTNESS_STATUS: NOT_RUN
DOCUMENT_FIDELITY_STATUS: NOT_RUN; paragraph transaction checks reported separately
COMMERCIAL_USEFULNESS_STATUS: NOT_ASSESSED
PRODUCTION_READINESS: NOT_ESTABLISHED
```

Include per-model/arm counts (12 cases per cell), failures, KEEP, protected findings, unresolved semantics, length distributions, plan overhead, actual cost and latency. Use explicit denominators and small-sample limits. No significance or generalization claims from 12 synthetic cases per cell. A fully accounted NOT_RUN matrix is not a completed experiment.

Finish with a short recommendation for HW1-EN preparation, based on observed feasibility and failure types. **Return to the architect before any HW1-EN or DR execution.** No further infrastructure branch, Arabic restart, reserved-data opening, V4.2 rerun, selector/consensus/judge training, voice fitting, DOCX/Word integration, paid launch or detector tuning is permitted within this packet.